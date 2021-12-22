from dataclasses import dataclass
from typing import Literal, Optional

__all__ = ("Window", "Message", "InfoMessage", "WarningMessage", "ErrorMessage")


class Window:
    def __init__(self, ctx) -> None:
        self.ctx = ctx

    async def show(self, item):
        await self.ctx.ws.send(f"{item.content} {item.type}")

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
