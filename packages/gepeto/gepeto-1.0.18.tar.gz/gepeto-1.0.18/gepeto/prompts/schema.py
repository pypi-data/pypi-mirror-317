from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class PromptSearchRequest(BaseModel):
    name: str
    organization_id: int

class PromptRequest(PromptSearchRequest):
    description: Optional[str] = None
    content: Optional[str] = None

class Prompt(PromptRequest):
    id: int
    created_at: datetime
    updated_at: datetime
    prompt_id: int






