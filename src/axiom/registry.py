import os
import json
import yaml
from typing import Dict, Any, TypeVar, Generic

from .models import BaseAxiomModel, Prompt, Skill, UseCase
from .exceptions import AxiomNotFoundError, AxiomSchemaError, AxiomDependencyError

class AxiomRegistry:
    def __init__(self):
        # Index of registered entities: {id: {version: Model}}
        self._entities: Dict[str, Dict[str, BaseAxiomModel]] = {}
        
    def add(self, entity: BaseAxiomModel):
        if entity.id not in self._entities:
            self._entities[entity.id] = {}
        self._entities[entity.id][entity.version] = entity

    def get(self, entity_id: str, version: str = None) -> BaseAxiomModel:
        if entity_id not in self._entities:
            raise AxiomNotFoundError(f"Entity with id '{entity_id}' not found.")
            
        versions = self._entities[entity_id]
        if not versions:
            raise AxiomNotFoundError(f"No versions found for entity '{entity_id}'.")
            
        if version:
            if version not in versions:
                raise AxiomNotFoundError(f"Version '{version}' for entity '{entity_id}' not found.")
            return versions[version]
            
        # Return latest version based on string sorting for now
        latest_version = sorted(versions.keys())[-1]
        return versions[latest_version]

    def resolve(self, usecase_id: str, version: str = None):
        """Validates that all internal dependency chains exist in the registry."""
        usecase = self.get(usecase_id, version)
        if not isinstance(usecase, UseCase):
            raise AxiomDependencyError(f"ID '{usecase_id}' resolves to {usecase.type}, not a usecase.")
            
        for skill_id in usecase.skills:
            try:
                skill = self.get(skill_id)
            except AxiomNotFoundError:
                raise AxiomDependencyError(f"UseCase '{usecase_id}' depends on missing skill '{skill_id}'.")
                
            if not isinstance(skill, Skill):
                raise AxiomDependencyError(f"ID '{skill_id}' resolves to {skill.type}, not a skill.")
                
            if skill.prompts:
                for prompt_id in skill.prompts:
                    try:
                        self.get(prompt_id)
                    except AxiomNotFoundError:
                        raise AxiomDependencyError(f"Skill '{skill_id}' depends on missing prompt '{prompt_id}'.")
                        
    def load_directory(self, path: str):
        """Scans folder for .json and .yml files and indexes them."""
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith('.json') or file.endswith('.yml') or file.endswith('.yaml'):
                    file_path = os.path.join(root, file)
                    self._load_file(file_path)

    def _load_file(self, file_path: str):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_path.endswith('.json'):
                    data = json.load(f)
                else:
                    data = yaml.safe_load(f)
        except Exception as e:
            raise AxiomSchemaError(f"Failed to parse file {file_path}: {e}")

        self._parse_and_add(data, file_path)

    def _parse_and_add(self, data: Dict[str, Any], file_path: str):
        if "type" not in data:
            raise AxiomSchemaError(f"Missing 'type' field in {file_path}")
            
        entity_type = data["type"]
        try:
            if entity_type == "prompt":
                entity = Prompt(**data)
            elif entity_type == "skill":
                entity = Skill(**data)
            elif entity_type == "usecase":
                entity = UseCase(**data)
            else:
                raise AxiomSchemaError(f"Unknown type '{entity_type}' in {file_path}")
                
            self.add(entity)
        except Exception as e:
            raise AxiomSchemaError(f"Schema validation failed for {file_path}: {e}")
