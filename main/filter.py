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
        #TODO still does not yet account for the user input being a database row. Can't work on this till we connect the sample DB to the classifier
        
        text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", userIn.upper()).strip()
        return text 


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
    def __init__(self, appliesTo, order=2):
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
        #TODO turn order confidences into a config variable
        order_confidences = [90, 80, 70, 50] #ie 1 order is 90% confidence
        for common_spelling in list(self.ruleSet.keys()):
            dist = calc_fuzzy_dist(common_spelling, self._parseUserInput(rowInput))
            if dist <= self.order:
                hits.append((self.ruleSet[common_spelling], dist))
        
        hits = list(set(hits)) #to remove duplicates

        if len(hits) == 0:
            return (None, 0)
        elif len(hits) == 1:
            return (hits[0][0], order_confidences[hits[0][1]-1])
        elif len(hits) > 1:
            hits = sorted(hits, key= lambda x: x[1])
            min_hits_val = hits[0][1]
            min_hits = [spelling for spelling in hits if spelling[1] == min_hits_val]
            min_hits = sorted(min_hits, key=lambda x: x[0])
            return (min_hits[0][0], order_confidences[hits[0][1]-1])
        else:
            return (None, 0)
    

class ProcessingFilter(Filter):
    def __init__(self):
        pass


    def applyFilter(self, rowInput: str):
        return (None, 0)

        



        
    

    

