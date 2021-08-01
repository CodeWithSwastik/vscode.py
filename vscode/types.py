import json
import time
from .utils import *
from typing import Optional
from enum import IntEnum

class ActivityBar:
    """
    Content settings for the activity bar.
    """

    def __init__(self, id: str, title: str, icon: str) -> None:
        """
        Args:
            id: The unique id of the activity bar.
            title: The title shown to the user.
            icon: The icon of the activity bar.
        """
        self.id = id
        self.title = title
        self.icon = icon


class StaticWebview:
    """
    Content settings for a Static Webview.
    """

    def __init__(self, id: str, html: str, title: Optional[str] = None) -> None:
        """
        Args:
            id: The unique id of the static webview.
            title: The title shown to the user.
            html: The html to rendered in the webview.
        """
        self.id = id
        self.html = html
        self.title = title


class InputBoxOptions:
    """
    Options to configure the behavior of the input box UI.
    """

    def __init__(
        self,
        title: Optional[str] = None,
        password: Optional[bool] = None,
        ignore_focus_out: Optional[bool] = None,
        prompt: Optional[str] = None,
        place_holder: Optional[str] = None,
        value: Optional[str] = None,
    ) -> None:
        """
        Args:
            title: An optional string that represents the title of the input box.
            password: Controls if a password input is shown. Password input hides the typed text.
            ignore_focus_out: Set to True to keep the input box open when focus moves to another part of the editor or to another window. This setting is ignored on iPad and is always False.
            place_holder: An optional string to show as placeholder in the input box to guide the user what to type.
            prompt: The text to display underneath the input box.
            value: The value to prefill in the input box.
        """
        self.title = title
        self.password = password
        self.ignoreFocusOut = ignore_focus_out
        self.prompt = prompt
        self.placeHolder = place_holder
        self.value = value


class QuickPickOptions:
    """
    Options to configure the behavior of the quick pick UI.
    """

    def __init__(
        self,
        title: Optional[str] = None,
        can_pick_many: Optional[bool] = None,
        ignore_focus_out: Optional[bool] = None,
        match_on_description: Optional[bool] = None,
        place_holder: Optional[str] = None,
        match_on_detail: Optional[bool] = None,
    ) -> None:
        """
        Args:
            title: An optional string that represents the title of the quick pick.
            can_pick_many: An optional flag to make the picker accept multiple selections, if true the result is an array of picks.
            ignore_focus_out: Set to True to keep the input box open when focus moves to another part of the editor or to another window. This setting is ignored on iPad and is always False.
            place_holder: An optional string to show as placeholder in the input box to guide the user what to type.
            match_on_description: An optional flag to include the description when filtering the picks.
            match_on_detail: An optional flag to include the detail when filtering the picks.
        """
        self.title = title
        self.canPickMany = can_pick_many
        self.ignoreFocusOut = ignore_focus_out
        self.matchOnDescription = match_on_description
        self.placeHolder = place_holder
        self.matchOnDetail = match_on_detail


class QuickPickItem:
    """
    Represents an item that can be selected from a list of items.
    """

    def __init__(
        self,
        label: Optional[str] = None,
        detail: Optional[str] = None,
        description: Optional[str] = None,
        **options,
    ) -> None:
        self.label = label
        self.detail = detail
        self.description = description
        self.__dict__.update(options)


class OpenDialogOptions:
    """
    Options to configure the behaviour of a file open dialog.

    Note:
        On Windows and Linux, a file dialog cannot be both a file selector and a folder selector, so if you set both canSelectFiles and canSelectFolders to true on these platforms, a folder selector will be shown.
        Explicitly setting can_select_files and can_select_folders to false is futile and the editor then silently adjusts the options to select files.
    """

    def __init__(
        self,
        title: str = None,
        can_select_many: bool = None,
        can_select_files: bool = True,
        can_select_folders: bool = False,
        open_label: str = None,
        filters: Optional[dict] = None,
        default_uri: str = None,
    ) -> None:
        self.title = title
        self.canSelectMany = can_select_many
        self.canSelectFiles = can_select_files
        self.canSelectFolders = can_select_folders
        self.openLabel = open_label
        self.filters = filters if filters is not None else {}
        self.defaultUri = default_uri


class SaveDialogOptions:
    """
    Options to configure the behaviour of a file save dialog.
    """

    def __init__(
        self,
        title: str = None,
        save_label: str = None,
        filters: Optional[dict] = None,
        default_uri: str = None,
    ) -> None:
        self.title = title
        self.saveLabel = save_label
        self.filters = filters if filters is not None else {}
        self.defaultUri = default_uri

class ViewColumn(IntEnum):
    active = -1
    beside = -2
    eight = 8
    five = 5
    four = 4
    nine = 9
    one = 1 
    seven = 7
    six = 6
    three = 3
    two = 2

class Disposable:
    """
    Represents a type which can release resources, such as event listening or a timer.
    """

    def __init__(self, id):
        self.id = id

    def dispose(self):
        send_ipc("DI", [self.id])
        time.sleep(0.1) # Makes sure it is properly disposed.

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        self.dispose()

class Position:
    """
    Represents a line and character position, such as the position of the cursor.
    """

    def __init__(self, line: int, character: int):
        self.line = line
        self.character = character

    @staticmethod
    def from_dict(data: dict):
        pos = Position(0, 0)
        pos.__dict__.update(data)
        return pos

    def __eq__(self, other):
        return self.line == other.line and self.character == other.character

    def __sub__(self, other):
        return self.compare(other)

    def __lt__(self, other):
        return self.line < other.line or (
            self.line == other.line and self.character < other.character
        )

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def compare(self, other):
        return 1 if self > other else -1 if self < other else 0

    def __repr__(self):
        return f"{self.line}:{self.character}"


class Range:
    "A range represents an ordered pair of two positions. It is guaranteed that start.isBeforeOrEqual(end)"

    def __init__(self, start: Position, end: Position):
        self.start = start
        self.end = end

    @staticmethod
    def from_dict(data):
        return Range(Position.from_dict(data["start"]), Position.from_dict(data["end"]))

    @property
    def __dict__(self):
        return {"start": self.start.__dict__, "end": self.end.__dict__}

    @property
    def is_empty(self):
        return self.start == self.end

    @property
    def in_single_line(self):
        return self.start.line == self.end.line

    def __repr__(self):
        return f"[{self.start},{self.end}]"

    def __eq__(self, other):
        return self.start == other.start and self.end == other

    def __contains__(self, other):
        if isinstance(other, Position):
            return self.start <= other <= self.end
        else:
            return self.start <= other.start and self.end >= other.end

    def intersection(self, other):
        if self.end < other.start or other.end < self.start:
            return undefined

        start = max(self.start, other.start)
        end = min(self.end, other.end)

        return Range(start, end)

    def union(self, other):
        start = min(self.start, other.start)
        end = max(self.end, other.end)

        return Range(start, end)


class Selection(Range):
    """
    Represents a text selection in an editor.
    """

    def __init__(
        self, active: Position, anchor: Position, start: Position, end: Position
    ):
        self.active = active
        self.anchor = anchor
        self.start = start
        self.end = end

    @staticmethod
    def from_dict(data):
        return Selection(
            Position.from_dict(data["active"]),
            Position.from_dict(data["anchor"]),
            Position.from_dict(data["start"]),
            Position.from_dict(data["end"]),
        )

    @property
    def __dict__(self):
        return {
            "active": self.active.__dict__,
            "anchor": self.anchor.__dict__,
            "start": self.start.__dict__,
            "end": self.end.__dict__,
        }

    def is_reversed(self):
        return self.active < self.anchor


class TextLine:
    """
    Represents a line of text, such as a line of source code.

    TextLine objects are immutable. When a document changes, previously retrieved lines will not represent the latest state.
    """

    def __init__(self, data):
        self.__dict__.update(apply_func_to_keys(data, camel_to_snake))


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
            send_ipc("GT", [location])
        else:
            send_ipc("GT")

        return json_input()

    def line_at(self, location) -> TextLine:
        """
        Returns a text line denoted by the line number or Position. Note that the returned object is not live and changes to the document are not reflected.

        Note: If location.line > TextDocument.line_count, the last line will be returned.
        """
        if isinstance(location, Position):
            location = location.line
        if location >= self.line_count:
            location = self.line_count - 1
        send_ipc("LA", [location])
        return TextLine(json_input())

    # TODO: TextDocument methods

class TextDocumentShowOptions: 
    """
    Represents options to configure the behavior of showing a document in an editor.
    """

    def __init__(
        self,
        preserve_focus: Optional[bool] = None,
        preview: Optional[bool] = None,
        selection: Optional[Range] = None,
        view_column:  Optional[ViewColumn] = None,
    ) -> None:
        self.preserveFocus = preserve_focus
        self.preview = preview
        self.selection = selection
        self.viewColumn = view_column.value if view_column is not None else None  
