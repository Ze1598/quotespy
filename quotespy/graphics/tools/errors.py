class MissingGraphicSettings(Exception):
    """Error raised when there is no `graphic_settings` dictionary available.
    """

    def __init__(self, msg: str):
        """Initializes MissingGraphicSettings with an error message.

        Parameters
        ----------
        msg : str
            The error message.
        """
        self.msg = msg


class MissingGraphicInfoField(Exception):
    """Error raised when a `graphic_settings` dictionary is missing a required field.
    """

    def __init__(self, msg: str):
        """Initializes MissingGraphicInfoField with an error message.

        Parameters
        ----------
        msg : str
            The error message.
        """
        self.msg = msg


class FontNotFound(Exception):
    """Error raised when the specified `font_family` of a `graphic_settings` dictionary is not found in the machine.
    """

    def __init__(self, msg: str):
        """Initializes FontNotFound with an error message.

        Parameters
        ----------
        msg : str
            The error message.
        """
        self.msg = msg


class InvalidColorFormat(Exception):
    """Error raised when a color of the `color_schemes` field is not given in a valid Hexadecimal format.
    """

    def __init__(self, msg: str):
        """Initializes InvalidColorFormat with an error message.

        Parameters
        ----------
        msg : str
            The error message.
        """
        self.msg = msg


class InvalidFormatOption(Exception):
    """Error raised when the default `graphic_settings` format chosen is not a valid option.
    """

    def __init__(self, msg: str):
        """Initializes InvalidFormatOption with an error message.

        Parameters
        ----------
        msg : str
            The error message.
        """
        self.msg = msg


class InvalidFieldLength(Exception):
    """Error raised when a `graphic_settings` field that takes a list of values does not have enough values.
    """

    def __init__(self, msg: str):
        """Initializes InvalidFieldLength with an error message.

        Parameters
        ----------
        msg : str
            The error message.
        """
        self.msg = msg


class MissingDictKeys(Exception):
    """Error raised when the `graphic_settings` dictionary does not have all the required fields.
    """

    def __init__(self, msg: str):
        """Initializes MissingDictKeys with an error message.

        Parameters
        ----------
        msg : str
            The error message.
        """
        self.msg = msg


class MissingTitles(Exception):
    """Error raised when the `graphic_info` dictionary does not have a `title` field.
    """

    def __init__(self, msg: str):
        """Initializes MissingTitles with an error message.

        Parameters
        ----------
        msg : str
            The error message.
        """
        self.msg = msg


class MissingQuotes(Exception):
    """Error raised when the `graphic_info` dictionary does not have a `quote` field.
    """

    def __init__(self, msg: str):
        """Initializes MissingQuotes with an error message.

        Parameters
        ----------
        msg : str
            The error message.
        """
        self.msg = msg


class MissingTitlesOrQuotes(Exception):
    """Error raised when the titles and quotes loaded from a .txt file have been loaded in uneven quantity.
    """

    def __init__(self, msg: str):
        """Initializes MissingTitlesOrQuotes with an error message.

        Parameters
        ----------
        msg : str
            The error message.
        """
        self.msg = msg
