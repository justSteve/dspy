# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DSPy (Declarative Self-improving Python) is a framework for programming—not prompting—language models. It enables building modular AI systems with algorithms for optimizing their prompts and weights.

It's imparitive to understand the objective of code produced by our work in this repository, is for personal training reasons. As a complete novice to AI programming in general, my grasp of DSPy is based on a realization that it's going to be a very important skill to have as i widen my knowledge of AI and LLMs. 

So rather than brainstorming new features or optimizations, the goal here is to produce lesson plans and exercises that will help me understand how to use DSPy effectively, and how to build AI systems with it.

I've had great success learning how to use complex system when i've been able to see the progression from 'Hello Worlds' to more mid-level examples. In that context, my initial interest in DSPy has been the aspect that using it is a way to script one's interactions with the LLM instead of the more conventional 'chat' interface.

I'm very much aware that my thought process is more aligned with scripting than chatting. Therefore, as we begin developing courseware let's consider this to be our 'Hello World' example.

One style rule that i'd like to specify without knowing anything else about DSPy is that any document produced by any agent should not violate rules of common linters.

**Documentation:** https://dspy.ai/
**Discord:** https://discord.gg/XCGy2WDCQB
**Version:** 3.0.4b1

## Core Commands

### Development Setup

```bash
# Recommended: Using uv (Rust-based package manager)
uv sync --extra dev

# Alternative: Using conda + pip
conda create -n dspy-dev python=3.11
conda activate dspy-dev
pip install -e ".[dev]"
```

### Running Tests

```bash
# With uv
uv run pytest tests/predict              # Test specific module
uv run pytest tests/ -m "not reliability" # Skip reliability tests
uv run pytest tests/ -m "not llm_call"   # Skip real LM tests
uv run pytest tests/predict/test_predict.py::TestPredict::test_forward  # Single test

# Without uv
pytest tests/predict
pytest tests/ -k "test_bootstrap"        # Run tests matching pattern
```

### Code Quality

```bash
# Pre-commit hooks (run once after cloning)
pre-commit install

# Manual formatting/linting
uv run ruff format .     # Format code
uv run ruff check . --fix # Fix linting issues

# Check specific files
pre-commit run --files dspy/predict/predict.py
```

### Building Documentation

```bash
cd docs
pip install -r requirements.txt
mkdocs serve  # Local preview at http://localhost:8000
```

## Architecture Overview

### Module Organization

DSPy uses a declarative, compositional architecture:

1. **Signatures** (`dspy/signatures/`): Define input/output schemas for tasks
   - `Signature` class specifies field types and descriptions
   - Used to structure LM interactions

2. **Modules** (`dspy/predict/`): Composable AI program components
   - `Predict`: Basic inference module
   - `ChainOfThought`: Step-by-step reasoning
   - `ReAct`: Agent with tool use
   - `ProgramOfThought`: Mathematical reasoning
   - All extend `BaseModule`/`Module` base classes

3. **Adapters** (`dspy/adapters/`): Output formatting/parsing
   - `ChatAdapter`: Chat-based LMs
   - `JSONAdapter`: Structured JSON output
   - `XMLAdapter`: XML format parsing
   - Handle conversion between LM outputs and Python objects

4. **Optimizers** (`dspy/teleprompt/`): Automatic prompt/weight optimization
   - `BootstrapFewShot`: Few-shot example selection
   - `MIPRO`: Multi-stage instruction/demonstration optimization
   - `GEPA`: Reflective prompt evolution
   - `GRPO`: Group rollout policy optimization

5. **LM Clients** (`dspy/clients/`): Language model interfaces
   - Unified interface via `LM` class
   - Support for OpenAI, Anthropic, local models
   - Caching and retry logic built-in

### Key Design Patterns

- **Declarative Design**: Define what, not how (Signatures)
- **Modular Composition**: Chain modules like `dspy.ChainOfThought(dspy.Predict(...))`
- **Parameter System**: Trainable parameters via `Parameter` class
- **Callback System**: Instrumentation hooks for observability
- **Async/Sync Support**: Both execution patterns available

### Core Workflow

1. Define task with a `Signature`
2. Create module (e.g., `Predict`, `ChainOfThought`)
3. Optionally compile/optimize with teleprompt algorithms
4. Execute with inputs

Example:
```python
import dspy

# Configure LM
lm = dspy.LM("openai/gpt-4")
dspy.configure(lm=lm)

# Define signature
class QA(dspy.Signature):
    question = dspy.InputField()
    answer = dspy.OutputField()

# Create module
qa = dspy.Predict(QA)

# Use it
result = qa(question="What is DSPy?")
```

## Testing Guidelines

- Tests use pytest with markers:
  - `reliability`: Integration tests (skipped by default)
  - `llm_call`: Real LM tests (skipped by default)
  - `extra`: Optional extra tests

- Test fixtures in `conftest.py`:
  - `clear_settings`: Auto-clears DSPy settings
  - `lm_for_test`: Mock LM for testing

- Run targeted tests during development:
  ```bash
  uv run pytest tests/predict -v  # Verbose output
  uv run pytest tests/predict/test_predict.py -k "test_forward"
  ```

## Common Development Tasks

### Adding a New Module

1. Create in `dspy/predict/your_module.py`
2. Extend `dspy.Module` or `dspy.predict.Predict`
3. Add tests in `tests/predict/test_your_module.py`
4. Import in `dspy/predict/__init__.py`
5. Document in `docs/docs/api/modules/your_module.md`

### Adding a New Optimizer

1. Create in `dspy/teleprompt/your_optimizer.py`
2. Follow existing patterns (see `bootstrap.py` for reference)
3. Add tests in `tests/teleprompt/test_your_optimizer.py`
4. Document optimization strategy

### Working with Adapters

Adapters control how LM outputs are parsed:
- For structured output: Use/extend `JSONAdapter` or `XMLAdapter`
- For custom formats: Extend `Adapter` base class
- Location: `dspy/adapters/`

## Important Files and Directories

- `dspy/signatures/signature.py`: Core Signature implementation
- `dspy/primitives/base_module.py`: BaseModule class all modules extend
- `dspy/clients/lm.py`: Main LM client interface
- `dspy/teleprompt/bootstrap.py`: Reference optimizer implementation
- `tests/conftest.py`: Test configuration and fixtures
- `pyproject.toml`: Project configuration, dependencies, test settings

## Code Style

- Line length: 120 characters
- Formatter: Ruff (enforced via pre-commit)
- Style guide: Google Python Style Guide
- Double quotes for strings
- Type hints encouraged but not required

## PR Requirements

1. Title format: `{label}(dspy): {message}`
   - Labels: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `build`, `ci`
2. All CI checks must pass (ruff, pytest, build)
3. Pre-commit hooks must pass
4. Add tests for new functionality
5. Update documentation for API changes

## Debugging Tips

- Enable debug logging: `dspy.configure(log_level="DEBUG")`
- Inspect LM history: `lm.history` after calls
- Use callbacks for tracing: See `dspy/utils/callback.py`
- Cache location: `~/.cache/litellm/` (for LM response caching)

## Performance Considerations

- Use caching: Responses are cached by default via diskcache
- Batch operations when possible
- Consider async execution for parallel calls
- Streaming available via `streamify` decorator