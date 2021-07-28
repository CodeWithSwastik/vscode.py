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


class Position:
    """
    Represents a line and character position, such as the position of the cursor.
    """
    def __init__(self, line:int, character: int):
        self.line = line
        self.character = character

    @staticmethod
    def from_dict(data: dict):
        pos = Position(0,0)
        pos.__dict__.update(data)
        return pos

    def __eq__(self, other):
        return self.line == other.line and self.character == other.character

    # TODO: Position methods
        
class Range:
    "A range represents an ordered pair of two positions. It is guaranteed that start.isBeforeOrEqual(end)"
    
    def __init__(self, start: Position, end: Position):
        self.start = start
        self.end = end

    @staticmethod
    def from_dict(data):
        return Range(Position.from_dict(data['start']),Position.from_dict(data['end']))
    
    @property
    def __dict__(self):
        return {'start': self.start.__dict__, 'end': self.end.__dict__}

    @property
    def is_empty(self):
        return self.start == self.end

    @property
    def in_single_line(self):
        return self.start.line == self.end.line

    def __eq__(self, other):
        return self.start == other.start and self.end == other

    # TODO: Range methods


class TextDocument:
    """
    Represents a text document, such as a source file. Text documents have lines and knowledge about an underlying resource like a file.
    """
    def __init__(self, data):
        self.__dict__.update(data)



    def get_text(self, location: Range = None) -> str:
        """
        Get the text of this document. A substring can be retrieved by providing a range. The range will be adjusted.
        """
        if location is not None:
            if isinstance(location, Range):
                location = location.__dict__
            location = json.dumps(location)
            print(f'GT: {location}', flush=True, end="")
        else:
            print('GT', flush=True, end="")

        return json_input()
    
    # TODO: TextDocument methods

class ActiveTextEditor:
    """
    The currently active editor or undefined. The active editor is the one that currently has focus or, when none has focus, the one that has changed input most recently.
    """

    def __init__(self):
        print('AT', flush=True, end="")
        res = uinput()
        if not res:
            self = undefined
        res = json.loads(res.replace(r'\\', r'\\\\'))
        self.__dict__.update(apply_func_to_keys(res, camel_to_snake))
        self.document = TextDocument(self.document)
        if hasattr(self, 'selection'):
            self.selection = Range.from_dict(self.selection)

    def replace(self, location: Range, value: str) -> bool:
        """
        Replace a certain text region with a new value. 
        You can use \r\n or \n in value and they will be normalized to the current document.   
        """

        if isinstance(location, Range):
            location = location.__dict__    
        location = json.dumps(location)
        print(f'EE: {location}|||{value}', flush=True, end="")
        return eval(uinput().title()) 
    
    def delete(self, location: Range) -> bool:
        """
        Delete a certain text region.
        """
        return self.replace(location, '')

    def insert(self, location: Position, value:str) -> bool:

        """
        Insert text at a location. You can use \r\n or \n in value and they will be normalized to the current document.
        """

        return self.replace(Range(location,location), value)
        