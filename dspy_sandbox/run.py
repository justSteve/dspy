#!/usr/bin/env python3
"""
DSPy Learning Sandbox Runner
A reusable execution system for DSPy lessons and experiments.
"""

import sys
import os
import argparse
import importlib.util
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import traceback

# Add parent directory to path so we can import dspy
sys.path.insert(0, str(Path(__file__).parent.parent))

class SandboxRunner:
    """Main runner for DSPy sandbox lessons and experiments."""

    def __init__(self, verbose: bool = False, capture_output: bool = True):
        self.verbose = verbose
        self.capture_output = capture_output
        self.sandbox_root = Path(__file__).parent
        self.outputs_dir = self.sandbox_root / "outputs"
        self.outputs_dir.mkdir(exist_ok=True)

        # Track execution history
        self.history_file = self.outputs_dir / "history.json"
        self.history = self._load_history()

    def _load_history(self) -> list:
        """Load execution history."""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []

    def _save_history(self):
        """Save execution history."""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2, default=str)

    def _setup_logging(self, lesson_name: str) -> Path:
        """Set up logging for a lesson execution."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.outputs_dir / f"{lesson_name}_{timestamp}.log"
        return log_file

    def list_lessons(self) -> Dict[str, list]:
        """List all available lessons organized by category."""
        lessons_dir = self.sandbox_root / "lessons"
        lessons = {}

        if lessons_dir.exists():
            for category in lessons_dir.iterdir():
                if category.is_dir():
                    lesson_files = sorted([
                        f.stem for f in category.glob("*.py")
                        if not f.name.startswith("_")
                    ])
                    if lesson_files:
                        lessons[category.name] = lesson_files

        return lessons

    def find_lesson(self, name: str) -> Optional[Path]:
        """Find a lesson file by name."""
        # Check lessons directory
        lessons_dir = self.sandbox_root / "lessons"
        for category in lessons_dir.iterdir():
            if category.is_dir():
                lesson_file = category / f"{name}.py"
                if lesson_file.exists():
                    return lesson_file

        # Check lab directory
        lab_file = self.sandbox_root / "lab" / f"{name}.py"
        if lab_file.exists():
            return lab_file

        return None

    def run_lesson(self, lesson_name: str, **kwargs) -> Dict[str, Any]:
        """Run a specific lesson and capture results."""
        print(f"\n{'='*60}")
        print(f"Running: {lesson_name}")
        print(f"{'='*60}\n")

        # Find the lesson file
        lesson_path = self.find_lesson(lesson_name)
        if not lesson_path:
            print(f"❌ Lesson not found: {lesson_name}")
            return {"status": "error", "message": "Lesson not found"}

        # Set up logging
        log_file = self._setup_logging(lesson_name)

        # Record execution
        execution_record = {
            "lesson": lesson_name,
            "timestamp": datetime.now(),
            "path": str(lesson_path),
            "log_file": str(log_file)
        }

        try:
            # Import and run the lesson
            spec = importlib.util.spec_from_file_location("lesson", lesson_path)
            lesson_module = importlib.util.module_from_spec(spec)

            # Add utilities to the module
            lesson_module.verbose = self.verbose
            lesson_module.sandbox_root = self.sandbox_root

            # Execute the lesson
            print(f"📂 Loading from: {lesson_path.relative_to(self.sandbox_root)}\n")
            spec.loader.exec_module(lesson_module)

            # Run main if it exists
            if hasattr(lesson_module, 'main'):
                result = lesson_module.main(**kwargs)
                execution_record["status"] = "success"
                execution_record["result"] = result
            else:
                execution_record["status"] = "success"
                execution_record["result"] = "Module executed successfully"

            print(f"\n✅ Lesson completed successfully")

            if self.capture_output and log_file.exists():
                print(f"📝 Output saved to: {log_file.relative_to(self.sandbox_root)}")

        except Exception as e:
            print(f"\n❌ Error running lesson: {e}")
            if self.verbose:
                traceback.print_exc()
            execution_record["status"] = "error"
            execution_record["error"] = str(e)

        # Save to history
        self.history.append(execution_record)
        self._save_history()

        print(f"\n{'='*60}\n")
        return execution_record

    def compare(self, lesson_name: str) -> None:
        """Run a comparison lesson that shows different approaches."""
        print(f"\n🔄 Running comparison: {lesson_name}\n")
        self.run_lesson(lesson_name, mode="compare")

    def show_progress(self) -> None:
        """Display learning progress based on history."""
        if not self.history:
            print("No lessons completed yet. Start with: python run.py lesson 01_hello_dspy")
            return

        print("\n📊 Your Learning Progress\n")
        print(f"Total executions: {len(self.history)}")

        # Count unique lessons
        completed = set()
        for record in self.history:
            if record.get("status") == "success":
                completed.add(record["lesson"])

        print(f"Unique lessons completed: {len(completed)}")

        # Show available vs completed
        all_lessons = self.list_lessons()
        total_available = sum(len(lessons) for lessons in all_lessons.values())

        print(f"Progress: {len(completed)}/{total_available} lessons")

        # Show completion by category
        print("\nBy category:")
        for category, lessons in all_lessons.items():
            completed_in_category = [l for l in lessons if l in completed]
            print(f"  {category}: {len(completed_in_category)}/{len(lessons)}")
            if self.verbose:
                for lesson in lessons:
                    status = "✅" if lesson in completed else "⭕"
                    print(f"    {status} {lesson}")

def main():
    parser = argparse.ArgumentParser(description="DSPy Learning Sandbox Runner")
    parser.add_argument("command", choices=["lesson", "lab", "list", "compare", "progress"],
                       help="Command to run")
    parser.add_argument("target", nargs="?", help="Lesson or lab script name")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Show detailed output")
    parser.add_argument("--no-capture", action="store_true",
                       help="Don't capture output to file")

    args = parser.parse_args()

    runner = SandboxRunner(
        verbose=args.verbose,
        capture_output=not args.no_capture
    )

    if args.command == "list":
        lessons = runner.list_lessons()
        if not lessons:
            print("No lessons found. Please check the lessons directory.")
        else:
            print("\n📚 Available Lessons:\n")
            for category, lesson_list in lessons.items():
                print(f"{category.upper()}:")
                for lesson in lesson_list:
                    print(f"  • {lesson}")
                print()

    elif args.command == "progress":
        runner.show_progress()

    elif args.command == "compare":
        if not args.target:
            print("Please specify a lesson to compare")
            sys.exit(1)
        runner.compare(args.target)

    elif args.command in ["lesson", "lab"]:
        if not args.target:
            print(f"Please specify a {args.command} to run")
            sys.exit(1)
        runner.run_lesson(args.target)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()