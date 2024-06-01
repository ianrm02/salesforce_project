import common_country_alternates
import common_state_alternates
from fuzzy_distance import calc_fuzzy_dist
import config
import re


class InvalidFilter(Exception):
    pass


class Filter:
    _name = None
    ruleSet = {}
    appliesTo = None #Enumerable: C S or A for country state address respectively

    def __init__(self, filterRule={}, name=None):
        self.ruleSet = filterRule #expects a hashmap
        self.appliesTo = None
        self._name = name

    def _parseUserInput(self, userIn)->str:
        """
            Input: userIn as a tuple of strings ('[ADDRESS FIELD]', '[STATE FIELD]', '[COUNTRY FIELD]')
        """      
        text = ""
        if self.appliesTo == 'C':
            relevantText = userIn[3]
            text = ''.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http\S+"," ",str(relevantText)).split())
            text = re.sub(r"[0-9]", "", text)
        elif self.appliesTo == 'S':
            relevantText = userIn[2]
            text = ''.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",str(relevantText)).split())
            text = re.sub(r"[0-9]", "", text) #Might become problematic for Japan's number based state system, but TODO for now.
        elif self.appliesTo == 'A':
            relevantText = userIn[1]
            text = ''.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",str(relevantText)).split())
        elif self.appliesTo == 'O':
            relevantText == userIn[1]
            text = ''.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",str(relevantText)).split())

        text = text.upper()
        return text 
    

    def applyFilter(rowInput: str):
        return (None, 0)
    

    def getKeys(self):
        return self.ruleSet.keys()
    
    def getName(self):
        return self._name
    
    def setName(self, name):
        self._name = name


class UserFilter(Filter):
    def __init__(self, filterRule, appliesTo, name=None):
        self.ruleSet = filterRule
        self.appliesTo = appliesTo
        self._name = name


    def applyFilter(self, rowInput: str):
        parsedIn = self._parseUserInput(rowInput)
        if parsedIn == "":
            return (None, 0)
        if self.ruleSet.__contains__(parsedIn):
            return (self.ruleSet[parsedIn], 100)
        else:
            return (None, 0)


class CountryExactFilter(Filter):
    def __init__(self, appliesTo, name=None):
        self.appliesTo = appliesTo
        self._name = name
        if self.appliesTo == 'C':
            self.ruleSet = common_country_alternates.COMMON_COUNTRY_ATERNATES
        else:
            raise Exception("Invalid Filter")


    def applyFilter(self, rowInput: str):
        parsedIn = self._parseUserInput(rowInput)
        if parsedIn == "":
            return (None, 0)
        if self.ruleSet.__contains__(parsedIn):
            return (self.ruleSet[parsedIn], 100)
        else:
            return (None, 0)
        

class StateExactFilter(Filter):
    def __init__(self, appliesTo, name=None):
        self.appliesTo = appliesTo
        self._name = name
        if self.appliesTo == 'S':
            self.ruleSet = common_state_alternates.COMMON_STATE_ALTERNATES
        else:
            raise Exception("Invalid Filter")


    def applyFilter(self, rowInput: str, identifiedCountry=False, probableCountry=None):
        parsedIn = self._parseUserInput(rowInput)
        if parsedIn == "":
            return (None, 0)

        if identifiedCountry:
            if self.ruleSet[probableCountry].__contains__(parsedIn):
                return (self.ruleSet[probableCountry][parsedIn], 100)
        elif not identifiedCountry:
            for country, common_state_spellings in self.ruleSet:
                if common_state_spellings.__contains__(parsedIn):
                    return (self.ruleSet[country][parsedIn], 80)
                
        #default
        return (None, 0)


class FuzzyFilter(Filter):
    def __init__(self, appliesTo, order=2, name=None):
        self.appliesTo = appliesTo
        self.order = order
        self._name = name
        self.hits = []
        self.min_hits_val = None
        if self.appliesTo == 'C':
            self.ruleSet = common_country_alternates.COMMON_COUNTRY_ATERNATES
        elif self.appliesTo == 'S':
            self.ruleSet = common_state_alternates.COMMON_STATE_ALTERNATES
        elif self.appliesTo == 'A':
            self.ruleSet = {} #TODO
        else:
            raise Exception("Invalid Filter")
    

    def applyFilter(self, rowInput: str):
        parsedIn = self._parseUserInput(rowInput)
        if parsedIn == "":
            return (None, 0)
        self.hits = []
        
        if self.appliesTo == "C":
            for common_spelling in list(self.ruleSet.keys()):
                dist = calc_fuzzy_dist(common_spelling, parsedIn)
                if dist <= self.order:
                    self.hits.append((parsedIn, self.ruleSet[common_spelling], dist))
        elif self.appliesTo == "S":
            for country, common_alternates in self.ruleSet.items():
                for common_spelling in list(common_alternates.keys()):
                    dist = calc_fuzzy_dist(common_spelling, parsedIn)
                    if dist <= self.order:
                        self.hits.append((parsedIn, self.ruleSet[country][common_spelling], dist))


        self.hits = list(set(self.hits)) #to remove duplicates
        self.hits = sorted(self.hits, key=lambda x: x[2])

        if len(self.hits) == 0:
            return (None, 0)
        elif len(self.hits) == 1:
            return (self.hits[0][1], config.ORDER_CONFIDENCES[self.hits[0][2]-1])
        elif len(self.hits) > 1:
            if self.hits[0][2] == 0:
                return (self.hits[0][1], config.ORDER_CONFIDENCES[self.hits[0][2]-1])
            return (self.hits[0][1], config.ORDER_CONFIDENCES[self.hits[0][2]-1])
        else:
            return (None, 0)
    

class ProcessingFilter(Filter):
    def __init__(self, appliesTo='A', name=None):
        self.appliesTo = appliesTo
        self._name = name


    def applyFilter(self, rowInput: str):
        return (None, 0)


        



        
    

    

