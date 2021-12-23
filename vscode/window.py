from dataclasses import dataclass
from typing import Literal, Optional

__all__ = ("Window", "Message", "InfoMessage", "WarningMessage", "ErrorMessage")


class Window:
    def __init__(self, ws) -> None:
        self.ws = ws

    async def show(self, item):
        code = f'vscode.window.showInformationMessage("{item.content} {item.type}");'
        await self.ws.send(type=1, code=code)

@dataclass
class Message:
    content: str
    title: Optional[str] = None
    modal: Optional[bool] = None

@dataclass
class InfoMessage(Message):
    type = "information"

@dataclass
class WarningMessage(Message):
    type = "warning"

@dataclass
class ErrorMessage(Message):
    type = "error"
