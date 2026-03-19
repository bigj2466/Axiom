from typing import Dict, List, Optional, Any
from ..schemas import BaseAxiomModel, Template, Prompt, Skill, UseCase
from .loader import SchemaLoader

class AxiomRegistry:
    """In-memory registry for indexing and resolving Axiom schemas."""
    
    def __init__(self):
        self._items: Dict[str, BaseAxiomModel] = {}
        self._by_type: Dict[str, List[str]] = {}
        self._by_capability: Dict[str, List[str]] = {}

    def load_directory(self, path: str):
        """Discovers and loads all valid schemas from a directory."""
        raw_schemas = SchemaLoader.scan_directory(path)
        for raw in raw_schemas:
            self.register(raw)

    def register(self, raw_data: Dict[str, Any]) -> BaseAxiomModel:
        """Validates and registers a raw dictionary into the correct Pydantic model."""
        if "type" not in raw_data:
            raise ValueError("Schema missing required 'type' field.")
            
        t = raw_data["type"]
        if t == "template":
            model = Template(**raw_data)
        elif t == "prompt":
            model = Prompt(**raw_data)
        elif t == "skill":
            model = Skill(**raw_data)
        elif t == "usecase":
            model = UseCase(**raw_data)
        else:
            raise ValueError(f"Unknown schema type: {t}")

        self._items[model.id] = model
        
        self._by_type.setdefault(model.type, []).append(model.id)
        if model.capability:
            for cap in model.capability:
                self._by_capability.setdefault(cap, []).append(model.id)
                
        return model

    def get(self, id: str) -> Optional[BaseAxiomModel]:
        return self._items.get(id)

    def find_by_type(self, entity_type: str) -> List[BaseAxiomModel]:
        ids = self._by_type.get(entity_type, [])
        return [self._items[i] for i in ids]

    def find_by_capability(self, capability: str) -> List[BaseAxiomModel]:
        ids = self._by_capability.get(capability, [])
        return [self._items[i] for i in ids]
