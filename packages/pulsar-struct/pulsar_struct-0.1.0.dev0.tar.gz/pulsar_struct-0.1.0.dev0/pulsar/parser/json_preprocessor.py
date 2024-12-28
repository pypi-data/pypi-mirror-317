# json_preprocessor.py

import re
import logging
from typing import Optional, Union, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Candidate:
    """
    A class representing a potential JSON data candidate with an associated score.

    Attributes:
        text (str): The text content of the candidate
        score (float): The candidate's score, indicating its validity as JSON data
    """
    text: str
    score: float = 0.0

    def __repr__(self):
        return f"Candidate(score={self.score}, text='{self.text[:50]}...')" if len(self.text) > 50 else f"Candidate(score={self.score}, text='{self.text}')"


class JSONPreprocessor:
    """
    A class for preprocessing and cleaning JSON-like text data before parsing.

    The preprocessor handles various tasks including:
    - Removing comments
    - Extracting JSON content from markdown blocks
    - Handling multiple JSON candidates
    - Fixing common formatting issues
    """

    def __init__(self):
        self.json_pattern = self._build_json_pattern()

    def _build_json_pattern(self) -> str:
        """
        Build a regex pattern for matching balanced JSON objects.

        Returns:
            str: A regular expression pattern that matches JSON object structures
        """
        quoted_string = r'"(?:[^"\\]|\\.)*"'
        # Add angle brackets to value pattern for type definitions
        value = rf'(?:{quoted_string}|[0-9]+(?:\.[0-9]*)?|true|false|null|""".*?"""|<.*?>)'
        key_value = rf'\s*{quoted_string}\s*:\s*{value}'
        object_start = r'\{'
        object_end = r'\}'
        array_pattern = r'\[.*?\]'
        return rf'{object_start}(?:[^{{}}]|{key_value}|{array_pattern})*{object_end}'

    def extract_content_blocks(self, text: str) -> List[str]:
        """
        Extract JSON content blocks from input text, prioritizing JSON structure.

        Args:
            text (str): Input text containing one or more JSON blocks

        Returns:
            List[str]: List of extracted JSON content blocks
        """
        logger.debug("Extracting content blocks")

        # Check if the text is already a valid JSON array structure
        text = text.strip()
        if text.startswith('['):
            logger.debug("Found potential JSON array structure")
            # For partial/incomplete arrays, extract individual objects
            array_content = text[1:]  # Remove leading [
            depth = 0
            object_start = -1
            objects = []
            current_object = []

            for i, char in enumerate(array_content):
                if char == '{':
                    if depth == 0:
                        object_start = i
                    depth += 1
                    current_object.append(char)
                elif char == '}':
                    depth -= 1
                    current_object.append(char)
                    if depth == 0:
                        objects.append(''.join(current_object))
                        current_object = []
                        object_start = -1
                elif object_start != -1:
                    current_object.append(char)

            # Handle any remaining partial object
            if current_object and '{' in ''.join(current_object):
                objects.append(''.join(current_object))

            if objects:
                logger.debug(f"Found {len(objects)} objects in array")
                return objects

        # Extract individual objects (original code)
        blocks = []
        current_pos = 0
        text_length = len(text)
        depth = 0
        current_block = []
        block_start = -1

        while current_pos < text_length:
            char = text[current_pos]

            if char == '{':
                if depth == 0:
                    block_start = current_pos
                depth += 1
                current_block.append(char)
            elif char == '}':
                depth -= 1
                current_block.append(char)
                if depth == 0 and current_block:
                    blocks.append(''.join(current_block))
                    current_block = []
            elif depth > 0:
                current_block.append(char)

            current_pos += 1

        # Handle remaining partial block
        if current_block and '{' in ''.join(current_block):
            blocks.append(''.join(current_block))

        if blocks:
            logger.debug(f"Found {len(blocks)} JSON blocks")
            return blocks

        # Try markdown blocks if no JSON found
        markdown_pattern = r'```(?:json)?\s*([\s\S]*?)```'
        markdown_blocks = re.findall(markdown_pattern, text)
        if markdown_blocks:
            logger.debug(f"Found {len(markdown_blocks)} markdown blocks")
            # For each markdown block, recursively process to handle arrays
            processed_blocks = []
            for block in markdown_blocks:
                if block.strip().startswith('['):
                    processed_blocks.extend(self.extract_content_blocks(block))
                else:
                    processed_blocks.append(block)
            return processed_blocks

        logger.debug("No JSON content found, returning original text")
        return [text]

    def _split_json_objects(self, text: str) -> List[str]:
        """
        Split a string containing multiple JSON objects into individual objects.

        Args:
            text (str): Input text containing multiple JSON objects

        Returns:
            List[str]: List of individual JSON object strings
        """
        objects = []
        current_pos = 0
        text_length = len(text)
        depth = 0
        array_depth = 0
        current_block = []

        while current_pos < text_length:
            char = text[current_pos]

            # Handle array nesting
            if char == '[':
                if depth == 0:
                    array_depth += 1
                    if array_depth == 1:  # Only append for top-level array
                        current_block = []
                current_block.append(char)
                depth += 1
            elif char == ']':
                depth -= 1
                current_block.append(char)
                if depth == 0 and array_depth > 0:
                    array_depth -= 1
                    if array_depth == 0:  # End of top-level array
                        obj = ''.join(current_block).strip()
                        if obj:
                            objects.append(obj)
                        current_block = []
            elif char == '{':
                if depth == 0:
                    current_block = [char]
                else:
                    current_block.append(char)
                depth += 1
            elif char == '}':
                depth -= 1
                current_block.append(char)
                if depth == 0 and array_depth == 0:
                    obj = ''.join(current_block).strip()
                    if obj:
                        objects.append(obj)
                    current_block = []
            elif char == ',' and depth == 1 and array_depth == 1:
                # Handle commas between array elements at depth 1
                current_block.append(char)
            elif depth > 0 or array_depth > 0:
                current_block.append(char)

            current_pos += 1

        # Handle any remaining content
        if current_block:
            obj = ''.join(current_block).strip()
            if obj:
                objects.append(obj)

        return objects

    def remove_comments(self, text: str) -> str:
        """
        Remove comments from JSON text while preserving string literals.

        Args:
            text (str): Input text containing potential comments

        Returns:
            str: Text with comments removed
        """
        logger.debug("Removing comments from text")
        result = []
        i = 0
        length = len(text)
        in_string = False
        string_char = None
        in_multiline_comment = False
        in_singleline_comment = False

        while i < length:
            # Handle string boundaries
            if not in_multiline_comment and not in_singleline_comment:
                if text[i] in '"\'`':
                    if not in_string:
                        in_string = True
                        string_char = text[i]
                    elif text[i] == string_char:
                        if i > 0 and text[i-1] == '\\':
                            # Check for escaped quote
                            if i > 1 and text[i-2] != '\\':
                                in_string = False
                                string_char = None
                        else:
                            in_string = False
                            string_char = None

            # Only process comments when not in a string
            if not in_string:
                # Handle multi-line comments
                if i + 1 < length and text[i:i+2] == '/*' and not in_singleline_comment:
                    in_multiline_comment = True
                    i += 2
                    continue
                elif i + 1 < length and text[i:i+2] == '*/' and in_multiline_comment:
                    in_multiline_comment = False
                    i += 2
                    continue

                # Handle single-line comments
                if i + 1 < length and text[i:i+2] == '//' and not in_multiline_comment:
                    in_singleline_comment = True
                    i += 2
                    continue
                elif text[i] == '\n' and in_singleline_comment:
                    in_singleline_comment = False
                    result.append('\n')
                    i += 1
                    continue

                # Skip characters in comments
                if in_multiline_comment or in_singleline_comment:
                    i += 1
                    continue

            # Add non-comment characters to result
            result.append(text[i])
            i += 1

        return ''.join(result)

    def strip_surrounding_text(self, text: str) -> str:
        """
        Strip non-JSON text before and after JSON content.

        Args:
            text (str): Input text potentially containing surrounding non-JSON content

        Returns:
            str: Clean JSON content with surrounding text removed
        """
        logger.debug("Stripping surrounding text")
        # Find the first { and last }
        start = text.find('{')
        end = text.rfind('}')

        if start != -1 and end != -1 and end > start:
            return text[start:end + 1]
        return text

    def fix_string_escapes(self, text: str) -> str:
        """
        Fix string escapes for any triple-quoted strings in JSON.

        Args:
            text (str): Input text containing potential string escapes

        Returns:
            str: Text with properly escaped strings
        """
        logger.debug("Fixing string escapes")

        def fix_multiline_string(match):
            key = match.group(1)
            content = match.group(2)
            # Normalize line endings
            content = content.replace('\r\n', '\n').replace('\r', '\n')
            # Preserve indentation but remove common leading whitespace
            lines = content.split('\n')
            if len(lines) > 1:
                # Find minimum indentation (excluding empty lines)
                min_indent = min((len(line) - len(line.lstrip())
                                  for line in lines if line.strip()))
                # Remove common indentation
                lines = [line[min_indent:] if line.strip() else ''
                         for line in lines]
                content = '\n'.join(lines)

            # Escape quotes and backslashes
            content = content.replace('\\', '\\\\').replace('"', '\\"')
            # Preserve newlines as \n
            content = content.replace('\n', '\\n')

            return f'"{key}": "{content}"'

        # Fix triple-quoted strings
        pattern = r'"([^"]+)":\s*"""(.*?)"""'
        text = re.sub(pattern, fix_multiline_string, text, flags=re.DOTALL)

        return text

    def score_candidate(self, text: str) -> float:
        """
        Score a candidate based on JSON structure validity.

        Args:
            text (str): Candidate JSON text to score

        Returns:
            float: Score indicating likelihood of valid JSON structure
        """
        score = 0.0
        text = text.strip()

        # Basic JSON structure
        if text.startswith('{') and text.endswith('}'):
            score += 5.0
        elif text.startswith('[') and text.endswith(']'):
            score += 5.0
        elif self._is_primitive_value(text):
            score += 5.0

        # Check for balanced brackets
        brackets_balance = text.count('{') == text.count('}')
        square_balance = text.count('[') == text.count(']')
        if brackets_balance and square_balance:
            score += 5.0

        # JSON elements
        score += text.count(':') * 0.5  # Key-value pairs
        score += text.count(',') * 0.3  # List/object elements

        # Analyze string content vs structure
        quoted_strings = re.findall(r'"([^"]*)"', text)
        for string in quoted_strings:
            if '...' in string and re.match(r'^[a-zA-Z].*', string):
                # Ellipsis in a normal text string (acceptable)
                score += 0.2
            elif '...' in string and not re.match(r'^[a-zA-Z].*', string):
                # Ellipsis in what looks like a placeholder/incomplete value
                score -= 5.0

        # Score string quotes, but exclude if they're empty or just placeholders
        for string in quoted_strings:
            if string and not re.match(r'^[\s\.]*$', string):
                score += 0.2

        # Penalize non-JSON content
        score -= len(re.findall(r'//.*?\n', text)) * \
            3.0  # Single-line comments
        score -= len(re.findall(r'/\*.*?\*/', text, re.DOTALL)) * \
            3.0  # Multi-line comments
        # Other non-JSON characters
        score -= len(re.findall(r'[^\s\{\}\[\],"\':\w\-\.]', text)) * 1.0

        # Strong bonus for valid-looking complete key-value structures
        valid_kv_pairs = len(re.findall(
            r'"[^"]+"\s*:\s*"[^"]+[^\.][^"]*"', text))
        score += valid_kv_pairs * 2.0

        # Penalize trailing ellipsis in the structure (not in strings)
        if text.strip().endswith('...'):
            score -= 10.0

        logger.debug(
            f"Candidate score: {score} for text: {text[:50]}... [detail: kv_pairs={valid_kv_pairs}, strings={quoted_strings}]")
        return score

    def select_best_candidate(self, candidates: List[str]) -> str:
        """
        Select the best JSON candidate from multiple possibilities.

        Args:
            candidates (List[str]): List of potential JSON candidates

        Returns:
            str: The best candidate based on scoring
        """
        if not candidates:
            return ""

        logger.debug(
            f"Selecting best candidate from {len(candidates)} candidates")

        # Clean and score candidates
        scored_candidates = []
        for text in candidates:
            # Basic cleanup
            cleaned = text.strip()
            # Remove comments
            cleaned = self.remove_comments(cleaned)
            # Strip surrounding text
            cleaned = self.strip_surrounding_text(cleaned)
            # Fix escapes
            cleaned = self.fix_string_escapes(cleaned)

            if cleaned:
                score = self.score_candidate(cleaned)
                scored_candidates.append(Candidate(text=cleaned, score=score))

        if not scored_candidates:
            return ""

        # Sort by score
        scored_candidates.sort(key=lambda x: x.score, reverse=True)

        for candidate in scored_candidates:
            logger.debug(f"Candidate {candidate}")

        best_candidate = scored_candidates[0].text
        logger.debug(
            f"Selected best candidate with score {scored_candidates[0].score}")

        return best_candidate

    def _is_numeric(self, text: str) -> bool:
        """
        Check if text represents a numeric value, including those with commas.

        Args:
            text (str): Text to check

        Returns:
            bool: True if text represents a valid number
        """
        text = text.strip()
        # Match numbers with commas between groups of 3 digits
        if re.match(r'^-?\d{1,3}(,\d{3})*(\.\d+)?$', text):
            return True
        # Match scientific notation
        if re.match(r'^-?\d+\.?\d*[eE][+-]?\d+$', text):
            return True
        # Match simple numbers
        if re.match(r'^-?\d+\.?\d*$', text):
            return True
        return False

    def _is_primitive_value(self, text: str) -> bool:
        """
        Check if text represents a JSON primitive value.

        Args:
            text (str): Text to check

        Returns:
            bool: True if text represents a JSON primitive
        """
        text = text.strip().lower()

        # Handle null
        if text == 'null':
            return True

        # Handle booleans
        if text in ('true', 'false'):
            return True

        # Handle numbers using _is_numeric
        if self._is_numeric(text):
            return True

        # Handle strings (with or without quotes)
        if (text.startswith('"') and text.endswith('"')) or \
           (text.startswith("'") and text.endswith("'")):
            return True

        # Handle unquoted strings (more lenient)
        if text and not any(c in text for c in '{}[]'):
            return True

        return False

    def preprocess(self, text: str, allow_partial: bool = False) -> Union[str, List[str]]:
        """
        Main preprocessing function that handles all cleanup steps.

        Args:
            text (str): Input text to preprocess
            allow_partial (bool): Whether to allow partial JSON structures

        Returns:
            Union[str, List[str]]: Preprocessed JSON text or list of JSON texts
        """
        logger.debug("Starting preprocessing")

        if not text:
            logger.debug("Empty input received")
            return ""

        text = text.strip()

        # Special handling for numeric values
        if self._is_numeric(text):
            logger.debug(f"Detected numeric value: {text}")
            return text

        # Remove comments before further processing
        text = self.remove_comments(text)

        # Extract content blocks
        candidates = self.extract_content_blocks(text)

        # Handle array structure
        if text.strip().startswith('[') and text.strip().endswith(']'):
            # Check if this is a simple array (no objects)
            array_content = text.strip()[1:-1].strip()
            if not '{' in array_content:
                # Clean and return simple array
                array_text = self.strip_surrounding_text(text.strip())
                array_text = self.fix_string_escapes(array_text)
                return array_text

            processed_array = []
            for candidate in candidates:
                # Strip surrounding text
                cleaned = self.strip_surrounding_text(candidate)
                # Fix string escapes
                cleaned = self.fix_string_escapes(cleaned)
                # Basic cleanup
                cleaned = cleaned.strip()
                if cleaned:
                    processed_array.append(cleaned)
            if processed_array:
                return '[' + ','.join(processed_array) + ']'

        # Process candidates and maintain original order
        processed_candidates = []
        for candidate in candidates:
            # Strip surrounding text
            cleaned = self.strip_surrounding_text(candidate)
            # Fix string escapes
            cleaned = self.fix_string_escapes(cleaned)
            # Basic cleanup
            cleaned = cleaned.strip()

            if cleaned:
                processed_candidates.append(cleaned)

        # Score candidates but keep original order
        valid_candidates = []
        for candidate in processed_candidates:
            score = self.score_candidate(candidate)
            stripped = candidate.strip()

            # Handle primitive values (strings, numbers, booleans, null)
            if self._is_primitive_value(stripped):
                return stripped

            # Handle JSON objects
            if ((score > 10.0 or allow_partial) and
                stripped.startswith('{') and
                    (stripped.endswith('}') or allow_partial)):
                valid_candidates.append(candidate)

            # Handle JSON arrays
            elif (stripped.startswith('[') and
                  (stripped.endswith(']') or allow_partial) and
                    (score > 10.0 or allow_partial)):
                return candidate

        # Return all valid candidates in original order
        if len(valid_candidates) > 1:
            return valid_candidates
        elif valid_candidates:
            return valid_candidates[0]

        # If no valid candidates found, return the first processed candidate
        return processed_candidates[0] if processed_candidates else ""


if __name__ == "__main__":
    # Test the preprocessor
    preprocessor = JSONPreprocessor()

    # Test case with comments and surrounding text
    test_input = '''
    Some prefix text
    ```json
    {
        // This is a comment
        "key": "value",
        /* Multi-line
        comment */
        "array": [1, 2, 3]
    }
    Some suffix text
    '''
    result = preprocessor.preprocess(test_input)
    print("Preprocessed result:")
    import json
    print(json.loads(result))
