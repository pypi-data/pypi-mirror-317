import requests
from .schema import PromptSchema
import os
from typing import Optional, List


class Prompt:
    def __init__(self, api_key: Optional[str] = None, base_url = "", org_id = None):
        """Initialize Gepeto client with API key from env or passed directly"""
        self.api_key = api_key or os.environ.get("GEPETO_API_KEY")
        if not self.api_key:
            raise ValueError("GEPETO_API_KEY must be set in environment or passed to constructor")
        self.base_url = base_url
        self.org_id = org_id
    
    def get(self, name: str) -> PromptSchema:
        """Get a specific prompt by name"""
        #not implemented in API
        response = requests.get(
            f"{self.base_url}/prompts/{self.org_id}/{name}",
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        response.raise_for_status()
        return Prompt(**response.json())

    def get_all(self) -> List[PromptSchema]:
        """Get all prompts"""
        response = requests.get(
            f"{self.base_url}/prompts/{self.org_id}",
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        response.raise_for_status()
        return [Prompt(**prompt) for prompt in response.json()]
    
    def create(self, prompt: PromptSchema) -> PromptSchema:
        pass

    def update(self, name: str, prompt: PromptSchema) -> PromptSchema:
        pass

    def delete(self, name: str) -> None:
        pass
