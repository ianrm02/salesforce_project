import input_standardization
import load_standards
import re
import config
from filter import *

class Classifier:
    filters = []
    address_list = []
    standard_df = None

    def __init__(self):
        self.address_list = input_standardization.generateStandardizedInput(config.DATASET_PATH, config.WORKING_DATASET)
        self.standard_df = load_standards.load_standards_from_config(config.STANDARDS_PATH)

        #Filter System:
        userCountry_f = userCountryFilter()
        exactCountry_f = countryExactFilter()

        self.filters = [
            userCountry_f, exactCountry_f
        ]

    #TODO Might be obsolete, but leaving in just in case. Test for later.
    def _parseUserInput(userIn: str)->str:
        return re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", userIn.upper())
    
    def applyFilterStack(self, rowInput:str):
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
        """
        pass