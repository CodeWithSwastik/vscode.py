from typing import Optional
from .utils import *

class Webview:
    def __init__(self, name: str):
        self.name = name
        self.disposed = False
        # self.start_listening()

    def send_wb_ipc(self, code:str, args: list = None):
        if not hasattr(self,'ipc_id'):
            raise Exception("The Webview hasn't been created yet!")

        send_ipc("WB", [self.ipc_id, {"code": code, "args":args or []}])
        return json_input()

    def post_message(self, message:str):
        self.send_wb_ipc("POST-MSG", [message])

    # def listen_ipc(self):
    #     while not self.disposed:
    #         func = self.parse_ipc(json_input())
    #         if func:
    #             func()

    # def parse_ipc(self, res):
    #     print(res)
    #     if isinstance(res, dict) and res.get('name'):
    #         return getattr(self,res.get('name'))
    #     else:
    #         return None

    # def start_listening(self):
    #     self.listen_ipc()

    def on_ready(self):
        pass

    def set_html(self, html: str):
        self.send_wb_ipc("SET-HTML", [html])

    def set_title(self, title: str):
        self.send_wb_ipc("SET-TITLE", [title])

    def on_did_dispose(self):
        self.dispose()
    
    def dispose(self):
        self.disposed = True
        self.send_wb_ipc("DISPOSE")

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