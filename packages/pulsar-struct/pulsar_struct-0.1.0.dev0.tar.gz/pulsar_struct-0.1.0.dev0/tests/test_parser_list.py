import pytest
from typing import List, Optional, Union, Any
from pydantic import BaseModel
from pulsar.parser import parse

# Model for object list tests
class Foo(BaseModel):
    a: int
    b: str

class ListClass(BaseModel):
    date: str
    description: str
    transaction_amount: float
    transaction_type: str

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

# Basic list tests
def test_list():
    data = '["a", "b"]'
    expected = ["a", "b"]
    case_parse(data, List[str], expected)

def test_list_with_quotes():
    data = r'["\"a\"", "\"b\""]'
    expected = ['"a"', '"b"']
    case_parse(data, List[str], expected)

def test_list_with_extra_text():
    data = '["a", "b"] is the output.'
    expected = ["a", "b"]
    case_parse(data, List[str], expected)

def test_list_with_invalid_extra_text():
    data = '[a, b] is the output.'
    expected = ["a", "b"]
    case_parse(data, List[str], expected)

def test_list_object_from_string():
    data = '[{"a": 1, "b": "hello"}, {"a": 2, "b": "world"}]'
    expected = [
        {"a": 1, "b": "hello"},
        {"a": 2, "b": "world"}
    ]
    case_parse(data, List[Foo], expected)

def test_class_list():
    data = """
    [
        {
            "date": "01/01",
            "description": "Transaction 1",
            "transaction_amount": -100.00,
            "transaction_type": "Withdrawal"
        },
        {
            "date": "01/02",
            "description": "Transaction 2",
            "transaction_amount": -2,000.00,
            "transaction_type": "Withdrawal"
        },
        {
            "date": "01/03",
            "description": "Transaction 3",
            "transaction_amount": -300.00,
            "transaction_type": "Withdrawal"
        },
        {
            "date": "01/04",
            "description": "Transaction 4",
            "transaction_amount": -4,000.00,
            "transaction_type": "Withdrawal"
        },
        {
            "date": "01/05",
            "description": "Transaction 5",
            "transaction_amount": -5,000.00,
            "transaction_type": "Withdrawal"
        }
    ]
    """
    expected = [
        {
            "date": "01/01",
            "description": "Transaction 1",
            "transaction_amount": -100.00,
            "transaction_type": "Withdrawal"
        },
        {
            "date": "01/02",
            "description": "Transaction 2",
            "transaction_amount": -2000.00,
            "transaction_type": "Withdrawal"
        },
        {
            "date": "01/03",
            "description": "Transaction 3",
            "transaction_amount": -300.00,
            "transaction_type": "Withdrawal"
        },
        {
            "date": "01/04",
            "description": "Transaction 4",
            "transaction_amount": -4000.00,
            "transaction_type": "Withdrawal"
        },
        {
            "date": "01/05",
            "description": "Transaction 5",
            "transaction_amount": -5000.00,
            "transaction_type": "Withdrawal"
        }
    ]
    case_parse(data, List[ListClass], expected)

def test_list_streaming():
    data = '[1234, 5678'
    expected = [1234, 5678]
    case_parse(data, List[int], expected)

def test_list_streaming_2():
    data = '[1234'
    expected = [1234]
    case_parse(data, List[int], expected)

def test_list_streaming_partial():
    data = '[1234, 5678'
    expected = [1234, 5678]
    case_parse(data, List[int], expected, allow_partial=True)

