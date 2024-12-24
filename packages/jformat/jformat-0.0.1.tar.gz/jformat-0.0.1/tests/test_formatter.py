# File: tests/test_formatter.py
import pytest
from jformat.cli import format_json

def test_format_json():
    input_json = '{"b":2,"a":1}'
    expected_sorted = '{\n    "a": 1,\n    "b": 2\n}'
    expected_unsorted = '{\n    "b": 2,\n    "a": 1\n}'
    
    assert format_json(input_json, sort_keys=True) == expected_sorted
    assert format_json(input_json, sort_keys=False) == expected_unsorted