import json
from textwrap import wrap
from typing import Dict, List, Tuple, Union
from PIL import Image, ImageDraw, ImageFont, ImageOps
from .type_interfaces import GraphicSettings, TweetInfo


def __calculate_header_height(
    tweet_info: TweetInfo,
    graphic_settings: GraphicSettings,
    font: ImageFont.FreeTypeFont,
) -> float:
    """Calculate the header height: username, user tag and profile picture.

    Parameters
    ----------
    tweet_info : TweetInfo
        Dictionary with all the tweet's information.
    graphic_settings : GraphicSettings
        Dictionary with the graphic's settings.
    font : ImageFont.FreeTypeFont
        Font to be used for the header.

    Returns
    -------
    float
        Height needed for the header (pixels).
    """
    user_pic = tweet_info["user_pic"]
    height_margin = graphic_settings["margin_bottom"]
    profile_pic_size = graphic_settings["profile_pic_size"]
    user_name = tweet_info["user_name"]
    user_tag = tweet_info["user_tag"]

    # Calculate the height of the header's text: user name and user tag
    height_user_name = __calculate_username_height(user_name, user_pic, height_margin, font)
    height_usertag = font.getmask(user_tag).getbbox()[3] + font.font.getsize(user_tag)[1][1]
    height_header_text = height_user_name + height_usertag + height_margin

    # If the header's text is taller than the profile picture, than that's\
    # the header height
    if (height_header_text + height_margin) > profile_pic_size[1]:
        height_header = height_header_text
    # Otherwise, the profile picture sets the header height
    else:
        height_header = profile_pic_size[1]

    return height_header


def __calculate_header_width(
    tweet_info: TweetInfo,
    graphic_settings: GraphicSettings,
    font_header: ImageFont.FreeTypeFont
) -> float:
    """Calculate the width of the header.

    Parameters
    ----------
    tweet_info : TweetInfo
        Dictionary with all the tweet's information.
    graphic_settings : GraphicSettings
        Dictionary with the graphic's settings.
    font : ImageFont.FreeTypeFont
        Font to be used for the text.

    Returns
    -------
    float
        Width needed to draw the header (pixels).
    """
    # Calculate the header of the profile picture
    profile_pic_width = graphic_settings["profile_pic_size"][0]
    # Calculate the user name width
    username_width = __calculate_username_width(
        tweet_info["user_name"],
        tweet_info["user_pic"],
        font_header
    )
    # Calculate the user tag width
    user_tag = tweet_info["user_tag"]
    usertag_width = font_header.getmask(user_tag).getbbox()[2] +\
        font_header.font.getsize(user_tag)[1][0]

    # The width of the header's text is set by the largest of the user\
    # name and user tag
    if username_width > usertag_width:
        text_width = username_width
    else:
        text_width = usertag_width

    # The header width is given as the sum of the profile picture and\
    # the header text width
    width_header = profile_pic_width + \
        graphic_settings["margin_bottom"] + text_width

    return width_header


def __calculate_text_height(
    tweet_info: TweetInfo,
    graphic_settings: GraphicSettings,
    font: ImageFont.FreeTypeFont,
) -> float:
    """Calculate the height needed to draw the tweet text.

    Parameters
    ----------
    tweet_info : TweetInfo
        Dictionary with all the tweet's information.
    graphic_settings : GraphicSettings
        Dictionary with the graphic's settings.
    font : ImageFont.FreeTypeFont
        Font to be used for the text.

    Returns
    -------
    float
        Height needed to draw the text (pixels).
    """
    # Wrap the tweet's text based on the line character limit
    text_wrapped = wrap(
        tweet_info["tweet_text"],
        graphic_settings["wrap_limit"]
    )
    height_margin = graphic_settings["margin_bottom"]

    # Total text height is the sum of height of each text line
    heights_text = [
        font.getmask(line).getbbox()[3] +
        font.font.getsize(line)[1][1] +
        height_margin
        for line in text_wrapped]
    # Last line does not have bottom margin
    heights_text[-1] -= height_margin
    total_text_height = sum(heights_text)

    return total_text_height


def __calculate_text_width(
    tweet_info: TweetInfo,
    graphic_settings: GraphicSettings,
    font: ImageFont.FreeTypeFont
) -> float:
    """Calculate the width of the tweet content. 
    The width is given as the width of the largest tweet text line.

    Parameters
    ----------
    tweet_info : TweetInfo
        Dictionary with all the tweet's information.
    graphic_settings : GraphicSettings
        Dictionary with the graphic's settings.
    font : ImageFont.FreeTypeFont
        Font to be used for the text.

    Returns
    -------
    float
        Width needed to draw the text.
    """
    # Break the text into multiple lines based on the character limit
    text_wrapped = wrap(
        tweet_info["tweet_text"],
        graphic_settings["wrap_limit"]
    )

    # The text's width is set by the largest text line
    width_text = max([
        font.getmask(text_line).getbbox()[2] +
        font.font.getsize(text_line)[1][0]
        for text_line in text_wrapped
    ])

    return width_text


def __calculate_username_width(
    user_name: str,
    user_pic: str,
    font: ImageFont.FreeTypeFont
) -> float:
    """Calculate the width of the username.
    The width is given as the width of the largest username line (in case it is broken up into multiple lines).

    user_name : str
        User name.
    user_pic : str
        Path to the profile picture.
    font : ImageFont.FreeTypeFont
        Font to be used for the username (header).

    Returns
    -------
    float
        Width needed to draw the username.
    """
    # Calculate username character limit per line based on the presence of\
    # the profile picture
    username_char_limit = 19 if user_pic != "" else 38
    # Break the text into multiple lines based on the character limit
    username_wrapped = wrap(user_name, username_char_limit)

    # The username's width is set by the largest username text line
    width_username = max([
        font.getmask(text_line).getbbox()[2] +
        font.font.getsize(text_line)[1][0]
        for text_line in username_wrapped
    ])

    return width_username


def __calculate_username_height(
    user_name: str,
    user_pic: str,
    height_margin: int,
    font: ImageFont.FreeTypeFont
) -> float:
    """Calculate the height of the username.
    The height is given as the sum of the heights each line of username (when the username exceeds the limit of characters per line).

    Parameters
    ----------
    user_name : str
        User name.
    user_pic : str
        Path to the profile picture.
    height_margin: int
        Vertical margin between lines of text.
    font : ImageFont.FreeTypeFont
        Font to be used for the username (header).

    Returns
    -------
    float
        Height needed to draw the username.
    """
    # Wrap the username into multiple lines as needed
    username_char_limit = 19 if user_pic != "" else 38
    user_name = wrap(user_name, username_char_limit)

    # Total username height is the sum of height of each username line
    heights_username = [
        font.getmask(line).getbbox()[3] +
        font.font.getsize(line)[1][1] +
        height_margin
        for line in user_name]
    # Last line does not have bottom margin
    heights_username[-1] -= height_margin
    total_height_username = sum(heights_username)

    return total_height_username


def process_pic(
    graphic_settings: GraphicSettings,
    pic_source: str
) -> Image.Image:
    """Load the user profile picture, resize and crop it to be circular and 10% of the graphic size.

    Parameters
    ----------
    graphic_settings : GraphicSettings
        Dictionary with the settings needed to draw the graphic.
    pic_source : str
        Path to the user's profile picture.

    Returns
    -------
    Image.Image
        Resized and cropped user profile, ready to be drawn in the final graphic.
    """
    # Load the profile picture
    pic = Image.open(pic_source, "r")

    graphic_dimensions = graphic_settings["size"]
    profile_pic_dimensions = graphic_settings["profile_pic_size"]

    # If there's no profile pic dimensions, set it to be the default\
    # value: one tenth of the graphic's dimensions
    if 0 in profile_pic_dimensions:
        width = int(graphic_dimensions[0] * 0.1)
        height = int(graphic_dimensions[1] * 0.1)
        new_dimensions = (width, height)
    else:
        new_dimensions = tuple(profile_pic_dimensions)

    # Create a mask for the circular crop
    mask = Image.new("L", new_dimensions, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + new_dimensions, fill=255)

    # Resize and crop the profile picture based on the circular mask
    cropped_pic = ImageOps.fit(pic, mask.size, centering=(0, 0))
    cropped_pic.putalpha(mask)

    return cropped_pic


def create_graphic_fonts(
    graphic_settings: GraphicSettings
) -> List[ImageFont.FreeTypeFont]:
    """Create all fonts needed for the graphic.

    Parameters
    ----------
    graphic_settings : GraphicSettings
        Settings for the creation of the graphic.

    Returns
    -------
    List[ImageFont.FreeTypeFont]
        A list with all created fonts.
    """
    # Get the font settings from the input dictionary
    font_family = graphic_settings["font_family"]
    font_size_text = graphic_settings["font_size_text"]
    font_size_header = graphic_settings["font_size_header"]
    # Create the fonts
    font_header = ImageFont.truetype(
        font_family, font_size_header, encoding="utf-8")
    font_text = ImageFont.truetype(
        font_family, font_size_text, encoding="utf-8")

    return [font_header, font_text]


def calculate_content_dimensions(
    tweet_info: TweetInfo,
    graphic_settings: GraphicSettings
) -> Dict[str, List[int]]:
    """Calculate the dimensions needed to draw the graphic header and the tweet text.

    Parameters
    ----------
    tweet_info : TweetInfo
        Dictionary with all the tweet's information.
    graphic_settings : GraphicSettings
        Dictionary with the graphic's settings.

    Returns
    -------
    Dict[str, List[int]]
        Dictionary with the dimensions of the header (without profile picture) and of the text.
    """

    # Create all fonts needed
    font_header, font_text = create_graphic_fonts(graphic_settings)

    # Calculate the height needed for the header
    height_header = __calculate_header_height(
        tweet_info, graphic_settings, font_header
    )

    width_header = __calculate_header_width(
        tweet_info, graphic_settings, font_header)

    # Calculate the width needed for the tweet text
    width_text = __calculate_text_width(
        tweet_info, graphic_settings, font_text
    )

    # Calculate the height needed for the tweet text
    height_text = __calculate_text_height(
        tweet_info, graphic_settings, font_text
    )

    # Agreggate the header and text heights in a single dictionary
    dimensions = {
        "header": [width_header, height_header],
        "text": [width_text, height_text],
    }

    return dimensions


def parse_json_settings(file_path: str) -> GraphicSettings:
    """Load a JSON object of settings for the image to be drawn as a Python dictionary.

    Parameters
    ----------
    file_path : str
        Path to the .json file.

    Returns
    -------
    GraphicSettings
        Loaded graphic settings.
    """
    with open(file_path, "r", encoding="utf-8") as json_file:
        json_settings = json.load(json_file)
    return json_settings


def get_ready_tweets(file_path: str) -> List[TweetInfo]:
    """Load a list of tweets (`tweet_info`) from a .json file.

    Parameters
    ----------
    file_path : str
        Path to the .json file.

    Returns
    -------
    List[TweetInfo]
        List of `tweet_info` dictionaries.
    """
    with open(file_path, "r", encoding="utf-8") as json_file:
        json_tweets = json.load(json_file)

    return json_tweets
