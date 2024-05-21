import common_alternates_db
import re
from fuzzy_distance import calc_fuzzy_dist

class InvalidFilter(Exception):
    pass


class Filter:
    ruleSet = {}
    appliesTo = None #Enumerable: C S or A

    def __init__(self, filterRule={}):
        self.ruleSet = filterRule #expects a hashmap
        self.appliesTo = None

    def _parseUserInput(self, userIn: str)->str:
        return re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", userIn.upper()).strip()


    def applyFilter(rowInput: str):
        return (None, 0)
    

    def getKeys(self):
        return self.ruleSet.keys()


class userFilter(Filter):
    def __init__(self, filterRule, appliesTo):
        self.ruleSet = filterRule
        self.appliesTo = appliesTo


    def applyFilter(self, rowInput: str):
        if self.ruleSet.__contains__(self._parseUserInput(rowInput)):
            return (self.ruleSet[rowInput], 100)
        else:
            return (None, 0) 


class exactFilter(Filter):
    def __init__(self, appliesTo):
        self.appliesTo = appliesTo
        if self.appliesTo == 'C':
            self.ruleSet = common_alternates_db.COMMON_ALTERNATES
        elif self.appliesTo == 'S':
            self.ruleSet = {} #TODO
        elif self.appliesTo == 'A':
            self.ruleSet = {} #TODO
        else:
            raise Exception("Invalid Filter")


    def applyFilter(self, rowInput: str):
        parsedOutput = self._parseUserInput(rowInput)
        if self.ruleSet.__contains__(parsedOutput):
            return (self.ruleSet[parsedOutput], 100)
        else:
            return (None, 0)
        
class fuzzyFilter(Filter):
    def __init__(self, appliesTo, order=1):
        self.appliesTo = appliesTo
        self.order = order
        if self.appliesTo == 'C':
            self.ruleSet = common_alternates_db.COMMON_ALTERNATES
        elif self.appliesTo == 'S':
            self.ruleSet = {} #TODO
        elif self.appliesTo == 'A':
            self.ruleSet = {} #TODO
        else:
            raise Exception("Invalid Filter")
        

    def applyFilter(self, rowInput: str):
        hits = []
        for common_spelling in list(self.ruleSet.keys()):
            dist = calc_fuzzy_dist(common_spelling, self._parseUserInput(rowInput))
            if dist <= self.order:
                hits.append((self.ruleSet[common_spelling], dist))
        
        return hits, 50
    
class ProcessingFilter(Filter):
    pass

        



        
    

    

