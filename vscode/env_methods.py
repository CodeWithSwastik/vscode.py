from .utils import *


class Env:
    def open_external(self, target: str) -> None:
        """
        Open an external url with the device's default browser
        """
        send_ipc("OE", [target])

    @property
    def app_name(self):
        send_ipc("EP", ["appName"])
        return json_input()

    @property
    def app_root(self):
        send_ipc("EP", ["appRoot"])
        return json_input()

    @property
    def clipboard(self):
        send_ipc("EP", ["clipboard"])
        return json_input()

    @property
    def is_new_app_install(self) -> bool:
        send_ipc("EP", ["isNewAppInstall"])
        return eval(json_input().title())

    @property
    def is_telemetry_enabled(self) -> bool:
        send_ipc("EP", ["isTelemetryEnabled"])
        return eval(json_input().title())

    @property
    def language(self):
        send_ipc("EP", ["language"])
        return json_input()

    @property
    def machine_id(self):
        send_ipc("EP", ["machineId"])
        return json_input()

    @property
    def remote_name(self):
        send_ipc("EP", ["remoteName"])
        return json_input()

    @property
    def session_id(self):
        send_ipc("EP", ["sessionId"])
        return json_input()

    @property
    def shell(self):
        send_ipc("EP", ["shell"])
        return json_input()

    @property
    def ui_kind(self):
        send_ipc("EP", ["uiKind"])
        return json_input()

    @property
    def uri_scheme(self):
        send_ipc("EP", ["uriScheme"])
        return json_input()


env = Env()
