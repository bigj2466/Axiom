import pytest
from pydantic import ValidationError
from axiom.schemas import Template, Message, Role, Prompt

def test_valid_template():
    t = Template(
        id="test.template",
        type="template",
        inputs={"text": {"type": "string"}},
        messages=[
            Message(role=Role.USER, content="Hello {{text}}")
        ]
    )
    assert t.id == "test.template"
    assert len(t.messages) == 1

def test_invalid_template():
    with pytest.raises(ValidationError):
        # Missing required 'id' and 'type' is strictly literal 'template'
        Template(
            messages=[Message(role="invalid_role", content="")] # type: ignore
        )

def test_valid_prompt():
    p = Prompt(
        id="chat.basic",
        type="prompt",
        extends="base.chat",
        inputs={"query": {"type": "string"}},
        config={"temperature": 0.5}
    )
    assert p.extends == "base.chat"
    assert p.config.temperature == 0.5
