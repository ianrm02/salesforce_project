#paths
DATASET_PATH = "datasets/"
WORKING_DATASET = 'example_set_full.txt'
PREPROCESS_DATA_FILE = 'standardizedOut.csv'
ISO_3166_1_PATH = 'main/iso3166_1.csv'

#formats
OUTPUT_FORMAT = "alpha-2"
FILTER_ORDER = ['C', 'S', 'A', 'O'] #Country filters, then State, then Address, then Overflow (Processing filter + any add ons)

#Fuzzy Distance Confidences
ORDER_CONFIDENCES = [90, 80, 70, 50] #ie 1 order is 90% confidence
MULTIPLE_SIMILAR_HITS_FALLBACK_CONFIDENCE = 30
NON_TYPO_MISMATCH_LENGTH_CONFIDENCE = 60
WELL_PLACED_CONFIDENCE_THRESHOLD = 70

BATCH_SIZE = 10

#database config
DBNAME = 'bobby_db'
USER = 'postgres'
PASSWORD = 'bobby'
HOST = 'localhost'

STATED_COUNTRIES = ['AU', 'BR', 'CA', 'CN', 'IE', 'IN', 'IT', 'JP', 'MX', 'US']