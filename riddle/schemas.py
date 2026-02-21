from dataclasses import dataclass
from enum import Enum
from pydantic import BaseModel, Field


class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXTREME = "extreme"


class Category(Enum):
    PLANTS = "plants"
    ANIMALS = "animals"
    KITCHENWARE = "kitchen_items"
    FLOWERS = "flowers"


@dataclass
class RiddleConfig:
    difficulty: Difficulty
    category: Category


@dataclass
class Riddle:
    query: str
    answer: str
    incorrect_answers: list[str]
    hints: list[str]
    cautions: list[str]
    difficulty: Difficulty
    category: list[Category]


class LLMResult(Enum):
    CORRECT = "correct"
    INCORRECT = "incorrect"

class LLMResponse(BaseModel):
    result:LLMResult
    hint:str