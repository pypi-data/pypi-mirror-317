import pytest
from pydantic import ValidationError
from typing import Literal, Optional

from pulsar.helpers import schema_to_pydantic, function_to_json


@pytest.fixture
def basic_schema():
    return {
        "type": "function",
        "function": {
            "name": "greet",
            "description": "Greets the user. Make sure to get their name and age before calling.\n\nArgs:\n   name: Name of the user.\n   age: Age of the user.\n   location: Best place on earth.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"},
                    "location": {"type": "string"}
                },
                "required": ["name", "age"]
            }
        }
    }

def test_basic_model_creation(basic_schema):
    """Test basic model creation without func_name."""
    model = schema_to_pydantic(basic_schema)
    
    # Check class name
    assert model.__name__ == "Greet"
    
    # Check field types
    assert model.__annotations__["name"] == str
    assert model.__annotations__["age"] == int
    assert model.__annotations__["location"] == Optional[str]

def test_model_with_func_name(basic_schema):
    """Test model creation with func_name included."""
    model = schema_to_pydantic(basic_schema, include_name=True)
    
    # Check func_name field exists and has correct Literal type
    assert model.__annotations__["func_name"] == Literal["greet"]
    
    # Create instance and verify func_name
    instance = model(func_name="greet", name="Alice", age=30)
    assert instance.func_name == "greet"

def test_required_fields(basic_schema):
    """Test validation of required fields."""
    model = schema_to_pydantic(basic_schema)
    
    # Should work with all required fields
    instance = model(name="Alice", age=30)
    assert instance.name == "Alice"
    assert instance.age == 30
    
    # Should fail without required fields
    with pytest.raises(ValidationError):
        model(name="Alice")  # Missing age
    
    with pytest.raises(ValidationError):
        model(age=30)  # Missing name

def test_optional_fields(basic_schema):
    """Test optional fields with default values."""
    model = schema_to_pydantic(basic_schema)
    
    # Create instance without optional field
    instance = model(name="Alice", age=30)
    assert instance.location == "New York"  # Default value
    
    # Create instance with optional field
    instance = model(name="Alice", age=30, location="Paris")
    assert instance.location == "Paris"

def test_field_types_validation(basic_schema):
    """Test type validation for fields."""
    model = schema_to_pydantic(basic_schema)
    
    # Test invalid types
    with pytest.raises(ValidationError):
        model(name=123, age=30)  # name should be string
    
    with pytest.raises(ValidationError):
        model(name="Alice", age="thirty")  # age should be integer
    
    with pytest.raises(ValidationError):
        model(name="Alice", age=30, location=123)  # location should be string

def test_docstring_generation(basic_schema):
    """Test docstring is generated correctly."""
    model = schema_to_pydantic(basic_schema)
    
    # Check main description
    assert "Greets the user" in model.__doc__
    
    # Check args documentation
    assert "name: Name of the user" in model.__doc__
    assert "age: Age of the user" in model.__doc__
    assert "location: Best place on earth" in model.__doc__

def test_invalid_schema():
    """Test handling of invalid schema."""
    invalid_schema = {
        "type": "not_function",
        "function": {}
    }
    
    with pytest.raises(ValueError, match="Schema must be of type 'function'"):
        schema_to_pydantic(invalid_schema)

def test_different_field_types(basic_schema):
    """Test handling of different field types."""
    basic_schema["function"]["parameters"]["properties"].update({
        "is_active": {"type": "boolean"},
        "score": {"type": "number"},
        "tags": {"type": "array"},
        "metadata": {"type": "object"}
    })
    
    model = schema_to_pydantic(basic_schema)
    
    # Check field types
    assert model.__annotations__["is_active"] == Optional[bool]
    assert model.__annotations__["score"] == Optional[float]
    assert model.__annotations__["tags"] == Optional[list]
    assert model.__annotations__["metadata"] == Optional[dict]

def test_func_name_in_docstring(basic_schema):
    """Test func_name field is documented when included."""
    model = schema_to_pydantic(basic_schema, include_name=True)
    
    assert 'func_name: The name of the function (always "greet")' in model.__doc__

def test_model_instance_creation_with_all_fields(basic_schema):
    """Test creating model instance with all fields."""
    model = schema_to_pydantic(basic_schema, include_name=True)
    
    instance = model(
        func_name="greet",
        name="Alice",
        age=30,
        location="Paris"
    )
    
    assert instance.name == "Alice"
    assert instance.age == 30
    assert instance.location == "Paris"
    assert instance.func_name == "greet"
    
    # Verify model dump works
    data = instance.model_dump()
    assert all(k in data for k in ["name", "age", "location", "func_name"])


def test_basic_function():
    def basic_function(arg1, arg2):
        return arg1 + arg2

    result = function_to_json(basic_function)
    assert result == {
        "type": "function",
        "function": {
            "name": "basic_function",
            "description": "",
            "parameters": {
                "type": "object",
                "properties": {
                    "arg1": {"type": "string"},
                    "arg2": {"type": "string"},
                },
                "required": ["arg1", "arg2"],
            },
        },
    }


def test_complex_function():
    def complex_function_with_types_and_descriptions(
        arg1: int, arg2: str, arg3: float = 3.14, arg4: bool = False
    ):
        """This is a complex function with a docstring."""
        pass

    result = function_to_json(complex_function_with_types_and_descriptions)
    assert result == {
        "type": "function",
        "function": {
            "name": "complex_function_with_types_and_descriptions",
            "description": "This is a complex function with a docstring.",
            "parameters": {
                "type": "object",
                "properties": {
                    "arg1": {"type": "integer"},
                    "arg2": {"type": "string"},
                    "arg3": {"type": "number"},
                    "arg4": {"type": "boolean"},
                },
                "required": ["arg1", "arg2"],
            },
        },
    }