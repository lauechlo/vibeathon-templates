"""
Resume & Cover Letter Builder - Advanced Version
AI-powered resume and cover letter generation with Claude!

Features:
- Transform experience descriptions into professional bullet points
- Generate tailored resume bullets from job descriptions
- Create customized cover letters
- ATS keyword analysis
- Resume critique and suggestions
"""

import streamlit as st
import json
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Resume Builder", page_icon="🤖", layout="wide")

DATA_DIR = "data"
RESUME_FILE = os.path.join(DATA_DIR, "resume_data.json")


@st.cache_resource
def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("⚠️ ANTHROPIC_API_KEY not found!")
        st.stop()
    return Anthropic(api_key=api_key)


def improve_bullet_point(bullet: str, client) -> str:
    """Use AI to improve a resume bullet point."""
    prompt = f"""Improve this resume bullet point to be more impactful:

"{bullet}"

Make it:
- Start with a strong action verb
- Include quantifiable achievements (if possible, estimate based on context)
- Be concise (1-2 lines)
- Use professional language
- Focus on impact and results

Return ONLY the improved bullet point, no explanation."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text.strip()
    except Exception as e:
        return f"Error: {e}"


def generate_tailored_bullets(experience: str, job_description: str, client) -> list:
    """Generate resume bullets tailored to a specific job."""
    prompt = f"""Based on this experience and job description, create 3-5 impactful resume bullet points.

My experience:
{experience}

Job description:
{job_description}

Create bullet points that:
- Highlight skills/experiences relevant to the job
- Use keywords from the job description naturally
- Start with strong action verbs
- Include quantifiable achievements
- Are concise and impactful

Return ONLY the bullet points, one per line, starting with •"""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        response = message.content[0].text.strip()
        bullets = [line.strip().lstrip("•").strip() for line in response.split("\n") if line.strip()]
        return bullets
    except Exception as e:
        return [f"Error: {e}"]


def generate_cover_letter(resume_summary: str, job_description: str, company: str, position: str, client) -> str:
    """Generate a personalized cover letter."""
    prompt = f"""Write a professional cover letter for this job application.

Applicant background:
{resume_summary}

Company: {company}
Position: {position}

Job description:
{job_description}

Create a compelling cover letter that:
- Is 3-4 paragraphs
- Shows enthusiasm for the specific role
- Connects applicant's experience to job requirements
- Demonstrates knowledge of the company
- Includes a strong closing

Use a professional but warm tone. Format with proper spacing."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text.strip()
    except Exception as e:
        return f"Error generating cover letter: {e}"


def analyze_ats_keywords(resume_text: str, job_description: str, client) -> dict:
    """Analyze resume against job description for ATS optimization."""
    prompt = f"""Analyze this resume against the job description for ATS (Applicant Tracking System) optimization.

Resume:
{resume_text}

Job Description:
{job_description}

Provide:
1. **Matching Keywords**: Important keywords found in both
2. **Missing Keywords**: Critical keywords from the job description not in the resume
3. **Optimization Tips**: 3 specific suggestions to improve ATS score

Format as clear sections."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text.strip()
    except Exception as e:
        return f"Error: {e}"


def critique_resume(resume_text: str, client) -> str:
    """Get AI feedback on resume."""
    prompt = f"""Review this resume and provide constructive feedback.

Resume:
{resume_text}

Provide:
1. **Strengths**: What's working well (2-3 points)
2. **Areas for Improvement**: Specific suggestions (3-4 points)
3. **Quick Wins**: Easy changes that would have big impact (2-3 points)

Be specific, constructive, and actionable."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text.strip()
    except Exception as e:
        return f"Error: {e}"


def main():
    client = get_client()

    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("🤖 AI Resume & Cover Letter Builder")
        st.markdown("Transform your experiences with AI-powered suggestions!")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("✨ **AI Powered**")

    with st.sidebar:
        st.header("🚀 AI Tools")
        st.markdown("""
        **Available AI Features:**
        - ✨ Improve bullet points
        - 🎯 Generate tailored bullets
        - 📝 Create cover letters
        - 🔍 ATS keyword analysis
        - 💡 Resume critique
        """)

        st.divider()
        st.info("💡 For a complete resume builder, use `app.py` then come back here for AI enhancements!")

    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "✨ Improve Bullets",
        "🎯 Tailor to Job",
        "📝 Cover Letter",
        "🔍 ATS Analysis"
    ])

    # TAB 1: Improve Bullet Points
    with tab1:
        st.header("✨ AI Bullet Point Enhancer")
        st.markdown("Transform basic descriptions into impactful achievement statements!")

        st.subheader("Examples")
        with st.expander("See before & after examples"):
            st.markdown("""
            **Before:** Helped customers at the store
            **After:** Delivered exceptional customer service to 50+ daily customers, achieving 95% satisfaction rating

            **Before:** Made a website for my club
            **After:** Designed and deployed responsive web application for 200+ member organization, reducing administrative workload by 40%

            **Before:** Did research with professor
            **After:** Collaborated on machine learning research project, co-authoring paper presented at regional AI conference
            """)

        user_bullet = st.text_area(
            "Enter your bullet point:",
            placeholder="e.g., 'Worked on a team project to build a mobile app'",
            height=100
        )

        if st.button("✨ Enhance with AI", type="primary", disabled=not user_bullet):
            with st.spinner("🤖 Improving your bullet point..."):
                improved = improve_bullet_point(user_bullet, client)

                st.divider()
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Before")
                    st.info(user_bullet)

                with col2:
                    st.subheader("After")
                    st.success(improved)

                st.caption("💡 Tip: You can further customize this to match your specific achievements!")

    # TAB 2: Tailor to Job
    with tab2:
        st.header("🎯 Generate Job-Tailored Bullets")
        st.markdown("Get resume bullets customized for a specific job posting!")

        experience_desc = st.text_area(
            "Describe your experience:",
            placeholder="e.g., 'I was a software engineering intern at a startup where I worked on the backend API using Python and Django. I fixed bugs, added new features, and helped with deployment.'",
            height=150
        )

        job_desc = st.text_area(
            "Paste the job description:",
            placeholder="Paste the full job posting here...",
            height=200
        )

        if st.button("🎯 Generate Tailored Bullets", type="primary", disabled=not (experience_desc and job_desc)):
            with st.spinner("🤖 Analyzing job description and crafting bullets..."):
                bullets = generate_tailored_bullets(experience_desc, job_desc, client)

                st.divider()
                st.subheader("✨ Tailored Resume Bullets")

                for i, bullet in enumerate(bullets, 1):
                    st.markdown(f"**{i}.** {bullet}")

                st.divider()
                st.success("💡 These bullets highlight skills relevant to the job description!")

    # TAB 3: Cover Letter Generator
    with tab3:
        st.header("📝 AI Cover Letter Generator")
        st.markdown("Create a personalized cover letter in seconds!")

        col1, col2 = st.columns(2)

        with col1:
            company_name = st.text_input("Company Name", placeholder="Google")
            position_name = st.text_input("Position", placeholder="Software Engineering Intern")

        with col2:
            st.caption("Optional but recommended:")
            hiring_manager = st.text_input("Hiring Manager (if known)", placeholder="Jane Smith")

        resume_summary = st.text_area(
            "Brief summary of your background:",
            placeholder="e.g., 'Junior at Princeton studying Computer Science. Experience with Python, Java, web development. Previous intern at tech startup. President of coding club.'",
            height=100
        )

        job_description = st.text_area(
            "Paste job description:",
            placeholder="Paste the full job posting...",
            height=200
        )

        if st.button("📝 Generate Cover Letter", type="primary",
                    disabled=not (company_name and position_name and resume_summary and job_description)):
            with st.spinner("🤖 Writing your cover letter..."):
                cover_letter = generate_cover_letter(resume_summary, job_description,
                                                     company_name, position_name, client)

                st.divider()
                st.subheader("📝 Your Cover Letter")

                # Display the cover letter
                st.text_area("", value=cover_letter, height=400, label_visibility="collapsed")

                # Download button
                st.download_button(
                    label="📥 Download Cover Letter",
                    data=cover_letter,
                    file_name=f"Cover_Letter_{company_name.replace(' ', '_')}.txt",
                    mime="text/plain"
                )

                st.divider()
                st.info("💡 **Pro tip**: Customize the opening and closing paragraphs to add your personal touch!")

    # TAB 4: ATS Analysis
    with tab4:
        st.header("🔍 ATS Keyword Analysis")
        st.markdown("Optimize your resume to pass Applicant Tracking Systems!")

        st.info("""
        **What is ATS?**
        Applicant Tracking Systems scan resumes for keywords before a human sees them.
        This tool helps you identify missing keywords to improve your chances!
        """)

        resume_text = st.text_area(
            "Paste your current resume:",
            placeholder="Paste your entire resume here...",
            height=250
        )

        job_posting = st.text_area(
            "Paste the job description:",
            placeholder="Paste the job posting...",
            height=250
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔍 Analyze Keywords", type="primary",
                        disabled=not (resume_text and job_posting)):
                with st.spinner("🤖 Analyzing for ATS optimization..."):
                    analysis = analyze_ats_keywords(resume_text, job_posting, client)

                    st.divider()
                    st.markdown(analysis)

        with col2:
            if st.button("💡 Get Resume Critique", disabled=not resume_text):
                with st.spinner("🤖 Reviewing your resume..."):
                    critique = critique_resume(resume_text, client)

                    st.divider()
                    st.subheader("💡 Resume Feedback")
                    st.markdown(critique)

    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: gray;'>
    <p>🤖 Powered by Claude AI | Built with ❤️ for job seekers</p>
    <p>💡 Tip: Use these AI tools to enhance the resume you built in <code>app.py</code></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
