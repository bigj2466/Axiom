# Quickstart

Welcome to Axiom v1.0. Axiom establishes enterprise rigor inside your generic unconstrained LLM orchestrations by compiling stateless, version-locked schemas explicitly offline.

## 1. Installation

Axiom seamlessly injects into your environment globally minimizing intrusive external network dependencies.
```bash
pip install axiom-core
```

## 2. CLI Execution Basics

Deploy the standard command line tool to dynamically initialize, interact with, evaluate, and build against your schema directories without touching python mechanics purely offline natively:

```bash
# Validates schema directories completely catching syntax faults strictly offline natively 
axiom validate examples/support_router/registry

# Computes a pure discrete offline ExecutionPlan JSON explicit representation structurally.
axiom build examples/support_router/registry workflow.support_router --inputs '{"intent":"refund", "user_id":"123", "query": "hello"}' 

# Connect the securely derived offline execution configuration against dynamic external Translators natively.
axiom run examples/support_router/registry workflow.support_router --adapter openai --inputs '{"intent":"refund"}'
```
