import os
import pytest
from axiom.registry import AxiomRegistry
from axiom.runtime import AxiomRuntime
from axiom.adapters import OpenAIAdapter, LangchainAdapter

def setup_registry_and_plan():
    r = AxiomRegistry()
    r.register({
        "id": "base.translate",
        "type": "template",
        "inputs": {"text": {"type": "string"}, "language": {"type": "string"}},
        "messages": [
            {"role": "system", "content": "You are a translator. Translate to {{language}}."},
            {"role": "user", "content": "{{text}}"}
        ],
        "capability": ["translation"]
    })
    r.register({
        "id": "prompt.translate",
        "type": "prompt",
        "extends": "base.translate",
        "inputs": {"text": {"type": "string"}, "language": {"type": "string"}},
        "config": {"temperature": 0.0}
    })
    
    engine = AxiomRuntime(r)
    plan = engine.build("prompt.translate", {"text": "Hello world", "language": "French"})
    return r, plan

def test_openai_adapter_translation():
    os.environ["AXIOM_MOCK_OPENAI"] = "1"
    _, plan = setup_registry_and_plan()
    adapter = OpenAIAdapter()
    adapter.ingest(plan)
    
    results = adapter.execute()
    assert len(results) == 1
    mocked_call = results[0]
    
    assert mocked_call["mocked"] is True
    assert mocked_call["messages"][0]["content"] == "You are a translator. Translate to French."
    assert mocked_call["messages"][1]["content"] == "Hello world"
    assert mocked_call["kwargs"]["temperature"] == 0.0

def test_langchain_adapter_translation():
    _, plan = setup_registry_and_plan()
    adapter = LangchainAdapter()
    adapter.ingest(plan)
    
    try:
        import langchain_core
    except ImportError:
        pytest.skip("Langchain not installed, skipping test.")
        
    chain = adapter.to_chain()
    messages = chain.messages
    assert messages[0].prompt.template == "You are a translator. Translate to French."
    assert messages[1].prompt.template == "Hello world"
