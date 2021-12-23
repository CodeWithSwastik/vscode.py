from vscode.env import Env
from vscode.window import Window
from vscode.workspace import Workspace

__all__ = ("Context",)


class Context:
    def __init__(self, ws) -> None:
        self.ws = ws
        self.command = None
        self.window = Window(self.ws)
        self.env = Env(self.ws)
        self.workspace = Workspace(self.ws)

    @property
    def show(self):
        return self.window.show
