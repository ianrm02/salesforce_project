from classifier import Classifier
from fuzzy_distance import calc_fuzzy_dist
import config
import unittest
import pandas as pd

class ClassifierInitTestCase(unittest.TestCase):
    def setUp(self):
        self.clf = Classifier()


    def test_classifier_has_iso(self):
        self.assertIs(type(self.clf.iso_standard_df), pd.DataFrame, "ISO Standard Wrong Type After Load")


    def test_classifier_has_address(self):
        pass


class DatabaseHandlerTestCase(unittest.TestCase):
    def setUp(self):
        pass


    def test_db_for_something(self):
        pass


unittest.main()