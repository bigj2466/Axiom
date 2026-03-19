from typing import Dict, Any, List
from ..registry import AxiomRegistry
from ..schemas import Template, Prompt, Skill, UseCase
from ..schemas.execution_plan import ExecutionPlan, ExecutionNode, ExecutionEdge

class AxiomRuntime:
    """Deterministic graph compiler for Axiom execution plans."""
    
    def __init__(self, registry: AxiomRegistry):
        self.registry = registry

    def build(self, entrypoint_id: str, runtime_inputs: Dict[str, Any] = None) -> ExecutionPlan:
        runtime_inputs = runtime_inputs or {}
        
        entry = self.registry.get(entrypoint_id)
        if not entry:
            raise ValueError(f"Entrypoint '{entrypoint_id}' not found in registry.")
            
        nodes: Dict[str, ExecutionNode] = {}
        edges: List[ExecutionEdge] = []
        
        last_node_id = "start"

        if isinstance(entry, UseCase):
            for skill_id in entry.skills:
                skill_node_id = f"node_{skill_id.replace('.', '_')}"
                resolved_prompts = self._resolve_skill(skill_id, runtime_inputs)
                
                nodes[skill_node_id] = ExecutionNode(
                    type="skill",
                    ref=skill_id,
                    resolved_prompts=resolved_prompts
                )
                edges.append(ExecutionEdge(**{"from": last_node_id, "to": skill_node_id}))
                last_node_id = skill_node_id

        elif isinstance(entry, Skill):
            skill_node_id = f"node_{entry.id.replace('.', '_')}"
            resolved_prompts = self._resolve_skill(entry.id, runtime_inputs)
            nodes[skill_node_id] = ExecutionNode(
                type="skill",
                ref=entry.id,
                resolved_prompts=resolved_prompts
            )
            edges.append(ExecutionEdge(**{"from": last_node_id, "to": skill_node_id}))
            
        elif isinstance(entry, Prompt):
            prompt_node_id = f"node_{entry.id.replace('.', '_')}"
            self._resolve_prompt(entry.id, runtime_inputs)
            nodes[prompt_node_id] = ExecutionNode(
                type="prompt",
                ref=entry.id,
                resolved_prompts=[entry.id]
            )
            edges.append(ExecutionEdge(**{"from": last_node_id, "to": prompt_node_id}))

        else:
            raise ValueError(f"Unsupported entrypoint type: {type(entry).__name__}")
            
        return ExecutionPlan(
            id=f"plan.{entrypoint_id}",
            entrypoint=entrypoint_id,
            nodes=nodes,
            edges=edges,
            resolved_inputs=runtime_inputs
        )

    def _resolve_skill(self, skill_id: str, runtime_inputs: Dict[str, Any]) -> List[str]:
        skill = self.registry.get(skill_id)
        if not skill or not isinstance(skill, Skill):
            raise ValueError(f"Skill '{skill_id}' not found or invalid.")
            
        if not skill.prompts:
            return []
            
        for prompt_id in skill.prompts:
            self._resolve_prompt(prompt_id, runtime_inputs)
            
        return skill.prompts

    def _resolve_prompt(self, prompt_id: str, runtime_inputs: Dict[str, Any]):
        prompt = self.registry.get(prompt_id)
        if not prompt or not isinstance(prompt, Prompt):
            raise ValueError(f"Prompt '{prompt_id}' not found or invalid.")
            
        if prompt.extends:
            template = self.registry.get(prompt.extends)
            if not template or not isinstance(template, Template):
                raise ValueError(f"Base template '{prompt.extends}' for prompt '{prompt_id}' not found.")
                
            for req_input in template.inputs.keys():
                if req_input not in runtime_inputs:
                    raise ValueError(f"Missing required input '{req_input}' for inherited template '{template.id}'")
        
        # Check prompt-level schema mapped inputs
        for req_input in prompt.inputs.keys():
            if req_input not in runtime_inputs:
                raise ValueError(f"Missing required input '{req_input}' for prompt '{prompt.id}'")
