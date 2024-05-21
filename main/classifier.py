import common_alternates_db
import input_standardization
import load_standards
import re
import config

class Classifier:
    filters = []
    address_list = []

    def __init__(self):
        self.address_list = input_standardization.generateStandardizedInput(config.DATASET_PATH, config.WORKING_DATASET)
        self.standard_df = load_standards.load_standards_from_config(config.STANDARDS_PATH)


    def _parseUserInput(userIn: str)->str:
        return re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", userIn.upper())
    

    

clf = Classifier()
print(clf.address_list)

