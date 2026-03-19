import pytest
from axiom.registry import AxiomRegistry
from axiom.runtime import AxiomRuntime

def get_test_registry():
    r = AxiomRegistry()
    r.register({
        "id": "base.chat",
        "type": "template",
        "inputs": {"context": {"type": "string"}},
        "messages": [{"role": "system", "content": "You are helpful."}]
    })
    
    r.register({
        "id": "prompt.chat",
        "type": "prompt",
        "extends": "base.chat",
        "inputs": {"query": {"type": "string"}},
        "config": {"temperature": 0.5}
    })
    
    r.register({
        "id": "skill.chat",
        "type": "skill",
        "strategy": "pipeline",
        "prompts": ["prompt.chat"]
    })
    
    r.register({
        "id": "usecase.chat",
        "type": "usecase",
        "skills": ["skill.chat"]
    })
    
    return r

def test_runtime_compiles_usecase():
    r = get_test_registry()
    engine = AxiomRuntime(r)
    
    inputs = {"query": "Tell me a joke.", "context": "Be funny."}
    plan = engine.build("usecase.chat", inputs)
    
    assert plan.id == "plan.usecase.chat"
    assert "node_skill_chat" in plan.nodes
    assert len(plan.edges) > 0
    assert plan.nodes["node_skill_chat"].type == "skill"
    assert "prompt.chat" in plan.nodes["node_skill_chat"].resolved_prompts
    
    # ZER0 API Calls have successfully yielded an execution plan
    assert plan.resolved_inputs["query"] == "Tell me a joke."

def test_runtime_fails_missing_inputs():
    r = get_test_registry()
    engine = AxiomRuntime(r)
    
    # Missing base template context
    with pytest.raises(ValueError, match="Missing required input 'context'"):
        engine.build("prompt.chat", {"query": "Hello"})
        
    # Missing direct prompt query
    with pytest.raises(ValueError, match="Missing required input 'query'"):
        engine.build("prompt.chat", {"context": "Hello"})
