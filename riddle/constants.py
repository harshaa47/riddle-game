from pathlib import Path
import json
from riddle.schemas import Riddle, Category, Difficulty

RIDDLE_PATH = Path(__file__).parent / "riddles.json"

_riddles_dict = json.loads(RIDDLE_PATH.read_text())

riddles: list[Riddle] = [
    Riddle(
        query=riddle_item['query'],
        answer=riddle_item['answer'],
        category=[Category(cat) for cat in riddle_item['category']],
        incorrect_answers=riddle_item['incorrect_answers'],
        difficulty=Difficulty(riddle_item['difficulty']),
        hints=riddle_item['hints'],
        cautions=riddle_item.get('cautions', []),
    ) for riddle_item in _riddles_dict
]
