import pytest
from pydantic import ValidationError
from axiom.models import Prompt, Skill, UseCase

def test_prompt_model_valid():
    p = Prompt(
        id="summarize",
        template="Summarize: {{text}}",
        inputs=["text"]
    )
    assert p.id == "summarize"
    assert p.type == "prompt"
    assert p.version == "1.0.0"

def test_prompt_model_invalid():
    with pytest.raises(ValidationError):
        # Missing required template
        Prompt(id="summarize")

def test_skill_model_valid():
    s = Skill(
        id="rag",
        steps=["retrieve", "answer"],
        strategy="pipeline"
    )
    assert s.id == "rag"
    assert s.type == "skill"

def test_usecase_model_valid():
    u = UseCase(
        id="chat",
        skills=["rag", "summarize"]
    )
    assert u.id == "chat"
    assert u.type == "usecase"
