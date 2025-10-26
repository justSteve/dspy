"""
Lesson 01: Hello DSPy - Your First Script
==========================================

This is the "Hello World" of DSPy. We'll write our first DSPy script
that transforms a simple prompt into a programmatic operation.

Key Concepts:
- DSPy programs are Python scripts, not chat conversations
- Signatures define input/output contracts
- Predict modules execute the contracts
- Results are structured and predictable
"""

import dspy
from dspy import LM

def main():
    print("🎯 Lesson 01: Hello DSPy\n")
    print("Let's write our first DSPy script!\n")

    # ============================================================
    # PART 1: The Traditional Way (What We're Moving Away From)
    # ============================================================

    print("=" * 50)
    print("PART 1: The Old Way - Prompting")
    print("=" * 50)

    print("""
In traditional LLM usage, you might write:

    prompt = "Please greet the user named Alice warmly"
    response = llm.complete(prompt)

This approach has problems:
- No structure to the output
- Have to parse the response manually
- Different every time you run it
- No type safety or contracts
    """)

    # ============================================================
    # PART 2: The DSPy Way - Programming, Not Prompting
    # ============================================================

    print("=" * 50)
    print("PART 2: The DSPy Way - Scripting")
    print("=" * 50)
    print()

    # Step 1: Configure DSPy with a language model
    # For this lesson, we'll use a mock LM that shows what's happening
    print("Step 1: Configure DSPy")
    print("```python")
    print("lm = dspy.LM('openai/gpt-4o-mini')")
    print("dspy.configure(lm=lm)")
    print("```")

    # Use a simple mock for demonstration
    # In real usage, you'd use: lm = dspy.LM('openai/gpt-4o-mini')
    try:
        # Try to use real LM if available
        lm = dspy.LM('openai/gpt-4o-mini')
        dspy.configure(lm=lm)
        print("✓ Connected to OpenAI GPT-4o-mini\n")
    except:
        # Fall back to mock for demonstration
        print("ℹ️  Using mock LM for demonstration (no API key found)\n")

        class MockLM:
            def __call__(self, prompt, **kwargs):
                # Simple mock responses for demonstration
                if "greet" in prompt.lower():
                    return ["Hello, Alice! It's wonderful to meet you!"]
                return ["This is a mock response for demonstration."]

        dspy.configure(lm=MockLM())

    # Step 2: Define a Signature (the contract)
    print("Step 2: Define the Input/Output Contract")
    print("```python")
    print("class GreetUser(dspy.Signature):")
    print('    """Generate a warm greeting for a user."""')
    print("    name = dspy.InputField(desc='The name of the user')")
    print("    greeting = dspy.OutputField(desc='A warm, friendly greeting')")
    print("```")
    print()

    class GreetUser(dspy.Signature):
        """Generate a warm greeting for a user."""
        name = dspy.InputField(desc="The name of the user")
        greeting = dspy.OutputField(desc="A warm, friendly greeting")

    print("✓ Signature defined: GreetUser\n")

    # Step 3: Create a module that uses the signature
    print("Step 3: Create a DSPy Module")
    print("```python")
    print("greeter = dspy.Predict(GreetUser)")
    print("```")
    print()

    greeter = dspy.Predict(GreetUser)
    print("✓ Module created: greeter\n")

    # Step 4: Execute the script
    print("Step 4: Run the Script")
    print("```python")
    print("result = greeter(name='Alice')")
    print("print(result.greeting)")
    print("```")
    print()

    # Run it!
    print("🚀 Executing...\n")
    result = greeter(name="Alice")

    print(f"📤 Input: name = 'Alice'")
    print(f"📥 Output: {result.greeting}\n")

    # ============================================================
    # PART 3: Understanding What Just Happened
    # ============================================================

    print("=" * 50)
    print("PART 3: What Makes This Different?")
    print("=" * 50)
    print("""
1. STRUCTURED: We defined exact input/output fields
2. REPEATABLE: Same inputs give consistent outputs
3. PROGRAMMATIC: It's a function call, not a conversation
4. COMPOSABLE: This module can be chained with others
5. OPTIMIZABLE: DSPy can automatically improve this

This is the fundamental shift: We're SCRIPTING interactions,
not having conversations. The LLM becomes a function in our
program, not a chat partner.
    """)

    # ============================================================
    # PART 4: Try It Yourself
    # ============================================================

    print("=" * 50)
    print("PART 4: Your Turn!")
    print("=" * 50)
    print("""
Modify this lesson to:
1. Change the name from 'Alice' to your name
2. Add a 'style' input field (formal/casual/funny)
3. Create a different signature for a different task

Run again with: python run.py lesson 01_hello_dspy
    """)

    return {
        "lesson": "01_hello_dspy",
        "concepts": ["Signatures", "Predict", "Scripting vs Prompting"],
        "success": True
    }

if __name__ == "__main__":
    main()