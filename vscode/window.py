from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterable, List, Optional, Union
from vscode.objects import QuickPickItem, QuickPickOptions

if TYPE_CHECKING:
    from vscode.objects import Position, Range


from .enums import ViewColumn

__all__ = (
    "Window",
    "TextEditor",
    "TextDocument",
    "TextLine",
    "Terminal",
    "QuickPick",
    "InputBox",
    "WindowState",
    "Message",
    "InfoMessage",
    "WarningMessage",
    "ErrorMessage",
)


class Showable(ABC):
    @abstractmethod
    async def _show(self, ws):
        ...


class Window:
    def __init__(self, ws) -> None:
        self.ws = ws

    async def show(self, item):
        if not isinstance(item, Showable):
            raise ValueError(f"item must be a Showable")

        return await item._show(self.ws)


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


class Terminal:
    def __init__(self, data) -> None:
        for key, val in data.items():
            setattr(key, val)

    async def dispose(self):
        pass

    async def hide(self):
        pass

    async def send_text(self, text: str, add_new_line: bool):
        pass

    async def show(self, preserve_focus: bool):
        pass


class QuickInput:
    def __init__(self) -> None:
        pass

    async def dispose(self):
        pass

    async def hide(self):
        pass

    async def show(self):
        pass


class QuickPick(Showable, QuickInput):
    def __init__(
        self, 
        items: List[str, QuickPickItem], 
        options: Optional[QuickPickOptions] = None
    ) -> None:  
        self.items = [QuickPickItem(i) if isinstance(i, str) else i for i in items]
        self.options = options

    async def _show(self, ws) -> Optional[Union[QuickPickItem, List[QuickPickItem]]]:
        items = [
            i.to_dict() for i in self.items
        ]

        options = ','+json.dumps(self.options.to_dict()) if self.options else ''

        chosen = await ws.run_code(
            f"vscode.window.showQuickPick({json.dumps(items)}{options})",
        )
        if chosen:
            if isinstance(chosen, dict):
                return QuickPickItem(**chosen)
            else:
                return [QuickPickItem(**r) for r in chosen]


class InputBox(Showable, QuickInput):
    def __init__(
        self,
        title: Optional[str] = None,
        password: Optional[bool] = None,
        ignore_focus_out: Optional[bool] = None,
        prompt: Optional[str] = None,
        place_holder: Optional[str] = None,
        value: Optional[str] = None,
    ) -> None:
        self.title = title
        self.password = password
        self.ignore_focus_out = ignore_focus_out
        self.prompt = prompt
        self.place_holder = place_holder
        self.value = value

    async def _show(self, ws):
        options_dict = {
            "title": self.title,
            "password": self.password,
            "ignoreFocusOut": self.ignore_focus_out,
            "prompt": self.prompt,
            "placeHolder": self.place_holder,
            "value": self.value,
        }
        return await ws.run_code(
            f"vscode.window.showInputBox({json.dumps(options_dict)})"
        )


@dataclass
class WindowState:
    focused: bool


@dataclass
class Message(Showable):
    content: str
    items: Optional[Iterable] = None

    async def _show(self, ws):
        base = f'vscode.window.show{self.type.capitalize()}Message("{self.content}"'
        if self.items:
            return await ws.run_code(
                base + "".join(f', "{i}"' for i in self.items) + ")",
            )
        else:
            return await ws.run_code(base + ")", wait_for_response=False)


@dataclass
class InfoMessage(Message):
    type = "information"


@dataclass
class WarningMessage(Message):
    type = "warning"


@dataclass
class ErrorMessage(Message):
    type = "error"
