import websockets
import json

class Gateway:
    GATEWAY_URL = "wss://gateway.discord.gg/?v=10&encoding=json"

    def __init__(self, token, intents, event_handlers, commands, prefix, http_client):
        self.token = token
        self.intents = intents
        self.event_handlers = event_handlers
        self.commands = commands
        self.prefix = prefix
        self.http_client = http_client
        self.connection = None

    async def connect(self):
        """Connects to the Discord Gateway"""
        async with websockets.connect(self.GATEWAY_URL) as websocket:
            self.connection = websocket
            await self.identify()
            await self.listen()

    async def identify(self):
        """Sends identify payload to Discord"""
        payload = {
            "op": 2,
            "d": {
                "token": self.token,
                "intents": self.intents.flags,
                "properties": {
                    "$os": "linux",
                    "$browser": "discord-lite",
                    "$device": "discord-lite"
                }
            }
        }
        await self.connection.send(json.dumps(payload))

    async def listen(self):
        """Listens for events from Discord Gateway"""
        try:
            async for message in self.connection:
                data = json.loads(message)
                await self.handle_event(data)
        except websockets.ConnectionClosed:
            print("Connection closed!")

    async def handle_event(self, data):
        """Processes events from Discord"""
        event_type = data.get("t")
        payload = data.get("d", {})

        if event_type == "READY":
            if "on_ready" in self.event_handlers:
                await self.event_handlers["on_ready"]()

        elif event_type == "MESSAGE_CREATE":
            await self.handle_message(payload)

    async def handle_message(self, payload):
        """Handles MESSAGE_CREATE events"""
        content = payload.get("content", "")
        channel_id = payload.get("channel_id")
        author = payload.get("author", {})
        member = payload.get("member", {})
        mentions = payload.get("mentions", [])
        permissions = int(member.get("permissions", 0))
        roles = member.get("roles", [])

        author_info = {
            "id": author.get("id"),
            "username": author.get("username"),
            "mention": f"<@{author.get('id')}>",
            "permissions": permissions,
            "roles": roles,
        }

        if content.startswith(self.prefix):
            command_name = content[len(self.prefix):].split()[0]
            args = content[len(self.prefix) + len(command_name):].strip().split()
            if command_name in self.commands:
                await self.commands[command_name](self.http_client, channel_id, author_info, *args)

    async def close(self):
        """Closes the WebSocket connection"""
        if self.connection:
            await self.connection.close()
