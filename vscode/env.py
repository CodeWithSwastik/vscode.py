import asyncio


class Env:
    def __init__(self, ws) -> None:
        self.ws = ws

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
    async def clipboard(self):
        return await self._get_property("clipboard")

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
