import pytest
from typing import Union, Literal
from pydantic import BaseModel
from pulsar.parser import parse


#  Test Helper Functions
def case_parse(data: str, model_type: type, expected_json: dict = None, should_fail: bool = False, allow_partial: bool = False, exclude_none=True):
    if should_fail:
        with pytest.raises(ValueError):
            parse(data, model_type, allow_partial)
        return
    result = parse(data, model_type, allow_partial)

    if expected_json is not None:
        if isinstance(result, BaseModel):
            assert result.model_dump(exclude_none=exclude_none) == expected_json
        elif isinstance(result, list) and all(isinstance(r, BaseModel) for r in result):
            assert [r.model_dump(exclude_none=exclude_none) for r in result] == expected_json
        else:
            assert result == expected_json

# Test integer literals
def test_literal_integer_positive():
    data = "2"
    expected = 2
    case_parse(data, Literal[2], expected)

def test_literal_integer_negative():
    data = "-42"
    expected = -42
    case_parse(data, Literal[-42], expected)

def test_literal_integer_zero():
    data = "0"
    expected = 0
    case_parse(data, Literal[0], expected)

# Test boolean literals
def test_literal_boolean_true():
    data = "true"
    expected = True
    case_parse(data, Literal[True], expected)

def test_literal_boolean_false():
    data = "false"
    expected = False
    case_parse(data, Literal[False], expected)

# Test string literals
def test_literal_string_uppercase_with_double_quotes():
    data = '"TWO"'
    expected = "TWO"
    case_parse(data, Literal["TWO"], expected)

def test_literal_string_uppercase_without_quotes():
    data = "TWO"
    expected = "TWO"
    case_parse(data, Literal["TWO"], expected)

def test_literal_string_mismatched_case():
    data = "Two"
    expected = "TWO"
    case_parse(data, Literal["TWO"], expected)

def test_literal_string_lowercase():
    data = "two"
    expected = "TWO"
    case_parse(data, Literal["TWO"], expected)

def test_literal_string_preceded_by_extra_text():
    data = "The answer is TWO"
    expected = "TWO"
    case_parse(data, Literal["TWO"], expected)

def test_literal_string_preceded_by_extra_text_case_mismatch():
    data = "The answer is Two"
    expected = "TWO"
    case_parse(data, Literal["TWO"], expected)

def test_literal_string_followed_by_extra_text():
    data = "TWO is the answer"
    expected = "TWO"
    case_parse(data, Literal["TWO"], expected)

def test_literal_string_followed_by_extra_text_case_mismatch():
    data = "Two is the answer"
    expected = "TWO"
    case_parse(data, Literal["TWO"], expected)

def test_literal_string_with_quotes_preceded_by_extra_text():
    data = 'The answer is "TWO"'
    expected = "TWO"
    case_parse(data, Literal["TWO"], expected)

def test_literal_string_with_quotes_preceded_by_extra_text_case_mismatch():
    data = 'The answer is "two"'
    expected = "TWO"
    case_parse(data, Literal["TWO"], expected)

def test_literal_string_with_quotes_followed_by_extra_text():
    data = '"TWO" is the answer'
    expected = "TWO"
    case_parse(data, Literal["TWO"], expected)

def test_literal_string_with_quotes_followed_by_extra_text_case_mismatch():
    data = '"Two" is the answer'
    expected = "TWO"
    case_parse(data, Literal["TWO"], expected)

def test_literal_string_case_mismatch_upper():
    data = 'The answer "TWO" is the correct one'
    expected = "two"
    case_parse(data, Literal["two"], expected)

def test_literal_string_with_special_characters():
    data = '"TWO!@#"'
    expected = "TWO"
    case_parse(data, Literal["TWO"], expected)

def test_literal_string_with_whitespace():
    data = '"  TWO  "'
    expected = "TWO"
    case_parse(data, Literal["TWO"], expected)

def test_union_literal_integer_positive():
    data = "2"
    expected = 2
    case_parse(data, Union[Literal[2], Literal[3]], expected)

def test_union_literal_integer_positive_with_both():
    data = "2 or 3"
    case_parse(data, Union[Literal[2], Literal[3]])

def test_union_literal_bool_with_both():
    data = "true or false"
    case_parse(data, Union[Literal[2], Literal[3]], should_fail=True)

def test_union_literal_string_with_both():
    data = "TWO or THREE"
    expected = "TWO"
    case_parse(data, Union[Literal["TWO"], Literal["THREE"]], expected)

