default_settings_lyrics = {
    "font_family": "arial.ttf",
    "font_size": 250,
    "size": [2800, 2800],
    "color_scheme": ["#000000", "#ffffff"],
    "wrap_limit": 20,
    "margin_bottom": 0
}
default_settings_lyrics_returned = {
    "font_family": "arial.ttf",
    "font_size": 250,
    "size": [2800, 2800],
    "color_scheme": [(0, 0, 0), (255, 255, 255)],
    "wrap_limit": 20,
    "margin_bottom": 0
}

default_settings_quote = {
    "font_family": "arial.ttf",
    "font_size": 200,
    "size": [3840, 2160],
    "color_scheme": ["#000000", "#ffffff"],
    "wrap_limit": 32,
    "margin_bottom": 0
}
default_settings_quote_returned = {
    "font_family": "arial.ttf",
    "font_size": 200,
    "size": [3840, 2160],
    "color_scheme": [(0, 0, 0), (255, 255, 255)],
    "wrap_limit": 32,
    "margin_bottom": 0
}

valid_custom_settings = {
    "font_family": "arial.ttf",
    "font_size": 250,
    "size": [2800, 2800],
    "color_scheme": ["#000", "#fff"],
    "wrap_limit": 20,
    "margin_bottom": 15
}
valid_custom_settings_returned = {
    "font_family": "arial.ttf",
    "font_size": 250,
    "size": [2800, 2800],
    "color_scheme": [(0, 0, 0), (255, 255, 255)],
    "wrap_limit": 20,
    "margin_bottom": 15
}
valid_custom_settings_rgba = {
    "font_family": "arial.ttf",
    "font_size": 100,
    "size": [1800, 1800],
    "color_scheme": ["rgba(0, 0, 0, 0)", "#ffffff"],
    "wrap_limit": 32,
    "margin_bottom": 30
}
valid_custom_settings_rgba_returned = {
    "font_family": "arial.ttf",
    "font_size": 100,
    "size": [1800, 1800],
    "color_scheme": ["rgba(0, 0, 0, 0)", (255, 255, 255)],
    "wrap_limit": 32,
    "margin_bottom": 30
}
valid_custom_settings_none_bg = {
    "font_family": "arial.ttf",
    "font_size": 100,
    "size": [1800, 1800],
    "color_scheme": [None, "#ffffff"],
    "wrap_limit": 32,
    "margin_bottom": 30
}
valid_custom_settings_none_bg_returned = {
    "font_family": "arial.ttf",
    "font_size": 100,
    "size": [1800, 1800],
    "color_scheme": [None, (255, 255, 255)],
    "wrap_limit": 32,
    "margin_bottom": 30
}

missing_font_family = {
    "font_size": 250,
    "size": [2800, 2800],
    "color_scheme": ["#000", "#fff"],
    "wrap_limit": 20,
    "margin_bottom": 312.5
}
missing_font_size = {
    "font_family": "Inkfree.ttf",
    "size": [2800, 2800],
    "color_scheme": ["#000", "#fff"],
    "wrap_limit": 20,
    "margin_bottom": 312.5
}
missing_size = {
    "font_family": "Inkfree.ttf",
    "font_size": 250,
    "color_scheme": ["#000", "#fff"],
    "wrap_limit": 20,
    "margin_bottom": 312.5
}
missing_color_scheme = {
    "font_family": "Inkfree.ttf",
    "font_size": 250,
    "size": [2800, 2800],
    "wrap_limit": 20,
    "margin_bottom": 312.5
}
missing_wrap_limit = {
    "font_family": "Inkfree.ttf",
    "font_size": 250,
    "size": [2800, 2800],
    "color_scheme": ["#000", "#fff"],
    "margin_bottom": 312.5
}
missing_margin = {
    "font_family": "Inkfree.ttf",
    "font_size": 250,
    "size": [2800, 2800],
    "color_scheme": ["#000", "#fff"],
    "wrap_limit": 20,
}

invalid_font_family = {
    "font_family": "test",
    "font_size": 250,
    "size": [2800, 2800],
    "color_scheme": ["#000", "#fff"],
    "wrap_limit": 20,
    "margin_bottom": 312.5
}
invalid_font_size = {
    "font_family": "Inkfree.ttf",
    "font_size": "test",
    "size": [2800, 2800],
    "color_scheme": ["#000", "#fff"],
    "wrap_limit": 20,
    "margin_bottom": 312.5
}
invalid_size_length = {
    "font_family": "Inkfree.ttf",
    "font_size": 250,
    "size": [2800, 2800, "test"],
    "color_scheme": ["#000", "#fff"],
    "wrap_limit": 20,
    "margin_bottom": 312.5
}
invalid_size_value = {
    "font_family": "Inkfree.ttf",
    "font_size": 250,
    "size": [2800, "test"],
    "color_scheme": ["#000", "#fff"],
    "wrap_limit": 20,
    "margin_bottom": 312.5
}
invalid_color_scheme_length = {
    "font_family": "Inkfree.ttf",
    "font_size": 250,
    "size": [2800, 2800],
    "color_scheme": ["#000", "#fff", "test"],
    "wrap_limit": 20,
    "margin_bottom": 312.5
}
invalid_color_scheme_value = {
    "font_family": "Inkfree.ttf",
    "font_size": 250,
    "size": [2800, 2800],
    "color_scheme": ["test", "#fff"],
    "wrap_limit": 20,
    "margin_bottom": 312.5
}
invalid_color_scheme_rgba = {
    "font_family": "arial.ttf",
    "font_size_text": 100,
    "font_size_header": 80,
    "size": [1800, 1800],
    "color_scheme": ["#15202b", "rgba(0, 0, 255, -1)"],
    "wrap_limit": 32,
    "margin_bottom": 30
}
invalid_wrap_limit = {
    "font_family": "arial.ttf",
    "font_size": 250,
    "size": [2800, 2800],
    "color_scheme": ["#000", "#fff"],
    "wrap_limit": "test",
    "margin_bottom": 312.5
}
invalid_margin_bottom = {
    "font_family": "arial.ttf",
    "font_size": 250,
    "size": [2800, 2800],
    "color_scheme": ["#000", "#fff"],
    "wrap_limit": 20,
    "margin_bottom": "test"
}

valid_info = {
    "title": "info1",
    "text": "test test test test test"
}
missing_title = {
    "text": "test test test test test"
}
invalid_title = {
    "title": 123,
    "text": "test test test test test"
}
missing_text = {
    "title": "info1",
}
invalid_text = {
    "title": "info1",
    "text": 123
}

valid_info_list = [
    {
        "title": "info1",
        "text": "test test test test test"
    },
    {
        "title": "info2",
        "text": "test test test test test"
    },
    {
        "title": "info3",
        "text": "test test test test test"
    },
]