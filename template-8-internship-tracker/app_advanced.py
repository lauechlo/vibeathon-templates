"""
Internship Application Tracker - Advanced Version
AI-powered application insights and email generation!
"""

import streamlit as st
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="AI Internship Tracker", page_icon="🤖", layout="wide")


@st.cache_resource
def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("⚠️ ANTHROPIC_API_KEY not found!")
        st.stop()
    return Anthropic(api_key=api_key)


def generate_follow_up_email(company, position, context, client):
    """Generate a follow-up email for an application."""
    prompt = f"""Write a professional follow-up email for this internship application:

Company: {company}
Position: {position}
Context: {context}

The email should:
- Be polite and professional
- Express continued interest
- Ask about application status
- Be concise (3-4 sentences)
- Have an appropriate subject line

Format:
Subject: [subject line]

[Email body]"""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text.strip()
    except Exception as e:
        return f"Error: {e}"


def analyze_job_description(jd, client):
    """Analyze a job description and extract key requirements."""
    prompt = f"""Analyze this job description and provide:

1. **Key Skills Required** (list top 5)
2. **Nice-to-Have Skills** (list 3)
3. **Application Tips** (3 specific suggestions)

Job Description:
{jd}

Be specific and actionable."""

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
        st.title("🤖 AI Internship Tracker")
        st.markdown("Smart application management with AI assistance!")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("✨ **AI Enhanced**")

    tab1, tab2 = st.tabs(["📧 Follow-Up Email", "🔍 Job Analysis"])

    with tab1:
        st.header("Generate Follow-Up Email")

        company = st.text_input("Company", placeholder="Google")
        position = st.text_input("Position", placeholder="Software Engineering Intern")
        context = st.text_area(
            "Context",
            placeholder="e.g., 'Applied 2 weeks ago, haven't heard back. Had a great phone screen last week.'",
            height=100
        )

        if st.button("📧 Generate Email", type="primary", disabled=not (company and position)):
            with st.spinner("Writing email..."):
                email = generate_follow_up_email(company, position, context, client)

                st.divider()
                st.subheader("📧 Your Follow-Up Email")
                st.text_area("", value=email, height=250, label_visibility="collapsed")

                st.download_button(
                    "📥 Download Email",
                    data=email,
                    file_name=f"follow_up_{company.replace(' ', '_')}.txt",
                    mime="text/plain"
                )

    with tab2:
        st.header("Analyze Job Description")

        jd = st.text_area(
            "Paste job description:",
            placeholder="Paste the full job posting here...",
            height=300
        )

        if st.button("🔍 Analyze", type="primary", disabled=not jd):
            with st.spinner("Analyzing job requirements..."):
                analysis = analyze_job_description(jd, client)

                st.divider()
                st.markdown(analysis)

    st.divider()
    st.markdown("""
    <div style='text-align: center; color: gray;'>
    <p>🤖 Powered by Claude AI | Use with <code>app.py</code> for full tracking features</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
