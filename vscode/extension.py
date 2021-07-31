from .config import Config
from .types import *
from .utils import *
from typing import Optional, Callable, Union, List


class Extension:
    """Represents a vscode extension.

    A number of options can be passed to the `Extension`.
    """

    def __init__(
        self,
        name: str,
        display_name: str,
        version: str,
        description: Optional[str] = None,
        config: List[Config] = [],
        icon: Optional[str] = None,
        publisher: Optional[str] = None,
        repository: Optional[dict] = None,
    ) -> None:
        """
        Initialize the extension.

        Note:
            There must be no spaces in the extension name.

        Args:
            name: The name of the extension.
            display_name: The display name of the extension.
                This will be shown in the marketplace and to the user.
            version: The version of the extension.
                        config: a list of `Config` classes for the extension.
            icon : The icon for the extension.
            publisher: The name of the publisher of this extension.
            repository: The repository of this extension. This can be set with `set_repository`

        Raises:
            ValueError: If `name` has spaces.
        """
        if " " in name:
            raise ValueError(
                "The Extension name should not contain any spaces! If you want to include spaces please use the display_name attribute."
            )
        self.name = name
        self.display_name = display_name
        self.version = version
        self.description = description
        self.config = config
        self.icon = icon
        self.repository = repository
        self.publisher = publisher

        self.commands = []
        self.events = {}
        self.default_category = None
        self.keybindings = []
        self.activity_bar = None
        self.activity_bar_webview = None

    def register_command(
        self,
        func: Callable,
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
            func: The function to register as a command.
            name: The internal name of the command.
            title: The title of the command. This is shown in the command palette.
            category: The category that this command belongs to.
                Default categories set by Extensions will be overriden if this is not None.
                False should be passed in order to override a default category.
            keybind: The keybind for this command.
            when: A condition for when keybinds should be functional.
        """
        name = func.__name__ if name is None else name
        category = self.default_category if category is None else category
        command = Command(name, func, title, category, keybind, when)
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
            name: The internal name of the command.
            title: The title of the command. This is shown in the command palette.
            category: The category that this command belongs to.
                Default categories set by Extensions will be overriden if this is not None.
                False should be passed in order to override a default category.
            keybind: The keybind for this command.
            when: A condition for when keybinds should be functional.
        """

        def decorator(func):
            self.register_command(func, name, title, category, keybind, when)
            return func

        return decorator

    def event(self, func: Callable[[], str]):
        """
        A decorator for registering event handlers.
        """
        name = func.__name__.replace("on_", "")
        self.events[name] = func
        return func

    def get_config(self, target: str):
        """
        A method to get a configuration key.
        """
        send_ipc("GC", [self.name, target])
        return json_input()

    def register_keybind(self, command: "Command") -> None:
        """
        A method called internally to register a keybind.
        """
        keybind = {"command": command.extension(self.name), "key": command.keybind}
        if command.when:
            keybind.update({"when": command.when})
        self.keybindings.append(keybind)

    def set_repository(self, url: str, repo_type: str = "git") -> None:
        """
        A method to set a repository for the Extension.
        Args:
            url: The repository url.
            repo_type: The type of the repository.
        """
        self.repository = {"type": repo_type, "url": url}

    def set_default_category(self, category) -> None:
        """
        Set a default category for new commands.
        Args:
            category: The name of the default category.
        """
        self.default_category = category

    def set_activity_bar(
        self,
        activity_bar: Union[ActivityBar, dict],
        webview: Optional[Union[StaticWebview, dict]] = None,
    ) -> None:
        """
        Set an activity bar.
        """
        if isinstance(activity_bar, ActivityBar):
            self.activity_bar = activity_bar.__dict__
        elif isinstance(activity_bar, dict):
            self.activity_bar = activity_bar
        else:
            raise TypeError(
                "activity_bar must be either an instance of vscode.ActivityBar or dict"
            )
        if webview:
            if isinstance(webview, StaticWebview):
                self.activity_bar_webview = webview.__dict__
            elif isinstance(webview, dict):
                self.activity_bar_webview = webview
            else:
                raise TypeError(
                    "activity_bar_webview must be either an instance of vscode.StaticWebview or dict"
                )


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
        title: Optional[str] = None,
        category: Optional[str] = None,
        keybind: Optional[str] = None,
        when: Optional[str] = None,
    ):
        """
        Initialize a command.

        Args:
            name: The internal name of the command.
            func: The function to register as a command.
            title: The title of the command. This is shown in the command palette.
            category: The category that this command belongs to.
            keybind: The keybind for this command.
            when: A condition for when keybinds should be functional.
        """

        self.name = convert_snake_to_camel(name)
        self.title = convert_snake_to_title(name) if title is None else title
        self.func = func
        self.func_name = self.func.__name__
        self.category = None if category is False else category
        self.keybind = keybind.upper() if keybind is not None else None
        self.when = convert_python_condition(when) if when is not None else None

    def extension(self, ext_name: str) -> str:
        """
        The string representation for an extension.
        """
        return f"{ext_name}.{self.name}"

    def __repr__(self):
        return f"<vscode.Command {self.name}>"
