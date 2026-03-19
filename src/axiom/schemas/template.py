from enum import Enum
from typing import List, Literal
from pydantic import BaseModel, ConfigDict, Field
from .base import BaseAxiomModel

class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
    FUNCTION = "function"

class Message(BaseModel):
    model_config = ConfigDict(extra="allow")
    
    role: Role
    content: str

class Template(BaseAxiomModel):
    type: Literal["template"] = "template"
    messages: List[Message] = Field(default_factory=list, description="Array of roles and content")
