import json
import socket
import asyncio
import websockets


class WSClient:
    """
    This class manages the websocket connection.
    """

    BASE_URI = "ws://localhost:"

    def __init__(self, extension, port: int = None) -> None:
        self.extension = extension
        self.port = port
        self.ws = None

    @property
    def uri(self) -> str:
        return self.BASE_URI + str(self.port)

    def run_webserver(self):
        if self.port is None:
            self.port = self.get_free_port()
        async def webserver():
            async with websockets.serve(self.handler, "localhost", self.port):
                await asyncio.Future()  # run forever

        print(f"Listening on {self.uri}", flush=True)  # js will read this
        asyncio.run(webserver())

    def get_free_port(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', 0))
        _, port = sock.getsockname()
        sock.close()
        return port

    async def handler(self, websocket, path):
        self.ws = websocket
        while True:
            try:
                message = await websocket.recv()
            except websockets.ConnectionClosedOK:
                break
            data = json.loads(message)
            await self.extension.parse_ws_data(data)

    async def send(self, **kwargs):
        return await self.ws.send(json.dumps(kwargs))


