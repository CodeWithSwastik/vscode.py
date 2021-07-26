class Extension:
    def __init__(self, name, display_name, version, description=""):
        self.name = name
        self.display_name = display_name
        self.version = version
        self.description = description
        self.commands = []
        self.events = {}
        self.default_category = None
        
    def register_command(self, func, name=None, title=None, category = None):
        name = func.__name__ if name is None else name
        category = self.default_category if category is None else category
        self.commands.append(Command(name, func, title, category))

    def command(self, name=None, title=None, category = None):
        def decorator(func):
            self.register_command(func, name, title, category)
            return func

        return decorator

    def event(self, func):
        name = func.__name__.replace("on_", "")
        self.events[name] = func
        return func

    def set_default_category(self, category=None):
        self.default_category = category if category is not None else self.display_name

class Command:
    def __init__(self, name, func, title=None, category=None):
        self.name = self.convert_snake_to_camel(name)
        if title is None:
            self.title = self.convert_snake_to_title(name)
        else:
            self.title = title

        self.func = func
        self.func_name = self.func.__name__
        self.category = None if category is False else category

    def extension(self, ext_name):
        return f"{ext_name}.{self.name}"

    def convert_snake_to_camel(self, text):
        temp = text.split("_")
        return temp[0] + "".join(ele.title() for ele in temp[1:])

    def convert_snake_to_title(self, text):
        return text.replace("_", " ").title()

    def __repr__(self):
        return f"<vscode.Command {self.name}>"
