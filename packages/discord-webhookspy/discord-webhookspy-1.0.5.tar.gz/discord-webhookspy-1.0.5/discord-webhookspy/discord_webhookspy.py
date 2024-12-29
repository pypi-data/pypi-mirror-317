import requests

class Webhook:
    def __init__(self, webhook_url):
        self.url = webhook_url
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "Windows10"
        }
        self.fields = []  # Alanlar bir liste olarak saklanır
        self.payload = {}

    class Color:
        """:returns: Decimal colors -> supports discord api
        :example: webhook = Webhook.Color.blue() returns the int value."""
        @staticmethod
        def red():
            """:returns: Gives the color code with integer value."""
            return 16711680
        
        def green():
            """:returns: Gives the color code with integer value."""
            return 32768
        
        def blue():
            """:returns: Gives the color code with integer value."""
            return 255

        def cyan():
            """:returns: Gives the color code with integer value."""
            return 65505
        
        def black():
            return 512

    def username(self, name):
        """## Webhook username
        - example: Webhook.username('hello webhook')"""
        self.payload['username'] = name

    def content(self, ctx):
        """## Content
        - The basically context"""
        self.payload['content'] = ctx

    def avatar(self, url):
        """## Webhook avatar url
        - example: Webhook.avatar('https://url') -> supports just url"""
        self.payload['avatar_url'] = url

    def field(self, name, value, inline=True):
        """## Webhook fileds
        - Adding embed to fields -> Webhook.field('name1', 'value1', inline=False)"""
        # Yeni bir alan (field) ekler
        self.fields.append({
            "name": name,
            "value": value,
            "inline": inline
        })

    def embed(self, title="None", color=65505, desc="None", author="None", image="None", thumb="None", footerText="None", footerUrl="None"):
        """Is embeds too easy??"""
        embed_data = {
            "title": title,
            "description": desc,
            "color": color,
            "fields": self.fields  # Daha önce eklenen alanlar buraya eklenir
        }

        if author != "None":
            embed_data["author"] = {"name": author}
        
        if image != "None":
            embed_data["image"] = {"url": image}
        
        if thumb != "None":
            embed_data["thumbnail"] = {"url": thumb}
        
        if footerText != "None":
            embed_data["footer"] = {"text": footerText}
            if footerUrl != "None":
                embed_data["footer"]["icon_url"] = footerUrl

        self.payload["embeds"] = [embed_data]  # Embed bir liste içinde olmalı

    def send(self):
        """## Requesting the discord api."""
        # Webhooku gönder ve yanıtı döndür
        response = requests.post(self.url, json=self.payload, headers=self.headers)
        return response