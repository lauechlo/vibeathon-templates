"""
Code Learning Companion
Advanced Template - 60% Complete

An AI tutor that uses Socratic teaching to help students learn programming.
Instead of giving answers, it asks guiding questions and provides visualizations.

COMPLETED FEATURES:
✅ Code analysis and bug detection
✅ Socratic questioning system
✅ Practice problem generator
✅ Concept explanations with visual artifacts
✅ Extended thinking for complex analysis

YOUR TODOs:
🚧 Adaptive difficulty based on student performance
🚧 Comprehensive test case generator
🚧 Algorithm step-by-step visualizer
🚧 Concept mastery tracking system
"""

import streamlit as st
import anthropic
import os
from dotenv import load_dotenv
import ast
import json

# Load environment variables
load_dotenv()

# Initialize Claude client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Configure Streamlit page
st.set_page_config(
    page_title="Code Learning Companion",
    page_icon="💻",
    layout="wide"
)

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'student_profile' not in st.session_state:
    st.session_state.student_profile = {
        'problems_attempted': 0,
        'problems_solved': 0,
        'current_difficulty': 'beginner',
        'concepts_mastered': []
    }


def parse_code(code: str) -> dict:
    """
    Parse Python code using AST to identify structure and potential issues.

    Args:
        code: Python code string

    Returns:
        dict with parsing results and identified issues
    """
    try:
        tree = ast.parse(code)

        # Extract information about the code
        functions = []
        classes = []
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    'name': node.name,
                    'args': [arg.arg for arg in node.args.args],
                    'line': node.lineno
                })
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
            elif isinstance(node, ast.Import):
                imports.extend([alias.name for alias in node.names])

        return {
            'valid': True,
            'functions': functions,
            'classes': classes,
            'imports': imports,
            'line_count': len(code.split('\n'))
        }

    except SyntaxError as e:
        return {
            'valid': False,
            'error': str(e),
            'line': e.lineno,
            'message': e.msg
        }


def generate_socratic_questions(code: str, problem_description: str, parse_result: dict) -> str:
    """
    Generate Socratic questions to guide student thinking instead of giving answers.

    This is the CORE of the educational approach - we ask questions, not give solutions.
    """
    prompt = f"""You are an expert programming tutor using the Socratic method.

IMPORTANT: Do NOT give away the answer. Instead, ask 3-4 guiding questions that help the student discover the solution themselves.

Student's code:
```python
{code}
```

What they're trying to do:
{problem_description}

Code analysis:
{json.dumps(parse_result, indent=2)}

Generate 3-4 Socratic questions that:
1. Guide them to identify the problem themselves
2. Make them think about edge cases
3. Help them understand the concept, not just fix the bug
4. Build on each other (each question leads to the next)

Use a friendly, encouraging tone. Include hints like "What would happen if..." or "Have you considered..."

End with: "Try working through these questions, then let me know what you discover!"
"""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2000,
        thinking={
            "type": "enabled",
            "budget_tokens": 5000
        },
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract text response
    for block in response.content:
        if block.type == "text":
            return block.text

    return "Could not generate questions. Please try again."


def create_concept_visualization(concept: str, difficulty: str = "beginner") -> str:
    """
    Create an interactive visual explanation of a programming concept.

    Returns HTML artifact with visualization.
    """
    prompt = f"""Create an interactive HTML visualization explaining the concept: {concept}

Difficulty level: {difficulty}

Requirements:
1. Use simple, clear visuals (SVG or HTML/CSS)
2. Include step-by-step animation or interactive elements
3. Use analogies appropriate for {difficulty} level
4. Add brief text explanations alongside visuals
5. Use friendly colors and clear typography
6. Make it engaging and fun!

For example, if explaining recursion:
- Show Russian nesting dolls or infinite mirrors
- Animate function calls going down and returning up
- Highlight base case

Return ONLY the complete HTML code with embedded CSS/JavaScript."""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


def generate_practice_problem(concept: str, difficulty: str) -> dict:
    """
    Generate a practice coding problem at specified difficulty level.

    Args:
        concept: Programming concept (e.g., "recursion", "loops", "arrays")
        difficulty: "beginner", "intermediate", or "advanced"

    Returns:
        dict with problem description, hints, and solution outline
    """
    prompt = f"""Generate a {difficulty} level coding problem focused on: {concept}

Requirements:
1. Clear problem statement
2. Input/output examples (at least 3)
3. Constraints and edge cases to consider
4. 2-3 progressive hints (reveal more as student struggles)
5. DO NOT include the full solution - students should solve it

Format as JSON:
{{
    "title": "Problem title",
    "description": "Clear problem description",
    "examples": [
        {{"input": "...", "output": "...", "explanation": "..."}},
        ...
    ],
    "constraints": ["...", "..."],
    "hints": [
        "First hint (vague)",
        "Second hint (more specific)",
        "Third hint (very specific but not solution)"
    ],
    "difficulty": "{difficulty}",
    "concepts": ["{concept}"]
}}
"""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=3000,
        thinking={
            "type": "enabled",
            "budget_tokens": 5000
        },
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract text and parse JSON
    try:
        import re
        text = response.content[0].text if isinstance(response.content[0], anthropic.types.TextBlock) else ""
        for block in response.content:
            if block.type == "text":
                text = block.text
                break

        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except:
        pass

    # Fallback
    return {
        "title": f"{concept.title()} Practice Problem",
        "description": "Generate a new problem to practice " + concept,
        "examples": [],
        "hints": ["Think about the base case", "Consider edge cases", "Try tracing through manually"]
    }


def analyze_solution(problem: dict, student_code: str) -> str:
    """
    Analyze student's solution to a practice problem.

    Uses Socratic method - points out issues with questions, not direct corrections.
    """
    prompt = f"""You are a programming tutor reviewing a student's solution.

Problem:
{json.dumps(problem, indent=2)}

Student's code:
```python
{student_code}
```

Provide feedback that:
1. Celebrates what they did well (be specific!)
2. Asks questions about potential issues (don't just point them out)
3. Suggests test cases they should try
4. Guides them to optimize if needed
5. Encourages them to keep learning

Use the Socratic method - guide with questions, not statements.

If the solution is correct, still ask questions that deepen understanding:
- "Why did you choose this approach?"
- "What's the time complexity? Can you explain why?"
- "What would happen if the input was [edge case]?"
"""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2000,
        thinking={
            "type": "enabled",
            "budget_tokens": 5000
        },
        messages=[{"role": "user", "content": prompt}]
    )

    for block in response.content:
        if block.type == "text":
            return block.text

    return "Could not analyze solution."


# ============================================================================
# TODO SECTION FOR STUDENTS
# ============================================================================

def adapt_difficulty(student_profile: dict) -> str:
    """
    TODO #1: Adaptive Difficulty System (2-3 hours)

    Adjust problem difficulty based on student performance.

    Your task:
    1. Track student performance metrics in session state:
       - Problems attempted vs solved
       - Average time per problem
       - Concepts mastered
       - Recent success rate (last 5 problems)

    2. Implement difficulty adjustment algorithm:
       - If last 3 problems solved quickly → increase difficulty
       - If last 2 problems failed → decrease difficulty
       - If struggling with same concept repeatedly → suggest different concept

    3. Return recommended difficulty: "beginner", "intermediate", or "advanced"

    4. Create visualization showing:
       - Performance over time (line chart)
       - Current level and progress to next level
       - Concepts mastered (skill tree or radar chart)

    Hints:
    - Use st.session_state.student_profile to persist data
    - Consider time spent (fast solve = maybe too easy)
    - Weight recent performance more than old (exponential decay)
    - Return HTML artifact showing progress visualization
    """
    # YOUR CODE HERE
    st.warning("🚧 TODO #1: Implement adaptive difficulty tracking!")

    # Default behavior for now
    return student_profile.get('current_difficulty', 'beginner')


def generate_test_cases(problem_description: str, function_signature: str):
    """
    TODO #2: Test Case Generator (2-3 hours)

    Generate comprehensive test cases for any coding problem.

    Your task:
    1. Given a problem description and function signature, create:
       - Normal cases (typical inputs)
       - Edge cases (empty input, single element, very large)
       - Corner cases (negative numbers, special values like 0)
       - Error cases (invalid types, None, etc.)

    2. Use extended thinking to reason about coverage

    3. Generate test cases as:
       - Interactive HTML table (artifact) showing all cases
       - Python code students can copy-paste to test their solution
       - Explanation of what each case tests

    4. Aim for 100% code coverage

    Example return format:
    {
        'test_cases': [
            {
                'input': '[1, 2, 3]',
                'expected_output': '6',
                'category': 'normal',
                'tests': 'basic functionality'
            },
            {
                'input': '[]',
                'expected_output': '0',
                'category': 'edge',
                'tests': 'empty input handling'
            }
        ],
        'python_code': 'def test_...',
        'artifact_html': '<table>...</table>'
    }

    Hints:
    - Ask Claude to "think like a QA engineer"
    - Use extended thinking for comprehensive coverage
    - Include explanation of *why* each test matters
    - Consider boundary value analysis
    """
    # YOUR CODE HERE
    st.warning("🚧 TODO #2: Implement comprehensive test case generation!")
    return None


def visualize_algorithm(code: str, algorithm_type: str):
    """
    TODO #3: Algorithm Visualizer (3-4 hours)

    Create step-by-step visualization of algorithm execution.

    Your task:
    1. Support common algorithms:
       - Sorting: bubble sort, merge sort, quick sort
       - Searching: binary search, linear search
       - Recursion: factorial, fibonacci, tree traversal
       - Arrays: reverse, rotate, sliding window

    2. Generate execution trace:
       - Each step of algorithm execution
       - Variable values at each step
       - For arrays: show swaps, comparisons visually
       - For recursion: show call stack

    3. Create interactive HTML artifact with:
       - Step-by-step animation (play/pause controls)
       - Current line highlighted
       - Variable inspector
       - For arrays: visual bars or boxes
       - For recursion: tree visualization

    4. Use JavaScript for interactivity:
       - Play/Pause button
       - Step Forward/Back
       - Speed control
       - Explanation of current step

    Example structure:
    - Parse code to understand algorithm
    - Generate execution trace (or ask Claude to describe steps)
    - Create HTML with Canvas/SVG for visualization
    - Add JavaScript controls

    Hints:
    - Start with simpler algorithms (bubble sort, linear search)
    - Don't need full Python interpreter - simulate execution
    - Claude can generate JavaScript code for animation
    - Use color coding (green=current, red=comparison, blue=sorted)
    """
    # YOUR CODE HERE
    st.warning("🚧 TODO #3: Implement algorithm step-by-step visualization!")
    return "<p>Algorithm visualization not yet implemented</p>"


def track_mastery(concept: str, success: bool):
    """
    TODO #4: Concept Mastery Tracker (1-2 hours)

    Track which programming concepts student has mastered.

    Your task:
    1. Define core concepts:
       concepts = {
           'loops': {'for', 'while', 'nested_loops'},
           'conditionals': {'if', 'elif', 'else', 'ternary'},
           'data_structures': {'list', 'dict', 'set', 'tuple'},
           'algorithms': {'sorting', 'searching', 'recursion'},
           'oop': {'classes', 'inheritance', 'polymorphism'},
           ...
       }

    2. Track per concept:
       - Attempts
       - Success rate
       - Last practiced date (for spaced repetition)
       - Mastery score (0-100)

    3. Update mastery score based on:
       - Recent performance (weight more)
       - Spaced repetition (needs review after X days)
       - Difficulty level of problems solved

    4. Create visualization artifact:
       - Skill tree (nodes = concepts, connections = prerequisites)
       - Radar chart (axes = concept categories)
       - Progress bars for each concept
       - Recommendations: "Practice recursion next!"

    5. Implement spaced repetition:
       - Suggest reviewing concepts after: 1 day, 3 days, 1 week, 2 weeks
       - Notify when concept needs review

    Example structure:
    st.session_state.concept_mastery = {
        'loops': {
            'attempts': 10,
            'successes': 8,
            'last_practiced': '2024-01-15',
            'mastery_score': 75,
            'needs_review': False
        },
        ...
    }

    Hints:
    - Simple scoring: mastery = (successes / attempts) * 100
    - Decay score over time if not practiced
    - Use st.session_state for persistence
    - Create visual skill tree with HTML/SVG
    """
    # YOUR CODE HERE
    st.warning("🚧 TODO #4: Implement concept mastery tracking!")
    pass


# ============================================================================
# STREAMLIT UI
# ============================================================================

def main():
    # Header
    st.title("💻 Code Learning Companion")
    st.markdown("*Learn to code with AI-powered Socratic teaching*")

    # Sidebar
    with st.sidebar:
        st.header("👤 Student Profile")

        profile = st.session_state.student_profile
        st.metric("Problems Attempted", profile['problems_attempted'])
        st.metric("Problems Solved", profile['problems_solved'])
        st.metric("Current Level", profile['current_difficulty'].title())

        if profile['concepts_mastered']:
            st.write("**Concepts Mastered:**")
            for concept in profile['concepts_mastered']:
                st.write(f"✅ {concept}")

        st.markdown("---")

        st.info("💡 **Teaching Philosophy**: I won't give you the answer - I'll guide you to discover it yourself!")

    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🐛 Debug Help",
        "📚 Learn Concept",
        "💪 Practice",
        "📊 Progress"
    ])

    # TAB 1: Debug Help (Socratic Method)
    with tab1:
        st.header("Get Help Debugging Your Code")
        st.markdown("*I'll ask you guiding questions instead of just fixing it for you*")

        col1, col2 = st.columns([2, 1])

        with col1:
            problem_desc = st.text_area(
                "What are you trying to do?",
                placeholder="e.g., Write a function that returns the factorial of a number",
                height=100
            )

            student_code = st.text_area(
                "Paste your code here:",
                placeholder="def factorial(n):\n    # your code here",
                height=300,
                key="debug_code"
            )

        with col2:
            st.markdown("### 💡 Tips")
            st.markdown("""
            **Before asking:**
            1. Describe what you expected
            2. Describe what actually happens
            3. Share what you've tried

            **I will:**
            - Ask guiding questions
            - Help you think through it
            - Suggest what to test

            **I won't:**
            - Give you the answer
            - Write the code for you
            """)

        if st.button("🤔 Help Me Think Through This", type="primary"):
            if student_code and problem_desc:
                with st.spinner("Analyzing your code..."):
                    # Parse the code
                    parse_result = parse_code(student_code)

                    # Show code analysis
                    with st.expander("🔍 Code Analysis", expanded=False):
                        if parse_result['valid']:
                            st.success("✅ Your code has valid syntax!")
                            st.json(parse_result)
                        else:
                            st.error(f"❌ Syntax Error on line {parse_result['line']}: {parse_result['message']}")
                            st.info("💡 Fix the syntax error first, then I can help with logic!")

                    # Generate Socratic questions
                    if parse_result['valid']:
                        questions = generate_socratic_questions(
                            student_code,
                            problem_desc,
                            parse_result
                        )

                        st.subheader("🤔 Let's Think Through This Together")
                        st.markdown(questions)

                        # Follow-up conversation
                        st.markdown("---")
                        st.subheader("💬 Your Response")
                        student_response = st.text_area(
                            "What did you discover? What are your thoughts?",
                            placeholder="Share your thinking here...",
                            key="student_response"
                        )

                        if st.button("💬 Continue Conversation"):
                            if student_response:
                                # Continue Socratic dialogue
                                st.info("🚧 Multi-turn conversation coming soon! For now, revise your code and submit again.")
            else:
                st.warning("Please provide both your code and a description of what you're trying to do!")

    # TAB 2: Learn Concept
    with tab2:
        st.header("Learn Programming Concepts")
        st.markdown("*Visual explanations with interactive diagrams*")

        col1, col2 = st.columns([2, 1])

        with col1:
            concept = st.selectbox(
                "Choose a concept to learn:",
                [
                    "Recursion",
                    "Binary Search",
                    "Sorting Algorithms",
                    "Dynamic Programming",
                    "Big O Notation",
                    "Linked Lists",
                    "Trees and Graphs",
                    "Hash Tables",
                    "Stack and Queue",
                    "Custom..."
                ]
            )

            if concept == "Custom...":
                concept = st.text_input("Enter concept:", "loops")

            difficulty = st.radio(
                "Your current level:",
                ["beginner", "intermediate", "advanced"],
                horizontal=True
            )

        with col2:
            st.markdown("### 📖 Learning Modes")
            st.markdown("""
            **Visual**: Interactive diagrams
            **Analogy**: Real-world comparisons
            **Example**: Code walkthrough
            **Practice**: Try it yourself
            """)

        if st.button("🎨 Generate Visual Explanation", type="primary"):
            with st.spinner(f"Creating visual explanation of {concept}..."):
                visualization = create_concept_visualization(concept, difficulty)

                st.subheader(f"📊 Understanding {concept}")
                st.components.v1.html(visualization, height=600, scrolling=True)

                # Algorithm visualization (TODO)
                st.markdown("---")
                st.subheader("🎬 Step-by-Step Animation")
                st.info("🚧 TODO #3: Implement algorithm step-by-step visualizer!")

    # TAB 3: Practice Problems
    with tab3:
        st.header("Practice Coding Problems")
        st.markdown("*Get problems tailored to your level*")

        col1, col2 = st.columns(2)

        with col1:
            practice_concept = st.selectbox(
                "Concept to practice:",
                ["loops", "recursion", "arrays", "sorting", "searching", "dynamic programming", "graphs"]
            )

        with col2:
            practice_difficulty = st.selectbox(
                "Difficulty:",
                ["beginner", "intermediate", "advanced"]
            )

        if st.button("🎲 Generate Practice Problem", type="primary"):
            with st.spinner("Generating problem..."):
                problem = generate_practice_problem(practice_concept, practice_difficulty)
                st.session_state.current_problem = problem
                st.session_state.student_profile['problems_attempted'] += 1

        # Display current problem
        if 'current_problem' in st.session_state:
            problem = st.session_state.current_problem

            st.subheader(f"📝 {problem.get('title', 'Practice Problem')}")
            st.markdown(problem.get('description', ''))

            # Examples
            if 'examples' in problem and problem['examples']:
                with st.expander("📌 Examples", expanded=True):
                    for i, ex in enumerate(problem['examples'], 1):
                        st.markdown(f"**Example {i}:**")
                        st.code(f"Input: {ex.get('input', '')}\nOutput: {ex.get('output', '')}")
                        if 'explanation' in ex:
                            st.caption(ex['explanation'])

            # Constraints
            if 'constraints' in problem and problem['constraints']:
                with st.expander("⚠️ Constraints"):
                    for constraint in problem['constraints']:
                        st.write(f"• {constraint}")

            # Hints (progressive)
            if 'hints' in problem and problem['hints']:
                st.markdown("### 💡 Hints")
                for i, hint in enumerate(problem['hints'], 1):
                    with st.expander(f"Hint {i} (click to reveal)"):
                        st.write(hint)

            # Solution submission
            st.markdown("### 💻 Your Solution")
            solution_code = st.text_area(
                "Write your code here:",
                placeholder="def solution(...):\n    # your code here\n    pass",
                height=300,
                key="solution_code"
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Submit Solution"):
                    if solution_code:
                        with st.spinner("Analyzing your solution..."):
                            feedback = analyze_solution(problem, solution_code)
                            st.markdown("### 📝 Feedback")
                            st.markdown(feedback)

                            # Update student profile (simplified - should track success)
                            # In TODO #1, you'll make this smarter
                            st.session_state.student_profile['problems_solved'] += 1
                    else:
                        st.warning("Please write your solution first!")

            with col2:
                if st.button("🧪 Generate Test Cases"):
                    st.info("🚧 TODO #2: Implement test case generator!")

    # TAB 4: Progress Tracking
    with tab4:
        st.header("📊 Your Learning Progress")
        st.markdown("*Track your growth as a programmer*")

        st.info("🚧 TODO #4: Implement concept mastery tracker with visualizations!")

        # Basic stats for now
        profile = st.session_state.student_profile

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Problems", profile['problems_attempted'])
        with col2:
            st.metric("Solved", profile['problems_solved'])
        with col3:
            if profile['problems_attempted'] > 0:
                success_rate = (profile['problems_solved'] / profile['problems_attempted']) * 100
                st.metric("Success Rate", f"{success_rate:.0f}%")
            else:
                st.metric("Success Rate", "N/A")

        st.markdown("---")
        st.subheader("🎯 What to Build")
        st.markdown("""
        Complete the TODOs to add:

        1. **Adaptive Difficulty** (TODO #1)
           - Track performance over time
           - Automatically adjust problem difficulty
           - Visualize learning progress

        2. **Test Case Generator** (TODO #2)
           - Comprehensive test suites
           - Edge case coverage
           - Copy-paste ready Python tests

        3. **Algorithm Visualizer** (TODO #3)
           - Step-by-step animations
           - Interactive playback controls
           - Visual debugging

        4. **Concept Mastery Tracker** (TODO #4)
           - Skill tree visualization
           - Spaced repetition reminders
           - Personalized learning path
        """)


if __name__ == "__main__":
    main()
