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
    
    
    def _sort_multiple_hits(self, parsedIn):
        self.hits = sorted(self.hits, key= lambda x: x[1]) #sorts list min->max by dist
        self.min_hits_val = self.hits[0][2] #gets min_hit_val from min->max sorted list
        min_hits = [spelling for spelling in self.hits if spelling[2] == self.min_hits_val] #selects all hits with the same min_hit_val
        min_hits = sorted(min_hits, key=lambda x: x[0]) #sorts remaining viable hits alphebtically

        possibles = [full[1] for full in min_hits]

        for i, char in enumerate(parsedIn):
            if len(possibles) == 1: #only 1 probable hit remaining
                return (self.ruleSet[possibles[0]], config.ORDER_CONFIDENCES[self.min_hits_val-1])
            temp_possibles = []
            for hit in possibles:
                if i <= len(hit)-1:
                    if hit[i] == char:
                        temp_possibles.append(hit)
            if len(temp_possibles) == 0:
                return (self.ruleSet[possibles[0]], config.ORDER_CONFIDENCES[self.min_hits_val-1])
            
            possibles = temp_possibles
        
        if len(possibles) == 1: 
            #Base case when the input is shorter than but has no typos when compared to a longer common spelling 
            # ie Nigeri to Nigeria or Niger, we decide to assume if you are trying to enter the word with which your input
            # has the most similar characters, in order. We however are not strong in this assumption, so we return with only 60% confidence
            return (self.ruleSet[possibles[0]], config.NON_TYPO_MISMATCH_LENGTH_CONFIDENCE)

        #If we get to here, we are not confident but we think you might be trying to guess something similar
        return (self.ruleSet[self.hits[0][0]], config.MULTIPLE_SIMILAR_HITS_FALLBACK_CONFIDENCE)
    

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

        if len(self.hits) == 0:
            return (None, 0)
        elif len(self.hits) == 1:
            return (self.hits[0][0], config.ORDER_CONFIDENCES[self.hits[0][2]-1])
        elif len(self.hits) > 1:
            if self.appliesTo == "C":
                return self._sort_multiple_hits(parsedIn=parsedIn)
            else:
                return (self.hits[0][0], config.ORDER_CONFIDENCES[self.hits[0][2]-1])
        else:
            return (None, 0)
    

class ProcessingFilter(Filter):
    def __init__(self, appliesTo='A', name=None):
        self.appliesTo = appliesTo
        self._name = name


    def applyFilter(self, rowInput: str):
        return (None, 0)


        



        
    

    

