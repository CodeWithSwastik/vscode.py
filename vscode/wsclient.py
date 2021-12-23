import asyncio
import json
import websockets

from vscode.context import Context

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
            await self.parse_data(data)


    async def parse_data(self, data: dict):
        if data["type"] == 1: # Command 
            name = data.get("name")
            if any(name == (cmd:=i).name for i in self.extension.commands):
                ctx = Context(ws=self)
                ctx.command = cmd
                asyncio.ensure_future(cmd.func(ctx))
            else:
                await self.ws.send(f"Invalid Command '{name}'")

        elif data["type"] == 2: # Event
            event = data.get("event").lower()
            events = self.extension.events
            if event in events:
                asyncio.ensure_future(events[event]())
        elif data["type"] == 3: # Eval Response:
            print(data, flush=True)
        else:
            print(data, flush=True)

    async def send(self, **kwargs):
        return await self.ws.send(json.dumps(kwargs))