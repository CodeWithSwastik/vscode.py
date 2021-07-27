from .interfaces import *


class Extension:
    def __init__(self, name, display_name, version, description=None, icon=None, repository = None):
        self.name = name
        self.display_name = display_name
        self.version = version
        self.description = description
        self.icon = icon
        self.repository = repository

        self.commands = []
        self.events = {}
        self.default_category = None
        self.keybindings = []
        self.activity_bar = None
        self.activity_bar_webview = None

    def register_command(
        self, func, name=None, title=None, category=None, keybind=None, when=None
    ):
        name = func.__name__ if name is None else name
        category = self.default_category if category is None else category
        command = Command(name, func, title, category, keybind, when)
        if keybind:
            self.register_keybind(command)
        self.commands.append(command)

    def command(self, name=None, title=None, category=None, keybind=None, when=None):
        def decorator(func):
            self.register_command(func, name, title, category, keybind, when)
            return func

        return decorator

    def event(self, func):
        name = func.__name__.replace("on_", "")
        self.events[name] = func
        return func

    def register_keybind(self, command):
        keybind = {"command": command.extension(self.name), "key": command.keybind}
        if command.when:
            keybind.update({"when": command.when})
        self.keybindings.append(keybind)

    def set_repository(self, url):
        self.repository = {'type': 'git', 'url': url}

    def set_default_category(self, category):
        self.default_category = category

    def set_activity_bar(self, activity_bar, webview=None):
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
    def __init__(self, name, func, title=None, category=None, keybind=None, when=None):
        self.name = self.convert_snake_to_camel(name)
        if title is None:
            self.title = self.convert_snake_to_title(name)
        else:
            self.title = title

        self.func = func
        self.func_name = self.func.__name__
        self.category = None if category is False else category
        self.keybind = keybind.upper() if keybind is not None else None
        self.when = self.convert_python_condition(when) if when is not None else None

    def extension(self, ext_name):
        return f"{ext_name}.{self.name}"

    def convert_snake_to_camel(self, text):
        temp = text.split("_")
        return temp[0] + "".join(ele.title() for ele in temp[1:])

    def convert_snake_to_title(self, text):
        return text.replace("_", " ").title()

    def convert_python_condition(self, condition):
        condition = " ".join(
            i if "_" not in i else self.convert_snake_to_camel(i)
            for i in condition.split(" ")
        )
        condition = condition.replace(" and ", " && ")
        condition = condition.replace(" or ", " || ")
        if " not " in condition:
            if not ("(" in condition and ")" in condition):
                raise SyntaxError(
                    "Use parenthesis '()' while using 'not' otherwise your conditions might not work as expected!"
                )
            else:
                condition = condition.replace(" not ", " !")

        return condition

    def __repr__(self):
        return f"<vscode.Command {self.name}>"
