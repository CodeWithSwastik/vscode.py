import json
from collections import ChainMap

from .undef import undefined


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


def send_ipc(code, args=None):
    obj = json.dumps({"code": code, "args": args or []})
    print(f"{obj}", flush=True, end="")


def camel_to_snake(text: str) -> str:
    return "".join("_" + i.lower() if i.isupper() else i for i in text).lstrip("_")


def apply_func_to_keys(dictionary: dict, func) -> dict:
    new = {}
    for key, value in dictionary.items():
        if isinstance(value, dict):
            new[func(key)] = apply_func_to_keys(value, func)
        else:
            new[func(key)] = dictionary[key]
    return new


def combine_list_dicts(li) -> dict:
    return dict(ChainMap(*li[::-1]))


def convert_snake_to_camel(text: str) -> str:
    temp = text.split("_")
    return temp[0] + "".join(ele.title() for ele in temp[1:])


def convert_snake_to_title(text) -> str:
    return text.replace("_", " ").title()


def convert_python_condition(condition) -> str:
    condition = " ".join(
        i if "_" not in i else convert_snake_to_camel(i) for i in condition.split(" ")
    )
    condition = condition.replace(" and ", " && ")
    condition = condition.replace(" or ", " || ")
    if " not " in condition:
        if "(" not in condition or ")" not in condition:
            raise SyntaxError(
                "Use parenthesis '()' while using 'not' otherwise your conditions might not work as expected!"
            )
        else:
            condition = condition.replace(" not ", " !")

    return condition
