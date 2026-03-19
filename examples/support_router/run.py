import json
import os
import sys

# Ensure Axiom is in python path for local execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from axiom.registry import AxiomRegistry
from axiom.runtime import AxiomRuntime

def run_example():
    print("1. Initializing Axiom Registry...")
    registry = AxiomRegistry()
    
    # Prove registry loads from disk accurately
    registry_path = os.path.join(os.path.dirname(__file__), "registry")
    registry.load_directory(registry_path)
    print(f"Loaded {len(registry._items)} unique schema entities.")
    
    # Prove metadata search
    print("\n2. Testing Registry Capability Search...")
    # Add a mock tag live to show query()
    registry.get("workflow.support_router").tags = ["demo", "router"]
    registry._by_tag.setdefault("router", []).append("workflow.support_router")
    
    routers = registry.query(type="workflow", tag="router")
    print(f"Found {len(routers)} workflow tagged 'router': {routers[0].id}")
    
    print("\n3. Compiling the Graph AST Offline via AxiomRuntime...")
    runtime = AxiomRuntime(registry)
    
    # Assume dynamic input parameters representing a user hitting a support page
    inputs = {
        "intent": "refund",
        "user_id": "usr_9921x",
        "query": "My package arrived broken, I need my money back."
    }
    
    # Compile the Declarative Workflow into a strict ExecutionPlan
    plan = runtime.build("workflow.support_router", inputs)
    
    print(f"\nExecutionPlan successfully compiled: {plan.id}")
    print(f"Total Locked Nodes: {len(plan.nodes)}")
    
    # Print the strictly resolved nodes showing implicit version locks
    for node_id, node in plan.nodes.items():
        print(f"  - Node '{node_id}' -> Pinned Ref: {node.ref}")
        print(f"    Messages: {json.dumps(node.messages, indent=2)}")
        print(f"    Config: {node.config}")
        
    print(f"\nTotal Edges: {len(plan.edges)}")
    for edge in plan.edges:
        cond_str = f"Condition: {edge.condition}" if edge.condition else "No Condition"
        print(f"  - Edge: {edge.from_node} -> {edge.to_node} | {cond_str}")
        
    print("\n4. Handing off static plan to the Translators (Adapters)...")
    print("(You would initialize OpenAIAdapter().ingest(plan) here)")
    print("✅ Axiom Example completed perfectly statelessly and offline.")

if __name__ == "__main__":
    run_example()
