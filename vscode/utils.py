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
