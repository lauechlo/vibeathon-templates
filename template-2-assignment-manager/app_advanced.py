"""
Course & Assignment Manager - Advanced Version
AI-powered assignment tracking with Claude!

Features:
- Natural language assignment input
- AI-generated study plans
- Personalized productivity tips
- Intelligent deadline management
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="AI Assignment Manager",
    page_icon="🤖",
    layout="wide"
)

# Constants
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "assignments.json")
ASSIGNMENT_TYPES = ["Homework", "Project", "Essay", "Exam", "Reading", "Lab", "Presentation", "Other"]


# Initialize Anthropic client
@st.cache_resource
def get_anthropic_client():
    """Initialize and cache the Anthropic client."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("⚠️ ANTHROPIC_API_KEY not found in .env file!")
        st.stop()
    return Anthropic(api_key=api_key)


@dataclass
class Assignment:
    """Represents a single assignment."""
    id: str
    course: str
    title: str
    description: str
    due_date: str
    assignment_type: str
    completed: bool = False
    created_at: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

    def days_until_due(self) -> int:
        due = datetime.fromisoformat(self.due_date)
        return (due - datetime.now()).days

    def is_overdue(self) -> bool:
        return self.days_until_due() < 0 and not self.completed

    def is_due_soon(self, days_threshold: int = 3) -> bool:
        days = self.days_until_due()
        return 0 <= days <= days_threshold and not self.completed


def initialize_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_assignments() -> List[Assignment]:
    initialize_data_dir()
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                return [Assignment(**a) for a in data]
        except Exception as e:
            st.error(f"Error loading assignments: {e}")
            return []
    return []


def save_assignments(assignments: List[Assignment]):
    initialize_data_dir()
    try:
        with open(DATA_FILE, 'w') as f:
            data = [asdict(a) for a in assignments]
            json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f"Error saving assignments: {e}")


def generate_assignment_id() -> str:
    import uuid
    return str(uuid.uuid4())[:8]


def parse_natural_language_assignment(text: str, client) -> dict:
    """Use Claude to parse natural language assignment description."""
    prompt = f"""Parse this assignment description into structured data. Extract:
- course: course code or name
- title: brief title
- assignment_type: one of [{', '.join(ASSIGNMENT_TYPES)}]
- due_date: in ISO format (YYYY-MM-DD)
- description: any additional details

Today's date: {datetime.now().strftime('%Y-%m-%d')}

User input: "{text}"

Return ONLY a JSON object with these exact keys: course, title, assignment_type, due_date, description

Example: {{"course": "COS 126", "title": "Programming Assignment 3", "assignment_type": "Homework", "due_date": "2024-03-20", "description": ""}}"""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text.strip()
        parsed = json.loads(response_text)

        # Validate required fields
        required = ['course', 'title', 'assignment_type', 'due_date']
        if all(k in parsed for k in required):
            return parsed
        return None

    except Exception as e:
        st.error(f"Error parsing assignment: {e}")
        return None


def generate_study_plan(assignment: Assignment, client) -> str:
    """Generate AI study plan for an assignment."""
    due_date = datetime.fromisoformat(assignment.due_date)
    days_until = assignment.days_until_due()

    prompt = f"""Create a brief study plan for this assignment:

Assignment: {assignment.title}
Course: {assignment.course}
Type: {assignment.assignment_type}
Due: {due_date.strftime('%B %d, %Y')} ({days_until} days from now)
Description: {assignment.description}

Provide a 3-5 step action plan with suggested dates. Be specific and practical.
Format as a bulleted list. Keep it concise (3-4 sentences max)."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}]
        )

        return message.content[0].text.strip()

    except Exception as e:
        return f"Error generating study plan: {e}"


def get_productivity_tips(assignments: List[Assignment], client) -> str:
    """Get AI-powered productivity tips based on current workload."""
    upcoming = [a for a in assignments if not a.completed and not a.is_overdue()]
    upcoming.sort(key=lambda x: x.due_date)

    if not upcoming:
        return "Great job! You're all caught up. Take some time to relax or get ahead on future work."

    # Create summary of workload
    workload_summary = f"Current workload: {len(upcoming)} assignments\n\n"
    for a in upcoming[:5]:
        days = a.days_until_due()
        workload_summary += f"- {a.course} {a.assignment_type}: {days} days\n"

    prompt = f"""{workload_summary}

Based on this workload, provide 2-3 specific, actionable productivity tips.
Be encouraging and practical. Keep it brief (3-4 sentences total)."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}]
        )

        return message.content[0].text.strip()

    except Exception as e:
        return f"Error generating tips: {e}"


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Initialize Claude client
    client = get_anthropic_client()

    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("🤖 AI Assignment Manager")
        st.markdown("Smart assignment tracking with Claude-powered insights")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("✨ **AI Enhanced**")

    # Load assignments
    assignments = load_assignments()

    # Sidebar
    with st.sidebar:
        st.header("📊 Dashboard")

        total = len(assignments)
        completed = sum(1 for a in assignments if a.completed)
        overdue = sum(1 for a in assignments if a.is_overdue())
        upcoming = sum(1 for a in assignments if a.is_due_soon())

        st.metric("Total Assignments", total)
        st.metric("Completed", completed)
        st.metric("⚡ Due Soon", upcoming)
        st.metric("⚠️ Overdue", overdue)

        # AI Productivity Tips
        if assignments:
            st.divider()
            st.subheader("💡 AI Tips")
            with st.spinner("Generating tips..."):
                tips = get_productivity_tips(assignments, client)
                st.info(tips)

    # Main tabs
    tab1, tab2, tab3 = st.tabs(["📋 Upcoming", "✨ Add with AI", "📚 All"])

    # TAB 1: Upcoming Dashboard
    with tab1:
        st.header("📋 Upcoming Deadlines")

        upcoming_assignments = [a for a in assignments if not a.completed and not a.is_overdue()]
        upcoming_assignments.sort(key=lambda x: x.due_date)

        if upcoming_assignments:
            for assignment in upcoming_assignments[:10]:
                with st.expander(
                    f"**{assignment.course}** - {assignment.title} "
                    f"({assignment.days_until_due()} days)",
                    expanded=assignment.is_due_soon()
                ):
                    col1, col2 = st.columns([2, 1])

                    with col1:
                        st.write(f"**Type:** {assignment.assignment_type}")
                        due_date = datetime.fromisoformat(assignment.due_date)
                        st.write(f"**Due:** {due_date.strftime('%B %d, %Y at %I:%M %p')}")

                        if assignment.description:
                            st.write(f"**Description:** {assignment.description}")

                        # AI Study Plan
                        if st.button(f"✨ Generate Study Plan", key=f"plan_{assignment.id}"):
                            with st.spinner("Creating your study plan..."):
                                study_plan = generate_study_plan(assignment, client)
                                st.markdown("**📅 Suggested Study Plan:**")
                                st.markdown(study_plan)

                    with col2:
                        if st.button("✅ Mark Complete", key=f"complete_{assignment.id}"):
                            for a in assignments:
                                if a.id == assignment.id:
                                    a.completed = True
                            save_assignments(assignments)
                            st.success("Completed!")
                            st.rerun()

        else:
            st.success("🎉 All caught up! No upcoming assignments.")

    # TAB 2: AI-Powered Add
    with tab2:
        st.header("✨ Add Assignment with AI")
        st.markdown("**Just describe your assignment naturally!**")

        # Examples
        with st.expander("💡 See examples"):
            st.write("""
            Try phrases like:
            - "Essay on Kant's ethics for PHI 201 due next Friday"
            - "COS 126 programming assignment 3 due March 20th"
            - "Math problem set 5 for MAT 201, due in 5 days"
            - "Reading response for ENG 101 due this Thursday"
            """)

        # Natural language input
        nl_input = st.text_area(
            "Describe your assignment:",
            placeholder="e.g., 'Essay on modernism for ENG 215 due March 25th'",
            height=100
        )

        if st.button("✨ Parse with AI", type="primary", disabled=not nl_input):
            with st.spinner("🤖 Understanding your assignment..."):
                parsed = parse_natural_language_assignment(nl_input, client)

                if parsed:
                    st.success("✅ Assignment parsed!")

                    # Show parsed data and allow editing
                    st.subheader("Review & Edit")

                    with st.form("confirm_ai_assignment"):
                        col1, col2 = st.columns(2)

                        with col1:
                            course = st.text_input("Course", value=parsed.get('course', ''))
                            title = st.text_input("Title", value=parsed.get('title', ''))
                            assignment_type = st.selectbox(
                                "Type",
                                options=ASSIGNMENT_TYPES,
                                index=ASSIGNMENT_TYPES.index(parsed.get('assignment_type', 'Other'))
                                if parsed.get('assignment_type') in ASSIGNMENT_TYPES else 0
                            )

                        with col2:
                            due_date_str = parsed.get('due_date', '')
                            try:
                                due_date = datetime.fromisoformat(due_date_str).date()
                            except:
                                due_date = datetime.now().date()

                            due_date_input = st.date_input("Due Date", value=due_date)
                            due_time = st.time_input("Due Time", value=None)

                        description = st.text_area(
                            "Description",
                            value=parsed.get('description', ''),
                            height=100
                        )

                        if st.form_submit_button("➕ Add Assignment", type="primary"):
                            if due_time:
                                due_datetime = datetime.combine(due_date_input, due_time)
                            else:
                                due_datetime = datetime.combine(due_date_input, datetime.max.time())

                            new_assignment = Assignment(
                                id=generate_assignment_id(),
                                course=course.strip().upper(),
                                title=title.strip(),
                                description=description.strip(),
                                due_date=due_datetime.isoformat(),
                                assignment_type=assignment_type,
                                completed=False
                            )

                            assignments.append(new_assignment)
                            save_assignments(assignments)

                            st.success(f"✅ Added: {title}")
                            st.balloons()
                            st.rerun()
                else:
                    st.error("Couldn't parse assignment. Please try again or use manual entry.")

        # Manual entry option
        st.divider()
        st.subheader("Or Add Manually")

        with st.form("manual_add"):
            col1, col2 = st.columns(2)

            with col1:
                course = st.text_input("Course Code")
                title = st.text_input("Assignment Title")
                assignment_type = st.selectbox("Type", options=ASSIGNMENT_TYPES)

            with col2:
                due_date = st.date_input("Due Date")
                due_time = st.time_input("Due Time (optional)", value=None)

            description = st.text_area("Description (optional)", height=100)

            if st.form_submit_button("➕ Add"):
                if course and title:
                    if due_time:
                        due_datetime = datetime.combine(due_date, due_time)
                    else:
                        due_datetime = datetime.combine(due_date, datetime.max.time())

                    new_assignment = Assignment(
                        id=generate_assignment_id(),
                        course=course.strip().upper(),
                        title=title.strip(),
                        description=description.strip(),
                        due_date=due_datetime.isoformat(),
                        assignment_type=assignment_type,
                        completed=False
                    )

                    assignments.append(new_assignment)
                    save_assignments(assignments)
                    st.success(f"✅ Added: {title}")
                    st.rerun()
                else:
                    st.error("Please fill in course and title!")

    # TAB 3: All Assignments
    with tab3:
        st.header("📚 All Assignments")

        show_completed = st.checkbox("Show completed", value=False)
        filtered = [a for a in assignments if show_completed or not a.completed]
        filtered.sort(key=lambda x: x.due_date)

        if filtered:
            for assignment in filtered:
                col1, col2, col3 = st.columns([3, 2, 1])

                with col1:
                    if assignment.completed:
                        st.markdown(f"~~**{assignment.course}**: {assignment.title}~~")
                    else:
                        st.markdown(f"**{assignment.course}**: {assignment.title}")

                with col2:
                    due_date = datetime.fromisoformat(assignment.due_date)
                    st.write(f"📅 {due_date.strftime('%b %d, %Y')}")

                with col3:
                    if not assignment.completed:
                        if st.button("✅", key=f"all_complete_{assignment.id}"):
                            for a in assignments:
                                if a.id == assignment.id:
                                    a.completed = True
                            save_assignments(assignments)
                            st.rerun()

                    if st.button("🗑️", key=f"delete_{assignment.id}"):
                        assignments.remove(assignment)
                        save_assignments(assignments)
                        st.rerun()

                st.divider()
        else:
            st.info("No assignments to show.")

    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: gray;'>
    <p>🤖 Powered by Claude AI | Built with ❤️ for students</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
