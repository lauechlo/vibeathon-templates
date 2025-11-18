"""
Internship Application Tracker - Beginner Version
Track your internship applications and never miss a deadline!
"""

import streamlit as st
import json
import os
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List

st.set_page_config(page_title="Internship Tracker", page_icon="💼", layout="wide")

DATA_DIR = "data"
APPS_FILE = os.path.join(DATA_DIR, "applications.json")

STATUSES = ["Researching", "Applied", "Phone Screen", "Interview", "Offer", "Accepted", "Rejected"]


@dataclass
class Application:
    id: str
    company: str
    position: str
    location: str
    deadline: str
    applied_date: str
    status: str
    notes: str = ""
    follow_up_date: str = None


def init_data():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_apps():
    init_data()
    if os.path.exists(APPS_FILE):
        with open(APPS_FILE, 'r') as f:
            return [Application(**a) for a in json.load(f)]
    return []


def save_apps(apps):
    with open(APPS_FILE, 'w') as f:
        json.dump([asdict(a) for a in apps], f, indent=2)


def main():
    st.title("💼 Internship Application Tracker")
    st.markdown("Manage your internship search efficiently!")

    if 'apps' not in st.session_state:
        st.session_state.apps = load_apps()

    apps = st.session_state.apps

    # Sidebar stats
    with st.sidebar:
        st.header("📊 Statistics")
        st.metric("Total Applications", len(apps))
        st.metric("In Progress", len([a for a in apps if a.status not in ["Accepted", "Rejected"]]))
        st.metric("Offers", len([a for a in apps if a.status == "Offer"]))

        # Upcoming deadlines
        st.divider()
        st.subheader("⏰ Upcoming")
        upcoming = [a for a in apps if a.deadline and datetime.fromisoformat(a.deadline) > datetime.now()]
        upcoming.sort(key=lambda x: x.deadline)

        for app in upcoming[:5]:
            days = (datetime.fromisoformat(app.deadline) - datetime.now()).days
            st.write(f"**{app.company}** - {days}d")

    tab1, tab2, tab3 = st.tabs(["➕ Add Application", "📋 All Applications", "📊 Dashboard"])

    # TAB 1: Add
    with tab1:
        st.header("Add New Application")

        with st.form("add_app"):
            col1, col2 = st.columns(2)

            with col1:
                company = st.text_input("Company *", placeholder="Google")
                position = st.text_input("Position *", placeholder="Software Engineering Intern")
                location = st.text_input("Location", placeholder="Mountain View, CA")

            with col2:
                deadline = st.date_input("Application Deadline")
                applied_date = st.date_input("Date Applied (if already applied)")
                status = st.selectbox("Status", STATUSES)

            notes = st.text_area("Notes", placeholder="Job description, requirements, contact info...")

            if st.form_submit_button("Add Application", type="primary"):
                if company and position:
                    new_app = Application(
                        id=str(len(apps) + 1),
                        company=company,
                        position=position,
                        location=location,
                        deadline=deadline.isoformat(),
                        applied_date=applied_date.isoformat() if applied_date else None,
                        status=status,
                        notes=notes
                    )
                    apps.append(new_app)
                    save_apps(apps)
                    st.success(f"✅ Added {position} at {company}!")
                    st.rerun()
                else:
                    st.error("Please fill in company and position!")

    # TAB 2: All Applications
    with tab2:
        st.header("All Applications")

        if apps:
            for app in sorted(apps, key=lambda x: x.deadline if x.deadline else "9999"):
                with st.expander(f"**{app.company}** - {app.position} ({app.status})"):
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.write(f"**Position:** {app.position}")
                        st.write(f"**Location:** {app.location}")
                        st.write(f"**Deadline:** {app.deadline}")
                        st.write(f"**Status:** {app.status}")
                        if app.notes:
                            st.write(f"**Notes:** {app.notes}")

                    with col2:
                        # Update status
                        new_status = st.selectbox("Update Status", STATUSES,
                                                 index=STATUSES.index(app.status),
                                                 key=f"status_{app.id}")
                        if new_status != app.status:
                            app.status = new_status
                            save_apps(apps)
                            st.success("Status updated!")
                            st.rerun()

                        if st.button("🗑️ Delete", key=f"del_{app.id}"):
                            apps.remove(app)
                            save_apps(apps)
                            st.rerun()
        else:
            st.info("No applications yet. Add one in the first tab!")

    # TAB 3: Dashboard
    with tab3:
        st.header("Application Dashboard")

        if apps:
            # Status breakdown
            st.subheader("Status Breakdown")
            status_counts = {}
            for app in apps:
                status_counts[app.status] = status_counts.get(app.status, 0) + 1

            cols = st.columns(len(status_counts))
            for i, (status, count) in enumerate(status_counts.items()):
                with cols[i]:
                    st.metric(status, count)

            # Recent activity
            st.divider()
            st.subheader("Recent Applications")
            recent = sorted(apps, key=lambda x: x.applied_date if x.applied_date else "1900-01-01", reverse=True)[:5]

            for app in recent:
                st.write(f"**{app.company}** - {app.position} ({app.status})")
        else:
            st.info("No data yet. Start adding applications!")


if __name__ == "__main__":
    main()
