from PIL import Image, ImageDraw, ImageFont
from random import choice
from textwrap import wrap
from typing import Tuple, List, Dict, Union, Optional
import utils as g_utils
from type_interfaces import GraphicInfo, GraphicSettings, DefaultFormats
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
        settings_file = f"quotespy\graphics\default_settings\default_settings_{default_settings_format}.json"
        chosen_settings = g_utils.parse_json_settings(settings_file)
    else:
        chosen_settings = graphic_settings
    # TODO: validate settings, no matter if custom or default
    # validate_g_settings(chosen_settings)
    
    return chosen_settings


def create_img(
    graphic_info: GraphicInfo,
    graphic_settings: GraphicSettings,
    default_settings_format: Optional[DefaultFormats] = DefaultFormats.CUSTOM.value,
    save_dir: Optional[str] = ""
) -> None:
    """Create a single graphic given the title, the text and the graphic settings.
    create_img(graphic_info, graphic_settings)

    Create a single graphic given a tuple of (title, text_to_draw), a dictionary of various settings for the graphic (font family, font size, size of the image, color scheme, max number of characters per line and vertical magin between lines) and the desired file extension for the final image.

    If `default_settings_format` is passed, `graphic_settings` must be an empty dictionary.

    Parameters
    ----------
    graphic_info : GraphicInfo
        Dictionary with the title and the text of the graphic.
    graphic_settings : GraphicSettings
        Dictionary with the settings for the graphic. This includes font_family, font_size, size, color_scheme, wrap_limit and margin_bottom.
    default_settings_format : DefaultFormats
        If "lyrics" or "quote" is passed, `graphic_settings` is ignored and the graphic uses the respective default settings; otherwise defaults to an empty string (`DefaultFormats.Custom.value`), i.e., it is ignored.
    save_dir : str
        Destination path of the created graphic.
    file_ext : str
        File extension for the graphic (image).
    """
    # Use the graphic settings passed (either custom or default)
    g_settings = __choose_graphic_settings(graphic_settings, default_settings_format)

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
    file_name: str,
    graphic_settings: GraphicSettings,
    default_settings_format: DefaultFormats = DefaultFormats.CUSTOM.value,
    save_dir: Optional[str] = ""
) -> None:
    """Load quotes from the specified TXT or JSON file and create a graphic for each one.

    If `default_settings_format` is passed, `graphic_settings` must be an empty dictionary.
    """
    # Get the quotes from the source file (TXT or JSON) (make sure duplicate\
    # titles have their respective frequency in the name)
    titles_quotes_updated = g_utils.get_ready_text(file_name)
    # Use the graphic settings passed (either custom or default)
    g_settings = __choose_graphic_settings(graphic_settings,default_settings_format)

    # Create a graphic for each quote
    for quote in titles_quotes_updated:
        quote_dict = {"title": quote, "text": titles_quotes_updated[quote]}
        create_img(quote_dict, g_settings, save_dir=save_dir)


if __name__ == "__main__":
    # Load lyrics from a txt file and create graphics
    lyrics_source = "lyrics.txt"
    # Load the settings from a JSON file
    lyrics_settings = g_utils.parse_json_settings(
        "quotespy\graphics\default_settings\default_settings_lyrics.json"
    )
    # gen_graphics(lyrics_source, lyrics_settings)
    gen_graphics(lyrics_source, {}, default_settings_format="lyrics")

    # Create a single graphic
    info = {
        "title": "crown_of_shit",
        "text": "You don't get anything playing the part when it's insincere yet you canonize yourself while you wear this crown of shit"
    }
    quote_settings = g_utils.parse_json_settings(
        "quotespy\graphics\default_settings\default_settings_quote.json")
    quotes_source = "quotes.json"
    # gen_graphics(quotes_source, quote_settings)
    # gen_graphics(quotes_source, {}, default_settings_format="quote")
    create_img(info, {}, default_settings_format="quote")