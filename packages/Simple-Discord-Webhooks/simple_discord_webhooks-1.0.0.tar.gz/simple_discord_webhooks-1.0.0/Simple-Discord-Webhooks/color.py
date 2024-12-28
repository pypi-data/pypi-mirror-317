class Color:
    @staticmethod
    def rgb_to_color(r, g, b):
        """Convert RGB values to a Discord embed color code."""
        return (r << 16) + (g << 8) + b

    RED = 0xFF0000
    GREEN = 0x00FF00
    BLUE = 0x0000FF
    WHITE = 0xFFFFFF
    BLACK = 0x000000
    YELLOW = 0xFFFF00
    CYAN = 0x00FFFF
    MAGENTA = 0xFF00FF
