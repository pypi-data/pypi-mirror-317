import json
import urllib3
from .embed import Embed

class Webhook:
    def __init__(self, url):
        self.url = url
        self.username = None
        self.avatar_url = None
        self.embeds = []
        self.http = urllib3.PoolManager()

    def set_username(self, username):
        """Set the username of the webhook."""
        self.username = username

    def set_avatar_url(self, avatar_url):
        """Set the avatar URL of the webhook."""
        self.avatar_url = avatar_url

    def add_embed(self, embed):
        """Add an embed to the webhook."""
        if isinstance(embed, Embed):
            self.embeds.append(embed.to_dict())
        else:
            raise ValueError("embed must be an instance of Embed")

    def send(self, content=None):
        """Send the webhook."""
        payload = {
            "content": content,
            "username": self.username,
            "avatar_url": self.avatar_url,
            "embeds": self.embeds,
        }
        headers = {"Content-Type": "application/json"}
        response = self.http.request(
            "POST",
            self.url,
            body=json.dumps(payload).encode("utf-8"),
            headers=headers,
        )
        return response.status, response.data
