import pytest
from typing import List, Dict, Union, Optional
from pydantic import BaseModel, Field
from pulsar.parser import parse


# Book Analysis Models
class Score(BaseModel):
    year: int
    score: int

class PopularityOverTime(BaseModel):
    bookName: str
    scores: List[Score]

class WordCount(BaseModel):
    bookName: str
    count: int

class Ranking(BaseModel):
    bookName: str
    score: int

class BookAnalysis(BaseModel):
    bookNames: List[str]
    popularityData: List[PopularityOverTime]
    popularityRankings: List[Ranking]
    wordCounts: List[WordCount]

# Graph Models
class Error(BaseModel):
    code: int
    message: str

class ErrorBasic(BaseModel):
    message: str

class Vertex(BaseModel):
    id: str
    metadata: Dict[str, str]

class Edge(BaseModel):
    source_id: str
    target_id: str
    relationship: str

class GraphJson(BaseModel):
    vertices: List[Vertex]
    edges: List[Edge]

# incomplete str
class ContentModel(BaseModel):
    content: str

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

def test_partial_analysis_1():
    data = """
    ```json
    {
      "bookNames": [
        "brave new world",
        "the lord of the rings",
        "three body problem",
        "stormlight archive"
      ],
      "popularityData": [
        {
          "bookName": "brave new world",
          "scores": [
            {"year": 1950, "score": 70},
            {"year": 1960, "score": 75},
            {"year": 1970, "score": 80},
            {"year": 1980, "score": 85},
            {"year": 1990, "score": 85},
            {"year": 2000, "score": 90},
            {"year": 2010, "score": 95},
            {"year": 2020, "score": 97},
            {"year": 2023, "score": 98}
          ]
        },
        {
          "bookName": "the lord of the rings",
          "scores": [
            {"year": 1954, "score": 60},
            {"year": 1960, "score": 75},
            {"year": 1970, "score": 85},
            {"year": 1980, "score": 90},
            {"year": 1990, "score": 92},
            {"year": 2000, "score": 95},
            {"year": 2010, "score": 96},
            {"year": 2020, "score": 98},
            {"year": 2023, "score": 99}
          ]
        },
        {
          "bookName": "three body problem",
          "scores": [
            {"year": 2008, "score": 50},
            {"year": 2010, "score": 60},
            {"year": 2015, "score": 70},
            {"year": 2020, "score": 80},
            {"year": 2023, "score": 85}
          ]
        },
        {
          "bookName": "stormlight archive",
          "scores": [
            {"year": 2010, "score": 55},
            {"year": 2014, "score": 65},
            {"year": 2017, "score": 75},
            {"year": 2020, "score": 80},
            {"year": 2023, "score": 85}
          ]
        }
      ],
      "popularityRankings": [
        {"bookName": "the lord of the rings", "score": 99},
        {"bookName": "brave new world", "score": 97},
        {"bookName": "stormlight archive", "score": 85},
        {"bookName": "three body problem", "score": 85}
      ],
      "wordCounts": [
        {"bookName": "brave new world", "count": 64000},
        {"bookName": "the lord of the rings", "count": 470000},
        {"bookName": "three body problem", "count": 150000},
        {"bookName": "stormlight archive", "count": 400000}
      ]
    }
    ```
    """
    expected = {
        "bookNames": [
            "brave new world",
            "the lord of the rings",
            "three body problem",
            "stormlight archive"
        ],
        "popularityData": [
            {
                "bookName": "brave new world",
                "scores": [{"year": 1950, "score": 70}, {"year": 1960, "score": 75}, {"year": 1970, "score": 80},
                          {"year": 1980, "score": 85}, {"year": 1990, "score": 85}, {"year": 2000, "score": 90},
                          {"year": 2010, "score": 95}, {"year": 2020, "score": 97}, {"year": 2023, "score": 98}]
            },
            {
                "bookName": "the lord of the rings",
                "scores": [
            {"year": 1954, "score": 60},
            {"year": 1960, "score": 75},
            {"year": 1970, "score": 85},
            {"year": 1980, "score": 90},
            {"year": 1990, "score": 92},
            {"year": 2000, "score": 95},
            {"year": 2010, "score": 96},
            {"year": 2020, "score": 98},
            {"year": 2023, "score": 99}
          ]
            },
            {
                "bookName": "three body problem",
                "scores": [
            {"year": 2008, "score": 50},
            {"year": 2010, "score": 60},
            {"year": 2015, "score": 70},
            {"year": 2020, "score": 80},
            {"year": 2023, "score": 85}
          ]
            },
            {
                "bookName": "stormlight archive",
                "scores": [
            {"year": 2010, "score": 55},
            {"year": 2014, "score": 65},
            {"year": 2017, "score": 75},
            {"year": 2020, "score": 80},
            {"year": 2023, "score": 85}
          ]
            },
        ],
        "popularityRankings": [
            {"bookName": "the lord of the rings", "score": 99},
            {"bookName": "brave new world", "score": 97},
            {"bookName": "stormlight archive", "score": 85},
            {"bookName": "three body problem", "score": 85}
        ],
        "wordCounts": [
            {"bookName": "brave new world", "count": 64000},
            {"bookName": "the lord of the rings", "count": 470000},
            {"bookName": "three body problem", "count": 150000},
            {"bookName": "stormlight archive", "count": 400000}
        ]
    }
    case_parse(data, BookAnalysis, expected, allow_partial=True)

def test_partial_analysis_2():
    data = """
    ```json
    {
      "bookNames": [
        "brave new world",
        "the lord of the rings",
        "three body problem",
        "stormlight archive"
      ],
      "popularityData": [
        {
          "bookName": "brave new world",
          "scores": [
            {"year": 1950, "score": 70},
    """
    expected = {
        "bookNames": [
            "brave new world",
            "the lord of the rings",
            "three body problem",
            "stormlight archive"
        ],
        "popularityData": [
            {
                "bookName": "brave new world",
                "scores": [{"year": 1950, "score": 70}]
            }
        ],
        "popularityRankings": [],
        "wordCounts": []
    }
    case_parse(data, BookAnalysis, expected, allow_partial=True)

def test_partial_choppy():
    data = """
    ```json
    {
      "vertices": [
        {
          "id": "stephanie_morales",
          "metadata": {
            "name": "Stephanie Morales",
            "affiliation": "Made Space"
          }
        },
        {
          "id": 
    """
    expected = {
        "vertices": [
            {
                "id": "stephanie_morales",
                "metadata": {
                    "name": "Stephanie Morales",
                    "affiliation": "Made Space"
                }
            }
        ],
        "edges": []
    }
    case_parse(data, GraphJson, expected, allow_partial=True)

def test_partial_choppy_union():
    data = """
    ```json
    {
      "vertices": [
        {
          "id": "stephanie_morales",
          "metadata": {
            "name": "Stephanie Morales",
            "affiliation": "Made Space"
          }
        },
        {
          "id": 
    """
    expected = {
        "vertices": [
            {
                "id": "stephanie_morales",
                "metadata": {
                    "name": "Stephanie Morales",
                    "affiliation": "Made Space"
                }
            }
        ],
        "edges": []
    }
    case_parse(data, Union[GraphJson, List[GraphJson], Error], expected, allow_partial=True)

def test_partial_choppy_union_2():
    data = """
    ```json
    {
      "vertices": [
        {
          "id": "stephanie_morales",
          "metadata": {
            "name": "Stephanie Morales",
            "affiliation": "Made Space"
          }
        },
        {
          "id": 
    """
    expected = {
        "vertices": [
            {
                "id": "stephanie_morales",
                "metadata": {
                    "name": "Stephanie Morales",
                    "affiliation": "Made Space"
                }
            }
        ],
        "edges": []
    }
    case_parse(data, Union[GraphJson, ErrorBasic], expected, allow_partial=True)

def test_partial_incomplete_str():
    data = """```json {content: "asd"""

    expected = { "content": "asd"}
    case_parse(data, ContentModel, expected, allow_partial=True)

    data = """```json [{content: "asd"}, {content: "dff"""
    expected = [{"content": "asd"}, {"content": "dff"}]
    case_parse(data, List[ContentModel], expected, allow_partial=True)
