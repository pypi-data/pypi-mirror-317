import pytest
from typing import List, Optional, Union, Literal
from enum import Enum
from pydantic import BaseModel, Field, EmailStr, constr
from pulsar.parser import parse

# Basic union test models
class Foo(BaseModel):
    hi: List[str]

class Bar(BaseModel):
    foo: str

# Cat enums and models
class CatA(str, Enum):
    A = "A"

class CatB(str, Enum):
    C = "C"
    D = "D"

class CatC(str, Enum):
    E = "E"
    F = "F"
    G = "G"
    H = "H"
    I = "I"

class CatAPicker(BaseModel):
    cat: CatA

class CatBPicker(BaseModel):
    cat: CatB
    item: int

class CatCPicker(BaseModel):
    cat: CatC
    item: Union[int, str, None]
    data: Optional[int] = None

# Assistant API models
class AssistantType(str, Enum):
    ETF = "ETFAssistantAPI"
    Stock = "StockAssistantAPI"

class AskClarificationAction(str, Enum):
    ASK_CLARIFICATION = "AskClarificationAPI"

class RespondToUserAction(str, Enum):
    RESPOND_TO_USER = "RespondToUserAPI"

class UIType(str, Enum):
    CompanyBadge = "CompanyBadge"
    Markdown = "Markdown"
    NumericalSlider = "NumericalSlider"
    BarGraph = "BarGraph"
    ScatterPlot = "ScatterPlot"

class MarkdownContent(BaseModel):
    text: str

class CompanyBadgeContent(BaseModel):
    name: str
    symbol: str
    logo_url: str

class NumericalSliderContent(BaseModel):
    title: str
    min: float
    max: float
    value: float

class GraphDataPoint(BaseModel):
    name: str
    expected: float
    reported: float

class ScatterDataPoint(BaseModel):
    x: str
    y: float

class ScatterPlotContent(BaseModel):
    expected: List[ScatterDataPoint]
    reported: List[ScatterDataPoint]

class UIContent(BaseModel):
    richText: Optional[MarkdownContent] = None
    companyBadge: Optional[CompanyBadgeContent] = None
    numericalSlider: Optional[NumericalSliderContent] = None
    barGraph: Optional[List[GraphDataPoint]] = None
    scatterPlot: Optional[ScatterPlotContent] = None
    foo: Optional[str] = None

class UI(BaseModel):
    section_title: str
    types: List[UIType]
    content: UIContent

class RespondToUserAPI(BaseModel):
    action: Literal[RespondToUserAction.RESPOND_TO_USER]
    sections: List[UI]

class AskClarificationAPI(BaseModel):
    action: Literal[AskClarificationAction.ASK_CLARIFICATION]
    question: str

class AssistantAPI(BaseModel):
    action: AssistantType
    instruction: str
    user_message: str


# Test Helper Functions
def case_parse(data: str, model_type: type, expected_json: dict = None, should_fail: bool = False, allow_partial: bool = False, exclude_none=True):
    if should_fail:
        with pytest.raises(ValueError):
            parse(data, model_type, allow_partial)
        return
    result = parse(data, model_type, allow_partial)

    if expected_json is not None:
        if isinstance(result, BaseModel):
            assert result.model_dump(exclude_none=exclude_none, mode='json') == expected_json
        elif isinstance(result, list) and all(isinstance(r, BaseModel) for r in result):
            assert [r.model_dump(exclude_none=exclude_none) for r in result] == expected_json
        else:
            assert result == expected_json

# Tests
def test_union():
    data = '{"hi": ["a", "b"]}'
    expected = {"hi": ["a", "b"]}
    case_parse(data, Union[Foo, Bar], expected)

def test_union2():
    data = """```json
    {
      "cat": "E",
      "item": "28558C",
      "data": null
    }
    ```"""
    expected = {
        "cat": "E",
        "item": "28558C",
        "data": None
    }
    case_parse(data, Union[CatAPicker, CatBPicker, CatCPicker], expected, exclude_none=False)

def test_union3():
    data = """```json
    {
      "action": "RespondToUserAPI",
      "sections": [
        {
          "section_title": "NVIDIA Corporation (NVDA) Latest Earnings Summary",
          "types": ["CompanyBadge", "Markdown", "BarGraph"],
          "content": {
            "companyBadge": {
              "name": "NVIDIA Corporation",
              "symbol": "NVDA",
              "logo_url": "https://upload.wikimedia.org/wikipedia/en/thumb/2/21/Nvidia_logo.svg/1920px-Nvidia_logo.svg.png"
            },
            "richText": {
              "text": "### Key Metrics for the Latest Earnings Report (2024-08-28)\\n\\n- **Earnings Per Share (EPS):** $0.68\\n- **Estimated EPS:** $0.64\\n- **Revenue:** $30.04 billion\\n- **Estimated Revenue:** $28.74 billion\\n\\n#### Notable Highlights\\n- NVIDIA exceeded both EPS and revenue estimates for the quarter ending July 28, 2024.\\n- The company continues to show strong growth in its data center and gaming segments."
            },
            "barGraph": [
              {
                "name": "Earnings Per Share (EPS)",
                "expected": 0.64,
                "reported": 0.68
              },
              {
                "name": "Revenue (in billions)",
                "expected": 28.74,
                "reported": 30.04
              }
            ]
          }
        }
      ]
    }
    ```"""
    expected = {
        "action": "RespondToUserAPI",
        "sections": [
            {
                "section_title": "NVIDIA Corporation (NVDA) Latest Earnings Summary",
                "types": ["CompanyBadge", "Markdown", "BarGraph"],
                "content": {
                    "companyBadge": {
                        "name": "NVIDIA Corporation",
                        "symbol": "NVDA",
                        "logo_url": "https://upload.wikimedia.org/wikipedia/en/thumb/2/21/Nvidia_logo.svg/1920px-Nvidia_logo.svg.png"
                    },
                    "richText": {
                        "text": "### Key Metrics for the Latest Earnings Report (2024-08-28)\n\n- **Earnings Per Share (EPS):** $0.68\n- **Estimated EPS:** $0.64\n- **Revenue:** $30.04 billion\n- **Estimated Revenue:** $28.74 billion\n\n#### Notable Highlights\n- NVIDIA exceeded both EPS and revenue estimates for the quarter ending July 28, 2024.\n- The company continues to show strong growth in its data center and gaming segments."
                    },
                    "barGraph": [
                        {
                            "name": "Earnings Per Share (EPS)",
                            "expected": 0.64,
                            "reported": 0.68
                        },
                        {
                            "name": "Revenue (in billions)",
                            "expected": 28.74,
                            "reported": 30.04
                        }
                    ]
                }
            }
        ]
    }
    case_parse(data, Union[RespondToUserAPI, AskClarificationAPI, List[AssistantAPI]], expected)

