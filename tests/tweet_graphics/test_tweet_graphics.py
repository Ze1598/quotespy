from os import path

import pytest
from PIL import Image, ImageDraw, ImageFont
from pytest_mock import mocker

import quotespy
import quotespy.tweet_graphics.tools.errors as errors
import quotespy.tweet_graphics.tools.validation as validation
import quotespy.tweet_graphics.tools.utils as utils
import quotespy.tweet_graphics.tweet_graphics as src

from .data_samples import (blue_mode_settings, dark_mode_settings,
                           invalid_color_scheme_length,
                           invalid_color_scheme_value, invalid_font_family,
                           invalid_font_size_header, invalid_font_size_text,
                           invalid_margin_bottom, invalid_name,
                           invalid_size_length, invalid_size_value,
                           invalid_tag, invalid_text, invalid_user_pic,
                           invalid_username, invalid_wrap_limit,
                           light_mode_settings, missing_color_scheme,
                           missing_font_family, missing_font_size_header,
                           missing_profile_pic_size,
                           invalid_profile_pic_size_length,
                           invalid_profile_pic_size_value,
                           missing_font_size_text, missing_margin,
                           missing_name, missing_pic, missing_size,
                           missing_tag, missing_text, missing_username,
                           missing_wrap_limit, valid_custom_settings,
                           valid_info_no_picture, valid_info_with_picture,
                           valid_info_list, invalid_color_scheme_rgba,
                           valid_custom_settings_rgba, valid_custom_settings_none_bg,
                           valid_custom_settings_rgba_returned,
                           valid_custom_settings_none_bg_returned,
                           valid_custom_settings_returned,
                           blue_mode_settings_returned,
                           dark_mode_settings_returned,
                           light_mode_settings_returned)


@pytest.mark.parametrize("format_chosen, return_settings", [
    ("blue", blue_mode_settings),
    ("light", light_mode_settings),
    ("dark", dark_mode_settings),
    ("", None)
])
def test_load_settings(mocker, format_chosen, return_settings):
    spy = mocker.spy(src, "__load_default_settings")
    # format_chosen = "lyrics"
    src.__load_default_settings(format_chosen)
    assert spy.spy_return == return_settings


@pytest.mark.parametrize("tweet_info, graphic_settings, default_format, expected_result", [
    (valid_info_with_picture, valid_custom_settings,
     "", valid_custom_settings_returned),
    (valid_info_with_picture, {}, "blue", blue_mode_settings_returned),
    (valid_info_with_picture, {}, "light", light_mode_settings_returned),
    (valid_info_with_picture, {}, "dark", dark_mode_settings_returned),
    (valid_info_with_picture, valid_custom_settings,
     "blue", valid_custom_settings_returned),
    (valid_info_with_picture, valid_custom_settings,
     "light", valid_custom_settings_returned),
    (valid_info_with_picture, valid_custom_settings,
     "dark", valid_custom_settings_returned),
    (valid_info_with_picture, valid_custom_settings_rgba,
     "", valid_custom_settings_rgba_returned),
    (valid_info_with_picture, valid_custom_settings_none_bg,
     "", valid_custom_settings_none_bg_returned)
])
def test_choose_settings_valid(mocker, tweet_info, graphic_settings, default_format, expected_result):
    settings_chosen = src.__choose_graphic_settings(
        tweet_info,
        graphic_settings,
        default_format
    )
    assert settings_chosen == expected_result


@pytest.mark.parametrize("tweet_info, custom_settings, default_format, expected_error", [
    (valid_info_with_picture, {}, "", errors.MissingGraphicSettings),
    (valid_info_with_picture, missing_font_family, "", errors.MissingDictKeys),
    (valid_info_with_picture, missing_font_size_header, "", errors.MissingDictKeys),
    (valid_info_with_picture, missing_font_size_text, "", errors.MissingDictKeys),
    (valid_info_with_picture, missing_size, "", errors.MissingDictKeys),
    (valid_info_with_picture, missing_color_scheme, "", errors.MissingDictKeys),
    (valid_info_with_picture, missing_wrap_limit, "", errors.MissingDictKeys),
    (valid_info_with_picture, missing_margin, "", errors.MissingDictKeys),
    (valid_info_with_picture, invalid_font_family, "", errors.FontNotFound),
    (valid_info_with_picture, invalid_font_size_header, "", TypeError),
    (valid_info_with_picture, invalid_font_size_text, "", TypeError),
    (valid_info_with_picture, invalid_size_length, "", errors.InvalidFieldLength),
    (valid_info_with_picture, invalid_size_value, "", TypeError),
    (valid_info_with_picture, invalid_color_scheme_length,
     "", errors.InvalidFieldLength),
    (valid_info_with_picture, invalid_color_scheme_value,
     "", errors.InvalidColorFormat),
    (valid_info_with_picture, invalid_wrap_limit, "", TypeError),
    (valid_info_with_picture, invalid_margin_bottom, "", TypeError),
])
def test_choose_settings_invalid(mocker, tweet_info, custom_settings, default_format, expected_error):
    with pytest.raises(expected_error):
        src.__choose_graphic_settings(
            tweet_info, custom_settings, default_format)


@pytest.mark.parametrize("graphic_info, graphic_settings, default_format, save_dir", [
    (valid_info_no_picture, valid_custom_settings, "", ""),
    (valid_info_no_picture, valid_custom_settings, "blue", ""),
    (valid_info_no_picture, valid_custom_settings, "light", ""),
    (valid_info_no_picture, valid_custom_settings, "dark", ""),
    (valid_info_no_picture, valid_custom_settings, "", "C:\\Users\\user\\Desktop"),
    (valid_info_no_picture, valid_custom_settings,
     "blue", "C:\\Users\\user\\Desktop"),
    (valid_info_no_picture, valid_custom_settings,
     "light", "C:\\Users\\user\\Desktop"),
    (valid_info_no_picture, valid_custom_settings,
     "dark", "C:\\Users\\user\\Desktop"),
    (valid_info_no_picture, {}, "blue", ""),
    (valid_info_no_picture, {}, "blue", "C:\\Users\\user\\Desktop"),
    (valid_info_no_picture, {}, "light", ""),
    (valid_info_no_picture, {}, "light", "C:\\Users\\user\\Desktop"),
    (valid_info_no_picture, {}, "dark", ""),
    (valid_info_no_picture, {}, "dark", "C:\\Users\\user\\Desktop")
])
def test_create_tweet(mocker, graphic_info, graphic_settings, default_format, save_dir):
    # Mock the `save` method
    mocker.patch("PIL.Image.Image.save")
    # Create a graphic
    src.create_tweet(
        graphic_info,
        graphic_settings,
        default_settings_format=default_format,
        save_dir=save_dir)
    # Assert the `save` method was called with the appropiate file name
    save_name = f"{graphic_info['tweet_name']}.png"
    save_name = path.join(save_dir, save_name)
    Image.Image.save.assert_called_once_with(save_name)


@pytest.mark.parametrize("graphic_info, graphic_settings, default_format, expected_error", [
    ({}, {}, "", errors.MissingDictKeys),
    (missing_name, {}, "", errors.MissingDictKeys),
    (missing_username, {}, "", errors.MissingDictKeys),
    (missing_tag, {}, "", errors.MissingDictKeys),
    (missing_pic, {}, "", errors.MissingDictKeys),
    (missing_text, {}, "", errors.MissingDictKeys),
    (valid_info_no_picture, missing_font_family, "", errors.MissingDictKeys),
    (valid_info_no_picture, missing_font_size_header, "", errors.MissingDictKeys),
    (valid_info_no_picture, missing_font_size_text, "", errors.MissingDictKeys),
    (valid_info_no_picture, missing_size, "", errors.MissingDictKeys),
    (valid_info_no_picture, missing_profile_pic_size, "", errors.MissingDictKeys),
    (valid_info_no_picture, missing_color_scheme, "", errors.MissingDictKeys),
    (valid_info_no_picture, missing_wrap_limit, "", errors.MissingDictKeys),
    (valid_info_no_picture, missing_margin, "", errors.MissingDictKeys),
    (valid_info_no_picture, invalid_font_family, "", errors.FontNotFound),
    (valid_info_no_picture, invalid_font_size_header, "", TypeError),
    (valid_info_no_picture, invalid_font_size_text, "", TypeError),
    (valid_info_no_picture, invalid_size_length, "", errors.InvalidFieldLength),
    (valid_info_no_picture, invalid_size_value, "", TypeError),
    (valid_info_no_picture, invalid_profile_pic_size_length,
     "", errors.InvalidFieldLength),
    (valid_info_no_picture, invalid_profile_pic_size_value, "", TypeError),
    (valid_info_no_picture, invalid_color_scheme_length, "", errors.InvalidFieldLength),
    (valid_info_no_picture, invalid_color_scheme_value, "", errors.InvalidColorFormat),
    (valid_info_no_picture, invalid_color_scheme_rgba, "", errors.InvalidColorFormat),
    (valid_info_no_picture, invalid_wrap_limit, "", TypeError),
    (valid_info_no_picture, invalid_margin_bottom, "", TypeError)
])
def test_create_graphic_fails(mocker, graphic_info, graphic_settings, default_format, expected_error):
    # Mock the `save` method
    mocker.patch("PIL.Image.Image.save")
    with pytest.raises(expected_error):
        #  Create a graphic
        src.create_tweet(
            graphic_info,
            graphic_settings,
            default_settings_format=default_format
        )


@pytest.mark.parametrize("graphic_info, graphic_settings, expected_dimensions", [
    (valid_info_no_picture, valid_custom_settings,
     {"header": [680, 210], "text": [542, 92]}),
    (valid_info_with_picture, valid_custom_settings,
     {"header": [680, 210], "text": [542, 92]})
])
def test_calculate_content_dimensions(mocker, graphic_info, graphic_settings, expected_dimensions):
    content_dimensions = utils.calculate_content_dimensions(
        graphic_info, graphic_settings)
    assert content_dimensions == expected_dimensions


@pytest.mark.parametrize("tweet_info, graphic_settings", [
    (valid_info_no_picture, blue_mode_settings),
    (valid_info_no_picture, dark_mode_settings),
    (valid_info_no_picture, light_mode_settings)
])
def test_draw_header_without_profile_pic(mocker, tweet_info, graphic_settings):
    coords = (620, 734)
    return_y = 974
    header_height = 210

    img_size = graphic_settings["size"]
    bg_color = graphic_settings["color_scheme"][0]
    font_family = graphic_settings["font_family"]
    font_size = graphic_settings["font_size_header"]

    dummy_img = Image.new("RGB", img_size, color=bg_color)
    draw = ImageDraw.Draw(dummy_img)
    font_header = ImageFont.truetype(font_family, font_size, encoding="utf-8")
    spy = mocker.spy(src, "__draw_header_without_profile_pic")

    src.__draw_header_without_profile_pic(
        tweet_info,
        graphic_settings,
        dummy_img,
        draw,
        coords,
        header_height,
        font_header
    )
    assert spy.spy_return == return_y


@pytest.mark.parametrize("tweet_info, graphic_settings", [
    (valid_info_with_picture, valid_custom_settings),
    (valid_info_with_picture, valid_custom_settings_rgba),
    (valid_info_with_picture, valid_custom_settings_none_bg)
])
def test_draw_header_with_profile_pic(mocker, tweet_info, graphic_settings):
    coords = (377, 732)
    return_y = 956
    header_height = 194

    img_size = graphic_settings["size"]
    profile_pic_size = graphic_settings["profile_pic_size"]
    bg_color = graphic_settings["color_scheme"][0]
    font_family = graphic_settings["font_family"]
    font_size = graphic_settings["font_size_header"]

    dummy_img = Image.new("RGB", img_size, color=bg_color)
    dummy_profile_pic = Image.new("RGBA", profile_pic_size, color="black")
    draw = ImageDraw.Draw(dummy_img)
    font_header = ImageFont.truetype(font_family, font_size, encoding="utf-8")
    spy = mocker.spy(src, "__draw_header_with_profile_pic")

    src.__draw_header_with_profile_pic(
        tweet_info,
        graphic_settings,
        dummy_img,
        draw,
        coords,
        header_height,
        font_header,
        dummy_profile_pic
    )
    assert spy.spy_return == return_y


@pytest.mark.parametrize("graphic_settings", [
    (blue_mode_settings),
    (dark_mode_settings),
    (light_mode_settings)
])
def test_get_initial_coords(mocker, graphic_settings):
    dimensions = {"header": [797.0, 194.0], "text": [1045, 111.0]}
    return_coords = (377, 732)
    spy = mocker.spy(src, "__get_initial_coordinates")

    src.__get_initial_coordinates(graphic_settings, dimensions)
    assert spy.spy_return == return_coords


@pytest.mark.parametrize("color, expected_value", [
    ("rgba(0,0,0,0)", "rgba(0, 0, 0, 0)"),
    ("rgba(0,0,0,1)", "rgba(0, 0, 0, 255)"),
    ("rgba(0,0,255,0)", "rgba(0, 0, 255, 0)"),
    ("rgba(123,124,12,0.75)", "rgba(123, 124, 12, 191)")
])
def test_validate_rgba(mocker, color, expected_value):
    error_msg = "Invalid color format"
    assert expected_value == validation.__validate_rgba(color, error_msg)


@pytest.mark.parametrize("g_settings", [
    (invalid_color_scheme_rgba)
])
def test_validate_rgba_fails(mocker, g_settings):
    error_msg_size = "Too few colors"
    error_msg_format = "Invalid color format"
    color_scheme = g_settings["color_scheme"]
    with pytest.raises(errors.InvalidColorFormat):
        validation.__validate_color_scheme(
            color_scheme, error_msg_size, error_msg_format)


@pytest.mark.parametrize("graphic_settings", [
    (blue_mode_settings_returned),
    (dark_mode_settings_returned),
    (light_mode_settings_returned),
    (valid_custom_settings_returned),
    (valid_custom_settings_rgba_returned),
    (valid_custom_settings_none_bg_returned)
])
def test_create_graphic_fonts_header(mocker, graphic_settings):
    font_family = graphic_settings["font_family"]
    font_size = graphic_settings["font_size_header"]

    font_header, _ = utils.create_graphic_fonts(graphic_settings)
    # font_header_family = font_header.getname()[0]
    font_header_size = font_header.size
    # font_header_encoding = font_header.encoding

    # assert font_family == font_header_family
    assert font_size == font_header_size


@pytest.mark.parametrize("graphic_settings", [
    (blue_mode_settings_returned),
    (dark_mode_settings_returned),
    (light_mode_settings_returned),
    (valid_custom_settings_returned),
    (valid_custom_settings_rgba_returned),
    (valid_custom_settings_none_bg_returned)
])
def test_create_graphic_fonts_text(mocker, graphic_settings):
    font_family = graphic_settings["font_family"]
    font_size = graphic_settings["font_size_text"]

    _, font_text = utils.create_graphic_fonts(graphic_settings)
    # font_text_family = font_text.getname()[0]
    font_text_size = font_text.size
    # font_text_encoding = font_text.encoding

    # assert font_family == font_text_family
    assert font_size == font_text_size
