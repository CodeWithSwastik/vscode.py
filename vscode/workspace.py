from typing import Optional


class Workspace:
    def __init__(self, ws) -> None:
        self.ws = ws

    

    async def open_text_document(self, file):
        return await self.ws.run_code(f'vscode.workspace.openTextDocument("{file}")')

    async def open_untitled_text_document(
        self, 
        content: Optional[str] = None, 
        language: Optional[str] = None
    ):
        obj = {}
        if content:
            obj["content"] = content
        if language:
            obj["language"] = language
    
        return await self.ws.run_code(f'vscode.workspace.openTextDocument({obj})')