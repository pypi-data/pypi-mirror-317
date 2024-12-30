import asyncio
from .gateway import Gateway
from .http import HTTPClient

class Bot:
    PERMISSIONS = {
        "ADMINISTRATOR": 1 << 3,
        "MANAGE_MESSAGES": 1 << 13,
    }

    def __init__(self, prefix: str, intents):
        self.prefix = prefix
        self.intents = intents
        self.token = None
        self.gateway = None
        self.http = None
        self.event_handlers = {}
        self.commands = {}
        self.command_permissions = {}
        self.command_roles = {}
        self.username = "Unknown"
        self.active_events = []
        self.active_commands = []

    def add_event(self, event_name: str, handler):
        """Registers an event and adds to active events"""
        self.event_handlers[event_name] = handler
        self.active_events.append(event_name)

    def add_command(self, command_name: str, handler, required_permissions=None, required_roles=None):
        """Registers a command and adds to active commands"""
        self.commands[command_name] = handler
        self.active_commands.append(command_name)
        if required_permissions:
            self.command_permissions[command_name] = required_permissions
        if required_roles:
            self.command_roles[command_name] = required_roles

    def has_permission(self, user_permissions, required_permissions):
        """Checks if user has required permissions"""
        return (user_permissions & required_permissions) == required_permissions

    def has_role(self, user_roles, required_roles):
        """Checks if user has one of the required roles"""
        return any(role in user_roles for role in required_roles)

    @property
    def event_count(self):
        """Returns the count of active events"""
        return len(self.active_events)

    @property
    def command_count(self):
        """Returns the count of active commands"""
        return len(self.active_commands)

    def run(self, token: str):
        """Runs the bot"""
        self.token = token
        self.http = HTTPClient(token)
        asyncio.run(self._initialize_and_run())

    async def _initialize_and_run(self):
        """Initializes HTTP client, fetches username, and starts gateway"""
        await self.http.initialize()
        self.username = await self.http.get_bot_username()
        self.gateway = Gateway(self.token, self.intents, self.event_handlers, self.commands, self.prefix, self.http)
        try:
            await self.gateway.connect()
        except KeyboardInterrupt:
            await self.gateway.close()
            await self.http.close()

    async def send_message(self, channel_id: str, content: str, file_paths: list = None):
        """Sends a message with optional file attachments"""
        await self.http.send_message(channel_id, content, file_paths)
