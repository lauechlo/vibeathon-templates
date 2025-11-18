"""
Flashcard Generator - Beginner Version
Create and study flashcards with spaced repetition!

This version focuses on manual flashcard creation and effective study techniques.
"""

import streamlit as st
import json
import os
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List
import random

st.set_page_config(page_title="Flashcard App", page_icon="🎴", layout="wide")

DATA_DIR = "data"
DECKS_FILE = os.path.join(DATA_DIR, "flashcard_decks.json")


@dataclass
class Flashcard:
    """A single flashcard."""
    id: str
    question: str
    answer: str
    deck_name: str
    created_at: str
    last_reviewed: str = None
    next_review: str = None
    ease_factor: float = 2.5  # For SM-2 algorithm
    interval: int = 0  # Days until next review
    repetitions: int = 0
    correct_count: int = 0
    incorrect_count: int = 0


def initialize_data():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_flashcards() -> List[Flashcard]:
    """Load all flashcards from file."""
    initialize_data()

    if os.path.exists(DECKS_FILE):
        try:
            with open(DECKS_FILE, 'r') as f:
                data = json.load(f)
                return [Flashcard(**card) for card in data]
        except:
            return []
    return []


def save_flashcards(cards: List[Flashcard]):
    """Save flashcards to file."""
    initialize_data()
    with open(DECKS_FILE, 'w') as f:
        json.dump([asdict(card) for card in cards], f, indent=2)


def create_card_id() -> str:
    """Generate unique ID for flashcard."""
    import uuid
    return str(uuid.uuid4())[:8]


def calculate_next_review(card: Flashcard, quality: int) -> Flashcard:
    """
    Calculate next review date using SM-2 algorithm.

    quality: 0-5
    0-1: Forgot (reset)
    2-3: Hard (small increase)
    4-5: Easy (large increase)
    """
    if quality < 2:  # Forgot
        card.interval = 1
        card.repetitions = 0
        card.ease_factor = max(1.3, card.ease_factor - 0.2)
        card.incorrect_count += 1
    else:  # Remembered
        card.correct_count += 1

        if card.repetitions == 0:
            card.interval = 1
        elif card.repetitions == 1:
            card.interval = 6
        else:
            card.interval = int(card.interval * card.ease_factor)

        card.repetitions += 1

        # Adjust ease factor
        card.ease_factor = max(1.3, card.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))

    # Set next review date
    card.last_reviewed = datetime.now().isoformat()
    card.next_review = (datetime.now() + timedelta(days=card.interval)).isoformat()

    return card


def get_cards_due_for_review(cards: List[Flashcard]) -> List[Flashcard]:
    """Get cards that are due for review today."""
    now = datetime.now()
    due_cards = []

    for card in cards:
        if card.next_review is None:  # New card
            due_cards.append(card)
        else:
            next_review_date = datetime.fromisoformat(card.next_review)
            if next_review_date <= now:
                due_cards.append(card)

    return due_cards


def get_deck_names(cards: List[Flashcard]) -> List[str]:
    """Get unique deck names."""
    return sorted(set(card.deck_name for card in cards))


def get_deck_stats(cards: List[Flashcard], deck_name: str) -> dict:
    """Get statistics for a deck."""
    deck_cards = [c for c in cards if c.deck_name == deck_name]

    if not deck_cards:
        return None

    new_cards = [c for c in deck_cards if c.next_review is None]
    due_cards = get_cards_due_for_review(deck_cards)
    mastered_cards = [c for c in deck_cards if c.repetitions >= 3]

    return {
        'total': len(deck_cards),
        'new': len(new_cards),
        'due': len(due_cards),
        'mastered': len(mastered_cards),
        'accuracy': (sum(c.correct_count for c in deck_cards) /
                    max(1, sum(c.correct_count + c.incorrect_count for c in deck_cards))) * 100
    }


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    st.title("🎴 Flashcard Study App")
    st.markdown("Master any subject with spaced repetition!")

    # Initialize session state
    if 'cards' not in st.session_state:
        st.session_state.cards = load_flashcards()

    if 'study_mode' not in st.session_state:
        st.session_state.study_mode = False

    if 'current_card_idx' not in st.session_state:
        st.session_state.current_card_idx = 0

    if 'show_answer' not in st.session_state:
        st.session_state.show_answer = False

    cards = st.session_state.cards

    # Sidebar
    with st.sidebar:
        st.header("📚 Your Decks")

        decks = get_deck_names(cards)

        if decks:
            for deck in decks:
                stats = get_deck_stats(cards, deck)
                if stats:
                    with st.expander(f"**{deck}**"):
                        st.metric("Total Cards", stats['total'])
                        st.metric("Due Today", stats['due'])
                        st.metric("Mastered", stats['mastered'])
                        if stats['accuracy'] > 0:
                            st.metric("Accuracy", f"{stats['accuracy']:.0f}%")
        else:
            st.info("No decks yet. Create your first flashcard!")

        st.divider()

        # Overall stats
        if cards:
            total_due = len(get_cards_due_for_review(cards))
            st.metric("📅 Due Today (All Decks)", total_due)

    # Main content
    if not st.session_state.study_mode:
        # Browse/Create mode
        tab1, tab2, tab3 = st.tabs(["➕ Create Cards", "📚 Browse Decks", "📊 Statistics"])

        # TAB 1: Create Cards
        with tab1:
            st.header("Create New Flashcard")

            with st.form("create_card"):
                deck_name = st.text_input(
                    "Deck Name *",
                    placeholder="e.g., Biology Ch. 3, Spanish Vocab",
                    help="Group related cards in a deck"
                )

                question = st.text_area(
                    "Question *",
                    placeholder="What is photosynthesis?",
                    height=100,
                    help="The front of the card - what you'll see during study"
                )

                answer = st.text_area(
                    "Answer *",
                    placeholder="The process by which plants convert light energy into chemical energy...",
                    height=150,
                    help="The back of the card - the correct answer"
                )

                col1, col2 = st.columns([3, 1])

                with col1:
                    st.caption("💡 **Tip**: Make questions specific and test one concept at a time")

                with col2:
                    submitted = st.form_submit_button("Add Card", type="primary", use_container_width=True)

                if submitted:
                    if deck_name and question and answer:
                        new_card = Flashcard(
                            id=create_card_id(),
                            question=question,
                            answer=answer,
                            deck_name=deck_name.strip(),
                            created_at=datetime.now().isoformat()
                        )

                        cards.append(new_card)
                        save_flashcards(cards)

                        st.success(f"✅ Card added to '{deck_name}'!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Please fill in all fields!")

            # Quick add multiple cards
            st.divider()
            st.subheader("🚀 Quick Add Multiple Cards")

            with st.expander("Add several cards at once"):
                bulk_deck = st.text_input("Deck name for all cards", key="bulk_deck")

                bulk_text = st.text_area(
                    "Enter Q&A pairs (one per line, use '|' to separate question and answer):",
                    placeholder="What is 2+2? | 4\nCapital of France? | Paris\nMitochondria function? | Powerhouse of the cell",
                    height=200
                )

                if st.button("Add All Cards"):
                    if bulk_deck and bulk_text:
                        lines = bulk_text.strip().split('\n')
                        added = 0

                        for line in lines:
                            if '|' in line:
                                q, a = line.split('|', 1)
                                new_card = Flashcard(
                                    id=create_card_id(),
                                    question=q.strip(),
                                    answer=a.strip(),
                                    deck_name=bulk_deck.strip(),
                                    created_at=datetime.now().isoformat()
                                )
                                cards.append(new_card)
                                added += 1

                        if added > 0:
                            save_flashcards(cards)
                            st.success(f"✅ Added {added} cards to '{bulk_deck}'!")
                            st.rerun()
                        else:
                            st.warning("No valid Q|A pairs found. Make sure to use '|' separator!")
                    else:
                        st.error("Please enter deck name and Q&A pairs!")

        # TAB 2: Browse Decks
        with tab2:
            st.header("Browse Your Flashcards")

            if cards:
                # Filter by deck
                selected_deck = st.selectbox("Select Deck", ["All"] + get_deck_names(cards))

                filtered_cards = cards if selected_deck == "All" else [c for c in cards if c.deck_name == selected_deck]

                st.write(f"Showing {len(filtered_cards)} card(s)")

                for i, card in enumerate(filtered_cards):
                    with st.expander(f"❓ {card.question[:60]}..."):
                        st.write(f"**Q:** {card.question}")
                        st.write(f"**A:** {card.answer}")

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.caption(f"Deck: {card.deck_name}")
                        with col2:
                            st.caption(f"Reviews: {card.repetitions}")
                        with col3:
                            if card.next_review:
                                next_date = datetime.fromisoformat(card.next_review)
                                st.caption(f"Next: {next_date.strftime('%b %d')}")
                            else:
                                st.caption("Next: Not studied yet")

                        if st.button(f"🗑️ Delete", key=f"delete_{card.id}"):
                            cards.remove(card)
                            save_flashcards(cards)
                            st.rerun()

            else:
                st.info("No flashcards yet. Create some in the 'Create Cards' tab!")

        # TAB 3: Statistics
        with tab3:
            st.header("📊 Study Statistics")

            if cards:
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Total Cards", len(cards))
                with col2:
                    due_today = len(get_cards_due_for_review(cards))
                    st.metric("Due Today", due_today)
                with col3:
                    new_cards = [c for c in cards if c.repetitions == 0]
                    st.metric("New Cards", len(new_cards))
                with col4:
                    mastered = [c for c in cards if c.repetitions >= 3]
                    st.metric("Mastered", len(mastered))

                st.divider()

                # Deck breakdown
                st.subheader("Deck Breakdown")

                for deck in get_deck_names(cards):
                    stats = get_deck_stats(cards, deck)
                    with st.expander(f"**{deck}** ({stats['total']} cards)"):
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.metric("Due", stats['due'])
                        with col2:
                            st.metric("Mastered", stats['mastered'])
                        with col3:
                            st.metric("Accuracy", f"{stats['accuracy']:.0f}%")

            else:
                st.info("No statistics yet. Create flashcards to see your progress!")

        # Study button at the bottom
        st.divider()

        due_cards = get_cards_due_for_review(cards)

        if due_cards:
            if st.button(f"🎓 Start Studying ({len(due_cards)} cards due)", type="primary", use_container_width=True):
                st.session_state.study_mode = True
                st.session_state.study_cards = due_cards
                st.session_state.current_card_idx = 0
                st.session_state.show_answer = False
                st.rerun()
        else:
            st.success("🎉 All caught up! No cards due for review right now.")
            st.info("💡 Create more cards or come back tomorrow for your next review session!")

    else:
        # Study mode
        study_cards = st.session_state.study_cards
        idx = st.session_state.current_card_idx

        if idx < len(study_cards):
            current_card = study_cards[idx]

            # Progress
            st.progress((idx + 1) / len(study_cards))
            st.caption(f"Card {idx + 1} of {len(study_cards)} | Deck: {current_card.deck_name}")

            st.divider()

            # Question
            st.subheader("Question:")
            st.markdown(f"## {current_card.question}")

            st.divider()

            if not st.session_state.show_answer:
                # Show answer button
                if st.button("🔍 Show Answer", use_container_width=True, type="primary"):
                    st.session_state.show_answer = True
                    st.rerun()
            else:
                # Show answer
                st.subheader("Answer:")
                st.info(current_card.answer)

                st.divider()
                st.write("**How well did you know this?**")

                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button("😰 Forgot", use_container_width=True):
                        current_card = calculate_next_review(current_card, 0)
                        cards[cards.index(study_cards[idx])] = current_card
                        save_flashcards(cards)
                        st.session_state.current_card_idx += 1
                        st.session_state.show_answer = False
                        st.rerun()

                with col2:
                    if st.button("🤔 Hard", use_container_width=True):
                        current_card = calculate_next_review(current_card, 3)
                        cards[cards.index(study_cards[idx])] = current_card
                        save_flashcards(cards)
                        st.session_state.current_card_idx += 1
                        st.session_state.show_answer = False
                        st.rerun()

                with col3:
                    if st.button("✅ Easy", use_container_width=True, type="primary"):
                        current_card = calculate_next_review(current_card, 5)
                        cards[cards.index(study_cards[idx])] = current_card
                        save_flashcards(cards)
                        st.session_state.current_card_idx += 1
                        st.session_state.show_answer = False
                        st.rerun()

        else:
            # Study session complete
            st.success("🎉 Study session complete!")
            st.balloons()

            st.write(f"You reviewed {len(study_cards)} cards!")
            st.write("Come back tomorrow for your next review session.")

            if st.button("📚 Back to Decks", type="primary"):
                st.session_state.study_mode = False
                st.rerun()


if __name__ == "__main__":
    main()
