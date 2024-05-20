import config
import pandas as pd
import numpy as np

#currently only handles 3166-1, but will need to be adapted to include 3166-2 as well.
#do we want to have 3 files: 3166-1, 3166-2 and user-defined?
def _load_iso_standard(standards_folder_path: str, working_standard: str = "ISO3166_1.csv"):
    standard_df = pd.read_csv(standards_folder_path + working_standard, keep_default_na=False)
    return standard_df

def load_standards_from_config(standards_folder_path: str):
    #eventually for standard in standards_folder, for now just the one.
    return _load_iso_standard(standards_folder_path=standards_folder_path)

