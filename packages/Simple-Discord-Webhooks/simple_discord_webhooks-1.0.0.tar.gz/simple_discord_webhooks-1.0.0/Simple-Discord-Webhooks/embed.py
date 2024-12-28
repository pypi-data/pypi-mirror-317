class Embed:
    def __init__(self, title=None, description=None, color=None):
        self.title = title
        self.description = description
        self.color = color
        self.fields = []
        self.thumbnail = None
        self.image = None
        self.author = None
        self.footer = None
        self.url = None

    def add_field(self, name, value, inline=True):
        """Add a field to the embed."""
        self.fields.append({"name": name, "value": value, "inline": inline})

    def set_thumbnail(self, url):
        """Set the thumbnail image URL."""
        self.thumbnail = {"url": url}

    def set_image(self, url):
        """Set the large image URL."""
        self.image = {"url": url}

    def set_author(self, name, url=None, icon_url=None):
        """Set the author of the embed."""
        self.author = {"name": name, "url": url, "icon_url": icon_url}

    def set_footer(self, text, icon_url=None):
        """Set the footer of the embed."""
        self.footer = {"text": text, "icon_url": icon_url}

    def set_url(self, url):
        """Set the URL of the embed."""
        self.url = url

    def to_dict(self):
        """Convert the embed to a dictionary."""
        embed = {
            "title": self.title,
            "description": self.description,
            "color": self.color,
            "fields": self.fields,
        }
        if self.thumbnail:
            embed["thumbnail"] = self.thumbnail
        if self.image:
            embed["image"] = self.image
        if self.author:
            embed["author"] = self.author
        if self.footer:
            embed["footer"] = self.footer
        if self.url:
            embed["url"] = self.url
        return embed
