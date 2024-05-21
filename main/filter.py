import common_alternates_db
import re

class Filter:
    ruleSet = []
    appliesTo = None #Enumerable: C S or A

    def __init__(self, filterRule):
        self.ruleSet = filterRule #expects a hashmap
        self.appliesTo = None

    def _parseUserInput(self, userIn: str)->str:
        return re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", userIn.upper())


    def applyFilter(rowInput: str):
        return (None, 0)
    

class userCountryFilter(Filter):
    def __init__(self, filterRule):
        self.ruleSet = filterRule
        self.appliesTo = 'C'


    def applyFilter(self, rowInput: str):
        if self.ruleSet.__contains__(self._parseUserInput(rowInput)):
            return (self.ruleSet[rowInput], 100)
        else:
            return (None, 0)
        
    def loadUserFilter(self, userCountryFilters):
        pass
        

class countryExactFilter(Filter):
    def __init__(self):
        self.ruleSet = common_alternates_db.COMMON_ALTERNATES
        self.appliesTo = 'C'
    

    def applyFilter(self, rowInput: str):
        parsedOutput = self._parseUserInput(rowInput)
        if self.ruleSet.__contains__(parsedOutput):
            return (self.ruleSet[parsedOutput], 100)
        else:
            return (None, 0)
    

    

