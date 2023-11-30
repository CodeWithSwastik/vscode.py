from __future__ import annotations

from typing import Optional
from vscode.utils import snake_case_to_camel_case

__all__ = ("Object", "QuickPickItem", "QuickPickOptions", "Position", "Range")


class Object:
    """
    Represents a generic vscode object.
    """

    def __repr__(self):
        return f"<vscode.{self.__class__.__name__}>"

    def to_dict(self) -> dict:
        return {snake_case_to_camel_case(k): v for k, v in self.__dict__.items()}


class QuickPickItem(Object):
    def __init__(
        self,
        label: str,
        always_show: Optional[bool] = None,
        description: Optional[str] = None,
        detail: Optional[str] = None,
        picked: Optional[bool] = None,
        **kwargs,
    ):
        self.label = label
        self.always_show = always_show or kwargs.pop("alwaysShow", None)
        self.detail = detail
        self.description = description
        self.picked = picked
        self.__dict__.update(kwargs)


class QuickPickOptions(Object):
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
        self.can_pick_many = can_pick_many
        self.ignore_focus_out = ignore_focus_out
        self.match_on_description = match_on_description
        self.place_holder = place_holder
        self.match_on_detail = match_on_detail


class Position(Object):
    def __init__(self, line: int, character: int):
        self.line = line
        self.character = character

    @staticmethod
    def from_dict(data):
        return Position(data["line"], data["character"])

    def to_dict(self):
        return {"line": self.line, "character": self.character}

    def __eq__(self, other):
        return self.line == other.line and self.character == other.character

    def __lt__(self, other):
        return self.line < other.line or (
            self.line == other.line and self.character < other.character
        )

    def __le__(self, other):
        return self == other or self < other

    def compare_to(self, other: Position) -> int:
        return 1 if self > other else -1 if self < other else 0

    def __repr__(self):
        return f"{self.line}:{self.character}"

    def translate(self, line_delta: int, character_delta: int) -> Position:
        return Position(self.line + line_delta, self.character + character_delta)


class Range(Object):
    def __init__(self, start: Position, end: Position):
        self.start = start
        self.end = end
    
    @staticmethod
    def from_dict(data):
        start = Position.from_dict(data["start"])
        end = Position.from_dict(data["end"])
        return Range(start, end)

    def to_dict(self):
        return {"start": self.start.to_dict(), "end": self.end.to_dict()}

    @property
    def is_empty(self) -> bool:
        return self.start == self.end

    @property
    def in_single_line(self) -> bool:
        return self.start.line == self.end.line

    def __eq__(self, other):
        return self.start == other.start and self.end == other

    def __contains__(self, other):
        if isinstance(other, Position):
            return self.start <= other <= self.end
        else:
            return self.start <= other.start and self.end >= other.end

    def intersection(self, other) -> Optional[Range]:
        if self.end < other.start or other.end < self.start:
            return None

        start = max(self.start, other.start)
        end = min(self.end, other.end)

        return Range(start, end)

    def union(self, other) -> Range:
        start = min(self.start, other.start)
        end = max(self.end, other.end)

        return Range(start, end)

    def __repr__(self):
        return f"<vscode.{self.__class__.__name__} [{self.start} -> {self.end}]>"

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

    def to_dict(self):
        return {
            "active": self.active.to_dict(),
            "anchor": self.anchor.to_dict(),
            "start": self.start.to_dict(),
            "end": self.end.to_dict(),
        }

    def is_reversed(self):
        return self.active < self.anchor