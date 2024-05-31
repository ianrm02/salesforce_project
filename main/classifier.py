import input_standardization
import config
from filter import *

import common_country_alternates

import re
import pandas as pd
import numpy as np

import os

class Classifier:
    filters = []
    address_list = []
    standard_country_df = pd.DataFrame()

    # Format:
    # Old String | New String | Confidence | Num Occurences

    def __init__(self):
        #TODO check for valid loading of files, throw errors if not
        self.address_list = input_standardization.generateStandardizedInput(config.DATASET_PATH, config.WORKING_DATASET)
        self.iso_standard_df = self._load_iso_standard()
        self.filterOrder = config.FILTER_ORDER
        self.results = {}

        #Filter System:
        userCountry_f   = UserFilter(  filterRule={}, appliesTo='C', name="user_ctry")
        exactCountry_f  = ExactFilter(                appliesTo='C', name="exct_ctry")
        fuzzyCountry_f  = FuzzyFilter(                appliesTo='C', order=2, name="fzzy_ctry")
        userState_f     = UserFilter(  filterRule={}, appliesTo='S', name="user_stte")
        exactState_f    = ExactFilter(                appliesTo='S', name="exct_stte")
        fuzzyState_f    = FuzzyFilter(                appliesTo='S', order=2, name="fzzy_stte")
        userAddress_f   = UserFilter(  filterRule={}, appliesTo='A', name="user_addr")
        proccessing_f   = ProcessingFilter(name="proc_mgic", appliesTo='O')

        self.filters = [
            userCountry_f, exactCountry_f, fuzzyCountry_f, userState_f, exactState_f, fuzzyState_f, userAddress_f, proccessing_f
        ]

    #currently only handles main/ISO3166_1.csv
    def _load_iso_standard(self, iso_standard_file=config.ISO_3166_1_PATH):
        standard_df = pd.read_csv(iso_standard_file, keep_default_na=False)
        return standard_df
    

    def applyFilterStack(self, rowInput):
        #If the system ever returns 100 confidence, it should break out of the filter stack for that specific input
        """
            Operational Order:
            1. User Country Filter
            2. Exact Country Filter
            3. Fuzzy Country Filter
            ----- UI Break: Country
            4. User State Filter
            5. Exact State Filter
            6. Fuzzy State Filter.
            ----- UI Break: State
            7. User Address Filter
            8. Processing Filter
            ----- UI Break: Address
            ----- UI Confirm Screen
        """
        probable_mapping = None
        confidence = 0

        for filter in self.filters:
            if confidence == 100:
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
            if confidence == 100:
                break
            new_probable_mapping, new_confidence = filter.applyFilter(rowInput)
            if new_confidence > confidence:
                probable_mapping = new_probable_mapping
                confidence = new_confidence
            
        return probable_mapping, confidence

    
    def batch_process(self, batch, stepThroughRuntime=False):
        for stage in self.filterOrder: #For each stage: Country, State, Address, Processing
            for item in batch:         #For each address in the batch
                whole_addr = f"{str(item[0]).strip()} {str(item[1]).strip()} {str(item[2]).strip()}" #clean the whole address to use as a key
                if whole_addr not in self.results: self.results[whole_addr] = ["", 0, "", 0, item[0], item[1], item[2]] #if the key is not already in the results db, create it and initialize its values to "", 0, "", 0
                probable_match, confidence = self.applyFilterSubset(item, stage) #apply the subset of filters to that address, apply results to probable_match and confidence
                if stage == 'C': 
                    relevant_text = item[2]
                    self.results[whole_addr][0] = probable_match  #If in country stage, change probable_country_mapping
                    self.results[whole_addr][1] = confidence      #                        and country_confidence
                elif stage == 'S':
                    relevant_text = item[1]
                    self.results[whole_addr][2] = probable_match  #If in state stage, change probable_state_mapping
                    self.results[whole_addr][3] = confidence      #                      and state_confidence
                elif stage == 'A':
                    relevant_text = whole_addr
                    #TODO [BLOCKER] how does the state or country get decided by these changes internally? I need some sample user rules I think at this point to progress
                elif stage == 'O':
                    relevant_text = f"{item[0]} {item[1]} {item[2]}"
                    #TODO Once processing filter is created, decide how its output will update the results for that address

                print(f"{item[0]} | {item[1]} | {item[2]}")
                print(f"{relevant_text} mapped to {probable_match} with {confidence}% confidence in the {stage} stage")
            print(" ")
            
            #Results stored intermediately as a dictionary of [address]: [country map, contry conf, state map, state conf, adr line, country, state]

            print(f"{stage} Stage Completed...")
            if stepThroughRuntime == True:
                _ = input("")

    
    def get_results(self):
        return self.results
                
