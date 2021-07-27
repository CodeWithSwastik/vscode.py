# IPC Commands are in the following format
# {2digitcode}: {arg1}|||{arg2}|||{argn}

import json
from ._types import *
from .utils import *


def show_quick_pick(items: list, options: QuickPickOptions) -> dict:
    """
    Shows a selection list allowing multiple selections.

    Returns either the selected items or undefined.
    """
    
    items = json.dumps(items)
    if isinstance(options, QuickPickOptions):
        options = options.__dict__
    options = json.dumps(options)
    print(f"QP: {items}|||{options}", flush=True, end="")
    return json_input()


def show_input_box(options: InputBoxOptions) -> str:
    """
    Opens an input box to ask the user for input.

    The returned value will be undefined if the input box was canceled (e.g. pressing ESC). Otherwise the returned value will be the string typed by the user or an empty string if the user did not type anything but dismissed the input box with OK.
    """
    if isinstance(options, InputBoxOptions):
        options = options.__dict__
    options = json.dumps(options)
    print(f"IB: {options}", flush=True, end="")
    return uinput()


def _base(func:str, text:str, *args:str) -> str:
    print(
        f"SM: {func}|||{text}" + "|||" * bool(args) + "|||".join(args),
        flush=True,
        end="",
    )
    res = uinput()
    return res


def show_info_message(text:str, *args:str) -> str:
    """
    Show an information message.
    """
    return _base("showInformationMessage", text, *args)


def show_warn_message(text:str, *args:str) -> str:
    """
    Show a warning message.
    """
    return _base("showWarningMessage", text, *args)


def show_error_message(text:str, *args:str) -> str:
    """
    Show an error message.
    """
    return _base("showErrorMessage", text, *args)
