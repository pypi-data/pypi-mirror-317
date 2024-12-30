class Color:
    def __init__(self, red: int = 0, green: int = 0, blue: int = 0):
        self.red = red
        self.green = green
        self.blue = blue

    def __repr__(self):
        return f'Color (R: {self.red}, G: {self.green}, B: {self.blue})'

    def to_hex(self) -> str:
        return f'#{self.red:02x}{self.green:02x}{self.blue:02x}'

    def to_normalized(self):
        return self.red / 255, self.green / 255, self.blue / 255

    @classmethod
    def from_hex(cls, hex_str: str|None):
        if not hex_str: return None
        hex_str = hex_str.lstrip('#')
        return cls(int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16))