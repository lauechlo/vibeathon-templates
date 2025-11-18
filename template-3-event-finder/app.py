"""
Princeton Event Finder - Beginner Version
Discover campus events with easy filtering and search.
"""

import streamlit as st
import json
import os
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List

st.set_page_config(page_title="Event Finder", page_icon="🎉", layout="wide")

DATA_DIR = "data"
EVENTS_FILE = os.path.join(DATA_DIR, "events.json")
SAVED_FILE = os.path.join(DATA_DIR, "saved_events.json")

EVENT_TYPES = ["Academic", "Social", "Food", "Sports", "Arts", "Career", "Other"]
LOCATIONS = ["Frist", "Whitman", "Butler", "McCosh", "Friend Center", "Lewis Library", "Other"]


@dataclass
class Event:
    id: str
    title: str
    description: str
    event_type: str
    location: str
    date: str  # ISO format
    time: str
    tags: List[str]

    def get_datetime(self):
        return datetime.fromisoformat(self.date)


def initialize_data():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Create sample events if file doesn't exist
    if not os.path.exists(EVENTS_FILE):
        sample_events = [
            Event(
                id="1",
                title="Free Pizza Study Break",
                description="Free pizza and snacks while studying for midterms!",
                event_type="Food",
                location="Frist",
                date=(datetime.now() + timedelta(days=1)).date().isoformat(),
                time="21:00",
                tags=["free food", "study break"]
            ),
            Event(
                id="2",
                title="CS Career Panel",
                description="Tech industry professionals discuss career paths",
                event_type="Career",
                location="Friend Center",
                date=(datetime.now() + timedelta(days=3)).date().isoformat(),
                time="18:30",
                tags=["cs", "career", "tech"]
            ),
            Event(
                id="3",
                title="Acappella Concert",
                description="Tigertones spring showcase",
                event_type="Arts",
                location="Richardson Auditorium",
                date=(datetime.now() + timedelta(days=5)).date().isoformat(),
                time="20:00",
                tags=["music", "performance"]
            ),
        ]
        save_events([asdict(e) for e in sample_events])


def load_events() -> List[Event]:
    initialize_data()
    try:
        with open(EVENTS_FILE, 'r') as f:
            data = json.load(f)
            return [Event(**e) for e in data]
    except:
        return []


def save_events(events_data):
    with open(EVENTS_FILE, 'w') as f:
        json.dump(events_data, f, indent=2)


def load_saved_events() -> List[str]:
    initialize_data()
    if os.path.exists(SAVED_FILE):
        with open(SAVED_FILE, 'r') as f:
            return json.load(f)
    return []


def save_saved_events(event_ids):
    with open(SAVED_FILE, 'w') as f:
        json.dump(event_ids, f)


def main():
    st.title("🎉 Princeton Event Finder")
    st.markdown("Discover what's happening on campus!")

    events = load_events()
    saved_event_ids = load_saved_events()

    # Sidebar filters
    with st.sidebar:
        st.header("🔍 Filters")

        search_query = st.text_input("Search events", placeholder="e.g., free food, CS talk")

        filter_type = st.multiselect("Event Type", options=EVENT_TYPES)
        filter_location = st.multiselect("Location", options=LOCATIONS)

        date_range = st.radio("When?", ["All", "Today", "This Week", "This Month"])

        st.divider()
        st.metric("Total Events", len(events))
        st.metric("Saved Events", len(saved_event_ids))

    # Filter events
    filtered_events = events.copy()

    # Apply search
    if search_query:
        filtered_events = [
            e for e in filtered_events
            if search_query.lower() in e.title.lower()
            or search_query.lower() in e.description.lower()
            or any(search_query.lower() in tag for tag in e.tags)
        ]

    # Apply type filter
    if filter_type:
        filtered_events = [e for e in filtered_events if e.event_type in filter_type]

    # Apply location filter
    if filter_location:
        filtered_events = [e for e in filtered_events if e.location in filter_location]

    # Apply date filter
    now = datetime.now()
    if date_range == "Today":
        filtered_events = [e for e in filtered_events if e.get_datetime().date() == now.date()]
    elif date_range == "This Week":
        week_end = now + timedelta(days=7)
        filtered_events = [e for e in filtered_events if now <= e.get_datetime() <= week_end]
    elif date_range == "This Month":
        filtered_events = [e for e in filtered_events if e.get_datetime().month == now.month]

    # Sort by date
    filtered_events.sort(key=lambda x: x.date)

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📅 All Events", "⭐ Saved Events", "➕ Add Event"])

    with tab1:
        st.subheader(f"Showing {len(filtered_events)} events")

        if filtered_events:
            for event in filtered_events:
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 1])

                    with col1:
                        st.markdown(f"### {event.title}")
                        st.write(event.description)
                        st.caption(" · ".join([f"#{tag}" for tag in event.tags]))

                    with col2:
                        event_datetime = event.get_datetime()
                        st.write(f"📅 {event_datetime.strftime('%b %d, %Y')}")
                        st.write(f"🕐 {event.time}")
                        st.write(f"📍 {event.location}")
                        st.write(f"🏷️ {event.event_type}")

                    with col3:
                        if event.id in saved_event_ids:
                            if st.button("❤️ Saved", key=f"unsave_{event.id}"):
                                saved_event_ids.remove(event.id)
                                save_saved_events(saved_event_ids)
                                st.rerun()
                        else:
                            if st.button("🤍 Save", key=f"save_{event.id}"):
                                saved_event_ids.append(event.id)
                                save_saved_events(saved_event_ids)
                                st.rerun()

                    st.divider()
        else:
            st.info("No events match your filters. Try adjusting your search!")

    with tab2:
        saved_events = [e for e in events if e.id in saved_event_ids]

        if saved_events:
            st.write(f"You have {len(saved_events)} saved event(s)")

            for event in saved_events:
                with st.container():
                    col1, col2 = st.columns([4, 1])

                    with col1:
                        st.markdown(f"### {event.title}")
                        st.write(f"📅 {event.date} at {event.time} · 📍 {event.location}")

                    with col2:
                        if st.button("Remove", key=f"remove_{event.id}"):
                            saved_event_ids.remove(event.id)
                            save_saved_events(saved_event_ids)
                            st.rerun()

                    st.divider()
        else:
            st.info("No saved events yet. Browse events and click 🤍 to save!")

    with tab3:
        st.subheader("➕ Add New Event")

        with st.form("add_event"):
            title = st.text_input("Event Title *")
            description = st.text_area("Description")

            col1, col2 = st.columns(2)
            with col1:
                event_type = st.selectbox("Type", EVENT_TYPES)
                location = st.selectbox("Location", LOCATIONS)

            with col2:
                date = st.date_input("Date")
                time = st.time_input("Time")

            tags_input = st.text_input("Tags (comma-separated)", placeholder="free food, cs, career")

            if st.form_submit_button("Add Event", type="primary"):
                if title:
                    new_event = Event(
                        id=str(len(events) + 1),
                        title=title,
                        description=description,
                        event_type=event_type,
                        location=location,
                        date=date.isoformat(),
                        time=time.strftime("%H:%M"),
                        tags=[t.strip() for t in tags_input.split(",") if t.strip()]
                    )

                    all_events = [asdict(e) for e in events] + [asdict(new_event)]
                    save_events(all_events)

                    st.success(f"✅ Added: {title}")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Please enter an event title!")


if __name__ == "__main__":
    main()
