import sys
import asyncio
from typing import Any, Callable, Optional, List

from vscode.context import Context
from vscode.wsclient import WSClient
from vscode.compiler import build
from vscode.config import Config
from vscode.utils import *

__all__ = ("ExtensionMetadata", "Extension", "Command")

class ExtensionMetadata:
    """
    Holds details of a vscode extension.

    Refer to https://code.visualstudio.com/api/references/extension-manifest for more details.
    """

    def __init__(
        self,
        version: str = "0.0.1",
        publisher: Optional[str] = None,
        engine: str = "^1.58.0",
        license: Optional[str] = None,
        display_name: Optional[str] = None,
        description: Optional[str] = None,
        categories: Optional[List[str]] = None,
        icon: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        preview: Optional[bool] = None,
        repository: Optional[str] = None,
    ) -> None:
        self.version = version
        self.repository = repository
        self.publisher = publisher
        self.engine = engine
        self.license = license
        self.display_name = display_name
        self.description = description
        self.categories = categories
        self.icon = icon
        self.keywords = keywords
        self.preview = preview

    def to_dict(self) -> dict:
        metadata = {}
        for key, value in self.__dict__.items():
            if value is not None:

                if key == "engine":
                    metadata["engines"] = {"vscode": value}
                elif key == "repository":
                    metadata["repository"] = {"url": value}
                elif key == "display_name":
                    pass
                else:
                    metadata[key] = value
        return metadata

class Extension:
    """
    Represents a vscode extension.
    """

    def __init__(self, name: str, *, metadata: Optional[ExtensionMetadata] = None, config: Optional[List[Config]] = None) -> None:
        self.name = name.lower().replace(" ", "-")
        self.metadata = metadata if metadata is not None else ExtensionMetadata()
        self.display_name = name if metadata is None or metadata.display_name is None else metadata.display_name

        self.config = [] if config is None else config
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
        command = Command(name, func, self, title, category, keybind, when)
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


    def set_default_category(self, category) -> None:
        """
        Set a default category for new commands.
        Args:
            category: The name of the default category.
        """
        self.default_category = category

    def run(self):
        if len(sys.argv) > 1:
            self.ws.run_webserver()
        else:
            build(self)

    async def parse_ws_data(self, data: dict):
        if data["type"] == 1: # Command 
            name = data.get("name")
            if any(name == (cmd:=i).name for i in self.commands):
                ctx = Context(ws=self.ws)
                ctx.command = cmd
                asyncio.create_task(cmd.func(ctx))
            else:
                print(f"Invalid Command '{name}'", flush=True)

        elif data["type"] == 2: # Event
            event = data.get("event").lower()
            if event in self.events:
                event_data = data.get("data")
                coro = self.events[event]
                if event_data:
                    coro = coro(event_data)
                else:
                    coro = coro()

                asyncio.create_task(coro)

        elif data["type"] == 3: # Eval Response:
            self.ws.responses[data["uuid"]] = data.get("res", None)
        elif data["type"] == 4: # Webview Event
            asyncio.create_task(self.ws.webviews[data["id"]].handle_event(data["name"], data.get("data", None)))
        else: # Unrecognized 
            print(data, flush=True)


class Command:
    """
    A class that implements the protocol for commands that can be used via the command palette.
    These should not be created manually, instead they should be created via the
    decorator or functional interface.
    """

    def __init__(
        self,
        name: str,
        func: Callable,
        ext: Extension,
        title: Optional[str] = None,
        category: Optional[str] = None,
        keybind: Optional[str] = None,
        when: Optional[str] = None,
    ):
        """
        Initialize a command.
        Args:
            name: 
                The internal name of the command.
            func: 
                The function to register as a command.
            ext: 
                The extension this command is registered in.
            title: 
                The title of the command. This is shown in the command palette.
            category: 
                The category that this command belongs to.
            keybind: 
                The keybind for this command.
            when: 
                A condition for when keybinds should be functional.
        """

        self.name = snake_case_to_camel_case(name)
        self.title = snake_case_to_title_case(name)
        self.ext = ext

        if not asyncio.iscoroutinefunction(func):
            raise TypeError("Callback must be a coroutine.")

        self.func = func
        self.func_name = self.func.__name__
        self.category = None if category is False else category
        self.keybind = keybind.upper() if keybind is not None else None
        self.when = python_condition_to_js_condition(when)

    def __repr__(self):
        return f"<vscode.Command {self.name}>"

    @property
    def extension_string(self) -> str:
        return f"{self.ext.name}.{self.name}"

    def to_dict(self) -> str:
        cmd = {"command": self.extension_string, "title": self.title}
        if self.category is not None:
            cmd.update({"category": self.category})
        return cmd
