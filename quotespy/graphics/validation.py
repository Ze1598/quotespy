from typing import Tuple, List, Dict, Union, Optional
from PIL import ImageFont
from errors import FontNotFound, InvalidColorFormat, MissingGraphicSettings, MissingGraphicField, InvalidFormatOption
from re import findall
from type_interfaces import GraphicSettings, DefaultFormats, DefaultFormats

# print(GraphicSettings.__annotations__)


def __validate_font_family(value, error_msg):
    try:
        dummy_font = ImageFont.truetype(value, 1, encoding="utf-8")
        return value
    except OSError:
        raise FontNotFound(error_msg)


def __validate_integer_fields(value, error_msg):
    try:
        int_field = int(value)
        return int_field
    except ValueError:
        raise TypeError(error_msg)
    pass


def __validate_size(value, error_msg):
    width = __validate_integer_fields(value[0], error_msg)
    height = __validate_integer_fields(value[1], error_msg)
    return [width, height]


def __validate_color_scheme(value, error_msg):
    hex_color_pattern = r'^#(?:[0-9a-fA-F]{3}){1,2}$'
    background_color = findall(hex_color_pattern, value[0])
    text_color = findall(hex_color_pattern, value[1])
    if (background_color == None) or (text_color == None):
        raise InvalidColorFormat(error_msg)
    else:
        return [background_color[0], text_color[0]]


def __validate_float_fields(value, error_msg):
    try:
        float_field = float(value)
        return float_field
    except TypeError:
        raise TypeError(error_msg)


def validate_settings_existence(g_settings, def_settings) -> None:
    settings_not_received = (g_settings == dict()) and (
        def_settings == DefaultFormats.CUSTOM.value)
    if settings_not_received:
        raise MissingGraphicSettings("You did not pass custom settings (`graphic_settings`) nor a default settings format (`default_settings_format`).\n\tYou can either specify your own settings in a dictionary or, if you don't want that, pass an empty dictionary and specify a default format: \"lyrics\" or \"quote\".\n\tYou can call the `settings_help` method for indications on the fields needed for custom settings.")


def validate_format_option(format_option):
    valid_options = [option.value for option in DefaultFormats]
    format_option = format_option.lower()
    if format_option in valid_options:
        return format_option
    else:
        avail_options = [option for option in valid_options if option != ""]
        error_msg = f"You chose an invalid default graphic settings format.\n\tPlease choose one of this: {avail_options}"
        raise InvalidFormatOption(error_msg)


def validate_g_settings(g_settings: GraphicSettings) -> GraphicSettings:
    font_family_error_msg = f"The font {g_settings['font_family']} was not in found in your machine.\n\tPlease note you can provide an absolute path to your font if needed."
    font_family_validated = __validate_font_family(
        g_settings["font_family"], font_family_error_msg)

    font_size_error_msg = "Please provide a number for the font size (preferably an integer)."
    font_size_validated = __validate_integer_fields(
        g_settings["font_size"], font_size_error_msg)

    size_error_msg = "Please provide a list of numbers for the width and height of the graphic (preferably an integer)."
    size_validated = __validate_size(
        [g_settings["size"][0], g_settings["size"][1]], size_error_msg)

    color_scheme_error_msg = "Please provide valid Hex color values for both the background and text colors."
    color_scheme_validated = __validate_color_scheme(
        g_settings["color_scheme"], color_scheme_error_msg)

    wrap_limit_error_msg = "Please provide a number for the maximum number of characters to include in each line of the graphic text (preferably an integer)."
    wrap_limit_validated = __validate_integer_fields(
        g_settings["wrap_limit"], wrap_limit_error_msg)

    margin_bottom_error_msg = "Please provide a number (float or int) for the margin bottom."
    margin_bottom_validated = __validate_float_fields(
        g_settings["margin_bottom"], margin_bottom_error_msg)

    validated_settings = {
        "font_family": font_family_validated,
        "font_size": font_size_validated,
        "size": size_validated,
        "color_scheme": color_scheme_validated,
        "wrap_limit": wrap_limit_validated,
        "margin_bottom": margin_bottom_validated
    }

    return validated_settings


def __validate_graphic_info_field(g_info, field, error_msg) -> None:
    try:
        field = g_info[field]
    except KeyError:
        raise MissingGraphicField(error_msg)

    if type(field) != str:
        raise MissingGraphicField(error_msg)


def validate_graphic_info(g_info) -> None:
    title_error_msg = "The graphic info dictionary must have a \"title\" field with the title of the graphic as a string."
    __validate_graphic_info_field(g_info, "title", title_error_msg)
    text_error_msg = "The graphic info dictionary must have a \"text\" field with the quote/lyrics you want to be drawn, as a string."
    __validate_graphic_info_field(g_info, "text", text_error_msg)


if __name__ == "__main__":
    sample_settings: GraphicSettings = {
        "font_family": "Inkfree.ttf",
        "font_size": 200,
        "size": [2800, 2800],
        "color_scheme": ["#000000", "#ffffff"],
        "wrap_limit": 20,
        "margin_bottom": 312.5
    }
    validate_g_settings(sample_settings)

    sample_info = {
        "title": "crown_of_shit",
        "text": "You don't get anything playing the part when it's insincere yet you canonize yourself while you wear this crown of shit"
    }
    validate_graphic_info(sample_info)

    # validate_format_option("afadf")
    validate_format_option("quote")
