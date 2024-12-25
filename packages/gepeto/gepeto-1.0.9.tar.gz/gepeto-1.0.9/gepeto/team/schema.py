from openai.types.chat import ChatCompletionMessage
from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall, Function 

from typing import List, Callable, Union, Optional
from pydantic import BaseModel

AgentFunction = Callable[[], Union[str, "Agent", dict]]


class Agent(BaseModel):
    name: str = "Agent"
    model: str = "gpt-4o"
    instructions: Union[str, Callable[[], str]] = "You are a helpful agent"
    functions: List[AgentFunction] = []
    tool_choice: str = None
    parallel_tool_calls: bool = True
    max_tokens: int = 4096
    temperature: float = 0.0


class Response(BaseModel):
    messages: List = []
    agent: Optional[Agent] = None
    variable_inputs: dict = {}


class Result(BaseModel):
    '''possible return values of agent function'''
    value: str = ""
    agent: Optional[Agent] = None
    variable_inputs: dict = {}
