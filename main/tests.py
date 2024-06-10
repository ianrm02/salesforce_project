from classifier import Classifier
from fuzzy_distance import calc_fuzzy_dist
from database_functions import *
import config
import unittest
import pandas as pd
from filter import *

class ClassifierInitTestCase(unittest.TestCase):
    def setUp(self):
        self.clf = Classifier()


    def test_classifier_init(self):
        self.assertIs(type(self.clf), Classifier, "Classifier is not of type Classifier")
        self.assertIs(type(self.clf.filters), list, "clf.filters is NOT expected list of objects of type Filter")


    def test_classifier_filter_types(self):
        expected_filter_types = [UserFilter, CountryExactFilter, FuzzyFilter, UserFilter, StateExactFilter, FuzzyFilter, UserFilter, ProcessingFilter]
        
        for i, filter in enumerate(self.clf.filters):
            self.assertIs(type(filter), expected_filter_types[i], f"{i}th filter was of {type(filter)} but was expected to be {expected_filter_types[i]}")


    def test_classifier_filter_application_types(self):
        expected_filter_appliesTo_types = ['C', 'C', 'C', 'S', 'S', 'S', 'A', 'O']

        for i, filter in enumerate(self.clf.filters):
            self.assertIs(filter.getAppliesTo(), expected_filter_appliesTo_types[i], f"{i}th filter of type {type(filter)} was applied to {filter.getAppliesTo()}but was expected to be {expected_filter_appliesTo_types[i]}")


    def test_classifier_has_iso(self):
        self.assertIs(type(self.clf.iso_standard_df), pd.DataFrame, "ISO Standard Wrong Type After Load")

        
class DatabaseHandlerTestCase(unittest.TestCase):
    """
        - Proper Connection
        - Queries are producing expected outputs

        Before running make sure you have a database called "test_db" created in postgres.
        You can do this be running 'CREATE DATABASE test_db;' from the postgres shell
    """
    def setUp(self):
        self.db_handler = DatabaseManager(db_name='bobby_db')
        self.db_handler.setup_test_database()


    def testDatabseConnectionEstablished(self):
        # Testing if no connection made when a bad database is passed        
        with self.assertRaises(pg8000.DatabaseError):
            self.db_handler = DatabaseManager(db_name='fake_db')

        # Testing if connection made when a good database is passed
        self.db_handler = DatabaseManager(db_name='bobby_db')
        self.assertIsNot(self.db_handler.conn, None)
        self.assertIsNot(self.db_handler.cur, None)


    def test_db_insert_address(self):
        pass


    def test_db_delete_address(self):
        pass
    

    def test_db_re_id_database(self):
        pass
    

    def test_get_next_n(self):
        pass
    

    def test_get_db_size(self):
        self.assertEqual(self.db_handler.get_db_size(), 377)


    def test_get_freq(self): #TODO: make this more robust
        self.assertEqual(self.db_handler.get_freq('C', 'US'), 59)
        self.assertEqual(self.db_handler.get_freq('S', 'CA'), 3)
        self.assertEqual(self.db_handler.get_freq('A', '1545 liona street honolulu'), 1)


    def test_store_temp_values(self):
        pass


    def test_search_db(self):
        self.assertEqual(len(self.db_handler.search_db(("BIGSOLV ADVANCED LABS PRIVATE LIMITED", None, None))), 1)
        self.assertEqual(len(self.db_handler.search_db((None, "karnataka", "IN"))), 2)



    def test_get_all_from_table(self):
        pass

    



class CountryExactFilterTestCase(unittest.TestCase):
    def setUp(self):
        self.cef = CountryExactFilter(appliesTo='C', name="Test Country Exact Filter")


    def test_ukraina(self):
        pass


class StateExactFilterTestCase(unittest.TestCase):
    def setUp(self):
        self.sef = StateExactFilter(appliesTo='S', name="Test State Exact Filter")


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