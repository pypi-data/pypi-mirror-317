import requests
from .schema import AgentSchema, AgentSearchRequest, AgentRequest, AgentCreateSchema
from prompts.schema import PromptRequest
from prompts import Prompts
import os
from typing import Optional, List
from gepeto.team.schema import Agent

class Agents:
    def __init__(self, api_key: Optional[str] = None, base_url = "", org_id = None, prompts: Prompts = None):
        """Initialize Gepeto client with API key from env or passed directly"""
        self.api_key = api_key or os.environ.get("GEPETO_API_KEY")
        if not self.api_key:
            raise ValueError("GEPETO_API_KEY must be set in environment or passed to constructor")
        self.base_url = base_url
        self.org_id = org_id
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.prompts = prompts
    def _make_request(self, method: str, endpoint: str, json_data: dict = None) -> dict:
        """Make HTTP request to API"""
        url = f"{self.base_url}{endpoint}"
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            json=json_data
        )
        response.raise_for_status()
        return response.json()
    
    def search(self, name: str) -> List[AgentSchema]:
        """Search for agents by name."""
        search_request = AgentSearchRequest(
            organization_id=self.org_id,
            name=name
        )
        json_data = self._make_request("POST", "/shared/agents/search", search_request.model_dump())
        return [AgentSchema(**agent).name for agent in json_data]

    def get(self, name: str) -> AgentSchema:
        """Get a specific agent by name. Case-insensitive."""
        json_data = self._make_request("GET", f"/gepeto/agents/{self.org_id}/{name}")
        response = json_data['agent']
        return AgentSchema(**response).to_agent()

    def list(self) -> List[AgentSchema]:
        """Get all agents."""
        json_data = self._make_request("GET", f"/shared/organizations/{self.org_id}/agents")
        return [AgentSchema(**agent).name for agent in json_data]
    
    def create(
        self, agent: Agent) -> AgentSchema:
        """Create a new agent."""

        #convert instructions to Prompt if its a string
        if type(agent.instructions) == str:
            instructions = PromptRequest(name = agent.name + ' prompt', content=agent.instructions, description = 'prompt for ' + agent.name, organization_id=self.org_id)
        elif type(agent.instructions) == function:
            raise NotImplementedError("functions are not currently implemented in the API")
        elif type(agent.instructions) == PromptRequest:
            instructions = agent.instructions
        else:
            raise ValueError("Invalid instructions type")

        #create/update the prompt
        try:
            prompt = self.prompts.update(name=instructions.name, content=instructions.content, description = instructions.description)
        except Exception as e:
            prompt = self.prompts.create(name=instructions.name, content=instructions.content, description = instructions.description)
        #prompt type = prompt... need to convert it into PromptVersionSchema before sending to API

        print('made prompt ', prompt)
        print('prompt type ', type(prompt))

        agent_request = AgentCreateSchema(
            name=agent.name,
            model=agent.model,
            organization_id=self.org_id,
            prompt_version_id=prompt.id,
            response_schema=agent.response_format.model_json_schema() if agent.response_format else None,
            temperature=agent.temperature,
            max_tokens=agent.max_tokens,
            functions=agent.functions,
            tool_choice=agent.tool_choice,
            parallel_tool_calls=agent.parallel_tool_calls,
  
        )
        # Endpoint for 'create' is left as a placeholder:
        json_data = self._make_request("POST", "/shared/agents", agent_request.model_dump())
        return AgentSchema(**json_data)

    def update(
        self,
        name: Optional[str] = None,
        instructions: Optional[str] = None,
        description: Optional[str] = None,
        model: Optional[str] = None,
        agent_id: Optional[int] = None
    ) -> AgentSchema:
        """Update an existing agent."""
        agent_request = AgentRequest(
            name=name or "",
            instructions=instructions or "You are a helpful agent",
            description=description,
            organization_id=self.org_id
        )
        # Endpoint for 'update' is left as a placeholder:
        json_data = self._make_request("POST", "/version", agent_request.model_dump())
        return AgentSchema(**json_data)

    def delete(self, name: str) -> None:
        """Delete an agent by name."""
        request = self._make_request("DELETE", f"/shared/agents/{name}/{self.org_id}")
        return request
