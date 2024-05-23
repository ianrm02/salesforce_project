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

    def __init__(self):
        #TODO check for valid loading of files, throw errors if not
        self.address_list = input_standardization.generateStandardizedInput(config.DATASET_PATH, config.WORKING_DATASET)
        self.standard_country_df = self._load_iso_standard()

        #Filter System:
        userCountry_f   = userFilter(  filterRule={}, appliesTo='C', name="user_ctry")
        exactCountry_f  = exactFilter(                appliesTo='C', name="exct_ctry")
        fuzzyCountry_f  = fuzzyFilter(                appliesTo='C', order=2, name="fzzy_ctry")
        userState_f     = userFilter(  filterRule={}, appliesTo='S', name="user_stte")
        exactState_f    = exactFilter(                appliesTo='S', name="exct_stte")
        fuzzyState_f    = fuzzyFilter(                appliesTo='S', order=2, name="fzzy_stte")
        userAddress_f   = userFilter(  filterRule={}, appliesTo='A', name="user_addr")
        proccessing_f   = ProcessingFilter(name="proc_mgic")

        self.filters = [
            userCountry_f, exactCountry_f, fuzzyCountry_f, userState_f, exactState_f, fuzzyState_f, userAddress_f, proccessing_f
        ]

    #currently only handles main/ISO3166_1.csv
    def _load_iso_standard(self, iso_standard_file=config.ISO_3166_1_PATH):
        standard_df = pd.read_csv(iso_standard_file, keep_default_na=False)
        return standard_df
    

    #TODO Might be obsolete, but leaving in just in case. Test for later.
    def _parseUserInput(userIn: str)->str:
        return re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", userIn.upper())

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

        #num_filters = 0
        for filter in self.filters:
            if confidence == 100:
                break
            #num_filters += 1
            (new_probable_mapping, new_confidence) = filter.applyFilter(rowInput)
            if new_confidence == 30:
                print(filter.getName(), rowInput, new_probable_mapping)
            if new_confidence > confidence:
                probable_mapping = new_probable_mapping
                confidence = new_confidence
        
        return probable_mapping, confidence
    
    
    def batch_process(self, batch):
        batch_results = []
        for item in batch:
            whole_addr = f"{item[0]} | {item[1]} | {item[2]}"
            probable_match, confidence = self.applyFilterStack(item)
            print(f"{whole_addr} mapped to {probable_match} with {confidence}% confidence")
