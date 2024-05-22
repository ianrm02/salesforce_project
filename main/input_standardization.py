import re #regular expressions to detokenize
import config

def _txt_file_to_list(dataset_path: str, dataset_file: str, encoding='utf-8'):
    with open(dataset_path + dataset_file, encoding=encoding) as file:
        lines = [line.rstrip() for line in file]
    
    return lines


def _detokenize_addresses(address_list: list[str]):
    detokenized_addresses = [re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", address.upper()) for address in address_list]
    
    return detokenized_addresses


def generateStandardizedInput(dataset_path: str, dataset_file: str, encoding='utf-8'):
    return _detokenize_addresses(_txt_file_to_list(dataset_path, dataset_file, encoding))


def _all_caps_dict(dictToConv: dict):
    capitalized_dict = {}
    for key, value in dictToConv.items():
        if isinstance(key, str):
            key = key.upper()
        if isinstance(value, str):
            value = value.upper()
        capitalized_dict[key] = value
    return capitalized_dict

