import argparse
import json
import sys
import os

from axiom.registry import AxiomRegistry
from axiom.runtime import AxiomRuntime
from axiom.adapters.registry import AdapterRegistry

def main():
    parser = argparse.ArgumentParser(description="Axiom Ecosystem CLI: Deterministic LLM workflow compiler.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 1. VALIDATE
    parser_validate = subparsers.add_parser("validate", help="Validate a directory of Axiom schemas.")
    parser_validate.add_argument("path", help="Directory path to scan")

    # 2. BUILD
    parser_build = subparsers.add_parser("build", help="Compile an entrypoint into an ExecutionPlan.")
    parser_build.add_argument("path", help="Directory path containing schemas")
    parser_build.add_argument("entrypoint", help="The ID of the workflow, usecase, skill or prompt to build.")
    parser_build.add_argument("--inputs", help="JSON string of runtime inputs", default="{}")

    # 3. RUN
    parser_run = subparsers.add_parser("run", help="Compile and evaluate an ExecutionPlan dynamically over an Adapter.")
    parser_run.add_argument("path", help="Directory path containing schemas")
    parser_run.add_argument("entrypoint", help="The ID of the entrypoint to run.")
    parser_run.add_argument("--adapter", help="The canonical name of the registered adapter (e.g. 'openai')", required=True)
    parser_run.add_argument("--inputs", help="JSON string of runtime inputs", default="{}")

    # 4. SEARCH
    parser_search = subparsers.add_parser("search", help="Search the Axiom Registry offline.")
    parser_search.add_argument("path", help="Directory path containing schemas")
    parser_search.add_argument("--tag", help="Filter by tag")
    parser_search.add_argument("--capability", help="Filter by capability")
    parser_search.add_argument("--type", help="Filter by type")

    args = parser.parse_args()

    registry = AxiomRegistry()
    if getattr(args, "path", None):
        if not os.path.exists(args.path):
            print(f"Error: Path '{args.path}' does not exist.")
            sys.exit(1)
        registry.load_directory(args.path)

    if args.command == "validate":
        print(f"✅ Successfully validated and securely loaded {len(registry._items)} unique schema entities.")

    elif args.command == "build":
        runtime = AxiomRuntime(registry)
        runtime_inputs = json.loads(args.inputs)
        try:
            plan = runtime.build(args.entrypoint, runtime_inputs)
            print(json.dumps(plan.model_dump(), indent=2))
        except Exception as e:
            print(f"Compilation Failed: {e}")
            sys.exit(1)

    elif args.command == "run":
        runtime = AxiomRuntime(registry)
        runtime_inputs = json.loads(args.inputs)
        try:
            plan = runtime.build(args.entrypoint, runtime_inputs)
            print(f"✅ AST Compiled: {plan.id} (Nodes: {len(plan.nodes)}, Edges: {len(plan.edges)})")
            
            adapter_cls = AdapterRegistry.get(args.adapter)
            adapter = adapter_cls()
            adapter.ingest(plan)
            print(f"✅ Successfully deployed precompiled Plan [{plan.id}] strictly into Framework Adapter [{args.adapter}].")
            
        except Exception as e:
            print(f"Execution Routing Failed: {e}")
            sys.exit(1)

    elif args.command == "search":
        results = registry.query(type=args.type, capability=args.capability, tag=args.tag)
        print(f"🔍 Found {len(results)} exact matches restricting out capabilities offline:")
        for res in results:
            print(f" - {res.id}@{getattr(res, 'version', '1.0.0')} (Type: {res.type})")

if __name__ == "__main__":
    main()
