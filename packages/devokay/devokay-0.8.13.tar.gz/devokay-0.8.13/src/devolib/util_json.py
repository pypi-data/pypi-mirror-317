
# -*- coding: UTF-8 -*-
# python3

import json

from devolib.util_log import LOG_E
from devolib.util_fs import write_file

def json_from_str(str):
    return json.loads(str)

def json_to_str(dict):
    return json.dumps(dict)

'''
@brief read file to json object
'''
def json_from_file(file_path):
    json_obj = {}
    try:
        with open(file_path, 'r') as file:
            json_obj = json.load(file)
    except FileNotFoundError:
        LOG_E(f'{file_path} not exists')
    except json.JSONDecodeError as e:
        LOG_E(f'Error decoding JSON: {e}')

    return json_obj

def json_to_file(file_path, json_data):
    write_file(file_path, json.dumps(json_data))