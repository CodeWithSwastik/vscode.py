class Clipboard:
    def __init__(self, ws) -> None:
        self.ws = ws

    async def read(self):
        return await self.ws.run_code("vscode.env.clipboard.readText()")

    async def write(self, text: str):
        await self.ws.run_code(
            f"vscode.env.clipboard.writeText(`{text}`)", wait_for_response=False
        )


class Env:
    def __init__(self, ws) -> None:
        self.ws = ws
        self.clipboard = Clipboard(self.ws)

    async def _get_property(self, property):
        return await self.ws.run_code(f"vscode.env.{property}", thenable=False)

    @property
    async def app_host(self):
        return await self._get_property("appHost")

    @property
    async def app_name(self):
        return await self._get_property("appName")

    @property
    async def app_root(self):
        return await self._get_property("appRoot")

    @property
    async def is_new_app_install(self) -> bool:
        return await self._get_property("isNewAppInstall")

    @property
    async def is_telemetry_enabled(self) -> bool:
        return await self._get_property("isTelemetryEnabled")

    @property
    async def language(self):
        return await self._get_property("language")

    @property
    async def machine_id(self):
        return await self._get_property("machineId")

    @property
    async def remote_name(self):
        return await self._get_property("remoteName")

    @property
    async def session_id(self):
        return await self._get_property("sessionId")

    @property
    async def shell(self):
        return await self._get_property("shell")

    @property
    async def ui_kind(self):
        return await self._get_property("uiKind")

    @property
    async def uri_scheme(self):
        return await self._get_property("uriScheme")

    async def open_external(self, uri) -> bool:
        return await self.ws.run_code(f'vscode.env.openExternal("{uri}")')
