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

    def __eq__(self, other):
        return self.line == other.line and self.character == other.character

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

    def compare_to(self, other: Position) -> int:
        return 1 if self > other else -1 if self < other else 0

    def is_after(self, other: Position) -> bool:
        return self.compareTo(other) == 1

    def is_after_or_equal(self, other: Position) -> bool:
        return self.compareTo(other) in (0, 1)

    def is_before(self, other: Position) -> bool:
        return self.compareTo(other) == -1

    def is_before_or_equal(self, other: Position) -> bool:
        return self.compareTo(other) in (-1, 0)

    def is_equal(self, other: Position) -> bool:
        return self.compareTo(other) == 0

    def __repr__(self):
        return f"{self.line}:{self.character}"

    def translate(line_delta: int, character_delta: int) -> Position:
        pass


class Range(Object):
    def __init__(self, start: Position, end: Position):
        self.start = start
        self.end = end

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

    def intersection(self, other) -> Range:
        pass

    def union(self, other) -> Range:
        pass
