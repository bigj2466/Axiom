from typing import Dict, List, Optional, Any
from ..schemas import BaseAxiomModel, Template, Prompt, Skill, UseCase, Workflow
from .loader import SchemaLoader

class AxiomRegistry:
    """In-memory registry for indexing and resolving Axiom schemas deterministically by version."""
    
    def __init__(self):
        self._items: Dict[str, List[BaseAxiomModel]] = {}
        self._by_id_version: Dict[str, BaseAxiomModel] = {}
        
        self._by_type: Dict[str, List[str]] = {}
        self._by_capability: Dict[str, List[str]] = {}
        self._by_tag: Dict[str, List[str]] = {}

    def load_directory(self, path: str):
        raw_schemas = SchemaLoader.scan_directory(path)
        for raw in raw_schemas:
            self.register(raw)
            
    def load_remote(self, url: str) -> BaseAxiomModel:
        """Fetches and securely registers a remote HTTP/HTTPS schema payload offline."""
        raw_schema = SchemaLoader.fetch_remote(url)
        return self.register(raw_schema)
            
    def _parse_version(self, version_str: str) -> tuple:
        try:
            return tuple(map(int, version_str.split(".")))
        except Exception:
            return (0, 0, 0)

    def register(self, raw_data: Dict[str, Any]) -> BaseAxiomModel:
        if "type" not in raw_data:
            raise ValueError("Schema missing required 'type' field.")
            
        t = raw_data["type"]
        if t == "template": model = Template(**raw_data)
        elif t == "prompt": model = Prompt(**raw_data)
        elif t == "skill": model = Skill(**raw_data)
        elif t == "usecase": model = UseCase(**raw_data)
        elif t == "workflow": model = Workflow(**raw_data)
        else: raise ValueError(f"Unknown schema type: {t}")

        version = getattr(model, "version", "1.0.0")
        model_id_version = f"{model.id}@{version}"
        
        if model_id_version in self._by_id_version:
            raise ValueError(f"Version collision: {model_id_version} is already registered.")

        self._by_id_version[model_id_version] = model
        self._items.setdefault(model.id, []).append(model)
        
        self._by_type.setdefault(model.type, []).append(model.id)
        if model.capability:
            for cap in model.capability:
                self._by_capability.setdefault(cap, []).append(model.id)
        if getattr(model, "tags", None):
            for tag in model.tags:
                self._by_tag.setdefault(tag, []).append(model.id)
                
        return model

    def get(self, ref: str) -> Optional[BaseAxiomModel]:
        """Gets exact id@version, or highest semantic version if just id is passed."""
        if "@" in ref:
            return self._by_id_version.get(ref)
            
        candidates = self._items.get(ref)
        if not candidates:
            return None
            
        best = sorted(candidates, key=lambda m: self._parse_version(getattr(m, "version", "1.0.0")))
        return best[-1]

    def find_by_type(self, entity_type: str) -> List[BaseAxiomModel]:
        ids = self._by_type.get(entity_type, [])
        return [self.get(i) for i in ids if self.get(i)]

    def find_by_capability(self, capability: str) -> List[BaseAxiomModel]:
        ids = self._by_capability.get(capability, [])
        return [self.get(i) for i in ids if self.get(i)]

    def query(self, type: Optional[str] = None, capability: Optional[str] = None, 
              tag: Optional[str] = None, id_contains: Optional[str] = None) -> List[BaseAxiomModel]:
        """Provides intuitive multi-dimensional intersection search returning securely determined latest semantic versions."""
        base_set = set(self._items.keys())
        
        if type:
            base_set &= set(self._by_type.get(type, []))
        if capability:
            base_set &= set(self._by_capability.get(capability, []))
        if tag:
            base_set &= set(self._by_tag.get(tag, []))
        if id_contains:
            base_set = {i for i in base_set if id_contains in i}
            
        return [self.get(i) for i in base_set if self.get(i)]
