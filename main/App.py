from classifier import Classifier
from database_functions import DatabaseManager
import config

class App(object):
    _total_db_size = None
    _entries_processed = 0
    _batch_size = 0

    def __init__(self):
        self.clf = Classifier()
        self.db_handler =  DatabaseManager()
        self._total_db_size = self.db_handler.get_db_size()
        self._batch_size = config.BATCH_SIZE
        
        #TODO testing - get rid of
        #self._total_db_size = 10


    def run(self):
        print("Starting...")
        while self._entries_processed + self._batch_size < self._total_db_size:
            self.clf.batch_process(self.db_handler.get_next_n(self._batch_size))
            self._entries_processed += self._batch_size
        
        remainder = self._total_db_size - self._entries_processed

        if remainder > 0:
            self.clf.batch_process(self.db_handler.get_next_n(remainder))
            self._entries_processed += remainder

        if self._entries_processed == self._total_db_size: 
            print("")
            print("All entries proccessed.")
            print("")
            results = self.clf.get_results()
            total_country_confidence = 0
            total_state_confidence = 0
            num_max_confident_country = 0
            num_fully_converted = 0
            for key, mappings in results.items():
                print(f"{key} ||| {mappings[0]} {mappings[1]} {mappings[2]} {mappings[3]}")
                #0: New Country, #1: New Country Confidence, #2 New State, #3 New State Confidence, #4 ID, #5 Addr Line, #6 State Line, #7 Country Line
                total_country_confidence += mappings[1]
                total_state_confidence += mappings[3]
                if mappings[1] == 100: 
                    num_max_confident_country += 1
                    if mappings[0] not in config.STATED_COUNTRIES: num_fully_converted += 1
                    if mappings[3] == 100:
                        if mappings[0] in config.STATED_COUNTRIES: num_fully_converted += 1


            print(f"AVG COUNTRY CONF: {total_country_confidence/self._total_db_size}")
            print(f"AVG STATE   CONF: {total_state_confidence/self._total_db_size}")

            print(f"%DB with 100% Country Confidence: {num_max_confident_country/self._total_db_size*100:.2f}")
            print("")
            print(f"% Entries Fully Converted (with 100% confidence): {num_fully_converted/self._total_db_size*100:.2f}")


        
        #TODO Now Do UI Here


        print("")
        print("Done")
        return 0


app = App()
app.run()