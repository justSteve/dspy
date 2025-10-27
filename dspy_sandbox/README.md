# DSPy Learning Sandbox

A progressive learning environment for mastering DSPy through scripting, not prompting.

## Philosophy

This sandbox treats LLM interactions as **scripted operations** rather than conversations. Each lesson is a runnable Python script that demonstrates a concept, building from "Hello World" to practical applications.

## Quick Start

### 1. Install Dependencies (First Time Only)

```bash
# From dspy_sandbox directory
pip install -r requirements.txt
```

### 2. Run Your First Lesson

```bash
# Run your first DSPy script
python run.py lesson 01_hello_dspy

# See what lessons are available
python run.py list

# Run with detailed output
python run.py lesson 01_hello_dspy --verbose

# Compare two approaches
python run.py compare 02_chat_vs_script
```

### 3. Configure Your LM Provider

The sandbox automatically detects available API keys in this order:
1. **Anthropic** (if `ANTHROPIC_API_KEY` is set)
2. **OpenAI** (if `OPENAI_API_KEY` is set)
3. **Mock LM** (no API key needed, for learning offline)

```bash
# Example: Use Anthropic (recommended)
export ANTHROPIC_API_KEY='sk-ant-...'
python run.py lesson 01_hello_dspy

# Example: Force OpenAI
export OPENAI_API_KEY='sk-...'
export LM_PROVIDER='openai'
python run.py lesson 01_hello_dspy

# Example: Use mock (no API key)
export LM_PROVIDER='mock'
python run.py lesson 01_hello_dspy
```

See `.env.example` for all configuration options.

## Structure

```
dspy_sandbox/
├── lessons/           # Progressive learning modules
│   ├── basics/       # Foundation concepts
│   ├── building/     # Combining components
│   └── applied/      # Real-world applications
├── lab/              # Your experimental scripts
├── lib/              # Reusable utilities
├── outputs/          # Execution results and logs
└── data/            # Sample datasets
```

## Learning Path

### Stage 1: Basics (Hello World)
- `01_hello_dspy` - Your first DSPy script
- `02_chat_vs_script` - Understanding the paradigm shift
- `03_signatures` - Defining input/output contracts
- `04_simple_chain` - Sequential operations

### Stage 2: Building
- `05_question_answer` - Basic QA system
- `06_text_transform` - Various transformations
- `07_extract_info` - Structured extraction
- `08_decisions` - Conditional logic with LLMs

### Stage 3: Applied
- `09_doc_processor` - Multi-step analysis
- `10_data_pipeline` - Process structured data
- `11_report_gen` - Automated reports
- `12_code_explain` - Code understanding

## Design Principles

1. **Visibility**: Every lesson shows what DSPy is doing under the hood
2. **Progression**: Each lesson builds on previous concepts
3. **Experimentation**: Easy to modify and run variations
4. **Comparison**: See differences between approaches side-by-side
5. **Reusability**: Components you build can be imported in later lessons

## The Runner System

The `run.py` script provides a consistent interface for:
- Executing lessons with proper setup
- Capturing and formatting output
- Logging LLM interactions
- Tracking your progress
- Comparing different approaches

## Your Lab Space

The `lab/` directory is your experimental playground. Copy lessons here, modify them, and create your own scripts. The runner system works with lab scripts too:

```bash
python run.py lab my_experiment
```

## Next Steps

1. Run `python run.py lesson 01_hello_dspy` to start
2. Read the output carefully - it explains what's happening
3. Open the lesson file and modify it
4. Run again to see your changes
5. Progress to the next lesson when ready