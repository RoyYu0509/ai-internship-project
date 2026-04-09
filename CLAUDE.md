# LLM SERVING SYSTEM

## Project Overview
An LLM Serving System that is able to serving multiple users requests at the same time. The system should be able to handle multiple requests at the same time, and should be able to scale up or down as needed.

## Repository Structure
- `src/` — Source code
- `tests/` — Test code
- `docs/templates/` — Reusable templates (design doc, ADR, task spec)
- `docs/decisions/` — Architecture Decision Records (ADR-001, ADR-002...)
- `docs/designs/` — Actual design documents
- `docs/progress/` — Weekly summaries and milestone notes
- `benchmarks/` — Benchmark scripts and results
  
## Tech Stack 
- Python 3.12+ for core logic and API
- C++20+ for performance-critical components
- PyTorch 

## Code Conventions 
- Google Python Style Guide

## Git Conventions
- Commit format: `type(scope): description`
- Types: feat, fix, refactor, test, docs, chore, perf
- One logical change per commit. Never mix refactor + feature.
- Branch naming: `feature/short-desc`, `fix/short-desc`, `docs/short-desc`
- All changes go through PR to main. Never push directly to main.

## Code Standards
- Python 3.12+, C++20+ 
- Max function length: 50 lines. Extract if longer.
- All public APIs must have documentation comments.
- No commented-out code in commits.
- No TODO without linked issue number.

## Architecture Constraints


## Forbidden
- Do not modify files outside src/ and tests/ without explicit discussion.
- Do not install new dependencies without documenting rationale.
- Do not auto-generate large amounts of boilerplate — prefer understanding over speed.


## Development Workflow
- CPU/MPS functional testing
- benchmarking & production on Nvidia GPU（CUDA）
