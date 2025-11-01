"""
Lesson Executor - Renders and executes lessons from judge0 courseware
"""
import subprocess
import json
from pathlib import Path
from typing import Optional, Dict, Any
from courseware_config import get_lesson_path, get_all_lessons, COURSEWARE_ROOT
from judge0_client import Judge0Client


class LessonExecutor:
    """Execute lessons from judge0 courseware repository"""

    def __init__(self, judge0_endpoint: Optional[str] = None):
        """
        Initialize the lesson executor.

        Args:
            judge0_endpoint: Optional judge0 API endpoint for remote execution.
                           If None, executes locally.
        """
        self.judge0_endpoint = judge0_endpoint or "http://localhost:2358"
        self.judge0_client = Judge0Client(self.judge0_endpoint)
        self.execution_history = []

    def execute_lesson(
        self,
        category: str,
        lesson_name: str,
        use_judge0: bool = False
    ) -> Dict[str, Any]:
        """
        Execute a lesson from the courseware.

        Args:
            category: Lesson category (e.g., 'basics')
            lesson_name: Lesson filename (e.g., '01_hello_dspy.py')
            use_judge0: If True, execute via judge0 API. If False, execute locally.

        Returns:
            Dict with execution results:
            {
                'success': bool,
                'output': str,
                'error': str or None,
                'lesson_path': Path
            }
        """
        lesson_path = get_lesson_path(category, lesson_name)

        if not lesson_path.exists():
            return {
                'success': False,
                'output': '',
                'error': f'Lesson not found: {lesson_path}',
                'lesson_path': lesson_path
            }

        if use_judge0 and self.judge0_endpoint:
            result = self._execute_via_judge0(lesson_path)
        else:
            result = self._execute_locally(lesson_path)

        # Store in history
        self.execution_history.append({
            'lesson': lesson_name,
            'category': category,
            'result': result
        })

        return result

    def _execute_locally(self, lesson_path: Path) -> Dict[str, Any]:
        """Execute lesson locally using Python subprocess"""
        try:
            # Execute the lesson script
            result = subprocess.run(
                ['python', str(lesson_path)],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=COURSEWARE_ROOT
            )

            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr if result.returncode != 0 else None,
                'lesson_path': lesson_path,
                'execution_mode': 'local'
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'output': '',
                'error': 'Execution timeout (30s)',
                'lesson_path': lesson_path,
                'execution_mode': 'local'
            }
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': str(e),
                'lesson_path': lesson_path,
                'execution_mode': 'local'
            }

    def _execute_via_judge0(self, lesson_path: Path) -> Dict[str, Any]:
        """Execute lesson via judge0 API"""
        try:
            result = self.judge0_client.execute_file(lesson_path)
            result['lesson_path'] = lesson_path
            result['execution_mode'] = 'judge0'
            return result
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': f'Judge0 execution error: {str(e)}',
                'lesson_path': lesson_path,
                'execution_mode': 'judge0'
            }

    def render_lesson(self, category: str, lesson_name: str) -> str:
        """
        Render lesson content for display without executing.

        Args:
            category: Lesson category
            lesson_name: Lesson filename

        Returns:
            Lesson source code as string
        """
        lesson_path = get_lesson_path(category, lesson_name)

        if not lesson_path.exists():
            return f"Error: Lesson not found at {lesson_path}"

        try:
            with open(lesson_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading lesson: {e}"

    def list_available_lessons(self, category: str = "basics") -> list[Path]:
        """List all available lessons in a category"""
        return get_all_lessons(category)

    def get_lesson_info(self, category: str, lesson_name: str) -> Dict[str, Any]:
        """
        Get metadata about a lesson.

        Returns:
            Dict with lesson info including docstring, path, size, etc.
        """
        lesson_path = get_lesson_path(category, lesson_name)

        if not lesson_path.exists():
            return {'error': f'Lesson not found: {lesson_path}'}

        # Extract docstring
        content = self.render_lesson(category, lesson_name)
        docstring = ""
        if '"""' in content:
            parts = content.split('"""')
            if len(parts) >= 3:
                docstring = parts[1].strip()

        return {
            'name': lesson_name,
            'category': category,
            'path': str(lesson_path),
            'size': lesson_path.stat().st_size,
            'docstring': docstring,
            'exists': True
        }


def main():
    """Demo/test the lesson executor"""
    executor = LessonExecutor()

    print("=" * 60)
    print("DSPy Lesson Executor - Demo")
    print("=" * 60)
    print()

    # List available lessons
    print("Available lessons in 'basics':")
    lessons = executor.list_available_lessons("basics")
    for lesson in lessons:
        print(f"  - {lesson.name}")
    print()

    # Get info about first lesson
    if lessons:
        first_lesson = lessons[0].name
        print(f"Info for {first_lesson}:")
        info = executor.get_lesson_info("basics", first_lesson)
        print(f"  Docstring: {info.get('docstring', 'N/A')[:100]}...")
        print()

        # Execute the lesson
        print(f"Executing {first_lesson}...")
        result = executor.execute_lesson("basics", first_lesson)
        print(f"  Success: {result['success']}")
        if result['output']:
            print(f"  Output preview: {result['output'][:200]}...")
        if result['error']:
            print(f"  Error: {result['error']}")


if __name__ == "__main__":
    main()
