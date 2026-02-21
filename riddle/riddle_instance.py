from riddle.schemas import RiddleConfig, Riddle
from riddle.constants import riddles
import random
from dataclasses import replace


class Riddle:

    def __init__(self, config: RiddleConfig):
        self.config = config
        self.riddle: Riddle = self._pick_riddle()

    def _pick_riddle(self):
        valid_riddles = []
        for riddle in riddles:
            if self.config.category not in  riddle.category:
                continue
            if self.config.difficulty != riddle.difficulty:
                continue
            valid_riddles.append(riddle)
        return replace(random.choice(valid_riddles))
    


