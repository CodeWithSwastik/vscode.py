from dataclasses import dataclass
from typing import Literal, Optional

__all__ = ("Window", "Message", "InfoMessage", "WarningMessage", "ErrorMessage")


class Window:
    def __init__(self, ws) -> None:
        self.ws = ws

    async def show(self, item):
        await self.ws.run_code(item.jscode)


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
