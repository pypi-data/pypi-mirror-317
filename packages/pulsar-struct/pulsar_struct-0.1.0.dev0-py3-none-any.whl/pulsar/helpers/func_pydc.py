from typing import Dict, Any, Optional, Type, Literal, Callable, List
from pydantic import create_model, BaseModel
import inspect


def parse_docstring(description: str) -> tuple[str, Dict[str, str]]:
    """Parse function description into docstring and args documentation."""
    parts = description.split("\n\nArgs:\n")
    main_desc = parts[0].strip()
    args_desc = {}

    if len(parts) > 1:
        arg_lines = parts[1].strip().split("\n")
        for line in arg_lines:
            if ":" in line:
                arg_name, arg_desc = line.split(":", 1)
                args_desc[arg_name.strip()] = arg_desc.strip()

    return main_desc, args_desc


def get_type_mapping(schema_type: str) -> Type:
    """Convert JSON schema types to Python types."""
    type_map = {
        "string": str,
        "integer": int,
        "number": float,
        "boolean": bool,
        "array": list,
        "object": dict
    }
    return type_map.get(schema_type, Any)


def schema_to_pydantic(schema: Dict[str, Any], include_name: bool = False) -> Type[BaseModel]:
    """Convert a JSON schema to a Pydantic model class.

    Args:
        schema: The input JSON schema
        include_name: If True, adds a required func_name field with Literal type of the function name
    """
    if schema["type"] != "function":
        raise ValueError("Schema must be of type 'function'")

    func_schema = schema["function"]
    name = func_schema["name"].capitalize()
    description = func_schema["description"]
    parameters = func_schema["parameters"]

    # Parse properties
    fields = {}
    required = parameters.get("required", [])
    properties = parameters.get("properties", {})

    # Parse docstring
    main_desc, args_desc = parse_docstring(description)

    # Build fields
    for field_name, field_schema in properties.items():
        field_type = get_type_mapping(field_schema["type"])
        is_required = field_name in required

        if not is_required:
            # Add default value for optional fields
            if field_type == str:
                fields[field_name] = (Optional[field_type], "New York")
            else:
                fields[field_name] = (Optional[field_type], None)
        else:
            fields[field_name] = (field_type, ...)

    # Add func_name field if requested - now always as required
    if include_name:
        # Making it required by using ...
        fields["func_name"] = (Literal[func_schema["name"]], ...)

    # Create docstring
    docstring = f'"""{main_desc}\n\nArgs:'
    for arg_name, arg_desc in args_desc.items():
        docstring += f'\n   {arg_name}: {arg_desc}'
    if include_name:
        docstring += f'\n   func_name: The name of the function (always "{func_schema["name"]}")'
    docstring += '\n"""'

    # Create model
    model = create_model(
        name,
        __base__=BaseModel,
        **fields
    )

    # Add docstring
    model.__doc__ = docstring

    return model


def function_to_json(func, skip_params: Optional[List[str]] = None) -> dict:
    """
    Converts a Python function into a JSON-serializable dictionary
    that describes the function's signature, including its name,
    description, and parameters.

    Args:
        func: The function to be converted.

    Returns:
        A dictionary representing the function's signature in JSON format.
    """
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        type(None): "null",
    }

    try:
        signature = inspect.signature(func)
    except ValueError as e:
        raise ValueError(
            f"Failed to get signature for function {func.__name__}: {str(e)}"
        )

    skip_params = skip_params if skip_params is not None else []
    parameters = {}
    for param in signature.parameters.values():
        if param.name in skip_params:
            continue
        try:
            param_type = type_map.get(param.annotation, "string")
        except KeyError as e:
            raise KeyError(
                f"Unknown type annotation {param.annotation} for parameter {param.name}: {str(e)}"
            )
        parameters[param.name] = {"type": param_type}

    required = [
        param.name
        for param in signature.parameters.values()
        if param.default == inspect._empty
    ]

    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": func.__doc__ or "",
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": required,
            },
        },
    }


def function_to_pydantic(func: Callable, include_name=False, skip_params: Optional[List[str]] = None):
    input_schema = function_to_json(func, skip_params)
    model = schema_to_pydantic(input_schema, include_name=include_name)
    return model


# Example usage:
if __name__ == "__main__":
    input_schema = {
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

    # Without func_name
    GreetModel = schema_to_pydantic(input_schema)
    print("Without func_name:")
    print(GreetModel.__doc__)
    print("\nModel fields:", GreetModel.__fields__)

    # With func_name
    GreetModelWithName = schema_to_pydantic(input_schema, include_name=True)
    print("\nWith func_name:")
    print(GreetModelWithName.__doc__)
    print("\nModel fields:", GreetModelWithName.__fields__)

    def greet(name, age: int, location: str = "New York", context_variables=None):
        """Greets the user. Make sure to get their name and age before calling.

        Args:
            name: Name of the user.
            age: Age of the user.
            location: Best place on earth.
        """
        print(f"Hello {name}, glad you are {age} in {location}!")

    GreetModelWithName = function_to_pydantic(
        greet, include_name=True, skip_params=["context_variables"])
    print("\nWith func_name:")
    print(GreetModelWithName.__doc__)
    print("\nModel fields:", GreetModelWithName.__fields__)
