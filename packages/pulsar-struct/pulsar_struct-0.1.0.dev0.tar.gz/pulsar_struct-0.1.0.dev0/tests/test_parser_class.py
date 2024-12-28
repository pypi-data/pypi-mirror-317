import pytest
from typing import List, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum
from pulsar.parser import parse


# Test Models
class Foo(BaseModel):
    hi: List[str]

class Bar(BaseModel):
    foo: str

class FooOptional(BaseModel):
    foo: Optional[str] = None

class FooMulti(BaseModel):
    one: str
    two: Optional[str] = None


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

# Test Cases
def test_class():
    """Test basic class."""
    case_parse('{"hi": ["a", "b"]}', Foo, {"hi": ["a", "b"]})
    case_parse('This is a test. The output is: {"hi": ["a", "b"]}', Foo, {"hi": ["a", "b"]})
    case_parse('{"hi": ["a", "b"]} is the output.', Foo, {"hi": ["a", "b"]})
    case_parse('{"hi": "a"}', Foo, {"hi": ["a"]})

@pytest.mark.skip(reason="TODO")
def test_str_quotes():
    """Test quotes class."""
    case_parse('{"foo": "[\"bar\"]"}', Bar, {"foo": "[\"bar\"]"})
    case_parse('{"foo": "{\"foo\": [\"bar\"]}"}', Bar, {"foo": "{\"foo\": [\"bar\"]}"})

def test_optional():
    """Test optional fields in class."""
    case_parse('{}', FooOptional, { })
    case_parse('{"foo": ""}', FooOptional, { "foo": "" })

def test_multi_optional():
    """Test multi optional fields in class."""
    case_parse('{"one": "a"}', FooMulti, { "one": "a" })
    case_parse('{"one": "a", "two": "b"}', FooMulti, { "one": "a", "two": "b" })

def test_multi_optional_extra_text():
    """Test multi optional fields in class with extra text."""
    data = """Here is how you can build the API call:
    ```json
        {
            "test2": {
                "key2": "value"
            },
            "test21": [
            ]    
        }
    ```
    ```json
    {
        "one": "hi",
        "two": "hello"
    }
    ```"""
    case_parse(data, FooMulti, { "one": "hi", "two": "hello" })

def test_multi_with_list():
    """Test multi fields in class with list."""
    class FooMultiList(BaseModel):
        a: int
        b: str
        c: List[str]

    case_parse('{"a": 1, "b": "hi", "c": ["a", "b"]}', FooMultiList, { "a": 1, "b": "hi", "c": ["a", "b"] })

def test_nested_class():
    """Test nested class."""
    class FooInner(BaseModel):
        a: str

    class BarNested(BaseModel):
        foo: FooInner

    case_parse('{"foo": {"a": "hi"}}', BarNested, { "foo": { "a": "hi" } })
    data = """Here is how you can build the API call:
    ```json
    {
        "foo": {
            "a": "hi"
        }
    }
    ```
    
    and this
    ```json
    {
        "foo": {
            "a": "twooo"
        }
    }"""
    case_parse(data, BarNested, { "foo": { "a": "hi" } })

    data = """Here is how you can build the API call:
    {
        "foo": {
            "a": "hi"
        }
    }
    
    and this
    {
        "foo": {
            "a": "twooo"
        }
    }"""
    case_parse(data, BarNested, { "foo": { "a": "hi" } })

## -----------------------







# Resume related models
class Resume(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    experience: List[str]
    education: List[str]
    skills: List[str]

# Test cases for Resume
def test_resume():
    data = """{
        "name": "Lee Hsien Loong",
        "email": null,
        "phone": null,
        "experience": [
            "Senior Minister of Singapore since 2024",
            "Prime Minister of Singapore from 2004 to 2024",
            "Member of Parliament (MP) for the Teck Ghee division of Ang Mo Kio GRC since 1991",
            "Teck Ghee SMC between 1984 and 1991",
            "Secretary-General of the People's Action Party (PAP) since 2004"
        ],
        "education": [],
        "skills": ["politician", "former brigadier-general"]
    }"""
    expected = {
        "name": "Lee Hsien Loong",
        "experience": [
            "Senior Minister of Singapore since 2024",
            "Prime Minister of Singapore from 2004 to 2024",
            "Member of Parliament (MP) for the Teck Ghee division of Ang Mo Kio GRC since 1991",
            "Teck Ghee SMC between 1984 and 1991",
            "Secretary-General of the People's Action Party (PAP) since 2004"
        ],
        "education": [],
        "skills": [
            "politician",
            "former brigadier-general"
        ]
    }
    case_parse(data, Resume, expected)

def test_resume_partial():
    data = """{
        "name": "Lee Hsien Loong",
        "email": null,
        "phone": null,
        "experience": [
            "Senior Minister of Singapore since 2024",
            "Prime Minister of Singapore from 2004 to 
    """
    expected = {
        "name": "Lee Hsien Loong",
        "experience": [
            "Senior Minister of Singapore since 2024",
            "Prime Minister of Singapore from 2004 to"
        ],
        "education": [],
        "skills": []
    }
    case_parse(data, Resume, expected, allow_partial=True)

# Nested class with list
class Education(BaseModel):
    school: str
    degree: str
    year: int

class ResumeWithEducation(BaseModel):
    name: str
    education: List[Education]
    skills: List[str]

def test_class_with_nested_list():
    data = """{
        "name": "Vaibhav Gupta",
        "education": [
            {
                "school": "FOOO",
                "degree": "FOOO",
                "year": 2015
            },
            {
                "school": "BAAR",
                "degree": "BAAR",
                "year": 2019
            }
        ],
        "skills": [
          "C++",
          "SIMD on custom silicon"
        ]
    }"""
    expected = {
        "name": "Vaibhav Gupta",
        "education": [
            {
                "school": "FOOO",
                "degree": "FOOO",
                "year": 2015
            },
            {
                "school": "BAAR",
                "degree": "BAAR",
                "year": 2019
            }
        ],
        "skills": [
            "C++",
            "SIMD on custom silicon"
        ]
    }
    case_parse(data, ResumeWithEducation, expected)

# Function related models
class Function1(BaseModel):
    function_name: str
    radius: int

class Function2(BaseModel):
    function_name: str
    diameter: int

class Function3(BaseModel):
    function_name: str
    length: int
    breadth: int

class Function(BaseModel):
    selected: Union[Function1, Function2, Function3]

@pytest.mark.skip(reason="TODO")
def test_function():
    data = """[
        {
          // Calculate the area of a circle based on the radius.
          function_name: 'circle.calculate_area',
          // The radius of the circle.
          radius: 5,
        },
        {
          // Calculate the circumference of a circle based on the diameter.
          function_name: 'circle.calculate_circumference',
          // The diameter of the circle.
          diameter: 10,
        }
    ]"""
    expected = [
        {"selected": {
            "function_name": "circle.calculate_area",
            "radius": 5
        }},
        {"selected": {
            "function_name": "circle.calculate_circumference",
            "diameter": 10
        }}
    ]
    case_parse(data, List[Function], expected)

@pytest.mark.skip(reason="TODO")
def test_recursive_type():
    """Test Recursive type tests."""
    class FooRecursive(BaseModel):
        pointer: Optional['FooRecursive'] = None
    data = """
    The answer is
    {
      "pointer": {
        "pointer": null
      }
    },
    
    Anything else I can help with?
    """
    expected = {
        "pointer": {
            "pointer": None
        }
    }
    case_parse(data, FooRecursive, expected, exclude_none=False)

# BigNumbers related tests
class BigNumbers(BaseModel):
    a: int
    b: float

class CompoundBigNumbers(BaseModel):
    big: Optional[BigNumbers] = None
    big_nums: List[BigNumbers] = []
    another: Optional[BigNumbers] = None

def test_big_object_empty():
    data = "{"
    expected = {"big": None, "big_nums": [], "another": None}
    case_parse(data, CompoundBigNumbers, expected, allow_partial=True, exclude_none=False)

def test_big_object_start_big():
    data = """{"big": {"a": 11, "b": 12"""
    expected = {"big": {"a": 11, "b": 12.0}, "big_nums": [], "another": None}
    case_parse(data, CompoundBigNumbers, expected, allow_partial=True, exclude_none=False)

def test_empty_string_value():
    class EmptyStringTest(BaseModel):
        a: str
        b: str
        res: List[str]

    data = """{
        a: "",
        b: "",
        res: []
    }"""
    expected = {"a": "", "b": "", "res": []}
    case_parse(data, EmptyStringTest, expected)
