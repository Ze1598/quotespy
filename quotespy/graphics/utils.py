from PIL import Image, ImageDraw, ImageFont
from random import choice
from textwrap import wrap
from typing import Tuple, List, Dict, Union
import json


def load_quotes_txt(
    file_name: str
) -> List[List[str]]:
    """
    Scrape quotes from a given TXT file. Titles need to be wrapped
    by square brackets ([]) lyrics are separated from the next one by
    a blank line.
    Example:
    [song1]
    lyric

    [song2]
    lyric
    """
    # Titles of songs
    titles = []
    # Each item corresponds to the quotes of a single image
    quotes = []

    # Used to extract the lyrics
    temp_string = ""
    # Loop through the quotes file
    for i, line in enumerate(open(file_name, "r")):

        # The first line is a special case
        if i == 0:
            title = line[4:-2]
            titles.append(title)

        # Any line that isn't the first line
        else:
            # If the line starts with an opening bracket, it's a title line
            if line[0] == "[":
                titles.append(line[1:-2])

            # If the line is a newline and the temporary string has content, then\
            # we finished scraping a quote
            elif line == "\n" and temp_string != "":
                quotes.append(temp_string[:-1])
                temp_string = ""

            # Else, just add the current line (a line of text) to the temporary string
            else:
                temp_string += line

    # If `temp_string` still has some text saved (that is, since the file didn't end\
    # with an empty line, it wasn't possible to append the last quote to the list\
    # inside the loop), then append whatever that string is to the list of lyrics
    if len(temp_string) > 0 and temp_string != "\n":
        quotes.append(temp_string)

    # Pair the titles with the respective quotes in two-item lists
    titles_quotes = list(zip(titles, quotes))

    return titles_quotes


def load_text_json(
    file_path: str
) -> List[List[str]]:
    """
    Load quotes from a JSON file, i.e., load a JSON object that maps
    titles to quotes.
    """
    with open(file_path, "r") as json_file:
        json_songs = json.load(json_file)
    return json_songs


def parse_json_settings(
    file_path: str
) -> Dict[str, Union[str, int, float, List[str]]]:
    """
    Load a JSON object of settings for the image to be drawn as a Python dictionary.
    """
    with open(file_path, "r") as json_file:
        json_settings = json.load(json_file)
    return json_settings


def update_title_counts(
    quotes: List[Tuple[str, str]]
) -> List[Tuple[str, str]]:
    """
    Given a list of tuples of the type (title, quotes), update the title with its frequency
    in a new dictionary.
    """
    # Freqs of each unique quote
    title_freqs = {}
    # Dictionary with the updated titles mapped to the corresponding quotes
    updated_quotes = {}

    # Loop through the loaded quotes to update titles with their frequencies
    for quote in quotes:
        title = quote[0]
        lyrics = quote[1]

        # If this quote title has been seen before, update the title with its current frequency
        if title in title_freqs:
            # Update the title frequency
            title_freqs[title] += 1

            # Update the title with its current frequency
            updated_title = title + f" {str(title_freqs[title])}"

            # Add the updated quote information to the dictionary
            updated_quotes[updated_title] = lyrics

        # If this is the first time seeing the quote, simply use it as is
        else:
            title_freqs[title] = 1
            updated_quotes[title] = lyrics

    return updated_quotes


def get_ready_text(
    file_name: str
) -> List[Tuple[str, str]]:
    """
    Load quotes/lyrics from a source file, TXT or JSON, and update the corresponding
    quotes/lyrics' titles with their frequency.
    """
    # Get the file extension and load the quotes accordingly (from a TXT or JSON)
    file_ext = file_name.split(".")[-1]

    if file_ext == "txt":
        titles_quotes = load_quotes_txt(file_name)
        # And update the titles with their frequencies
        titles_quotes_updated = update_title_counts(titles_quotes)
        return titles_quotes_updated

    elif file_ext == "json":
        # Since json can't have duplicate object keys, it is assumed the keys\
        # (titles) already include the frequency
        titles_quotes = load_text_json(file_name)
        return titles_quotes


if __name__ == "__main__":
    """
    # Title of the lyrics text files
    lyrics_file = "lyrics.txt"
    # Scrape the titles and lyrics for each graphic
    titles, lyrics = load_lyrics(lyrics_file)

    # Now get the frequencies for each song title
    title_freqs = count_song_freqs(titles)
    """
