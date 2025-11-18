"""
Flashcard Generator - Advanced Version with AI
Auto-generate flashcards from your notes using Claude!
"""

import streamlit as st
import json
import os
from datetime import datetime
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Flashcard Generator", page_icon="🤖", layout="wide")

DATA_DIR = "data"


@st.cache_resource
def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("⚠️ ANTHROPIC_API_KEY not found!")
        st.stop()
    return Anthropic(api_key=api_key)


def generate_flashcards_from_notes(notes: str, num_cards: int, client) -> list:
    """Generate flashcards from study notes using AI."""
    prompt = f"""Generate {num_cards} high-quality flashcards from these study notes.

Notes:
{notes}

Create flashcards that:
- Test understanding, not just memorization
- Cover key concepts
- Are clear and concise
- Have specific, accurate answers

Format each card as:
Q: [question]
A: [answer]

Generate exactly {num_cards} flashcards."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )

        response = message.content[0].text.strip()

        # Parse Q&A pairs
        cards = []
        lines = response.split('\n')
        current_q = None

        for line in lines:
            line = line.strip()
            if line.startswith('Q:'):
                current_q = line[2:].strip()
            elif line.startswith('A:') and current_q:
                answer = line[2:].strip()
                cards.append({'question': current_q, 'answer': answer})
                current_q = None

        return cards

    except Exception as e:
        st.error(f"Error: {e}")
        return []


def generate_multiple_choice(notes: str, num_questions: int, client) -> list:
    """Generate multiple choice questions."""
    prompt = f"""Create {num_questions} multiple choice questions from these notes:

{notes}

Format each as:
Q: [question]
A) [option]
B) [option]
C) [option]
D) [option]
Correct: [letter]

Make distractors plausible but clearly wrong."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )

        return message.content[0].text.strip()

    except Exception as e:
        return f"Error: {e}"


def main():
    client = get_client()

    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("🤖 AI Flashcard Generator")
        st.markdown("Auto-generate study flashcards from your notes!")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("✨ **AI Powered**")

    tab1, tab2 = st.tabs(["✨ Generate from Notes", "🎯 Multiple Choice"])

    with tab1:
        st.header("Generate Flashcards from Notes")

        st.info("""
        **How it works:**
        1. Paste your lecture notes, textbook passages, or study materials
        2. Choose how many flashcards you want
        3. AI extracts key concepts and creates Q&A pairs
        4. Review and save the cards you like
        """)

        notes_input = st.text_area(
            "Paste your study notes here:",
            placeholder="e.g., 'Photosynthesis is the process by which plants convert light energy into chemical energy. It occurs in chloroplasts and requires sunlight, water, and CO2. The products are glucose and oxygen...'",
            height=300
        )

        col1, col2 = st.columns([3, 1])

        with col1:
            deck_name = st.text_input("Deck name", placeholder="Biology Ch. 5")

        with col2:
            num_cards = st.number_input("Number of cards", min_value=1, max_value=50, value=10)

        if st.button("✨ Generate Flashcards", type="primary", disabled=not notes_input):
            with st.spinner(f"🤖 Generating {num_cards} flashcards..."):
                cards = generate_flashcards_from_notes(notes_input, num_cards, client)

                if cards:
                    st.success(f"✅ Generated {len(cards)} flashcards!")

                    st.divider()
                    st.subheader("Review Generated Cards")

                    for i, card in enumerate(cards, 1):
                        with st.expander(f"Card {i}: {card['question'][:50]}..."):
                            st.write(f"**Q:** {card['question']}")
                            st.write(f"**A:** {card['answer']}")

                    # Export options
                    st.divider()

                    export_text = "\n\n".join([
                        f"Q: {card['question']}\nA: {card['answer']}"
                        for card in cards
                    ])

                    col1, col2 = st.columns(2)

                    with col1:
                        st.download_button(
                            label="📥 Download as Text",
                            data=export_text,
                            file_name=f"{deck_name or 'flashcards'}.txt",
                            mime="text/plain"
                        )

                    with col2:
                        # Format for Anki import
                        anki_format = "\n".join([
                            f"{card['question']}\t{card['answer']}"
                            for card in cards
                        ])

                        st.download_button(
                            label="📥 Download for Anki",
                            data=anki_format,
                            file_name=f"{deck_name or 'flashcards'}_anki.txt",
                            mime="text/plain"
                        )

                    st.info("💡 **Tip**: Review these cards and edit any that need improvement before importing to your study app!")

    with tab2:
        st.header("Generate Multiple Choice Questions")

        mc_notes = st.text_area(
            "Paste study material:",
            placeholder="Enter the content you want to be quizzed on...",
            height=300,
            key="mc_notes"
        )

        num_questions = st.number_input("Number of questions", min_value=1, max_value=20, value=5, key="mc_num")

        if st.button("🎯 Generate Quiz", type="primary", disabled=not mc_notes):
            with st.spinner("Generating questions..."):
                quiz = generate_multiple_choice(mc_notes, num_questions, client)

                st.divider()
                st.subheader("Generated Quiz")
                st.markdown(quiz)

                st.download_button(
                    label="📥 Download Quiz",
                    data=quiz,
                    file_name="quiz.txt",
                    mime="text/plain"
                )

    st.divider()
    st.markdown("""
    <div style='text-align: center; color: gray;'>
    <p>🤖 Powered by Claude AI | Study smarter with AI-generated flashcards!</p>
    <p>💡 Use with <code>app.py</code> for the full flashcard study experience with spaced repetition</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
