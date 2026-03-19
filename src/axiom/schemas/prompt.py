from typing import Literal, Optional
from pydantic import Field
from .base import BaseAxiomModel

class Prompt(BaseAxiomModel):
    type: Literal["prompt"] = "prompt"
    extends: Optional[str] = Field(None, description="ID of the base template this prompt extends")
