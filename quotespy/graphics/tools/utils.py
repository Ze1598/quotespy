from PIL import Image, ImageDraw, ImageFont
from random import choice
from textwrap import wrap
from typing import Tuple, List, Dict, Union
import json
import re

def __load_quotes_txt(
    file_name: str
) -> List[List[str]]:
    """
    Scrape quotes from a given TXT file. Titles need to be wrapped
    by square brackets ([]) and the respective quote needs to come in
    the next line.
    Example:
    [title1]
    quote

    [title2]
    quote
    """
    # Load the source file contents as a single string
    with open(file_name, "r", encoding="utf-8") as source_file:
        contents = "".join(source_file.readlines())

    # Get all the titles
    pattern_titles = r'\[(.*?)\]'
    titles = re.findall(pattern_titles, contents)
    # Get all the quotes
    pattern_quotes = r'^([^\[].*?[^\]])$'
    quotes = re.findall(pattern_quotes, contents, flags=re.MULTILINE)

    # Pair the titles with the respective quotes in two-item lists
    titles_quotes = list(zip(titles, quotes))

    return titles_quotes


def __load_text_json(
    file_path: str
) -> List[List[str]]:
    """
    Load quotes from a JSON file, i.e., load a JSON object that maps
    titles to quotes.
    """
    with open(file_path, "r", encoding="utf-8") as json_file:
        json_quotes = json.load(json_file)
    return json_quotes


def parse_json_settings(
    file_path: str
) -> Dict[str, Union[str, int, float, List[str]]]:
    """
    Load a JSON object of settings for the image to be drawn as a Python dictionary.
    """
    with open(file_path, "r", encoding="utf-8") as json_file:
        json_settings = json.load(json_file)
    return json_settings


def __update_title_counts(
    quotes: List[List[str]]
) -> Dict[str, str]:
    """
    Given a list of lists of the type [title, quote], update the title with its frequency
    in a new dictionary.
    """
    # Freqs of each unique quote
    title_freqs = {}
    # Dictionary with the updated titles mapped to the corresponding quotes
    updated_quotes = {}

    # Loop through the loaded quotes to update titles with their frequencies
    for quote in quotes:
        title = quote[0]
        text = quote[1]

        # If this quote title has been seen before, update the title with its current frequency
        if title in title_freqs:
            # Update the title frequency
            title_freqs[title] += 1

            # Update the title with its current frequency
            updated_title = f"{title} {str(title_freqs[title])}"

            # Add the updated quote information to the dictionary
            updated_quotes[updated_title] = text

        # If this is the first time seeing the quote, simply use it as is
        else:
            title_freqs[title] = 1
            updated_quotes[title] = text

    return updated_quotes


# TODO: validate
def get_ready_text(
    file_name: str
) -> List[Tuple[str, str]]:
    """
    Load quotes/lyrics from a source file, TXT or JSON, and update the corresponding
    quotes/lyrics' titles with their frequency.
    """
    # Get the file extension and load the quotes accordingly (from a TXT or JSON)
    file_ext = file_name.split(".")[-1]

    # TXT need to be loaded and have their titles updated (so there's no duplicate
    # titles)
    if file_ext == "txt":
        titles_quotes = __load_quotes_txt(file_name)
        # And update the titles with their frequencies
        titles_quotes_updated = __update_title_counts(titles_quotes)
        return titles_quotes_updated

    # Since JSON objects can't have duplicate keys, it is assumed the the titles\
    # are already unique in some way
    elif file_ext == "json":
        titles_quotes = __load_text_json(file_name)
        return titles_quotes

