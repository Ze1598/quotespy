from typing import Union, List
from typing_extensions import TypedDict
from enum import Enum


class GraphicInfo(TypedDict):
    title: str
    text: str


class GraphicSettings(TypedDict):
    font_family: str
    font_size: int
    size: List[int]
    color_scheme: List[str]
    wrap_limit: int
    margin_bottom: float


class DefaultFormats(Enum):
    CUSTOM = ""
    LYRICS = "lyrics"
    QUOTE = "quote"
