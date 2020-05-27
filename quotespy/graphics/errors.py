class MissingGraphicSettings(Exception):
    def __init__(self, msg):
        self.msg = msg

class FontNotFound(Exception):
    def __init__(self, msg):
        self.msg = msg

class InvalidColorFormat(Exception):
    def __init__(self, msg):
        self.msg = msg