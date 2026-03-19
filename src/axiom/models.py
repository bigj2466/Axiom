from pydantic import BaseModel, ConfigDict, Field
from typing import List, Dict, Any, Optional, Literal

class BaseAxiomModel(BaseModel):
    model_config = ConfigDict(extra="allow")
    
    id: str
    type: str
    version: str = "1.0.0"
    inputs: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Prompt(BaseAxiomModel):
    type: Literal["prompt"] = "prompt"
    template: str
    tags: List[str] = Field(default_factory=list)

class Skill(BaseAxiomModel):
    type: Literal["skill"] = "skill"
    prompts: Optional[List[str]] = Field(default_factory=list)
    steps: Optional[List[str]] = Field(default_factory=list)
    strategy: Optional[str] = None

class UseCase(BaseAxiomModel):
    type: Literal["usecase"] = "usecase"
    skills: List[str] = Field(default_factory=list)
