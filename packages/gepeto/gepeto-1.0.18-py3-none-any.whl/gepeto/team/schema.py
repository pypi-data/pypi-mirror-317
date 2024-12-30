from openai.types.chat import ChatCompletionMessage
from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall, Function 
from prompts import Prompt
from typing import List, Callable, Union, Optional, Type, Any
from pydantic import BaseModel

AgentFunction = Callable[[], Union[str, "Agent", dict]]


class Agent(BaseModel):
    name: str = "Agent"
    model: str = "gpt-4o"
    instructions: Union[str, Callable[[], str], Prompt] = "You are a helpful agent"
    functions: List[AgentFunction] = []
    tool_choice: str = None
    parallel_tool_calls: bool = True
    max_tokens: int = 4096
    temperature: float = 0.0
    response_format: Optional[Type[BaseModel]] = None


class Response(BaseModel):
    messages: List = []
    # agent: Optional[Agent] = None
    agent: Optional[Agent] = None
    context: dict = {}
    #populated only if the agent has a response_format
    response_object: Optional[BaseModel] = None


class Result(BaseModel):
    '''possible return values of agent function'''
    value: str = ""
    agent: Optional[Agent] = None
    context: dict = {}
