class MissingDictKeys(Exception):
    """Error raised when a dictionary does not have all the required fields.
    """

    def __init__(self, msg: str):
        """Initializes MissingDictKeys with an error message.

        Parameters
        ----------
        msg : str
            The error message.
        """
        self.msg = msg


class MissingGraphicSettings(Exception):
    """Error raised when there is no `graphic_settings` dictionary available.
    """

    def __init__(self, msg):
        """Initializes MissingGraphicSettings with an error message.

        Parameters
        ----------
        msg : str
            The error message.
        """
        self.msg = msg


class MissingGraphicField(Exception):
    """Error raised when a `graphic_settings` dictionary is missing a field.
    """

    def __init__(self, msg):
        """Initializes MissingGraphicField with an error message.

        Parameters
        ----------
        msg : str
            The error message.
        """
        self.msg = msg


class FontNotFound(Exception):
    """Error raised when font specified is not found in the user's machine.
    """

    def __init__(self, msg):
        """Initializes FontNotFound with an error message.

        Parameters
        ----------
        msg : str
            The error message.
        """
        self.msg = msg


class InvalidColorFormat(Exception):
    """Error raised when the color specified is not valid Hexadecimal value.
    """

    def __init__(self, msg):
        """Initializes InvalidColorFormat with an error message.

        Parameters
        ----------
        msg : str
            The error message.
        """
        self.msg = msg


class InvalidFormatOption(Exception):
    """Error raised when the default graphic settings option chosen does not exist.
    """

    def __init__(self, msg):
        """Initializes InvalidFormatOption with an error message.

        Parameters
        ----------
        msg : str
            The error message.
        """
        self.msg = msg


class InvalidFieldLength(Exception):
    """Error raised when a field's list has does not have the required length.
    """

    def __init__(self, msg):
        """Initializes InvalidFieldLength with an error message.

        Parameters
        ----------
        msg : str
            The error message.
        """
        self.msg = msg


class InvalidTweetName(Exception):
    """Error raised when the tweet name specified in the `tweet_info` dictionary is not valid.
    """

    def __init__(self, msg):
        """Initializes InvalidTweetName with an error message.

        Parameters
        ----------
        msg : str
            The error message.
        """
        self.msg = msg


class InvalidUsername(Exception):
    """Error raised when the tweet's username specified in the `tweet_info` dictionary is not valid.
    """

    def __init__(self, msg):
        """Initializes InvalidUsername with an error message.

        Parameters
        ----------
        msg : str
            The error message.
        """
        self.msg = msg


class InvalidUserTag(Exception):
    """Error raised when the tweet's user tag/handle specified in the `tweet_info` dictionary is not valid.
    """

    def __init__(self, msg):
        """Initializes InvalidUserTag with an error message.

        Parameters
        ----------
        msg : str
            The error message.
        """
        self.msg = msg


class InvalidProfilePicturePath(Exception):
    """Error raised when the tweet's user profile picture path specified in the `tweet_info` dictionary is not valid.
    """

    def __init__(self, msg):
        """Initializes InvalidProfilePicturePath with an error message.

        Parameters
        ----------
        msg : str
            The error message.
        """
        self.msg = msg


class InvalidTweetText(Exception):
    """Error raised when the tweet text specified in the `tweet_info` dictionary is not valid.
    """

    def __init__(self, msg):
        """Initializes InvalidTweetText with an error message.

        Parameters
        ----------
        msg : str
            The error message.
        """
        self.msg = msg
