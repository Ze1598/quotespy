from os import path

import pytest
from PIL import Image, ImageFont
from pytest_mock import mocker
from textwrap import wrap

import quotespy
import quotespy.graphics.graphics as src
import quotespy.graphics.tools.errors as errors

from .data_samples import (default_settings_lyrics, default_settings_quote,
                           invalid_color_scheme_length,
                           invalid_color_scheme_value, invalid_font_family,
                           invalid_font_size, invalid_margin_bottom,
                           invalid_size_length, invalid_size_value,
                           invalid_text, invalid_title, invalid_wrap_limit,
                           missing_color_scheme, missing_font_family,
                           missing_font_size, missing_margin, missing_size,
                           missing_text, missing_title, missing_wrap_limit,
                           valid_custom_settings, valid_info, valid_info_list)


@pytest.mark.parametrize("format_chosen, return_settings", [
    ("lyrics", default_settings_lyrics),
    ("quote", default_settings_quote),
    ("", None)
])
def test_load_settings(mocker, format_chosen, return_settings):
    print(return_settings)
    spy = mocker.spy(src, "__load_default_settings")
    src.__load_default_settings(format_chosen)
    assert spy.spy_return == return_settings


@pytest.mark.parametrize("custom_settings, default_format, expected_result", [
    (valid_custom_settings, "", valid_custom_settings),
    ({}, "lyrics", default_settings_lyrics),
    ({}, "quote", default_settings_quote),
    (valid_custom_settings, "lyrics", valid_custom_settings),
    (valid_custom_settings, "quote", valid_custom_settings)
])
def test_choose_settings_valid(mocker, custom_settings, default_format, expected_result):
    spy = mocker.spy(src, "__choose_graphic_settings")
    src.__choose_graphic_settings(custom_settings, default_format)
    assert spy.spy_return == expected_result


@pytest.mark.parametrize("custom_settings, default_format, expected_error", [
    ({}, "", errors.MissingGraphicSettings),
    (missing_font_family, "", errors.MissingDictKeys),
    (missing_font_size, "", errors.MissingDictKeys),
    (missing_size, "", errors.MissingDictKeys),
    (missing_color_scheme, "", errors.MissingDictKeys),
    (missing_wrap_limit, "", errors.MissingDictKeys),
    (missing_margin, "", errors.MissingDictKeys),
    (invalid_font_family, "", errors.FontNotFound),
    (invalid_font_size, "", TypeError),
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
    (valid_info, valid_custom_settings, "lyrics", ""),
    (valid_info, valid_custom_settings, "quote", ""),
    (valid_info, valid_custom_settings, "", "C:\\Users\\user\\Desktop"),
    (valid_info, valid_custom_settings, "lyrics", "C:\\Users\\user\\Desktop"),
    (valid_info, valid_custom_settings, "quote", "C:\\Users\\user\\Desktop"),
    (valid_info, {}, "lyrics", ""),
    (valid_info, {}, "lyrics", "C:\\Users\\user\\Desktop"),
    (valid_info, {}, "quote", ""),
    (valid_info, {}, "quote", "C:\\Users\\user\\Desktop"),
])
def test_create_graphic(mocker, graphic_info, graphic_settings, default_format, save_dir):
    # Mock the `save` method
    mocker.patch("PIL.Image.Image.save")
    # Create a graphic
    src.create_graphic(
        graphic_info,
        graphic_settings,
        default_settings_format=default_format,
        save_dir=save_dir)
    # Assert the `save` method was called with the appropiate file name
    save_name = f"{graphic_info['title']}.png"
    save_name = path.join(save_dir, save_name)
    Image.Image.save.assert_called_once_with(save_name)


@pytest.mark.parametrize("graphic_info, graphic_settings, default_format, expected_error", [
    ({}, {}, "", errors.MissingDictKeys),
    (missing_title, {}, "", errors.MissingDictKeys),
    (missing_text, {}, "", errors.MissingDictKeys),
    (invalid_title, {}, "", errors.MissingGraphicInfoField),
    (invalid_text, {}, "", errors.MissingGraphicInfoField),
    (valid_info, missing_font_family, "", errors.MissingDictKeys),
    (valid_info, missing_font_size, "", errors.MissingDictKeys),
    (valid_info, missing_size, "", errors.MissingDictKeys),
    (valid_info, missing_color_scheme, "", errors.MissingDictKeys),
    (valid_info, missing_wrap_limit, "", errors.MissingDictKeys),
    (valid_info, missing_margin, "", errors.MissingDictKeys),
    (valid_info, invalid_font_family, "", errors.FontNotFound),
    (valid_info, invalid_font_size, "", TypeError),
    (valid_info, invalid_size_length, "", errors.InvalidFieldLength),
    (valid_info, invalid_size_value, "", TypeError),
    (valid_info, invalid_color_scheme_length, "", errors.InvalidFieldLength),
    (valid_info, invalid_color_scheme_value, "", errors.InvalidColorFormat),
    (valid_info, invalid_wrap_limit, "", TypeError),
    (valid_info, invalid_margin_bottom, "", TypeError)
])
def test_create_graphic_fails(mocker, graphic_info, graphic_settings, default_format, expected_error):
    # Mock the `save` method
    mocker.patch("PIL.Image.Image.save")
    with pytest.raises(expected_error):
        #  Create a graphic
        src.create_graphic(
            graphic_info,
            graphic_settings,
            default_settings_format=default_format
        )

@pytest.mark.parametrize("text, char_limit, margin, height_avail, font_family, font_size, return_expected", [
    ("You don't get anything playing the part when it's insincere", 20, 0, 2800, "Inkfree.ttf", 250, (833, [310, 310, 277, 237])),
    ("Who needs memories", 9, 50, 2800, "Inkfree.ttf", 450, (945, [484, 425])),
])
def test_y_is_centered(mocker, text, char_limit, margin, height_avail, font_family, font_size, return_expected):
    font = ImageFont.truetype(font_family, font_size, encoding="utf-8")
    text_wrapped = wrap(text, char_limit)
    returned_values = src.__get_y_and_heights(text_wrapped, height_avail, margin, font)
    assert return_expected == returned_values

@pytest.mark.parametrize("text, width, font_family, font_size, return_expected", [
    ("Who needs", 2800, "Inkfree.ttf", 450, 441),
    ("memories", 2800, "Inkfree.ttf", 450, 523),
    ("You don't get", 2800, "Inkfree.ttf", 250, 704),
    ("anything playing the", 2800, "Inkfree.ttf", 250, 318),
    ("part when it's", 2800, "Inkfree.ttf", 250, 641),
    ("insincere", 2800, "Inkfree.ttf", 250, 963)
])
def test_x_is_centered(mocker, text, width, font_family, font_size, return_expected):
    font = ImageFont.truetype(font_family, font_size, encoding="utf-8")
    returned_values = src.__get_x_centered(text, width, font)
    assert return_expected == returned_values
