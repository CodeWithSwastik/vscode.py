# IPC Commands are in the following format
# {2digitcode}: {arg1}|||{arg2}|||{argn}

import json
from ._types import *
from .utils import *


def show_quick_pick(items: list, options: QuickPickOptions = None) -> QuickPickItem:
    """
    Shows a selection list allowing multiple selections.

    Returns either the selected items or undefined.
    """
    data = []
    for item in items:
        if isinstance(item, QuickPickItem):
            data.append(item.__dict__)
        else:
            data.append(item)
    
    items = json.dumps(data)
    if not options:
        options = {}
    
    if isinstance(options, QuickPickOptions):
        options = options.__dict__
    options = json.dumps(options)
    print(f"QP: {items}|||{options}", flush=True, end="")
    res = json_input()
    if not res or isinstance(res, str):
        return res
    else:
        return QuickPickItem(**res)



def show_input_box(options: InputBoxOptions = None) -> str:
    """
    Opens an input box to ask the user for input.

    The returned value will be undefined if the input box was canceled (e.g. pressing ESC). Otherwise the returned value will be the string typed by the user or an empty string if the user did not type anything but dismissed the input box with OK.
    """
    if not options:
        options = {}
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

def set_status_bar_message(text: str, hide_after_timeout: int = None) -> Disposable:
    """
    Set a message to the status bar. 

    Note that status bar messages stack and that they must be disposed when no longer used.

    hide_after_timeout: Timeout in seconds after which the message will be auto disposed.
    """

    print(
        f"BM: {text}" + f"|||{hide_after_timeout*1000}" * (hide_after_timeout is not None),
        flush=True,
        end="",
    )
    res = uinput()
    return Disposable(res)