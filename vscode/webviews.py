from typing import Optional
from .utils import *

class Webview:
    def __init__(self, name: str):
        self.name = name

    def send_wb_ipc(self, code:str, args: list = None):
        if not hasattr(self,'ipc_id'):
            raise Exception("The Webview hasn't been created yet!")

        send_ipc("WB", [self.ipc_id, {"code": code, "args":args or []}])
        return json_input()
        
    def set_html(self, html: str):
        self.send_wb_ipc("SET-HTML", [html])

    def on_ready(self):
        pass

class StaticWebview:
    """
    Content settings for a Static Webview.
    """

    def __init__(self, id: str, html: str, title: Optional[str] = None) -> None:
        """
        Args:
            id: The unique id of the static webview.
            title: The title shown to the user.
            html: The html to rendered in the webview.
        """
        self.id = id
        self.html = html
        self.title = title