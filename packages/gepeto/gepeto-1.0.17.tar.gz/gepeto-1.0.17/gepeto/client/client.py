import requests
from ..prompts import Prompts
from ..agents import Agents
import os
from typing import Optional, List


class Gepeto:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gepeto client with API key from env or passed directly"""
        self.api_key = api_key or os.environ.get("GEPETO_API_KEY")
        if not self.api_key:
            raise ValueError("GEPETO_API_KEY must be set in environment or passed to constructor")
        
        self.base_url = "https://agent-builder-be-dizrd.ondigitalocean.app/api/v1"

        # Authenticate with API
        self.org_id = self._authenticate()
        self.prompts = Prompts(api_key=self.api_key, base_url=self.base_url, org_id=self.org_id)
        self.agents = Agents(api_key=self.api_key, base_url=self.base_url, org_id=self.org_id, prompts=self.prompts)
        
    def _authenticate(self):
        """Authenticate with the Gepeto API"""
        return 3
        #TODO: implement this
        response = requests.post(
            "",  # URL to be filled in
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        response.raise_for_status()
        return response.json().get("organization_id")



