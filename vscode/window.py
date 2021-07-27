# IPC Commands are in the following format
# {2digitcode}: {arg1}|||{arg2}|||{argn}

import json
from .interfaces import *


def _input():
    res = input()
    if res.strip() == "undefined":
        return undefined
    else:
        return res


def _json_input():
    res = _input()
    if not res:
        return res
    try:
        return json.loads(res)
    except json.decoder.JSONDecodeError:
        return res


def show_quick_pick(items, options):
    items = json.dumps(items)
    if isinstance(options, QuickPickOptions):
        options = options.__dict__
    options = json.dumps(options)
    print(f"QP: {items}|||{options}", flush=True, end="")
    return _json_input()


def show_input_box(options):
    if isinstance(options, InputBoxOptions):
        options = options.__dict__
    options = json.dumps(options)
    print(f"IB: {options}", flush=True, end="")
    return _input()


def _base(func, text, *args):
    print(
        f"SM: {func}|||{text}" + "|||" * bool(args) + "|||".join(args),
        flush=True,
        end="",
    )
    res = _input()
    return res


def show_info_message(text, *args):
    return _base("showInformationMessage", text, *args)


def show_warn_message(text, *args):
    return _base("showWarningMessage", text, *args)


def show_error_message(text, *args):
    return _base("showErrorMessage", text, *args)
