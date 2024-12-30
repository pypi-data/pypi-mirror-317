"""
data_formatting_help

A Python package for data formatting utilities, including JSON, CSV, and string manipulation,
as well as date and time formatting.

Modules:
    - formatter: Core functionality for data formatting.

Version:
    0.1.0
"""

__version__ = '1.0.2'

from .formatter import (
    format_json,
    validate_json,
    format_csv,
    parse_csv,
    normalise_string,
    split_and_capitalise,
    format_date,
    parse_date,
    convert_timestamp,
    reformat_data_structure,
    flatten_nested_dict,
)

__all__ = [
    "format_json",
    "validate_json",
    "format_csv",
    "parse_csv",
    "normalise_string",
    "split_and_capitalise",
    "format_date",
    "parse_date",
    "convert_timestamp",
    "reformat_data_structure",
    "flatten_nested_dict",
]