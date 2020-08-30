from os import path
from textwrap import wrap
from typing import Dict, List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
from .tools.default_settings import (
    blue_mode_settings,
    dark_mode_settings,
    light_mode_settings,
)
from .tools.type_interfaces import DefaultFormats, GraphicSettings, TweetInfo
from .tools.utils import (
    calculate_content_dimensions,
    get_ready_tweets,
    parse_json_settings,
    process_pic,
    create_graphic_fonts
)
from .tools.validation import (
    validate_format_option,
    validate_g_settings,
    validate_settings_existence,
    validate_tweet_info,
)


def __load_default_settings(default_settings_format: str) -> GraphicSettings:
    """Based on the option chosen, load default graphic settings.

    Parameters
    ----------
    default_settings_format : str
        Default graphic settings format chosen.

    Returns
    -------
    GraphicSettings
        Loaded default graphic settings.
    """
    if default_settings_format == DefaultFormats.LIGHT.value:
        return light_mode_settings
    elif default_settings_format == DefaultFormats.BLUE.value:
        return blue_mode_settings
    elif default_settings_format == DefaultFormats.DARK.value:
        return dark_mode_settings


def __choose_graphic_settings(
    tweet_info: TweetInfo,
    graphic_settings: GraphicSettings,
    default_settings_format: DefaultFormats = DefaultFormats.CUSTOM.value,
) -> GraphicSettings:
    """Based on the custom graphic settings and (lack of) default settings passed,
    choose the settings to be used.

    Parameters
    ----------
    tweet_info : TweetInfo
        Dictionary with the necessary information about the tweet.
    graphic_settings : GraphicSettings
        Custom graphic settings dictionary.
    default_settings_format : DefaultFormats, optional
        Default graphic settings format, by default DefaultFormats.CUSTOM.value

    Returns
    -------
    GraphicSettings
        A dictionary of graphic settings to be used.
    """
    # Validate that either custom or default settings were passed
    validate_settings_existence(graphic_settings, default_settings_format)

    # Validate and sanitize the default settings format chosen
    if default_settings_format != "":
        default_settings_format = validate_format_option(
            default_settings_format)

    # If the custom settings are just an empty dict, use the default settings format specified
    if graphic_settings == dict():
        chosen_settings = __load_default_settings(default_settings_format)

    # Otherwise, use the custom settingss
    else:
        chosen_settings = graphic_settings
    # Validate the chosen settings, independent of it being custom or default settings
    validated_settings = validate_g_settings(tweet_info, chosen_settings)

    return validated_settings


def __draw_header_with_profile_pic(
    tweet_info: TweetInfo,
    graphic_settings: GraphicSettings,
    wip_img: Image.Image,
    draw_interface: ImageDraw.ImageDraw,
    coordinates: Tuple[int],
    header_height: int,
    font_header: ImageFont.FreeTypeFont,
    profile_picture: Image.Image
) -> int:
    """Draw the graphic's header: username, user tag and profile picture.

    Parameters
    ----------
    tweet_info : TweetInfo
        Dictionary with all the tweet's information.
    graphic_settings : GraphicSettings
        Dictionary with the graphic's settings.
    wip_img : Image.Image
        Work-in-progress tweet graphic.
    draw_interface : ImageDraw.ImageDraw
        Interface used to draw in the Image.
    coordinates : Tuple[int]
        Initial coordinates at which to draw the header.
    header_height: int
        Total height of the header.
    font_header : ImageFont.FreeTypeFont
        Font used for the header.
    profile_picture : Image.Image
        Profile picture ready to be drawn in the graphic.

    Returns
    -------
    int
        Vertical coordinate at which to start drawing the tweet body.
    """
    x = coordinates[0]
    y = coordinates[1]

    username = tweet_info["user_name"]
    user_tag = tweet_info["user_tag"]
    text_color = graphic_settings["color_scheme"][1]
    margin = graphic_settings["margin_bottom"]
    profile_pic_height = graphic_settings["profile_pic_size"][1]
    profile_pic_width = graphic_settings["profile_pic_size"][0]
    user_name = wrap(username, 19)

    # Draw the profile picture
    wip_img.paste(profile_picture, (x, y), mask=profile_picture)
    # Horizontal coordinate at which to draw the username and user tag
    x_header_text = int(coordinates[0] + profile_pic_width + margin)

    # Draw the username
    for line in user_name:
        draw_interface.text(
            (x_header_text, y),
            line,
            font=font_header,
            fill=text_color
        )
        y += font_header.size + margin

    # Draw the user tag
    draw_interface.text(
        (x_header_text, y),
        user_tag,
        font=font_header,
        fill=text_color
    )

    # Calculate the vertical coordinate at which to start drawing the\
    # tweet text
    return_y = coordinates[1] + header_height + margin

    # Return the current vertical coordinate
    return return_y


def __draw_header_without_profile_pic(
    tweet_info: TweetInfo,
    graphic_settings: GraphicSettings,
    wip_img: Image.Image,
    draw_interface: ImageDraw.ImageDraw,
    coordinates: Tuple[int],
    header_height: int,
    font_header: ImageFont.FreeTypeFont,
) -> int:
    """Draw the graphic's header: username and user tag only.

    Parameters
    ----------
    tweet_info : TweetInfo
        Dictionary with all the tweet's information.
    graphic_settings : GraphicSettings
        Dictionary with the graphic's settings.
    wip_img : Image.Image
        Work-in-progress tweet graphic.
    draw_interface : ImageDraw.ImageDraw
        Interface used to draw in the Image.
    coordinates : Tuple[int]
        Initial coordinates at which to draw the header.
    header_height : int
        Total height of the header.
    font_header : ImageFont.FreeTypeFont
        Font used for the header.
    profile_picture : Image.Image
        Profile picture ready to be drawn in the graphic.

    Returns
    -------
    int
        Vertical coordinate at which to start drawing the tweet body.
    """
    x = coordinates[0]
    y = coordinates[1]

    username = tweet_info["user_name"]
    user_name = wrap(username, 19)
    user_tag = tweet_info["user_tag"]
    text_color = graphic_settings["color_scheme"][1]
    margin = graphic_settings["margin_bottom"]
    profile_pic_width = graphic_settings["profile_pic_size"][0]

    # Draw the username
    user_name = wrap(username, 38)
    for line in user_name:
        draw_interface.text((x, y), line, font=font_header, fill=text_color)
        y += font_header.size + margin

    # Draw the user tag
    draw_interface.text((x, y), user_tag, font=font_header, fill=text_color)

    # Calculate the vertical coordinate at which to start drawing the\
    # tweet text
    return_y = coordinates[1] + header_height + margin

    # Return the current vertical coordinate
    return return_y


def __get_initial_coordinates(
    graphic_settings: GraphicSettings,
    dimensions: Dict[str, List[int]]
) -> Tuple[int]:
    """Calculate the initial X and Y coordinates at which to start drawing.

    Parameters
    ----------
    graphic_settings : GraphicSettings
        Dictionary with the graphic's settings.
    dimensions : Dict[str, List[int]]
        Dictionary of the header and tweet text dimensions, respectively.

    Returns
    -------
    Tuple[int]
        Initial coordinates to start drawing at.
    """
    # Get header and tweet text dimensions
    header_width, header_height = dimensions["header"]
    text_width, text_height = dimensions["text"]
    img_size = graphic_settings["size"]
    margin = graphic_settings["margin_bottom"]

    # Horizontal coordinate to start drawing at (centered)
    if text_width > header_width:
        x = (img_size[0] - text_width) // 2
    else:
        x = (img_size[0] - header_width) // 2

    # Vertical coordinate to start drawing at (centered)
    content_height = header_height + text_height + margin
    y = (img_size[1] - content_height) // 2

    x = int(x)
    y = int(y)

    return (x, y)


def create_tweet(
    tweet_info: TweetInfo,
    graphic_settings: GraphicSettings,
    default_settings_format: DefaultFormats = DefaultFormats.CUSTOM.value,
    save_dir: Optional[str] = "",
) -> None:
    """Create a tweet graphic.

    Parameters
    ----------
    tweet_info : TweetInfo
        Dictionary with the necessary information about the tweet.
    graphic_settings : GraphicSettings
        Dictionary with the settings needed to draw the graphic.
    default_settings_format : DefaultFormats, optional
        Default graphic settings option chosen, by default DefaultFormats.CUSTOM.value
    save_dir : Optional[str], optional
        Directory in which to save the graphic., by default ""
    """
    # Validate the tweet info
    t_info = validate_tweet_info(tweet_info)
    # Use the graphic settings passed (either custom or default)
    graphic_settings = __choose_graphic_settings(
        tweet_info, graphic_settings, default_settings_format)

    # Get the tweet info received
    tweet_text = tweet_info["tweet_text"]
    user_pic = tweet_info["user_pic"]
    # Dimensions of the graphic
    img_size = graphic_settings["size"]
    # Final dimensions of the profile picture
    profile_pic_size = graphic_settings["profile_pic_size"]
    # Vertical margin in between lines
    margin_bottom = graphic_settings["margin_bottom"]
    background_color = graphic_settings["color_scheme"][0]
    text_color = graphic_settings["color_scheme"][1]
    # Maximum number of character per line of text
    chars_limit = graphic_settings["wrap_limit"]

    # Create all the fonts needed
    font_header, font_text = create_graphic_fonts(graphic_settings)

    # Process the profile picture
    if user_pic != "":
        # Process the profile picture
        profile_pic_processed = process_pic(graphic_settings, user_pic)

    # Dictionary with dimensions for the header and text (width, height)
    content_dims = calculate_content_dimensions(tweet_info, graphic_settings)
    header_height = content_dims["header"][1]

    # Create what will be the final image
    img = Image.new("RGBA", (img_size[0], img_size[1]), color=background_color)
    # Create the drawing interface
    draw = ImageDraw.Draw(img)

    # Calculate the inital drawing coordinates for the header
    x, y = __get_initial_coordinates(graphic_settings, content_dims)

    # Draw the header (and update the vertical coordinate to be where the\
    # tweet text starts)
    if user_pic == "":
        y = __draw_header_without_profile_pic(
            tweet_info, graphic_settings, img, draw, (x, y), header_height, font_header)
    else:
        y = __draw_header_with_profile_pic(
            tweet_info, graphic_settings, img, draw, (x, y), header_height, font_header, profile_pic_processed)

    # Split the tweet text into lines
    text_wrapped = wrap(tweet_text, chars_limit)
    # Draw the tweet text
    for line in text_wrapped:
        draw.text((x, y), line, font=font_text, fill=text_color)
        y += font_text.size + margin_bottom

    save_name = f"{tweet_info['tweet_name']}.png"
    save_name = path.join(save_dir, save_name)
    img.save(save_name)


def gen_tweets_from_file(
    file_path: str,
    graphic_settings: GraphicSettings,
    default_settings_format: DefaultFormats = DefaultFormats.CUSTOM.value,
    save_dir: Optional[str] = "",
) -> None:
    """Load tweets from a .json file and create a graphic for each one.

    If `default_settings_format` is passed, `graphic_settings` must be an empty dictionary.

    Parameters
    ----------
    file_path : str
        Path to the .json file with tweets.
    graphic_settings : GraphicSettings
        Dictionary of graphic settings.
    default_settings_format : DefaultFormats, optional
        Default graphic settings chosen, by default DefaultFormats.CUSTOM.value
    save_dir : Optional[str], optional
        Directory at which to save the graphic, by default ""
    """
    # Load the tweets from a JSON file as a list of tweet_info dictionaries
    json_tweets = get_ready_tweets(file_path)

    # Create a graphic for each quote
    for tweet in json_tweets:
        # Use the graphic settings passed (either custom or default)
        g_settings = __choose_graphic_settings(
            tweet, graphic_settings, default_settings_format)
        create_tweet(tweet, g_settings, save_dir=save_dir)
