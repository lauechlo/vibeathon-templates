# 💻 Code Learning Companion

**Difficulty**: Advanced (6-10 hours to extend)
**Completion**: 60% (Core features working, advanced features ready to implement)

## 🎯 What You'll Build

An AI-powered coding tutor that uses Socratic teaching methods to help students learn programming without just giving away answers. It analyzes code, asks guiding questions, generates practice problems, and provides step-by-step debugging guidance.

**Perfect for**: CS students, anyone learning to code, coding bootcamps

## ✨ Core Features (Already Implemented)

- ✅ Code analysis with bug detection
- ✅ Socratic questioning system (asks questions instead of giving answers)
- ✅ Interactive code visualization (algorithm step-through)
- ✅ Practice problem generator at different difficulty levels
- ✅ Concept explanation with visual artifacts
- ✅ Extended thinking for complex debugging scenarios

## 🚀 Advanced Features (TODO - You'll Build These!)

- [ ] **Adaptive Difficulty**: Track student progress and adjust problem difficulty
- [ ] **Test Case Generator**: Auto-generate comprehensive test cases for student code
- [ ] **Code Review Mode**: Detailed code review with learning-focused feedback
- [ ] **Algorithm Visualizer**: Step-by-step visualization of algorithm execution
- [ ] **Concept Mastery Tracker**: Track which concepts student has mastered
- [ ] **Multi-Language Support**: Support Python, Java, C++, JavaScript
- [ ] **Peer Comparison**: Anonymous comparison with how others solved the problem
- [ ] **Hint System**: Progressive hints that reveal more as student struggles

## 🧠 What You'll Learn

### AI Techniques
- **Socratic dialogue**: Teaching through questions, not answers
- **Extended thinking**: Deep code analysis before responding
- **Artifacts**: Interactive code visualizations and diagrams
- **Educational AI**: Scaffolding student learning
- **Code parsing**: Analyzing code structure without execution

### Software Engineering
- Abstract Syntax Tree (AST) parsing
- Code pattern recognition
- Test case generation strategies
- Algorithm complexity analysis
- Educational technology design

## 🛠️ Tech Stack

- **Claude API**: Sonnet 4.5 with extended thinking
- **Streamlit**: Web interface
- **Python AST**: Code parsing and analysis
- **Artifacts**: Interactive code visualizations

## 📦 Installation

```bash
# Navigate to this template
cd advanced/11-code-learning-companion

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# Run the app
streamlit run app.py
```

## 🎮 How to Use

### For Students Getting Stuck on Assignments

1. **Paste your buggy code** into the code editor
2. **Describe what you're trying to do**
3. **Get Socratic questions** that guide you to the solution
4. **Request hints** if you're still stuck
5. **See algorithm visualizations** to understand how it should work

### For Practice and Learning

1. **Choose a concept** (e.g., "recursion", "sorting", "dynamic programming")
2. **Set difficulty level** (beginner, intermediate, advanced)
3. **Generate practice problem**
4. **Solve it and submit for analysis**
5. **Get feedback** focused on learning, not just correctness

## 📝 Example Interactions

### Debugging Help (Socratic Method)

**Student Code:**
```python
def factorial(n):
    if n == 0:
        return 0
    return n * factorial(n - 1)
```

**❌ Bad AI Response (just gives answer):**
"The base case is wrong. It should return 1, not 0."

**✅ Good AI Response (Socratic):**
"Let's think about this together:
1. What should factorial(0) equal mathematically?
2. If factorial(0) returns 0, what happens to factorial(1)?
3. Try tracing through factorial(3) with your current code. What value do you get?"

### Concept Explanation

**Student:** "Explain recursion like I'm 5"

**Response with Artifact:**
"Recursion is like a Russian nesting doll! 🪆

[Interactive visualization showing:]
- Each function call as a doll opening
- Base case as the smallest doll
- Return values building back up

Let me show you with a visual..."

## 🏗️ Architecture

```
Student submits code
    ↓
Parse with Python AST
    ↓
Identify bugs/patterns
    ↓
[EXTENDED THINKING ENABLED]
Generate Socratic questions
    ↓
Student responds
    ↓
Provide progressive hints
    ↓
Generate visualization artifact (if helpful)
    ↓
Track concept mastery
```

## 📝 Code Structure

```python
app.py
├── parse_code()                  # AST parsing and analysis
├── identify_bugs()               # Detect common errors
├── generate_socratic_questions() # Create guiding questions
├── create_visualization()        # Algorithm visualization artifact
├── generate_practice_problem()   # Create practice problems
├── provide_hint()                # Progressive hint system
├── analyze_solution()            # Student solution analysis
└── main()                        # Streamlit UI
```

## 🎨 Artifacts You'll Create

### 1. Algorithm Visualization (HTML/SVG)
```
Step-by-step animation showing:
- Variable states at each step
- Function call stack
- Array/list transformations
- Recursion tree
```

### 2. Concept Explanation Diagrams (SVG)
```
Visual explanations of:
- Recursion as nested boxes
- Sorting algorithms with animations
- Data structure operations
```

### 3. Test Case Matrix (HTML Table)
```
| Input | Expected | Your Output | Status |
| [1,2,3] | 6 | 6 | ✅ Pass |
| [] | 0 | Error | ❌ Fail |
```

### 4. Code Complexity Analysis (Interactive Chart)
```
Time/space complexity visualization
Comparison with optimal solution
```

## 🚧 TODOs for You to Implement

### TODO 1: Adaptive Difficulty System (2-3 hours)
**File**: `app.py`, function `adapt_difficulty()`

Track student performance and adjust problem difficulty automatically.

**Your task:**
1. Create a simple student profile in session state
2. Track: problems attempted, problems solved, concepts mastered, time spent
3. Implement difficulty scoring algorithm:
   - If student solves 3 problems in a row → increase difficulty
   - If student fails 2 in a row → decrease difficulty
   - Track response time (fast = maybe too easy)
4. Adjust next problem generation based on performance
5. Create visualization showing progress over time (artifact)

**Hints:**
- Use `st.session_state.student_profile` to persist data
- Weight recent performance more than old attempts
- Consider concept-specific difficulty (good at loops, weak at recursion)

### TODO 2: Test Case Generator (2-3 hours)
**File**: `app.py`, function `generate_test_cases()`

Automatically generate comprehensive test cases for any problem.

**Your task:**
1. Given a problem description and function signature, generate:
   - Normal cases (typical inputs)
   - Edge cases (empty, single element, maximum size)
   - Corner cases (negative numbers, special values)
   - Error cases (invalid input types)

2. Use extended thinking to reason about what cases are needed

3. Format as interactive HTML table artifact showing:
   - Input, Expected Output, Explanation
   - Coverage (which cases test which aspects)

4. Generate Python code for test cases (students can copy-paste)

**Hints:**
- Prompt Claude with problem description
- Ask for "comprehensive test suite covering all edge cases"
- Include explanation of *why* each test case matters
- Consider property-based testing concepts

### TODO 3: Algorithm Visualizer (3-4 hours)
**File**: `app.py`, function `visualize_algorithm()`

Create step-by-step visualizations of algorithm execution.

**Your task:**
1. Parse student's code to understand algorithm structure
2. Simulate execution step-by-step (or use Claude to describe steps)
3. Generate interactive HTML/JavaScript artifact showing:
   - Current line of code highlighted
   - Variable values at each step
   - For arrays: visual representation of swaps/comparisons
   - For recursion: call stack visualization
   - For trees/graphs: node traversal animation

4. Add controls: Play, Pause, Step Forward, Step Back

5. Support common algorithms:
   - Sorting (bubble, merge, quick)
   - Searching (binary, linear)
   - Recursion (factorial, fibonacci, tree traversal)
   - Dynamic programming (knapsack, LCS)

**Hints:**
- Use HTML5 Canvas or SVG for visualization
- JavaScript for animation controls
- Simplified execution trace (don't need full Python interpreter)
- Claude can generate JavaScript code for visualization

### TODO 4: Concept Mastery Tracker (1-2 hours)
**File**: `app.py`, function `track_mastery()`

Track which programming concepts the student has mastered.

**Your task:**
1. Define core concepts (e.g., loops, recursion, arrays, OOP, etc.)
2. Tag each problem/question with relevant concepts
3. Track student performance per concept:
   - Attempts, success rate, time to solve
   - Spaced repetition: when did they last practice this?
4. Create mastery visualization (artifact):
   - Skill tree or radar chart
   - Color-coded (red = needs practice, green = mastered)
   - Recommendations for what to practice next
5. Implement spaced repetition: suggest reviewing concepts after X days

**Hints:**
- Use a simple scoring system (0-100 per concept)
- Weight recent performance more
- Consider creating a "study path" based on prerequisites
- Gamification: badges for mastering concepts

## 💡 Extension Ideas

1. **Code Golf Mode**: Challenge students to solve in fewest characters
2. **Multiplayer**: Students compete on same problem, leaderboard
3. **Voice Mode**: Verbal explanations of concepts (future)
4. **IDE Integration**: VS Code extension for inline help
5. **Video Tutorials**: Generate links to relevant video explanations
6. **Code Translation**: Convert between languages (Python ↔ Java)
7. **Interview Prep**: Practice common interview questions with hints
8. **Pair Programming**: AI acts as pair programming partner

## 🎯 Success Criteria

Your implementation is successful when:
- ✅ Socratic questioning works (doesn't give direct answers)
- ✅ Students can get progressively harder problems as they improve
- ✅ Test case generation covers edge cases comprehensively
- ✅ Algorithm visualizations are clear and educational
- ✅ Concept mastery tracker shows meaningful progress over time
- ✅ Students report they're *learning*, not just getting answers

## 📚 Helpful Resources

- [Claude API Documentation](https://docs.anthropic.com/)
- [Python AST Module](https://docs.python.org/3/library/ast.html)
- [Socratic Teaching Method](https://en.wikipedia.org/wiki/Socratic_method)
- [Spaced Repetition Systems](https://en.wikipedia.org/wiki/Spaced_repetition)
- [Algorithm Visualization](https://visualgo.net/)

## 🏆 Portfolio Tips

When showcasing this project:
1. **Demo the Socratic approach**: Show how it guides, not tells
2. **Highlight visualizations**: Algorithm animations are impressive
3. **Show learning progression**: Demonstrate adaptive difficulty
4. **Explain pedagogy**: Discuss educational AI design choices
5. **Metrics**: If possible, show effectiveness (students improved X%)

## 🐛 Common Issues

**Issue**: AI gives away the answer instead of asking questions
**Solution**: Stronger system prompt emphasizing Socratic method. Include examples.

**Issue**: Algorithm visualization doesn't work for complex code
**Solution**: Start with simple algorithms (sorting, searching). Build complexity gradually.

**Issue**: Test case generation misses edge cases
**Solution**: Use extended thinking. Provide few-shot examples of comprehensive test suites.

**Issue**: Students frustrated by questions, want direct answers
**Solution**: Add "hint" button that gives progressively more direct help.

## 🎉 Next Steps

After completing this template:
1. Test with real students and iterate based on feedback
2. Add support for more programming languages
3. Create a study curriculum (30-day coding challenge)
4. Build teacher dashboard to monitor student progress
5. Publish as an educational tool for coding bootcamps!

---

**Happy teaching!** 👨‍🏫

The best way to learn is to build this yourself - check the TODOs in `app.py`!
