from classifier import Classifier
from database_functions import DatabaseManager
import config
import time
import logging

class ClassifierApp(object):
    _total_db_size = 0
    _entries_processed = 0
    _batch_size = 0
    _payload = None
    db_handler = DatabaseManager()

    def __init__(self):
        self.clf = Classifier()
        self._batch_size = config.BATCH_SIZE
        #TODO implement custom payload loading
        self.db_handler = DatabaseManager()
        self._total_db_size = self.db_handler.get_db_size()


    def process_entries(self):
        #TODO add comments
        start_time = time.time()
        while self._entries_processed + self._batch_size < self._total_db_size:
            self.clf.batch_process(self.db_handler.get_next_n(self._batch_size))
            self._entries_processed += self._batch_size
        
        remainder = self._total_db_size - self._entries_processed

        if remainder > 0:
            self.clf.batch_process(self.db_handler.get_next_n(remainder))
            self._entries_processed += remainder

        print("")
        if self._entries_processed == self._total_db_size: 
            print(f"All {self._total_db_size} entries proccessed in {time.time()-start_time:.4f} seconds.")
        else:
            print("[WARNING] Not all entries processed")
            #TODO error handling / logging for non-processed entries and why they couldnt be processed
        print("")

            
    def print_intermediate_diagnostics(self, results):
        #TODO add comments
        total_country_confidence = 0
        total_state_confidence = 0
        num_max_confident_country = 0
        num_fully_converted = 0
        for _, mappings in results.items(): 
            #print(f"{mappings[4]} {mappings[5]} {mappings[6]} {mappings[7]} NewCo:{mappings[0]} CoConf:{mappings[1]} NewSt:{mappings[2]} StConf:{mappings[3]} {"[FULLY MAPPED]" if mappings[1]+mappings[3] == 200 else ""}")
            total_country_confidence += mappings[1]
            total_state_confidence += mappings[3]
            if mappings[1] == config.MAX_CONFIDENCE: 
                num_max_confident_country += 1
                if mappings[0] not in config.STATED_COUNTRIES: num_fully_converted += 1
                if mappings[3] == config.MAX_CONFIDENCE:
                    if mappings[0] in config.STATED_COUNTRIES: num_fully_converted += 1

        print("")
        print(f"AVG COUNTRY CONF: {total_country_confidence/self._total_db_size:.2f}")
        print(f"AVG STATE   CONF: {total_state_confidence/self._total_db_size:.2f}")

        print(f"%DB with 100% Country Confidence: {num_max_confident_country/self._total_db_size*100:.2f}")
        print("")
        print(f"% Entries Fully Converted (with 100% confidence): {num_fully_converted/self._total_db_size*100:.2f}")


    def uploadProcessedToDB(self):
        for _, mappings in self.clf.get_results().items():
            self.db_handler.store_temp_values(mappings)


    def load_db_from_payload(self, payload):
        self._payload = payload
        self.db_handler = self._create_db_manager(payload=self._payload)
        self._total_db_size = self.db_handler.get_db_size()

        print(self.db_handler.get_db_size())


    def _create_db_manager(self, payload):
        print(payload)
        #TODO with custom payload, for now just default to config
        db_handler = DatabaseManager()
        return db_handler


    def run(self):
        self.process_entries()

        intermediate_results = self.clf.get_results()
        #List elements for each address in intermediate_results:
        #0: New Country, #1: New Country Confidence, #2 New State, #3 New State Confidence, #4 ID, #5 Addr Line, #6 State Line, #7 Country Line
        self.print_intermediate_diagnostics(intermediate_results)

        #upload the processed to result to intermediate database to await UI stage.
        self.uploadProcessedToDB()

        del self.db_handler #TODO test if the connection is still open

        """Test Cases to observe / processing filter?
        198 "Hospital; Bangalore; 560099" "" "IN" Maps to India correctly but not Bangalore because
            Bangalore was ^^^ in the address field. 
            
            Should the address filter check every element of the address field against all of the common_state_alternates and common_country_alterantes?
            That would be pretty expensive computationally, but assuming relatively clean user data most states should get filtered to 100% and not get to this stage of filters before this and only really crummy user data get to this stage. Or is it the
            responsibility of the user to then manually find this in the UI stages of the solution and correct it because they had poor data quality?
        """

        logging.info('[Finished ClassifierApp.run()]')       

        return 0