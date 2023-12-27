from vscode.env import Env
from vscode.window import Window
from vscode.workspace import Workspace

__all__ = ("Context",)


class Context:
    """
    Represents the context in which a command is being invoked under.

    This class is not created manually and is instead passed around to commands as the first parameter.
    
    This class is the python equivalent of the `vscode` module in the JavaScript API i.e. vscode.window becomes context.window and so on.
    """
    def __init__(self, ws) -> None:
        self.ws = ws
        self.command = None
        self.window = Window(self.ws)
        self.env = Env(self.ws)
        self.workspace = Workspace(self.ws)

    @property
    def show(self):
        return self.window.show
