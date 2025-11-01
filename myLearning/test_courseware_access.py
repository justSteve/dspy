"""
Test script to verify courseware access from dspy agent to judge0/.dspy
"""
from courseware_config import (
    COURSEWARE_ROOT,
    LESSONS_PATH,
    get_lesson_path,
    get_all_lessons,
    get_data_file
)

def test_paths():
    """Test that all paths are accessible"""
    print("Testing courseware path configuration...\n")

    print(f"Courseware root: {COURSEWARE_ROOT}")
    print(f"Exists: {COURSEWARE_ROOT.exists()}\n")

    print(f"Lessons path: {LESSONS_PATH}")
    print(f"Exists: {LESSONS_PATH.exists()}\n")

def test_lesson_access():
    """Test accessing individual lessons"""
    print("Testing lesson access...\n")

    lesson = get_lesson_path("basics", "01_hello_dspy.py")
    print(f"Lesson path: {lesson}")
    print(f"Exists: {lesson.exists()}\n")

    if lesson.exists():
        print("First 10 lines of lesson:")
        with open(lesson, encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                if i > 10:
                    break
                print(f"  {line.rstrip()}")
        print()

def test_all_lessons():
    """Test getting all lessons in a category"""
    print("Testing get all lessons...\n")

    lessons = get_all_lessons("basics")
    print(f"Found {len(lessons)} lessons in 'basics':")
    for lesson in lessons:
        print(f"  - {lesson.name}")
    print()

def test_data_access():
    """Test accessing data files"""
    print("Testing data file access...\n")

    data_file = get_data_file("sample_reviews.json")
    print(f"Data file path: {data_file}")
    print(f"Exists: {data_file.exists()}\n")

if __name__ == "__main__":
    print("=" * 60)
    print("DSPy Agent -> judge0 Courseware Access Test")
    print("=" * 60)
    print()

    try:
        test_paths()
        test_lesson_access()
        test_all_lessons()
        test_data_access()

        print("=" * 60)
        print("All tests passed!")
        print("=" * 60)

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
