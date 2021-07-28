import json
from ._types import undefined


def uinput():
    res = input()
    if res.strip() == "undefined":
        return undefined
    else:
        return res


def json_input():
    res = uinput()
    if not res:
        return res
    try:
        return json.loads(res)
    except json.decoder.JSONDecodeError:
        return res

def camel_to_snake(text:str) -> str:
    return ''.join(['_'+i.lower() if i.isupper() else i for i in text]).lstrip('_')

def apply_func_to_keys(dictionary: dict, func) -> dict:
    new = {}
    for key in dictionary:
        if isinstance(dictionary[key], dict):
            new[func(key)] = apply_func_to_keys(dictionary[key], func)
        else:
            new[func(key)] = dictionary[key]
    return new