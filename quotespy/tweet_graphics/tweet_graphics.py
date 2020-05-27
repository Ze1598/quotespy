from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap
from typing import Optional
from type_interfaces import TweetInfo, GraphicSettings, DefaultFormats
import utils as tweet_utils
from os import path

def __choose_graphic_settings(
    graphic_settings: GraphicSettings,
    default_settings_format: DefaultFormats = DefaultFormats.CUSTOM.value
) -> None:
    """Based on the custom graphic settings and (lack of) default settings passed,
    choose the settings to be used.
    """
    # TODO: create custom error
    if (graphic_settings == dict()) and (default_settings_format == DefaultFormats.CUSTOM.value):
        raise NotImplementedError
    elif (graphic_settings == dict()):
        settings_file = f"quotespy\\tweet_graphics\default_settings\{default_settings_format}_mode_settings.json"
        chosen_settings = tweet_utils.parse_json_settings(settings_file)
    else:
        chosen_settings = graphic_settings
    # TODO: validate settings, no matter if custom or default
    # validate_g_settings(chosen_settings)
    
    return chosen_settings


def __draw_header(username, user_tag, user_pic, graphic_size, img, d_interface, coords, margin, font, color):
    """Draw the graphic header (username, user tag and, if specified, profile picture).
    """
    x = int(coords[0])
    y = int(coords[1])

    # If a profile picture was not specified, draw the username and user tag
    if user_pic == "":
        # Draw the username
        user_name = wrap(username, 38)
        for line in user_name:
            d_interface.text((x, y), line, font=font, fill=color)
            y += font.size + margin
        # Draw the user handle
        d_interface.text((x, y), user_tag, font=font, fill=color)
        y += int(font.size + margin * 1.5)

    # Otherwise, draw the profile picture additionally
    else:
        # Process the profile picture and draw it
        user_pic_processed = tweet_utils.process_pic(graphic_size, user_pic)
        img.paste(user_pic_processed, (x, y), mask=user_pic_processed)
        # Due to the presence of the profile picture, the horizontal\
        # coordinate for the rest of the header is updated
        x = int(coords[0] + user_pic_processed.size[0] + margin)
        # Draw the username
        user_name = wrap(username, 19)
        for line in user_name:
            d_interface.text((x, y), line, font=font, fill=color)
            y += font.size + margin
        # Draw the user tag
        d_interface.text((x, y), user_tag, font=font, fill=color)
        y += int(font.size + margin * 1.5)

    # Return the current vertical coordinate
    return y


def __get_initial_coordinates(img_size, dimensions):
    """Calculate the initial X and Y coordinates at which to start drawing.
    """
    # Get header and tweet text dimensions
    header_width, header_height = dimensions["header"]
    text_width, text_height = dimensions["text"]

    # Horizontal coordinate to draw at (centered)
    x = (img_size[0] - text_width) // 2
    # Initial vertical coordinate to draw at (centered)
    content_height = header_height + text_height
    y = (img_size[1] - content_height) // 2

    return (x, y)

# TODO: pass `save_dir` to `tweet_info`
def create_tweet(
    tweet_info, 
    graphic_settings, 
    default_settings_format: DefaultFormats = DefaultFormats.CUSTOM.value,
    save_dir: Optional[str] = ""
) -> None:
    # TODO validate tweet_info (including missing optional information)
    # t_info = __validate_tweet_info(tweet_info)
    # Use the graphic settings passed (either custom or default)
    g_settings = __choose_graphic_settings(graphic_settings, default_settings_format)

    user_name = tweet_info["user_name"]
    user_tag = tweet_info["user_tag"]
    tweet_text = tweet_info["tweet_text"]
    user_pic = tweet_info["user_pic"]
   
    font_family = g_settings["font_family"]
    font_size_text = g_settings["font_size_text"]
    font_size_header = g_settings["font_size_header"]
    # Set up the fonts based on settings
    font_header = ImageFont.truetype(
        font_family, font_size_header, encoding="utf-8")
    font_text = ImageFont.truetype(
        font_family, font_size_text, encoding="utf-8")
   
    # Size of the graphic
    img_size = g_settings["size"]
    # Vertical margin in between lines
    margin_bottom = g_settings["margin_bottom"]
    background_color = g_settings["color_scheme"][0]
    text_color = g_settings["color_scheme"][1]
    chars_limit = g_settings["wrap_limit"]

    # Dict with size of header and size of text
    content_dims = tweet_utils.calculate_content_dimensions(
        tweet_info, g_settings)
    # Calculate the inital drawing coordinates
    x, y = __get_initial_coordinates(img_size, content_dims)

    # Create what will be the final image
    img = Image.new("RGB", (img_size[0], img_size[1]), color=background_color)
    # Create the drawing interface
    draw = ImageDraw.Draw(img)

    # Draw the header text (and update the vertical coordinate to be where\
    # the header finishes)
    y = __draw_header(user_name, user_tag, user_pic, img_size, img,
        draw, (x, y), margin_bottom, font_header, text_color)

    # Split the tweet text into lines
    text_wrapped = wrap(tweet_text, chars_limit)
    # Draw the tweet text
    for line in text_wrapped:
        draw.text((x, y), line, font=font_text, fill=text_color)
        y += font_text.size + margin_bottom

    save_name = f"{tweet_info['tweet_name']}.png"
    save_name = path.join(save_dir, save_name)
    img.save(save_name)


if __name__ == "__main__":
    t = {
        "tweet_name": "tweet_test",
        "user_name": "José Fernando Costa",
        "user_tag": "@soulsinporto",
        "user_pic": "user_photo2.png",
        "tweet_text": "Some mistakes and, dare I say, failures may lead to results you had never thought you could achieve."
    }
    g = {
        "font_family": "arial.ttf",
        "font_size_text": 100,
        "font_size_header": 80,
        "size": [1800, 1800],
        "color_scheme": ["#000000", "#ffffff"],
        "wrap_limit": 32,
        "margin_bottom": 30
    }

    g = tweet_utils.parse_json_settings(
        "quotespy\\tweet_graphics\default_settings\dark_mode_settings.json")
    create_tweet(t, {}, default_settings_format="light")
