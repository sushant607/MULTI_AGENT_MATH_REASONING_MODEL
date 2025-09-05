# Math Debate Agents — Version 1 (MVP)

This repo contains a minimal, runnable implementation of the **Proposer–Critic–Optimizer**
multi-agent pipeline for solving math problems and generating diagrams (when applicable).

## Goals (V1)
- Implement 3 agents as prompt-conditioned roles (using a single LLM stub or a real model).
- Run the propose → critique → optimize loop on user queries.
- Verify numeric/algebraic answers via SymPy.
- Render geometry diagrams by executing model-generated plotting code (sandboxed stub).
- Persist successful debate traces to `data/traces.csv` (JSON in a CSV cell) for V3 training.

## How to run
1. Create a Python 3.10+ venv and install requirements:

```bash
pip install -r requirements.txt
```

2. Run demo CLI (uses a stub LLM by default):

```bash
python app/cli.py
```

3. To use a real model, edit `agents/policy_llm.py` and implement `LLM.generate()` using
   Hugging Face or an API.

## Notes
- The LLM used in V1 is a stub that simulates proposer/critic/optimizer outputs.
- All generated plotting code is executed only if it matches a safe template. Do not
  execute arbitrary code returned by untrusted LLMs.
