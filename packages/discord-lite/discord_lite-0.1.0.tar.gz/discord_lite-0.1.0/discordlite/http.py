import aiohttp
import os
import json

class HTTPClient:
    BASE_URL = "https://discord.com/api/v10"
    MAX_FILE_SIZE = 8 * 1024 * 1024  # 8MB
    ALLOWED_FILE_TYPES = {".txt", ".png", ".jpg", ".jpeg", ".gif"}

    def __init__(self, token):
        self.token = token
        self.session = None

    async def initialize(self):
        """Initializes the aiohttp session"""
        self.session = aiohttp.ClientSession(
            headers={"Authorization": f"Bot {self.token}"}
        )

    async def get_bot_username(self):
        """Fetches bot username from Discord API"""
        url = f"{self.BASE_URL}/users/@me"
        async with self.session.get(url) as response:
            if response.status != 200:
                raise DiscordHTTPException(response.status, await response.text())
            data = await response.json()
            return data.get("username", "Unknown")

    async def send_message(self, channel_id: str, content: str, file_paths: list = None):
        """Sends a message to a Discord channel with optional file attachments"""
        url = f"{self.BASE_URL}/channels/{channel_id}/messages"
        payload = {"content": content}
        form = aiohttp.FormData()

        valid_files = []
        if file_paths:
            for file_path in file_paths:
                if not os.path.exists(file_path):
                    print(f"File {file_path} does not exist. Skipping.")
                    continue
                if os.path.getsize(file_path) > self.MAX_FILE_SIZE:
                    print(f"File {file_path} exceeds the size limit of 8MB. Skipping.")
                    continue
                if os.path.splitext(file_path)[-1].lower() not in self.ALLOWED_FILE_TYPES:
                    print(f"File {file_path} is not an allowed type. Skipping.")
                    continue
                valid_files.append(file_path)

            for file_path in valid_files:
                form.add_field("file", open(file_path, "rb"), filename=os.path.basename(file_path))

        if not valid_files:
            async with self.session.post(url, json=payload) as response:
                if response.status != 200:
                    raise DiscordHTTPException(response.status, await response.text())
            return

        form.add_field("payload_json", json.dumps(payload))
        async with self.session.post(url, data=form) as response:
            if response.status != 200:
                raise DiscordHTTPException(response.status, await response.text())

    async def close(self):
        """Closes the aiohttp session"""
        if self.session:
            await self.session.close()


class DiscordHTTPException(Exception):
    """Custom exception for Discord HTTP errors"""
    def __init__(self, status_code, response_text):
        super().__init__(f"HTTP error {status_code}: {response_text}")
        self.status_code = status_code
        self.response_text = response_text
