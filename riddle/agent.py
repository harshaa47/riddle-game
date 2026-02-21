from langchain_anthropic import ChatAnthropic
from langchain_core.prompt_values import ChatPromptValue
from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableLambda

from riddle.prompts import system_prompt, user_message, chat_history
from riddle.schemas import LLMResponse
from langchain_core.prompts import (
    ChatPromptTemplate
)

llm = ChatAnthropic(
    model="claude-sonnet-4-6"
)

llm_with_structured_output = llm.with_structured_output(LLMResponse, method="json_schema")


def add_cache_control(prompt_value: ChatPromptValue) -> ChatPromptValue:
    messages = prompt_value.messages
    # Cache the system prompt (static for the entire game session)
    for msg in messages:
        if isinstance(msg, SystemMessage):
            msg.additional_kwargs["cache_control"] = {"type": "ephemeral"}
            break
    # Cache up to the last chat history message (everything before the current user turn)
    # This avoids re-processing the full conversation prefix on each turn
    if len(messages) >= 3:
        messages[-2].additional_kwargs["cache_control"] = {"type": "ephemeral"}
    return prompt_value


def build_chain():
    prompts = ChatPromptTemplate.from_messages([system_prompt, chat_history, user_message])
    chain = prompts | RunnableLambda(add_cache_control) | llm_with_structured_output
    return chain
