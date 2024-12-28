import pytest
from typing import List, Optional, Union, Literal
from pydantic import BaseModel
from pulsar.parser import parse

# Base Model
class Test(BaseModel):
    type: Literal["code"] = "code"
    code: str


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


def test_backticks():
    data = """
    {
      "type": "code",
      "code": `print("Hello, world!")`
    }
    """
    expected = {
      "type": "code",
      "code": 'print("Hello, world!")'
    }
    case_parse(data, Test, expected)

def test_single_quotes():
    data = """
    {
      "type": "code",
      "code": 'print("Hello, world!")'
    }
    """
    expected = {
      "type": "code",
      "code": 'print("Hello, world!")'
    }
    case_parse(data, Test, expected)

def test_double_quotes():
    data = """
    {
      "type": "code",
      "code": "print(\\"Hello, world!\\")"
    }
    """
    expected = {
      "type": "code",
      "code": 'print("Hello, world!")'
    }
    case_parse(data, Test, expected)

def test_unquoted_string():
    data = """
    {
      "type": "code",
      "code": "print(\\"Hello, world!\\")"
    }
    """
    expected = {
      "type": "code",
      "code": 'print("Hello, world!")'
    }
    case_parse(data, Test, expected)

def test_triple_quotes():
    data = """
    {
      "type": "code",
      "code": '''print("Hello, world!")'''
    }
    """
    expected = {
      "type": "code",
      "code": 'print("Hello, world!")'
    }
    case_parse(data, Test, expected)

def test_unescaped_newline_double_quotes():
    data = """
    {
      "type": "code",
      "code": "print(\\"Hello, world!
Goodbye, world!\\")"
    }
    """
    expected = {
      "type": "code",
      "code": 'print("Hello, world!\nGoodbye, world!")'
    }
    case_parse(data, Test, expected)

def test_unescaped_newline_backticks():
    data = """
    {
      "type": "code",
      "code": `print("Hello, world!
Goodbye, world!")`
    }
    """
    expected = {
      "type": "code",
      "code": 'print("Hello, world!\nGoodbye, world!")'
    }
    case_parse(data, Test, expected)

def test_unescaped_newline_single_quotes():
    data = """
    {
      "type": "code",
      "code": 'print("Hello, world!
Goodbye, world!")'
    }
    """
    expected = {
      "type": "code",
      "code": 'print("Hello, world!\nGoodbye, world!")'
    }
    case_parse(data, Test, expected)

def test_unescaped_newline_triple_quotes():
    data = """
    {
      "type": "code",
      "code": '''print("Hello, world!
Goodbye, world!")'''
    }
    """
    expected = {
      "type": "code",
      "code": 'print("Hello, world!\nGoodbye, world!")'
    }
    case_parse(data, Test, expected)

def test_unescaped_double_quotes_in_double_quotes():
    data = """
    {
      "type": "code",
      "code": "print("Hello, world!")"
    }
    """
    expected = {
      "type": "code",
      "code": 'print("Hello, world!")'
    }
    case_parse(data, Test, expected)

def test_unescaped_double_quotes_in_backticks():
    data = """
    {
      "type": "code",
      "code": `print("Hello, world!")`
    }
    """
    expected = {
      "type": "code",
      "code": 'print("Hello, world!")'
    }
    case_parse(data, Test, expected)

def test_unescaped_single_quotes_in_single_quotes():
    data = """
    {
      "type": "code",
      "code": 'print('Hello, world!')'
    }
    """
    expected = {
      "type": "code",
      "code": "print('Hello, world!')"
    }
    case_parse(data, Test, expected)

def test_unescaped_double_quotes_in_triple_quotes():
    data = """
    {
      "type": "code",
      "code": '''print("Hello, world!")'''
    }
    """
    expected = {
      "type": "code",
      "code": 'print("Hello, world!")'
    }
    case_parse(data, Test, expected)

def test_unescaped_single_quotes_in_triple_quotes():
    data = """
    {
      "type": "code",
      "code": '''print('''Hello, world!''')'''
    }
    """
    expected = {
      "type": "code",
      "code": 'print('
    }
    case_parse(data, Test, expected)

def test_unescaped_backticks_in_backticks():
    data = """
    {
      "type": "code",
      "code": `console.log(`Hello, world!`)`
    }
    """
    expected = {
      "type": "code",
      "code": "console.log(`Hello, world!`)"
    }
    case_parse(data, Test, expected)

def test_large_backticks():
    data = """
    {
      "type": "code",
      "code": `import { query } from './_generated/server';
import { v } from 'convex/values';

export default query(async (ctx) => {
  const posts = await ctx.db
    .query('posts')
    .order('desc')
    .collect();

  const postsWithDetails = await Promise.all(
    posts.map(async (post) => {
      // Fetch author information
      const author = await ctx.db.get(post.authorId);
      if (!author) {
        throw new Error('Author not found');
      }

      // Count upvotes
      const upvotes = await ctx.db
        .query('upvotes')
        .filter((q) => q.eq(q.field('postId'), post._id))
        .collect();

      return {
        id: post._id.toString(),
        title: post.title,
        content: post.content,
        author: {
          id: author._id.toString(),
          name: author.name,
        },
        upvoteCount: upvotes.length,
        createdAt: post._creationTime.toString(),
      };
    })
  );

  return postsWithDetails;
})`
    }
    """
    
    expected = {
      "type": "code",
      "code": """import { query } from './_generated/server';
import { v } from 'convex/values';

export default query(async (ctx) => {
  const posts = await ctx.db
    .query('posts')
    .order('desc')
    .collect();

  const postsWithDetails = await Promise.all(
    posts.map(async (post) => {
      // Fetch author information
      const author = await ctx.db.get(post.authorId);
      if (!author) {
        throw new Error('Author not found');
      }

      // Count upvotes
      const upvotes = await ctx.db
        .query('upvotes')
        .filter((q) => q.eq(q.field('postId'), post._id))
        .collect();

      return {
        id: post._id.toString(),
        title: post.title,
        content: post.content,
        author: {
          id: author._id.toString(),
          name: author.name,
        },
        upvoteCount: upvotes.length,
        createdAt: post._creationTime.toString(),
      };
    })
  );

  return postsWithDetails;
})"""
    }
    case_parse(data, Test, expected)

