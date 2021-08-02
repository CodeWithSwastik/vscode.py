from typing import Optional

class Webview:
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