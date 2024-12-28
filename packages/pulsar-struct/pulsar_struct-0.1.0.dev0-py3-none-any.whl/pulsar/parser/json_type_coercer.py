# json_type_coercer.py

from enum import Enum
from typing import ForwardRef, Any, Dict, List, Optional, Union, Type, TypeVar, get_args, get_origin, Literal
from pydantic import BaseModel
import logging
from dataclasses import dataclass
from .json_preprocessor import JSONPreprocessor
from .json_tokenizer import JSONTokenizer
from .json_ast_builder import JSONASTBuilder
import re

logger = logging.getLogger(__name__)

T = TypeVar('T')


@dataclass
class TypeCoercionContext:
    """
    Context for type coercion operations.

    Tracks path and settings during coercion process.

    Attributes:
        path (List[str]): Current path in object structure
        allow_partial (bool): Whether to allow partial data
        type_namespace (Dict[str, Type]): Namespace for type resolution
    """
    path: List[str]
    allow_partial: bool = False
    type_namespace: Dict[str, Type] = None

    def __post_init__(self):
        if self.type_namespace is None:
            self.type_namespace = {}

    def enter(self, key: str) -> 'TypeCoercionContext':
        """Create a new context for nested coercion"""
        return TypeCoercionContext(
            path=self.path + [key],
            allow_partial=self.allow_partial,
            type_namespace=self.type_namespace
        )

    @property
    def current_path(self) -> str:
        return '.'.join(self.path)


class TypeCoercer:
    """
    Handles coercion of parsed JSON data into typed Python objects.

    Supports:
    - Primitive types
    - Enums
    - Pydantic models
    - Lists and Unions
    - Optional fields
    """

    def coerce(self, value: Any, target_type: Type[T], context: Optional[TypeCoercionContext] = None) -> T:
        """
        Coerce a value to a target type.

        Args:
            value (Any): Value to coerce
            target_type (Type[T]): Target type
            context (Optional[TypeCoercionContext]): Coercion context

        Returns:
            T: Coerced value of target type
        """
        context = context or TypeCoercionContext(path=[])

        if context.allow_partial:
            # For BaseModel types, provide empty lists for missing required fields
            if self._is_pydantic_model(target_type):
                if isinstance(value, dict):
                    for field_name, field_type in target_type.__annotations__.items():
                        if field_name not in value:
                            # Initialize missing fields with empty lists if they're List types
                            if get_origin(field_type) in (list, List):
                                value[field_name] = []
        logger.debug(
            f"Coercing value {value} to {target_type} at path {context.current_path}")

        # Handle forward references
        if isinstance(target_type, ForwardRef):
            target_type = self._resolve_forward_ref(target_type, context)

        if target_type is None:
            return None

        # Special handling for NoneType
        if target_type is type(None):
            if value is None or (isinstance(value, str) and value.lower() == 'null'):
                return None
            raise ValueError(
                f"Cannot coerce {value} to NoneType at {context.current_path}")

        # if target_type == str and value is None:
        #     return ""

        # Handle None/null values
        if value is None or (isinstance(value, str) and value.lower() == 'null'):
            if self._is_optional(target_type):
                return None
            if context.allow_partial:
                return None
            if target_type == str:
                return ""
            raise ValueError(
                f"Non-optional value is None at {context.current_path}")

        # Get base type if Optional
        base_type = self._get_base_type(target_type)

        # Handle Union types
        if self._is_union(base_type):
            return self._coerce_union(value, base_type, context)

        # Handle Lists
        if self._is_list(base_type):
            return self._coerce_list(value, base_type, context)

        # Handle Enums
        if self._is_enum(base_type):
            if isinstance(value, list):
                for v in value:
                    try:
                        return self._coerce_enum(v, base_type, context)
                    except:
                        pass
            return self._coerce_enum(value, base_type, context)

        # Handle Pydantic models
        if self._is_pydantic_model(base_type):
            # Update type namespace with the model
            context.type_namespace[base_type.__name__] = base_type
            return self._coerce_model(value, base_type, context)

        # Handle primitive types
        return self._coerce_primitive(value, base_type, context)

    def _resolve_forward_ref(self, ref: ForwardRef, context: TypeCoercionContext) -> Optional[Type]:
        """
        Resolve a ForwardRef using the context's type namespace.

        Args:
            ref (ForwardRef): Forward reference to resolve
            context (TypeCoercionContext): Current context

        Returns:
            Optional[Type]: Resolved type or None
        """
        ref_name = ref.__forward_arg__

        if ref_name in context.type_namespace:
            return context.type_namespace[ref_name]

        # Handle Optional[ForwardRef]
        if ref_name.startswith("Optional[") and ref_name.endswith("]"):
            inner_name = ref_name[9:-1]
            if inner_name in context.type_namespace:
                return Optional[context.type_namespace[inner_name]]

        return None

    def _is_optional(self, type_: Type) -> bool:
        """Check if type is Optional[...]"""
        return (
            get_origin(type_) is Union and
            type(None) in get_args(type_)
        )

    def _get_base_type(self, type_: Type) -> Type:
        """Get base type from Optional"""
        if self._is_optional(type_):
            args = get_args(type_)
            return next(arg for arg in args if arg is not type(None))
        return type_

    def _is_union(self, type_: Type) -> bool:
        """Check if type is Union[...]"""
        return (
            get_origin(type_) is Union and
            not self._is_optional(type_)
        )

    def _is_list(self, type_: Type) -> bool:
        """Check if type is List[...]"""
        return get_origin(type_) in (list, List)

    def _is_enum(self, type_: Type) -> bool:
        """Check if type is an Enum"""
        return isinstance(type_, type) and issubclass(type_, Enum)

    def _is_pydantic_model(self, type_: Type) -> bool:
        """Check if type is a Pydantic model"""
        return isinstance(type_, type) and issubclass(type_, BaseModel)

    def _coerce_union(self, value: Any, union_type: Type, context: TypeCoercionContext) -> Any:
        """Try to coerce value to one of the union types"""
        args = get_args(union_type)
        errors = []

        for arg_type in args:
            try:
                return self.coerce(value, arg_type, context)
            except Exception as e:
                errors.append((arg_type, str(e)))

        error_msg = "\n".join(f"- {t}: {e}" for t, e in errors)
        raise ValueError(
            f"Could not coerce to any union type at {context.current_path}:\n{error_msg}")

    def _coerce_list(self, value: Any, list_type: Type, context: TypeCoercionContext) -> List:
        """Coerce value to a list of the specified element type"""
        if not isinstance(value, list):
            value = [value]

        element_type = get_args(list_type)[0]
        result = []

        for i, item in enumerate(value):
            item_context = context.enter(f"[{i}]")
            try:
                coerced = self.coerce(item, element_type, item_context)
                result.append(coerced)
            except Exception as e:
                if context.allow_partial:
                    # Don't skip valid items when validation fails
                    # Instead check if we have basic required fields
                    if isinstance(item, dict):
                        try:
                            # For Pydantic models, try to create with partial data
                            if self._is_pydantic_model(element_type):
                                # Get required fields from model
                                required_fields = {
                                    name: field for name, field in element_type.model_fields.items()
                                    if field.is_required()
                                }
                                # Check if we have all required fields
                                has_required = all(
                                    rf in item for rf in required_fields)
                                if has_required:
                                    # Create model with available data
                                    coerced = element_type(**item)
                                    result.append(coerced)
                                    continue
                        except:
                            pass
                if not context.allow_partial:
                    raise ValueError(
                        f"Invalid list item at {item_context.current_path}: {str(e)}")
                logger.debug(
                    f"Skipping invalid list item at {item_context.current_path}: {e}")

        return result

    def _extract_enum_value(self, text: str, enum_type: Type[Enum]) -> str:
        """Extract potential enum value from text"""
        # Get all possible enum values for matching
        enum_values = [e.name for e in enum_type]

        # First try exact matches (case-insensitive)
        text_upper = text.upper()
        for enum_val in enum_values:
            if text_upper == enum_val.upper():
                return enum_val

        # Try splitting on common delimiters
        for delimiter in [':', '.', ' is ', ' = ', '-']:
            if delimiter in text:
                parts = text.split(delimiter)
                # Try both first and last part (handles both prefix and postfix cases)
                for part in [parts[0], parts[-1]]:
                    part = part.strip()
                    part_upper = part.upper()
                    for enum_val in enum_values:
                        if part_upper == enum_val.upper():
                            return enum_val

        # Try finding enum values within the text
        text_upper = text.upper()
        for enum_val in enum_values:
            enum_upper = enum_val.upper()
            # Match whole words only
            for match in re.finditer(r'\b' + re.escape(enum_upper) + r'\b', text_upper):
                return enum_val

        # If no match found, return original text
        return text

    def _coerce_enum(self, value: Any, enum_type: Type[Enum], context: TypeCoercionContext) -> Enum:
        """Coerce value to an enum"""
        if isinstance(value, enum_type):
            return value

        try:
            # Try direct conversion first
            return enum_type(value)
        except ValueError:
            if isinstance(value, str):
                # Extract enum value from text
                extracted_value = self._extract_enum_value(value, enum_type)
                try:
                    return enum_type(extracted_value)
                except ValueError:
                    # If extraction failed, try case-insensitive match on original value
                    upper_value = value.upper()
                    for enum_value in enum_type:
                        if enum_value.name.upper() == upper_value:
                            return enum_value

            raise ValueError(
                f"Invalid enum value '{value}' for {enum_type.__name__} at {context.current_path}")

    def _coerce_model(self, value: Any, model_type: Type[BaseModel], context: TypeCoercionContext) -> BaseModel:
        """Coerce value to a Pydantic model"""
        if not isinstance(value, dict):
            if isinstance(value, str):
                value = value.strip()
                if not (value.startswith('{') and value.endswith('}')):
                    raise ValueError(
                        f"String value must be a JSON object at {context.current_path}")
                try:
                    import json
                    value = json.loads(value)
                except:
                    raise ValueError(
                        f"Invalid JSON object at {context.current_path}")
            else:
                raise ValueError(
                    f"Expected dict for {model_type.__name__}, got {type(value)} at {context.current_path}")

        # Additional validation for empty or invalid dicts
        if (not value or all(not k for k in value.keys())) and context.type_namespace.get('List') is not None:
            raise ValueError(
                f"Empty or invalid object for {model_type.__name__} at {context.current_path}")

        # Get model fields info
        fields = {
            name: field.annotation
            for name, field in model_type.model_fields.items()
        }
        coerced_data = {}

        for field_name, field_type in fields.items():
            field_context = context.enter(field_name)

            # Handle forward references
            if isinstance(field_type, ForwardRef):
                field_type = self._resolve_forward_ref(field_type, context)
                if field_type is None:
                    raise ValueError(
                        f"Could not resolve forward reference for field '{field_name}' at {context.current_path}")

            if field_name in value:
                field_value = value[field_name]

                # Special handling for Union types
                origin = get_origin(field_type)
                if origin is Union:
                    success = False
                    errors = []
                    # Optional => Union[T, None]
                    # Reversed to handle the None value first
                    for arg_type in reversed(get_args(field_type)):
                        try:
                            coerced_data[field_name] = self.coerce(
                                field_value, arg_type, field_context)
                            success = True
                            break
                        except Exception as e:
                            errors.append((arg_type, str(e)))
                    if not success:
                        error_msg = "\n".join(f"- {t}: {e}" for t, e in errors)
                        raise ValueError(
                            f"Could not coerce field to any union type at {field_context.current_path}:\n{error_msg}")
                    continue

                # Special handling for nested models
                if (isinstance(field_value, dict) and
                    isinstance(field_type, type) and
                        issubclass(field_type, BaseModel)):
                    try:
                        coerced_data[field_name] = self._coerce_model(
                            field_value, field_type, field_context)
                        continue
                    except Exception as e:
                        if not context.allow_partial:
                            raise ValueError(
                                f"Error coercing nested model at {field_context.current_path}: {str(e)}")

                try:
                    coerced_data[field_name] = self.coerce(
                        field_value, field_type, field_context)
                except Exception as e:
                    if not context.allow_partial:
                        raise ValueError(
                            f"Error coercing field at {field_context.current_path}: {str(e)}")
            elif not self._is_optional(field_type) and not context.allow_partial:
                raise ValueError(
                    f"Missing required field '{field_name}' at {context.current_path}")

        # Create model instance
        try:
            return model_type(**coerced_data)
        except Exception as e:
            raise ValueError(
                f"Error creating {model_type.__name__} at {context.current_path}: {str(e)}")

    def _extract_literal_value(self, text: str, literal_values: tuple) -> str:
        """Extract potential literal value from text using similar logic to enum extraction"""
        # Convert all to strings for comparison
        str_literals = [str(lit) for lit in literal_values]

        # First try exact match (case-insensitive)
        text_upper = text.upper()
        for lit in str_literals:
            if text_upper == lit.upper():
                return lit

        # Try splitting on common delimiters
        for delimiter in [':', '.', ' is ', ' = ', '-']:
            if delimiter in text:
                parts = text.split(delimiter)
                # Try both first and last part
                for part in [parts[0], parts[-1]]:
                    part = part.strip()
                    part_upper = part.upper()
                    for lit in str_literals:
                        if part_upper == lit.upper():
                            return lit

        # Try finding literal values within the text
        text_upper = text.upper()
        for lit in str_literals:
            lit_upper = lit.upper()
            # Match whole words only
            for match in re.finditer(r'\b' + re.escape(lit_upper) + r'\b', text_upper):
                return lit

        # If no match found, return original text
        return text

    def _coerce_primitive(self, value: Any, target_type: Type, context: TypeCoercionContext) -> Any:
        """Coerce value to a primitive type"""
        # Add handling for Union types at primitive level
        origin = get_origin(target_type)
        if origin is Union:
            args = get_args(target_type)
            errors = []
            for arg_type in args:
                try:
                    return self._coerce_primitive(value, arg_type, context)
                except Exception as e:
                    errors.append((arg_type, str(e)))
            error_msg = "\n".join(f"- {t}: {e}" for t, e in errors)
            raise ValueError(
                f"Could not coerce to any union type at {context.current_path}:\n{error_msg}")

        # Add Dict handling here
        if origin in (dict, Dict):
            if isinstance(value, str) and value.strip().startswith('{') and value.strip().endswith('}'):
                try:
                    # Try to parse the string as JSON
                    import json
                    parsed_value = json.loads(value)
                    if isinstance(parsed_value, dict):
                        # Get the key and value types from Dict generics
                        key_type, value_type = get_args(target_type)
                        # Convert the parsed dictionary keys and values to the correct types
                        return {
                            self._coerce_primitive(k, key_type, context):
                            self._coerce_primitive(v, value_type, context)
                            for k, v in parsed_value.items()
                        }
                except:
                    # If JSON parsing fails, continue with normal string handling
                    pass

        if target_type == str:
            # Convert dict to string if target is string
            if isinstance(value, dict):
                # Reconstruct object notation
                parts = []
                for k, v in value.items():
                    parts.append(f"{k}: {v}")
                return "{" + ", ".join(parts) + "}"
            return str(value)

        # Handle Literal types with enhanced matching
        if hasattr(target_type, "__origin__") and target_type.__origin__ is Literal:
            literal_values = target_type.__args__

            # Direct match check
            if value in literal_values:
                return value

            # String handling with smart extraction
            if isinstance(value, str):
                value = value.strip()
                # Try to extract literal value from text
                extracted = self._extract_literal_value(value, literal_values)

                # Check if extracted value matches any literal
                for lit in literal_values:
                    # Case-insensitive comparison for strings
                    if isinstance(lit, str) and isinstance(extracted, str):
                        if extracted.upper() == lit.upper():
                            return lit
                    # Direct comparison for non-string literals
                    elif extracted == lit:
                        return lit

                # Handle special case where literal value is embedded in text
                value_upper = value.upper()
                for lit in literal_values:
                    if isinstance(lit, str) and lit.upper() in value_upper:
                        return lit

            raise ValueError(
                f"Value '{value}' is not one of the allowed literal values {literal_values} at {context.current_path}")

        if isinstance(value, target_type):
            return value

        try:
            if target_type == bool:
                if isinstance(value, str):
                    return value.lower() in ('true', 'yes', '1', 'on')
                return bool(value)

            if target_type in (int, float):
                if isinstance(value, str):
                    # Check if the string contains non-numeric characters (except for common suffixes)
                    clean_value = value.lower().strip()
                    for suffix in ['k', 'm', 'b']:
                        if clean_value.endswith(suffix):
                            clean_value = clean_value[:-1]
                            break
                    if not clean_value.replace(',', '').replace('.', '').replace('-', '').replace('e', '').isdigit():
                        raise ValueError(
                            f"String contains non-numeric characters: {value}")

                    # Remove any commas from the string
                    value = value.replace(',', '')

                    # Handle common suffixes
                    multipliers = {
                        'k': 1_000,
                        'm': 1_000_000,
                        'b': 1_000_000_000,
                    }

                    value = value.lower().strip()
                    for suffix, multiplier in multipliers.items():
                        if value.endswith(suffix):
                            value = float(value[:-1]) * multiplier
                            break

                # Convert to float first to handle scientific notation
                float_val = float(value)
                if target_type == int:
                    return int(float_val)
                return float_val

            if target_type == str:
                if isinstance(value, (int, float, bool)):
                    return str(value)
                if value is None:
                    return ''
                return str(value)

            raise ValueError(f"Unsupported primitive type {target_type}")

        except Exception as e:
            if target_type in (int, float) and isinstance(value, str):
                # If conversion to number fails and the value is a string,
                # indicate in the error message that it's not a valid number
                raise ValueError(f"String '{value}' is not a valid number")
            raise ValueError(
                f"Could not coerce '{value}' to {target_type.__name__} at {context.current_path}: {str(e)}")


def _try_parse(json_obj: List, target_type: Type[T], allow_partial: bool = False) -> T:
    """Main parsing function that combines all stages"""
    # Stage 2: Tokenize
    logger.debug(f"PREPROCESSED: {json_obj}")
    tokenizer = JSONTokenizer()
    tokens = tokenizer.tokenize(json_obj)
    logger.debug(f"Tokenizer tokens: {tokens}")

    # Stage 3: Build AST
    ast_builder = JSONASTBuilder()
    ast = ast_builder.parse(tokens)
    logger.debug(f"AST: {ast}")

    # Stage 4: Type Coercion
    coercer = TypeCoercer()

    # Create context with type namespace for forward refs
    context = TypeCoercionContext(
        path=[],
        allow_partial=allow_partial,
        type_namespace={}
    )

    # Add target type and any nested types to namespace
    def add_to_namespace(t):
        if hasattr(t, '__name__'):
            context.type_namespace[t.__name__] = t
        if hasattr(t, '__annotations__'):
            for field_type in t.__annotations__.values():
                if isinstance(field_type, type):
                    add_to_namespace(field_type)

    add_to_namespace(target_type)

    # For non-list target types, ensure we're not passing a list value
    if get_origin(target_type) not in (list, List) and isinstance(ast.value, list):
        if ast.value and len(ast.value) == 1:
            ast.value = ast.value[0]
    result = coercer.coerce(ast.value, target_type, context)
    return result


def parse(text: str, target_type: Type[T], allow_partial: bool = False) -> T:
    """Main parsing function that combines all stages"""

    # Stage 1: Preprocess
    preprocessor = JSONPreprocessor()
    cleaned_text = preprocessor.preprocess(
        text, allow_partial)  # Added allow_partial here

    # Handle case where we got multiple JSON objects
    if isinstance(cleaned_text, list):
        # If target type is a list, parse all objects
        if get_origin(target_type) in (list, List):
            item_type = get_args(target_type)[0]
            results = []
            for json_obj in cleaned_text:
                # Process each JSON object
                logger.debug(f"PREPROCESSED: {json_obj}")
                tokens = JSONTokenizer().tokenize(json_obj)
                logger.debug(f"Tokenizer tokens: {tokens}")
                ast = JSONASTBuilder().parse(tokens)
                logger.debug(f"AST: {ast}")
                coercer = TypeCoercer()
                context = TypeCoercionContext(
                    path=[], allow_partial=allow_partial)
                results.append(coercer.coerce(ast.value, item_type, context))
            return results
        else:
            # If target type is not a list, use the first valid object
            for json_obj in cleaned_text:
                try:
                    return _try_parse(json_obj=json_obj, target_type=target_type, allow_partial=allow_partial)
                except:
                    pass
            raise ValueError(
                f"Could not parse any of {len(cleaned_text)} blocks")
    else:
        json_obj = cleaned_text

    return _try_parse(json_obj=json_obj, target_type=target_type, allow_partial=allow_partial)


if __name__ == "__main__":
    from enum import Enum
    from typing import List, Optional
    from pydantic import BaseModel

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

    # Test input
    test_input = '''
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

    result = parse(test_input, City)
    print(result)
