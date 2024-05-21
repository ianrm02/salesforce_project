import common_alternates_db
import re
from fuzzy_distance import calc_fuzzy_dist
import config

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
        # Will rely on the self.appliesTo field to determine which column of the input to extract from. 
        # the filters should be grouped and ordered all of the c, then all of s, then all of a filters.
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
        self.hits = []
        self.min_hits_val = None
        if self.appliesTo == 'C':
            self.ruleSet = common_alternates_db.COMMON_ALTERNATES
        elif self.appliesTo == 'S':
            self.ruleSet = {} #TODO
        elif self.appliesTo == 'A':
            self.ruleSet = {} #TODO
        else:
            raise Exception("Invalid Filter")
    
    
    def _sort_multiple_hits(self):
        self.hits = sorted(self.hits, key= lambda x: x[1]) #sorts list min->max by dist
        self.min_hits_val = self.hits[0][2] #gets min_hit_val from min->max sorted list
        min_hits = [spelling for spelling in self.hits if spelling[2] == self.min_hits_val] #selects all hits with the same min_hit_val
        min_hits = sorted(min_hits, key=lambda x: x[0]) #sorts remaining viable hits alphebtically
        #should it return 50% confidence or should it return the scaling order_confidence

        possibles = [full[1] for full in min_hits]

        for i, char in enumerate(self.rowInput):
            if len(possibles) == 1:
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
            return (self.ruleSet[possibles[0]], 60)

        #If we get to here, we are not confident but we think you might be trying to guess something similar
        return (self.ruleSet[self.hits[0][0]], 30)
    

    def applyFilter(self, rowInput: str):
        self.rowInput = self._parseUserInput(rowInput)
        self.hits = []
        for common_spelling in list(self.ruleSet.keys()):
            dist = calc_fuzzy_dist(common_spelling, self.rowInput)
            if dist <= self.order:
                self.hits.append((self.ruleSet[common_spelling], common_spelling, dist))
        
        self.hits = list(set(self.hits)) #to remove duplicates

        if len(self.hits) == 0:
            return (None, 0)
        elif len(self.hits) == 1:
            return (self.hits[0][0], config.ORDER_CONFIDENCES[self.hits[0][2]-1])
        elif len(self.hits) > 1:
            return self._sort_multiple_hits()
        else:
            return (None, 0)
    

class ProcessingFilter(Filter):
    def __init__(self):
        pass


    def applyFilter(self, rowInput: str):
        return (None, 0)


        



        
    

    

