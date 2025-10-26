"""
Lab Experiment Template
=======================

Use this template as a starting point for your DSPy experiments.
Copy this file and modify it to explore your own ideas.

Remember: We're SCRIPTING with LLMs, not chatting!
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import dspy
from lib.helpers import (
    ScriptingHelper,
    ExperimentTracker,
    setup_mock_environment,
    DSPyExplainer
)

def main():
    """Your experiment entry point."""
    print("🧪 DSPy Lab Experiment\n")

    # Setup (choose mock or real)
    setup_mock_environment()  # Use this for learning without API keys
    # Or for real API:
    # lm = dspy.LM('openai/gpt-4o-mini')
    # dspy.configure(lm=lm)

    # ============================================================
    # YOUR EXPERIMENT STARTS HERE
    # ============================================================

    print("=" * 50)
    print("Experiment: [Your Title Here]")
    print("=" * 50)
    print()

    # Step 1: Define your signature(s)
    class YourSignature(dspy.Signature):
        """What does this signature do?"""
        input_field = dspy.InputField(desc="Description")
        output_field = dspy.OutputField(desc="Description")

    # Show what you've defined
    ScriptingHelper.show_signature(YourSignature)

    # Step 2: Create your module(s)
    your_module = dspy.Predict(YourSignature)

    # Step 3: Prepare test data
    test_input = "Your test data here"

    print(f"Input: {test_input}")
    print("\nProcessing...")

    # Step 4: Execute
    result = your_module(input_field=test_input)

    # Step 5: Display results
    print("\n📊 Results:")
    print("-" * 30)
    print(f"Output: {result.output_field}")
    print("-" * 30)

    # ============================================================
    # EXPERIMENT VARIATIONS
    # ============================================================

    print("\n" + "=" * 50)
    print("Variations to Try")
    print("=" * 50)
    print("""
    1. Add more fields to your signature
    2. Chain multiple operations together
    3. Try different input data
    4. Create a pipeline class
    5. Add error handling
    """)

    return {
        "experiment": "template",
        "status": "complete"
    }

# ============================================================
# HELPER FUNCTIONS (Add your own!)
# ============================================================

def helper_function():
    """Add helper functions as needed."""
    pass

# ============================================================
# NOTES AND OBSERVATIONS
# ============================================================

"""
Use this space to document:
- What worked
- What didn't work
- Surprising behaviors
- Ideas for improvement
- Questions that came up
"""

if __name__ == "__main__":
    main()