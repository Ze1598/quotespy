from os import path

import pytest
from PIL import Image, ImageDraw, ImageFont
from pytest_mock import mocker

import quotespy
import quotespy.tweet_graphics.tools.errors as errors
import quotespy.tweet_graphics.tools.validation as validation
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
                           missing_font_size_text, missing_margin,
                           missing_name, missing_pic, missing_size,
                           missing_tag, missing_text, missing_username,
                           missing_wrap_limit, valid_custom_settings,
                           valid_info, valid_info_list, invalid_color_scheme_rgba,
                           valid_custom_settings_rgba, valid_custom_settings_none_bg)


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


@pytest.mark.parametrize("custom_settings, default_format, expected_result", [
    (valid_custom_settings, "", valid_custom_settings),
    ({}, "blue", blue_mode_settings),
    ({}, "light", light_mode_settings),
    ({}, "dark", dark_mode_settings),
    (valid_custom_settings, "blue", valid_custom_settings),
    (valid_custom_settings, "light", valid_custom_settings),
    (valid_custom_settings, "dark", valid_custom_settings),
    (valid_custom_settings_rgba, "", valid_custom_settings),
    (valid_custom_settings_none_bg, "", valid_custom_settings)
])
def test_choose_settings_valid(mocker, custom_settings, default_format, expected_result):
    spy = mocker.spy(src, "__choose_graphic_settings")
    src.__choose_graphic_settings(custom_settings, default_format)
    assert spy.spy_return == expected_result


@pytest.mark.parametrize("custom_settings, default_format, expected_error", [
    ({}, "", errors.MissingGraphicSettings),
    (missing_font_family, "", errors.MissingDictKeys),
    (missing_font_size_header, "", errors.MissingDictKeys),
    (missing_font_size_text, "", errors.MissingDictKeys),
    (missing_size, "", errors.MissingDictKeys),
    (missing_color_scheme, "", errors.MissingDictKeys),
    (missing_wrap_limit, "", errors.MissingDictKeys),
    (missing_margin, "", errors.MissingDictKeys),
    (invalid_font_family, "", errors.FontNotFound),
    (invalid_font_size_header, "", TypeError),
    (invalid_font_size_text, "", TypeError),
    (invalid_size_length, "", errors.InvalidFieldLength),
    (invalid_size_value, "", TypeError),
    (invalid_color_scheme_length, "", errors.InvalidFieldLength),
    (invalid_color_scheme_value, "", errors.InvalidColorFormat),
    (invalid_wrap_limit, "", TypeError),
    (invalid_margin_bottom, "", TypeError),
])
def test_choose_settings_invalid(mocker, custom_settings, default_format, expected_error):
    with pytest.raises(expected_error):
        src.__choose_graphic_settings(custom_settings, default_format)


@pytest.mark.parametrize("graphic_info, graphic_settings, default_format, save_dir", [
    (valid_info, valid_custom_settings, "", ""),
    (valid_info, valid_custom_settings, "blue", ""),
    (valid_info, valid_custom_settings, "light", ""),
    (valid_info, valid_custom_settings, "dark", ""),
    (valid_info, valid_custom_settings, "", "C:\\Users\\user\\Desktop"),
    (valid_info, valid_custom_settings, "blue", "C:\\Users\\user\\Desktop"),
    (valid_info, valid_custom_settings, "light", "C:\\Users\\user\\Desktop"),
    (valid_info, valid_custom_settings, "dark", "C:\\Users\\user\\Desktop"),
    (valid_info, {}, "blue", ""),
    (valid_info, {}, "blue", "C:\\Users\\user\\Desktop"),
    (valid_info, {}, "light", ""),
    (valid_info, {}, "light", "C:\\Users\\user\\Desktop"),
    (valid_info, {}, "dark", ""),
    (valid_info, {}, "dark", "C:\\Users\\user\\Desktop"),
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
    (valid_info, missing_font_family, "", errors.MissingDictKeys),
    (valid_info, missing_font_size_header, "", errors.MissingDictKeys),
    (valid_info, missing_font_size_text, "", errors.MissingDictKeys),
    (valid_info, missing_size, "", errors.MissingDictKeys),
    (valid_info, missing_color_scheme, "", errors.MissingDictKeys),
    (valid_info, missing_wrap_limit, "", errors.MissingDictKeys),
    (valid_info, missing_margin, "", errors.MissingDictKeys),
    (valid_info, invalid_font_family, "", errors.FontNotFound),
    (valid_info, invalid_font_size_header, "", TypeError),
    (valid_info, invalid_font_size_text, "", TypeError),
    (valid_info, invalid_size_length, "", errors.InvalidFieldLength),
    (valid_info, invalid_size_value, "", TypeError),
    (valid_info, invalid_color_scheme_length, "", errors.InvalidFieldLength),
    (valid_info, invalid_color_scheme_value, "", errors.InvalidColorFormat),
    (valid_info, invalid_color_scheme_rgba, "", errors.InvalidColorFormat),
    (valid_info, invalid_wrap_limit, "", TypeError),
    (valid_info, invalid_margin_bottom, "", TypeError)
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


def test_draw_header(mocker):
    coords = (197, 602)
    return_y = 837
    dummy_img = Image.new("RGB", (0, 0), color="black")
    draw = ImageDraw.Draw(dummy_img)
    font_header = ImageFont.truetype("arial.ttf", 80, encoding="utf-8")
    spy = mocker.spy(src, "__draw_header")

    src.__draw_header(
        "test",
        "@test",
        "",
        [1800, 1800],
        dummy_img,
        draw,
        coords,
        30,
        font_header,
        "black"
    )
    assert spy.spy_return == return_y


def test_get_initial_coords(mocker):
    size = [1800, 1800]
    dimensions = {'header': [770, 48.0], 'text': [1406, 548]}
    return_coords = (197, 602)
    spy = mocker.spy(src, "__get_initial_coordinates")

    src.__get_initial_coordinates(size, dimensions)
    assert spy.spy_return == return_coords


@pytest.mark.parametrize("color, expected_value", [
    ("rgba(0,0,0,0)", "rgba(0, 0, 0, 0)"),
    ("rgba(0,0,0,1)", "rgba(0, 0, 0, 255)"),
    ("rgba(0,0,255,0)", "rgba(0, 0, 255, 0)"),
    ("rgba(123,124,12,0.75)", "rgba(123, 124, 12, 191)"),
    
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
        validation.__validate_color_scheme(color_scheme, error_msg_size, error_msg_format)