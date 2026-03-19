from typing import Any
from .base import BaseAdapter

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
            if not node.messages:
                continue
                
            lc_messages = []
            for msg in node.messages:
                if msg["role"] == "system":
                    lc_messages.append(("system", msg["content"]))
                elif msg["role"] == "user":
                    lc_messages.append(("user", msg["content"]))
                    
            chat_prompt = ChatPromptTemplate.from_messages(lc_messages)
            chains.append(chat_prompt)
        
        if not chains:
            return None
        return chains[0]
