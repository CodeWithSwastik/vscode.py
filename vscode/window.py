from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable, List, Optional, Union

from vscode.enums import ViewColumn, ProgressLocation
from vscode.objects import QuickPickItem, QuickPickOptions, Position, Range, Selection

from vscode.webviews import WebviewPanel

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
        self._active_terminal = None
        self._active_text_editor = None

    @property
    async def active_terminal(self):
        res = await self.ws.run_code("vscode.window.activeTerminal", thenable=False)
        self._active_terminal = Terminal(res, self.ws, active=True)
        return self._active_terminal

    @property
    async def active_text_editor(self):
        res = await self.ws.run_code("vscode.window.activeTextEditor", thenable=False)
        self._active_text_editor = TextEditor(res, self.ws, active=True)
        return self._active_text_editor
    
    async def show(self, item):
        if not isinstance(item, Showable):
            raise ValueError(f"item must be a Showable")

        return await item._show(self.ws)

    async def create_webview_panel(self, webview_panel: WebviewPanel):
        if not isinstance(webview_panel, WebviewPanel):
            raise ValueError(f"webview_panel must be a WebviewPanel")
        
        await webview_panel._setup(self.ws)

    def progress(self, title: str, location: ProgressLocation = ProgressLocation.Window, cancellable: bool = False) -> Progress:
        return Progress(self.ws, title, location, cancellable)

class TextEditor:
    def __init__(self, data, ws, active) -> None:
        self._active = active
        self.ws = ws

        self.document = TextDocument(
            data=data["document"], 
            ws=ws, 
            editor_code="let editor = vscode.window.activeTextEditor;"
        )
        self.options = data.get("creationOptions")
        self.selection = data.get("selection")
        self.selections = data.get("selections")

        if self.selections:
            self.selections = [Selection.from_dict(s) for s in self.selections]
            self.selection = self.selections[0]

        self.view_column = ViewColumn(data.get("viewColumn"))
        self.visible_ranges = data.get("visibleRanges")
        if self.visible_ranges:
            self.visible_ranges = [
                Range(
                    start = Position.from_dict(r[0]), 
                    end = Position.from_dict(r[1])
                ) for r in self.visible_ranges
            ]

    @property
    def cursor(self) -> Position:
        """
        The cursor position of the 1st selection.
        """
        return self.selection.active

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
    def __init__(self, data, ws, editor_code) -> None:
        for key, val in data.items():
            setattr(self, key, val)

        self.ws = ws
        self._editor_code = editor_code

    async def get_text(self, range: Range) -> str:
        s = range.start
        e = range.end
        code = self._editor_code + \
            f"let range = new vscode.Range({s.line}, {s.character}, {e.line}, {e.character});" + \
            "editor.document.getText(range);"
        return await self.ws.run_code(code, thenable=False)

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
    def __init__(self, data, ws, active = True) -> None:
        self.ws = ws
        self._active = active

        self.name = data["name"]
        self.creation_options = data.get("creationOptions")
        self.exit_status = data.get("exitStatus")
        self.process_id = data.get("processID")
        self.state = data.get("state")
        self.dimensions = data.get("dimensions")


    async def dispose(self) -> None:
        await self.ws.run_code("vscode.window.activeTerminal.dispose()", wait_for_response=False)
         

    async def hide(self) -> None:
        await self.ws.run_code("vscode.window.activeTerminal.hide()", wait_for_response=False)

    async def send_text(self, text: str, add_new_line: bool = True):
        await self.ws.run_code(
            f"vscode.window.activeTerminal.sendText(\"{text}\", {str(add_new_line).lower()})", 
            wait_for_response=False
        )

    async def show(self, preserve_focus: bool = False) -> None:
        await self.ws.run_code(
            f"vscode.window.activeTerminal.show({str(preserve_focus).lower()})", 
            wait_for_response=False
        )

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
        options: Optional[QuickPickOptions] = None,
    ) -> None:
        self.items = [QuickPickItem(i) if isinstance(i, str) else i for i in items]
        self.options = options

    async def _show(self, ws) -> Optional[Union[QuickPickItem, List[QuickPickItem]]]:
        items = [i.to_dict() for i in self.items]

        options = "," + json.dumps(self.options.to_dict()) if self.options else ""

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

    def __post_init__(self):
        if not hasattr(self, "type"):
            self.type = "information"

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


class Progress:
    def __init__(self, ws, title: str, location: ProgressLocation = ProgressLocation.Window, cancellable: bool = False) -> None:
        self.ws = ws
        self.title = title
        self.cancellable = cancellable
        self.location = location

    async def __aenter__(self):
        await self.ws.run_code(
            f'''
            vscode.window.withProgress({{"location": {self.location.value}, "title": "{self.title}", "cancellable":{str(self.cancellable).lower()}}}, async (progress, token) => {{ 
                progressRecords["{self.title}"] = {{ "progress": progress, "token": token, "completed": false }};

                const checkProgressComplete = () => {{
                    return new Promise(resolve => {{
                        const interval = setInterval(() => {{
                            if (progressRecords["{self.title}"].completed) {{
                                console.log("Progress Complete");
                                clearInterval(interval);
                                resolve();
                            }}
                        }}, 100);
                    }});
                }};                                
                
                await checkProgressComplete();
            }});
            ''',
            thenable=False
        )
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.dispose()

    async def report(self, increment: int, message: str = ""):
        await self.ws.run_code(
            f'''
            progressRecords["{self.title}"].progress.report({{ increment: {increment}, message: "{message}" }});
            ''',
            thenable=False
        )

    async def dispose(self):
        await self.ws.run_code(
            f'''
            progressRecords["{self.title}"].completed = true;
            ''',
            thenable=False
        )