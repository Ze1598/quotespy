from PIL import Image, ImageDraw, ImageFont, ImageOps
from textwrap import wrap
from typing import Dict, Union, List
import json


def create_dummy_img_components(graphic_settings):
    # Set up the fonts based on settings
    font_header = ImageFont.truetype(
        graphic_settings["font_family"],
        graphic_settings["font_size_header"],
        encoding="utf-8"
    )
    font_text = ImageFont.truetype(
        graphic_settings["font_family"],
        graphic_settings["font_size_text"],
        encoding="utf-8"
    )
    # Dummy Img to find text size
    dummy_img = Image.new("RGB", (0, 0))
    dummy_img = ImageDraw.Draw(dummy_img)

    return (font_header, font_text, dummy_img)


def calculate_username_height(user_name, font, img, height_margin):
    """Calculate the total height for the username, including vertical margins.
    """
    # Calculate the height needed for each line and sum all of them
    height_user_name = sum([
        img.textsize(line, font=font)[1]
        for line in user_name])
    # Take the margin of each line into account
    height_user_name += (height_margin * len(user_name))
    return height_user_name


def calculate_header_height(tweet_info, graphic_settings, font, img):
    """Calculate the header height (username, user tag plus, optionally, profile picture).
    """
    user_pic = tweet_info["user_pic"]
    height_margin = graphic_settings["margin_bottom"]
    profile_pic_size = (
        graphic_settings["size"][0] * 0.1,
        graphic_settings["size"][1] * 0.1
    )
    # Wrap the username into multiple lines as needed
    _user_name = tweet_info["user_name"]
    username_char_limit = 19 if user_pic != "" else 38
    user_name = wrap(_user_name, username_char_limit)

    # If the username fits in a single line, the header height is given by the\
    # profile picture; else it is given by the username and user tag heights
    if (len(user_name) == 1):
        height_header = height_header = (profile_pic_size[1] * 0.1) + height_margin
    else:
        height_header = calculate_username_height(user_name, font, img, height_margin)\
            + img.textsize(tweet_info["user_tag"], font=font)[1]\
            + height_margin
    
    return height_header


def calculate_text_height(tweet_info, graphic_settings, font, img):
    """Calculate the height needed to draw the tweet text.
    """
    text_wrapped = wrap(tweet_info["tweet_text"],
                        graphic_settings["wrap_limit"])
    line_heights = [
        img.textsize(text_wrapped[i], font=font)[1]
        for i in range(len(text_wrapped))]
    height_text = sum(line_heights)\
        + (len(line_heights) * graphic_settings["margin_bottom"])
    return height_text


def calculate_text_width(tweet_info, graphic_settings, font, img):
    """Calculate the width of the tweet content.

    The width is given as the width of the largest tweet text line.
    """
    # Break the text into multiple lines based on the character limit
    text_wrapped = wrap(
        tweet_info["tweet_text"],
        graphic_settings["wrap_limit"]
    )
    # Width of the longest line (hence the width of the text)
    width_text = max([
        img.textsize(line, font=font)[0]
        for line in text_wrapped])

    return width_text


def calculate_username_width(user_name, user_pic, font, img):
    """Calculate the width of the username.

    The width is given as the width of the largest username line (in case it is broken up into multiple lines).
    """
    # Calculate username character limit per line based on the presence of\
    # the profile picture
    username_char_limit = 19 if user_pic != "" else 38
    # Break the text into multiple lines based on the character limit
    user_name_wrapped = wrap(
        user_name,
        username_char_limit
    )

    # Width of the longest line (hence the width of the text)
    width_username = max([
        img.textsize(line, font=font)[0]
        for line in user_name_wrapped])
    return width_username


def process_pic(graphic_size, pic_source):
    """Load the user profile picture, resize and crop it to be circular and 10% of the graphic size.
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


def calculate_content_dimensions(tweet_info, graphic_settings):
    """Calculate the dimensions needed to draw the graphic header and the tweet text.
    """
    # Set up dummy image elements for calculations: the fonts\
    # and an image in which to draw for measures
    font_header, font_text, dummy_img = create_dummy_img_components(
        graphic_settings)

    # Calculate the width needed for the tweet text
    width_text = calculate_text_width(
        tweet_info, graphic_settings, font_text, dummy_img)
    # Calculate the width needed for the username
    width_username = calculate_username_width(
        tweet_info["user_name"], tweet_info["user_pic"], font_header, dummy_img)

    # Calculate the height needed for the header
    height_header = calculate_header_height(
        tweet_info, graphic_settings, font_header, dummy_img)
    # Calculate the height needed for the tweet text
    height_text = calculate_text_height(
        tweet_info, graphic_settings, font_text, dummy_img)

    # Agreggate the header and text heights in a single dictionary
    dimensions = {
        "header": [width_username, height_header],
        "text": [width_text, height_text]
    }

    return dimensions


def parse_json_settings(
    file_path: str
) -> Dict[str, Union[str, int, float, List[str]]]:
    """
    Load a JSON object of settings for the image to be drawn as a Python dictionary.
    """
    with open(file_path, "r") as json_file:
        json_settings = json.load(json_file)
    return json_settings


if __name__ == "__main__":
    t = {
        "tweet_name": "blah",
        "user_name": "José Fernando Costa",
        "user_tag": "@soulsinporto",
        "user_pic": "",
        "tweet_text": "Some mistakes and, dare I say, failures may lead to results you had never thought you could achieve."
    }
    g = {
        "font_family": "arial.ttf",
        "font_size": 95,
        "size": [2800, 2800],
        "color_scheme": ["black", "white"],
        "wrap_limit": 37,
        "margin_bottom": 30
    }
    calculate_content_dimensions(t, g)
