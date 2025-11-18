"""
Study Group Matcher - Beginner Version
Find study partners for your courses!
"""

import streamlit as st
import json
import os
from dataclasses import dataclass, asdict
from typing import List

st.set_page_config(page_title="Study Matcher", page_icon="🤝", layout="wide")

DATA_DIR = "data"
PROFILES_FILE = os.path.join(DATA_DIR, "profiles.json")

LEARNING_STYLES = ["Visual", "Auditory", "Reading/Writing", "Kinesthetic", "Mixed"]
AVAILABILITY = ["Mornings", "Afternoons", "Evenings", "Weekends", "Flexible"]
LOCATIONS = ["Firestone", "Lewis Library", "Frist", "Dorm Study Room", "Coffee Shop", "Anywhere"]


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
            data = json.load(f)
            return [StudentProfile(**p) for p in data]
    return []


def save_profiles(profiles):
    with open(PROFILES_FILE, 'w') as f:
        json.dump([asdict(p) for p in profiles], f, indent=2)


def calculate_match_score(profile1: StudentProfile, profile2: StudentProfile) -> float:
    """Simple matching algorithm based on shared attributes."""
    score = 0

    # Shared courses (most important)
    shared_courses = set(profile1.courses) & set(profile2.courses)
    score += len(shared_courses) * 40

    # Availability overlap
    shared_availability = set(profile1.availability) & set(profile2.availability)
    score += len(shared_availability) * 15

    # Location preferences
    shared_locations = set(profile1.preferred_locations) & set(profile2.preferred_locations)
    score += len(shared_locations) * 10

    # Learning style match
    if profile1.learning_style == profile2.learning_style:
        score += 20

    return min(score, 100)  # Cap at 100


def find_matches(current_profile: StudentProfile, all_profiles: List[StudentProfile]) -> List[tuple]:
    """Find and rank potential study partners."""
    matches = []

    for profile in all_profiles:
        if profile.id != current_profile.id:
            score = calculate_match_score(current_profile, profile)
            if score > 20:  # Minimum threshold
                matches.append((profile, score))

    # Sort by score descending
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches


def main():
    st.title("🤝 Study Group Matcher")
    st.markdown("Find the perfect study partners for your courses!")

    profiles = load_profiles()

    # Check if user has a profile
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None

    # Sidebar - User profile
    with st.sidebar:
        st.header("👤 Your Profile")

        if st.session_state.user_id:
            user_profile = next((p for p in profiles if p.id == st.session_state.user_id), None)
            if user_profile:
                st.success(f"Logged in as: **{user_profile.name}**")
                st.write(f"**Courses:** {', '.join(user_profile.courses)}")
                st.write(f"**Learning Style:** {user_profile.learning_style}")

                if st.button("Edit Profile"):
                    st.session_state.user_id = None
                    st.rerun()
        else:
            st.info("Create or select your profile to find matches!")

    # Main tabs
    tab1, tab2, tab3 = st.tabs(["🔍 Find Matches", "👤 My Profile", "📋 All Students"])

    with tab1:
        if not st.session_state.user_id:
            st.warning("Please create or select your profile first!")
        else:
            user_profile = next((p for p in profiles if p.id == st.session_state.user_id), None)

            if user_profile:
                st.subheader("Your Best Matches")

                matches = find_matches(user_profile, profiles)

                if matches:
                    for profile, score in matches:
                        with st.container():
                            col1, col2, col3 = st.columns([3, 2, 1])

                            with col1:
                                st.markdown(f"### {profile.name}")
                                if profile.bio:
                                    st.write(profile.bio)

                                # Shared courses
                                shared_courses = set(user_profile.courses) & set(profile.courses)
                                if shared_courses:
                                    st.write(f"**Shared courses:** {', '.join(shared_courses)}")

                            with col2:
                                st.write(f"**Learning Style:** {profile.learning_style}")
                                st.write(f"**Available:** {', '.join(profile.availability)}")
                                st.write(f"**Locations:** {', '.join(profile.preferred_locations)}")

                            with col3:
                                st.metric("Match Score", f"{score}%")

                                if score >= 70:
                                    st.success("Great match!")
                                elif score >= 50:
                                    st.info("Good match")
                                else:
                                    st.warning("Okay match")

                            st.divider()
                else:
                    st.info("No matches found yet. More students will join soon!")

    with tab2:
        st.subheader("Create or Update Your Profile")

        # Get existing profile if editing
        existing = next((p for p in profiles if p.id == st.session_state.user_id), None) if st.session_state.user_id else None

        with st.form("profile_form"):
            name = st.text_input("Name *", value=existing.name if existing else "")

            courses_input = st.text_input(
                "Courses (comma-separated) *",
                value=", ".join(existing.courses) if existing else "",
                placeholder="e.g., COS 126, MAT 201, PHI 201"
            )

            learning_style = st.selectbox(
                "Learning Style",
                options=LEARNING_STYLES,
                index=LEARNING_STYLES.index(existing.learning_style) if existing else 0
            )

            availability_select = st.multiselect(
                "When are you available?",
                options=AVAILABILITY,
                default=existing.availability if existing else []
            )

            locations_select = st.multiselect(
                "Preferred study locations",
                options=LOCATIONS,
                default=existing.preferred_locations if existing else []
            )

            bio = st.text_area(
                "Bio (optional)",
                value=existing.bio if existing else "",
                placeholder="Tell others about your study habits, goals, or interests..."
            )

            submitted = st.form_submit_button("Save Profile", type="primary")

            if submitted:
                if not name or not courses_input:
                    st.error("Please fill in name and courses!")
                else:
                    courses_list = [c.strip().upper() for c in courses_input.split(",") if c.strip()]

                    if existing:
                        # Update existing profile
                        existing.name = name
                        existing.courses = courses_list
                        existing.learning_style = learning_style
                        existing.availability = availability_select
                        existing.preferred_locations = locations_select
                        existing.bio = bio

                        save_profiles(profiles)
                        st.success("Profile updated!")
                    else:
                        # Create new profile
                        new_id = str(len(profiles) + 1)
                        new_profile = StudentProfile(
                            id=new_id,
                            name=name,
                            courses=courses_list,
                            learning_style=learning_style,
                            availability=availability_select,
                            preferred_locations=locations_select,
                            bio=bio
                        )

                        profiles.append(new_profile)
                        save_profiles(profiles)

                        st.session_state.user_id = new_id
                        st.success(f"Profile created! Welcome, {name}!")

                    st.rerun()

    with tab3:
        st.subheader("All Student Profiles")

        if profiles:
            # Filter by course
            all_courses = sorted(set(c for p in profiles for c in p.courses))
            filter_course = st.selectbox("Filter by course", ["All"] + all_courses)

            filtered = profiles
            if filter_course != "All":
                filtered = [p for p in profiles if filter_course in p.courses]

            st.write(f"Showing {len(filtered)} student(s)")

            for profile in filtered:
                with st.expander(f"{profile.name} - {', '.join(profile.courses)}"):
                    col1, col2 = st.columns(2)

                    with col1:
                        if profile.bio:
                            st.write(f"**Bio:** {profile.bio}")
                        st.write(f"**Courses:** {', '.join(profile.courses)}")

                    with col2:
                        st.write(f"**Learning Style:** {profile.learning_style}")
                        st.write(f"**Available:** {', '.join(profile.availability)}")
                        st.write(f"**Prefers:** {', '.join(profile.preferred_locations)}")

        else:
            st.info("No profiles yet. Be the first to create one!")


if __name__ == "__main__":
    main()
