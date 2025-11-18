# 🎓 Vibe Coding Starter Templates

**Ready-to-use templates for building AI-powered student projects with Claude**

These templates are designed to get you coding in 5 minutes or less. Each template solves a real student problem and comes in beginner and advanced versions.

## 🚀 Quick Start

1. **Choose a template** from the list below
2. **Copy the template folder** to your own directory
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Add your API key**: Create a `.env` file with `ANTHROPIC_API_KEY=your_key_here`
5. **Run the app**: `streamlit run app.py` (or `python app.py` for non-Streamlit templates)

## 📚 Available Templates

### 1. Princeton Late Meal Tracker 🍕
**Difficulty**: Beginner-friendly
**What it does**: Track late meal purchases, calculate if you're over the limit, and get weekly spending summaries.

**Tech Stack**: Python + Streamlit + Claude API
**Great for**: First-time AI app builders, Princeton students

**Features**:
- ✅ Pre-built Princeton late meal menu
- ✅ Automatic price calculation
- ✅ Weekly spending "wrapped" summary
- 🚀 Advanced: Receipt photo analysis, budget recommendations, trend analysis

[**Get Started →**](./template-1-late-meal/)

---

### 2. Course & Assignment Manager 📝
**Difficulty**: Beginner-friendly
**What it does**: Track assignments, get smart deadline reminders, and receive AI-powered study tips.

**Tech Stack**: Python + Streamlit + Claude API
**Great for**: All students, anyone learning web development

**Features**:
- ✅ Add and track assignments
- ✅ Deadline reminders
- ✅ AI study suggestions
- 🚀 Advanced: Google Calendar integration, email notifications, syllabus PDF parsing

[**Get Started →**](./template-2-assignment-manager/)

---

### 3. Princeton Event Finder 🎉
**Difficulty**: Beginner to Intermediate
**What it does**: Discover campus events with natural language search ("Find me free food events tonight").

**Tech Stack**: Python + Streamlit + Claude API
**Great for**: Students interested in web scraping and NLP

**Features**:
- ✅ Browse curated event listings
- ✅ Natural language search
- ✅ Filter by date, type, location
- 🚀 Advanced: Web scraping, email digests, calendar integration

[**Get Started →**](./template-3-event-finder/)

---

### 4. Study Group Matcher 🤝
**Difficulty**: Intermediate
**What it does**: Match students for study groups based on courses, learning style, and availability.

**Tech Stack**: Python + Claude API + Simple Database
**Great for**: Students interested in recommendation systems and social apps

**Features**:
- ✅ Create student profiles
- ✅ Find study partners
- ✅ AI-powered matching
- 🚀 Advanced: Smart scheduling, location-based matching, effectiveness tracking

[**Get Started →**](./template-4-study-matcher/)

---

### 5. Precept Prep Assistant 📖
**Difficulty**: Beginner-friendly
**What it does**: Upload readings and get AI-generated discussion questions, summaries, and key concepts.

**Tech Stack**: Python + Claude API
**Great for**: Humanities students, anyone wanting to explore AI for learning

**Features**:
- ✅ Paste text → get discussion questions
- ✅ Auto-generate summaries
- ✅ Extract key terms
- 🚀 Advanced: PDF upload, argument analysis, connection to previous readings

[**Get Started →**](./template-5-precept-prep/)

---

### 6. Resume & Cover Letter Builder 📄
**Difficulty**: Beginner-friendly
**What it does**: Create professional resumes and cover letters with AI-powered bullet point generation.

**Tech Stack**: Python + Streamlit + Claude API
**Great for**: Students applying for internships/jobs

**Features**:
- ✅ Form-based resume builder
- ✅ Export to text/PDF
- ✅ Pre-built templates
- 🚀 Advanced: AI bullet point enhancement, job-tailored resumes, cover letter generation, ATS optimization

[**Get Started →**](./template-6-resume-builder/)

---

### 7. Flashcard Generator 🎴
**Difficulty**: Beginner-friendly
**What it does**: Auto-generate flashcards from notes with spaced repetition learning.

**Tech Stack**: Python + Streamlit + Claude API
**Great for**: Students who want effective study tools

**Features**:
- ✅ Manual flashcard creation
- ✅ Spaced repetition (SM-2 algorithm)
- ✅ Progress tracking
- 🚀 Advanced: AI-generated flashcards from notes, multiple choice questions, Anki export

[**Get Started →**](./template-7-flashcard-generator/)

---

### 8. Internship Application Tracker 💼
**Difficulty**: Beginner to Intermediate
**What it does**: Track internship applications, deadlines, and interview stages in one place.

**Tech Stack**: Python + Streamlit + Claude API
**Great for**: Students applying to internships

**Features**:
- ✅ Application pipeline tracking
- ✅ Deadline reminders
- ✅ Status management
- 🚀 Advanced: AI follow-up email generation, job description analysis, application strategy insights

[**Get Started →**](./template-8-internship-tracker/)

---

### 9. Roommate Expense Splitter 💰
**Difficulty**: Beginner-friendly
**What it does**: Track shared expenses with roommates and calculate who owes what.

**Tech Stack**: Python + Streamlit + Claude Vision API
**Great for**: Students living with roommates

**Features**:
- ✅ Expense tracking
- ✅ Flexible splitting (equal/custom)
- ✅ Balance calculations
- ✅ Smart settlement algorithm
- 🚀 Advanced: Receipt photo scanning with Claude Vision, natural language expense entry

[**Get Started →**](./template-9-expense-splitter/)

---

## 🚀 Advanced Templates (8-12 hours)

Ready to level up? These advanced templates showcase cutting-edge AI patterns and build impressive portfolio pieces. They're ~60% complete - you'll implement the most interesting features yourself!

⚠️ **Prerequisites**: Comfort with Python, basic understanding of AI concepts, and completion of at least 2-3 beginner templates recommended.

### 10. Multi-Document Research Assistant 📚
**Difficulty**: Advanced (8-12 hours)
**What it does**: Analyze multiple research papers simultaneously, extract citations, find contradictions, and generate literature reviews.

**Tech Stack**: Python + Streamlit + Claude API (Extended Thinking) + PyPDF2 + Artifacts
**Great for**: Research projects, thesis work, comprehensive exams

**Features**:
- ✅ Multi-document querying with extended thinking
- ✅ Interactive concept maps (SVG artifacts)
- ✅ Comparison tables between papers
- ✅ Basic citation extraction
- 🚧 **YOU BUILD**: Advanced citation parsing, literature review generator, contradiction detector, LaTeX export

**What you'll learn**: RAG patterns, extended thinking, multi-document reasoning, artifact generation, academic writing AI

[**Get Started →**](./advanced/10-multi-doc-research/)

---

### 11. Code Learning Companion 💻
**Difficulty**: Advanced (6-10 hours)
**What it does**: AI tutor that uses Socratic teaching methods to help you learn programming without giving away answers.

**Tech Stack**: Python + Streamlit + Claude API (Extended Thinking) + Python AST
**Great for**: CS students, coding bootcamps, self-learners

**Features**:
- ✅ Code analysis and bug detection
- ✅ Socratic questioning (asks guiding questions, not answers)
- ✅ Practice problem generator
- ✅ Concept visualizations
- 🚧 **YOU BUILD**: Adaptive difficulty system, test case generator, algorithm visualizer, concept mastery tracker

**What you'll learn**: Educational AI patterns, Socratic method, code parsing (AST), adaptive learning systems, algorithm visualization

[**Get Started →**](./advanced/11-code-learning-companion/)

---

### 12. Course Material Remix Engine 📖
**Difficulty**: Advanced (6-10 hours)
**What it does**: Transform boring textbooks and lectures into engaging content tailored to YOUR learning style.

**Tech Stack**: Python + Streamlit + Claude API + Artifacts + PDF Processing
**Great for**: Visual learners, students with ADHD, anyone who finds traditional materials boring

**Features**:
- ✅ Transform to story mode (concepts as narrative)
- ✅ Analogy mode (sports, cooking, music analogies)
- ✅ ELI5 mode (simplify complex concepts)
- ✅ Interactive quizzes and concept maps
- 🚧 **YOU BUILD**: Podcast script generator, flashcard deck with Anki export, accessibility modes, multi-format export

**What you'll learn**: Style transfer, pedagogical transformation, accessibility design, multi-format content generation, educational artifacts

[**Get Started →**](./advanced/12-course-material-remix/)

---

### 13. Interactive Lecture Companion 🎓
**Difficulty**: Advanced (8-12 hours)
**What it does**: Real-time AI assistant that enhances your notes, generates questions, and keeps you engaged during lectures.

**Tech Stack**: Python + Streamlit + Claude API (Extended Thinking + Streaming) + Artifacts
**Great for**: Large lectures, difficult courses, students who struggle with attention

**Features**:
- ✅ Real-time note enhancement (type rough → get clean notes)
- ✅ Auto-generate check-for-understanding questions
- ✅ Post-lecture summary with gap analysis
- ✅ Interactive timeline visualization
- 🚧 **YOU BUILD**: Confusion detection, multi-lecture context linking, attention tracker, collaborative notes merging

**What you'll learn**: Real-time AI processing, streaming responses, long context management, temporal reasoning, engagement tracking

[**Get Started →**](./advanced/13-lecture-companion/)

---

## 🎯 Why Advanced Templates?

These advanced templates are designed to:

1. **Teach Cutting-Edge AI Patterns**
   - Extended thinking for complex analysis
   - Artifacts for rich, interactive outputs
   - Streaming for real-time responses
   - RAG (Retrieval Augmented Generation) for long documents

2. **Build Portfolio-Worthy Projects**
   - Impressive technical depth
   - Solves real, complex problems
   - Demonstrates advanced AI/ML knowledge
   - Great talking points for interviews

3. **Learn by Building**
   - ~60% starter code provided
   - You implement the most interesting features
   - Clear TODOs with hints
   - Comprehensive README guides

4. **Progressive Difficulty**
   - Start with working core features
   - Build increasingly complex extensions
   - Multiple difficulty levels within each template

## 💡 How to Use Advanced Templates

1. **Complete Prerequisites**: Finish 2-3 beginner templates first
2. **Read the README Carefully**: Each has detailed learning objectives
3. **Run the Base Version**: See what's already working
4. **Choose a TODO**: Pick one feature to implement
5. **Use the Hints**: Each TODO has implementation guidance
6. **Test Thoroughly**: Make sure your features work well
7. **Extend Further**: Add your own creative features!

---

## 🔑 Getting Your Claude API Key

1. Go to [console.anthropic.com](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to "API Keys"
4. Click "Create Key"
5. Copy your key and add it to your `.env` file

**Never commit your `.env` file to git!** All templates include `.env` in `.gitignore`.

## 💡 Template Philosophy

- **Copy-paste friendly**: Get running in 5 minutes
- **Well-commented**: Every line explains what it does
- **Customizable**: Easy to modify for your use case
- **Progressive complexity**: Start with `app.py` (beginner), level up to `app_advanced.py`

## 🛠️ Common Setup (All Templates)

```bash
# 1. Clone or download this repository
git clone <your-repo-url>
cd vibeathon-templates

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Navigate to a template
cd template-1-late-meal

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file with your API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# 6. Run the app
streamlit run app.py
```

## 🎯 Choosing Your First Template

**Brand new to coding?** Start with:
- Template 5 (Precept Prep) - Simplest, no database needed
- Template 1 (Late Meal Tracker) - Fun, practical, beginner-friendly
- Template 9 (Expense Splitter) - Useful for everyday life

**Some Python experience?** Try:
- Template 2 (Assignment Manager) - Good full-stack introduction
- Template 6 (Resume Builder) - Career-focused, practical output
- Template 7 (Flashcard Generator) - Learn spaced repetition algorithms

**Looking for career tools?** Build:
- Template 6 (Resume Builder) - Create professional application materials
- Template 8 (Internship Tracker) - Manage your job search

**Want a challenge?** Build:
- Template 4 (Study Group Matcher) - Recommendation systems and databases
- Template 7 (Flashcard Generator) - Advanced learning algorithms

**Ready for advanced features?** Try:
- Template 10 (Multi-Doc Research) - RAG patterns, extended thinking, literature reviews
- Template 11 (Code Learning) - Socratic teaching, educational AI, algorithm visualization
- Template 12 (Material Remix) - Style transfer, accessibility, creative transformations
- Template 13 (Lecture Companion) - Real-time AI, streaming, long context management

## 📖 Learning Resources

- [Anthropic Claude API Docs](https://docs.anthropic.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python Beginner's Guide](https://www.python.org/about/gettingstarted/)

## 🤝 Contributing

Have an idea for a new template? Found a bug? Contributions welcome!

1. Fork this repository
2. Create a new branch (`git checkout -b feature/new-template`)
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - feel free to use these templates for any purpose!

## 🎉 Inspiration

These templates were inspired by projects from Princeton's Vibe Coding events, where students build AI-powered solutions to real campus problems.

**Happy coding!** 🚀
