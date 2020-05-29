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
    def __init(self, msg):
        self.msg = msg

class InvalidTweetName(Exception):
    def __init__(self, msg):
        self.msg = msg


class InvalidUsername(Exception):
    def __init__(self, msg):
        self.msg = msg

class InvalidUserTag(Exception):
    def __init__(self, msg):
        self.msg = msg

class InvalidProfilePicturePath(Exception):
    def __inint__(self, msg):
        self.msg = msg

class InvalidTweetText(Exception):
    def __init__(self, msg):
        self.msg = msg