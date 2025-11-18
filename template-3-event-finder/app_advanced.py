"""
Princeton Event Finder - Advanced Version with AI
Natural language event search powered by Claude!
"""

import streamlit as st
import json
import os
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Event Finder", page_icon="🤖", layout="wide")

DATA_DIR = "data"
EVENTS_FILE = os.path.join(DATA_DIR, "events.json")
EVENT_TYPES = ["Academic", "Social", "Food", "Sports", "Arts", "Career", "Other"]


@st.cache_resource
def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("⚠️ ANTHROPIC_API_KEY not found!")
        st.stop()
    return Anthropic(api_key=api_key)


@dataclass
class Event:
    id: str
    title: str
    description: str
    event_type: str
    location: str
    date: str
    time: str
    tags: List[str]

    def get_datetime(self):
        return datetime.fromisoformat(self.date)


def initialize_data():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if not os.path.exists(EVENTS_FILE):
        sample = [
            {"id": "1", "title": "Free Late Night Snacks", "description": "Pizza and cookies at Whitman",
             "event_type": "Food", "location": "Whitman College", "date": (datetime.now() + timedelta(days=1)).date().isoformat(),
             "time": "22:00", "tags": ["free food", "late night"]},
            {"id": "2", "title": "AI Research Symposium", "description": "Faculty present latest ML research",
             "event_type": "Academic", "location": "Friend Center", "date": (datetime.now() + timedelta(days=2)).date().isoformat(),
             "time": "16:00", "tags": ["cs", "ai", "research"]},
            {"id": "3", "title": "Basketball Game vs Harvard", "description": "Men's basketball game",
             "event_type": "Sports", "location": "Jadwin Gym", "date": (datetime.now() + timedelta(days=4)).date().isoformat(),
             "time": "19:00", "tags": ["sports", "basketball"]},
        ]
        with open(EVENTS_FILE, 'w') as f:
            json.dump(sample, f, indent=2)


def load_events():
    initialize_data()
    try:
        with open(EVENTS_FILE, 'r') as f:
            data = json.load(f)
            return [Event(**e) for e in data]
    except:
        return []


def natural_language_search(query: str, events: List[Event], client) -> List[Event]:
    """Use Claude to understand natural language queries and filter events."""

    events_summary = "\n".join([
        f"{i+1}. {e.title} - {e.event_type} - {e.date} - Tags: {', '.join(e.tags)}"
        for i, e in enumerate(events)
    ])

    prompt = f"""You are helping filter events based on a natural language query.

Events available:
{events_summary}

User query: "{query}"
Today's date: {datetime.now().strftime('%Y-%m-%d')}

Return ONLY a JSON array of event numbers (1-indexed) that match the query.
Consider: event type, tags, dates, and semantic meaning.

Example: If query is "free food tonight" and event 1 is free food today, return: [1]
Return: [numbers]"""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}]
        )

        response = message.content[0].text.strip()
        # Parse the response to get event indices
        import re
        numbers = re.findall(r'\d+', response)
        indices = [int(n) - 1 for n in numbers if 0 < int(n) <= len(events)]

        return [events[i] for i in indices if i < len(events)]

    except Exception as e:
        st.error(f"Error in AI search: {e}")
        return events


def get_event_recommendations(events: List[Event], client) -> str:
    """Generate personalized event recommendations."""

    events_desc = "\n".join([
        f"- {e.title} ({e.event_type}) on {e.date}"
        for e in events[:10]
    ])

    prompt = f"""Based on these upcoming campus events, provide 2-3 brief recommendations
for a Princeton student. Be specific and enthusiastic!

Events:
{events_desc}

Keep it to 3-4 sentences max."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text.strip()
    except:
        return "Explore the events below to find something interesting!"


def main():
    client = get_client()

    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("🤖 AI Event Finder")
        st.markdown("Search events with natural language!")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("✨ **AI Powered**")

    events = load_events()

    # Natural language search
    st.subheader("🔍 Natural Language Search")

    with st.expander("💡 Try these examples"):
        st.write("""
        - "Show me free food events tonight"
        - "Find CS-related talks this week"
        - "What sports events are happening?"
        - "Any career or networking events?"
        """)

    nl_query = st.text_input(
        "What are you looking for?",
        placeholder="e.g., 'free food events tonight'"
    )

    if st.button("✨ Search with AI", type="primary", disabled=not nl_query):
        with st.spinner("🤖 Understanding your query..."):
            results = natural_language_search(nl_query, events, client)

            st.subheader(f"Found {len(results)} matching events")

            if results:
                for event in results:
                    with st.container():
                        col1, col2 = st.columns([3, 2])

                        with col1:
                            st.markdown(f"### {event.title}")
                            st.write(event.description)
                            st.caption(" · ".join([f"#{tag}" for tag in event.tags]))

                        with col2:
                            st.write(f"📅 {event.date}")
                            st.write(f"🕐 {event.time}")
                            st.write(f"📍 {event.location}")
                            st.write(f"🏷️ {event.event_type}")

                        st.divider()
            else:
                st.info("No events match your search. Try rephrasing!")

    # AI Recommendations
    st.divider()
    st.subheader("💡 Personalized Recommendations")

    with st.spinner("Generating recommendations..."):
        recommendations = get_event_recommendations(events, client)
        st.info(recommendations)

    # Browse all events
    st.divider()
    st.subheader("📅 All Upcoming Events")

    upcoming = [e for e in events if e.get_datetime() >= datetime.now()]
    upcoming.sort(key=lambda x: x.date)

    for event in upcoming:
        with st.expander(f"{event.title} - {event.date}"):
            st.write(f"**{event.description}**")
            st.write(f"📍 {event.location} · 🕐 {event.time} · 🏷️ {event.event_type}")
            st.write(f"Tags: {', '.join(['#' + t for t in event.tags])}")


if __name__ == "__main__":
    main()
