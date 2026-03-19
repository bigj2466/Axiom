from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Any, Optional, List

class AxiomConfig(BaseModel):
    model_config = ConfigDict(extra="allow")

    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    timeout: Optional[int] = None
    retries: Optional[int] = None

class BaseAxiomModel(BaseModel):
    id: str = Field(..., description="Unique identifier in namespace.type.name format")
    type: str = Field(..., description="Entity type")
    version: str = Field("1.0.0", description="SemVer version string")
    inputs: Dict[str, Any] = Field(default_factory=dict, description="Typed JSON schema block for inputs validation")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom metadata")
    config: Optional[AxiomConfig] = Field(None, description="Execution or model configuration")
    capability: Optional[List[str]] = Field(None, description="Tags describing capabilities matching the indexer")
