import pytest
from axiom.registry import AxiomRegistry

def test_registry_offline_set_intersection_querying():
    r = AxiomRegistry()
    
    r.register({
        "id": "prompt.finance_bot", "type": "prompt", "version": "1.0.0",
        "capability": ["chat", "finance"], "tags": ["prod", "eu"]
    })
    
    r.register({
        "id": "prompt.support_bot", "type": "prompt", "version": "1.5.0",
        "capability": ["chat", "support"], "tags": ["prod", "us"]
    })
    
    r.register({
        "id": "skill.finance_router", "type": "skill", "version": "2.0.0",
        "capability": ["router", "finance"], "tags": ["beta", "eu"]
    })
    
    # 1. Type Intersection Returns 2
    assert len(r.query(type="prompt")) == 2
    
    # 2. Capability Intersection Returns 2
    assert len(r.query(capability="finance")) == 2
    
    # 3. Tags & Capability Intersection Returns correctly overlapping properties
    results = r.query(capability="finance", tag="eu")
    assert len(results) == 2
    
    results = r.query(type="prompt", capability="finance", tag="eu")
    assert len(results) == 1
    assert results[0].id == "prompt.finance_bot"
    
    # 4. id_contains substring filter maps explicitly correctly 
    results = r.query(id_contains="router")
    assert len(results) == 1
    assert results[0].id == "skill.finance_router"

def test_query_returns_absolute_latest_versions():
    r = AxiomRegistry()
    r.register({
        "id": "prompt.tax_bot", "type": "prompt", "version": "1.0.0",
        "tags": ["tax"]
    })
    r.register({
        "id": "prompt.tax_bot", "type": "prompt", "version": "1.5.0",
        "tags": ["tax"]
    })
    
    # Resolves mapped implicit limitations securely verifying bounds deterministic limits 
    results = r.query(tag="tax")
    assert len(results) == 1
    assert results[0].version == "1.5.0"
