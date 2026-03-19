import os
import json
import yaml
from typing import Dict, Any, List

class SchemaLoader:
    """Loads raw dictionary definitions from JSON/YAML files."""
    
    @staticmethod
    def load_file(filepath: str) -> Dict[str, Any]:
        ext = os.path.splitext(filepath)[1].lower()
        with open(filepath, 'r', encoding='utf-8') as f:
            if ext == '.json':
                return json.load(f)
            elif ext in ('.yaml', '.yml'):
                return yaml.safe_load(f)
            else:
                raise ValueError(f"Unsupported file extension: {ext}")

    @staticmethod
    def scan_directory(directory: str) -> List[Dict[str, Any]]:
        results = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(('.json', '.yml', '.yaml')):
                    try:
                        data = SchemaLoader.load_file(os.path.join(root, file))
                        results.append(data)
                    except Exception as e:
                        raise RuntimeError(f"Failed to load {file}: {e}")
        return results
