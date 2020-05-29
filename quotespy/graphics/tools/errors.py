class MissingGraphicSettings(Exception):
    def __init__(self, msg):
        self.msg = msg


class MissingGraphicField(Exception):
    def __init__(self, msg):
        self.msg = msg


class FontNotFound(Exception):
    def __init__(self, msg):
        self.msg = msg


class InvalidColorFormat(Exception):
    def __init__(self, msg):
        self.msg = msg


class InvalidFormatOption(Exception):
    def __init__(self, msg):
        self.msg = msg


class InvalidFieldLength(Exception):
    def __init__(self, msg):
        self.msg = msg


class MissingDictKeys(Exception):
    def __init__(self, msg):
        self.msg = msg


class MissingTitles(Exception):
    def __init__(self, msg):
        self.msg = msg


class MissingQuotes(Exception):
    def __init__(self, msg):
        self.msg = msg
