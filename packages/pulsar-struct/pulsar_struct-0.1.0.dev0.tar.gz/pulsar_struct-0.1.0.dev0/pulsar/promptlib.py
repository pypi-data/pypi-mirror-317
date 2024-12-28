from typing import Any, Dict, List, Optional, Union, get_args, get_origin, Tuple, Literal
from pydantic import BaseModel, Field
import inspect
from typing import _GenericAlias  # type: ignore
import json
from dataclasses import dataclass
from enum import Enum


@dataclass
class SchemaNode:
    """Helper class to maintain schema structure before final string conversion"""
    value: Any
    class_name: str = None
    description: str = None


class JsonSchemaGenerator:
    PRIMITIVE_TYPE_MAP = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        type(None): "null"
    }

    @classmethod
    def _handle_literal(cls, literal_type: type) -> Tuple[SchemaNode, int]:
        """Handle Literal type hints."""
        args = get_args(literal_type)
        values = [f'"{arg}"' if isinstance(
            arg, str) else str(arg) for arg in args]
        return SchemaNode(" or ".join(values)), len(args)

    @classmethod
    def _handle_enum(cls, enum_class: type) -> Tuple[SchemaNode, int]:
        """Handle Enum classes."""
        values = [f"'{item.value}'" for item in enum_class]
        return SchemaNode(" or ".join(values)), len(values)

    @classmethod
    def _format_schema(cls, node: SchemaNode, indent_level: int = 0, show_name: bool = True) -> str:
        """Convert schema node to its string representation."""
        indent_str = "  " * indent_level

        if isinstance(node.value, str):
            return node.value
        elif isinstance(node.value, dict):
            lines = []

            # Add opening brace with class name if provided and show_name is True
            if node.class_name and show_name:
                lines.append(f"{indent_str}{{ // {node.class_name}")
            else:
                lines.append(f"{indent_str}{{")

            # Format fields with inline descriptions
            field_items = list(node.value.items())
            for idx, (key, value) in enumerate(field_items):
                if key.startswith("//"):
                    continue

                # Get description if available
                desc_key = f"//{key}"
                description = node.value.get(desc_key)

                # Format the value
                value_str = cls._format_schema(
                    value, indent_level + 1, show_name)
                if isinstance(value.value, (dict, list)):
                    line = f'{indent_str}  "{key}": {value_str}'
                else:
                    # Removed quotes around value_str
                    line = f'{indent_str}  "{key}": {value_str}'

                if description:
                    line += f" // {description}"

                # Add comma if not the last item
                if idx < len([k for k in field_items if not k[0].startswith("//")]) - 1:
                    line += ","

                lines.append(line)

            lines.append(f"{indent_str}}}")
            return "\n".join(lines)
        elif isinstance(node.value, list):
            if len(node.value) == 0:
                return "[]"

            lines = [f"{indent_str}["]

            for idx, item in enumerate(node.value):
                item_str = cls._format_schema(
                    item, indent_level + 1, show_name)
                if idx < len(node.value) - 1:
                    item_str += ","
                lines.append(item_str)

            lines.append(f"{indent_str}]")
            return "\n".join(lines)

        return str(node.value)

    @classmethod
    def _handle_union(cls, union_type: type, show_name: bool) -> Tuple[SchemaNode, int]:
        args = get_args(union_type)
        schemas_with_lens = [cls.generate_schema(
            arg, show_name) for arg in args]

        formatted_schemas = []
        for arg, (schema, _) in zip(args, schemas_with_lens):
            if inspect.isclass(arg) and issubclass(arg, BaseModel):
                formatted_schemas.append(schema)
            elif (get_origin(arg) is list and
                  len(get_args(arg)) > 0 and
                  inspect.isclass(get_args(arg)[0]) and
                  issubclass(get_args(arg)[0], BaseModel)):
                formatted_schemas.append(schema)
            else:
                formatted_schemas.append(schema)

        return SchemaNode("\nor\n".join(cls._format_schema(s, show_name=show_name) for s in formatted_schemas)), len(args)

    @classmethod
    def _handle_list(cls, list_type: type, show_name: bool) -> Tuple[SchemaNode, int]:
        item_type = get_args(list_type)[0]
        item_schema, inner_len = cls.generate_schema(item_type, show_name)

        class_name = None
        if inspect.isclass(item_type) and issubclass(item_type, BaseModel):
            class_name = item_type.__name__

        return SchemaNode([item_schema], class_name), 1

    @classmethod
    def _handle_optional(cls, optional_type: type, show_name: bool) -> Tuple[SchemaNode, int]:
        inner_type = get_args(optional_type)[0]
        inner_schema, _ = cls.generate_schema(inner_type, show_name)
        null_schema, _ = cls.generate_schema(type(None), show_name)
        return SchemaNode([null_schema, inner_schema]), 2

    @classmethod
    def _handle_pydantic_model(cls, model_class: type) -> Tuple[SchemaNode, int]:
        schema = {}

        for name, field in model_class.model_fields.items():
            field_type = field.annotation
            field_schema, _ = cls.generate_schema(field_type, True)

            description = field.description
            if description:
                schema[f"//{name}"] = description

            schema[name] = field_schema

        return SchemaNode(schema, model_class.__name__), 1

    @classmethod
    def generate_schema(cls, type_hint: Any, show_name: bool = True) -> Tuple[SchemaNode, int]:
        # Handle None
        if type_hint is None:
            return SchemaNode("null"), 1

        # Handle primitives
        if type_hint in cls.PRIMITIVE_TYPE_MAP:
            return SchemaNode(cls.PRIMITIVE_TYPE_MAP[type_hint]), 1

        # Handle Enum classes
        if inspect.isclass(type_hint) and issubclass(type_hint, Enum):
            return cls._handle_enum(type_hint)

        # Get origin type for generic types
        origin = get_origin(type_hint)

        # Handle Literal types
        if origin is Literal:
            return cls._handle_literal(type_hint)

        # Handle Union types (including Optional)
        if origin is Union:
            schema, length = cls._handle_union(type_hint, show_name)
            if len(schema.value) == 2 and any(s.value == "null" for s in schema.value):
                # Format Optional types differently
                non_null = next(s for s in schema.value if s.value != "null")
                return SchemaNode(f"null or {cls._format_schema(non_null, show_name=show_name)}"), length
            return schema, length

        # Handle List types
        if origin is list or (isinstance(type_hint, _GenericAlias) and type_hint.__origin__ is list):
            return cls._handle_list(type_hint, show_name)

        # Handle Optional types
        if origin is Optional:
            return cls._handle_optional(type_hint, show_name)

        # Handle Pydantic models
        if inspect.isclass(type_hint) and issubclass(type_hint, BaseModel):
            return cls._handle_pydantic_model(type_hint)

        # Default to string for unknown types
        return SchemaNode("string"), 1


def json_schema(from_type: Any, *, use_md: bool = False, show_name: bool = True) -> Tuple[str, int]:
    """
    Convert a type hint or Pydantic model to a JSON schema representation and return its length.

    Args:
        from_type: The type to convert. Can be:
            - Primitive types (str, int, float, bool, None)
            - Pydantic models
            - Lists of supported types
            - Unions of supported types
            - Optional types
            - Literal types
            - Enum classes
        use_md: If True, wraps the output in markdown code block
        show_name: If True, shows Pydantic model names in comments

    Returns:
        A tuple containing:
        - The JSON schema representation as a string
        - The number of possible types (1 for primitive/models, 2+ for unions/optional)
    """
    schema_node, length = JsonSchemaGenerator.generate_schema(
        from_type, show_name)
    schema_str = JsonSchemaGenerator._format_schema(
        schema_node, show_name=show_name)
    if use_md:
        schema_str = f"```json\n{schema_str}\n```"
    return schema_str, length
