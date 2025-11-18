# 📚 Multi-Document Research Assistant

**Difficulty**: Advanced (8-12 hours to extend)
**Completion**: 60% (Core features working, advanced features ready to implement)

## 🎯 What You'll Build

An AI-powered research assistant that analyzes multiple academic papers simultaneously, extracts citations, finds connections between documents, and generates literature review sections.

**Perfect for**: Literature reviews, research projects, thesis work, comprehensive exams

## ✨ Core Features (Already Implemented)

- ✅ Upload and process multiple PDF documents
- ✅ Ask questions across all documents simultaneously
- ✅ Generate interactive concept maps showing relationships between papers
- ✅ Extract key citations with automatic formatting
- ✅ Create comparison tables between papers
- ✅ Use extended thinking for complex research questions
- ✅ Beautiful artifact-based visualizations

## 🚀 Advanced Features (TODO - You'll Build These!)

- [ ] **Smart Citation Extraction**: Automatically parse references section and build bibliography
- [ ] **Literature Review Generator**: AI generates full literature review sections
- [ ] **Contradiction Detector**: Find where papers disagree with each other
- [ ] **Methodology Comparison**: Compare research methodologies across papers
- [ ] **Timeline Visualization**: Show how research evolved chronologically
- [ ] **Export to LaTeX/Word**: Generate formatted literature review documents
- [ ] **Semantic Search**: Find similar papers based on concepts, not just keywords
- [ ] **Annotation System**: Highlight and save important passages

## 🧠 What You'll Learn

### AI Techniques
- **Multi-document reasoning**: How to handle multiple long documents in a single query
- **Extended thinking**: Using Claude's extended thinking for complex analysis
- **Artifacts**: Generating interactive HTML/SVG visualizations
- **RAG patterns**: Retrieval-augmented generation for long documents
- **Prompt engineering**: Structuring prompts for academic analysis

### Software Engineering
- PDF processing with PyPDF2
- Document chunking strategies
- Interactive data visualization
- State management for multi-document apps
- File upload handling in Streamlit

## 🛠️ Tech Stack

- **Claude API**: Sonnet 4.5 with extended thinking
- **Streamlit**: Web interface
- **PyPDF2**: PDF text extraction
- **Artifacts**: Interactive concept maps, citation lists, comparison tables

## 📦 Installation

```bash
# Navigate to this template
cd advanced/10-multi-doc-research

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# Run the app
streamlit run app.py
```

## 🎮 How to Use

### Basic Workflow

1. **Upload Documents**: Click "Upload PDFs" and select 2-5 research papers
2. **Ask Questions**: Try queries like:
   - "What are the main arguments across all these papers?"
   - "How do these authors define [concept]?"
   - "What methodologies do these papers use?"
3. **Generate Visualizations**: Click "Create Concept Map" to see relationships
4. **Extract Citations**: Get formatted citation list for your bibliography

### Example Queries

**Comparison Questions:**
- "Compare the methodologies used in these papers"
- "Which papers support theory X vs theory Y?"
- "What are the contradictions between these papers?"

**Synthesis Questions:**
- "What are the 3 main themes across all documents?"
- "How has this field evolved based on publication dates?"
- "What research gaps do these papers identify?"

**Practical Questions:**
- "Generate an outline for a literature review on this topic"
- "What are the most cited works across these papers?"
- "Summarize each paper in 2-3 sentences"

## 🏗️ Architecture

```
User uploads PDFs
    ↓
Extract text with PyPDF2
    ↓
Store in session state (simple in-memory storage)
    ↓
User asks question
    ↓
[EXTENDED THINKING ENABLED]
Claude analyzes all documents
    ↓
Generate response + artifacts (concept maps, tables, etc.)
    ↓
Display interactive visualizations
```

## 📝 Code Structure

```python
app.py
├── extract_text_from_pdf()      # PDF processing
├── create_concept_map()         # Generate artifact: SVG concept map
├── create_comparison_table()    # Generate artifact: HTML table
├── extract_citations()          # Parse and format citations
├── ask_question_across_docs()   # Main query function with extended thinking
└── main()                       # Streamlit UI
```

## 🎨 Artifacts You'll Create

### 1. Interactive Concept Map (SVG)
```
Papers are nodes, connections are edges
Click to highlight related papers
```

### 2. Comparison Table (HTML)
```
| Paper | Methodology | Main Finding | Limitations |
```

### 3. Citation List (Formatted HTML)
```
Formatted in APA/MLA/Chicago style
Clickable links to papers
```

### 4. Literature Review Outline (Markdown)
```
Generated section headers with paper references
```

## 🚧 TODOs for You to Implement

### TODO 1: Smart Citation Extraction (2-3 hours)
**File**: `app.py`, function `extract_citations_advanced()`

Currently, citations are manually formatted. Your job:
1. Parse the "References" section from each PDF
2. Use Claude to structure citations into standard format
3. Detect citation style (APA, MLA, Chicago)
4. Generate clickable bibliography

**Hints**:
- Look for "References" or "Bibliography" section in PDF
- Use regex to detect citation patterns
- Claude can help normalize citation formats

### TODO 2: Literature Review Generator (3-4 hours)
**File**: `app.py`, function `generate_lit_review()`

Create a full literature review section:
1. Identify main themes across papers
2. Group papers by theme
3. Generate narrative text with in-text citations
4. Create transitions between paragraphs
5. Export as artifact (formatted HTML or Markdown)

**Hints**:
- Use extended thinking for complex synthesis
- Structure prompt to request thematic organization
- Include direct quotes from papers with page numbers

### TODO 3: Contradiction Detector (2-3 hours)
**File**: `app.py`, function `find_contradictions()`

Find where papers disagree:
1. Analyze claims across all papers
2. Identify conflicting evidence or interpretations
3. Create visualization showing debate sides
4. Generate artifact: "Debate Map" showing opposing views

**Hints**:
- Prompt: "Identify contradictory claims or findings"
- Use extended thinking for nuanced analysis
- Create interactive artifact with collapsible sections

### TODO 4: Export to LaTeX/Word (1-2 hours)
**File**: `app.py`, function `export_to_latex()`

Export formatted literature review:
1. Convert generated review to LaTeX format
2. Include proper bibliography formatting
3. Add option to export as .docx (using python-docx)
4. Maintain formatting and citations

**Hints**:
- Use LaTeX templates for academic papers
- python-docx library for Word export
- Streamlit download button for file delivery

## 💡 Extension Ideas

Once you complete the core TODOs, try these advanced extensions:

1. **Semantic Search**: Use embeddings to find similar passages across papers
2. **Timeline View**: Show research evolution over time
3. **Author Network**: Visualize co-authorship and citation networks
4. **Methodology Extractor**: Auto-detect and compare research methods
5. **Gap Analysis**: Identify under-researched areas
6. **Relevance Scorer**: Rank papers by relevance to your research question
7. **Annotation System**: Highlight and save important quotes
8. **Multi-language Support**: Translate papers and query in different languages

## 🎯 Success Criteria

Your implementation is successful when:
- ✅ You can upload 5+ papers and query them simultaneously
- ✅ Citation extraction works for at least 2 citation styles
- ✅ Literature review generator creates coherent paragraphs with citations
- ✅ Contradictions are identified and visualized clearly
- ✅ Export to at least one format (LaTeX or Word) works perfectly
- ✅ Interactive artifacts load quickly and look professional

## 📚 Helpful Resources

- [Claude API Documentation](https://docs.anthropic.com/)
- [Extended Thinking Guide](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking)
- [Streamlit Artifacts](https://docs.streamlit.io/)
- [PyPDF2 Documentation](https://pypdf2.readthedocs.io/)
- [Academic Citation Formats](https://www.citationmachine.net/citation-guide)

## 🏆 Portfolio Tips

When showcasing this project:
1. **Demo video**: Show uploading 3-5 papers and asking complex questions
2. **Highlight artifacts**: Show off the interactive visualizations
3. **Explain RAG**: Discuss how you handle long documents
4. **Show edge cases**: How does it handle poorly formatted PDFs?
5. **Performance**: Mention optimization strategies for large documents

## 🐛 Common Issues

**Issue**: PDF text extraction fails
**Solution**: Some PDFs are images. Consider adding OCR with pytesseract.

**Issue**: Claude times out on large documents
**Solution**: Implement chunking strategy (break into 10k character chunks).

**Issue**: Citations aren't formatted correctly
**Solution**: Use few-shot examples in your prompt to show desired format.

**Issue**: Concept map is cluttered with many papers
**Solution**: Implement hierarchical clustering or limit edges to strongest connections.

## 🎉 Next Steps

After completing this template:
1. Share your project on GitHub with a great README
2. Write a blog post about multi-document RAG
3. Extend to handle other document types (Word, HTML, etc.)
4. Add collaboration features (share analyses with classmates)
5. Deploy to Streamlit Cloud and share with your class!

---

**Happy researching!** 🚀

If you get stuck, check the comments in `app.py` for detailed hints on each TODO.
