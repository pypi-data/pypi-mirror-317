import pytest
from typing import List, Union, Optional, Dict, Any
from pydantic import BaseModel, Field

from pulsar.promptlib import json_schema  # Update this import based on your module name

# Test Models
class TextMessage(BaseModel):
    content: str

class TransferToAgent(BaseModel):
    agent: int = Field(..., description="Value from the list of agents")
    task_description: str = Field(..., description="A detailed description to the agent")
    expected_output: str
    extra_data: str

class NestedModel(BaseModel):
    name: str
    messages: List[TextMessage]
    transfer: Optional[TransferToAgent]

def assert_schema_format(schema: str):
    """Helper function to check if the schema string is properly formatted"""
    assert isinstance(schema, str), "Schema should be a string"
    assert len(schema.strip()) > 0, "Schema should not be empty"

def normalize_whitespace(s: str) -> str:
    """Normalize whitespace and newlines for comparison"""
    return ' '.join(s.replace('\n', ' ').split())

def test_formatting_options():
    """Test different formatting options (use_md and show_name)"""
    # Test markdown formatting
    schema, length = json_schema(TransferToAgent, use_md=True)
    assert schema.startswith("```json\n")
    assert schema.endswith("\n```")
    assert "// TransferToAgent" in schema
    
    # Test without class names
    schema, length = json_schema(TransferToAgent, show_name=False)
    assert "// TransferToAgent" not in schema
    assert "agent" in schema
    
    # Test both options together
    schema, length = json_schema(TransferToAgent, use_md=True, show_name=False)
    assert schema.startswith("```json\n")
    assert schema.endswith("\n```")
    assert "// TransferToAgent" not in schema

def test_inline_class_name_format():
    """Test that class names appear inline with opening braces"""
    # Test single model
    schema, _ = json_schema(TransferToAgent)
    lines = schema.split("\n")
    assert any("{ // TransferToAgent" in line.strip() for line in lines)
    
    # Test in list
    schema, _ = json_schema(List[TransferToAgent])
    lines = schema.split("\n")
    assert any("{ // TransferToAgent" in line.strip() for line in lines)
    
    # Test in union
    schema, _ = json_schema(Union[TextMessage, TransferToAgent])
    lines = schema.split("\n")
    assert any("{ // TextMessage" in line.strip() for line in lines)
    assert any("{ // TransferToAgent" in line.strip() for line in lines)

def test_inline_description_format():
    """Test that field descriptions appear as inline comments"""
    schema, _ = json_schema(TransferToAgent)
    lines = [line.strip() for line in schema.split("\n")]
    
    # Check that descriptions are on the same line as fields
    assert any('"agent": integer // Value from the list of agents' in line for line in lines)
    assert any('"task_description": string // A detailed description to the agent' in line for line in lines)

def test_list_formatting():
    """Test list formatting with indentation"""
    schema, _ = json_schema(List[TransferToAgent])
    lines = schema.split("\n")
    
    # Check basic structure
    assert lines[0].strip() == "["
    assert lines[-1].strip() == "]"
    
    # Check inline comments
    content_lines = [line.strip() for line in lines if "//" in line]
    assert any('Value from the list of agents' in line for line in content_lines)

def test_nested_model_formatting():
    """Test formatting of nested models"""
    schema, _ = json_schema(NestedModel)
    normalized = normalize_whitespace(schema)
    
    # Check inline class name
    assert "{ // NestedModel" in normalized
    
    # Check nested structures are properly formatted
    assert '"messages":[' in schema.replace(" ", "")
    assert "TextMessage" in schema
    assert "TransferToAgent" in schema
    
    # Verify structure of nested components
    assert '"name": string' in normalized
    assert '"content": string' in normalized

def test_union_types():
    """Test Union type conversions"""
    # Test simple union
    schema, length = json_schema(Union[str, int])
    assert_schema_format(schema)
    normalized = normalize_whitespace(schema)
    assert "string" in normalized and "integer" in normalized
    assert "\nor\n" in schema
    assert length == 2

    # Test complex union with proper formatting
    schema, length = json_schema(Union[TextMessage, List[TransferToAgent]])
    lines = [line.strip() for line in schema.split("\n")]
    assert any("{ // TextMessage" in line for line in lines)
    assert any("{ // TransferToAgent" in line for line in lines)
    assert length == 2

def test_edge_cases():
    """Test edge cases and potential error conditions"""
    # Test with unsupported type
    class UnsupportedType:
        pass

    schema, length = json_schema(UnsupportedType)
    assert_schema_format(schema)
    assert schema == "string"  # Default fallback
    assert length == 1

    # Test with empty List
    with pytest.raises((TypeError, IndexError)):
        json_schema(List)

    # Test with empty Union
    schema, length = json_schema(Union)
    assert_schema_format(schema)
    assert schema == "string"  # Default type
    assert length == 1

    # Test markdown with empty type
    schema, length = json_schema(str, use_md=True)
    assert schema == '```json\nstring\n```'

if __name__ == "__main__":
    pytest.main([__file__])