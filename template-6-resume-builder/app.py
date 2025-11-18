"""
Resume & Cover Letter Builder - Beginner Version
Build professional resumes with a simple form-based interface.

This version doesn't require AI - perfect for getting started!
"""

import streamlit as st
import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict, field
from typing import List

# Configure the page
st.set_page_config(
    page_title="Resume Builder",
    page_icon="📄",
    layout="wide"
)

# Constants
DATA_DIR = "data"
RESUME_FILE = os.path.join(DATA_DIR, "resume_data.json")

# Action verbs for bullet points
ACTION_VERBS = [
    "Achieved", "Analyzed", "Built", "Collaborated", "Created", "Designed",
    "Developed", "Directed", "Established", "Implemented", "Improved", "Increased",
    "Led", "Managed", "Organized", "Presented", "Reduced", "Researched",
    "Solved", "Streamlined"
]


@dataclass
class Experience:
    """Work or internship experience."""
    company: str
    position: str
    location: str
    start_date: str
    end_date: str
    current: bool
    bullets: List[str] = field(default_factory=list)


@dataclass
class Education:
    """Educational background."""
    school: str
    degree: str
    major: str
    minor: str
    gpa: str
    graduation: str
    relevant_coursework: List[str] = field(default_factory=list)


@dataclass
class Project:
    """Personal or academic project."""
    name: str
    description: str
    technologies: List[str] = field(default_factory=list)
    link: str = ""


@dataclass
class Resume:
    """Complete resume data."""
    name: str = ""
    email: str = ""
    phone: str = ""
    linkedin: str = ""
    github: str = ""
    website: str = ""

    education: List[Education] = field(default_factory=list)
    experiences: List[Experience] = field(default_factory=list)
    projects: List[Project] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)


def initialize_data_dir():
    """Create data directory if it doesn't exist."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_resume() -> Resume:
    """Load resume data from file."""
    initialize_data_dir()

    if os.path.exists(RESUME_FILE):
        try:
            with open(RESUME_FILE, 'r') as f:
                data = json.load(f)

                # Convert lists back to dataclass objects
                resume = Resume(**{k: v for k, v in data.items() if k not in ['education', 'experiences', 'projects']})
                resume.education = [Education(**e) for e in data.get('education', [])]
                resume.experiences = [Experience(**e) for e in data.get('experiences', [])]
                resume.projects = [Project(**p) for p in data.get('projects', [])]

                return resume
        except Exception as e:
            st.error(f"Error loading resume: {e}")
            return Resume()

    return Resume()


def save_resume(resume: Resume):
    """Save resume data to file."""
    initialize_data_dir()

    try:
        # Convert to dict for JSON serialization
        data = {
            'name': resume.name,
            'email': resume.email,
            'phone': resume.phone,
            'linkedin': resume.linkedin,
            'github': resume.github,
            'website': resume.website,
            'education': [asdict(e) for e in resume.education],
            'experiences': [asdict(e) for e in resume.experiences],
            'projects': [asdict(p) for p in resume.projects],
            'skills': resume.skills
        }

        with open(RESUME_FILE, 'w') as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        st.error(f"Error saving resume: {e}")


def generate_text_resume(resume: Resume) -> str:
    """Generate a plain text version of the resume."""
    lines = []

    # Header
    lines.append(f"{resume.name.upper()}")
    lines.append("=" * len(resume.name))

    contact = []
    if resume.email:
        contact.append(resume.email)
    if resume.phone:
        contact.append(resume.phone)
    if resume.linkedin:
        contact.append(f"LinkedIn: {resume.linkedin}")
    if resume.github:
        contact.append(f"GitHub: {resume.github}")

    lines.append(" | ".join(contact))
    lines.append("")

    # Education
    if resume.education:
        lines.append("EDUCATION")
        lines.append("-" * 50)
        for edu in resume.education:
            lines.append(f"{edu.school}")
            degree_line = f"{edu.degree} in {edu.major}"
            if edu.minor:
                degree_line += f", Minor in {edu.minor}"
            lines.append(degree_line)
            if edu.gpa:
                lines.append(f"GPA: {edu.gpa}")
            lines.append(f"Expected Graduation: {edu.graduation}")
            if edu.relevant_coursework:
                lines.append(f"Relevant Coursework: {', '.join(edu.relevant_coursework)}")
            lines.append("")

    # Experience
    if resume.experiences:
        lines.append("EXPERIENCE")
        lines.append("-" * 50)
        for exp in resume.experiences:
            lines.append(f"{exp.position} | {exp.company}")
            end = "Present" if exp.current else exp.end_date
            lines.append(f"{exp.location} | {exp.start_date} - {end}")
            for bullet in exp.bullets:
                lines.append(f"  • {bullet}")
            lines.append("")

    # Projects
    if resume.projects:
        lines.append("PROJECTS")
        lines.append("-" * 50)
        for proj in resume.projects:
            proj_line = proj.name
            if proj.link:
                proj_line += f" ({proj.link})"
            lines.append(proj_line)
            lines.append(f"  {proj.description}")
            if proj.technologies:
                lines.append(f"  Technologies: {', '.join(proj.technologies)}")
            lines.append("")

    # Skills
    if resume.skills:
        lines.append("SKILLS")
        lines.append("-" * 50)
        lines.append(", ".join(resume.skills))
        lines.append("")

    return "\n".join(lines)


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Header
    st.title("📄 Resume & Cover Letter Builder")
    st.markdown("Build a professional resume step by step!")

    # Load resume data
    if 'resume' not in st.session_state:
        st.session_state.resume = load_resume()

    resume = st.session_state.resume

    # Sidebar - Quick actions
    with st.sidebar:
        st.header("💾 Quick Actions")

        if st.button("💾 Save Resume", use_container_width=True):
            save_resume(resume)
            st.success("Resume saved!")

        if st.button("🔄 Clear All Data", use_container_width=True):
            if st.session_state.get('confirm_clear', False):
                st.session_state.resume = Resume()
                if os.path.exists(RESUME_FILE):
                    os.remove(RESUME_FILE)
                st.success("Data cleared!")
                st.session_state.confirm_clear = False
                st.rerun()
            else:
                st.session_state.confirm_clear = True
                st.warning("Click again to confirm")

        st.divider()

        st.subheader("📊 Resume Stats")
        st.metric("Experiences", len(resume.experiences))
        st.metric("Projects", len(resume.projects))
        st.metric("Skills", len(resume.skills))

        st.divider()

        st.subheader("💡 Tips")
        st.markdown("""
        - Use **action verbs** to start bullets
        - **Quantify** achievements when possible
        - Keep bullets **concise** (1-2 lines)
        - **Tailor** for each job
        """)

    # Main tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "👤 Contact Info",
        "🎓 Education",
        "💼 Experience",
        "🚀 Projects",
        "🛠️ Skills",
        "📄 Preview"
    ])

    # TAB 1: Contact Information
    with tab1:
        st.header("Contact Information")

        col1, col2 = st.columns(2)

        with col1:
            resume.name = st.text_input("Full Name *", value=resume.name)
            resume.email = st.text_input("Email *", value=resume.email)
            resume.phone = st.text_input("Phone", value=resume.phone, placeholder="(123) 456-7890")

        with col2:
            resume.linkedin = st.text_input("LinkedIn URL", value=resume.linkedin, placeholder="linkedin.com/in/yourname")
            resume.github = st.text_input("GitHub URL", value=resume.github, placeholder="github.com/yourname")
            resume.website = st.text_input("Personal Website", value=resume.website, placeholder="yourwebsite.com")

        if st.button("💾 Save Contact Info"):
            save_resume(resume)
            st.success("Contact info saved!")

    # TAB 2: Education
    with tab2:
        st.header("Education")

        # Add new education
        with st.expander("➕ Add Education", expanded=len(resume.education) == 0):
            with st.form("add_education"):
                school = st.text_input("School/University *", placeholder="Princeton University")

                col1, col2 = st.columns(2)
                with col1:
                    degree = st.selectbox("Degree", ["B.A.", "B.S.E.", "B.S.", "M.A.", "M.S.", "Ph.D.", "Other"])
                    major = st.text_input("Major *", placeholder="Computer Science")

                with col2:
                    minor = st.text_input("Minor (optional)", placeholder="Mathematics")
                    gpa = st.text_input("GPA (optional)", placeholder="3.8/4.0")

                graduation = st.text_input("Expected Graduation *", placeholder="May 2025")

                coursework = st.text_input(
                    "Relevant Coursework (comma-separated)",
                    placeholder="Data Structures, Algorithms, Machine Learning"
                )

                if st.form_submit_button("Add Education"):
                    if school and degree and major and graduation:
                        new_edu = Education(
                            school=school,
                            degree=degree,
                            major=major,
                            minor=minor,
                            gpa=gpa,
                            graduation=graduation,
                            relevant_coursework=[c.strip() for c in coursework.split(",") if c.strip()]
                        )
                        resume.education.append(new_edu)
                        save_resume(resume)
                        st.success("Education added!")
                        st.rerun()
                    else:
                        st.error("Please fill in all required fields (*)")

        # Display existing education
        if resume.education:
            st.subheader("Your Education")
            for i, edu in enumerate(resume.education):
                with st.expander(f"{edu.school} - {edu.degree} in {edu.major}"):
                    st.write(f"**Degree:** {edu.degree} in {edu.major}")
                    if edu.minor:
                        st.write(f"**Minor:** {edu.minor}")
                    if edu.gpa:
                        st.write(f"**GPA:** {edu.gpa}")
                    st.write(f"**Graduation:** {edu.graduation}")
                    if edu.relevant_coursework:
                        st.write(f"**Coursework:** {', '.join(edu.relevant_coursework)}")

                    if st.button(f"🗑️ Remove", key=f"remove_edu_{i}"):
                        resume.education.pop(i)
                        save_resume(resume)
                        st.rerun()
        else:
            st.info("No education added yet. Click '➕ Add Education' above.")

    # TAB 3: Experience
    with tab3:
        st.header("Work Experience")

        # Add new experience
        with st.expander("➕ Add Experience", expanded=len(resume.experiences) == 0):
            with st.form("add_experience"):
                col1, col2 = st.columns(2)

                with col1:
                    company = st.text_input("Company *", placeholder="Google")
                    position = st.text_input("Position *", placeholder="Software Engineering Intern")

                with col2:
                    location = st.text_input("Location", placeholder="Mountain View, CA")
                    current = st.checkbox("Currently working here")

                col3, col4 = st.columns(2)
                with col3:
                    start_date = st.text_input("Start Date *", placeholder="June 2024")
                with col4:
                    end_date = st.text_input("End Date", placeholder="August 2024", disabled=current)

                st.subheader("Responsibilities & Achievements")
                st.caption("Add 3-5 bullet points describing your impact")

                bullets = []
                for i in range(5):
                    bullet = st.text_area(
                        f"Bullet Point {i+1}" + (" *" if i < 2 else " (optional)"),
                        placeholder=f"Start with an action verb: {ACTION_VERBS[i % len(ACTION_VERBS)]}...",
                        key=f"exp_bullet_{i}",
                        height=60
                    )
                    if bullet:
                        bullets.append(bullet)

                if st.form_submit_button("Add Experience"):
                    if company and position and start_date and (current or end_date) and len(bullets) >= 2:
                        new_exp = Experience(
                            company=company,
                            position=position,
                            location=location,
                            start_date=start_date,
                            end_date=end_date if not current else "",
                            current=current,
                            bullets=bullets
                        )
                        resume.experiences.append(new_exp)
                        save_resume(resume)
                        st.success("Experience added!")
                        st.rerun()
                    else:
                        st.error("Please fill in required fields and add at least 2 bullet points")

        # Display existing experiences
        if resume.experiences:
            st.subheader("Your Experience")
            for i, exp in enumerate(resume.experiences):
                end = "Present" if exp.current else exp.end_date
                with st.expander(f"{exp.position} at {exp.company} ({exp.start_date} - {end})"):
                    st.write(f"**Position:** {exp.position}")
                    st.write(f"**Company:** {exp.company}")
                    st.write(f"**Location:** {exp.location}")
                    st.write(f"**Duration:** {exp.start_date} - {end}")

                    st.write("**Responsibilities:**")
                    for bullet in exp.bullets:
                        st.write(f"• {bullet}")

                    if st.button(f"🗑️ Remove", key=f"remove_exp_{i}"):
                        resume.experiences.pop(i)
                        save_resume(resume)
                        st.rerun()
        else:
            st.info("No experience added yet. Click '➕ Add Experience' above.")

    # TAB 4: Projects
    with tab4:
        st.header("Projects")

        # Add new project
        with st.expander("➕ Add Project", expanded=len(resume.projects) == 0):
            with st.form("add_project"):
                proj_name = st.text_input("Project Name *", placeholder="Personal Portfolio Website")
                proj_desc = st.text_area(
                    "Description *",
                    placeholder="Brief description of what the project does and your role",
                    height=100
                )
                proj_tech = st.text_input(
                    "Technologies (comma-separated)",
                    placeholder="Python, React, PostgreSQL"
                )
                proj_link = st.text_input("Link (GitHub, demo, etc.)", placeholder="github.com/yourname/project")

                if st.form_submit_button("Add Project"):
                    if proj_name and proj_desc:
                        new_proj = Project(
                            name=proj_name,
                            description=proj_desc,
                            technologies=[t.strip() for t in proj_tech.split(",") if t.strip()],
                            link=proj_link
                        )
                        resume.projects.append(new_proj)
                        save_resume(resume)
                        st.success("Project added!")
                        st.rerun()
                    else:
                        st.error("Please fill in name and description")

        # Display existing projects
        if resume.projects:
            st.subheader("Your Projects")
            for i, proj in enumerate(resume.projects):
                with st.expander(f"{proj.name}"):
                    st.write(f"**Description:** {proj.description}")
                    if proj.technologies:
                        st.write(f"**Technologies:** {', '.join(proj.technologies)}")
                    if proj.link:
                        st.write(f"**Link:** {proj.link}")

                    if st.button(f"🗑️ Remove", key=f"remove_proj_{i}"):
                        resume.projects.pop(i)
                        save_resume(resume)
                        st.rerun()
        else:
            st.info("No projects added yet. Click '➕ Add Project' above.")

    # TAB 5: Skills
    with tab5:
        st.header("Skills")

        st.markdown("""
        List your technical and soft skills. Group them by category for better organization.

        **Examples:**
        - Programming Languages: Python, Java, JavaScript, C++
        - Tools & Technologies: Git, Docker, AWS, React
        - Languages: English (Native), Spanish (Fluent)
        """)

        skills_input = st.text_area(
            "Enter your skills (comma-separated)",
            value=", ".join(resume.skills) if resume.skills else "",
            height=150,
            placeholder="Python, Java, JavaScript, React, Node.js, Git, AWS"
        )

        if st.button("💾 Save Skills"):
            resume.skills = [s.strip() for s in skills_input.split(",") if s.strip()]
            save_resume(resume)
            st.success("Skills saved!")
            st.rerun()

        if resume.skills:
            st.subheader("Your Skills")
            # Display as pills
            cols = st.columns(4)
            for i, skill in enumerate(resume.skills):
                with cols[i % 4]:
                    st.button(skill, disabled=True, use_container_width=True)

    # TAB 6: Preview & Export
    with tab6:
        st.header("Resume Preview")

        if not resume.name or not resume.email:
            st.warning("⚠️ Please add your contact information first!")
        else:
            # Generate text preview
            text_resume = generate_text_resume(resume)

            # Display preview
            st.text(text_resume)

            # Export options
            st.divider()
            st.subheader("Export Options")

            col1, col2 = st.columns(2)

            with col1:
                st.download_button(
                    label="📥 Download as Text",
                    data=text_resume,
                    file_name=f"{resume.name.replace(' ', '_')}_Resume.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            with col2:
                st.info("💡 Copy the text and paste into Google Docs or Word to format further")

            st.divider()

            # Resume completeness check
            st.subheader("✅ Resume Checklist")

            checklist = {
                "Contact information (name, email)": bool(resume.name and resume.email),
                "Education": len(resume.education) > 0,
                "At least 1 experience or project": len(resume.experiences) + len(resume.projects) > 0,
                "Skills listed": len(resume.skills) > 0,
                "Action verbs in bullets": any("ed " in bullet.lower() or "ing " in bullet.lower()
                                              for exp in resume.experiences for bullet in exp.bullets),
            }

            for item, complete in checklist.items():
                if complete:
                    st.success(f"✅ {item}")
                else:
                    st.warning(f"⚠️ {item}")

            # Tips
            st.divider()
            st.subheader("💡 Next Steps")
            st.markdown("""
            1. **Tailor for each job**: Customize bullets to match job description
            2. **Quantify achievements**: Add numbers/percentages where possible
            3. **Proofread**: Check for typos and grammar
            4. **Get feedback**: Have someone review your resume
            5. **Format**: Create a polished version in Word/Google Docs
            6. **Try the advanced version**: Use `app_advanced.py` for AI-powered improvements!
            """)


if __name__ == "__main__":
    main()
