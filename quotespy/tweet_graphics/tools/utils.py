import json
from textwrap import wrap
from typing import Dict, List, Tuple, Union
from PIL import Image, ImageDraw, ImageFont, ImageOps
from .type_interfaces import GraphicSettings, TweetInfo


def __create_dummy_img_components(
    graphic_settings: GraphicSettings,
) -> Tuple[ImageFont.FreeTypeFont, ImageFont.FreeTypeFont, Image.Image]:
    """Create dummy fonts and a PIL image to be used for calculations.

    Parameters
    ----------
    graphic_settings : GraphicSettings
        Dictionary of graphic settings to be used for the final graphic.

    Returns
    -------
    Tuple[ImageFont.FreeTypeFont, ImageFont.FreeTypeFont, Image.Image]
        Tuple with the font for the header, font for the tweet text and the Image, all to be used only in calculations.
    """
    # Set up the fonts based on settings
    font_header = ImageFont.truetype(
        graphic_settings["font_family"],
        graphic_settings["font_size_header"],
        encoding="utf-8",
    )
    font_text = ImageFont.truetype(
        graphic_settings["font_family"],
        graphic_settings["font_size_text"],
        encoding="utf-8",
    )
    # Dummy Img to find text size
    dummy_img = Image.new("RGB", (0, 0))
    dummy_img = ImageDraw.Draw(dummy_img)

    return (font_header, font_text, dummy_img)


def __calculate_username_height(
    user_name: str, font: ImageFont.FreeTypeFont, img: Image.Image, height_margin: float
) -> float:
    """Calculate the total height for the username, including vertical margins.

    Parameters
    ----------
    user_name : str
        Tweet's username.
    font : ImageFont.FreeTypeFont
        Font to be used for the header.
    img : Image.Image
        Dummy PIL Image for calculations.
    height_margin : float
        Vertical margin in between text lines.

    Returns
    -------
    float
        Height needed for the username (pixels).
    """
    # Calculate the height needed for each line and sum all of them
    height_user_name = sum([img.textsize(line, font=font)[1]
                            for line in user_name])
    # Take the margin of each line into account
    height_user_name += height_margin * len(user_name)
    return height_user_name


def __calculate_header_height(
    tweet_info: TweetInfo,
    graphic_settings: GraphicSettings,
    font: ImageFont.FreeTypeFont,
) -> float:
    """Calculate the header height (username, user tag plus, optionally, profile picture).

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
    profile_pic_size = (
        graphic_settings["size"][0] * 0.1,
        graphic_settings["size"][1] * 0.1,
    )
    # Wrap the username into multiple lines as needed
    _user_name = tweet_info["user_name"]
    username_char_limit = 19 if user_pic != "" else 38
    user_name = wrap(_user_name, username_char_limit)
    user_tag = tweet_info["user_tag"]

    # If the username fits in a single line, the header height is given by the\
    # profile picture
    if len(user_name) == 1:
        height_header = profile_pic_size[1] + height_margin
    # Otherwise the height is the sum of the username height, tag and margin
    else:
        # Total username height is the sum of height of each username line
        heights_username = [
            font.getmask(line).getbbox()[3] +
            font.font.getsize(line)[1][1] +
            height_margin
            for line in user_name]
        # Last line does not have bottom margin
        heights_username[-1] -= height_margin
        total_height_username = sum(heights_username)

        height_usertag = font.getmask(user_tag).getbbox()[3] +\
            font.font.getsize(user_tag)[1][1]

        height_header = total_height_username + height_usertag + height_margin

    return height_header


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

    Parameters
    ----------
    user_name : str
        [description]
    user_pic : str
        [description]
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

    width_username = max([
        font.getmask(text_line).getbbox()[2] + 
        font.font.getsize(text_line)[1][0] 
        for text_line in username_wrapped
    ])

    return width_username


def process_pic(graphic_size: List[int], pic_source: str) -> Image.Image:
    """Load the user profile picture, resize and crop it to be circular and 10% of the graphic size.

    Parameters
    ----------
    graphic_size : List[int]
        Dimensions of the graphic.
    pic_source : str
        Path to the user's profile picture.

    Returns
    -------
    Image.Image
        Resized and cropped user profile, ready to be drawn in the final graphic.
    """
    # Load the profile picture
    pic = Image.open(pic_source, "r")

    # New side length
    side = int(graphic_size[0] * 0.1)
    new_size = (side, side)

    # Create a mask for the circular crop
    mask = Image.new("L", new_size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + new_size, fill=255)

    # Resize and crop the profile picture based on the circular mask
    cropped_pic = ImageOps.fit(pic, mask.size, centering=(0, 0))
    cropped_pic.putalpha(mask)

    return cropped_pic


def calculate_content_dimensions(
    tweet_info: TweetInfo, graphic_settings: GraphicSettings
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
    # Set up dummy image elements for calculations: the fonts\
    # and an image in which to draw for measures
    font_header, font_text, dummy_img = __create_dummy_img_components(
        graphic_settings)

    # Calculate the width needed for the tweet text
    width_text = __calculate_text_width(
        tweet_info, graphic_settings, font_text
    )
    # Calculate the width needed for the username
    width_username = __calculate_username_width(
        tweet_info["user_name"], tweet_info["user_pic"], font_header
    )

    # Calculate the height needed for the header
    height_header = __calculate_header_height(
        tweet_info, graphic_settings, font_header
    )
    # Calculate the height needed for the tweet text
    height_text = __calculate_text_height(
        tweet_info, graphic_settings, font_text
    )

    # Agreggate the header and text heights in a single dictionary
    dimensions = {
        "header": [width_username, height_header],
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
