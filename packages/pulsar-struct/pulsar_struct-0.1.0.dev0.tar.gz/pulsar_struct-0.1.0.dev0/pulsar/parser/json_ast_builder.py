# json_ast_builder.py

import logging
from dataclasses import dataclass
from enum import Enum, auto
import re
from typing import Any, Dict, List, Optional, Union
from .json_tokenizer import Token, TokenType, TokenStream


logger = logging.getLogger(__name__)


class ASTNodeType(Enum):
    """
    Enumeration of possible AST node types.

    Represents all possible JSON value types in the AST.
    """
    OBJECT = auto()
    ARRAY = auto()
    STRING = auto()
    NUMBER = auto()
    BOOLEAN = auto()
    NULL = auto()


@dataclass
class ASTNode:
    """
    A class representing a node in the Abstract Syntax Tree.

    Attributes:
        type (ASTNodeType): Type of the node
        value (Any): Value stored in the node
        depth (int): Nesting depth in the tree
        start (int): Starting position in source
        end (int): Ending position in source
        parent (Optional[ASTNode]): Parent node reference
    """
    type: ASTNodeType
    value: Any
    depth: int
    start: int
    end: int
    parent: Optional['ASTNode'] = None

    def __repr__(self):
        return f"ASTNode({self.type.name}, {self.value}, depth={self.depth})"


class JSONASTBuilder:
    """
    Builds an Abstract Syntax Tree from JSON tokens.

    Handles parsing of JSON structures and creation of the AST.
    """

    def __init__(self):
        self.stream: Optional[TokenStream] = None
        self.errors: List[str] = []

    def parse(self, tokens: List['Token']) -> ASTNode:
        """
        Parse tokens into an Abstract Syntax Tree.

        Args:
            tokens (List[Token]): List of tokens to parse

        Returns:
            ASTNode: Root node of the constructed AST
        """
        self.stream = TokenStream(tokens)
        self.errors = []

        # Handle empty input
        if not tokens or len(tokens) <= 1:  # Only EOF token
            return ASTNode(ASTNodeType.NULL, None, 0, 0, 0)

        first_token = self.stream.peek()

        if first_token.type == TokenType.LEFT_BRACE:
            return self._parse_object()
        elif first_token.type == TokenType.LEFT_BRACKET:
            return self._parse_array()
        else:
            return self._parse_value()

    def _is_numeric_with_commas(self, tokens: List['Token']) -> bool:
        """
        Check if tokens represent a number with commas.

        Args:
            tokens (List[Token]): Tokens to check

        Returns:
            bool: True if tokens form a valid number with commas
        """
        # Convert tokens to string, ignoring EOF
        value = ''.join(
            token.value for token in tokens if token.type != TokenType.EOF)
        # Check if it matches number with commas pattern
        return bool(re.match(r'^-?\d{1,3}(,\d{3})*(\.\d+)?$', value))

    def _parse_object(self) -> ASTNode:
        """
        Parse a JSON object from the token stream.

        Returns:
            ASTNode: Node representing the parsed object
        """
        start_token = self.stream.next()  # Consume {
        obj: Dict[str, Any] = {}
        depth = start_token.depth
        last_token = start_token
        current_key = None

        try:
            while self.stream.has_more():
                token = self.stream.peek()

                # End of object
                if token.type == TokenType.RIGHT_BRACE:
                    last_token = self.stream.next()
                    break

                # Parse key
                if token.type in (TokenType.STRING, TokenType.IDENTIFIER):
                    key_token = token
                    self.stream.next()

                    # Clean up key - remove quotes
                    current_key = key_token.value.strip()
                    if current_key.startswith('"') or current_key.startswith("'"):
                        current_key = current_key[1:]
                    if current_key.endswith('"') or current_key.endswith("'"):
                        current_key = current_key[:-1]
                    current_key = current_key.rstrip(':').strip()

                    # Look for colon
                    token = self.stream.peek()
                    if token.type == TokenType.COLON:
                        self.stream.next()

                    # Parse value or array
                    token = self.stream.peek()
                    if token.type == TokenType.LEFT_BRACKET:
                        # Parse array
                        array_node = self._parse_array()
                        obj[current_key] = array_node.value
                    else:
                        # Parse regular value
                        value_node = self._parse_value()
                        obj[current_key] = value_node.value

                    # Handle comma
                    token = self.stream.peek()
                    if token.type == TokenType.COMMA:
                        self.stream.next()

                    last_token = token
                else:
                    # Skip unexpected tokens
                    self.stream.next()

        except Exception as e:
            # If parsing fails and we're at EOF, return what we have so far
            if not self.stream.has_more():
                return ASTNode(ASTNodeType.OBJECT, obj, depth, start_token.start, last_token.end)
            raise

        return ASTNode(ASTNodeType.OBJECT, obj, depth, start_token.start, last_token.end)

    def _parse_array(self) -> ASTNode:
        """
        Parse a JSON array from the token stream.

        Returns:
            ASTNode: Node representing the parsed array
        """
        start_token = self.stream.next()  # Consume [
        array: List[Any] = []
        depth = start_token.depth
        last_token = start_token

        while self.stream.has_more():
            token = self.stream.peek()

            if token.type == TokenType.RIGHT_BRACKET:
                last_token = self.stream.next()
                break

            # Parse value
            if token.type == TokenType.LEFT_BRACE:
                # Try to parse as object first
                try:
                    obj_node = self._parse_object()
                    array.append(obj_node.value)
                except Exception:
                    # If parsing fails due to incomplete structure,
                    # collect tokens until end or next top-level token
                    value_tokens = []
                    while self.stream.has_more():
                        next_token = self.stream.peek()
                        if next_token.depth <= depth:
                            break
                        value_tokens.append(next_token.value)
                        self.stream.next()
                    # Try to parse collected tokens
                    if value_tokens:
                        try:
                            partial_obj = {}
                            current_key = None
                            for i, val in enumerate(value_tokens):
                                if val.startswith('"') and val.endswith('"'):
                                    if current_key is None:
                                        current_key = val.strip('"')
                                    else:
                                        partial_obj[current_key] = val.strip(
                                            '"')
                                        current_key = None
                                elif val == ':':
                                    continue
                                elif val == '{':
                                    continue
                                elif val.isdigit():
                                    if current_key:
                                        partial_obj[current_key] = int(val)
                                        current_key = None
                            if partial_obj:
                                array.append(partial_obj)
                        except:
                            pass
            else:
                value_node = self._parse_value()
                array.append(value_node.value)

            # Handle comma or space separator
            token = self.stream.peek()
            if token.type == TokenType.COMMA:
                self.stream.next()

            last_token = token

        return ASTNode(ASTNodeType.ARRAY, array, depth, start_token.start, last_token.end)

    def _parse_type_definition(self) -> ASTNode:
        """
        Parse a type definition or function signature.

        Returns:
            ASTNode: Node representing the parsed type definition
        """
        start_token = self.stream.peek()
        value_parts = []
        brace_depth = 0
        paren_depth = 0

        while self.stream.has_more():
            token = self.stream.peek()

            if token.type == TokenType.LEFT_BRACE:
                brace_depth += 1
            elif token.type == TokenType.RIGHT_BRACE:
                brace_depth -= 1
            elif token.type == TokenType.LEFT_BRACKET:
                paren_depth += 1
            elif token.type == TokenType.RIGHT_BRACKET:
                paren_depth -= 1

            value_parts.append(token.value)
            self.stream.next()

            if brace_depth == 0 and paren_depth == 0:
                if token.type in (TokenType.COMMA, TokenType.RIGHT_BRACE):
                    break

        value = ''.join(value_parts).strip()
        return ASTNode(ASTNodeType.STRING, value, start_token.depth,
                       start_token.start, self.stream.peek().end)

    def _peek_ahead(self, count: int) -> List[Token]:
        """
        Look ahead at upcoming tokens without consuming them.

        Args:
            count (int): Number of tokens to peek ahead

        Returns:
            List[Token]: List of upcoming tokens
        """
        tokens = []
        original_pos = self.stream.position

        for _ in range(count):
            if self.stream.has_more():
                tokens.append(self.stream.next())

        self.stream.position = original_pos
        return tokens

    def _strip_quotes(self, value: str) -> str:
        """
        Strip quotes from a string value.

        Args:
            value (str): String to process

        Returns:
            str: String with quotes removed
        """
        if value.startswith('"""') and value.endswith('"""'):
            return value[3:-3]
        if value.startswith("'''") and value.endswith("'''"):
            return value[3:-3]
        if (value.startswith('"') and value.endswith('"')) or \
                (value.startswith("'") and value.endswith("'")):
            return value[1:-1]
        return value

    def _parse_value(self) -> ASTNode:
        """
        Parse a JSON value from the token stream.

        Returns:
            ASTNode: Node representing the parsed value
        """
        token = self.stream.peek()

        if token.type == TokenType.IDENTIFIER:
            value = token.value
            self.stream.next()

            # Track nested type definition brackets
            angle_depth = 0
            array_depth = 0

            while self.stream.has_more():
                next_token = self.stream.peek()
                if next_token.type in (TokenType.COMMA, TokenType.RIGHT_BRACE) and angle_depth == 0 and array_depth == 0:
                    break
                if next_token.depth != token.depth:
                    break

                # Track type definition nesting
                if '<' in value:
                    angle_depth += 1

                # Consume closing angle bracket even if next token is comma/brace
                if angle_depth > 0 and next_token.value == '>':
                    value += next_token.value
                    self.stream.next()
                    angle_depth -= 1
                    continue

                if next_token.value.startswith('['):
                    array_depth += 1
                elif next_token.value.startswith(']'):
                    array_depth -= 1

                # Only add space for normal identifiers
                if not any(c in next_token.value[0] for c in '[]<>'):
                    value += ' '
                value += next_token.value
                self.stream.next()

            return ASTNode(ASTNodeType.STRING, value, token.depth, token.start, self.stream.peek().end)

        if token.type == TokenType.LEFT_BRACE:
            # For partial nested objects, try to parse remaining tokens
            if not self.stream.has_more():
                # Get tokens collected so far for the object
                current_obj = {}
                current_key = None
                value = None

                while self.stream.position > 0:
                    self.stream.backup()
                    prev_token = self.stream.peek()

                    if prev_token.type == TokenType.NUMBER:
                        value = float(prev_token.value)
                    elif prev_token.type == TokenType.STRING:
                        if current_key is None:
                            current_key = prev_token.value.strip('"\'')
                            if value is not None:
                                current_obj[current_key] = value
                                value = None
                                current_key = None

                # Move position back to end
                while self.stream.has_more():
                    self.stream.next()

                if current_obj:
                    return ASTNode(ASTNodeType.OBJECT, current_obj, token.depth,
                                   token.start, token.end)

            return self._parse_object()
        elif token.type == TokenType.LEFT_BRACKET:
            return self._parse_array()
        elif token.type == TokenType.STRING:
            self.stream.next()
            # Use new _strip_quotes method instead of manual quote stripping
            value = self._strip_quotes(token.value)
            # Handle escape sequences
            value = value.replace('\\"', '"').replace("\\'", "'")
            return ASTNode(ASTNodeType.STRING, value, token.depth,
                           token.start, token.end)
        elif token.type == TokenType.NUMBER:
            # Look ahead for comma-separated number parts
            number_tokens = [token]
            self.stream.next()

            # Try to parse the number value, handling commas
            try:
                # Remove commas and convert to float/int
                clean_number = token.value.replace(',', '')
                if '.' in clean_number:
                    value = float(clean_number)
                else:
                    value = int(clean_number)
            except ValueError:
                value = 0

            return ASTNode(ASTNodeType.NUMBER, value, token.depth, token.start, token.end)
        elif token.type == TokenType.BOOLEAN:
            self.stream.next()
            return ASTNode(ASTNodeType.BOOLEAN, token.value == 'true', token.depth,
                           token.start, token.end)
        elif token.type == TokenType.NULL:
            self.stream.next()
            return ASTNode(ASTNodeType.NULL, None, token.depth, token.start, token.end)
        elif token.type == TokenType.IDENTIFIER:
            value = token.value.strip()
            self.stream.next()

            # Handle multi-line values by collecting subsequent tokens
            if self.stream.has_more():
                next_token = self.stream.peek()
                value_parts = [value]

                while (next_token.type == TokenType.IDENTIFIER and
                       next_token.depth == token.depth and
                       next_token.type not in (TokenType.RIGHT_BRACE, TokenType.COMMA)):
                    value_parts.append(next_token.value.strip())
                    self.stream.next()
                    if not self.stream.has_more():
                        break
                    next_token = self.stream.peek()

                value = ' '.join(part for part in value_parts if part)

            # Clean up value - remove quotes
            if value.startswith('"') or value.startswith("'"):
                value = value[1:]
            if value.endswith('"') or value.endswith("'"):
                value = value[:-1]

            # Handle array-like values
            if '[' in value and ']' in value:
                try:
                    array_part = value[value.index('['):value.index(']')+1]
                    values = [v.strip() for v in array_part[1:-1].split()]
                    array = []
                    for v in values:
                        try:
                            if '.' in v:
                                array.append(float(v))
                            else:
                                array.append(int(v))
                        except ValueError:
                            array.append(v)
                    return ASTNode(ASTNodeType.ARRAY, array, token.depth,
                                   token.start, token.end)
                except Exception:
                    pass

            return ASTNode(ASTNodeType.STRING, value, token.depth,
                           token.start, token.end)
        else:
            self.stream.next()  # Skip invalid token
            return ASTNode(ASTNodeType.NULL, None, token.depth, token.start, token.end)

    def _parse_key(self) -> str:
        """
        Parse an object key from the token stream.

        Returns:
            str: Parsed key string
        """
        token = self.stream.next()
        if token.type == TokenType.STRING:
            return token.value.strip('"\'')
        return token.value


class JSONSerializer:
    """
    Serializes AST nodes back into JSON text format.
    """
    @staticmethod
    def to_json(node: ASTNode, indent: int = 0) -> str:
        """
        Convert an AST node to JSON string representation.

        Args:
            node (ASTNode): Node to serialize
            indent (int): Indentation level

        Returns:
            str: JSON string representation
        """
        if node.type == ASTNodeType.OBJECT:
            if not node.value:
                return "{}"
            items = []
            for key, value in node.value.items():
                value_node = value if isinstance(value, ASTNode) else \
                    ASTNode(JSONSerializer._detect_type(
                        value), value, node.depth + 1, 0, 0)
                formatted_value = JSONSerializer.to_json(
                    value_node, indent + 2)
                items.append(f'"{key}": {formatted_value}')
            if indent:
                return "{\n" + " " * indent + \
                       (",\n" + " " * indent).join(items) + \
                       "\n" + " " * (indent - 2) + "}"
            return "{" + ", ".join(items) + "}"

        elif node.type == ASTNodeType.ARRAY:
            if not node.value:
                return "[]"
            items = []
            for item in node.value:
                item_node = item if isinstance(item, ASTNode) else \
                    ASTNode(JSONSerializer._detect_type(
                        item), item, node.depth + 1, 0, 0)
                items.append(JSONSerializer.to_json(item_node, indent + 2))
            if indent:
                return "[\n" + " " * indent + \
                       (",\n" + " " * indent).join(items) + \
                       "\n" + " " * (indent - 2) + "]"
            return "[" + ", ".join(items) + "]"

        elif node.type == ASTNodeType.STRING:
            return f'"{node.value}"'
        elif node.type == ASTNodeType.NUMBER:
            return str(node.value)
        elif node.type == ASTNodeType.BOOLEAN:
            return str(node.value).lower()
        elif node.type == ASTNodeType.NULL:
            return "null"

    @staticmethod
    def _detect_type(value: Any) -> ASTNodeType:
        """
        Detect the AST node type for a given value.

        Args:
            value (Any): Value to analyze

        Returns:
            ASTNodeType: Detected node type
        """
        if value is None:
            return ASTNodeType.NULL
        elif isinstance(value, bool):
            return ASTNodeType.BOOLEAN
        elif isinstance(value, (int, float)):
            return ASTNodeType.NUMBER
        elif isinstance(value, str):
            return ASTNodeType.STRING
        elif isinstance(value, list):
            return ASTNodeType.ARRAY
        elif isinstance(value, dict):
            return ASTNodeType.OBJECT
        return ASTNodeType.STRING


if __name__ == "__main__":
    from json_tokenizer import JSONTokenizer
    # Test input with various issues to fix
    test_input = '''{
        unquoted_key: "value",
        "numbers": [1 2.5 -3e4],
        "object": {
            nested_key: nested value,
            missing_comma
            incomplete_array: [1, 2, 3
        }
    }'''

    # Process the input
    tokenizer = JSONTokenizer()
    tokens = tokenizer.tokenize(test_input)

    ast_builder = JSONASTBuilder()
    ast = ast_builder.parse(tokens)

    # Serialize back to JSON
    result = JSONSerializer.to_json(ast, indent=2)
    print("Tokens:")
    print(tokens)
    print("\nAST:")
    print(ast)
    print("\nFixed JSON:")
    print(result)
