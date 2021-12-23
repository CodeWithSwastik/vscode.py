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

    def compareTo(self, other: Position) -> int:
        return 1 if self > other else -1 if self < other else 0
    
    def isAfter(self, other: Position) -> bool:
        return self.compareTo(other) == 1

    def isAfterOrEqual(self, other: Position) -> bool:
        return self.compareTo(other) in (0, 1)

    def isBefore(self, other: Position) -> bool:
        return self.compareTo(other) == -1

    def isBeforeOrEqual(self, other: Position) -> bool:
        return self.compareTo(other) in (-1, 0)

    def isEqual(self, other: Position) -> bool:
        return self.compareTo(other) == 0

    def __repr__(self):
        return f"{self.line}:{self.character}"

    def translate(lineDelta: int, characterDelta: int) -> Position:
        pass


class Range:
    def __init__(self, start: Position, end: Position):
        self.start = start
        self.end = end

    @property
    def isEmpty(self) -> bool:
        return self.start == self.end

    @property
    def inSingleLine(self) -> bool:
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

    async def insertSnippet(
        self,
        snippet,
        location: Union[Position, Range],
        *,
        undoStopAfter: bool = True,
        undoStopBefore: bool = True,
    ):
        pass

    async def revealRange(self, range: Range, revealType) -> Range:
        pass

    async def setDecorations(self, decorationType, rangesOrOptions):
        pass

    async def show(self, column: ViewColumn):
        pass


@dataclass
class TextLine:
    firstNonWhitespaceCharacterIndex: int
    isEmptyOrWhitespace: bool
    lineNumber: int
    range: Range
    rangeIncludingLineBreak: Range
    text: str


class TextDocument:
    def __init__(self, data) -> None:
        for key, val in data.items():
            setattr(key, val)

    async def getText(self, range: Range) -> str:
        pass

    async def getWordRangeAtPosition(self, position: Position, regex) -> Range:
        pass

    async def lineAt(self, lineOrPosition: Union[int, Position]) -> TextLine:
        pass

    async def offsetAt(self, position: Position) -> TextLine:
        pass

    async def positionAt(self, offset: int) -> Position:
        pass

    async def save(self):
        pass

    async def validatePosition(self, position):
        pass

    async def validateRange(self, range):
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
