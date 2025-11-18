"""
Precept Prep Assistant - Advanced Version
AI-powered reading analysis with Claude!
"""

import streamlit as st
import json
import os
from datetime import datetime
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Precept Prep", page_icon="🤖", layout="wide")

DATA_DIR = "data"
READINGS_FILE = os.path.join(DATA_DIR, "readings.json")


@st.cache_resource
def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("⚠️ ANTHROPIC_API_KEY not found!")
        st.stop()
    return Anthropic(api_key=api_key)


def init_data():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def save_reading(data):
    init_data()
    readings = []
    if os.path.exists(READINGS_FILE):
        with open(READINGS_FILE, 'r') as f:
            readings = json.load(f)
    readings.append(data)
    with open(READINGS_FILE, 'w') as f:
        json.dump(readings, f, indent=2)


def load_readings():
    init_data()
    if os.path.exists(READINGS_FILE):
        with open(READINGS_FILE, 'r') as f:
            return json.load(f)
    return []


def analyze_reading(text, client):
    """Use Claude to analyze a reading comprehensively."""

    prompt = f"""Analyze this academic reading for precept discussion. Provide:

1. **Summary** (2-3 sentences): Main points
2. **Key Concepts** (3-5 terms): Important ideas or terminology
3. **Main Argument**: The central thesis or claim
4. **Discussion Questions** (5 questions): Thought-provoking questions for seminar discussion

Reading text:
{text[:4000]}  # Limit to avoid token limits

Format your response clearly with headers."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )

        return message.content[0].text.strip()

    except Exception as e:
        return f"Error analyzing reading: {e}"


def generate_argument_analysis(text, client):
    """Generate analysis of arguments presented in the text."""

    prompt = f"""Analyze the argumentation in this text:

{text[:4000]}

Provide:
1. **Main Argument**: Core thesis
2. **Supporting Evidence**: Key pieces of evidence or reasoning
3. **Potential Objections**: Counterarguments or weaknesses
4. **Rebuttals**: How the author might respond to objections

Keep it concise and structured."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        return message.content[0].text.strip()

    except Exception as e:
        return f"Error: {e}"


def compare_readings(reading1_text, reading2_text, client):
    """Compare two readings and identify connections."""

    prompt = f"""Compare these two readings. Identify:

1. **Common Themes**: Shared ideas or topics
2. **Contrasting Views**: How they disagree
3. **Connections**: How they relate to each other
4. **Discussion Question**: A question that ties both readings together

Reading 1:
{reading1_text[:2000]}

Reading 2:
{reading2_text[:2000]}

Be specific and analytical."""

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
        st.title("🤖 AI Precept Prep Assistant")
        st.markdown("Ace your precepts with AI-powered reading analysis!")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("✨ **AI Enhanced**")

    tab1, tab2, tab3 = st.tabs(["📖 Analyze Reading", "🔄 Compare Readings", "💾 Saved"])

    with tab1:
        st.subheader("Upload or Paste Your Reading")

        course = st.text_input("Course", placeholder="e.g., PHI 201")
        title = st.text_input("Reading Title", placeholder="e.g., Kant's Categorical Imperative")

        reading_text = st.text_area(
            "Paste reading text:",
            height=200,
            placeholder="Paste the text you need to analyze..."
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✨ Full Analysis", type="primary", disabled=not reading_text):
                if reading_text:
                    with st.spinner("🤖 Analyzing reading with AI..."):
                        analysis = analyze_reading(reading_text, client)

                        st.divider()
                        st.markdown(analysis)

                        st.divider()

                        # Save option
                        if st.button("💾 Save Analysis"):
                            reading_data = {
                                'title': title or "Untitled",
                                'course': course or "General",
                                'text': reading_text,
                                'analysis': analysis,
                                'timestamp': datetime.now().isoformat()
                            }
                            save_reading(reading_data)
                            st.success("Saved!")

        with col2:
            if st.button("⚖️ Argument Analysis", disabled=not reading_text):
                if reading_text:
                    with st.spinner("Analyzing arguments..."):
                        arg_analysis = generate_argument_analysis(reading_text, client)

                        st.divider()
                        st.markdown("### Argument Analysis")
                        st.markdown(arg_analysis)

    with tab2:
        st.subheader("Compare Two Readings")
        st.markdown("Identify connections and contrasts between readings")

        saved_readings = load_readings()

        if len(saved_readings) >= 2:
            reading_titles = [f"{r['title']} ({r['course']})" for r in saved_readings]

            reading1_idx = st.selectbox("First Reading", range(len(saved_readings)), format_func=lambda x: reading_titles[x])
            reading2_idx = st.selectbox("Second Reading", range(len(saved_readings)), format_func=lambda x: reading_titles[x])

            if reading1_idx != reading2_idx:
                if st.button("🔄 Compare Readings", type="primary"):
                    with st.spinner("Comparing readings..."):
                        comparison = compare_readings(
                            saved_readings[reading1_idx]['text'],
                            saved_readings[reading2_idx]['text'],
                            client
                        )

                        st.divider()
                        st.markdown("### Comparative Analysis")
                        st.markdown(comparison)
            else:
                st.warning("Please select two different readings")
        else:
            st.info("Save at least 2 readings to use comparison feature")

            # Quick paste comparison
            st.divider()
            st.subheader("Or Paste Two Readings Directly")

            col1, col2 = st.columns(2)

            with col1:
                text1 = st.text_area("Reading 1", height=150)

            with col2:
                text2 = st.text_area("Reading 2", height=150)

            if text1 and text2:
                if st.button("Compare"):
                    with st.spinner("Comparing..."):
                        comparison = compare_readings(text1, text2, client)
                        st.markdown(comparison)

    with tab3:
        st.subheader("Saved Readings & Analyses")

        readings = load_readings()

        if readings:
            for reading in reversed(readings):
                with st.expander(f"📖 {reading['title']} - {reading['course']}"):
                    st.caption(f"Saved: {datetime.fromisoformat(reading['timestamp']).strftime('%Y-%m-%d %H:%M')}")

                    if 'analysis' in reading:
                        st.markdown("### AI Analysis")
                        st.markdown(reading['analysis'])

                    st.divider()
                    st.markdown("### Original Text")
                    st.write(reading['text'][:500] + "..." if len(reading['text']) > 500 else reading['text'])
        else:
            st.info("No saved readings. Analyze a reading and save it!")


if __name__ == "__main__":
    main()
