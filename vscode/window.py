from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Union

from .enums import ViewColumn

__all__ = ("Window", "Message", "InfoMessage", "WarningMessage", "ErrorMessage")


class Window:
    def __init__(self, ws) -> None:
        self.ws = ws

    async def show(self, item):
        await self.ws.run_code(item.jscode)


class Position:
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


class Range:
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


class TextEditor:
    def __init__(self, data) -> None:
        for key, val in data.items():
            setattr(key, val)

    async def edit(self, callback):
        pass

    async def reveal_range(self, range: Range, reveal_type) -> Range:
        pass

    async def show(self, column: ViewColumn):
        pass


@dataclass
class TextLine:
    first_non_whitespace_character_index: int
    is_empty_or_whitespace: bool
    line_number: int
    range: Range
    range_including_line_break: Range
    text: str


class TextDocument:
    def __init__(self, data) -> None:
        for key, val in data.items():
            setattr(key, val)

    async def get_text(self, range: Range) -> str:
        pass

    async def get_word_range_at_position(self, position: Position, regex) -> Range:
        pass

    async def line_at(self, line_or_position: Union[int, Position]) -> TextLine:
        pass

    async def offset_at(self, position: Position) -> TextLine:
        pass

    async def position_at(self, offset: int) -> Position:
        pass

    async def save(self):
        pass

    async def validate_position(self, position: Position) -> Position:
        pass

    async def validate_range(self, range: Range) -> Range:
        pass


@dataclass
class Message:
    content: str
    title: Optional[str] = None
    modal: Optional[bool] = None

    @property
    def jscode(self):
        return f'vscode.window.show{self.type.capitalize()}Message("{self.content}");'


@dataclass
class InfoMessage(Message):
    type = "information"


@dataclass
class WarningMessage(Message):
    type = "warning"


@dataclass
class ErrorMessage(Message):
    type = "error"
