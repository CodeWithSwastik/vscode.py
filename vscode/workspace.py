from typing import Optional, Union
from vscode.config import Config

class Workspace:
    def __init__(self, ws) -> None:
        self.ws = ws

    async def get_extension_configs(self, extension_name: Optional[str] = None):
        if extension_name is None:
            extension_name = self.ws.extension.name
            
        return await self.ws.run_code(f'vscode.workspace.getConfiguration("{extension_name}")', thenable=False)

    async def get_config_value(self, config: Union[str, Config]):
        if isinstance(config, Config):
            config = config.name
        
        return (await self.get_extension_configs()).get(config)


    async def get_workspace_folders(self):
        folders = await self.ws.run_code('vscode.workspace.workspaceFolders', thenable=False)
        return [WorkspaceFolder(**folder) for folder in folders] if folders is not None else []
    
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
    

class Uri:
    def __init__(self, uri):
        self._uri = uri

    def __repr__(self):
        return self._uri
    
    def __str__(self):
        return self._uri
    
    @property
    def fs_path(self):
        return self._uri.replace("file://", "")
    

class WorkspaceFolder:
    def __init__(self, index: int, name: str, uri: Union[Uri, dict]) -> None:
        self.index = index
        self.name = name
        self.uri: Uri = uri if isinstance(uri, Uri) else Uri(uri['fsPath']) # TODO: fix this
