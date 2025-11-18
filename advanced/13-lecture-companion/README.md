# 🎓 Interactive Lecture Companion

**Difficulty**: Advanced (8-12 hours to extend)
**Completion**: 60% (Core features working, advanced features ready to implement)

## 🎯 What You'll Build

A real-time AI companion that helps you stay engaged during lectures, automatically enhances your notes, generates questions, detects confusion, and creates comprehensive summaries - all while the lecture is happening!

**Perfect for**: Large lectures, difficult courses, online classes, students who struggle with attention

## ✨ Core Features (Already Implemented)

- ✅ Real-time note enhancement (you type rough notes → AI cleans them up)
- ✅ Automatic question generation during lecture pauses
- ✅ Concept linking (connects to previous lectures)
- ✅ Post-lecture summary generation with key points
- ✅ Gap analysis (what was covered vs what you noted)
- ✅ Interactive timeline visualization of lecture flow

## 🚀 Advanced Features (TODO - You'll Build These!)

- [ ] **Confusion Detection**: Identifies when notes become unclear/confused
- [ ] **Proactive Explanations**: Auto-explains concepts if notes suggest confusion
- [ ] **Multi-Lecture Context**: References previous lectures in same course
- [ ] **Study Recommendations**: "Review recursion from Lecture 5"
- [ ] **Attention Tracker**: Monitors engagement level, suggests breaks
- [ ] **Collaborative Notes**: Merge notes with classmates
- [ ] **Audio Transcription**: Future - transcribe lecture audio
- [ ] **Slide Integration**: Auto-match notes to professor's slides

## 🧠 What You'll Learn

### AI Techniques
- **Streaming responses**: Real-time text enhancement
- **Extended thinking**: Deep lecture analysis
- **Long context management**: Track full 90-minute lecture
- **Temporal reasoning**: Link concepts across time
- **Incremental summarization**: Build summary as lecture progresses
- **Artifacts**: Timeline visualizations, concept maps

### Software Engineering
- Real-time text processing
- Session state management
- Incremental data structures
- Timeline visualization
- WebSocket-like patterns (via Streamlit)
- Performance optimization for long sessions

## 🛠️ Tech Stack

- **Claude API**: Sonnet 4.5 with extended thinking
- **Streamlit**: Web interface with session state
- **Artifacts**: Timeline visualizations, concept maps
- **Real-time processing**: Streaming enhancements

## 📦 Installation

```bash
# Navigate to this template
cd advanced/13-lecture-companion

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# Run the app
streamlit run app.py
```

## 🎮 How to Use

### During a Lecture

1. **Start Session**: Create new lecture session (e.g., "COS 126 - Lecture 12")
2. **Type Notes**: Enter rough notes as you listen
3. **AI Enhancement**: Your notes get cleaned up in real-time
4. **Generate Questions**: Click "Generate Question" during pauses
5. **Flag Confusion**: Mark confusing sections for review
6. **See Connections**: AI highlights links to previous material

### After the Lecture

1. **Review Summary**: Get comprehensive lecture summary
2. **Identify Gaps**: See what was covered but you didn't note
3. **Study Plan**: Get personalized review recommendations
4. **Export Notes**: Download enhanced notes with timeline

## 📝 Example Workflow

**Your Rough Notes (during lecture):**
```
prof talking bout recursion
base case - when stop
recursive case - calls itself
example factorial
```

**AI-Enhanced Notes (real-time):**
```
📌 RECURSION

The professor is explaining recursion, which has two key components:

1. **Base Case**: The stopping condition that prevents infinite loops
   - This is where the recursion ends
   - Must be simple and directly solvable

2. **Recursive Case**: Where the function calls itself
   - Breaks problem into smaller sub-problems
   - Each call should move closer to base case

Example discussed: factorial function
- factorial(n) = n * factorial(n-1)
- Base case: factorial(0) = 1
```

**Auto-Generated Question:**
```
🤔 Check Your Understanding:
"What would happen if you forgot to include a base case in a recursive function?"

[Hint available]
```

## 🏗️ Architecture

```
Student types notes
    ↓
Store in session with timestamp
    ↓
AI enhances notes (streaming)
    ↓
Detect key concepts
    ↓
Check against previous lectures (context)
    ↓
Generate proactive questions/explanations
    ↓
Build incremental summary
    ↓
Create timeline visualization (artifact)
```

## 📝 Code Structure

```python
app.py
├── enhance_notes_realtime()      # Real-time note cleaning
├── generate_question()            # Concept-based questions
├── detect_confusion()             # Confusion detection (TODO)
├── link_to_previous()             # Multi-lecture linking (TODO)
├── create_timeline()              # Timeline visualization artifact
├── generate_summary()             # Post-lecture summary
├── identify_gaps()                # Coverage analysis
└── main()                         # Streamlit UI
```

## 🎨 Artifacts You'll Create

### 1. Lecture Timeline (SVG/HTML)
```
Visual timeline showing:
- Topics covered (color-coded)
- Your note timestamps
- Questions generated
- Confusion flags
- Connections to previous lectures
- Interactive: click to jump to that section
```

### 2. Concept Network (SVG)
```
Graph showing:
- Concepts introduced this lecture
- Links to concepts from previous lectures
- Strength of connections
- Hover for definitions
```

### 3. Study Dashboard (HTML)
```
Post-lecture dashboard with:
- Coverage percentage
- Mastery estimates per concept
- Recommended review topics
- Study time allocation
```

## 🚧 TODOs for You to Implement

### TODO 1: Confusion Detection System (2-3 hours)
**File**: `app.py`, function `detect_confusion()`

Automatically detect when student seems confused based on note quality.

**Your task:**
1. Analyze note patterns that indicate confusion:
   - Incomplete sentences
   - Question marks in notes ("wait what?", "huh?")
   - Repetition of same phrase
   - Notes that don't match topic flow
   - Sudden drop in note detail
   - Time gaps in note-taking

2. Assign confusion score (0-100) per note segment

3. When confusion detected, trigger:
   - Proactive explanation of current concept
   - Suggestion to flag for review
   - Alternative explanation or analogy
   - Related resources

4. Create visualization showing confusion timeline:
   - Green = following well
   - Yellow = slight confusion
   - Red = significant confusion

5. In post-lecture summary, highlight confused sections

**Example detection:**
```
Student notes: "prof said something about pointers??? lost me"

AI response:
🚨 Confusion Detected: Pointers

Let me explain pointers more clearly:
[Clear explanation]

💡 Suggested Action:
- Mark this section for office hours
- Review Chapter 4 in textbook
- Watch supplementary video on pointers
```

**Hints:**
- Use Claude to analyze note quality
- Track note timestamps vs topic progression
- Compare note density (words/minute)
- Look for uncertainty language ("maybe", "I think", "not sure")

### TODO 2: Multi-Lecture Context System (3-4 hours)
**File**: `app.py`, function `link_to_previous_lectures()`

Maintain context across all lectures in a course.

**Your task:**
1. Store all lecture notes in persistent format:
   ```python
   st.session_state.course_lectures = {
       'COS 126': {
           'Lecture 1': {...},
           'Lecture 2': {...},
           ...
       }
   }
   ```

2. When processing current notes:
   - Identify concepts that were introduced in previous lectures
   - Create links: "This connects to Lecture 5 where we learned [X]"
   - Detect when current lecture builds on previous concept

3. Generate "Review Recommendations":
   - "Before studying this lecture, review Lecture 3 (recursion basics)"
   - "This lecture assumes you understand [concept from Lecture 7]"

4. Create course-wide concept map artifact:
   - Shows all lectures as nodes
   - Edges = concept dependencies
   - Click lecture to see notes
   - Highlight current lecture

5. Implement smart search:
   - "Find all lectures where we discussed Big O notation"
   - Show results with context

**Example:**
```
Current note: "Prof explaining merge sort"

AI enhancement:
📌 MERGE SORT

This builds on divide-and-conquer from Lecture 8!

Key points:
[...]

🔗 Related Concepts:
- Recursion (Lecture 5)
- Array manipulation (Lecture 3)
- Time complexity analysis (Lecture 7)
```

**Hints:**
- Use pickle or JSON to persist lecture data
- Create concept index across all lectures
- Use embeddings for semantic search (advanced)
- Maintain course syllabus outline as structure

### TODO 3: Attention Tracker & Break Recommender (1-2 hours)
**File**: `app.py`, function `track_attention()`

Monitor engagement and suggest optimal break times.

**Your task:**
1. Track engagement signals:
   - Note-taking frequency (notes per minute)
   - Note quality over time
   - Time since last note
   - Length of notes (detail vs brief)
   - Question generation requests

2. Calculate attention score (0-100):
   - High: Detailed notes, frequent input, asks questions
   - Medium: Consistent but brief notes
   - Low: Long gaps, very brief notes, no questions

3. Recommend breaks when:
   - Attention score drops below 40
   - After 25-30 minutes (Pomodoro)
   - Natural topic transitions

4. Show attention graph (artifact):
   - Line chart of attention over lecture
   - Color-coded segments
   - Break suggestions marked

5. Gamification (optional):
   - "You stayed focused for 28 minutes! 🎯"
   - "Attention streak: 3 lectures!"

**Example:**
```
[After 28 minutes of lecture]

🧠 Attention Alert

Your note-taking has slowed down. This is a natural attention cycle!

Suggested action:
✅ Take a 2-minute break
✅ Stand up and stretch
✅ Grab water
✅ When you're ready, I'll summarize what you might have missed

[Start Break Timer]
```

**Hints:**
- Calculate rolling average of notes per 5-min window
- Compare current performance to lecture start
- Research Pomodoro technique timing
- Use st.line_chart() for visualization

### TODO 4: Collaborative Notes Feature (2-3 hours)
**File**: `app.py`, function `merge_notes_with_classmates()`

Combine notes from multiple students for comprehensive coverage.

**Your task:**
1. Allow exporting notes as JSON:
   ```json
   {
     "course": "COS 126",
     "lecture_title": "Recursion",
     "timestamp": "2024-01-15",
     "notes": [...],
     "questions": [...],
     "key_concepts": [...]
   }
   ```

2. Import notes from classmates:
   - Upload JSON files
   - Parse and merge content
   - Preserve attribution ("From Alex's notes: ...")

3. Merge strategy:
   - Combine all concepts mentioned
   - Keep best explanation for each concept
   - Flag contradictions ("Alex noted X, but Sarah noted Y")
   - Create comprehensive merged notes

4. Generate "Group Insight" report:
   - Topics covered by all students (core material)
   - Topics covered by few (might have missed)
   - Questions generated across all students
   - Confusion patterns (did everyone struggle here?)

5. Privacy considerations:
   - Anonymous contributions option
   - Don't share personal comments

**Example merged output:**
```
📚 MERGED LECTURE NOTES
From 4 students

Recursion Basics:
- Base case: when to stop (all 4 students noted)
- Recursive case: self-calling (all 4 students noted)

Example - Factorial:
[Synthesis of best explanations from all students]

🤔 Common Confusion:
3/4 students found the tower of Hanoi example confusing
→ Recommended for group review
```

**Hints:**
- Use Claude to merge and synthesize content
- Weight notes by quality/detail
- Create comparison view (side-by-side)
- Consider building simple sharing system

## 💡 Extension Ideas

1. **Audio Transcription**: Use Whisper API to transcribe lectures
2. **Slide Auto-Match**: Match notes to professor's slides
3. **Quiz Generation**: Auto-generate quiz from lecture content
4. **Flashcard Export**: Convert notes to Anki flashcards
5. **Study Group Matching**: Find classmates who struggled with same concepts
6. **Professor Q&A Helper**: Generate thoughtful questions to ask professor
7. **Exam Predictor**: "Based on lecture emphasis, expect questions on..."
8. **Video Timestamp Sync**: If lecture recorded, add video timestamps

## 🎯 Success Criteria

Your implementation is successful when:
- ✅ Notes are enhanced in real-time without lag
- ✅ Confusion detection correctly identifies struggle points
- ✅ Multi-lecture context creates meaningful connections
- ✅ Attention tracking helps maintain focus
- ✅ Merged notes are more comprehensive than individual ones
- ✅ Students report better lecture retention

## 📚 Helpful Resources

- [Claude API Documentation](https://docs.anthropic.com/)
- [Streamlit Session State](https://docs.streamlit.io/library/api-reference/session-state)
- [Cognitive Load Theory](https://www.instructionaldesign.org/theories/cognitive-load/)
- [Pomodoro Technique](https://francescocirillo.com/pages/pomodoro-technique)
- [Note-Taking Research](https://www.apa.org/science/about/psa/2016/04/note-taking)

## 🏆 Portfolio Tips

When showcasing this project:
1. **Live Demo**: Record yourself using it during a real/mock lecture
2. **Before/After**: Show rough notes vs enhanced notes
3. **Metrics**: Show improvement in retention/comprehension
4. **User Testing**: Get feedback from real students
5. **Accessibility**: Highlight how it helps struggling students

## 🐛 Common Issues

**Issue**: Real-time enhancement is too slow
**Solution**: Use streaming responses, limit enhancement frequency

**Issue**: Context management uses too much memory
**Solution**: Summarize older lectures, keep only key concepts

**Issue**: False confusion detection
**Solution**: Tune detection thresholds, add user feedback

**Issue**: Merged notes have redundancy
**Solution**: Better synthesis prompts, de-duplication logic

## 🎉 Next Steps

After completing this template:
1. Test with real lectures across different subjects
2. Gather user feedback and iterate
3. Add subject-specific features (math notation, code syntax)
4. Build mobile app for on-the-go note-taking
5. Partner with university to pilot in classrooms!

---

**Happy learning!** 🎓

This tool can genuinely transform how students experience lectures. Build it well!
