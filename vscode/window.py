from .types import *
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

    if not options:
        options = {}

    if isinstance(options, QuickPickOptions):
        options = options.__dict__
    send_ipc("QP", [data, options])

    res = json_input()
    if not res or isinstance(res, str):
        return res
    elif isinstance(res, dict):
        return QuickPickItem(**res)
    else:
        data = [QuickPickItem(**r) if isinstance(r, dict) else r for r in res]
        return data


def show_input_box(options: InputBoxOptions = None) -> str:
    """
    Opens an input box to ask the user for input.

    The returned value will be undefined if the input box was canceled (e.g. pressing ESC). Otherwise the returned value will be the string typed by the user or an empty string if the user did not type anything but dismissed the input box with OK.
    """
    if not options:
        options = {}
    if isinstance(options, InputBoxOptions):
        options = options.__dict__
    send_ipc("IB", [options])
    return json_input()


def _base(func: str, text: str, *args: str) -> str:
    send_ipc("SM", [func, text, *args])
    return json_input()


def show_info_message(text: str, *args: str) -> str:
    """
    Show an information message.
    """
    return _base("showInformationMessage", text, *args)


def show_warn_message(text: str, *args: str) -> str:
    """
    Show a warning message.
    """
    return _base("showWarningMessage", text, *args)


def show_error_message(text: str, *args: str) -> str:
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
    args = (
        [text, hide_after_timeout * 1000] if hide_after_timeout is not None else [text]
    )
    send_ipc("BM", args)
    res = json_input()
    return Disposable(res)


def show_open_dialog(options: OpenDialogOptions = None) -> list:
    if isinstance(options, OpenDialogOptions):
        options = options.__dict__
    elif options is None:
        options = {}

    send_ipc("SM", ["showOpenDialog", options])
    return json_input()


def show_save_dialog(options: SaveDialogOptions = None) -> dict:
    if isinstance(options, SaveDialogOptions):
        options = options.__dict__
    elif options is None:
        options = {}
    send_ipc("SM", ["showSaveDialog", options])
    return json_input()

class TextEditor:

    def __init__(self, data: dict = None):
        if not data:
            send_ipc("AT", [])
            res = json_input()
            if not res:
                self = undefined
        else:
            res = data
        self.__dict__.update(apply_func_to_keys(res, camel_to_snake))
        self.document = TextDocument(self.document)
        if hasattr(self, "selections"):
            data = [Selection.from_dict(sel) for sel in self.selections]
            self.selections = data
            self.selection = data[0]


    @property
    def cursor(self) -> Position:
        """
        The cursor position of the 1st selection.
        """
        return self.selection.active

    def replace(self, location: Range, value: str) -> bool:
        """
        Replace a certain text region with a new value.
        You can use \\r\\n or \\n in value and they will be normalized to the current document.
        """

        if isinstance(location, Range):
            location = location.__dict__
        send_ipc("EE", [location, value])
        return eval(json_input().title())

    def delete(self, location: Range) -> bool:
        """
        Delete a certain text region.
        """
        return self.replace(location, "")

    def insert(self, location: Position, value: str) -> bool:

        """
        Insert text at a location. You can use \\r\\n or \\n in value and they will be normalized to the current document.
        """

        return self.replace(Range(location, location), value)

class ActiveTextEditor(TextEditor):
    """
    The currently active editor or undefined. The active editor is the one that currently has focus or, when none has focus, the one that has changed input most recently.
    """
    pass

def show_text_document(uri: str, options: Optional[TextDocumentShowOptions] = None) -> TextEditor:
    if isinstance(options, TextDocumentShowOptions):
        options = options.__dict__
    elif options is None:
        options = {}
    send_ipc("ST", [uri, options])
    return TextEditor(json_input())