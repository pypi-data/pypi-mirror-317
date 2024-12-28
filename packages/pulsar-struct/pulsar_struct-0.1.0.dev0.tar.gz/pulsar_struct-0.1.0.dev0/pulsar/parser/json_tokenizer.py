# json_tokenizer.py

import logging
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional, Iterator, Tuple
import re

logger = logging.getLogger(__name__)


class TokenType(Enum):
    """
    Enumeration of possible JSON token types.

    Includes all standard JSON tokens plus additional types for preprocessing.
    """
    LEFT_BRACE = auto()    # {
    RIGHT_BRACE = auto()   # }
    LEFT_BRACKET = auto()  # [
    RIGHT_BRACKET = auto()  # ]
    COLON = auto()        # :
    COMMA = auto()        # ,
    STRING = auto()       # "..."
    NUMBER = auto()       # 123, 45.67
    BOOLEAN = auto()      # true, false
    NULL = auto()         # null
    IDENTIFIER = auto()   # unquoted string
    WHITESPACE = auto()   # spaces, tabs, newlines
    EOF = auto()          # end of input


@dataclass
class Token:
    """
    A class representing a token in the JSON text.

    Attributes:
        type (TokenType): The type of token
        value (str): The actual text value of the token
        start (int): Starting position in source text
        end (int): Ending position in source text
        depth (int): Nesting depth of the token
    """
    type: TokenType
    value: str
    start: int
    end: int
    depth: int = 0

    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}', pos={self.start}-{self.end}, depth={self.depth})"


class JSONTokenizer:
    """
    A tokenizer that converts JSON text into a sequence of tokens.

    Handles standard JSON syntax plus additional features like:
    - Unquoted strings
    - Comments
    - Special characters
    - Nested structures
    """

    def __init__(self):
        self.text = ""
        self.pos = 0
        self.depth = 0
        self.length = 0
        self.current_line = 1
        self.current_column = 1
        self._pending_tokens = []

    def _log_position(self, message: str):
        context = self.text[max(0, self.pos-10):min(self.length, self.pos+10)]
        logger.debug(
            f"{message} at line {self.current_line}, col {self.current_column}")
        logger.debug(f"Context: ...{context}...")

    def tokenize(self, text: str) -> List[Token]:
        """
        Convert input text into a list of tokens.

        Args:
            text (str): Input JSON text

        Returns:
            List[Token]: List of tokens representing the JSON structure
        """
        self.text = text
        self.pos = 0
        self.depth = 0
        self.length = len(text)
        self.current_line = 1
        self.current_column = 1
        self._pending_tokens = []

        tokens = []

        while self.pos < self.length:
            token = self._next_token()
            if token.type != TokenType.WHITESPACE:
                tokens.append(token)

        tokens.append(Token(TokenType.EOF, "", self.pos, self.pos, self.depth))
        return tokens

    def _next_token(self) -> Token:
        """
        Get the next token from the input text.

        Returns:
            Token: The next token in the sequence
        """
        if self._pending_tokens:
            return self._pending_tokens.pop(0)

        if self.pos >= self.length:
            return Token(TokenType.EOF, "", self.pos, self.pos, self.depth)

        char = self.text[self.pos]

        # Track position for error reporting
        if char == '\n':
            self.current_line += 1
            self.current_column = 1
        else:
            self.current_column += 1

        # Handle single-line comments - ADD THIS SECTION
        if char == '/' and self.pos + 1 < self.length and self.text[self.pos + 1] == '/':
            # Skip until end of line or end of input
            start = self.pos
            while self.pos < self.length and self.text[self.pos] != '\n':
                self.pos += 1
            return Token(TokenType.WHITESPACE, self.text[start:self.pos], start, self.pos, self.depth)

        # Handle whitespace
        if char.isspace():
            return self._consume_whitespace()

        # Check for arrow operator
        if char == '=' and self.pos + 1 < self.length and self.text[self.pos + 1] == '>':
            start = self.pos
            self.pos += 2
            return Token(TokenType.IDENTIFIER, '=>', start, self.pos, self.depth)

        # Handle parentheses as part of identifiers when they're part of type signatures
        if char == '(' and self._is_type_signature_context():
            return self._consume_identifier()

        # Handle standard JSON tokens
        if char == '{':
            self.depth += 1
            self.pos += 1
            return Token(TokenType.LEFT_BRACE, char, self.pos-1, self.pos, self.depth-1)
        elif char == '}':
            self.depth = max(0, self.depth - 1)
            self.pos += 1
            return Token(TokenType.RIGHT_BRACE, char, self.pos-1, self.pos, self.depth)
        elif char == '[':
            self.depth += 1
            self.pos += 1
            return Token(TokenType.LEFT_BRACKET, char, self.pos-1, self.pos, self.depth-1)
        elif char == ']':
            self.depth = max(0, self.depth - 1)
            self.pos += 1
            return Token(TokenType.RIGHT_BRACKET, char, self.pos-1, self.pos, self.depth)
        elif char == ':':
            self.pos += 1
            return Token(TokenType.COLON, char, self.pos-1, self.pos, self.depth)
        elif char == ',':
            self.pos += 1
            return Token(TokenType.COMMA, char, self.pos-1, self.pos, self.depth)

        # Handle strings - Add backtick here
        if char in '"\'`':  # Modified this line to include backtick
            return self._consume_string()

        # Handle numbers
        if char.isdigit() or char == '-' or char == '+':
            return self._consume_number()

        # Handle identifiers and keywords
        if char.isalpha() or char == '_' or char == '/':
            return self._consume_identifier()

        # Skip unexpected characters
        self._log_position(f"Unexpected character: {char}")
        self.pos += 1
        return self._next_token()

    def _is_type_signature_context(self) -> bool:
        """
        Check if current context is within a type signature.

        Returns:
            bool: True if currently parsing a type signature
        """
        # Look back for "onClick:" or similar identifiers
        prev_pos = self.pos - 1
        while prev_pos >= 0 and self.text[prev_pos].isspace():
            prev_pos -= 1

        # Look for a colon before the current position
        while prev_pos >= 0 and self.text[prev_pos] != ':':
            prev_pos -= 1

        if prev_pos >= 0:
            # Look for identifier before colon
            word_end = prev_pos
            prev_pos -= 1
            while prev_pos >= 0 and (self.text[prev_pos].isalnum() or self.text[prev_pos] == '_'):
                prev_pos -= 1
            return True

        return False

    def _consume_whitespace(self) -> Token:
        """
        Consume and return whitespace characters as a token.

        Returns:
            Token: A whitespace token
        """
        start = self.pos
        while self.pos < self.length and self.text[self.pos].isspace():
            self.pos += 1
        return Token(TokenType.WHITESPACE, self.text[start:self.pos], start, self.pos, self.depth)

    def _consume_string(self) -> Token:
        """
        Consume and return a string literal as a token.

        Handles single, double, and triple quoted strings.

        Returns:
            Token: A string token
        """
        start = self.pos
        quote_char = self.text[self.pos]

        # Check for triple quotes
        is_triple = (self.pos + 2 < self.length and
                     self.text[self.pos:self.pos + 3] in ('"""', "'''"))

        if quote_char in '"\'`':
            if is_triple:
                quote_sequence = self.text[self.pos:self.pos + 3]
                self.pos += 3
                while self.pos + 2 < self.length:
                    if self.text[self.pos:self.pos + 3] == quote_sequence:
                        self.pos += 3
                        # Get the content without the triple quotes
                        content = self.text[start+3:self.pos-3]
                        # Normalize newlines but don't escape them
                        content = content.replace(
                            '\r\n', '\n').replace('\r', '\n')
                        return Token(TokenType.STRING, f'"{content}"', start, self.pos, self.depth)
                    self.pos += 1
            else:
                self.pos += 1  # Move past opening quote
                escaped = False
                value_chars = []

                while self.pos < self.length:
                    char = self.text[self.pos]

                    if escaped:
                        if char == 'n':
                            # Convert \n to actual newline
                            value_chars.append('\n')
                        else:
                            value_chars.append(char)
                        escaped = False
                    elif char == '\\':
                        escaped = True
                    elif char == quote_char:
                        # Check if this quote is followed by more content
                        next_pos = self.pos + 1
                        if next_pos < self.length:
                            next_char = self.text[next_pos]
                            if next_char not in (':', ',', '}', ']', ' ', '\n', '\t', '\r'):
                                value_chars.append(char)
                                self.pos += 1
                                continue
                        # This is our closing quote
                        self.pos += 1
                        break
                    else:
                        value_chars.append(char)

                    self.pos += 1

                value = ''.join(value_chars)
                return Token(TokenType.STRING, f'"{value}"', start, self.pos, self.depth)

        # Return the entire string with quotes
        return Token(TokenType.STRING, self.text[start:self.pos], start, self.pos, self.depth)

    def _consume_number(self) -> Token:
        """
        Consume and return a numeric literal as a token.

        Handles integers, floats, and numbers with commas.

        Returns:
            Token: A number token
        """
        start = self.pos

        # Handle sign
        if self.text[self.pos] in '+-':
            self.pos += 1

        # Collect all parts of the number including commas
        number_parts = []
        while self.pos < self.length:
            char = self.text[self.pos]

            # Handle digits
            if char.isdigit():
                number_parts.append(char)
            # Handle decimal point
            elif char == '.':
                number_parts.append(char)
            # Handle commas between digits
            elif char == ',':
                # Only include comma if it's between digits and properly spaced
                if (self.pos > 0 and self.text[self.pos - 1].isdigit() and
                        self.pos + 1 < self.length and self.text[self.pos + 1].isdigit()):
                    number_parts.append(char)
                else:
                    break
            # Handle exponent
            elif char.lower() == 'e':
                number_parts.append(char)
                self.pos += 1
                if self.pos < self.length and self.text[self.pos] in '+-':
                    number_parts.append(self.text[self.pos])
                    self.pos += 1
                continue
            else:
                break
            self.pos += 1

        number_str = ''.join(number_parts)
        # Remove commas before returning
        clean_number = number_str.replace(',', '')

        return Token(TokenType.NUMBER,
                     self.text[start:self.pos],
                     start,
                     self.pos,
                     self.depth)

    def _consume_identifier(self) -> Token:
        """
        Consume and return an identifier as a token.

        Handles unquoted strings and keywords.

        Returns:
            Token: An identifier token
        """
        if self.text[self.pos] == '/' and self.pos + 1 < self.length and self.text[self.pos + 1] == '/':
            return self._next_token()
        start = self.pos
        brace_depth = 0
        paren_depth = 0
        angle_depth = 0

        # Track if we're in a special segment
        in_type_expr = False

        while self.pos < self.length:
            char = self.text[self.pos]

            # Once we start a parenthesis or type expression, capture everything until the matching end
            if char == '(':
                paren_depth += 1
                in_type_expr = True
            elif char == ')':
                paren_depth -= 1
            elif char == '{':
                brace_depth += 1
            elif char == '}':
                if brace_depth == 0:  # Top-level closing brace
                    break
                brace_depth -= 1
            elif char == '<':
                angle_depth += 1
                in_type_expr = True
            elif char == '>':
                angle_depth -= 1

            # Check for arrow operator
            if char == '=' and self.pos + 1 < self.length and self.text[self.pos + 1] == '>':
                in_type_expr = True
                self.pos += 2  # Skip both = and >
                continue

            # Only break on delimiters if we're not in a type expression and all depths are 0
            if not in_type_expr and brace_depth == 0 and paren_depth == 0 and angle_depth == 0:
                if char in '{}[],"\'\n' or char.isspace():
                    break

            self.pos += 1

        value = self.text[start:self.pos].strip()

        # Handle keywords
        if value.lower() == 'true' or value.lower() == 'false':
            return Token(TokenType.BOOLEAN, value.lower(), start, self.pos, self.depth)
        elif value.lower() == 'null':
            return Token(TokenType.NULL, value.lower(), start, self.pos, self.depth)

        return Token(TokenType.IDENTIFIER, value, start, self.pos, self.depth)


class TokenStream:
    """
    A stream interface for working with a sequence of tokens.

    Provides methods for traversing and inspecting tokens.
    """

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0

    def peek(self) -> Token:
        """
        Look at the next token without consuming it.

        Returns:
            Token: The next token in the stream
        """
        if self.position >= len(self.tokens):
            return self.tokens[-1]  # Return EOF token
        return self.tokens[self.position]

    def next(self) -> Token:
        """
        Get the next token and advance position.

        Returns:
            Token: The next token in the stream
        """
        token = self.peek()
        self.position += 1
        return token

    def backup(self):
        """
        Move back one token in the stream.
        """
        self.position = max(0, self.position - 1)

    def has_more(self) -> bool:
        """
        Check if there are more tokens in the stream.

        Returns:
            bool: True if more tokens are available
        """
        return self.position < len(self.tokens) - 1  # Exclude EOF token


if __name__ == "__main__":
    # Test the tokenizer
    tokenizer = JSONTokenizer()
    test_input = '''{
        key: "value",
        numbers: [1, 2.5, -3e4],
        boolean: true,
        null_value: null
    }'''

    tokens = tokenizer.tokenize(test_input)
    for token in tokens:
        print(token)
