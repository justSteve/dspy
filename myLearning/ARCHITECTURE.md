# DSPy Learning Agent Architecture

## Overview

The DSPy learning agent follows the **SWIP** (Separation of Workspace and Implementation Pattern) where courseware content is centralized in judge0, and each agent provides execution/rendering logic.

## Directory Structure

```
myClaude/
├── tooling/judge0/.dspy/          # COURSEWARE CONTENT
│   ├── lessons/
│   │   └── basics/                # Lesson files (*.py)
│   ├── data/                      # Sample data
│   ├── lib/                       # Shared utilities
│   ├── lab/                       # Experimental workspace
│   └── outputs/                   # Generated content
│
└── dspy/dspy/myLearning/          # AGENT IMPLEMENTATION
    ├── courseware_config.py       # Path configuration
    ├── lesson_executor.py         # Execution engine
    ├── judge0_client.py           # Judge0 API client
    ├── test_courseware_access.py  # Verification tests
    └── __init__.py                # Public API

```

## Data Flow

```
User Request
    ↓
DSPy Agent (dspy/myLearning/)
    ↓
LessonExecutor
    ├─→ Local Execution (subprocess)
    │   └─→ Reads from tooling/judge0/.dspy/
    │
    └─→ Remote Execution (judge0 API)
        └─→ Submits code from tooling/judge0/.dspy/
            └─→ Returns results
```

## Key Design Decisions

### 1. Separation of Content and Logic
- **Content** (lessons, data) → `tooling/judge0/.dspy/`
- **Logic** (execution, rendering) → `dspy/myLearning/`
- **Benefit**: Multiple agents can share courseware, easy to update content

### 2. Dual Execution Modes
- **Local**: Fast, direct Python subprocess
- **Judge0**: Sandboxed, safe, consistent environment
- **Benefit**: Flexibility for different use cases

### 3. Courseware Reference Pattern
```python
# Agent code references courseware via config
from courseware_config import get_lesson_path

lesson = get_lesson_path("basics", "01_hello_dspy.py")
# Returns: Path('tooling/judge0/.dspy/lessons/basics/01_hello_dspy.py')
```

### 4. Execution Abstraction
```python
executor = LessonExecutor()

# Same interface, different backends
result = executor.execute_lesson("basics", "01.py", use_judge0=False)  # Local
result = executor.execute_lesson("basics", "01.py", use_judge0=True)   # Judge0
```

## Components

### courseware_config.py
- Defines paths to judge0 courseware
- Provides helper functions (get_lesson_path, get_all_lessons, etc.)
- Validates courseware exists

### lesson_executor.py
- **LessonExecutor** class
- Methods:
  - `execute_lesson()` - Execute with local or judge0
  - `render_lesson()` - Display lesson source
  - `list_available_lessons()` - List lessons in category
  - `get_lesson_info()` - Extract metadata

### judge0_client.py
- **Judge0Client** class
- Methods:
  - `execute_code()` - Submit code to judge0
  - `execute_file()` - Submit file to judge0
  - `health_check()` - Verify judge0 is running

## Applying to Other Agents

To implement this pattern for a new agent (e.g., "foo"):

1. **Create courseware folder**:
   ```bash
   mkdir -p tooling/judge0/.foo/{lessons,data,lib}
   ```

2. **Add courseware content**:
   - Lessons → `tooling/judge0/.foo/lessons/`
   - Data → `tooling/judge0/.foo/data/`

3. **Create agent implementation**:
   ```bash
   mkdir -p foo/agent_logic/
   ```

4. **Create courseware_config.py** in agent:
   ```python
   COURSEWARE_ROOT = MYCLAUDE_ROOT / "tooling" / "judge0" / ".foo"
   ```

5. **Implement executor** (or use LessonExecutor as-is)

6. **Test access**:
   ```bash
   python foo/agent_logic/test_courseware_access.py
   ```

## Benefits of This Architecture

1. **DRY**: Courseware content in one place
2. **Reusability**: Multiple agents can share content
3. **Safety**: Judge0 provides sandboxed execution
4. **Flexibility**: Easy to switch between local/remote
5. **Scalability**: Easy to add new agents or courses
6. **Version Control**: Clear ownership and history
7. **Separation of Concerns**: Content vs. execution logic

## Environment Setup

### For Local Execution Only
No setup needed - works out of the box.

### For Judge0 Execution
```bash
cd tooling/judge0
docker-compose up -d
```

Then verify:
```python
from dspy.myLearning import Judge0Client
client = Judge0Client()
print(client.health_check())  # Should return True
```

## Future Enhancements

- [ ] Web UI for lesson browsing
- [ ] Progress tracking across lessons
- [ ] Interactive lesson mode with checkpoints
- [ ] Multi-language support via judge0
- [ ] Lesson authoring tools
- [ ] Integration with CI/CD for courseware validation
