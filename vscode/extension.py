import sys
import asyncio
from typing import Any, Callable, Optional, List, Coroutine

import vscode
from vscode.context import Context
from vscode.wsclient import WSClient
from vscode.utils import *

from pydantic import BaseModel, Field, validator, constr

__all__ = ("Extension", "Command", "Launch")

SEMVER_REGEX = "^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"


class Extension:
    """
    Represents a vscode extension.
    """

    def __init__(self, name: str) -> None:
        self.name = name.lower().replace(" ", "-")
        self.display_name = name

        self.commands = []
        self.events = {}
        self.default_category = None
        self.keybindings = []

        self.ws = WSClient(self)

    def __repr__(self):
        return f"<vscode.Extension {self.name}>"

    def register_command(
        self,
        func: Callable[..., Any],
        name: Optional[str] = None,
        title: Optional[str] = None,
        category: Optional[str] = None,
        keybind: Optional[str] = None,
        when: Optional[str] = None,
    ) -> None:
        """
        Register a command.
        This is usually not called, instead the command() shortcut decorators should be used instead.
        Args:
            func:
                The function to register as a command.
            name:
                The internal name of the command.
            title:
                The title of the command. This is shown in the command palette.
            category:
                The category that this command belongs to.
                Default categories set by Extensions will be overriden if this is not None.
                False should be passed in order to override a default category.
            keybind:
                The keybind for this command.
            when:
                A condition for when keybinds should be functional.
        """
        name = func.__name__ if name is None else name
        category = self.default_category if category is None else category
        command = Command(
            name=name,
            func=func,
            ext=self,
            title=title,
            category=category,
            keybind=keybind,
            when=when,
        )
        if keybind:
            self.register_keybind(command)
        self.commands.append(command)

    def command(
        self,
        name: Optional[str] = None,
        title: Optional[str] = None,
        category: Optional[str] = None,
        keybind: Optional[str] = None,
        when: Optional[str] = None,
    ):
        """
        A decorator for registering commands.
        Args:
            name:
                The internal name of the command.
            title:
                The title of the command. This is shown in the command palette.
            category:
                The category that this command belongs to.
                Default categories set by Extensions will be overriden if this is not None.
                False should be passed in order to override a default category.
            keybind:
                The keybind for this command.
            when:
                A condition for when keybinds should be functional.
        """

        def decorator(func):
            self.register_command(func, name, title, category, keybind, when)
            return func

        return decorator

    def register_keybind(self, command: "Command") -> None:
        """
        A method called internally to register a keybind.
        """
        keybind = {"command": command.extension_string, "key": command.keybind}
        if command.when:
            keybind.update({"when": command.when})
        self.keybindings.append(keybind)

    def event(self, func: Callable):
        """
        A decorator for registering event handlers.
        """
        name = func.__name__.replace("on_", "").lower()
        self.events[name] = func
        return func

    def run(self):
        if len(sys.argv) > 1:
            self.ws.run_webserver()
        else:
            vscode.compiler.build(self)

    async def parse_ws_data(self, data: dict):
        if data["type"] == 1:  # Command
            name = data.get("name")
            if any(name == (cmd := i).name for i in self.commands):
                ctx = Context(ws=self.ws)
                ctx.command = cmd
                asyncio.create_task(cmd.func(ctx))
            else:
                print(f"Invalid Command '{name}'", flush=True)

        elif data["type"] == 2:  # Event
            event = data.get("event").lower()
            if event in self.events:
                event_data = data.get("data")
                coro = self.events[event]
                if event_data:
                    coro = coro(event_data)
                else:
                    coro = coro()

                asyncio.create_task(coro)

        elif data["type"] == 3:  # Eval Response:
            self.ws.responses[data["uuid"]] = data.get("res", None)
        else:  # Unrecognized
            print(data, flush=True)


class Command(BaseModel):
    """
    A class that implements the protocol for commands that can be used via the command palette.
    These should not be created manually, instead they should be created via the
    decorator or functional interface.
    """

    name: str = Field(..., description="The internal name of the command.")
    func: Coroutine = Field(..., description="The function to register as a command.")
    ext: Extension = Field(
        ..., description="The extension this command is registered in."
    )
    title: Optional[str] = Field(
        description="The title of the command. This is shown in the command palette."
    )
    category: Optional[str] = Field(
        description="The category that this command belongs to."
    )
    keybind: Optional[str] = Field(description="The keybind for this command")
    when: Optional[str] = Field(
        description="A condition for when keybinds should be functional."
    )
    command: Optional[str] = Field(
        description="The command to execute when triggered. This field is autogenerated."
    )
    func_name: Optional[str] = Field(
        description="The function to execute when triggered. This field is autogenerated."
    )

    @validator("name")
    def name_convert(cls, v):
        return snake_case_to_camel_case(v)

    @validator("title")
    def title_convert(cls, v):
        return snake_case_to_title_case(v)

    @validator("when")
    def when_convert(cls, v):
        return python_condition_to_js_condition(v)

    @validator("keybind")
    def keybind_convert(cls, v):
        return None if v is None else v.upper()

    @validator("func", pre=True)
    def func_is_coroutine(cls, v):
        print(v.__name__)
        print(type(v))
        assert asyncio.iscoroutine(v)
        return v

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)

        self.func_name = self.func.__name__
        self.command = f"{self.ext.name}.{self.name}"


class Configuration(BaseModel):

    name: str = "Run Extension"
    type: str = "extensionHost"
    request: str = "launch"
    args: List[str] = ["--extensionDevelopmentPath=${workspaceFolder}"]


class Launch(BaseModel):

    version: constr(regex=SEMVER_REGEX) = "0.2.0"
    configurations: List[Configuration] = [Configuration()]
