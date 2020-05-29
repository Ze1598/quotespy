from typing import Tuple, List, Dict, Union, Optional
from PIL import ImageFont, Image
from re import findall
from .errors import FontNotFound, InvalidColorFormat, MissingGraphicSettings, MissingGraphicField, InvalidFormatOption, InvalidFieldLength, InvalidUsername, InvalidTweetName, InvalidUserTag, InvalidProfilePicturePath, InvalidTweetText, MissingDictKeys
from .type_interfaces import GraphicSettings, DefaultFormats, TweetInfo


def __validate_dict_keys(dict_data: Union[TweetInfo, GraphicSettings], typed_dict: Union[TweetInfo, GraphicSettings], dict_name: str) -> None:
    # Get the keys from the type interface
    if (dict_name == "graphic_settings"):
        keys = typed_dict.__annotations__.keys()
    elif (dict_name == "tweet_info"):
        keys = typed_dict.__annotations__.keys()

    # Get the keys given by the user
    provided_keys = dict_data.keys()
    # Get a list of the keys not provided by the user
    missing_keys = [key for key in keys if key not in provided_keys]

    # If there are any missing keys, raise an error
    if (missing_keys != list()):
        error_msg = f"The `{dict_name}` dictionary must include the keys:\n\t{keys}.\n\tYou are missing {missing_keys}"
        raise MissingDictKeys(error_msg)


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


def __validate_size(value, error_msg_length, error_msg_type):
    if len(value) != 2:
        raise InvalidFieldLength(error_msg_length)
    width = __validate_integer_fields(value[0], error_msg_type)
    height = __validate_integer_fields(value[1], error_msg_type)
    return [width, height]


def __validate_color_scheme(value, error_msg_size, error_msg_color_format):
    if len(value) != 2:
        raise InvalidFieldLength(error_msg_size)
    hex_color_pattern = r'^#(?:[0-9a-fA-F]{3}){1,2}$'
    background_color = findall(hex_color_pattern, value[0])
    text_color = findall(hex_color_pattern, value[1])
    if (background_color == list()) or (text_color == list()):
        raise InvalidColorFormat(error_msg_color_format)
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
        raise MissingGraphicSettings("You did not pass custom settings (`graphic_settings`) nor a default settings format (`default_settings_format`).\n\tYou can either specify your own settings in a dictionary or, if you don't want that, pass an empty dictionary and specify a default format: \"blue\", \"dark\" or \"light\".\n\tYou can call the `settings_help` method for indications on the fields needed for custom settings.")


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
    # Validate if the dictionary has all the required fields
    __validate_dict_keys(g_settings, GraphicSettings, "graphic_settings")

    font_family_error_msg = f"The font {g_settings['font_family']} was not in found in your machine.\n\tPlease note you can provide an absolute path to your font if needed."
    font_family_validated = __validate_font_family(
        g_settings["font_family"], font_family_error_msg)

    font_size_error_msg = "Please provide a number for the font size (preferably an integer)."
    font_size_header_validated = __validate_integer_fields(
        g_settings["font_size_header"], font_size_error_msg)
    font_size_text_validated = __validate_integer_fields(
        g_settings["font_size_text"], font_size_error_msg)

    size_error_msg_type = "Please provide a list of numbers for the width and height of the graphic (preferably an integer)."
    size_error_msg_length = "Please provide two measures for the graphic size: a first one for the width and a second for the height."
    size_validated = __validate_size(
        g_settings["size"], size_error_msg_length, size_error_msg_type)

    color_scheme_error_msg_format = "Please provide valid Hex color values for both the background and text colors."
    color_scheme_error_msg_length = "Please provide two colors for the color scheme: a first one for the background and a second for the text."
    color_scheme_validated = __validate_color_scheme(
        g_settings["color_scheme"], color_scheme_error_msg_length, color_scheme_error_msg_format)

    wrap_limit_error_msg = "Please provide a number for the maximum number of characters to include in each line of the graphic text (preferably an integer)."
    wrap_limit_validated = __validate_integer_fields(
        g_settings["wrap_limit"], wrap_limit_error_msg)

    margin_bottom_error_msg = "Please provide a number (float or int) for the margin bottom."
    margin_bottom_validated = __validate_float_fields(
        g_settings["margin_bottom"], margin_bottom_error_msg)

    validated_settings = {
        "font_family": font_family_validated,
        "font_size_header": font_size_header_validated,
        "font_size_text": font_size_text_validated,
        "size": size_validated,
        "color_scheme": color_scheme_validated,
        "wrap_limit": wrap_limit_validated,
        "margin_bottom": margin_bottom_validated
    }

    return validated_settings


def __validate_tweet_name(tweet_name: str, error_msg: str) -> str:
    if tweet_name == "":
        raise InvalidTweetName(error_msg)
    else:
        return tweet_name


def __validate_username(username: str, error_msg: str) -> str:
    if username == "" or len(username) > 50:
        raise InvalidUsername(error_msg)
    else:
        return username


def __validate_user_tag(user_tag: str, error_msg: str) -> str:
    tag_pattern = r'[\w]{1,15}'
    regex_match = findall(tag_pattern, user_tag)
    if (regex_match == list()):
        raise InvalidUserTag(error_msg)

    if (user_tag[0] == "@"):
        return user_tag
    else:
        return "@"+user_tag


def __validate_user_pic(user_pic_path: str, error_msg: str) -> str:
    try:
        pic = Image.open(user_pic_path, "r")
        return user_pic_path
    except:
        raise InvalidProfilePicturePath(error_msg)


def __validate_tweet_text(tweet_text: str, error_msg: str) -> str:
    if len(tweet_text) > 280:
        raise InvalidTweetText(tweet_text)
    else:
        tweet_text


def validate_tweet_info(t_info: TweetInfo) -> TweetInfo:
    # Validate if the input dictionary has all the required fields
    __validate_dict_keys(t_info, TweetInfo, "tweet_info")

    tweet_name_error_msg = "Please provide a valid name for your tweet. This will be used to name your graphic."
    tweet_name_validated = __validate_tweet_name(
        t_info["tweet_name"], tweet_name_error_msg)

    username_error_msg = "Please provide a valid Twitter username."
    username_validated = __validate_username(
        t_info["user_name"], username_error_msg)

    user_tag_error_msg = "Please provide a valid Twitter user tag/handle."
    user_tag_validated = __validate_user_tag(
        t_info["user_tag"], user_tag_error_msg)

    user_pic_error_msg = "Please provide a valid path for the profile picture location."
    user_pic_validated = __validate_user_pic(
        t_info["user_pic"], user_pic_error_msg)

    tweet_text_error_msg = "The tweet text must complies with the same rules as a normal tweet (namely the maximum of 280 characters)."
    tweet_text_validated = __validate_tweet_text(
        t_info["tweet_text"], tweet_text_error_msg)

    t_info_validated = {
        "tweet_name": tweet_name_validated,
        "user_name": username_validated,
        "user_tag": user_tag_validated,
        "user_pic": user_pic_validated,
        "tweet_text": tweet_text_validated
    }

    return t_info_validated
