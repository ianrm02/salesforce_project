#paths
DATASET_PATH = "datasets/"
WORKING_DATASET = 'example_set_full.txt'
PREPROCESS_DATA_FILE = 'standardizedOut.csv'
ISO_3166_1_PATH = 'main/iso3166_1.csv'

#formats
OUTPUT_FORMAT = "alpha-2"
FILTER_ORDER = ['C', 'S', 'A', 'O'] #Country filters, then State, then Address, then Overflow (Processing filter + any add ons)

#Fuzzy Distance Confidences
MAX_CONFIDENCE = 5
ORDER_CONFIDENCES = [5, 4, 3, 2] #ie 1 order is 90% confidence
MULTIPLE_SIMILAR_HITS_FALLBACK_CONFIDENCE = 1
NON_TYPO_MISMATCH_LENGTH_CONFIDENCE = 3
WELL_PLACED_CONFIDENCE_THRESHOLD = 4

BATCH_SIZE = 10

#database config
DBNAME = 'bobby_db'
USER = 'postgres'
PASSWORD = 'shellberb'
HOST = 'localhost'

STATED_COUNTRIES = ['AU', 'BR', 'CA', 'CN', 'IE', 'IN', 'IT', 'JP', 'MX', 'US']
COUNTRY_WITH_REQUIRED_STATES_ALL_STATES = {
    'AU': ['ACT', 'NSW', 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA'],
    'BR': ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO'],
    'CA': ['AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'NT', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT'],
    'CN': ['AH', 'BJ', 'CQ', 'FJ', 'GS', 'GD', 'GX', 'GZ', 'HA', 'HB', 'HE', 'HI', 'HK', 'HL', 'HN', 'JL', 'JS', 'JX', 'LN', 'MO', 'NM', 'NX', 'QH', 'SC', 'SD', 'SH', 'SN', 'SX', 'TJ', 'XJ', 'XZ', 'YN', 'ZJ'],
    'IE': ['C', 'CE', 'CN', 'CW', 'D', 'DL', 'G', 'KE', 'KK', 'KY', 'L', 'LD', 'LH', 'LK', 'LM', 'LS', 'MH', 'MN', 'MO', 'OY', 'RN', 'SO', 'TN', 'W', 'WD', 'WH', 'WX', 'WW'],
    'IN': ['AN', 'AP', 'AR', 'AS', 'BR', 'CH', 'CT', 'DD', 'DL', 'DN', 'GA', 'GJ', 'HP', 'HR', 'JH', 'JK', 'KA', 'KL', 'LD', 'MH', 'ML', 'MN', 'MP', 'MZ', 'NL', 'OR', 'PB', 'PY', 'RJ', 'SK', 'TG', 'TN', 'TR', 'UP', 'UT', 'WB'],
    'IT': ['AG', 'AL', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AT', 'AV', 'BA', 'BG', 'BI', 'BL', 'BN', 'BO', 'BR', 'BS', 'BT', 'BZ', 'CA', 'CB', 'CE', 'CH', 'CL', 'CN', 'CO', 'CR', 'CS', 'CT', 'CZ', 'EN', 'FC', 'FE', 'FG', 'FI', 'FM', 'FR', 'GE', 'GO', 'GR', 'IM', 'IS', 'KR', 'LC', 'LE', 'LI', 'LO', 'LT', 'LU', 'MB', 'MC', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NA', 'NO', 'NU', 'OR', 'PA', 'PC', 'PD', 'PE', 'PG', 'PI', 'PN', 'PO', 'PR', 'PT', 'PU', 'PV', 'PZ', 'RA', 'RC', 'RE', 'RG', 'RI', 'RM', 'RN', 'RO', 'SA', 'SI', 'SO', 'SP', 'SR', 'SS', 'SV', 'TA', 'TE', 'TN', 'TO', 'TP', 'TR', 'TS', 'TV', 'UD', 'VA', 'VB', 'VC', 'VE', 'VI', 'VR', 'VT', 'VV'],
    'JP': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47'],
    'MX': ['AGU', 'BCN', 'BCS', 'CAM', 'CHH', 'CHP', 'COA', 'COL', 'DIF', 'DUR', 'GRO', 'GUA', 'HID', 'JAL', 'MEX', 'MIC', 'MOR', 'NAY', 'NLE', 'OAX', 'PUE', 'QUE', 'ROO', 'SIN', 'SLP', 'SON', 'TAB', 'TAM', 'TLA', 'VER', 'YUC', 'ZAC'],
    'US': ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
}
