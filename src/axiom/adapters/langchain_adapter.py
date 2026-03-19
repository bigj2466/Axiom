from typing import Any
from .base import BaseAdapter
from ..schemas import Prompt, Template

class LangchainAdapter(BaseAdapter):
    """Translates Axiom ExecutionPlans into LangChain Runnables."""

    def execute(self) -> Any:
        raise NotImplementedError("Use to_chain() for LangChain adapter.")

    def to_chain(self):
        from langchain_core.prompts import ChatPromptTemplate
        
        if not self._plan:
            raise ValueError("No ExecutionPlan ingested.")
            
        chains = []
        for node_id, node in self._plan.nodes.items():
            if not node.resolved_prompts:
                continue
                
            for prompt_id in node.resolved_prompts:
                prompt = self.registry.get(prompt_id)
                if isinstance(prompt, Prompt) and prompt.extends:
                    template = self.registry.get(prompt.extends)
                    if isinstance(template, Template):
                        lc_messages = []
                        for msg in template.messages:
                            lc_content = msg.content.replace("{{", "{").replace("}}", "}")
                            
                            if msg.role.value == "system":
                                lc_messages.append(("system", lc_content))
                            elif msg.role.value == "user":
                                lc_messages.append(("user", lc_content))
                                
                        chat_prompt = ChatPromptTemplate.from_messages(lc_messages)
                        chains.append(chat_prompt)
        
        if not chains:
            return None
        return chains[0]
