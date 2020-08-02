# quotespy

## Python library to create quotes/lyrics graphics with PIL

It can be installed through pip using `pip install quotespy`.

## Usage

### Quotes/Lyrics Graphics

Create a graphic (.png) for lyrics, with default setings, saved in the current directory:

```python
import quotespy.graphics.graphics as g
graphic_info = {
    "title": "strange_days", 
    "text": "Say goodbye to the silence, we can dance to the sirens"
}

g.create_graphic(graphic_info, {}, default_settings_format="lyrics")
```

I encourage you to also try out the "quote" `default_settings_format` option.

Alternatively, you can specify custom graphic settings and omit default settings options (note custom settings are chosen over default settings if both are specified).

```python
import quotespy.graphics.graphics as g
graphic_info = {
    "title": "strange_days", 
    "text": "Say goodbye to the silence, we can dance to the sirens"
}

custom_settings = {
    "font_family": "arial.ttf", 
    "font_size": 250, 
    "size": [2800, 2800], 
    "color_scheme": ["#000", "#fff"], 
    "wrap_limit": 20, 
    "margin_bottom": 0
}

save_dir = "some_path"

g.create_graphic(graphic_info, custom_settings, save_dir=save_dir)
```

Plus, in this second example, the path in which to save the created graphic is also specified. 

Please note all fields/keys shown for `graphic_info` and for `custom_settings` in the examples are always required.

If you have a .txt or .json file with multiple lyrics/quotes, you can also load it and create individual graphics with a single function, just specify the path to the source file and the graphic settings (either custom or a default format).

```python
import quotespy.graphics.graphics as g
g.gen_graphics("samples\\lyrics.txt", {}, default_settings_format="lyrics", save_dir="some_path")
```

For more information on the text formatting required from these .txt and .json source files, please refer to the [samples]() folder in this repository. It contains example files.

---

### Tweet Graphics

Tweet graphics works largely the same as the `graphics` counterpart. The biggest difference is that it uses a different module, and the dictionaries require a couple of additional fields.

Starting with the most basic usage:

```python
import quotespy.tweet_graphics.tweet_graphics as t
tweet_info = {
    "tweet_name": "mistakes",
    "user_name": "José Fernando Costa",
    "user_tag": "@soulsinporto",
    "user_pic": "user_photo2.png",
    "tweet_text": "Some mistakes and, dare I say, failures may lead to results you had never thought you could achieve."
}
t.create_tweet(tweet_info, {}, default_settings_format="blue", save_dir="some_path")
```
Just like the other module has its own default settings formats, for tweets there are three options, which differ mostly in the color scheme: "blue", "light" and "dark".

That "user_pic" key's value in the `tweet_info` dictionary can either be a path to a .png file, or it can be left as an empty string. In other words, having a profile picture in the graphic is optional, but the dicitonary must always have the key. Also, note that the picture is pre-processed by reducing its dimensions to 10% of the graphic's dimensions, with a circular crop.

If you want to use custom graphic settings, you can use the following example for reference:

```python
import quotespy.tweet_graphics.tweet_graphics as t
tweet_info = {
    "tweet_name": "mistakes",
    "user_name": "José Fernando Costa",
    "user_tag": "@soulsinporto",
    "user_pic": "user_photo2.png",
    "tweet_text": "Some mistakes and, dare I say, failures may lead to results you had never thought you could achieve."
}
graphic_settings = {
    "font_family": "arial.ttf",
    "font_size_text": 100,
    "font_size_header": 80,
    "size": [1800, 1800],
    "color_scheme": ["#000000", "#ffffff"],
    "wrap_limit": 32,
    "margin_bottom": 30
}
t.create_tweet(tweet_info, graphic_settings)
```

And, just like for the `create_graphics` module, you can also bulk generate tweet graphics, but this time only from .json source files:

```python
import quotespy.tweet_graphics.tweet_graphics as t
t.gen_tweets("samples\\tweets.json", {}, default_settings_format="dark")
```

---

### New in v1.2: transparent backgrounds

Starting in version 1.2, quotespy now accepts RGBA color strings to create transparent backgrounds. The red, green and blue channels are integers between 0 and 255, the alpha/transparency value is a float between 0 and 1.

```python
import quotespy.tweet_graphics.tweet_graphics as t
tweet_info = {
    "tweet_name": "mistakes",
    "user_name": "José Fernando Costa",
    "user_tag": "@soulsinporto",
    "user_pic": "user_photo2.png",
    "tweet_text": "Some mistakes and, dare I say, failures may lead to results you had never thought you could achieve."
}
graphic_settings = {
    "font_family": "arial.ttf",
    "font_size_text": 100,
    "font_size_header": 80,
    "size": [1800, 1800],
    "color_scheme": ["rgba(255, 255, 255, 0)", "#ffffff"],
    "wrap_limit": 32,
    "margin_bottom": 30
}
t.create_tweet(tweet_info, graphic_settings)
```

Alternatively, `None` can be passed as the background color to create a transparent background. These new color options are available for both `tweet_graphics` and `graphics`.

---

### Real Example Usage

Lastly, I'd like to you show some "advanced" usage of this `tweet_graphics` module (hopefully it serves as inspiration for the `graphics` module as well):

```python
import quotespy.tweet_graphics.tweet_graphics as t
import os
SAVEDIR = "imgs"

USERNAME = "José Fernando Costa"
USERTAG = "@soulsinporto"
# List of `tweet_info` dictionaries
tweets = [
    {
        "tweet_name": "compare_to_others_sometimes",
        "user_name": USERNAME,
        "user_tag": USERTAG,
        "user_pic": "",
        "tweet_text": "Compare yourself to others once in a while (using a reasonable scale!). If you completely isolate yourself you will end up working aimlessly without ever knowing when it is enough or how much you've improved."
    },
    {
        "tweet_name": "merit_in_positives",
        "user_name": USERNAME,
        "user_tag": USERTAG,
        "user_pic": "",
        "tweet_text": "There is merit in talking about the positive aspects of terrible situations. It helps those going through the experience to see a glimpse of light at the end of the tunnel and it may help others who go through the same experience in the future."
    },
    {
        "tweet_name": "write_down_ideas",
        "user_name": USERNAME,
        "user_tag": USERTAG,
        "user_pic": "",
        "tweet_text": "Write down ideas that pop up in your head in a reliable place (note-taking app, physical notebook, etc.). We often come up with the ideas or inspiration we are looking for when we least expect it, but it's easy to let them escape."
    }
]

# Get all the titles (tweet names) from the previous list
titles = [tweet["tweet_name"] for tweet in tweets]

# Directory in which to save graphics
PATH = "some_path"

# Create custom light and dark mode settings
s_light = {
    "font_family": "arial.ttf",
    "font_size_text": 80,
    "font_size_header": 70,
    "size": [1800, 1800],
    "color_scheme": ["#ffffff", "#000000"],
    "wrap_limit": 36,
    "margin_bottom": 30
}
s_dark = {
    "font_family": "arial.ttf",
    "font_size_text": 80,
    "font_size_header": 70,
    "size": [1800, 1800],
    "color_scheme": ["#000000", "#ffffff"],
    "wrap_limit": 36,
    "margin_bottom": 30
}

# Create a graphic for each `tweet_info` in the list
for tweet in tweets:
    tweet_name = tweet["tweet_name"]
    # Each tweet is stored in its own folder
    tweet_path = os.path.join(PATH, tweet_name)
    os.system(f"mkdir {PATH}\\{tweet_name}")

    # And each folder has light and dark mode versions of the tweet
    t.create_tweet(tweet, s_light, save_dir=tweet_path)
    tweet["tweet_name"] = tweet_name + "_DM"
    t.create_tweet(tweet, s_dark, save_dir=tweet_path)
```
