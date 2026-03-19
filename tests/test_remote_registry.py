import pytest
import json
from unittest.mock import patch, MagicMock
from axiom.registry import AxiomRegistry

def test_remote_registry_loads_and_indexes_schema():
    r = AxiomRegistry()
    
    mock_payload = {
        "id": "prompt.remote_chat",
        "type": "prompt",
        "version": "1.5.0",
        "inputs": {},
        "config": {"temperature": 0.8}
    }
    
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps(mock_payload).encode("utf-8")
    
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        registered = r.load_remote("https://example.com/prompt.json")
        
        assert registered.id == "prompt.remote_chat"
        assert r.get("prompt.remote_chat@1.5.0") is not None
        assert r.get("prompt.remote_chat").version == "1.5.0"

def test_remote_registry_aborts_on_collisions():
    r = AxiomRegistry()
    
    mock_payload = {
        "id": "prompt.remote_chat", "type": "prompt", "version": "1.5.0"
    }
    r.register(mock_payload) 
    
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps(mock_payload).encode("utf-8")
    
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        with pytest.raises(ValueError, match="Version collision"):
            r.load_remote("https://example.com/prompt.json")
