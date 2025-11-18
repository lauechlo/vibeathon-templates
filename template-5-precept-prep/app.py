"""
Precept Prep Assistant - Beginner Version
Basic text analysis and question generation for precept prep.
"""

import streamlit as st
import json
import os
from datetime import datetime
import re

st.set_page_config(page_title="Precept Prep", page_icon="📖", layout="wide")

DATA_DIR = "data"
READINGS_FILE = os.path.join(DATA_DIR, "readings.json")


def init_data():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def save_reading(title, text, course, notes):
    """Save a reading for future reference."""
    init_data()

    reading = {
        'title': title,
        'text': text,
        'course': course,
        'notes': notes,
        'timestamp': datetime.now().isoformat()
    }

    readings = []
    if os.path.exists(READINGS_FILE):
        with open(READINGS_FILE, 'r') as f:
            readings = json.load(f)

    readings.append(reading)

    with open(READINGS_FILE, 'w') as f:
        json.dump(readings, f, indent=2)


def load_readings():
    """Load saved readings."""
    init_data()
    if os.path.exists(READINGS_FILE):
        with open(READINGS_FILE, 'r') as f:
            return json.load(f)
    return []


def extract_key_terms(text, min_length=5):
    """Simple keyword extraction based on word frequency."""
    # Remove common words
    common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
                    'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                    'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this',
                    'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'}

    # Tokenize and filter
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    words = [w for w in words if len(w) >= min_length and w not in common_words]

    # Count frequencies
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1

    # Get top words
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, freq in sorted_words[:10]]


def generate_basic_questions(text):
    """Generate simple discussion questions based on text."""
    questions = []

    # Look for key phrases that suggest arguments
    if "argues" in text.lower() or "argument" in text.lower():
        questions.append("What is the main argument presented in this reading?")

    if "because" in text.lower() or "therefore" in text.lower():
        questions.append("What reasoning does the author use to support their claims?")

    if "however" in text.lower() or "although" in text.lower():
        questions.append("What counterarguments or objections does the author address?")

    # Generic questions
    questions.extend([
        "What are the key concepts or ideas in this reading?",
        "How does this reading relate to previous course material?",
        "What questions or critiques do you have about this text?",
        "Can you think of real-world examples that illustrate these ideas?"
    ])

    return questions


def create_simple_summary(text, num_sentences=3):
    """Create a very basic summary by taking first few sentences."""
    sentences = text.split('.')
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    return '. '.join(sentences[:num_sentences]) + '.'


def main():
    st.title("📖 Precept Prep Assistant")
    st.markdown("Prepare for precept with reading analysis and discussion questions!")

    tab1, tab2, tab3 = st.tabs(["📝 Analyze Reading", "💾 Saved Readings", "💡 Tips"])

    with tab1:
        st.subheader("Paste Your Reading")

        course = st.text_input("Course (optional)", placeholder="e.g., PHI 201, ENG 215")
        title = st.text_input("Reading Title", placeholder="e.g., Kant's Critique of Pure Reason")

        reading_text = st.text_area(
            "Paste the reading text here:",
            height=200,
            placeholder="Paste the text you need to read for precept..."
        )

        if st.button("🔍 Analyze Reading", type="primary", disabled=not reading_text):
            if reading_text:
                st.divider()

                # Basic Summary
                st.subheader("📋 Quick Summary")
                summary = create_simple_summary(reading_text)
                st.info(summary)

                # Key Terms
                st.subheader("🔑 Key Terms")
                key_terms = extract_key_terms(reading_text)
                if key_terms:
                    cols = st.columns(5)
                    for i, term in enumerate(key_terms):
                        with cols[i % 5]:
                            st.button(f"**{term}**", disabled=True)
                else:
                    st.write("No key terms identified")

                # Discussion Questions
                st.subheader("💬 Discussion Questions")
                questions = generate_basic_questions(reading_text)

                for i, question in enumerate(questions, 1):
                    st.write(f"{i}. {question}")

                # Word count and reading time
                st.divider()
                col1, col2, col3 = st.columns(3)

                word_count = len(reading_text.split())
                reading_time = word_count / 200  # ~200 words per minute

                with col1:
                    st.metric("Word Count", f"{word_count:,}")
                with col2:
                    st.metric("Reading Time", f"~{reading_time:.0f} min")
                with col3:
                    st.metric("Key Terms", len(key_terms))

                # Save option
                st.divider()
                notes = st.text_area("Add your notes (optional):", height=100)

                if st.button("💾 Save This Reading"):
                    save_reading(title or "Untitled", reading_text, course or "General", notes)
                    st.success("Reading saved!")

    with tab2:
        st.subheader("Your Saved Readings")

        readings = load_readings()

        if readings:
            # Filter by course
            courses = list(set(r['course'] for r in readings))
            filter_course = st.selectbox("Filter by course:", ["All"] + courses)

            filtered = readings if filter_course == "All" else [r for r in readings if r['course'] == filter_course]

            for reading in reversed(filtered):  # Most recent first
                with st.expander(f"{reading['title']} ({reading['course']})"):
                    st.caption(f"Saved: {datetime.fromisoformat(reading['timestamp']).strftime('%Y-%m-%d %H:%M')}")

                    st.write("**Text Preview:**")
                    st.write(reading['text'][:300] + "..." if len(reading['text']) > 300 else reading['text'])

                    if reading['notes']:
                        st.write("**Your Notes:**")
                        st.info(reading['notes'])

                    word_count = len(reading['text'].split())
                    st.caption(f"Word count: {word_count}")
        else:
            st.info("No saved readings yet. Analyze a reading and save it!")

    with tab3:
        st.subheader("💡 Tips for Precept Prep")

        st.markdown("""
        ### Before Precept
        - ✅ Read the text carefully, taking notes as you go
        - ✅ Identify the main argument or thesis
        - ✅ Note any confusing passages to ask about
        - ✅ Think of 1-2 questions to bring to discussion

        ### During Analysis
        - Look for key terms and concepts
        - Identify the author's main claims
        - Consider counterarguments
        - Connect to previous readings or course themes

        ### Using This Tool
        - Paste challenging sections for quick analysis
        - Use generated questions as discussion starters
        - Save important readings for exam prep
        - Add your own notes and observations

        ### 🚀 Want More?
        Check out `app_advanced.py` for AI-powered features:
        - Deeper text analysis
        - PDF upload support
        - Argument extraction
        - Comparative analysis across readings
        """)


if __name__ == "__main__":
    main()
