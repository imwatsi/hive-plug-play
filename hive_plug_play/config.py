import json
import os

_path = os.path.dirname(__file__)

def load_config(path=_path):
    values = {}
    
    f = open(f'{path}/config.dat', 'r').readlines()
    for line in f:
        setting = line.split('=')
        _key = setting[0]
        _value = setting[1].strip('\n ')
        if '[' in _value or '{' in _value:
            values[_key] = json.loads(_value)
        else:
            values[_key] = _value
    return values
