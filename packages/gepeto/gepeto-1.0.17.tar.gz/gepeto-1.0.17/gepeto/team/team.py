import json
import copy
from collections import defaultdict
from typing import List
import litellm

#this is for anthropic to handle user-user or assistant-assistant messages
litellm.modify_params = True

#this is to drop any input parameters not supported by the openai spec
#https://docs.litellm.ai/docs/completion/input
litellm.drop_params = True

from .utils import debug_print, func_to_json
from prompts import Prompt
from team.schema import (Agent, 
                    AgentFunction, 
                    ChatCompletionMessage, 
                    ChatCompletionMessageToolCall,
                    #this will be used for streaming in the future
                    Function,
                    Response,
                    Result)


__VARS_NAME__ = "context"

class Team:
    def __init__(self):
        pass

    def run_agent(
            self, 
            agent: Agent,
            message_history: List,
            context: dict,
            debug: bool = False,
    ) -> ChatCompletionMessage:
        
        context = defaultdict(str, context)
        instructions = (agent.instructions(context) if callable(agent.instructions)
                        else agent.instructions.content.format(context) if isinstance(agent.instructions, Prompt)
                       else agent.instructions)
        
        messages = [{"role": "system", "content": instructions}] + message_history
        debug_print(debug, "messages", messages)

        tools = [func_to_json(f) for f in agent.functions]
        
        for tool in tools:
            params = tool["function"]["parameters"]
            params["properties"].pop(__VARS_NAME__, None)
            if __VARS_NAME__ in params["required"]:
                params["required"].remove(__VARS_NAME__)

        create_params = {
            "model": agent.model,
            "max_tokens": agent.max_tokens,
            "temperature": agent.temperature,
            "messages": messages,
        }

        if tools: 
            create_params["parallel_tool_calls"] = agent.parallel_tool_calls
            create_params["tools"] = tools
            create_params["tool_choice"] = agent.tool_choice
        
        #this is for structured output of an agent
        response_format = agent.response_format
        if response_format: 
            create_params["response_format"] = response_format

        return litellm.completion(**create_params)
    
    def handle_function_result(self, result, debug) -> Result:
        match result:
            case Result() as result:
                return result
            
            case Agent() as agent: 
                return Result(
                    value = json.dumps({"assistant": agent.name}),
                    agent = agent
                )

            case _:
                try:
                    return Result(value = str(result))
                except Exception as e:
                    error_message = f"Failed to cast response to string: {result}. Make sure agent functions return a string or Result object. Error: {str(e)}"
                    debug_print(debug, error_message)
                    raise TypeError(error_message)
                
    def handle_tool_calls(
            self,
            tool_calls: List[ChatCompletionMessageToolCall],
            functions: List[AgentFunction],
            context: dict,
            debug: bool,
    ) -> Response:
        
        function_map = {f.__name__: f for f in functions}
        constructed_response = Response(messages=[], agent=None, context = {})

        for tool_call in tool_calls:
            name = tool_call.function.name

            if name not in function_map:
                debug_print(debug, f"Tool {name} not found in function map")
                constructed_response.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "tool_name": name,
                        "content": f"Error: tool {name} not found in function map"
                    }
                )
                continue
            
            args = json.loads(tool_call.function.arguments)
            debug_print(debug, f"Processing tool call: {name} with args: {args}")

            func = function_map[name]
            if __VARS_NAME__ in func.__code__.co_varnames:
                args[__VARS_NAME__] = context
            raw_result = function_map[name](**args)

            result: Result = self.handle_function_result(raw_result, debug)

            constructed_response.messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "tool_name": name,
                    "content": result.value,
                }
            )

            constructed_response.context.update(result.context)
            if result.agent:
                constructed_response.agent = result.agent

        return constructed_response
    
    def run(
            self,
            agent: Agent,
            message_history: List,
            context: dict = {},
            debug: bool = False,
            max_turns: int = float("inf"),
            execute_tools: bool = True) -> Response:
        
        active_agent = agent
        context = copy.deepcopy(context)
        message_history = copy.deepcopy(message_history)
        initial_length = len(message_history)

        while len(message_history) - initial_length < max_turns and active_agent:
            completion = self.run_agent(
                agent=active_agent,
                message_history=message_history,
                context=context,
                debug=debug
            )
            message = completion.choices[0].message

            #parse the response if the agent has a response_format
            response_object = None
            if active_agent.response_format:
                stringified_response = message.content
                response_format = active_agent.response_format
                response_object = response_format.model_validate_json(stringified_response)


            debug_print(debug, "Received completion", message)
            message.sender = active_agent.name
            message_history.append(json.loads(message.model_dump_json()))

            if not message.tool_calls or not execute_tools:
                debug_print(debug, "Ending turn")
                break

            constructed_response = self.handle_tool_calls(
                message.tool_calls, active_agent.functions, context, debug)
    
            message_history.extend(constructed_response.messages)
            context.update(constructed_response.context)
            if constructed_response.agent:
                active_agent = constructed_response.agent
            print("saad" + active_agent)

        return Response(
            messages=message_history[initial_length:],
            agent=active_agent,
            context=context,
            response_object=response_object
        )

