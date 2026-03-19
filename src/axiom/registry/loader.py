import os
import json
import yaml
import urllib.request
from typing import Dict, Any, List

class SchemaLoader:
    @staticmethod
    def load_file(path: str) -> Dict[str, Any]:
        with open(path, "r", encoding="utf-8") as f:
            if path.endswith(".yaml") or path.endswith(".yml"):
                return yaml.safe_load(f)
            else:
                return json.load(f)

    @staticmethod
    def scan_directory(path: str) -> List[Dict[str, Any]]:
        results = []
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".json") or file.endswith(".yaml") or file.endswith(".yml"):
                    try:
                        data = SchemaLoader.load_file(os.path.join(root, file))
                        if data and "type" in data:
                            results.append(data)
                    except Exception:
                        pass
        return results

    @staticmethod
    def fetch_remote(url: str) -> Dict[str, Any]:
        """Fetches an abstract JSON or YAML schema payload statelessly securely over HTTP."""
        req = urllib.request.Request(url, headers={"User-Agent": "Axiom/0.6.0"})
        with urllib.request.urlopen(req) as response:
            body = response.read().decode("utf-8")
            
        if url.endswith(".yaml") or url.endswith(".yml"):
            return yaml.safe_load(body)
        else:
            return json.loads(body)
