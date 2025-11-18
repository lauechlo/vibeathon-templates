"""
Multi-Document Research Assistant
Advanced Template - 60% Complete

This app helps students analyze multiple research papers simultaneously,
extract citations, find connections, and generate literature reviews.

COMPLETED FEATURES:
✅ PDF upload and text extraction
✅ Multi-document querying with extended thinking
✅ Interactive concept map generation (artifact)
✅ Comparison table generation (artifact)
✅ Basic citation extraction

YOUR TODOs:
🚧 Advanced citation parsing from References section
🚧 Literature review generator
🚧 Contradiction detector
🚧 Export to LaTeX/Word
"""

import streamlit as st
import anthropic
import os
from dotenv import load_dotenv
import PyPDF2
from io import BytesIO
import json

# Load environment variables
load_dotenv()

# Initialize Claude client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Configure Streamlit page
st.set_page_config(
    page_title="Multi-Doc Research Assistant",
    page_icon="📚",
    layout="wide"
)

# Initialize session state for storing documents
if 'documents' not in st.session_state:
    st.session_state.documents = []


def extract_text_from_pdf(pdf_file) -> dict:
    """
    Extract text content from uploaded PDF file.

    Args:
        pdf_file: Streamlit UploadedFile object

    Returns:
        dict with 'title', 'text', and 'pages' keys
    """
    try:
        # Read PDF using PyPDF2
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file.read()))

        # Extract text from all pages
        full_text = ""
        for page_num, page in enumerate(pdf_reader.pages):
            full_text += f"\n--- Page {page_num + 1} ---\n"
            full_text += page.extract_text()

        return {
            'title': pdf_file.name,
            'text': full_text,
            'pages': len(pdf_reader.pages)
        }
    except Exception as e:
        st.error(f"Error processing {pdf_file.name}: {str(e)}")
        return None


def create_concept_map_artifact(papers_info: list) -> str:
    """
    Generate an interactive SVG concept map showing relationships between papers.
    This uses Claude's artifact feature to create a visual representation.

    Args:
        papers_info: List of dicts with paper titles and key concepts

    Returns:
        HTML string containing the SVG concept map
    """
    # Create a prompt for Claude to generate the concept map
    prompt = f"""Create an interactive SVG concept map showing the relationships between these research papers.

Papers:
{json.dumps(papers_info, indent=2)}

Generate an HTML artifact with an SVG that:
1. Shows each paper as a colored circle node
2. Connects papers with similar themes/concepts using lines
3. Labels connections with the shared concept
4. Makes it interactive (hover to highlight connections)
5. Uses a clean, academic color scheme
6. Includes a legend

Return ONLY the complete HTML code with embedded SVG and CSS."""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


def create_comparison_table_artifact(papers_data: list) -> str:
    """
    Generate an HTML comparison table artifact showing key aspects of each paper.

    Args:
        papers_data: List of dicts with paper information

    Returns:
        HTML string containing styled comparison table
    """
    prompt = f"""Create an interactive HTML comparison table for these research papers:

{json.dumps(papers_data, indent=2)}

Generate an HTML artifact with:
1. A professional table comparing: Title, Authors, Year, Methodology, Main Findings, Limitations
2. Color-coded rows (alternating for readability)
3. Sortable columns (use JavaScript)
4. Hover effects for better UX
5. Responsive design
6. Academic styling (clean, professional)

Return ONLY the complete HTML code with embedded CSS and JavaScript."""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


def extract_citations_basic(document_text: str, paper_title: str) -> list:
    """
    Basic citation extraction - extracts key information from paper.

    TODO FOR STUDENTS: Enhance this to parse the References section
    and extract formatted citations automatically.

    Args:
        document_text: Full text of the paper
        paper_title: Title of the paper

    Returns:
        List of citation strings
    """
    prompt = f"""From this academic paper, extract:
1. The main authors (if identifiable)
2. The publication year (if identifiable)
3. The journal/conference name (if identifiable)
4. Generate a basic citation in APA format

Paper title: {paper_title}

Paper excerpt (first 3000 chars):
{document_text[:3000]}

Return a JSON object with: authors, year, venue, citation"""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


def ask_question_across_docs(question: str, documents: list, use_extended_thinking: bool = True) -> dict:
    """
    Ask a question across multiple documents using Claude with extended thinking.

    This is the core function that enables multi-document reasoning.

    Args:
        question: User's research question
        documents: List of document dicts with 'title' and 'text'
        use_extended_thinking: Whether to enable extended thinking (default True)

    Returns:
        dict with 'answer' and 'thinking' (if extended thinking used)
    """
    # Construct context from all documents
    context = "# RESEARCH DOCUMENTS\n\n"
    for idx, doc in enumerate(documents, 1):
        context += f"## Document {idx}: {doc['title']}\n\n"
        # Include first 15000 chars of each document to stay within context limits
        context += doc['text'][:15000]
        context += "\n\n---\n\n"

    # Create the prompt
    prompt = f"""{context}

# USER QUESTION
{question}

# INSTRUCTIONS
Analyze all the documents above and provide a comprehensive answer to the user's question.
Your answer should:
1. Synthesize information across ALL documents
2. Note agreements and disagreements between papers
3. Cite specific papers when making claims (use "According to [Paper Title]...")
4. Identify patterns or themes across papers
5. Be academically rigorous

If you're uncertain about something, say so. Quality over speculation."""

    # Call Claude with extended thinking if requested
    if use_extended_thinking:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=16000,
            thinking={
                "type": "enabled",
                "budget_tokens": 10000
            },
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract thinking and response
        thinking_content = ""
        answer_content = ""

        for block in response.content:
            if block.type == "thinking":
                thinking_content = block.thinking
            elif block.type == "text":
                answer_content = block.text

        return {
            'answer': answer_content,
            'thinking': thinking_content,
            'model': 'claude-sonnet-4-5 (extended thinking)'
        }
    else:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            'answer': response.content[0].text,
            'thinking': None,
            'model': 'claude-sonnet-4-5'
        }


# ============================================================================
# TODO SECTION FOR STUDENTS
# ============================================================================

def extract_citations_advanced(document_text: str, paper_title: str):
    """
    TODO #1: Advanced Citation Extraction (2-3 hours)

    Your task: Parse the "References" or "Bibliography" section from the paper
    and extract all citations automatically.

    Steps:
    1. Find the References section (usually at the end)
       - Hint: Look for headers like "References", "Bibliography", "Works Cited"
       - Use regex or string searching

    2. Split into individual citations
       - Hint: Citations usually start with numbers [1] or author names

    3. Use Claude to parse each citation into structured format:
       - Authors, Year, Title, Venue, DOI/URL

    4. Detect citation style (APA, MLA, Chicago)
       - Hint: Ask Claude to identify the style from examples

    5. Return a list of structured citations

    Example return format:
    [
        {
            'authors': 'Smith, J., & Doe, J.',
            'year': '2020',
            'title': 'Machine Learning for Education',
            'venue': 'Journal of AI Research',
            'style': 'APA'
        },
        ...
    ]
    """
    # YOUR CODE HERE
    st.warning("🚧 TODO #1: Implement advanced citation extraction!")
    return []


def generate_lit_review(documents: list, topic: str):
    """
    TODO #2: Literature Review Generator (3-4 hours)

    Your task: Generate a full literature review section with proper citations.

    Steps:
    1. Identify main themes across all papers
       - Hint: Use extended thinking for complex thematic analysis
       - Ask Claude: "What are the 3-5 main themes across these papers?"

    2. Group papers by theme
       - Create a dict mapping themes to relevant papers

    3. For each theme, generate a paragraph that:
       - Introduces the theme
       - Discusses what different papers say about it
       - Uses in-text citations: "(Smith et al., 2020)"
       - Notes agreements/disagreements
       - Includes direct quotes with page numbers (if available)

    4. Add transitions between paragraphs

    5. Generate as an HTML artifact with:
       - Formatted paragraphs
       - Clickable citations
       - Section headers
       - Bibliography at the end

    6. Return the HTML artifact

    Example structure:
    # Introduction
    [Overview paragraph]

    # Theme 1: Machine Learning in Education
    [Paragraph discussing papers related to this theme]
    According to Smith et al. (2020), ...
    In contrast, Doe and Lee (2021) found that...

    # Theme 2: ...
    """
    # YOUR CODE HERE
    st.warning("🚧 TODO #2: Implement literature review generator!")
    return "<p>Literature review generation not yet implemented.</p>"


def find_contradictions(documents: list):
    """
    TODO #3: Contradiction Detector (2-3 hours)

    Your task: Find and visualize contradictions or disagreements between papers.

    Steps:
    1. Use extended thinking to analyze all papers for contradictory claims
       - Prompt: "Identify claims where these papers disagree or contradict each other"

    2. Extract contradictions with:
       - The claim being disputed
       - Which papers support position A
       - Which papers support position B
       - Quotes from each side

    3. Create a "Debate Map" artifact showing:
       - Central question/claim
       - Papers on "Side A" (with their argument)
       - Papers on "Side B" (with their argument)
       - Visual representation (use HTML/CSS or SVG)

    4. Return interactive HTML artifact

    Example output structure:
    {
        'contradictions': [
            {
                'claim': 'Machine learning improves student outcomes',
                'support': [
                    {'paper': 'Smith 2020', 'quote': '...', 'evidence': '...'}
                ],
                'oppose': [
                    {'paper': 'Doe 2021', 'quote': '...', 'evidence': '...'}
                ]
            }
        ],
        'artifact_html': '<div>...</div>'
    }
    """
    # YOUR CODE HERE
    st.warning("🚧 TODO #3: Implement contradiction detector!")
    return None


def export_to_latex(lit_review_content: str, citations: list):
    """
    TODO #4: Export to LaTeX (1-2 hours)

    Your task: Export the generated literature review to LaTeX format.

    Steps:
    1. Create a LaTeX template for academic papers
       - Use article class
       - Include packages: cite, hyperref, etc.

    2. Convert the lit review HTML/text to LaTeX format:
       - Replace HTML tags with LaTeX commands
       - Format citations as \cite{key}

    3. Generate bibliography section using:
       - \bibitem for each citation
       - Or use BibTeX format

    4. Return LaTeX string

    5. Add Streamlit download button:
       st.download_button(
           label="Download LaTeX",
           data=latex_content,
           file_name="literature_review.tex",
           mime="text/plain"
       )

    Bonus: Also implement export to Word (.docx) using python-docx library
    """
    # YOUR CODE HERE
    st.warning("🚧 TODO #4: Implement LaTeX export!")
    return None


# ============================================================================
# STREAMLIT UI
# ============================================================================

def main():
    # Header
    st.title("📚 Multi-Document Research Assistant")
    st.markdown("*Analyze multiple research papers simultaneously with AI*")

    # Sidebar for document management
    with st.sidebar:
        st.header("📄 Document Library")

        # File uploader
        uploaded_files = st.file_uploader(
            "Upload PDF Research Papers",
            type=['pdf'],
            accept_multiple_files=True,
            help="Upload 2-5 research papers to analyze together"
        )

        # Process uploaded files
        if uploaded_files:
            if st.button("📥 Process PDFs"):
                with st.spinner("Extracting text from PDFs..."):
                    st.session_state.documents = []
                    for pdf_file in uploaded_files:
                        doc_data = extract_text_from_pdf(pdf_file)
                        if doc_data:
                            st.session_state.documents.append(doc_data)
                    st.success(f"✅ Processed {len(st.session_state.documents)} documents!")

        # Show loaded documents
        if st.session_state.documents:
            st.subheader("📚 Loaded Documents")
            for idx, doc in enumerate(st.session_state.documents, 1):
                st.write(f"{idx}. **{doc['title']}** ({doc['pages']} pages)")
        else:
            st.info("👆 Upload PDFs to get started!")

    # Main content area
    if not st.session_state.documents:
        # Welcome screen
        st.markdown("""
        ## 🎯 What is this?

        A powerful research assistant that helps you analyze multiple academic papers at once.

        ### ✨ Features

        - **Multi-Document Querying**: Ask questions across all your papers
        - **Extended Thinking**: Claude deeply analyzes your research
        - **Interactive Visualizations**: Concept maps, comparison tables, and more
        - **Citation Extraction**: Automatically extract and format citations
        - **Literature Review Generation**: AI-powered lit review sections

        ### 🚀 Get Started

        1. Upload 2-5 PDF research papers using the sidebar
        2. Click "Process PDFs" to extract text
        3. Start asking questions or generate visualizations!

        ### 💡 Example Questions

        - "What are the main themes across these papers?"
        - "Compare the methodologies used in these studies"
        - "What contradictions exist between these papers?"
        - "Summarize each paper in 3 bullet points"
        - "What research gaps do these papers identify?"
        """)

    else:
        # Tabs for different features
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔍 Ask Questions",
            "🗺️ Concept Map",
            "📊 Comparison Table",
            "📝 Literature Review"
        ])

        # TAB 1: Ask Questions
        with tab1:
            st.header("Ask Questions Across All Documents")

            # Extended thinking toggle
            use_extended = st.checkbox(
                "🧠 Enable Extended Thinking",
                value=True,
                help="Claude will think deeply about your question before answering. Takes longer but gives better results."
            )

            # Question input
            question = st.text_area(
                "Your research question:",
                placeholder="e.g., What are the main methodological approaches across these papers?",
                height=100
            )

            if st.button("🔍 Analyze", type="primary"):
                if question:
                    with st.spinner("🧠 Analyzing documents with extended thinking..." if use_extended else "🤔 Analyzing documents..."):
                        result = ask_question_across_docs(
                            question,
                            st.session_state.documents,
                            use_extended_thinking=use_extended
                        )

                        # Show thinking process if extended thinking was used
                        if result['thinking']:
                            with st.expander("🧠 See Claude's Thinking Process", expanded=False):
                                st.markdown(f"*Model: {result['model']}*")
                                st.text(result['thinking'])

                        # Show answer
                        st.subheader("📝 Answer")
                        st.markdown(result['answer'])
                else:
                    st.warning("Please enter a question!")

            # Example questions
            with st.expander("💡 Example Questions"):
                st.markdown("""
                **Synthesis Questions:**
                - What are the 3 main themes across all documents?
                - How do these papers define [key concept]?
                - What theoretical frameworks are used?

                **Comparison Questions:**
                - Compare the methodologies used in these papers
                - Which papers support theory X vs theory Y?
                - What are the contradictions between these papers?

                **Practical Questions:**
                - What research gaps do these papers identify?
                - Generate an outline for a literature review on this topic
                - What are the most important takeaways for my research?
                """)

        # TAB 2: Concept Map
        with tab2:
            st.header("Interactive Concept Map")
            st.markdown("*Visualize relationships between your research papers*")

            if st.button("🗺️ Generate Concept Map"):
                with st.spinner("Creating concept map..."):
                    # Prepare paper info for concept map
                    papers_info = []
                    for doc in st.session_state.documents:
                        # Extract key concepts using Claude
                        prompt = f"""From this paper excerpt, extract 3-5 key concepts/themes:

{doc['text'][:5000]}

Return ONLY a JSON array of strings: ["concept1", "concept2", ...]"""

                        response = client.messages.create(
                            model="claude-sonnet-4-5-20250929",
                            max_tokens=500,
                            messages=[{"role": "user", "content": prompt}]
                        )

                        # Parse concepts (simple extraction)
                        concepts_text = response.content[0].text
                        try:
                            import re
                            concepts = eval(re.search(r'\[.*\]', concepts_text, re.DOTALL).group())
                        except:
                            concepts = ["machine learning", "education", "research"]

                        papers_info.append({
                            'title': doc['title'],
                            'concepts': concepts
                        })

                    # Generate concept map artifact
                    concept_map_html = create_concept_map_artifact(papers_info)

                    # Display the artifact
                    st.components.v1.html(concept_map_html, height=600, scrolling=True)

        # TAB 3: Comparison Table
        with tab3:
            st.header("Paper Comparison Table")
            st.markdown("*Compare key aspects of all papers side-by-side*")

            if st.button("📊 Generate Comparison Table"):
                with st.spinner("Analyzing papers for comparison..."):
                    # Extract comparison data for each paper
                    papers_data = []

                    for doc in st.session_state.documents:
                        prompt = f"""Analyze this paper excerpt and extract:
1. Authors (if identifiable)
2. Publication year (if identifiable)
3. Methodology (quantitative, qualitative, mixed, theoretical, etc.)
4. Main finding (1-2 sentences)
5. Key limitation (1 sentence)

Paper: {doc['title']}
Excerpt:
{doc['text'][:5000]}

Return ONLY a JSON object with keys: authors, year, methodology, main_finding, limitation"""

                        response = client.messages.create(
                            model="claude-sonnet-4-5-20250929",
                            max_tokens=1000,
                            messages=[{"role": "user", "content": prompt}]
                        )

                        # Parse response
                        try:
                            import re
                            json_text = re.search(r'\{.*\}', response.content[0].text, re.DOTALL).group()
                            paper_data = json.loads(json_text)
                            paper_data['title'] = doc['title']
                            papers_data.append(paper_data)
                        except:
                            papers_data.append({
                                'title': doc['title'],
                                'authors': 'Unknown',
                                'year': 'Unknown',
                                'methodology': 'Unknown',
                                'main_finding': 'Could not extract',
                                'limitation': 'Could not extract'
                            })

                    # Generate comparison table artifact
                    table_html = create_comparison_table_artifact(papers_data)

                    # Display the artifact
                    st.components.v1.html(table_html, height=500, scrolling=True)

        # TAB 4: Literature Review (TODO for students)
        with tab4:
            st.header("Literature Review Generator")
            st.markdown("*AI-generated literature review sections with citations*")

            st.info("🚧 **TODO for Students**: Implement the literature review generator!")

            topic = st.text_input(
                "Research topic:",
                placeholder="e.g., Machine learning in education"
            )

            if st.button("📝 Generate Literature Review"):
                st.warning("This feature is not yet implemented. Check the TODO section in the code!")
                # TODO: Uncomment when implemented
                # lit_review_html = generate_lit_review(st.session_state.documents, topic)
                # st.components.v1.html(lit_review_html, height=800, scrolling=True)

            st.markdown("---")
            st.subheader("📚 Extract Citations")

            if st.button("📋 Extract All Citations"):
                with st.spinner("Extracting citations..."):
                    citations = []
                    for doc in st.session_state.documents:
                        citation_info = extract_citations_basic(doc['text'], doc['title'])
                        citations.append(citation_info)

                    st.subheader("Citations (Basic)")
                    for citation in citations:
                        st.markdown(f"- {citation}")

                    st.info("💡 Want better citation extraction? Complete TODO #1!")


if __name__ == "__main__":
    main()
