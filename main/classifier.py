import input_standardization
import load_standards
import re
import config
from filter import *

class Classifier:
    filters = []
    address_list = []
    standard_country_df = None

    def __init__(self):
        #TODO check for valid loading of files, throw errors if not
        self.address_list = input_standardization.generateStandardizedInput(config.DATASET_PATH, config.WORKING_DATASET)
        self.standard_country_df = load_standards.load_standards_from_config(config.STANDARDS_PATH)

        #Filter System:
        userCountry_f = userFilter(filterRule={}, appliesTo='C')
        exactCountry_f = exactFilter(appliesTo='C')
        fuzzyCountry_f = fuzzyFilter(appliesTo='C', order=1)
        userState_f = userFilter(filterRule={}, appliesTo='S')
        exactState_f = exactFilter(appliesTo='S')
        fuzzyState_f = fuzzyFilter(appliesTo='S', order=1)
        userAddress_f = userFilter(filterRule={}, appliesTo='A')
        proccessing_f = ProcessingFilter()

        self.filters = [
            userCountry_f, exactCountry_f, fuzzyCountry_f, userState_f, exactState_f, fuzzyState_f, userAddress_f, proccessing_f
        ]


    #TODO Might be obsolete, but leaving in just in case. Test for later.
    def _parseUserInput(userIn: str)->str:
        return re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", userIn.upper())


    def applyFilterStack(self, rowInput:str):
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
            7. Processing Filter
            ----- UI Break: Address
            ----- UI Confirm Screen
        """
        probable_country = None
        confidence = 0

        num_filters = 0
        for filter in self.filters:
            if confidence == 100:
                break
            num_filters += 1
            #print(type(filter))
            (probable_country, confidence) = filter.applyFilter(rowInput)
        
        print(f"{rowInput.strip()} mapped to {probable_country} with {confidence}% confidence (through {num_filters} filters).")

        return probable_country, confidence


def testClassifierInit():
    pass


def testClassifier():
    clf = Classifier()
    sample_inputs = [
        "France",
        "Colombia",
        "USA",
        "U.S.A.",
        "   Argentina",
        "Intentional Failure",
    ]

    print(f"")
    print(f"Testing simple inputs on the newly implemented Classifier.applyFilterStack() method...")
    print(f"")

    for sample in sample_inputs:
        probable_country, confidence = clf.applyFilterStack(sample)

    print(f"Done.")


testClassifier()

