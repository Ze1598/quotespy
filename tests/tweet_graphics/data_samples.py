blue_mode_settings = {
    "font_family": "arial.ttf",
    "font_size_text": 100,
    "font_size_header": 80,
    "size": [1800, 1800],
    "color_scheme": ["#15202b", "#ffffff"],
    "wrap_limit": 32,
    "margin_bottom": 30
}
blue_mode_settings_returned = {
    "font_family": "arial.ttf",
    "font_size_text": 100,
    "font_size_header": 80,
    "size": [1800, 1800],
    "color_scheme": [(21, 32, 43), (255, 255, 255)],
    "wrap_limit": 32,
    "margin_bottom": 30
}

dark_mode_settings = {
    "font_family": "arial.ttf",
    "font_size_text": 100,
    "font_size_header": 80,
    "size": [1800, 1800],
    "color_scheme": ["#000000", "#ffffff"],
    "wrap_limit": 32,
    "margin_bottom": 30
}
dark_mode_settings_returned = {
    "font_family": "arial.ttf",
    "font_size_text": 100,
    "font_size_header": 80,
    "size": [1800, 1800],
    "color_scheme": [(0, 0, 0), (255, 255, 255)],
    "wrap_limit": 32,
    "margin_bottom": 30
}

light_mode_settings = {
    "font_family": "arial.ttf",
    "font_size_text": 100,
    "font_size_header": 80,
    "size": [1800, 1800],
    "color_scheme": ["#ffffff", "#000000"],
    "wrap_limit": 32,
    "margin_bottom": 30
}
light_mode_settings_returned = {
    "font_family": "arial.ttf",
    "font_size_text": 100,
    "font_size_header": 80,
    "size": [1800, 1800],
    "color_scheme": [(255, 255, 255), (0, 0, 0)],
    "wrap_limit": 32,
    "margin_bottom": 30
}


valid_custom_settings = {
    "font_family": "arial.ttf",
    "font_size_text": 100,
    "font_size_header": 80,
    "size": [1800, 1800],
    "color_scheme": ["#15202b", "#ffffff"],
    "wrap_limit": 32,
    "margin_bottom": 30
}
valid_custom_settings_returned = {
    "font_family": "arial.ttf",
    "font_size_text": 100,
    "font_size_header": 80,
    "size": [1800, 1800],
    "color_scheme": [(21, 32, 43), (255, 255, 255)],
    "wrap_limit": 32,
    "margin_bottom": 30
}
valid_custom_settings_rgba = {
    "font_family": "arial.ttf",
    "font_size_text": 100,
    "font_size_header": 80,
    "size": [1800, 1800],
    "color_scheme": ["rgba(0, 0, 0, 0)", "#ffffff"],
    "wrap_limit": 32,
    "margin_bottom": 30
}
valid_custom_settings_rgba_returned = {
    "font_family": "arial.ttf",
    "font_size_text": 100,
    "font_size_header": 80,
    "size": [1800, 1800],
    "color_scheme": ["rgba(0, 0, 0, 0)", (255, 255, 255)],
    "wrap_limit": 32,
    "margin_bottom": 30
}
valid_custom_settings_none_bg = {
    "font_family": "arial.ttf",
    "font_size_text": 100,
    "font_size_header": 80,
    "size": [1800, 1800],
    "color_scheme": [None, "#ffffff"],
    "wrap_limit": 32,
    "margin_bottom": 30
}
valid_custom_settings_none_bg_returned = {
    "font_family": "arial.ttf",
    "font_size_text": 100,
    "font_size_header": 80,
    "size": [1800, 1800],
    "color_scheme": [None, (255, 255, 255)],
    "wrap_limit": 32,
    "margin_bottom": 30
}

missing_font_family = {
    "font_size_text": 100,
    "font_size_header": 80,
    "size": [1800, 1800],
    "color_scheme": ["#15202b", "#ffffff"],
    "wrap_limit": 32,
    "margin_bottom": 30
}
missing_font_size_header = {
    "font_family": "arial.ttf",
    "font_size_text": 100,
    "size": [1800, 1800],
    "color_scheme": ["#15202b", "#ffffff"],
    "wrap_limit": 32,
    "margin_bottom": 30
}
missing_font_size_text = {
    "font_family": "arial.ttf",
    "font_size_header": 80,
    "size": [1800, 1800],
    "color_scheme": ["#15202b", "#ffffff"],
    "wrap_limit": 32,
    "margin_bottom": 30
}
missing_size = {
    "font_family": "arial.ttf",
    "font_size_text": 100,
    "font_size_header": 80,
    "color_scheme": ["#15202b", "#ffffff"],
    "wrap_limit": 32,
    "margin_bottom": 30
}
missing_color_scheme = {
    "font_family": "arial.ttf",
    "font_size_text": 100,
    "font_size_header": 80,
    "size": [1800, 1800],
    "wrap_limit": 32,
    "margin_bottom": 30
}
missing_wrap_limit = {
    "font_family": "arial.ttf",
    "font_size_text": 100,
    "font_size_header": 80,
    "size": [1800, 1800],
    "color_scheme": ["#15202b", "#ffffff"],
    "margin_bottom": 30
}
missing_margin = {
    "font_family": "arial.ttf",
    "font_size_text": 100,
    "font_size_header": 80,
    "size": [1800, 1800],
    "color_scheme": ["#15202b", "#ffffff"],
    "wrap_limit": 32,
}

invalid_font_family = {
    "font_family": "test",
    "font_size_text": 100,
    "font_size_header": 80,
    "size": [1800, 1800],
    "color_scheme": ["#15202b", "#ffffff"],
    "wrap_limit": 32,
    "margin_bottom": 30
}
invalid_font_size_header = {
    "font_family": "arial.ttf",
    "font_size_text": 100,
    "font_size_header": "test",
    "size": [1800, 1800],
    "color_scheme": ["#15202b", "#ffffff"],
    "wrap_limit": 32,
    "margin_bottom": 30
}
invalid_font_size_text = {
    "font_family": "arial.ttf",
    "font_size_text": "test",
    "font_size_header": 80,
    "size": [1800, 1800],
    "color_scheme": ["#15202b", "#ffffff"],
    "wrap_limit": 32,
    "margin_bottom": 30
}
invalid_size_length = {
    "font_family": "arial.ttf",
    "font_size_text": 100,
    "font_size_header": 80,
    "size": [1800, 1800, "test"],
    "color_scheme": ["#15202b", "#ffffff"],
    "wrap_limit": 32,
    "margin_bottom": 30
}
invalid_size_value = {
    "font_family": "arial.ttf",
    "font_size_text": 100,
    "font_size_header": 80,
    "size": [1800, "test"],
    "color_scheme": ["#15202b", "#ffffff"],
    "wrap_limit": 32,
    "margin_bottom": 30
}
invalid_color_scheme_length = {
    "font_family": "arial.ttf",
    "font_size_text": 100,
    "font_size_header": 80,
    "size": [1800, 1800],
    "color_scheme": ["#15202b", "#ffffff", "test"],
    "wrap_limit": 32,
    "margin_bottom": 30
}
invalid_color_scheme_value = {
    "font_family": "arial.ttf",
    "font_size_text": 100,
    "font_size_header": 80,
    "size": [1800, 1800],
    "color_scheme": ["#15202b", "test"],
    "wrap_limit": 32,
    "margin_bottom": 30
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
    "font_size_text": 100,
    "font_size_header": 80,
    "size": [1800, 1800],
    "color_scheme": ["#15202b", "#ffffff"],
    "wrap_limit": "test",
    "margin_bottom": 30
}
invalid_margin_bottom = {
    "font_family": "arial.ttf",
    "font_size_text": 100,
    "font_size_header": 80,
    "size": [1800, 1800],
    "color_scheme": ["#15202b", "#ffffff"],
    "wrap_limit": 32,
    "margin_bottom": "test"
}


valid_info = {
    "tweet_name": "test_name",
    "user_name": "test_username",
    "user_tag": "@testusertag",
    "user_pic": "",
    "tweet_text": "test test test"
}
missing_name = {
    "user_name": "test_username",
    "user_tag": "@testusertag",
    "user_pic": "",
    "tweet_text": "test test test"
}
missing_username = {
    "tweet_name": "test_name",
    "user_tag": "@testusertag",
    "user_pic": "",
    "tweet_text": "test test test"
}
missing_tag = {
    "tweet_name": "test_name",
    "user_name": "test_username",
    "user_pic": "",
    "tweet_text": "test test test"
}
missing_pic = {
    "tweet_name": "test_name",
    "user_name": "test_username",
    "user_tag": "@testusertag",
    "tweet_text": "test test test"
}
missing_text = {
    "tweet_name": "test_name",
    "user_name": "test_username",
    "user_tag": "@testusertag",
    "user_pic": "",
}
invalid_name = {
    "tweet_name": "",
    "user_name": "test_username",
    "user_tag": "@testusertag",
    "user_pic": "",
    "tweet_text": "test test test"
}
invalid_username = {
    "tweet_name": "test_name",
    "user_name": "test_usernametest_usernametest_usernametest_usernametest_username",
    "user_tag": "@testusertag",
    "user_pic": "",
    "tweet_text": "test test test"
}
invalid_tag = {
    "tweet_name": "test_name",
    "user_name": "test_username",
    "user_tag": "@testusertagtestusertagtestusertag",
    "user_pic": "",
    "tweet_text": "test test test"
}
invalid_user_pic = {
    "tweet_name": "test_name",
    "user_name": "test_username",
    "user_tag": "@testusertag",
    "user_pic": "",
    "tweet_text": "test test test"
}
invalid_text = {
    "tweet_name": "test_name",
    "user_name": "test_username",
    "user_tag": "@testusertag",
    "user_pic": "",
    "tweet_text": "test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test testvv test test test test test test test test test test test test"
}


valid_info_list = [
    {
        "tweet_name": "test_name1",
        "user_name": "test_username",
        "user_tag": "@testusertag",
        "user_pic": "",
        "tweet_text": "test test test"
    },
    {
        "tweet_name": "test_name2",
        "user_name": "test_username",
        "user_tag": "@testusertag",
        "user_pic": "",
        "tweet_text": "test test test"
    },
    {
        "tweet_name": "test_name3",
        "user_name": "test_username",
        "user_tag": "@testusertag",
        "user_pic": "",
        "tweet_text": "test test test"
    },
]
