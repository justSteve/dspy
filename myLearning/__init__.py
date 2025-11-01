"""
DSPy Learning Agent

This agent consumes courseware from tooling/judge0/.dspy/ and provides
execution/rendering capabilities for DSPy lessons.
"""

from .courseware_config import (
    COURSEWARE_ROOT,
    LESSONS_PATH,
    DATA_PATH,
    get_lesson_path,
    get_all_lessons,
    get_data_file
)
from .lesson_executor import LessonExecutor
from .judge0_client import Judge0Client

__all__ = [
    'COURSEWARE_ROOT',
    'LESSONS_PATH',
    'DATA_PATH',
    'get_lesson_path',
    'get_all_lessons',
    'get_data_file',
    'LessonExecutor',
    'Judge0Client'
]
