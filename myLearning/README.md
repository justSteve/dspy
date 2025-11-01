# DSPy Learning Agent

This agent implements the DSPy learning experience by consuming courseware from the centralized judge0 repository and executing it either locally or via judge0 API.

## Architecture

**Courseware Content**: `myClaude/tooling/judge0/.dspy/` (lessons, data, lib)
**Agent Implementation**: `myClaude/dspy/dspy/myLearning/` (execution, rendering, interface)

## How It Works

1. **Courseware** (lessons, data, etc.) lives in `tooling/judge0/.dspy/`
2. **This agent** references and executes that courseware
3. Execution can be:
   - **Local**: Using Python subprocess
   - **Remote**: Via judge0 API for sandboxed execution

## Components

### [courseware_config.py](courseware_config.py)
Path configuration and helper functions to access courseware.

### [lesson_executor.py](lesson_executor.py)
Core execution engine:
- Execute lessons locally or via judge0
- Render lesson content
- Track execution history

### [judge0_client.py](judge0_client.py)
Judge0 API client for remote code execution:
- Submit code to judge0
- Retrieve results
- Health checks

### [test_courseware_access.py](test_courseware_access.py)
Verification that courseware is accessible.

## Usage Examples

### Execute a Lesson

```python
from dspy.myLearning import LessonExecutor

# Create executor
executor = LessonExecutor()

# Execute locally
result = executor.execute_lesson("basics", "01_hello_dspy.py", use_judge0=False)
print(result['output'])

# Execute via judge0 (if running)
result = executor.execute_lesson("basics", "01_hello_dspy.py", use_judge0=True)
```

### List Available Lessons

```python
from dspy.myLearning import get_all_lessons

lessons = get_all_lessons("basics")
for lesson in lessons:
    print(lesson.name)
```

### Render Lesson Content

```python
from dspy.myLearning import LessonExecutor

executor = LessonExecutor()
content = executor.render_lesson("basics", "01_hello_dspy.py")
print(content)
```

## Running Judge0

To use remote execution via judge0:

```bash
cd ../tooling/judge0
docker-compose up -d
```

Then the agent can execute lessons in a sandboxed environment.

## Adding New Features

- **Agent execution/rendering code** → Add to this folder
- **Courseware content (lessons, data)** → Add to `tooling/judge0/.dspy/`

This maintains separation between content and execution logic.
