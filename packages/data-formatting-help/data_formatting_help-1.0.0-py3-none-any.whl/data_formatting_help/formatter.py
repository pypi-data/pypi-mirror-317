import json
import csv
import re
from datetime import datetime, date
import time
from collections.abc import MutableMapping
from typing import Any, Dict

import pandas as pd
from dateutil import parser

def format_json(data: dict, indent: int = 2) -> str:
    """
    Format a dictionary as a JSON string.

    Args:
        data (dict): The dictionary to format.
        indent (int): The number of spaces to indent the JSON string.

    Returns:
        str: The formatted JSON string.
    """
    return json.dumps(data, indent=indent)

def validate_json(data: str) -> bool:
    """
    Validate a JSON string.

    Args:
        data (str): The JSON string to validate.

    Returns:
        bool: True if the JSON string is valid, False otherwise.
    """
    try:
        json.loads(data)
        return True
    except json.JSONDecodeError:
        return False
    
def format_csv(data: list, delimiter=',') -> str:
    """
    Format a list of dictionaries as a CSV string.

    Args:
        data (list): The list of dictionaries to format.
        delimiter (str): The delimiter to use in the CSV string.

    Returns:
        str: The formatted CSV string.
    """
    if not data:
        return ""
    keys = data[0].keys()
    output = [delimiter.join(keys)]
    for row in data:
        output.append(delimiter.join(str(row[key]) for key in keys))
    return "\n".join(output)

def parse_csv(data: str, delimiter=',') -> list:
    """
    Parse a CSV string into a list of dictionaries.

    Args:
        data (str): The CSV string to parse.
        delimiter (str): The delimiter used in the CSV string.

    Returns:
        list: The list of dictionaries.
    """
    reader = csv.DictReader(data.splitlines(), delimiter=delimiter)
    return list(reader)

def normalise_string(data: str) -> str:
    """
    Normalise a string by removing leading and trailing whitespace and converting it to lowercase.

    Args:
        data (str): The string to normalise.

    Returns:
        str: The normalised string.
    """
    return data.strip().lower()

def split_and_capitalise(data: str, delimiter='_') -> str:
    """
    Split a string by a delimiter and capitalise each word.

    Args:
        data (str): The string to split and capitalise.
        delimiter (str): The delimiter to split the string by.

    Returns:
        str: The split and capitalised string.
    """
    return delimiter.join(word.capitalize() for word in data.split(delimiter))

def format_date(date: date, format="%Y-%m-%d") -> str:
    """
    Format a date as a string.

    Args:
        date (date): The date to format.
        format (str): The format string.

    Returns:
        str: The formatted date string.
    """
    return date.strftime(format)

def parse_date(date: str, format="%Y-%m-%d") -> date:
    """
    Parse a date string into a date object.

    Args:
        date (str): The date string to parse.
        format (str): The format string.

    Returns:
        date: The date object.
    """
    return datetime.strptime(date, format).date()

def convert_timestamp(timestamp: float, format="%Y-%m-%d %H:%M:%S") -> str:
    """
    Convert a timestamp to a formatted string.

    Args:
        timestamp (int | float): The timestamp to convert.
        format (str): The format string.

    Returns:
        str: The formatted timestamp string.
    """
    return datetime.fromtimestamp(timestamp).strftime(format)

def reformat_data_structure(data: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Reformats a given data structure to match the provided schema.

    Args:
        data (Dict[str, Any]): The input data to be reformatted. Must be a dictionary.
        schema (Dict[str, Any]): The schema describing the desired structure of the data.
            The schema defines the expected keys and their corresponding types.

    Returns:
        Dict[str, Any]: The reformatted data matching the schema.

    Raises:
        ValueError: If the data cannot be reformatted to match the schema.
    """
    reformatted = {}

    for key, value_type in schema.items():
        if key not in data:
            # Handle missing keys: assign None or a default value based on type
            if isinstance(value_type, dict):  # Nested structure
                reformatted[key] = reformat_data_structure({}, value_type)
            else:
                reformatted[key] = None
        else:
            # Process nested dictionaries
            if isinstance(value_type, dict):
                if isinstance(data[key], dict):
                    reformatted[key] = reformat_data_structure(data[key], value_type)
                else:
                    raise ValueError(f"Expected a nested dictionary for key '{key}'.")
            else:
                # Convert the value to the expected type if possible
                try:
                    reformatted[key] = value_type(data[key])
                except (TypeError, ValueError):
                    raise ValueError(
                        f"Key '{key}' cannot be converted to {value_type.__name__}."
                    )

    return reformatted

def flatten_nested_dict(nested_dict: Dict[str, Any], separator: str = ".") -> Dict[str, Any]:
    """
    Flattens a nested dictionary into a single-level dictionary, with keys joined by a separator.

    Args:
        nested_dict (Dict[str, Any]): The nested dictionary to flatten.
        separator (str): The string used to join keys in the flattened dictionary (default is ".").

    Returns:
        Dict[str, Any]: A single-level dictionary with flattened keys.
    """
    def _flatten(current_dict: Dict[str, Any], parent_key: str = "") -> Dict[str, Any]:
        flattened = {}
        for key, value in current_dict.items():
            full_key = f"{parent_key}{separator}{key}" if parent_key else key
            if isinstance(value, dict):
                # Recursively flatten nested dictionaries
                flattened.update(_flatten(value, full_key))
            else:
                # Add the value to the flattened dictionary
                flattened[full_key] = value
        return flattened

    return _flatten(nested_dict)