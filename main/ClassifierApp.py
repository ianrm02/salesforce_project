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

            
    def get_intermediate_diagnostics(self, results):
        #TODO add comments
        total_country_confidence = 0
        total_state_confidence = 0
        num_max_confident_country = 0
        num_fully_converted = 0
        for _, mappings in results.items(): 
            total_country_confidence += mappings[1]
            total_state_confidence += mappings[3]
            if mappings[1] == config.MAX_CONFIDENCE: 
                num_max_confident_country += 1
                if mappings[0] not in config.STATED_COUNTRIES: num_fully_converted += 1
                if mappings[3] == config.MAX_CONFIDENCE:
                    if mappings[0] in config.STATED_COUNTRIES: num_fully_converted += 1


        statistics = []
        avg_country_conf = total_country_confidence/self._total_db_size
        avg_state_conf = total_state_confidence/self._total_db_size
        percent_max_conf = num_max_confident_country/self._total_db_size*100
        percent_full_converted = num_fully_converted/self._total_db_size*100

        print("")

        print(f"AVG COUNTRY CONF: {avg_country_conf:.2f}")
        print(f"AVG STATE   CONF: {avg_state_conf:.2f}")

        print(f"%DB with Max Country Confidence: {percent_max_conf:.2f}")
        print("")
        print(f"% Entries Fully Converted (with Max confidence): {percent_full_converted:.2f}")

        statistics.append(["Avg. Country Confidence", avg_country_conf, "Average confidence of the addresses successfully converted to a country code. (Graded 1-5)"])
        statistics.append(["Avg. State Confidence", avg_state_conf, "Average confidence of the addresses successfully converted to a state code. (Graded 1-5)"])
        statistics.append(["Max Confidence Percentage", percent_max_conf, "Percentage of addresses that were converted with maximum confidence."])
        statistics.append(["Fully Converted Percentage", percent_full_converted, "Percentage of addresses that were converted with both country and state codes."])

        return statistics


    def uploadProcessedToDB(self):
        for _, mappings in self.clf.get_results().items():
            self.db_handler.store_temp_values(mappings)


    def load_db_from_payload(self, payload):
        self._payload = payload
        self.db_handler = self._create_db_manager(payload=self._payload)
        self._total_db_size = self.db_handler.get_db_size()


    def _create_db_manager(self, payload):
        #TODO with custom payload, for now just default to config. Would need to add security / authentication to protect user data
        db_handler = DatabaseManager()
        return db_handler


    def run(self):
        self.process_entries()

        self.clf.runKMeansModel()

        intermediate_results = self.clf.get_results()
        #List elements for each address in intermediate_results:
        #0: New Country, #1: New Country Confidence, #2 New State, #3 New State Confidence, #4 ID, #5 Addr Line, #6 State Line, #7 Country Line
        self.get_intermediate_diagnostics(intermediate_results)

        #upload the processed to result to intermediate database to await UI stage.
        self.uploadProcessedToDB()

        del self.db_handler #TODO test if the connection is still open

        logging.info('[Finished ClassifierApp.run()]')       

        return 0