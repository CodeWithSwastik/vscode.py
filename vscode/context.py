from vscode.window import Window

__all__ = ("Context",)


class Context:
    def __init__(self, ws) -> None:
        self.ws = ws
        self.command = None
        self.window = Window(self)

    @property
    def show(self):
        return self.window.show
