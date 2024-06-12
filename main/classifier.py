import input_standardization
import config
from filter import *

import re
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import normalize
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import TruncatedSVD


class Classifier:
    filters = []
    address_list = []
    standard_country_df = pd.DataFrame()

    def __init__(self):
        #TODO check for valid loading of files, throw errors if not
        self.address_list = input_standardization.generateStandardizedInput(config.DATASET_PATH, config.WORKING_DATASET)
        self.iso_standard_df = self._load_iso_standard()
        self.filterOrder = config.FILTER_ORDER
        self.countries_that_require_states = config.STATED_COUNTRIES
        self.results = {}
        self.clustering_to_place = []
        self.clusters = []
        self.rep_cou = set()

        #Filter System:
        userCountry_f   = UserFilter(  filterRule={}, appliesTo='C', name="user_ctry")
        exactCountry_f  = CountryExactFilter(                appliesTo='C', name="exct_ctry")
        fuzzyCountry_f  = FuzzyFilter(                appliesTo='C', order=2, name="fzzy_ctry")
        userState_f     = UserFilter(  filterRule={}, appliesTo='S', name="user_stte")
        exactState_f    = StateExactFilter(                appliesTo='S', name="exct_stte")
        fuzzyState_f    = FuzzyFilter(                appliesTo='S', order=1, name="fzzy_stte") #Order of 1 so that not every alpha 2 maps to every other alpha 2 within 2 order.
        userAddress_f   = UserFilter(  filterRule={}, appliesTo='A', name="user_addr")
        #proccessing_f   = ProcessingFilter(name="proc_mgic", appliesTo='O')

        self.filters = [
            userCountry_f, exactCountry_f, fuzzyCountry_f, userState_f, exactState_f, fuzzyState_f, userAddress_f, #proccessing_f
        ]

    #currently only handles main/ISO3166_1.csv
    def _load_iso_standard(self, iso_standard_file=config.ISO_3166_1_PATH):
        standard_df = pd.read_csv(iso_standard_file, keep_default_na=False)
        return standard_df
    

    def applyFilterStack(self, rowInput):
        #If the system ever returns max confidence, it should break out of the filter stack for that specific input
        probable_mapping = None
        confidence = 0

        for filter in self.filters:
            if confidence == config.MAX_CONFIDENCE:
                break

            (new_probable_mapping, new_confidence) = filter.applyFilter(rowInput)
            
            if new_confidence > confidence:
                probable_mapping = new_probable_mapping
                confidence = new_confidence
        
        return probable_mapping, confidence
    
    
    def applyFilterSubset(self, rowInput, subset: chr):
        filter_subset = [filter for filter in self.filters if filter.appliesTo == subset]

        probable_mapping = None
        confidence = 0

        for filter in filter_subset:
            if confidence == config.MAX_CONFIDENCE:
                break
                
            new_probable_mapping, new_confidence = filter.applyFilter(rowInput)
            if new_confidence > confidence:
                probable_mapping = new_probable_mapping
                confidence = new_confidence
            
        return probable_mapping, confidence
    

    def _state_selection_override(self, item, country):
        state_filter = [filter for filter in self.filters if filter._name == "exct_stte"][0]
        probable_state, _ = state_filter.applyFilter(item, identifiedCountry=True, probableCountry=country)
        return probable_state
    
    def getClusters(self):
        return self.clusters

    
    def batch_process(self, batch, stepThroughRuntime=False):
        for stage in self.filterOrder: #For each stage: Country, State, Address, Processing
            for item in batch:         #For each address in the batch
                foundCountry, foundState = False, False
                whole_addr = f"{str(item[1]).strip()} {str(item[2]).strip()} {str(item[3]).strip()}" #clean the whole address to use as a key
                if whole_addr not in self.results: self.results[whole_addr] = [None, 0, None, 0, item[0], item[1], item[2], item[3]] #if the key is not already in the results db, create it and initialize its values to "", 0, "", 0
                

                # CONTROL FLOW LOGIC TO PREVENT RECOMPUTING MAPPINGS IN LATER FILTERING STAGES
                if self.results[whole_addr][1] + self.results[whole_addr][1] == 2 * config.MAX_CONFIDENCE: #If we have a max confidence placement already, don't waste time computing repeat information that is (likely) less confident
                    continue
                if stage == "S" and self.results[whole_addr][1] == config.MAX_CONFIDENCE: #should logically never occur, but good to implement logic to prevent overusing compute
                    continue
                if stage == "C" and self.results[whole_addr][3] == config.MAX_CONFIDENCE: #if we have already confidently placed a state (e.g. from _state_selection_override with a good result), don't waste time computing what we already know
                    continue

                #If we have gotten to here, we are assuming that we have low confidence for our mapping for this stage of the address
                probable_match, confidence = self.applyFilterSubset(item, stage) #apply the subset of filters to that address, unpacking results to probable_match and confidence        
                
                if stage == 'C': 
                    relevant_text = item[3]
                    self.results[whole_addr][0] = probable_match  #If in country stage, change probable_country_mapping
                    self.results[whole_addr][1] = confidence      #                        and country_confidence
                    if confidence == config.MAX_CONFIDENCE: #If confidence is MAX
                        foundCountry = True
                        if probable_match in self.countries_that_require_states: #if found country requires a state
                            possible_state = self._state_selection_override(item, probable_match) #run override
                            if possible_state is not None: 
                                self.results[whole_addr][2] = possible_state  
                                self.results[whole_addr][3] = config.MAX_CONFIDENCE #an exact state match after a confidenct country mapping should result in a confident state

                elif stage == 'S':
                    relevant_text = item[2]
                    if confidence > self.results[whole_addr][3]:      
                        self.results[whole_addr][2] = probable_match      #If in state stage, change probable_state_mapping
                        self.results[whole_addr][3] = confidence          #                   and state_confidence as long as they are higher confidence than existing predictions
                    if confidence == config.MAX_CONFIDENCE:
                        #TODO if it found an exact match for the state, give it a mapping to that states country with some confidence (50?)
                        # This is not really doable without a list of all addresses in a given state to validate if it is truly in that state or if it's a typo
                        # Our client commented that Salesforce has this capability internally.
                        foundState = True
                        pass


                elif stage == 'A':
                    relevant_text = whole_addr
                    #TODO [BLOCKER] how does the state or country get decided by these changes internally? I need some sample user rules I think at this point to progress


            if stage == 'O': 
                self.rep_cou = set()

                for item in batch:
                    whole_addr = f"{str(item[1]).strip()} {str(item[2]).strip()} {str(item[3]).strip()}" #clean the whole address to use as a key
                    if self.results[whole_addr][1] == config.MAX_CONFIDENCE:
                        self.rep_cou.add(self.results[whole_addr][0])

                    if self.results[whole_addr][1] == 0: #If we have no confidence in this mapping, add it to the list of addressess that need to be send to the processing filter.
                        self.clustering_to_place.append(whole_addr)
                
                
            if stepThroughRuntime == True:
                print(f"{stage} Stage Completed...")
                print(f"[ENTER] to continue ")
                _ = input("")


    def runKMeansModel(self):
        print("[RUNNING K MEANS]")
        X = self.clustering_to_place
        num_clusters = min(len(list(self.rep_cou)) + 5, 25) #arbitrarily set amount of clusters, having it be +5 of the countries represented with max confidence until we find a more adaptive way to determine that metric

        print(self.clustering_to_place)
        vct = TfidfVectorizer(max_features=10)
        X = vct.fit_transform(self.clustering_to_place)

        #SVD dimensionality reduction? y/n?

        try: #realistically a ml model should NOT be a cluster so structuring it here in the code is more a remnant of the fact that we arent hosting a model on a 3rd party service. 
            #This is also definetely hurting the runtime of the processing stage of our algorithm
            #model = KMeans(n_clusters=num_clusters)
            model = DBSCAN(eps=1.0, min_samples=5) #eps is distance to consider same cluster, min_samples is minimum addresses for a cluster to form
            tmp_clusters = model.fit_predict(X)


            #cluster 0 is consistently one of the less "dense" and less accurate clusters, 
            #look into why
            
            for cluster_id in range(1, model.n_clusters):
                sample_stack = []
                cluster_samples = [self.clustering_to_place[i] for i, cluster in enumerate(tmp_clusters) if cluster == cluster_id]
                for sample in cluster_samples:
                    sample_stack.append(sample)
                self.clusters.append(sample_stack)


            #convert all the 1-element clusters into a merged "unmatchable" cluster
            unmatchable = []
            for clust in self.clusters:
                if len(clust) == 0:
                    self.clusters.remove(clust)
                elif len(clust) == 1:
                    unmatchable.append(clust[0])
                    self.clusters.remove(clust)
            self.clusters.append(unmatchable)
                    
        except:
            print("Processing filter error")
                
    
    def get_results(self):
        return self.results
                
