import pytest
from typing import List, Optional, Union, Literal
from enum import Enum
from pydantic import BaseModel, Field
from pulsar.parser import parse

# Enum definitions
class Category(str, Enum):
    ONE = "ONE"
    TWO = "TWO"

class PascalCaseCategory(str, Enum):
    One = "One"
    Two = "Two"

class CategoryWithDescriptions(str, Enum):
    ONE = "ONE"
    TWO = "TWO"
    THREE = "THREE"

class TaxReturnFormType(str, Enum):
    F9325 = "F9325"  # @alias("9325")
    F9465 = "F9465"  # @alias("9465")
    F1040 = "F1040"  # @alias("1040")
    F1040X = "F1040X"  # @alias("1040-X")

class Car(str, Enum):
    A = "A"  # @alias("car")
    B = "B"  # @alias("car-2")

# Test Helper Functions
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

# Basic enum tests
def test_enum():
    data = "TWO"
    expected = "TWO"
    case_parse(data, Category, expected)

def test_case_insensitive():
    data = "two"
    expected = "TWO"
    case_parse(data, Category, expected)

def test_with_quotes():
    data = '"TWO"'
    expected = "TWO"
    case_parse(data, Category, expected)

def test_from_enum_list_single():
    data = '["TWO"]'
    expected = "TWO"
    case_parse(data, Category, expected)

def test_from_enum_list_multi():
    data = '["TWO", "THREE"]'
    expected = "TWO"
    case_parse(data, Category, expected)

def test_from_string_with_extra_text_after_1():
    data = '"ONE: The description of k1"'
    expected = "ONE"
    case_parse(data, Category, expected)

def test_from_string_and_case_mismatch():
    data = "The answer is One"
    expected = "ONE"
    case_parse(data, Category, expected)

def test_from_string_and_case_mismatch_wrapped():
    data = "**one** is the answer"
    expected = "ONE"
    case_parse(data, Category, expected)

def test_from_string_and_case_mismatch_upper():
    data = "**ONE** is the answer"
    expected = "One"
    case_parse(data, PascalCaseCategory, expected)

def test_case_sensitive_non_ambiguous_match():
    data = 'TWO is one of the correct answers.'
    expected = "TWO"
    case_parse(data, Category, expected)

@pytest.mark.skip(reason="TODO")
def test_case_insensitive_ambiguous_match():
    data = 'Two is one of the correct answers.'
    case_parse(data, Category, should_fail=True)

def test_no_punctuation():
    data = "number three"
    expected = "THREE"
    case_parse(data, CategoryWithDescriptions, expected)

def test_descriptions():
    data = "ONE: The description of enum value une"
    expected = "ONE"
    case_parse(data, CategoryWithDescriptions, expected)

def test_list_of_enums():
    data = '["ONE", "TWO"]'
    expected = ["ONE", "TWO"]
    case_parse(data, List[CategoryWithDescriptions], expected)

def test_list_of_enums_2():
    data = '''I would think something like this!
```json    
[One, "two", "NUMBER THREE"]
```
'''
    expected = ["ONE", "TWO", "THREE"]
    case_parse(data, List[CategoryWithDescriptions], expected)

def test_numerical_enum():
    data = '''
(such as 1040-X, 1040, etc.) or any payment vouchers.

Based on the criteria provided, this page does not qualify as a tax return form page. Therefore, the appropriate response is:

```json
null
``` 

This indicates that there is no relevant tax return form type present on the page.
    '''
    expected = None
    case_parse(data, Optional[TaxReturnFormType], expected)

@pytest.mark.skip(reason="TODO")
def test_ambiguous_substring_enum():
    data = "The answer is not car or car-2!"
    case_parse(data, Car, should_fail=True)

