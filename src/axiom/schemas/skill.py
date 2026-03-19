from typing import List, Literal, Optional
from pydantic import Field
from .base import BaseAxiomModel

class Skill(BaseAxiomModel):
    type: Literal["skill"] = "skill"
    prompts: Optional[List[str]] = Field(None, description="IDs of component prompts")
    steps: Optional[List[str]] = Field(None, description="Steps for pipeline execution")
    strategy: Optional[str] = Field(None, description="Execution strategy (e.g., pipeline, select)")
