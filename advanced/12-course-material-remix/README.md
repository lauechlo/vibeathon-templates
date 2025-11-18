# 📖 Course Material Remix Engine

**Difficulty**: Advanced (6-10 hours to extend)
**Completion**: 60% (Core features working, advanced features ready to implement)

## 🎯 What You'll Build

Transform boring lecture slides and dense textbooks into engaging, personalized learning materials. Convert content into stories, analogies, interactive quizzes, podcasts, flashcards, and more - all tailored to YOUR learning style.

**Perfect for**: Visual learners, auditory learners, students with ADHD, anyone who finds traditional materials boring

## ✨ Core Features (Already Implemented)

- ✅ Upload lecture slides (PDF, text) or textbook chapters
- ✅ Transform into multiple formats:
  - Story with characters
  - Real-world analogies (sports, cooking, etc.)
  - ELI5 (Explain Like I'm 5) versions
  - Concept maps and visual diagrams
- ✅ Generate interactive quizzes with explanations
- ✅ Create practice problems at different difficulty levels
- ✅ Beautiful artifacts for each transformation

## 🚀 Advanced Features (TODO - You'll Build These!)

- [ ] **Podcast Script Generator**: Convert to conversational podcast format with timestamps
- [ ] **Flashcard Deck Builder**: Auto-generate spaced repetition flashcards (Anki export)
- [ ] **Mnemonic Device Creator**: Generate memory tricks for key concepts
- [ ] **Study Guide Generator**: Comprehensive study guide with practice questions
- [ ] **Accessibility Modes**: ADHD-friendly, dyslexia-friendly, ESL-friendly versions
- [ ] **Multi-format Export**: Download as Markdown, HTML, PDF, Notion, etc.
- [ ] **Interactive Simulations**: Create interactive demos of concepts
- [ ] **Video Script Generator**: Create engaging video scripts with visual cues

## 🧠 What You'll Learn

### AI Techniques
- **Style transfer**: Converting content to different narrative styles
- **Pedagogical transformation**: Adapting content for different learning styles
- **Artifacts**: Creating rich, interactive HTML/SVG visualizations
- **Extended thinking**: Deep content analysis before transformation
- **Multi-modal prompting**: Generating different output formats

### Software Engineering
- PDF and text processing
- Content extraction and structuring
- Export to multiple file formats
- Interactive quiz generation
- Accessibility best practices

## 🛠️ Tech Stack

- **Claude API**: Sonnet 4.5 with extended thinking
- **Streamlit**: Web interface
- **PyPDF2**: PDF text extraction
- **Artifacts**: Interactive quizzes, diagrams, concept maps
- **python-markdown**: Export formatting

## 📦 Installation

```bash
# Navigate to this template
cd advanced/12-course-material-remix

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# Run the app
streamlit run app.py
```

## 🎮 How to Use

### Basic Workflow

1. **Upload Content**: Paste text or upload PDF (lecture slides, textbook chapter)
2. **Choose Transformation**: Pick your learning style (story, analogy, visual, etc.)
3. **Generate**: AI transforms the content
4. **Interact**: Use quizzes, practice problems, interactive diagrams
5. **Export**: Download in your preferred format

### Example Transformations

**Original (boring textbook):**
> "Photosynthesis is the process by which plants convert light energy into chemical energy stored in glucose."

**→ Story Mode:**
> "Meet Chloro the Chloroplast, a tiny green superhero living inside a plant leaf. Every morning when the sun rises, Chloro puts on his solar panel cape and gets to work..."

**→ Cooking Analogy:**
> "Think of photosynthesis like baking cookies. Your ingredients (water + CO2) get mixed together, then you need heat (sunlight) to bake them, and out comes your delicious product (glucose sugar)..."

**→ Rap Battle:**
> "Yo, I'm a plant, standing tall in the sun / Photosynthesis is how I get stuff done / Six CO2, six H2O in my mix / Light energy cooking it up with some physics tricks..."

## 🏗️ Architecture

```
User uploads content (PDF/text)
    ↓
Extract and structure content
    ↓
User selects transformation style
    ↓
[EXTENDED THINKING ENABLED]
Claude analyzes content and transforms
    ↓
Generate artifact (interactive HTML, quiz, diagram)
    ↓
Display with export options
```

## 📝 Code Structure

```python
app.py
├── extract_content()           # Extract text from uploads
├── transform_to_story()        # Convert to narrative story
├── transform_to_analogy()      # Create real-world analogies
├── create_concept_map()        # Visual concept map artifact
├── generate_quiz()             # Interactive quiz artifact
├── generate_practice_problems() # Create practice questions
├── create_mnemonic()           # Memory tricks (TODO)
├── export_to_format()          # Export to various formats (TODO)
└── main()                      # Streamlit UI
```

## 🎨 Artifacts You'll Create

### 1. Interactive Quiz (HTML)
```
Multiple choice questions with:
- Instant feedback
- Explanations for each answer
- Progress tracking
- Score at the end
```

### 2. Concept Map (SVG)
```
Visual diagram showing:
- Key concepts as nodes
- Relationships as edges
- Hierarchical structure
- Color-coded by topic
```

### 3. Flashcard Deck (HTML)
```
Flip cards with:
- Front: Question/term
- Back: Answer/definition
- Keyboard shortcuts
- Spaced repetition hints
```

### 4. Timeline Visualization (HTML/SVG)
```
For historical content:
- Events on timeline
- Clickable details
- Images/icons
- Connections between events
```

## 🚧 TODOs for You to Implement

### TODO 1: Podcast Script Generator (2-3 hours)
**File**: `app.py`, function `generate_podcast_script()`

Transform course material into a conversational podcast script.

**Your task:**
1. Convert dense academic content into natural dialogue
2. Format as conversation between 2 hosts:
   - Host A: Explains concepts
   - Host B: Asks clarifying questions (student perspective)
3. Add production notes:
   - [PAUSE]
   - [SOUND EFFECT: ...]
   - [MUSIC: upbeat transition]
4. Include timestamps for each segment
5. Add "ad break" spots for natural breaks (every 10 min)
6. Generate artifact with:
   - Formatted script
   - Estimated total runtime
   - Downloadable as .txt or .pdf

**Example output:**
```
[INTRO MUSIC - 0:00]

Host A: "Welcome back to 'Learning Made Easy'! Today we're tackling photosynthesis."

Host B: "Oh man, I remember being SO confused about this in high school. Where do we even start?"

Host A: "Great question! Let's start with what you already know. What happens when you leave a plant in a dark closet for a week?"

[Continue dialogue...]

[TIMESTAMP: 5:30 - Key Concept: Light-Dependent Reactions]
...
```

**Hints:**
- Use extended thinking to understand content deeply first
- Make Host B ask questions students actually have
- Keep language conversational, not academic
- Add humor where appropriate
- Include analogies in the dialogue

### TODO 2: Flashcard Deck Builder with Anki Export (2-3 hours)
**File**: `app.py`, function `generate_flashcard_deck()`

Auto-generate high-quality flashcards from course material.

**Your task:**
1. Extract key concepts, definitions, formulas, dates
2. Generate cards in multiple formats:
   - Basic: Front/Back
   - Cloze: Fill in the blank
   - Image: Label the diagram
   - Matching: Match terms to definitions
3. Apply learning science principles:
   - One concept per card
   - Avoid yes/no questions
   - Use clear, concise wording
   - Include mnemonic hints
4. Create interactive artifact showing all flashcards
5. **BONUS**: Export to Anki format (.apkg file)
   - Research Anki deck structure
   - Use python libraries to generate .apkg
   - Include deck metadata

**Example flashcard:**
```
Front: "What is the primary product of photosynthesis?"
Back: "Glucose (C6H12O6)

💡 Mnemonic: G for Glucose, G for Green plants"

Tags: #photosynthesis #biology #cellular-processes
Difficulty: Easy
```

**Hints:**
- Use Claude to identify "flashcard-worthy" content
- Generate 15-25 cards per topic
- Include visual cards (describe image, generate SVG)
- For Anki export, look up genanki Python library

### TODO 3: Accessibility Transformation Modes (2-3 hours)
**File**: `app.py`, function `transform_for_accessibility()`

Adapt content for students with different learning needs.

**Your task:**
Implement 4 accessibility modes:

1. **ADHD-Friendly Mode:**
   - Break long paragraphs into bullet points
   - Add visual breaks (emojis, icons)
   - Highlight key terms in bold/color
   - Include "TL;DR" summaries
   - Chunk content into 5-minute segments
   - Add interactive elements to maintain engagement

2. **Dyslexia-Friendly Mode:**
   - Simplify complex sentences
   - Use shorter paragraphs
   - Increase line spacing in artifact
   - Use dyslexia-friendly fonts (OpenDyslexic)
   - Avoid italics
   - Define jargon inline

3. **ESL (English as Second Language) Mode:**
   - Simplify vocabulary
   - Define academic terms
   - Use shorter sentences
   - Add pronunciation guides for difficult words
   - Include visual aids
   - Translate key terms to common languages

4. **Visual Learner Mode:**
   - Heavy use of diagrams and concept maps
   - Color-coded information
   - Flowcharts for processes
   - Minimal text, maximum visuals
   - Infographic-style summaries

**Generate artifacts** with proper styling for each mode.

**Hints:**
- Research accessibility best practices
- Use CSS in artifacts to implement visual accommodations
- Ask Claude to "adapt for [specific need]"
- Test with longer content to see difference
- Include toggle to switch between modes

### TODO 4: Multi-Format Export System (1-2 hours)
**File**: `app.py`, function `export_content()`

Export transformed content to various formats.

**Your task:**
1. Support export to:
   - **Markdown**: For Notion, Obsidian, etc.
   - **HTML**: Standalone file with CSS
   - **PDF**: Professional formatting
   - **Plain Text**: Simple text file
   - **JSON**: Structured data for other apps

2. Preserve formatting:
   - Headings, lists, emphasis
   - Images (embedded or linked)
   - Code blocks
   - Math equations (LaTeX)

3. Add Streamlit download buttons for each format

4. Include metadata in exports:
   - Original source
   - Transformation type
   - Generation date
   - AI model used

**Hints:**
- Use python-markdown for Markdown → HTML
- Use pdfkit or reportlab for PDF generation
- For Notion, research their import format
- Include a "Copy to Clipboard" button too

## 💡 Extension Ideas

1. **Voice Mode Integration**: Generate audio of the podcast script
2. **Collaborative Study**: Share transformations with classmates
3. **Custom Analogies**: User provides their interests (e.g., "I love basketball") → all analogies use basketball
4. **Quiz Competition**: Multiplayer quiz games
5. **Progress Dashboard**: Track which topics you've mastered
6. **AI Tutor Chat**: Ask follow-up questions about the material
7. **Video Script Generator**: Create scripts for educational YouTube videos
8. **Meme Generator**: Create educational memes for each concept (fun!)

## 🎯 Success Criteria

Your implementation is successful when:
- ✅ Content transforms maintain educational accuracy
- ✅ Transformations are engaging and memorable
- ✅ Accessibility modes genuinely help different learners
- ✅ Exports work across multiple formats without errors
- ✅ Artifacts are interactive and visually appealing
- ✅ Students actually enjoy using it!

## 📚 Helpful Resources

- [Claude API Documentation](https://docs.anthropic.com/)
- [Accessibility Guidelines (WCAG)](https://www.w3.org/WAI/WCAG21/quickref/)
- [Anki Deck Format](https://github.com/kerrickstaley/genanki)
- [Learning Science Principles](https://www.learningscientists.org/)
- [Markdown Syntax](https://www.markdownguide.org/)

## 🏆 Portfolio Tips

When showcasing this project:
1. **Demo multiple transformations**: Show how same content looks in different styles
2. **Highlight accessibility**: Emphasize inclusive design
3. **Show export variety**: Demonstrate format flexibility
4. **User testimonials**: Get feedback from different types of learners
5. **Before/After**: Show original boring content → transformed engaging version

## 🐛 Common Issues

**Issue**: Transformations lose important technical details
**Solution**: Add validation step to check all key concepts are preserved

**Issue**: Analogies don't make sense for complex topics
**Solution**: Use extended thinking to find appropriate analogy domains

**Issue**: PDF export looks ugly
**Solution**: Use proper CSS templates and test with different content types

**Issue**: Artifacts don't work on mobile
**Solution**: Use responsive CSS (media queries) in artifact HTML

## 🎉 Next Steps

After completing this template:
1. Create a library of pre-made transformations for popular textbooks
2. Add social features (share favorite transformations)
3. Build a Chrome extension to transform web pages
4. Create a mobile app version
5. Partner with educators to test in real classrooms!

---

**Happy remixing!** 🎨

Remember: Different brains learn differently. Let's make education accessible to everyone!
