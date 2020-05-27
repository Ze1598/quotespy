from typing import Union, List
from typing_extensions import TypedDict
from enum import Enum

class GraphicSettings(TypedDict):
    font_family: str
    font_size: int
    size: List[int]
    color_scheme: List[str]
    wrap_limit: int
    margin_bottom: float


class TweetInfo (TypedDict):
    tweet_name: str
    user_name: str
    user_tag: str
    user_pic: str
    tweet_text: str

class DefaultFormats(Enum):
    CUSTOM = ""
    LIGHT = "light"
    DARK = "dark"
    BLUE = "blue"