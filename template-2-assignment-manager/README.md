# 📝 Course & Assignment Manager

**Never miss a deadline again! Track assignments and get AI-powered study tips.**

A smart assignment tracker that helps you manage coursework, deadlines, and study sessions. The advanced version uses Claude AI to parse assignment descriptions, suggest study plans, and provide personalized productivity tips.

## 🎯 What This App Does

- **Track assignments**: Add courses and their assignments with deadlines
- **Visual dashboard**: See all upcoming deadlines at a glance
- **Smart reminders**: Know what's due soon
- **Study session planning**: Break down large assignments into manageable chunks
- **AI study tips**: Get personalized suggestions (advanced version)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- A Claude API key for advanced version ([get one here](https://console.anthropic.com/))

### Installation

```bash
# 1. Navigate to this directory
cd template-2-assignment-manager

# 2. Install dependencies
pip install -r requirements.txt

# 3. For advanced version: Create .env file with your API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# 4. Run the beginner version
streamlit run app.py

# OR run the advanced version
streamlit run app_advanced.py
```

## 📁 File Structure

```
template-2-assignment-manager/
├── README.md           # This file
├── app.py             # Beginner version
├── app_advanced.py    # Advanced version with AI
├── requirements.txt   # Python dependencies
└── data/             # Created automatically
```

## 🎓 What You'll Learn

### Beginner Version (`app.py`)
- Building CRUD (Create, Read, Update, Delete) apps
- Working with dates and deadlines
- Data persistence with JSON
- Creating interactive dashboards
- Form handling in Streamlit

### Advanced Version (`app_advanced.py`)
- Claude API integration
- Natural language task parsing
- AI-generated study plans
- Intelligent scheduling
- Context-aware recommendations

## 🔧 Customization Ideas

### Easy
- Add custom course colors
- Change reminder thresholds (3 days → 1 week)
- Add assignment priorities (high/medium/low)
- Custom categories (homework, project, exam, reading)

### Medium
- Email notifications for upcoming deadlines
- Export to Google Calendar
- Weekly study schedule generator
- Grade tracking and GPA calculator

### Advanced
- Integration with course websites (Canvas, Blackboard)
- Syllabus PDF parsing with Claude
- Smart workload balancing across courses
- Collaboration features (study groups)
- Historical analytics (time spent per course)

## 📊 How It Works

### Beginner Version Flow
1. Add courses (e.g., "COS 126", "PHI 201")
2. Add assignments with deadlines
3. View dashboard with upcoming deadlines
4. Mark assignments as complete
5. See progress per course

### Advanced Version Flow
1. Type assignment in natural language: "Essay on Kant due next Friday"
2. Claude parses course, assignment type, and deadline
3. AI suggests a study plan: "Start outline Monday, draft Wednesday, revise Friday"
4. Get personalized tips based on workload
5. Track progress with AI-generated insights

## 💡 Extension Ideas

1. **Pomodoro timer integration**: Built-in study session timer
2. **Syllabus upload**: Parse entire semester from PDF
3. **Study buddy matcher**: Find classmates in same courses
4. **Resource library**: Save helpful links per assignment
5. **Time estimation**: AI predicts how long assignments will take
6. **Habit tracking**: Track study consistency

## 🐛 Troubleshooting

**Can't install dependencies**: Make sure you're using Python 3.8+: `python --version`

**Date formatting issues**: Use YYYY-MM-DD format (e.g., 2024-03-15)

**Data not saving**: Check that you have write permissions in the directory

**API errors (advanced)**: Verify your `.env` file exists and contains valid API key

## 📚 Code Walkthrough

### Key Components

**Beginner Version**:
- `Course` class: Represents a course with assignments
- `Assignment` class: Stores assignment details
- `load_data()` / `save_data()`: JSON persistence
- `get_upcoming_assignments()`: Deadline logic
- `display_dashboard()`: Visual overview

**Advanced Version** (additional):
- `parse_assignment()`: Uses Claude to understand natural language
- `generate_study_plan()`: AI creates breakdown of tasks
- `get_productivity_tips()`: Context-aware suggestions
- `analyze_workload()`: Identifies busy weeks

## 🎨 Sample Data

Try adding these example assignments to test the app:

- **COS 126**: Programming Assignment 3, Due: [3 days from now]
- **PHI 201**: Essay on Descartes, Due: [1 week from now]
- **MAT 201**: Problem Set 5, Due: [tomorrow]
- **ENG 101**: Reading Response, Due: [5 days from now]

## 🤝 Contributing

This is a starter template - make it your own! Add features, improve the UI, or adapt it for your specific needs.

## 📄 License

MIT License - use freely!

---

**Built with ❤️ for students everywhere**

Questions? Check the main repository README or visit [Anthropic's docs](https://docs.anthropic.com/).
