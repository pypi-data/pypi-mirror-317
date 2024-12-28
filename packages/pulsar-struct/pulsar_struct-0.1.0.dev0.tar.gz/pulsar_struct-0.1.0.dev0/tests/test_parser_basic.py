import pytest
from typing import List, Optional, Union
from pydantic import BaseModel
from enum import Enum
from pulsar.parser import parse


# Test Models
class Foo(BaseModel):
    key: str

class ExampleModel(BaseModel):
    key: str
    array: List[int]
    object: Optional[Foo] = None

class CityType(Enum):
    CAPITAL = "capital"
    METROPOLIS = "metropolis"
    TOWN = "town"

class City(BaseModel):
    name: str
    population: int
    type: CityType
    landmarks: List[str]
    mayor: Optional[str] = None

class Person(BaseModel):
    name: str
    age: int
    scores: List[int]
    occupation: Optional[str] = None

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
def test_null():
    """Test for null values"""
    case_parse("null", type(None))

def test_null_str():
    """Test for null values"""
    case_parse("null", str, "")
    case_parse('{"key": "null"}', Foo, {'key': ''})    

def test_null_optional():
    """Test for optional string accepting null"""
    class OptionalModel(BaseModel):
        value: Optional[str] = None
    case_parse('{ }', OptionalModel, {"value": None}, exclude_none=False)

def test_numbers():
    """Test number parsing"""
    case_parse("12111", int, 12111)
    case_parse("12,111", int, 12111)
    case_parse("12111.123", float, 12111.123)

def test_strings():
    """Test string parsing"""
    case_parse('"hello"', str, 'hello')

def test_booleans():
    """Test boolean parsing"""
    case_parse("true", bool, True)
    case_parse("True", bool, True)
    case_parse("false", bool, False)
    case_parse("False", bool, False)

def test_arrays():
    """Test array parsing"""
    case_parse("[1, 2, 3]", List[int], [1, 2, 3])
    case_parse("[1, 2, 3]", List[str], ["1", "2", "3"])
    case_parse("[1, 2, 3]", List[float], [1.0, 2.0, 3.0])

def test_objects():
    """Test object parsing"""
    class TestModel(BaseModel):
        key: str
        
    data = '{"key": "value"}'
    expected = {"key": "value"}
    case_parse(data, TestModel, expected)

def test_nested_objects():
    """Test nested object parsing"""
    data = '{"key": "A", "array": [1, 2, 3]}'
    expected = {"key": "A", "array": [1, 2, 3]}
    case_parse(data, ExampleModel, expected)

def test_whitespace():
    """Test handling of whitespace"""
    data = ' { "key" : "A", "array" : [ 1 , 2 , 3 ] } '
    expected = {"key": "A", "array": [1, 2, 3]}
    case_parse(data, ExampleModel, expected)

def test_prefix_suffix():
    """Test handling of prefix and suffix text"""
    data = 'prefix {"key": "A", "array": [1, 2, 3]} suffix'
    expected = {"key": "A", "array": [1, 2, 3]}
    case_parse(data, ExampleModel, expected)

def test_multiple_objects():
    """Test parsing multiple top-level objects"""
    class TestModel(BaseModel):
        key: str
        
    data = '{"key": "value1"} {"key": "value2"}'
    expected = {"key": "value1"}
    case_parse(data, TestModel, expected)
    
    case_parse(data, List[TestModel], [
        {"key": "value1"},
        {"key": "value2"}
    ])

def test_trailing_comma():
    """Test handling of trailing commas"""
    data = '[1, 2, 3,]'
    case_parse(data, List[int], [1, 2, 3])
    case_parse(data, List[str], ["1", "2", "3"])
    
    class TestModel(BaseModel):
        key: str
    data = '{"key": "value",}'
    expected = {"key": "value"}
    case_parse(data, TestModel, expected)

def test_invalid_json():
    """Test handling of invalid JSON"""
    data = '[1, 2, 3'  # Unclosed array
    case_parse(data, List[int], [1, 2, 3])
    
    class TestModel(BaseModel):
        key: List[int]
    data = '{"key": [1, 2, 3'  # Unclosed array in object
    expected = {"key": [1, 2, 3]}
    case_parse(data, TestModel, expected)

def test_unquoted_keys():
    """Test handling JSON unquoted keys"""
    data = "[1, 2, 3, 'some string with quotes' /* test */]" 
    case_parse(data, List[Union[int, str]], [1, 2, 3, "some string with quotes"])
    
    class TestModel(BaseModel):
        key: List[Union[int, str]]
    data = "{key: [1, 2, 3, 'some string with quotes' /* test */]"  
    expected = {"key": [1, 2, 3, "some string with quotes"]}
    case_parse(data, TestModel, expected)

def test_unquoted_values_with_spaces():
    """Test JSON unquoted values with spaces"""
    class TestModel(BaseModel):
        key: str
        
    data = '{ key: value with space }'
    expected = {"key": "value with space"}
    case_parse(data, TestModel, expected)

    data = '''{ key: value with 
    new line 
    }'''
    expected = {"key": "value with new line"}
    case_parse(data, TestModel, expected)

def test_localization():
    """Test JSON localize"""
    class TestModel(BaseModel):
        id: str
        English: str
        Portuguese: str
        
    data = '''To effectively localize these strings for a Portuguese-speaking audience, I will focus on maintaining the original tone and meaning while ensuring that the translations sound natural and culturally appropriate. For the game title "Arcadian Atlas," I will keep it unchanged as it is a proper noun and likely a branded term within the game. For the other strings, I will adapt them to resonate with Portuguese players, using idiomatic expressions if necessary and ensuring that the sense of adventure and urgency is conveyed.

    For the string with the placeholder {player_name}, I will ensure that the placeholder is kept intact and that the surrounding text is grammatically correct and flows naturally in Portuguese. The name "Jonathan" will remain unchanged as it is a proper noun and recognizable in Portuguese.

    JSON Output:
    ```
    [
    {
        "id": "CH1_Welcome",
        "English": "Welcome to Arcadian Atlas",
        "Portuguese": "Bem-vindo ao Arcadian Atlas"
    },
    {
        "id": "CH1_02",
        "English": "Arcadia is a vast land, with monsters and dangers!",
        "Portuguese": "Arcadia é uma terra vasta, repleta de monstros e perigos!"
    },
    {
        "id": "CH1_03",
        "English": "Find him {player_name}. Find him and save Arcadia. Jonathan will save us all. It is the only way.",
        "Portuguese": "Encontre-o {player_name}. Encontre-o e salve Arcadia. Jonathan nos salvará a todos. É a única maneira."
    }
    ]
    ```
    '''
    expected = [{
      "id": "CH1_Welcome",
      "English": "Welcome to Arcadian Atlas",
      "Portuguese": "Bem-vindo ao Arcadian Atlas"
    },
    {
      "id": "CH1_02",
      "English": "Arcadia is a vast land, with monsters and dangers!",
      "Portuguese": "Arcadia é uma terra vasta, repleta de monstros e perigos!"
    },
    {
      "id": "CH1_03",
      "English": "Find him {player_name}. Find him and save Arcadia. Jonathan will save us all. It is the only way.",
      "Portuguese": "Encontre-o {player_name}. Encontre-o e salve Arcadia. Jonathan nos salvará a todos. É a única maneira."
    }]
    case_parse(data, List[TestModel], expected)

def test_sidd():
    """Test SIDD"""

    class Heading(BaseModel):
        heading: str
        python_function_code: str
        description: str
    
    class Headings(BaseModel):
        headings: List[Heading]
        
    data = '''<thinking>
    To create a personalized catalogue for the customer, I need to analyze both the properties available and the customer's requirements. The customer is looking for an apartment that is 970.0 sq.ft. and costs Rs. 27,030,000.00. However, none of the listed properties match these specifications perfectly.

    1. **Analyze the Properties**: I'll look at the properties provided to identify common themes, features, or unique selling points that can inspire creative headings.
    2. **Consider Customer Requirements**: While the customer has specific requirements, the task is to create headings that are creative and interesting, not strictly based on those requirements.
    3. **Generate Creative Headings**: I will brainstorm seven catchy headings that can be used to categorize the properties in a way that highlights their best features or unique aspects.

    Next, I will generate the headings and their corresponding Python functions to categorize the properties.
    </thinking>

    <reflection>
    I have considered the properties and the customer's requirements. The next step is to formulate creative headings that reflect the unique aspects of the properties without being overly focused on the customer's specific requirements. I will ensure that each heading is distinct and engaging.
    </reflection>

    <thinking>
    Here are the seven creative headings along with their descriptions and Python functions:

    1. **Urban Oasis**
    - This heading captures properties that offer a serene living experience amidst the bustling city life.
    - Python function:
    ```python
    def is_urban_oasis(property):
        return 'Large Green Area' in property['amenities'] or 'Garden' in property['amenities']
    ```

    Now, I will compile these into the required format.
    </thinking>

    {
    "headings": [
        {
        "heading": "Urban Oasis",
        "python_function_code": """def is_urban_oasis(property):
        return 'Large Green Area' in property['amenities'] or 'Garden' in property['amenities']""",
        "description": "Properties that offer a serene living experience amidst the bustling city life."
        }
    ]
    }'''

    expected = {'headings': [{'heading': 'Urban Oasis', 'python_function_code': "def is_urban_oasis(property):\n        return 'Large Green Area' in property['amenities'] or 'Garden' in property['amenities']", 'description': 'Properties that offer a serene living experience amidst the bustling city life.'}]}
    case_parse(data, Headings, expected)

def test_markdown():
    """Test parsing markdown code blocks"""
    data = '''
    some text
    ```json
    {
        "key": "value",
        "array": [1, 2, 3],
        "object": {
            "key": "value"
        }
    }
    ```
    '''
    expected = {
        "key": "value",
        "array": [1, 2, 3],
        "object": {"key": "value"}
    }
    case_parse(data, ExampleModel, expected)

def test_union_parsing():
    """Test parsing Union types"""
    city_data = '''
    {
        "name": "New York",
        "population": "8.4M",
        "type": "METROPOLIS",
        "landmarks": [
            "Statue of Liberty",
            "Empire State Building",
            "Central Park"
        ],
        "mayor": "Eric Adams"
    }
    '''
    
    person_data = '''
    {
        "name": "John Doe",
        "age": 30,
        "scores": [85, 92, 78],
        "occupation": "Software Engineer"
    }
    '''
    
    # Test parsing as Union
    case_parse(city_data, Union[Person, City], {
        "name": "New York",
        "population": 8400000,
        "type": CityType.METROPOLIS,
        "landmarks": ["Statue of Liberty", "Empire State Building", "Central Park"],
        "mayor": "Eric Adams"
    })
    
    case_parse(person_data, Union[Person, City], {
        "name": "John Doe",
        "age": 30,
        "scores": [85, 92, 78],
        "occupation": "Software Engineer"
    })

def test_partial_parsing():
    """Test partial parsing mode"""
    class ComplexModel(BaseModel):
        required_field: str
        optional_field: Optional[str] = None
        nested: Optional[List[dict]] = None
        
    data = '''
    {
        "required_field": "value",
        "bad_field": {
            This is invalid JSON
        }
    }
    '''
    
    # Should fail in normal mode
    # case_parse(data, ComplexModel, should_fail=True)
    
    # Should succeed in partial mode
    expected = {"required_field": "value"}
    case_parse(data, ComplexModel, expected, allow_partial=True)

