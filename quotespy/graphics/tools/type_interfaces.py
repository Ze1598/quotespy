from enum import Enum
from typing import List, Union
from typing_extensions import TypedDict


class GraphicInfo(TypedDict):
    """TypedDict for the `graphic_info` dictionary, that is, the dictionary that contains the title and the quote of a graphic.
    """

    title: str
    text: str


class GraphicSettings(TypedDict):
    """TypedDict for the `graphic_settings` dictionary, that is, the dictionary that contains settings for the graphic creation.
    """

    font_family: str
    font_size: int
    size: List[int]
    color_scheme: List[str]
    wrap_limit: int
    margin_bottom: float


class DefaultFormats(Enum):
    """Contains the default `graphic_settings` format options.
    """

    CUSTOM = ""
    LYRICS = "lyrics"
    QUOTE = "quote"
