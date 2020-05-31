from os import path
from random import choice
from textwrap import wrap
from typing import Dict, List, Optional, Tuple, Union
from PIL import Image, ImageDraw, ImageFont
from .tools.default_settings import (default_settings_lyrics,
                                     default_settings_quote)
from .tools.errors import MissingGraphicSettings
from .tools.type_interfaces import DefaultFormats, GraphicInfo, GraphicSettings
from .tools.utils import get_ready_text, parse_json_settings
from .tools.validation import (validate_format_option, validate_g_settings,
                               validate_graphic_info,
                               validate_settings_existence)


def __load_default_settings(
    default_settings_format: str
) -> GraphicSettings:
    """Load the default graphic settings depending on what is chosen.

    Parameters
    ----------
    default_settings_format : str
        Name of the default settings format.

    Returns
    -------
    GraphicSettings
        Loaded default graphic settings.
    """
    if default_settings_format == DefaultFormats.LYRICS.value:
        return default_settings_lyrics
    elif default_settings_format == DefaultFormats.QUOTE.value:
        return default_settings_quote


def __choose_graphic_settings(
    graphic_settings: GraphicSettings,
    default_settings_format: DefaultFormats = DefaultFormats.CUSTOM.value
) -> GraphicSettings:
    """Based on the custom graphic settings and (lack of) default settings passed,
    choose the settings to be used.

    Parameters
    ----------
    graphic_settings : GraphicSettings
        Dictionary of custom graphic settings.
    default_settings_format : DefaultFormats, optional
        Name of the default settings format to use, by default DefaultFormats.CUSTOM.value

    Returns
    -------
    GraphicSettings
        Graphic settings to be used for the graphic creation.
    """
    # Validate that either custom or default settings were passed
    validate_settings_existence(
        graphic_settings, default_settings_format)

    # Validate and sanitize the default settings format chosen
    if default_settings_format != "":
        default_settings_format = validate_format_option(
            default_settings_format)

    # If the custom settings are just an empty dict, load the default settings format specified
    if (graphic_settings == dict()):
        chosen_settings = __load_default_settings(default_settings_format)

    # Otherwise, use the custom settings
    else:
        chosen_settings = graphic_settings

    # Validate the chosen settings, independent of it being custom or default settings
    validate_g_settings(chosen_settings)

    return chosen_settings


def create_graphic(
    graphic_info: GraphicInfo,
    graphic_settings: GraphicSettings,
    default_settings_format: Optional[DefaultFormats] = DefaultFormats.CUSTOM.value,
    save_dir: Optional[str] = ""
) -> None:
    """Create a single graphic given the title, the text and the graphic settings.
    create_img(graphic_info, graphic_settings)

    Create a single graphic given a tuple of (title, text_to_draw), a dictionary of various settings for the graphic (font family, font size, size of the image, color scheme, max number of characters per line and vertical magin between lines) and the desired file extension for the final image.

    If `default_settings_format` is passed, `graphic_settings` should be an empty dictionary.

    Parameters
    ----------
    graphic_info : GraphicInfo
        Dictionary with the title and the text of the graphic.
    graphic_settings : GraphicSettings
        Dictionary with the settings for the graphic. This includes font_family, font_size, size, color_scheme, wrap_limit and margin_bottom.
    default_settings_format : Optional[DefaultFormats], optional
        Default graphic settings format to use, by default DefaultFormats.CUSTOM.value
    save_dir : Optional[str], optional
        Destination path of the created graphic, by default ""
    """
    # Validate the graphic info
    validate_graphic_info(graphic_info)

    # Use the graphic settings passed (either custom or default)
    g_settings = __choose_graphic_settings(
        graphic_settings, default_settings_format)

    # Set up variables
    FNT = ImageFont.truetype(
        g_settings["font_family"],
        g_settings["font_size"],
        encoding="utf-8"
    )
    WIDTH, HEIGHT = g_settings["size"]
    # Break down the text into lines with a maximum of `wrap_limit` characters
    text_wrapped = wrap(graphic_info["text"], g_settings["wrap_limit"])

    # Find the height and width needed to draw the text
    temp_img = Image.new("RGB", (0, 0))
    temp_img = ImageDraw.Draw(temp_img)

    # Height of each text line to be drawn
    line_heights = [
        temp_img.textsize(text_wrapped[i], font=FNT)[1]
        for i in range(len(text_wrapped))]
    # Width of the longest line (hence the width of the text)
    width_text = max([
        temp_img.textsize(line, font=FNT)[0]
        for line in text_wrapped])
    # Total height needed to draw all lines
    height_text = sum(line_heights)
    # Set up the height at which to draw the next line (the first one right now)
    y = (HEIGHT - height_text) // 2

    # Create a new image
    img = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        color=g_settings["color_scheme"][0]
    )
    # Create the drawing interface
    drawing_interface = ImageDraw.Draw(img)

    # Draw each line of text
    for line in text_wrapped:
        # Find the X coordinate at which to draw the line, horizontally-centered
        line_width = drawing_interface.textsize(line, font=FNT)[0]
        x = (WIDTH - line_width) // 2

        # Draw the line
        drawing_interface.text(
            (x, y),
            line,
            font=FNT,
            fill=g_settings["color_scheme"][1]
        )

        # Update the Y coordinate for the next line
        y += g_settings["margin_bottom"]

    # Save the image
    save_name = f"{graphic_info['title']}.png"
    save_name = path.join(save_dir, save_name)
    img.save(save_name)


def gen_graphics(
    file_path: str,
    graphic_settings: GraphicSettings,
    default_settings_format: DefaultFormats = DefaultFormats.CUSTOM.value,
    save_dir: Optional[str] = ""
) -> None:
    """Load quotes from the specified .txt or .json file and create a graphic for each one.

    If `default_settings_format` is passed, `graphic_settings` must be an empty dictionary.

    Parameters
    ----------
    file_path : str
        Path to the .txt or .json file with lyrics/quotes.
    graphic_settings : GraphicSettings
        Custom settings for the graphics. 
    default_settings_format : DefaultFormats, optional
        Default graphic settings format to use, by default DefaultFormats.CUSTOM.value
    save_dir : Optional[str], optional
        Destination path of the created graphic, by default ""
    """
    # Get the quotes from the source file (TXT or JSON) (make sure duplicate\
    # titles have their respective frequency in the name)
    titles_quotes_updated = get_ready_text(file_path)
    # Use the graphic settings passed (either custom or default)
    g_settings = __choose_graphic_settings(
        graphic_settings, default_settings_format)

    # Create a graphic for each quote
    for quote in titles_quotes_updated:
        quote_dict = {"title": quote, "text": titles_quotes_updated[quote]}
        create_graphic(quote_dict, g_settings, save_dir=save_dir)
