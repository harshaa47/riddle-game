import uuid
import random
from langchain_core.messages import HumanMessage, AIMessage
from riddle.riddle_instance import Riddle
from riddle.agent import build_chain
from riddle.schemas import LLMResponse, LLMResult, RiddleConfig, Difficulty, Category

class RiddleGame:

    NON_RUNNING_STATES: list[str] = ['initialized', 'ended_won', 'ended_lost', 'cancelled']
    MAX_TURNS:int = 20

    def __init__(self, config:RiddleConfig = None) -> None:
        self.config:RiddleConfig = config
        self.uuid :uuid.UUID = uuid.uuid7()
        self.turns: int = 0
        self.game_state :str = 'initialized'
        self.guesses :list[dict[str, str]]= []
        self.hints = []
        self.chat_history: list[HumanMessage | AIMessage] = []
        self.chain = build_chain()
        self.riddle:Riddle = self._load_riddle().riddle
        self.game_state = 'running'

    def _load_riddle(self):
        if not self.config:
            self.config = RiddleConfig(
                difficulty=random.choice(list(Difficulty)),
                category=random.choice(list(Category))
            )
        return Riddle(self.config)

    def verify(self, guess) -> LLMResponse:
        response = self.chain.invoke({
            "query": self.riddle.query,
            "answer": self.riddle.answer,
            "incorrect_answers": self.riddle.incorrect_answers,
            "hints": self.riddle.hints,
            "guess": guess,
            "turn_count": self.turns,
            "chat_history": self.chat_history
        })
        self.chat_history.append(HumanMessage(content=guess))
        self.chat_history.append(AIMessage(content=response.hint))
        return response

    def add_user_guess(self, guess) -> str | None:
        self.turns += 1
        self.guesses.append(
           guess
        )
        result = self.verify(guess)
        if result.result == LLMResult.CORRECT:
            self.game_state = "ended_won"
            return None
        if result.result == LLMResult.INCORRECT:
            if self.turns == self.MAX_TURNS:
                self.game_state = "ended_lost"
                return None
            else:
                self.hints.append(result.hint)
                return result.hint

    def is_game_running(self) -> bool:
        return self.game_state not in self.NON_RUNNING_STATES

    def get_game_turns(self) -> int:
        return self.turns

    def get_game_state(self) -> str:
        return self.game_state

    def give_up(self):
        self.game_state = 'ended_lost'

    def get_game_result(self) -> int:
        if self.game_state == 'ended_won':
            return 1
        elif self.game_state == 'ended_lost' or self.game_state == 'cancelled':
            return -1
        return 0
