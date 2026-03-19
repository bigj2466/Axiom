import os
from typing import Any
from .base import BaseAdapter

class OpenAIAdapter(BaseAdapter):
    """Adapter for executing Axiom plans directly via OpenAI SDK."""
    
    def execute(self) -> Any:
        if not self._plan:
            raise ValueError("No ExecutionPlan ingested.")
            
        results = []
        
        for node_id, node in self._plan.nodes.items():
            if not node.messages:
                continue
                
            oai_messages = node.messages
            kwargs = {"model": "gpt-4"}
            if node.config:
                if "temperature" in node.config:
                    kwargs["temperature"] = node.config["temperature"]
                if "max_tokens" in node.config:
                    kwargs["max_tokens"] = node.config["max_tokens"]
            
            if os.getenv("AXIOM_MOCK_OPENAI") == "1":
                results.append({"mocked": True, "messages": oai_messages, "kwargs": kwargs})
            else:
                import openai 
                response = openai.chat.completions.create(messages=oai_messages, **kwargs)
                results.append(response.choices[0].message.content)
                    
        return results
