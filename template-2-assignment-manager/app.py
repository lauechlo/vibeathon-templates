"""
Course & Assignment Manager - Beginner Version
Track assignments, deadlines, and never miss a due date!

This version uses basic Python and Streamlit - no AI required.
Perfect for learning CRUD operations and deadline management.
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Optional

# Configure the page
st.set_page_config(
    page_title="Assignment Manager",
    page_icon="📝",
    layout="wide"
)

# Constants
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "assignments.json")

# Assignment categories
ASSIGNMENT_TYPES = [
    "Homework",
    "Project",
    "Essay",
    "Exam",
    "Reading",
    "Lab",
    "Presentation",
    "Other"
]


@dataclass
class Assignment:
    """Represents a single assignment."""
    id: str
    course: str
    title: str
    description: str
    due_date: str  # Store as ISO format string
    assignment_type: str
    completed: bool = False
    created_at: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

    def days_until_due(self) -> int:
        """Calculate days until due date."""
        due = datetime.fromisoformat(self.due_date)
        now = datetime.now()
        delta = due - now
        return delta.days

    def is_overdue(self) -> bool:
        """Check if assignment is overdue."""
        return self.days_until_due() < 0 and not self.completed

    def is_due_soon(self, days_threshold: int = 3) -> bool:
        """Check if assignment is due within threshold."""
        days = self.days_until_due()
        return 0 <= days <= days_threshold and not self.completed


def initialize_data_dir():
    """Create data directory if it doesn't exist."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_assignments() -> List[Assignment]:
    """Load assignments from JSON file."""
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
    """Save assignments to JSON file."""
    initialize_data_dir()

    try:
        with open(DATA_FILE, 'w') as f:
            data = [asdict(a) for a in assignments]
            json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f"Error saving assignments: {e}")


def generate_assignment_id() -> str:
    """Generate unique ID for assignment."""
    import uuid
    return str(uuid.uuid4())[:8]


def get_unique_courses(assignments: List[Assignment]) -> List[str]:
    """Get list of unique course names."""
    courses = sorted(set(a.course for a in assignments))
    return courses


def get_course_stats(assignments: List[Assignment], course: str) -> dict:
    """Get statistics for a specific course."""
    course_assignments = [a for a in assignments if a.course == course]

    if not course_assignments:
        return None

    total = len(course_assignments)
    completed = sum(1 for a in course_assignments if a.completed)
    incomplete = total - completed

    return {
        'total': total,
        'completed': completed,
        'incomplete': incomplete,
        'completion_rate': (completed / total * 100) if total > 0 else 0
    }


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Header
    st.title("📝 Course & Assignment Manager")
    st.markdown("Track all your assignments and deadlines in one place!")

    # Load assignments
    assignments = load_assignments()

    # Sidebar - Course overview
    with st.sidebar:
        st.header("📚 Courses")

        courses = get_unique_courses(assignments)

        if courses:
            for course in courses:
                stats = get_course_stats(assignments, course)
                if stats:
                    with st.expander(f"**{course}**", expanded=False):
                        st.metric("Total Assignments", stats['total'])
                        st.metric("Completed", stats['completed'])
                        st.metric("Incomplete", stats['incomplete'])
                        st.progress(stats['completion_rate'] / 100)
                        st.caption(f"{stats['completion_rate']:.0f}% complete")
        else:
            st.info("No courses yet. Add your first assignment below!")

        st.divider()

        # Quick stats
        st.subheader("📊 Overall Stats")
        total_assignments = len(assignments)
        completed_assignments = sum(1 for a in assignments if a.completed)
        overdue_assignments = sum(1 for a in assignments if a.is_overdue())

        st.metric("Total Assignments", total_assignments)
        st.metric("Completed", completed_assignments)
        st.metric("⚠️ Overdue", overdue_assignments)

    # Main content - Tabs
    tab1, tab2, tab3 = st.tabs(["📋 Dashboard", "➕ Add Assignment", "📚 All Assignments"])

    # TAB 1: Dashboard
    with tab1:
        st.header("📋 Upcoming Deadlines")

        # Filter upcoming assignments (not completed, not overdue)
        upcoming = [a for a in assignments if not a.completed and not a.is_overdue()]
        upcoming.sort(key=lambda x: x.due_date)

        if upcoming:
            # Due soon (within 3 days)
            due_soon = [a for a in upcoming if a.is_due_soon()]

            if due_soon:
                st.subheader("⚡ Due Soon (Next 3 Days)")
                for assignment in due_soon:
                    days = assignment.days_until_due()
                    col1, col2, col3 = st.columns([3, 2, 1])

                    with col1:
                        st.markdown(f"**{assignment.course}**: {assignment.title}")
                        if assignment.description:
                            st.caption(assignment.description)

                    with col2:
                        due_date = datetime.fromisoformat(assignment.due_date)
                        st.write(f"📅 {due_date.strftime('%b %d, %Y')}")
                        if days == 0:
                            st.error("Due TODAY!")
                        elif days == 1:
                            st.warning("Due tomorrow")
                        else:
                            st.info(f"Due in {days} days")

                    with col3:
                        if st.button("✓ Done", key=f"complete_{assignment.id}"):
                            for a in assignments:
                                if a.id == assignment.id:
                                    a.completed = True
                            save_assignments(assignments)
                            st.rerun()

                st.divider()

            # Rest of upcoming assignments
            st.subheader("📅 Coming Up")
            other_upcoming = [a for a in upcoming if not a.is_due_soon()]

            if other_upcoming:
                for assignment in other_upcoming[:10]:  # Show next 10
                    days = assignment.days_until_due()
                    col1, col2, col3 = st.columns([3, 2, 1])

                    with col1:
                        st.markdown(f"**{assignment.course}**: {assignment.title}")

                    with col2:
                        due_date = datetime.fromisoformat(assignment.due_date)
                        st.write(f"📅 {due_date.strftime('%b %d, %Y')} ({days} days)")

                    with col3:
                        if st.button("✓", key=f"complete_upcoming_{assignment.id}"):
                            for a in assignments:
                                if a.id == assignment.id:
                                    a.completed = True
                            save_assignments(assignments)
                            st.rerun()
            else:
                st.success("All caught up! No assignments due soon.")

        else:
            st.success("🎉 All caught up! No upcoming assignments.")

        # Show overdue assignments if any
        overdue = [a for a in assignments if a.is_overdue()]
        if overdue:
            st.divider()
            st.subheader("⚠️ Overdue")
            for assignment in overdue:
                days_overdue = abs(assignment.days_until_due())
                col1, col2, col3 = st.columns([3, 2, 1])

                with col1:
                    st.markdown(f"**{assignment.course}**: {assignment.title}")

                with col2:
                    st.error(f"Overdue by {days_overdue} days")

                with col3:
                    if st.button("✓", key=f"complete_overdue_{assignment.id}"):
                        for a in assignments:
                            if a.id == assignment.id:
                                a.completed = True
                        save_assignments(assignments)
                        st.rerun()

    # TAB 2: Add Assignment
    with tab2:
        st.header("➕ Add New Assignment")

        with st.form("add_assignment_form"):
            col1, col2 = st.columns(2)

            with col1:
                # Course input (with suggestions from existing courses)
                existing_courses = get_unique_courses(assignments)
                course = st.text_input(
                    "Course Code *",
                    placeholder="e.g., COS 126, PHI 201",
                    help="Enter course code or name"
                )

                # Show existing courses for reference
                if existing_courses:
                    st.caption(f"Your courses: {', '.join(existing_courses)}")

                title = st.text_input(
                    "Assignment Title *",
                    placeholder="e.g., Problem Set 3, Essay on Kant"
                )

                assignment_type = st.selectbox(
                    "Type",
                    options=ASSIGNMENT_TYPES
                )

            with col2:
                due_date = st.date_input(
                    "Due Date *",
                    min_value=datetime.now().date(),
                    help="When is this assignment due?"
                )

                # Add time for more precise deadlines
                due_time = st.time_input(
                    "Due Time (optional)",
                    value=None,
                    help="Assignment deadline time"
                )

            description = st.text_area(
                "Description (optional)",
                placeholder="Add any additional details, requirements, or notes...",
                height=100
            )

            submitted = st.form_submit_button("➕ Add Assignment", type="primary", use_container_width=True)

            if submitted:
                if not course or not title:
                    st.error("Please fill in course and title fields!")
                else:
                    # Combine date and time
                    if due_time:
                        due_datetime = datetime.combine(due_date, due_time)
                    else:
                        # Default to end of day (23:59)
                        due_datetime = datetime.combine(due_date, datetime.max.time())

                    # Create assignment
                    new_assignment = Assignment(
                        id=generate_assignment_id(),
                        course=course.strip().upper(),  # Normalize course codes
                        title=title.strip(),
                        description=description.strip(),
                        due_date=due_datetime.isoformat(),
                        assignment_type=assignment_type,
                        completed=False
                    )

                    # Add to list and save
                    assignments.append(new_assignment)
                    save_assignments(assignments)

                    st.success(f"✅ Added: {title} for {course}")
                    st.balloons()
                    st.rerun()

    # TAB 3: All Assignments
    with tab3:
        st.header("📚 All Assignments")

        # Filter options
        col1, col2, col3 = st.columns(3)

        with col1:
            show_completed = st.checkbox("Show completed", value=False)

        with col2:
            filter_course = st.selectbox(
                "Filter by course",
                options=["All"] + get_unique_courses(assignments)
            )

        with col3:
            sort_by = st.selectbox(
                "Sort by",
                options=["Due Date", "Course", "Type", "Created"]
            )

        # Apply filters
        filtered = assignments.copy()

        if not show_completed:
            filtered = [a for a in filtered if not a.completed]

        if filter_course != "All":
            filtered = [a for a in filtered if a.course == filter_course]

        # Apply sorting
        if sort_by == "Due Date":
            filtered.sort(key=lambda x: x.due_date)
        elif sort_by == "Course":
            filtered.sort(key=lambda x: x.course)
        elif sort_by == "Type":
            filtered.sort(key=lambda x: x.assignment_type)
        elif sort_by == "Created":
            filtered.sort(key=lambda x: x.created_at, reverse=True)

        # Display assignments
        if filtered:
            st.write(f"Showing {len(filtered)} assignment(s)")

            for assignment in filtered:
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

                    with col1:
                        if assignment.completed:
                            st.markdown(f"~~**{assignment.course}**: {assignment.title}~~")
                        else:
                            st.markdown(f"**{assignment.course}**: {assignment.title}")

                        if assignment.description:
                            st.caption(assignment.description)

                    with col2:
                        st.write(f"📊 {assignment.assignment_type}")

                    with col3:
                        due_date = datetime.fromisoformat(assignment.due_date)
                        st.write(f"📅 {due_date.strftime('%b %d, %Y')}")

                        if not assignment.completed:
                            days = assignment.days_until_due()
                            if assignment.is_overdue():
                                st.error(f"Overdue by {abs(days)} days")
                            elif assignment.is_due_soon():
                                st.warning(f"Due in {days} days")
                            else:
                                st.info(f"{days} days")

                    with col4:
                        if assignment.completed:
                            st.success("✓ Done")
                        else:
                            if st.button("✓", key=f"all_{assignment.id}"):
                                for a in assignments:
                                    if a.id == assignment.id:
                                        a.completed = True
                                save_assignments(assignments)
                                st.rerun()

                        # Delete button
                        if st.button("🗑️", key=f"delete_{assignment.id}"):
                            assignments.remove(assignment)
                            save_assignments(assignments)
                            st.rerun()

                    st.divider()
        else:
            st.info("No assignments match your filters.")

    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: gray;'>
    <p>💡 <b>Tip:</b> Want AI-powered study plans? Check out <code>app_advanced.py</code>!</p>
    <p>Built with ❤️ for students</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
