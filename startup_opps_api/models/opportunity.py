from pydantic import BaseModel
from typing import Optional

class Opportunity(BaseModel):
    title: str
    organization: str
    type: Optional[str]
    eligibility: Optional[str]
    deadline: Optional[str]
    url: str
