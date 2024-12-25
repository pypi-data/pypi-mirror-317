from pydantic import BaseModel
from datetime import datetime
from typing import Union, List

class PromptSchema(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    content: str
    description: str
    prompt_id: int
    variables: List[str]
    name: Union[str, None] = None
    organization_id: Union[int, None] = None
