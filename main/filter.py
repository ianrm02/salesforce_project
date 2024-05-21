import common_alternates_db

class Filter:
    ruleSet = []
    appliesTo = None #Enumerable: C S or A

    def __init__(self):
        self.ruleSet = None #expects a hashmap
        self.appliesTo = None

    def __init__(self, filterRule:dict[str:str]):
        self.ruleSet = filterRule

    def applyFilter(rowInput: str):
        return None
    

class userCountryFilter(Filter):
    def __init__(self):
        self.appliesTo = 'C'
    def applyFilter(self, rowInput: str):
        if self.ruleSet.__contains__(rowInput):
            return (self.ruleSet[rowInput], 100)
        else:
            return (None, 0)
    


filter = userCountryFilter()
print(filter.applyFilter)
    

    

