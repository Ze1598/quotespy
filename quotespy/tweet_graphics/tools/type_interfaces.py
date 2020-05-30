from enum import Enum
from typing import List, Union
from typing_extensions import TypedDict


class GraphicSettings(TypedDict):
    """TypedDict for the `graphic_settings` dictionary, that is, the dictionary that contains settings for the graphic creation.
    """
    font_family: str
    font_size_header: int
    font_size_text: int
    size: List[int]
    color_scheme: List[str]
    wrap_limit: int
    margin_bottom: float


class TweetInfo (TypedDict):
    """TypedDict for the `tweet_info` dictionary, that is, the dictionary that contains the tweet's information: name, username, user tag/handle, profile picture and the actual text.
    """
    tweet_name: str
    user_name: str
    user_tag: str
    user_pic: str
    tweet_text: str


class DefaultFormats(Enum):
    """Contains the default `graphic_settings` format options.
    """
    CUSTOM = ""
    LIGHT = "light"
    DARK = "dark"
    BLUE = "blue"
