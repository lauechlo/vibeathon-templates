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

**Some Python experience?** Try:
- Template 2 (Assignment Manager) - Good full-stack introduction
- Template 3 (Event Finder) - Learn web scraping and NLP

**Want a challenge?** Build:
- Template 4 (Study Group Matcher) - Recommendation systems and databases

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
