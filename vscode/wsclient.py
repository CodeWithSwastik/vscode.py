import asyncio
import json
import websockets


class WSClient:
    """
    This class manages the websocket connection.
    """

    BASE_URI = "ws://localhost:"

    def __init__(self, extension, port: int = 8765) -> None:
        self.extension = extension
        self.port = port
        self.ws = None

    @property
    def uri(self) -> str:
        return self.BASE_URI + str(self.port)

    def run_webserver(self):
        async def webserver():
            async with websockets.serve(self.handler, "localhost", self.port):
                await asyncio.Future()  # run forever

        print(f"Listening on {self.uri}", flush=True)  # js will read this
        asyncio.run(webserver())

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
