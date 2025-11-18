"""
Interactive Lecture Companion
Advanced Template - 60% Complete

A real-time AI assistant that helps you stay engaged during lectures,
enhances your notes, and ensures you don't miss important concepts.

COMPLETED FEATURES:
✅ Real-time note enhancement
✅ Automatic question generation
✅ Concept linking within lecture
✅ Post-lecture summary generation
✅ Gap analysis (what you missed)
✅ Timeline visualization (artifact)

YOUR TODOs:
🚧 Confusion detection system
🚧 Multi-lecture context tracking
🚧 Attention tracker & break recommender
🚧 Collaborative notes merging
"""

import streamlit as st
import anthropic
import os
from dotenv import load_dotenv
from datetime import datetime
import json

# Load environment variables
load_dotenv()

# Initialize Claude client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Configure Streamlit page
st.set_page_config(
    page_title="Lecture Companion",
    page_icon="🎓",
    layout="wide"
)

# Initialize session state
if 'lecture_session' not in st.session_state:
    st.session_state.lecture_session = None
if 'notes' not in st.session_state:
    st.session_state.notes = []
if 'enhanced_notes' not in st.session_state:
    st.session_state.enhanced_notes = []
if 'questions_generated' not in st.session_state:
    st.session_state.questions_generated = []
if 'lecture_summary' not in st.session_state:
    st.session_state.lecture_summary = ""


def enhance_notes_realtime(rough_notes: str, context: str = "") -> str:
    """
    Enhance student's rough notes in real-time.

    Takes messy, incomplete notes and makes them clear and organized
    while preserving all the information.
    """
    prompt = f"""You are a note-taking assistant helping a student during a lecture.

Context from earlier in the lecture:
{context if context else "This is the first note."}

Student's rough notes:
{rough_notes}

Your task:
1. Clean up the notes - proper grammar, complete sentences
2. Organize with bullet points or numbered lists
3. Add structure (headings if multiple topics)
4. Preserve ALL information the student wrote
5. Highlight key terms in **bold**
6. Add emoji icons for important points (📌, ⚠️, 💡)
7. Keep it concise - this is for quick reference

Return the enhanced notes as formatted markdown."""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


def generate_question_from_content(content: str) -> dict:
    """
    Generate a conceptual question based on lecture content.

    Helps students check their understanding during natural pauses.
    """
    prompt = f"""Based on this lecture content, generate ONE thought-provoking question to test understanding.

Content:
{content}

Requirements:
1. Question should test conceptual understanding, not memorization
2. Should be answerable based on the content
3. Include 2 progressive hints (don't give away answer)
4. Provide explanation of correct answer

Return JSON:
{{
    "question": "...",
    "hints": ["hint 1", "hint 2"],
    "answer": "...",
    "explanation": "..."
}}
"""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    # Parse JSON response
    try:
        import re
        text = response.content[0].text
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except:
        pass

    return {
        "question": "What is the main concept discussed?",
        "hints": ["Think about the topic", "Review your notes"],
        "answer": "Review content",
        "explanation": "Please review the content covered."
    }


def generate_summary(all_notes: list, lecture_title: str) -> str:
    """
    Generate comprehensive lecture summary from all notes.

    Uses extended thinking for deep analysis.
    """
    # Combine all notes
    combined = "\n\n".join([note['enhanced'] for note in all_notes])

    prompt = f"""Generate a comprehensive lecture summary from these enhanced notes.

Lecture: {lecture_title}

Notes:
{combined}

Create a summary with:
1. **Overview** (2-3 sentences)
2. **Key Concepts** (bullet points)
3. **Important Details** (organized by topic)
4. **Formulas/Definitions** (if any)
5. **Examples Discussed** (if any)
6. **Takeaways** (what students should remember)

Format as markdown with clear headings."""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=3000,
        thinking={
            "type": "enabled",
            "budget_tokens": 5000
        },
        messages=[{"role": "user", "content": prompt}]
    )

    for block in response.content:
        if block.type == "text":
            return block.text

    return "Could not generate summary."


def identify_gaps(all_notes: list) -> str:
    """
    Identify potential gaps in note coverage.

    Analyzes notes to find concepts that may have been mentioned but not fully noted.
    """
    combined = "\n\n".join([note['rough'] + " | " + note['enhanced'] for note in all_notes])

    prompt = f"""Analyze these lecture notes and identify potential gaps in coverage.

Notes:
{combined}

Look for:
1. Concepts mentioned briefly but not explained
2. Questions the professor might have answered that weren't fully noted
3. Transitions that suggest missing content ("as I mentioned before...")
4. Examples that seem incomplete

Return markdown list of potential gaps with:
- What might be missing
- Why you think it's a gap
- Suggested action (review recording, ask classmate, office hours)"""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


def create_timeline_artifact(notes: list, lecture_title: str) -> str:
    """
    Create an interactive timeline visualization of the lecture.

    Shows topics covered over time with your notes.
    """
    # Prepare timeline data
    timeline_data = []
    for note in notes:
        timeline_data.append({
            'time': note['timestamp'],
            'rough': note['rough'][:100],
            'topic': note['enhanced'][:200]
        })

    prompt = f"""Create an interactive HTML timeline visualization for this lecture.

Lecture: {lecture_title}
Timeline data:
{json.dumps(timeline_data, indent=2)}

Create an HTML artifact with:
1. Horizontal timeline showing lecture progression
2. Each note as a point on the timeline
3. Hover to see note content
4. Color-code by topic/concept (if you can detect themes)
5. Interactive: click to expand full note
6. Clean, modern design
7. Timestamps labeled
8. Visual indication of note density (busy periods)

Return ONLY complete HTML with embedded CSS and JavaScript."""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


# ============================================================================
# TODO SECTION FOR STUDENTS
# ============================================================================

def detect_confusion(notes: list, current_index: int) -> dict:
    """
    TODO #1: Confusion Detection (2-3 hours)

    Detect when student seems confused based on note patterns.

    Your task:
    1. Analyze indicators of confusion:
       - Incomplete sentences
       - Question marks ("what?", "huh?", "wait")
       - Repetition of same phrase
       - Sudden drop in note detail
       - Time gaps (no notes for 5+ minutes)
       - Notes not matching expected topic flow

    2. Calculate confusion score (0-100):
       0 = crystal clear understanding
       100 = completely lost

    3. When confusion > 60, trigger:
       - Proactive explanation of current concept
       - Alternative analogy
       - Suggestion to flag for review
       - Link to related resources

    4. Track confusion over time (for timeline visualization)

    5. Return dict:
    {
        'is_confused': bool,
        'confusion_score': int,
        'indicators': [list of detected indicators],
        'suggested_action': str,
        'explanation': str (if confusion detected)
    }

    Hints:
    - Look for uncertainty language ("I think", "maybe", "not sure")
    - Compare note length/quality to earlier notes
    - Track time between notes
    - Use Claude to analyze note quality
    """
    # YOUR CODE HERE
    return {
        'is_confused': False,
        'confusion_score': 0,
        'indicators': [],
        'suggested_action': 'Keep taking notes!',
        'explanation': ''
    }


def link_to_previous_lectures(current_content: str, course_name: str):
    """
    TODO #2: Multi-Lecture Context (3-4 hours)

    Link current lecture content to previous lectures in the course.

    Your task:
    1. Maintain persistent storage of all lectures:
       st.session_state.course_lectures = {
           'COS 126': {
               'Lecture 1': {...},
               'Lecture 2': {...},
           }
       }

    2. When processing current notes:
       - Identify concepts from previous lectures
       - Create links: "This builds on [concept] from Lecture X"
       - Detect prerequisite knowledge

    3. Generate review recommendations:
       - What to review before studying this lecture
       - Which previous concepts are being built upon

    4. Create course-wide concept map (artifact):
       - All lectures as nodes
       - Edges = concept dependencies
       - Highlight current lecture

    5. Implement search:
       - "Find all lectures discussing recursion"
       - Return matches with context

    Example return:
    {
        'connections': [
            {
                'previous_lecture': 'Lecture 5',
                'concept': 'recursion',
                'relationship': 'builds on'
            }
        ],
        'review_recommendations': [
            'Review recursion basics from Lecture 5',
            'Review Big O notation from Lecture 7'
        ],
        'concept_map_html': '<html>...</html>'
    }

    Hints:
    - Use pickle or JSON to persist data
    - Create concept index across lectures
    - Use Claude to identify connections
    - Maintain course syllabus structure
    """
    # YOUR CODE HERE
    st.warning("🚧 TODO #2: Multi-lecture context tracking not yet implemented!")
    return None


def track_attention(notes: list) -> dict:
    """
    TODO #3: Attention Tracker (1-2 hours)

    Monitor student engagement and recommend breaks.

    Your task:
    1. Track engagement signals:
       - Notes per minute (frequency)
       - Note quality (length, detail)
       - Time since last note
       - Question generation requests

    2. Calculate attention score (0-100):
       - High: Detailed notes, frequent, questions
       - Medium: Consistent but brief
       - Low: Long gaps, very brief notes

    3. Recommend breaks when:
       - Score drops below 40
       - After 25-30 minutes (Pomodoro)
       - Natural topic transitions

    4. Create attention graph:
       - Line chart over lecture time
       - Color-coded segments
       - Break suggestions marked

    5. Gamification:
       - "Focus streak: 28 minutes! 🎯"
       - "3 lectures in a row with great attention!"

    Return:
    {
        'current_score': int,
        'trend': 'increasing' | 'stable' | 'decreasing',
        'should_break': bool,
        'message': str,
        'graph_data': [...] for visualization
    }

    Hints:
    - Calculate rolling 5-minute average
    - Compare to lecture start performance
    - Research optimal break timing (Pomodoro)
    - Use st.line_chart() for visualization
    """
    # YOUR CODE HERE
    return {
        'current_score': 75,
        'trend': 'stable',
        'should_break': False,
        'message': 'Keep up the good work!',
        'graph_data': []
    }


def merge_notes_with_classmates(your_notes: dict, classmate_files: list):
    """
    TODO #4: Collaborative Notes (2-3 hours)

    Merge notes from multiple students for comprehensive coverage.

    Your task:
    1. Export format (JSON):
       {
         "course": "COS 126",
         "lecture": "Recursion",
         "date": "2024-01-15",
         "notes": [...],
         "key_concepts": [...]
       }

    2. Import classmates' notes:
       - Parse JSON files
       - Validate format
       - Preserve attribution

    3. Merge strategy:
       - Combine all unique concepts
       - Keep best explanation for each
       - Flag contradictions
       - Synthesize with Claude

    4. Generate merged report:
       - Topics covered by all (core material)
       - Topics covered by few (might have missed)
       - Common confusion points
       - Questions from all students

    5. Privacy:
       - Anonymous contributions option
       - Don't share personal comments

    Example output:
    {
        'merged_notes': {...},
        'coverage_analysis': {
            'core_topics': [...],
            'missed_by_you': [...],
            'common_confusion': [...]
        },
        'merged_html': '<html>...</html>'
    }

    Hints:
    - Use Claude to synthesize content
    - Weight by note quality
    - Create comparison view
    - Handle different note-taking styles
    """
    # YOUR CODE HERE
    st.warning("🚧 TODO #4: Collaborative notes merging not yet implemented!")
    return None


# ============================================================================
# STREAMLIT UI
# ============================================================================

def main():
    # Header
    st.title("🎓 Interactive Lecture Companion")
    st.markdown("*Your AI assistant for active learning during lectures*")

    # Sidebar - Session Management
    with st.sidebar:
        st.header("📝 Lecture Session")

        # Create or load session
        if st.session_state.lecture_session is None:
            course_name = st.text_input("Course:", placeholder="e.g., COS 126")
            lecture_title = st.text_input("Lecture Title:", placeholder="e.g., Recursion")

            if st.button("🎬 Start Lecture Session"):
                if course_name and lecture_title:
                    st.session_state.lecture_session = {
                        'course': course_name,
                        'title': lecture_title,
                        'start_time': datetime.now(),
                        'status': 'active'
                    }
                    st.success("✅ Session started!")
                    st.rerun()
                else:
                    st.warning("Please fill in both fields!")
        else:
            # Show active session
            session = st.session_state.lecture_session
            st.success(f"🔴 **LIVE**: {session['title']}")
            st.caption(f"Course: {session['course']}")

            elapsed = datetime.now() - session['start_time']
            minutes = int(elapsed.total_seconds() / 60)
            st.metric("Duration", f"{minutes} min")
            st.metric("Notes Taken", len(st.session_state.notes))

            if st.button("🛑 End Session"):
                session['status'] = 'completed'
                st.info("Session ended. Review your notes below!")
                st.rerun()

        st.markdown("---")

        # Tips
        st.subheader("💡 Tips")
        st.markdown("""
        - **Type rough notes** - don't worry about grammar
        - **Click enhance** after each concept
        - **Generate questions** during pauses
        - **Flag confusion** when lost
        """)

    # Main content
    if st.session_state.lecture_session is None:
        # Welcome screen
        st.markdown("""
        ## 👋 Welcome to Lecture Companion!

        ### What is this?

        An AI-powered tool that helps you stay engaged during lectures by:
        - ✨ Enhancing your rough notes in real-time
        - 🤔 Generating check-for-understanding questions
        - 🔗 Linking concepts to previous lectures
        - 📊 Creating visual timelines of lecture flow
        - 📝 Generating comprehensive summaries

        ### How to use:

        1. **Start a session** using the sidebar →
        2. **Take rough notes** as the professor talks
        3. **Enhance notes** to clean them up
        4. **Generate questions** to check understanding
        5. **Review summary** after lecture

        ### Get Started!

        Click "Start Lecture Session" in the sidebar!
        """)

    elif st.session_state.lecture_session['status'] == 'active':
        # Active lecture mode
        st.header("📝 Live Note-Taking")

        # Note input area
        col1, col2 = st.columns([3, 1])

        with col1:
            note_input = st.text_area(
                "Type your rough notes here:",
                placeholder="Prof talking about base case in recursion, when the function stops calling itself...",
                height=150,
                key=f"note_input_{len(st.session_state.notes)}"
            )

        with col2:
            st.markdown("### Quick Actions")

            if st.button("✨ Enhance Notes", type="primary"):
                if note_input:
                    with st.spinner("Enhancing your notes..."):
                        # Get context from previous notes
                        context = ""
                        if st.session_state.enhanced_notes:
                            context = "\n".join(st.session_state.enhanced_notes[-3:])

                        enhanced = enhance_notes_realtime(note_input, context)

                        # Store note
                        st.session_state.notes.append({
                            'rough': note_input,
                            'enhanced': enhanced,
                            'timestamp': datetime.now().strftime("%H:%M:%S")
                        })
                        st.session_state.enhanced_notes.append(enhanced)

                        st.success("✅ Notes enhanced!")
                        st.rerun()
                else:
                    st.warning("Write some notes first!")

            if st.button("🤔 Generate Question"):
                if st.session_state.enhanced_notes:
                    with st.spinner("Generating question..."):
                        content = "\n".join(st.session_state.enhanced_notes[-3:])
                        question = generate_question_from_content(content)
                        st.session_state.questions_generated.append(question)
                        st.success("✅ Question generated! See below.")
                        st.rerun()
                else:
                    st.warning("Take some notes first!")

            if st.button("🚩 Flag Confusion"):
                st.info("🚧 TODO #1: Implement confusion detection!")

        # Display enhanced notes
        if st.session_state.notes:
            st.markdown("---")
            st.subheader("📚 Your Enhanced Notes")

            for i, note in enumerate(reversed(st.session_state.notes), 1):
                with st.expander(f"📝 Note {len(st.session_state.notes) - i + 1} ({note['timestamp']})", expanded=(i==1)):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown("**Original:**")
                        st.caption(note['rough'])
                    with col_b:
                        st.markdown("**Enhanced:**")
                        st.markdown(note['enhanced'])

        # Display questions
        if st.session_state.questions_generated:
            st.markdown("---")
            st.subheader("🤔 Check Your Understanding")

            for i, q in enumerate(st.session_state.questions_generated, 1):
                with st.expander(f"❓ Question {i}", expanded=(i == len(st.session_state.questions_generated))):
                    st.markdown(f"**{q['question']}**")

                    with st.expander("💡 Hint 1"):
                        st.write(q['hints'][0])

                    with st.expander("💡 Hint 2"):
                        st.write(q['hints'][1])

                    with st.expander("✅ Answer & Explanation"):
                        st.write(f"**Answer:** {q['answer']}")
                        st.write(q['explanation'])

    else:
        # Post-lecture review mode
        st.header("📊 Lecture Review")

        tab1, tab2, tab3, tab4 = st.tabs([
            "📝 Summary",
            "🕐 Timeline",
            "🔍 Gap Analysis",
            "📤 Export"
        ])

        # TAB 1: Summary
        with tab1:
            st.subheader("Comprehensive Lecture Summary")

            if not st.session_state.lecture_summary:
                if st.button("📝 Generate Summary"):
                    with st.spinner("Analyzing all notes with extended thinking..."):
                        summary = generate_summary(
                            st.session_state.notes,
                            st.session_state.lecture_session['title']
                        )
                        st.session_state.lecture_summary = summary

            if st.session_state.lecture_summary:
                st.markdown(st.session_state.lecture_summary)

        # TAB 2: Timeline
        with tab2:
            st.subheader("Lecture Timeline Visualization")

            if st.button("🕐 Generate Timeline"):
                with st.spinner("Creating interactive timeline..."):
                    timeline_html = create_timeline_artifact(
                        st.session_state.notes,
                        st.session_state.lecture_session['title']
                    )
                    st.components.v1.html(timeline_html, height=500, scrolling=True)

        # TAB 3: Gap Analysis
        with tab3:
            st.subheader("Identify Potential Gaps")
            st.markdown("*What might you have missed?*")

            if st.button("🔍 Analyze Gaps"):
                with st.spinner("Analyzing for gaps..."):
                    gaps = identify_gaps(st.session_state.notes)
                    st.markdown(gaps)

        # TAB 4: Export
        with tab4:
            st.subheader("Export Your Notes")

            # Basic export (working)
            if st.button("📥 Export as JSON"):
                export_data = {
                    'course': st.session_state.lecture_session['course'],
                    'lecture': st.session_state.lecture_session['title'],
                    'date': st.session_state.lecture_session['start_time'].strftime("%Y-%m-%d"),
                    'notes': st.session_state.notes,
                    'summary': st.session_state.lecture_summary,
                    'questions': st.session_state.questions_generated
                }

                st.download_button(
                    label="💾 Download JSON",
                    data=json.dumps(export_data, indent=2, default=str),
                    file_name=f"{st.session_state.lecture_session['course']}_lecture_notes.json",
                    mime="application/json"
                )

            st.markdown("---")
            st.info("💡 Want more export formats? Complete TODO #4 to add Markdown, PDF, and more!")

        # TODOs section
        st.markdown("---")
        st.header("🚧 Advanced Features (TODOs)")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🚨 Confusion Detection")
            st.info("TODO #1: Auto-detect when you're confused")
            if st.button("Test Confusion Detector"):
                st.warning("Complete TODO #1 to unlock this feature!")

            st.subheader("🧠 Attention Tracker")
            st.info("TODO #3: Monitor focus and suggest breaks")
            if st.button("View Attention Graph"):
                st.warning("Complete TODO #3 to unlock this feature!")

        with col2:
            st.subheader("🔗 Multi-Lecture Context")
            st.info("TODO #2: Link to previous lectures")
            if st.button("Show Connections"):
                st.warning("Complete TODO #2 to unlock this feature!")

            st.subheader("👥 Collaborative Notes")
            st.info("TODO #4: Merge notes with classmates")
            if st.button("Import Classmate Notes"):
                st.warning("Complete TODO #4 to unlock this feature!")


if __name__ == "__main__":
    main()
