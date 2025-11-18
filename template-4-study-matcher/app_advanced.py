"""
Study Group Matcher - Advanced Version with AI
Intelligent matching powered by Claude!
"""

import streamlit as st
import json
import os
from dataclasses import dataclass, asdict
from typing import List
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Study Matcher", page_icon="🤖", layout="wide")

DATA_DIR = "data"
PROFILES_FILE = os.path.join(DATA_DIR, "profiles.json")

LEARNING_STYLES = ["Visual", "Auditory", "Reading/Writing", "Kinesthetic", "Mixed"]


@st.cache_resource
def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("⚠️ ANTHROPIC_API_KEY not found!")
        st.stop()
    return Anthropic(api_key=api_key)


@dataclass
class StudentProfile:
    id: str
    name: str
    courses: List[str]
    learning_style: str
    availability: List[str]
    preferred_locations: List[str]
    bio: str = ""


def init_data():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_profiles():
    init_data()
    if os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, 'r') as f:
            return [StudentProfile(**p) for p in json.load(f)]
    return []


def save_profiles(profiles):
    with open(PROFILES_FILE, 'w') as f:
        json.dump([asdict(p) for p in profiles], f, indent=2)


def ai_match_explanation(profile1: StudentProfile, profile2: StudentProfile, client) -> str:
    """Use Claude to explain why two students would be good study partners."""

    prompt = f"""Explain in 2-3 sentences why these two students would make good study partners:

Student 1: {profile1.name}
- Courses: {', '.join(profile1.courses)}
- Learning style: {profile1.learning_style}
- Bio: {profile1.bio}

Student 2: {profile2.name}
- Courses: {', '.join(profile2.courses)}
- Learning style: {profile2.learning_style}
- Bio: {profile2.bio}

Be specific and encouraging. Focus on shared courses and complementary strengths."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text.strip()
    except Exception as e:
        return f"Error: {e}"


def generate_ice_breaker(profile1: StudentProfile, profile2: StudentProfile, client) -> str:
    """Generate a conversation starter for matched students."""

    prompt = f"""Generate a friendly ice-breaker message for {profile1.name} to send to {profile2.name}.

They share these courses: {', '.join(set(profile1.courses) & set(profile2.courses))}

{profile2.name}'s bio: {profile2.bio}

Write a brief, casual message (2-3 sentences) to start a conversation about studying together.
Make it specific to their shared courses."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text.strip()
    except:
        return "Hey! I saw we're both in the same courses. Want to study together sometime?"


def main():
    client = get_client()

    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("🤖 AI Study Matcher")
        st.markdown("Find your perfect study partner with AI!")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("✨ **AI Enhanced**")

    profiles = load_profiles()

    if 'user_id' not in st.session_state:
        st.session_state.user_id = None

    with st.sidebar:
        st.header("👤 Your Profile")
        if st.session_state.user_id:
            user = next((p for p in profiles if p.id == st.session_state.user_id), None)
            if user:
                st.success(f"**{user.name}**")
                st.write(f"Courses: {', '.join(user.courses)}")
        else:
            st.info("Create your profile to start!")

    tab1, tab2 = st.tabs(["🔍 AI Matches", "👤 Profile"])

    with tab1:
        if not st.session_state.user_id:
            st.warning("Create your profile first!")
        else:
            user = next((p for p in profiles if p.id == st.session_state.user_id), None)

            if user:
                st.subheader("✨ AI-Powered Matches")

                potential_matches = [p for p in profiles if p.id != user.id]

                if potential_matches:
                    for match in potential_matches[:5]:  # Show top 5
                        # Check if they share courses
                        shared_courses = set(user.courses) & set(match.courses)

                        if shared_courses:
                            with st.expander(f"🎯 {match.name} - {len(shared_courses)} shared course(s)", expanded=True):
                                col1, col2 = st.columns([2, 1])

                                with col1:
                                    st.write(f"**Shared courses:** {', '.join(shared_courses)}")
                                    st.write(f"**Learning style:** {match.learning_style}")
                                    st.write(f"**Available:** {', '.join(match.availability)}")

                                    if match.bio:
                                        st.caption(f"*\"{match.bio}\"*")

                                    # AI Match Explanation
                                    with st.spinner("Getting AI insights..."):
                                        explanation = ai_match_explanation(user, match, client)
                                        st.info(f"💡 **Why this match?** {explanation}")

                                with col2:
                                    if st.button(f"✨ Ice Breaker", key=f"icebreaker_{match.id}"):
                                        with st.spinner("Generating message..."):
                                            message = generate_ice_breaker(user, match, client)
                                            st.success("**Suggested message:**")
                                            st.write(f"*{message}*")
                else:
                    st.info("No other students yet. Invite your classmates!")

    with tab2:
        st.subheader("Your Profile")

        existing = next((p for p in profiles if p.id == st.session_state.user_id), None) if st.session_state.user_id else None

        with st.form("profile"):
            name = st.text_input("Name", value=existing.name if existing else "")
            courses = st.text_input("Courses (comma-separated)", value=", ".join(existing.courses) if existing else "")
            learning_style = st.selectbox("Learning Style", LEARNING_STYLES)
            availability = st.multiselect("Availability", ["Mornings", "Afternoons", "Evenings", "Weekends"])
            locations = st.multiselect("Preferred Locations", ["Firestone", "Lewis", "Frist", "Coffee Shop"])
            bio = st.text_area("Bio", value=existing.bio if existing else "")

            if st.form_submit_button("Save", type="primary"):
                if name and courses:
                    courses_list = [c.strip().upper() for c in courses.split(",")]

                    if existing:
                        existing.name = name
                        existing.courses = courses_list
                        existing.learning_style = learning_style
                        existing.availability = availability
                        existing.preferred_locations = locations
                        existing.bio = bio
                    else:
                        new_profile = StudentProfile(
                            id=str(len(profiles) + 1),
                            name=name,
                            courses=courses_list,
                            learning_style=learning_style,
                            availability=availability,
                            preferred_locations=locations,
                            bio=bio
                        )
                        profiles.append(new_profile)
                        st.session_state.user_id = new_profile.id

                    save_profiles(profiles)
                    st.success("Profile saved!")
                    st.rerun()


if __name__ == "__main__":
    main()
