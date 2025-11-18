"""
Course Material Remix Engine
Advanced Template - 60% Complete

Transform boring course materials into engaging, personalized learning content.
Convert textbooks and lectures into stories, analogies, quizzes, and more!

COMPLETED FEATURES:
✅ Content upload and extraction
✅ Multiple transformation modes (story, analogy, ELI5)
✅ Interactive quiz generation (artifact)
✅ Concept map visualization (artifact)
✅ Practice problem generation

YOUR TODOs:
🚧 Podcast script generator
🚧 Flashcard deck builder with Anki export
🚧 Accessibility transformation modes
🚧 Multi-format export system
"""

import streamlit as st
import anthropic
import os
from dotenv import load_dotenv
import PyPDF2
from io import BytesIO
import json
import re

# Load environment variables
load_dotenv()

# Initialize Claude client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Configure Streamlit page
st.set_page_config(
    page_title="Course Material Remix",
    page_icon="📖",
    layout="wide"
)

# Initialize session state
if 'original_content' not in st.session_state:
    st.session_state.original_content = ""
if 'transformed_content' not in st.session_state:
    st.session_state.transformed_content = ""


def extract_content_from_pdf(pdf_file) -> str:
    """Extract text from uploaded PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file.read()))
        full_text = ""
        for page in pdf_reader.pages:
            full_text += page.extract_text() + "\n\n"
        return full_text
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return ""


def transform_to_story(content: str, topic: str) -> str:
    """
    Transform educational content into an engaging narrative story.

    Uses extended thinking to create a coherent, memorable story that
    teaches the same concepts in an entertaining way.
    """
    prompt = f"""Transform this educational content into an engaging story with characters and plot.

Topic: {topic}

Content to transform:
{content[:8000]}

Instructions:
1. Create relatable characters that represent key concepts
2. Use a narrative arc (setup, conflict, resolution)
3. Maintain educational accuracy - all facts must be correct
4. Make it memorable and fun to read
5. Include dialogue where appropriate
6. Target reading level: High school / College
7. Length: 500-800 words

Return the story in well-formatted HTML with:
- Proper paragraphs
- Character names in bold
- Key concepts highlighted
- Engaging formatting"""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=4000,
        thinking={
            "type": "enabled",
            "budget_tokens": 8000
        },
        messages=[{"role": "user", "content": prompt}]
    )

    for block in response.content:
        if block.type == "text":
            return block.text

    return "Could not generate story."


def transform_to_analogy(content: str, analogy_domain: str) -> str:
    """
    Transform content using a specific analogy domain (sports, cooking, music, etc.).

    Makes complex concepts relatable through familiar experiences.
    """
    prompt = f"""Explain this educational content using {analogy_domain} analogies.

Content:
{content[:8000]}

Instructions:
1. Find {analogy_domain}-related analogies for EACH major concept
2. Make analogies accurate and helpful, not forced
3. Use specific examples from {analogy_domain}
4. Maintain technical accuracy
5. Include comparisons table showing: Concept → {analogy_domain} Equivalent

Return formatted HTML with:
- Introduction explaining the analogy approach
- Detailed analogies for each concept
- Comparison table (HTML table)
- Key takeaways"""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=3000,
        thinking={
            "type": "enabled",
            "budget_tokens": 6000
        },
        messages=[{"role": "user", "content": prompt}]
    )

    for block in response.content:
        if block.type == "text":
            return block.text

    return "Could not generate analogy."


def transform_to_eli5(content: str) -> str:
    """
    Explain Like I'm 5 - simplify content to its essence.

    Uses simple language, concrete examples, and visual descriptions.
    """
    prompt = f"""Explain this content like I'm 5 years old (ELI5).

Content:
{content[:8000]}

Instructions:
1. Use simple, everyday language
2. Short sentences (max 15 words)
3. Concrete examples kids can understand
4. Avoid jargon - if you must use technical terms, define them simply
5. Use comparisons to everyday objects
6. Make it fun and engaging
7. Include emojis where helpful

Return formatted HTML with:
- Clear headings
- Short paragraphs
- Helpful emojis
- "Big word alert!" sections for necessary technical terms"""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2500,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


def create_concept_map_artifact(content: str, topic: str) -> str:
    """
    Generate an interactive concept map showing relationships between ideas.

    Returns HTML with SVG visualization.
    """
    prompt = f"""Analyze this educational content and create an interactive concept map.

Topic: {topic}
Content:
{content[:6000]}

Create an HTML artifact with an SVG concept map that:
1. Shows main concepts as nodes (circles or boxes)
2. Shows relationships as labeled edges
3. Uses hierarchical layout (main topic at top/center)
4. Color-codes by category/theme
5. Makes nodes interactive (hover to see definition)
6. Includes a legend
7. Uses clean, academic styling

Return ONLY the complete HTML code with embedded SVG and CSS."""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


def generate_quiz_artifact(content: str, topic: str, num_questions: int = 5) -> str:
    """
    Generate an interactive quiz with multiple choice questions.

    Returns HTML artifact with JavaScript for interactivity.
    """
    prompt = f"""Create an interactive multiple-choice quiz based on this content.

Topic: {topic}
Content:
{content[:8000]}

Generate {num_questions} multiple choice questions that:
1. Test understanding, not just memorization
2. Have 4 answer choices each
3. Include explanation for why each answer is correct/incorrect
4. Range from easy to challenging
5. Cover different aspects of the topic

Create an HTML artifact with:
- Question display with radio buttons
- "Submit Answer" button
- Instant feedback (green for correct, red for incorrect)
- Explanation after answering
- Score tracking
- "Next Question" button
- Final score at end
- Clean, modern UI with CSS styling
- JavaScript for interactivity

Return ONLY the complete HTML code."""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=5000,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


def generate_practice_problems(content: str, topic: str, difficulty: str = "medium") -> str:
    """
    Generate practice problems with solutions (hidden behind spoiler).

    Returns formatted HTML.
    """
    prompt = f"""Generate {difficulty} difficulty practice problems based on this content.

Topic: {topic}
Content:
{content[:8000]}

Create 3-5 practice problems that:
1. Test application of concepts, not just recall
2. Include clear problem statements
3. Provide step-by-step solutions (hidden in collapsible sections)
4. Explain the reasoning, not just the answer
5. Range in difficulty

Return formatted HTML with:
- Numbered problems
- Collapsible solution sections (click to reveal)
- Hints before solutions
- Clear formatting with CSS"""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=4000,
        thinking={
            "type": "enabled",
            "budget_tokens": 6000
        },
        messages=[{"role": "user", "content": prompt}]
    )

    for block in response.content:
        if block.type == "text":
            return block.text

    return "Could not generate practice problems."


# ============================================================================
# TODO SECTION FOR STUDENTS
# ============================================================================

def generate_podcast_script(content: str, topic: str):
    """
    TODO #1: Podcast Script Generator (2-3 hours)

    Transform course material into a conversational podcast script.

    Your task:
    1. Create dialogue between 2 hosts:
       - Host A (teacher): Explains concepts
       - Host B (student): Asks questions, provides student perspective

    2. Make it conversational and engaging:
       - Natural speech patterns
       - Humor where appropriate
       - Tangents that illustrate points
       - "Aha!" moments

    3. Add production notes:
       - [INTRO MUSIC - 0:00]
       - [PAUSE for effect]
       - [SOUND EFFECT: ...]
       - Timestamps every 2-3 minutes

    4. Structure:
       - Intro hook (30 seconds)
       - Main content (15-25 minutes)
       - Ad break spots (every 8-10 min)
       - Recap and outro (2 minutes)

    5. Generate artifact with:
       - Full script
       - Estimated runtime
       - Download as .txt button

    Example format:
    ```
    [INTRO MUSIC - 0:00-0:15]

    Host A: "Welcome back to Learning Made Easy! Today we're diving into
    photosynthesis, and trust me, it's way cooler than you remember from
    high school."

    Host B: "Oh man, I was SO confused about this. Where do we even start?"

    [Continue natural dialogue...]
    ```

    Hints:
    - Use extended thinking to understand content deeply
    - Make Host B ask real student questions
    - Keep segments under 3 minutes before switching topics
    - Include callback references to earlier points
    """
    # YOUR CODE HERE
    st.warning("🚧 TODO #1: Implement podcast script generator!")
    return "<p>Podcast script generation not yet implemented.</p>"


def generate_flashcard_deck(content: str, topic: str):
    """
    TODO #2: Flashcard Deck Builder (2-3 hours)

    Auto-generate high-quality flashcards from course material.

    Your task:
    1. Identify flashcard-worthy content:
       - Key definitions
       - Important formulas
       - Cause-effect relationships
       - Historical dates/events
       - Process steps

    2. Generate different card types:
       - Basic: Front/Back
       - Cloze: "The powerhouse of the cell is the {{c1::mitochondria}}"
       - Reverse: Can be answered both ways
       - Image: Describe diagram to label

    3. Apply learning science:
       - One concept per card
       - Avoid yes/no questions
       - Use clear, concise wording
       - Include mnemonic hints where helpful

    4. Create interactive artifact:
       - Flip animation (click to flip)
       - Keyboard navigation (space = flip, arrow = next)
       - Progress indicator
       - Shuffle option

    5. BONUS: Export to Anki format
       - Research genanki library
       - Create .apkg file
       - Include deck metadata
       - Add download button

    Example flashcard:
    {
        'front': 'What is the primary product of photosynthesis?',
        'back': 'Glucose (C6H12O6)',
        'hint': '💡 G for Glucose, G for Green plants',
        'tags': ['photosynthesis', 'biology'],
        'card_type': 'basic'
    }

    Hints:
    - Generate 15-25 cards per topic
    - Mix card types for variety
    - Use spaced repetition metadata
    - Make cards visually appealing with CSS
    """
    # YOUR CODE HERE
    st.warning("🚧 TODO #2: Implement flashcard deck builder!")
    return None


def transform_for_accessibility(content: str, mode: str):
    """
    TODO #3: Accessibility Transformation (2-3 hours)

    Adapt content for different learning needs.

    Your task:
    Implement 4 modes:

    1. ADHD-Friendly:
       - Break into bullet points
       - Add visual breaks (emojis, dividers)
       - Bold key terms
       - TL;DR summaries
       - 5-minute chunks
       - Interactive elements

    2. Dyslexia-Friendly:
       - Shorter sentences (<20 words)
       - Shorter paragraphs (3-4 sentences)
       - Define jargon inline
       - No italics
       - Increased line spacing
       - Dyslexia font (OpenDyslexic in CSS)

    3. ESL-Friendly:
       - Simple vocabulary
       - Define academic terms
       - Shorter sentences
       - Pronunciation guides [foh-toh-SIN-thuh-sis]
       - Visual aids
       - Translation of key terms

    4. Visual-Learner:
       - Heavy use of diagrams
       - Color-coded information
       - Flowcharts for processes
       - Minimal text
       - Infographic style
       - Concept maps

    Generate artifact with proper accessibility features.

    Hints:
    - Research WCAG guidelines
    - Use semantic HTML
    - Include proper ARIA labels
    - Test with screen reader in mind
    - Use Claude to simplify/adapt language
    """
    # YOUR CODE HERE
    st.warning(f"🚧 TODO #3: Implement {mode} accessibility mode!")
    return "<p>Accessibility transformations not yet implemented.</p>"


def export_content(content: str, format_type: str):
    """
    TODO #4: Multi-Format Export (1-2 hours)

    Export transformed content to various formats.

    Your task:
    Support 5 export formats:

    1. Markdown (.md)
       - For Notion, Obsidian, etc.
       - Convert HTML to Markdown
       - Preserve formatting (headings, lists, bold, italic)
       - Include frontmatter metadata

    2. HTML (.html)
       - Standalone file with CSS
       - Include all styling inline
       - Proper DOCTYPE and meta tags
       - Make it shareable

    3. PDF (.pdf)
       - Professional formatting
       - Use pdfkit or reportlab
       - Include table of contents
       - Proper page breaks

    4. Plain Text (.txt)
       - Simple text file
       - Remove HTML tags
       - Preserve basic structure
       - Include metadata header

    5. JSON (.json)
       - Structured data
       - Include metadata:
         {
           "title": "...",
           "topic": "...",
           "transformation_type": "...",
           "generated_date": "...",
           "content": "..."
         }

    Add Streamlit download buttons for each format.

    Hints:
    - Use python-markdown for MD → HTML
    - Use html2text for HTML → Markdown
    - For PDF, look into reportlab or weasyprint
    - Use st.download_button() for downloads
    - Include "Copy to Clipboard" button
    """
    # YOUR CODE HERE
    st.warning(f"🚧 TODO #4: Implement {format_type} export!")
    return None


# ============================================================================
# STREAMLIT UI
# ============================================================================

def main():
    # Header
    st.title("📖 Course Material Remix Engine")
    st.markdown("*Transform boring course materials into engaging, personalized learning content*")

    # Sidebar
    with st.sidebar:
        st.header("📄 Upload Content")

        input_method = st.radio(
            "How do you want to input content?",
            ["Paste Text", "Upload PDF"]
        )

        if input_method == "Paste Text":
            content_input = st.text_area(
                "Paste your course material:",
                placeholder="Paste lecture notes, textbook excerpt, or any educational content...",
                height=200
            )
            if st.button("📥 Load Content"):
                st.session_state.original_content = content_input
                st.success("✅ Content loaded!")

        else:  # Upload PDF
            uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])
            if uploaded_file:
                if st.button("📥 Extract Text from PDF"):
                    with st.spinner("Extracting text..."):
                        st.session_state.original_content = extract_content_from_pdf(uploaded_file)
                        st.success(f"✅ Extracted {len(st.session_state.original_content)} characters!")

        st.markdown("---")

        # Content preview
        if st.session_state.original_content:
            st.subheader("📝 Content Preview")
            preview = st.session_state.original_content[:300] + "..." if len(st.session_state.original_content) > 300 else st.session_state.original_content
            st.text_area("", preview, height=150, disabled=True)
            st.caption(f"Total length: {len(st.session_state.original_content)} characters")

    # Main content area
    if not st.session_state.original_content:
        # Welcome screen
        st.markdown("""
        ## 🎯 What is this?

        Transform dense textbooks and boring lectures into engaging content tailored to YOUR learning style.

        ### ✨ Transformation Modes

        - **📖 Story Mode**: Convert concepts into memorable narratives with characters
        - **🏀 Analogy Mode**: Explain using sports, cooking, music, or other familiar domains
        - **👶 ELI5 Mode**: Simplify to its essence (Explain Like I'm 5)
        - **🗺️ Visual Mode**: Create concept maps and diagrams
        - **🎯 Quiz Mode**: Generate interactive quizzes with instant feedback
        - **💪 Practice Mode**: Create practice problems with solutions

        ### 🚀 Advanced Features (TODOs)

        - **🎙️ Podcast Mode**: Conversational podcast scripts
        - **🎴 Flashcard Mode**: Spaced repetition decks (Anki export)
        - **♿ Accessibility**: ADHD, dyslexia, ESL-friendly versions
        - **📦 Export**: Download as PDF, Markdown, HTML, etc.

        ### 👈 Get Started

        1. Upload content using the sidebar (paste text or upload PDF)
        2. Choose a transformation mode below
        3. Interact with the generated content!
        """)

    else:
        # Topic input
        topic = st.text_input(
            "📌 What's the topic?",
            placeholder="e.g., Photosynthesis, Machine Learning, Ancient Rome",
            help="This helps the AI understand context for better transformations"
        )

        # Main transformation tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📖 Story Mode",
            "🎨 Analogy Mode",
            "👶 ELI5 Mode",
            "🗺️ Visual Mode",
            "🎯 Quiz Mode",
            "💪 Practice Mode"
        ])

        # TAB 1: Story Mode
        with tab1:
            st.header("Transform into a Story")
            st.markdown("*Convert educational content into an engaging narrative with characters and plot*")

            if st.button("📖 Generate Story", type="primary"):
                if topic:
                    with st.spinner("Creating your story..."):
                        story = transform_to_story(st.session_state.original_content, topic)
                        st.session_state.transformed_content = story

                        st.subheader("📚 Your Educational Story")
                        st.markdown(story, unsafe_allow_html=True)

                        # Export options
                        st.markdown("---")
                        st.info("💡 Want to save this? Complete TODO #4 to add export functionality!")
                else:
                    st.warning("Please enter a topic first!")

        # TAB 2: Analogy Mode
        with tab2:
            st.header("Explain Using Analogies")
            st.markdown("*Make complex concepts relatable through familiar experiences*")

            col1, col2 = st.columns([3, 1])
            with col1:
                analogy_domain = st.selectbox(
                    "Choose analogy domain:",
                    [
                        "Sports (Basketball, Football, Soccer)",
                        "Cooking and Recipes",
                        "Music and Instruments",
                        "Video Games",
                        "Movies and TV Shows",
                        "Building and Construction",
                        "Nature and Animals",
                        "Travel and Geography",
                        "Custom..."
                    ]
                )

                if analogy_domain == "Custom...":
                    analogy_domain = st.text_input("Enter your domain:", "gardening")

            with col2:
                st.markdown("### Why Analogies?")
                st.caption("Analogies help your brain connect new concepts to things you already understand!")

            if st.button("🎨 Generate Analogies", type="primary"):
                if topic:
                    with st.spinner(f"Creating {analogy_domain} analogies..."):
                        analogy_content = transform_to_analogy(st.session_state.original_content, analogy_domain)

                        st.subheader(f"🎯 {topic} Explained Through {analogy_domain}")
                        st.markdown(analogy_content, unsafe_allow_html=True)
                else:
                    st.warning("Please enter a topic first!")

        # TAB 3: ELI5 Mode
        with tab3:
            st.header("Explain Like I'm 5 (ELI5)")
            st.markdown("*Simplify complex concepts using simple language and concrete examples*")

            if st.button("👶 Make it Simple!", type="primary"):
                with st.spinner("Simplifying..."):
                    eli5_content = transform_to_eli5(st.session_state.original_content)

                    st.subheader("🌟 Simple Explanation")
                    st.markdown(eli5_content, unsafe_allow_html=True)

        # TAB 4: Visual Mode
        with tab4:
            st.header("Visual Concept Maps")
            st.markdown("*See relationships between concepts visually*")

            if st.button("🗺️ Generate Concept Map", type="primary"):
                if topic:
                    with st.spinner("Creating concept map..."):
                        concept_map = create_concept_map_artifact(st.session_state.original_content, topic)

                        st.subheader("🎨 Interactive Concept Map")
                        st.components.v1.html(concept_map, height=600, scrolling=True)
                else:
                    st.warning("Please enter a topic first!")

        # TAB 5: Quiz Mode
        with tab5:
            st.header("Interactive Quiz Generator")
            st.markdown("*Test your understanding with AI-generated questions*")

            num_questions = st.slider("Number of questions:", 3, 10, 5)

            if st.button("🎯 Generate Quiz", type="primary"):
                if topic:
                    with st.spinner("Generating quiz..."):
                        quiz = generate_quiz_artifact(st.session_state.original_content, topic, num_questions)

                        st.subheader("📝 Take the Quiz!")
                        st.components.v1.html(quiz, height=700, scrolling=True)
                else:
                    st.warning("Please enter a topic first!")

        # TAB 6: Practice Mode
        with tab6:
            st.header("Practice Problems")
            st.markdown("*Apply what you've learned with practice problems*")

            difficulty = st.select_slider(
                "Difficulty level:",
                options=["easy", "medium", "hard", "very hard"],
                value="medium"
            )

            if st.button("💪 Generate Practice Problems", type="primary"):
                if topic:
                    with st.spinner("Creating practice problems..."):
                        problems = generate_practice_problems(st.session_state.original_content, topic, difficulty)

                        st.subheader(f"📚 {difficulty.title()} Practice Problems")
                        st.markdown(problems, unsafe_allow_html=True)
                else:
                    st.warning("Please enter a topic first!")

        # Additional TODO features section
        st.markdown("---")
        st.header("🚧 Advanced Features (TODOs)")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🎙️ Podcast Mode")
            st.info("TODO #1: Generate conversational podcast scripts")
            if st.button("Generate Podcast Script"):
                st.warning("Complete TODO #1 in the code to unlock this feature!")

            st.subheader("♿ Accessibility Modes")
            st.info("TODO #3: Transform for different learning needs")
            access_mode = st.selectbox(
                "Accessibility mode:",
                ["ADHD-Friendly", "Dyslexia-Friendly", "ESL-Friendly", "Visual-Learner"]
            )
            if st.button("Transform for Accessibility"):
                st.warning("Complete TODO #3 in the code to unlock this feature!")

        with col2:
            st.subheader("🎴 Flashcard Deck")
            st.info("TODO #2: Generate spaced repetition flashcards")
            if st.button("Generate Flashcard Deck"):
                st.warning("Complete TODO #2 in the code to unlock this feature!")

            st.subheader("📦 Export Options")
            st.info("TODO #4: Export to multiple formats")
            export_format = st.selectbox(
                "Export format:",
                ["Markdown (.md)", "HTML (.html)", "PDF (.pdf)", "Plain Text (.txt)", "JSON (.json)"]
            )
            if st.button("Export Content"):
                st.warning("Complete TODO #4 in the code to unlock this feature!")


if __name__ == "__main__":
    main()
