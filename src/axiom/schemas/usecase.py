from typing import List, Literal
from pydantic import Field
from .base import BaseAxiomModel

class UseCase(BaseAxiomModel):
    type: Literal["usecase"] = "usecase"
    skills: List[str] = Field(..., description="IDs of skills comprising this use case")
