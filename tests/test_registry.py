import pytest
import os
import tempfile
import json
from axiom.registry import AxiomRegistry
from axiom.models import Prompt, Skill
from axiom.exceptions import AxiomNotFoundError, AxiomDependencyError

@pytest.fixture
def registry():
    return AxiomRegistry()

def test_registry_add_and_get(registry):
    p = Prompt(id="p1", template="Hello")
    registry.add(p)
    
    assert registry.get("p1").template == "Hello"
    
    # Version explicit
    assert registry.get("p1", "1.0.0").id == "p1"
    
    with pytest.raises(AxiomNotFoundError):
        registry.get("p2")

def test_registry_resolve(registry):
    from axiom.models import UseCase
    u = UseCase(id="u1", skills=["s1"])
    s = Skill(id="s1", prompts=["p1"])
    p = Prompt(id="p1", template="T")
    
    registry.add(u)
    registry.add(s)
    
    # Needs p1
    with pytest.raises(AxiomDependencyError):
        registry.resolve("u1")
        
    registry.add(p)
    # Should resolve cleanly now
    registry.resolve("u1")

def test_load_directory(registry):
    with tempfile.TemporaryDirectory() as tmpdir:
        prompt_data = {
            "id": "file.prompt",
            "type": "prompt",
            "template": "File content"
        }
        with open(os.path.join(tmpdir, "test.json"), "w") as f:
            json.dump(prompt_data, f)
            
        registry.load_directory(tmpdir)
        loaded = registry.get("file.prompt")
        assert loaded.template == "File content"
