"""
Courseware Configuration
References the centralized courseware content in judge0/.dspy
"""
from pathlib import Path

# Base path to myClaude root
MYCLAUDE_ROOT = Path(__file__).parent.parent.parent.parent

# Courseware paths in judge0
COURSEWARE_ROOT = MYCLAUDE_ROOT / "tooling" / "judge0" / ".dspy"
LESSONS_PATH = COURSEWARE_ROOT / "lessons"
DATA_PATH = COURSEWARE_ROOT / "data"
LIB_PATH = COURSEWARE_ROOT / "lib"
OUTPUTS_PATH = COURSEWARE_ROOT / "outputs"
LAB_PATH = COURSEWARE_ROOT / "lab"

# Lesson categories
BASICS_LESSONS = LESSONS_PATH / "basics"

def get_lesson_path(category: str, lesson_name: str) -> Path:
    """
    Get the full path to a specific lesson file.

    Args:
        category: Lesson category (e.g., 'basics')
        lesson_name: Lesson filename (e.g., '01_hello_dspy.py')

    Returns:
        Path to the lesson file
    """
    return LESSONS_PATH / category / lesson_name

def get_all_lessons(category: str = "basics") -> list[Path]:
    """
    Get all lesson files in a category.

    Args:
        category: Lesson category (default: 'basics')

    Returns:
        List of lesson file paths
    """
    category_path = LESSONS_PATH / category
    if not category_path.exists():
        return []

    return sorted(category_path.glob("*.py"))

def get_data_file(filename: str) -> Path:
    """
    Get path to a data file.

    Args:
        filename: Name of the data file

    Returns:
        Path to the data file
    """
    return DATA_PATH / filename

# Verify courseware exists
if not COURSEWARE_ROOT.exists():
    raise FileNotFoundError(
        f"Courseware not found at {COURSEWARE_ROOT}. "
        f"Expected structure: myClaude/tooling/judge0/.dspy/"
    )
