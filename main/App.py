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


    def run(self):
        while self._entries_processed + self._batch_size < self._total_db_size:
            self.clf.batch_process(self.db_handler.get_next_n(self._batch_size))
            self._entries_processed += self._batch_size
        
        remainder = self._total_db_size - self._entries_processed

        if remainder > 0:
            self.clf.batch_process(self.db_handler.get_next_n(remainder))
            self._entries_processed += remainder

        if self._entries_processed == self._total_db_size: print("All entries proccessed.")


    def testRun(self):
        example_case = ('6652 BIRCHWOOD ST; sandiego','US','CA')
        self.clf.applyFilterStack(example_case)


app = App()
app.run()

