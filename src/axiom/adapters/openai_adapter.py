import os
from typing import Any, Dict
from .base import BaseAdapter
from ..schemas import Prompt, Template

class OpenAIAdapter(BaseAdapter):
    """Adapter for executing Axiom plans directly via OpenAI SDK."""
    
    def _render_content(self, content: str, variables: Dict[str, Any]) -> str:
        """Simple template rendering replacing {{var}} with values."""
        result = content
        for k, v in variables.items():
            result = result.replace(f"{{{{{k}}}}}", str(v))
        return result

    def execute(self) -> Any:
        if not self._plan:
            raise ValueError("No ExecutionPlan ingested.")
            
        results = []
        inputs = self._plan.resolved_inputs
        
        for node_id, node in self._plan.nodes.items():
            if not node.resolved_prompts:
                continue
                
            for prompt_id in node.resolved_prompts:
                prompt = self.registry.get(prompt_id)
                template = None
                if isinstance(prompt, Prompt) and prompt.extends:
                    template = self.registry.get(prompt.extends)
                    
                if not template or not isinstance(template, Template):
                    raise ValueError(f"Extends template not found for prompt: {prompt_id}")
                
                oai_messages = []
                for msg in template.messages:
                    rendered_content = self._render_content(msg.content, inputs)
                    oai_messages.append({
                        "role": msg.role.value,
                        "content": rendered_content
                    })
                
                kwargs = {"model": "gpt-4"}
                if prompt.config:
                    if prompt.config.temperature is not None:
                        kwargs["temperature"] = prompt.config.temperature
                    if prompt.config.max_tokens is not None:
                        kwargs["max_tokens"] = prompt.config.max_tokens
                
                if os.getenv("AXIOM_MOCK_OPENAI") == "1":
                    results.append({"mocked": True, "messages": oai_messages, "kwargs": kwargs})
                else:
                    import openai 
                    response = openai.chat.completions.create(messages=oai_messages, **kwargs)
                    results.append(response.choices[0].message.content)
                    
        return results
