from classifier import Classifier
from fuzzy_distance import calc_fuzzy_dist
import config
import unittest
import pandas as pd
from filter import *

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


class CountryExactFilterTestCase(unittest.TestCase):
    def setUp(self):
        self.cef = ExactFilter(appliesTo='C', name="Test Country Exact Filter")


    def test_ukraina(self):
        pass


class StateExactFilterTestCase(unittest.TestCase):
    def setUp(self):
        self.sef = ExactFilter(appliesTo='S', name="Test State Exact Filter")


class CountryFuzzyFilterTestCase(unittest.TestCase):
    def setUp(self):
        self.cff = FuzzyFilter(appliesTo='C', name="Test Country Fuzzy Filter")


class StateFuzzyFilterTestCase(unittest.TestCase):
    def setUp(self):
        self.sff = FuzzyFilter(appliesTo='S', name="Test State Fuzzy Filter")


class ProcessingFiltertestCase(unittest.TestCase):
    def setUp(self):
        self.pf = ProcessingFilter(appliesTo='o', name="Test Processing Filter")


unittest.main()