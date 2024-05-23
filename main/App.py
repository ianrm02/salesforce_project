from classifier import Classifier
from database_functions import get_next_n, get_db_size
import config

class App(object):
    _total_db_size = None
    _entries_processed = 0
    _batch_size = 0

    def __init__(self):
        self.clf = Classifier()
        self.db_handler = None #for when we turn the database functions into a db handler class
        self._total_db_size = get_db_size()
        self._batch_size = config.BATCH_SIZE


    def run(self):
        while self._entries_processed + self._batch_size < self._total_db_size:
            self.clf.batch_process(get_next_n(self._batch_size))
            self._entries_processed += self._batch_size
        
        remainder = self._total_db_size - self._entries_processed

        if remainder > 0:
            self.clf.batch_process(get_next_n(remainder))
            self._entries_processed += remainder

        if self._entries_processed == self._total_db_size: print("All entries proccessed.")


    def testRun(self):
        example_case = ('6652 BIRCHWOOD ST; sandiego','US','CA')
        self.clf.applyFilterStack(example_case)


app = App()
app.run()

