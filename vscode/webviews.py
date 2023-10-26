import uuid
from .enums import ViewColumn

__all__ = (
    "WebviewPanel",
)

class WebviewPanel:
    def __init__(self, title: str, colomn: ViewColumn) -> None:
        self.title = title
        self.colomn = colomn
        self._html = ""
        self.id = str(uuid.uuid4())
        self.ws = None
        self.running = False

    @property
    def html(self) -> str:
        return self._html
    
    async def _setup(self, ws) -> None:
        self.ws = ws
        await self.ws.run_code(
            f"""
            let p = vscode.window.createWebviewPanel('{self.id}', '{self.name}', {self.colomn}, {{ enableScripts: true }}); 
            webviews['{self.id}'] = p;
            """
            )
        self.running = True

    async def set_html(self, html: str) -> None:
        if not self.running:
            raise ValueError(f"Webview is not running")
        
        self._html = html
        await self.ws.run_code(f"webviews['{self.id}'].webview.html = `{html}`")

    async def update_title(self, title: str) -> None:
        if not self.running:
            raise ValueError(f"Webview is not running")
        
        self.title = title
        await self.ws.run_code(f"webviews['{self.id}'].title = '{title}'")