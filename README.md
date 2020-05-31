# quotespy

## Python library to create quotes/lyrics graphics with PIL
---

## Usage

### Quotes/Lyrics Graphics

Create a graphic (.png) for lyrics, with default setings, saved in the current directory:
```
import quotespy.graphics.graphics as g
graphic_info = {
    "title": "strange_days", 
    "text": "Say goodbye to the silence, we can dance to the sirens"
}

g.create_graphic(graphic_info, {}, default_settings_format="lyrics")
```

I encourage you to also try out the "quote" `default_settings_format` option.

Alternatively, you can specify custom graphic settings and omit default settings options (note custom settings are chosen over default settings if both are specified).
```
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
    "margin_bottom": 312.5
}

save_dir = "some_path"

g.create_graphic(graphic_info, custom_settings, save_dir=save_dir)
```
Plus, in this second example, the path in which to save the created graphic is also specified. 

Please note all fields/keys specified for `graphic_info` and for `custom_settings` are always required.

If you have a .txt or .json file with multiple lyrics/quotes, you can also load and create individual graphics with a single function, just specify the path to the source file and the graphic settings (either custom or a default format).

```
import quotespy.graphics.graphics as g
g.gen_graphics("samples\\lyrics.txt", {}, default_settings_format="lyrics", save_dir="some_path")
```

For more information in the text formatting required from these .txt and .json source files, please refer to the [samples]() folder in this repository. It contains example files.

---

### Tweet Graphics

Tweet graphics work largely the same as lyrics/quotes graphics. The biggest difference is that it uses a different module, and the dictionaries require a couple of additional fields.

Starting with the most basic usage:
```
import quotespy.tweet_graphics.tweet_graphics as t
tweet_info = {
    "tweet_name": "mistakes",
    "user_name": "José Fernando Costa",
    "user_tag": "@soulsinporto",
    "user_pic": "samples\\user_photo2.png",
    "tweet_text": "Some mistakes and, dare I say, failures may lead to results you had never thought you could achieve."
}
t.create_tweet(tweet_info, {}, default_settings_format="blue", save_dir="some_path")
```
Just like the other module has its own default settings formats, for tweets there are three options, which differ mostly in the color scheme: "blue", "light" and "dark".

That "user_pic" key value in the `tweet_info` dictionary can either be a path to a .png file, or it can be left as an empty string. In other words, having a profile picture in the graphic is optional, but the dicitonary must always have the key. Also, note that the picture is pre-processed by reducing its dimensions to 10% of the graphic's dimensions and with a circular crop.

If you want to use custom graphic settings, you can use the following example for reference:
```
import quotespy.tweet_graphics.tweet_graphics as t
tweet_info = {
    "tweet_name": "mistakes",
    "user_name": "José Fernando Costa",
    "user_tag": "@soulsinporto",
    "user_pic": "samples\\user_photo2.png",
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
```
import quotespy.tweet_graphics.tweet_graphics as t
t.gen_tweets("samples\\tweets.json", {}, default_settings_format="dark")
```

Lastly, I'd like to you show some "advanced" usage of this `tweet_graphics` module (hopefully this serves as inspiration for the `graphics` module as well):
```
```


---

## TODO
* Update README with code examples
* Review package structure
* Finish package setup
