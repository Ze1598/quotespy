import json
import re
from random import choice
from textwrap import wrap
from typing import Dict, List, Tuple, Union
from PIL import Image, ImageDraw, ImageFont
from .type_interfaces import GraphicInfo, GraphicSettings
from .validation import __validate_text_loaded


def __load_quotes_txt(
    file_path: str
) -> List[Tuple[str]]:
    """Scrape quotes from a given TXT file. Titles need to be wrapped
    by square brackets ([]) and the respective quote needs to come in
    the next line.

    Parameters
    ----------
    file_path : str
        Path to the .txt file with lyrics/quotes.

    Returns
    -------
    List[Tuple[str]]
        List of tuples that contain the title and text of each quote loaded.
    """
    # Load the source file contents as a single string
    with open(file_path, "r", encoding="utf-8") as source_file:
        contents = "".join(source_file.readlines())

    # Get all the titles
    pattern_titles = r'\[(.*?)\]'
    titles = re.findall(pattern_titles, contents)
    # Get all the quotes
    pattern_quotes = r'^([^\[].*?[^\]])$'
    quotes = re.findall(pattern_quotes, contents, flags=re.MULTILINE)

    # Validate the loaded titles and quotes
    __validate_text_loaded(titles, quotes)

    # Pair the titles with the respective quotes in two-item lists
    titles_quotes = list(zip(titles, quotes))

    return titles_quotes


def __load_text_json(
    file_path: str
) -> Dict[str, str]:
    """Load quotes from a JSON file, i.e., load a JSON objects that maps titles to quotes/lyrics.

    Parameters
    ----------
    file_path : str
        Path to the .json file with lyrics/quotes.

    Returns
    -------
    Dict[str, str]
        Dictionary that maps titles to the respective quote/lyrics.
    """
    with open(file_path, "r", encoding="utf-8") as json_file:
        json_quotes = json.load(json_file)
    return json_quotes


def parse_json_settings(
    file_path: str
) -> GraphicSettings:
    """Load a the `graphic_settings` from a JSON file.

    Parameters
    ----------
    file_path : str
        Path to the .json file with lyrics/quotes.

    Returns
    -------
    GraphicSettings
        A dictionary of settings for a graphic.
    """
    with open(file_path, "r", encoding="utf-8") as json_file:
        json_settings = json.load(json_file)
    return json_settings


def __update_title_counts(
    quotes: List[Tuple[str]]
) -> Dict[str, str]:
    """Given a list of lists of titles and quotes loaded from a .txt file, update the titles with the respective frequencies.

    Parameters
    ----------
    quotes : List[Tuple[str]]
        List of tuples that contain the title and quote of each graphic.

    Returns
    -------
    Dict[str, str]
        Dictionary that maps titles to the corresponding lyrics/quote.
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


def get_ready_text(
    file_path: str
) -> Dict[str, str]:
    """Load quotes/lyrics from a source file, .txt or .json, and update the corresponding
    quotes/lyrics' titles with their frequency (in the case of the former option).

    Parameters
    ----------
    file_path : str
        Path to the .txt or .json file.

    Returns
    -------
    Dict[str, str]
        A mapping of the loaded titles to the respective quote/lyrics.
    """
    # Get the file extension and load the quotes accordingly (from a TXT or JSON)
    file_ext = file_path.split(".")[-1]

    # TXT need to be loaded and have their titles updated (so there's no duplicate
    # titles)
    if file_ext == "txt":
        titles_quotes = __load_quotes_txt(file_path)
        # And update the titles with their frequencies
        titles_quotes_ready = __update_title_counts(titles_quotes)

    # Since JSON objects can't have duplicate keys, it is assumed the the titles\
    # are already unique in some way
    elif file_ext == "json":
        titles_quotes_ready = __load_text_json(file_path)

    return titles_quotes_ready
