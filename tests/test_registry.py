import os
import json
import tempfile
import pytest
from axiom.registry import AxiomRegistry

def test_registry_load_and_index():
    registry = AxiomRegistry()
    
    with tempfile.TemporaryDirectory() as tempdir:
        test_file = os.path.join(tempdir, "test_template.json")
        data = {
            "id": "my.test.template",
            "type": "template",
            "inputs": {},
            "messages": [{"role": "system", "content": "You are a bot."}],
            "capability": ["chat"]
        }
        with open(test_file, "w") as f:
            json.dump(data, f)
            
        registry.load_directory(tempdir)
        
    assert registry.get("my.test.template") is not None
    assert len(registry.find_by_capability("chat")) == 1
    assert registry.find_by_type("template")[0].id == "my.test.template"

def test_registry_invalid_type():
    registry = AxiomRegistry()
    with pytest.raises(ValueError):
        registry.register({"id": "foo", "type": "bad_type"})
