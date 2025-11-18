# 🎉 Princeton Event Finder

**Discover campus events with natural language search!**

Never miss free food, talks, or fun activities on campus. This app aggregates Princeton events and lets you search using natural language like "Find me free food events tonight" or "CS talks this week."

## 🎯 What This App Does

- **Browse events**: See all upcoming campus events
- **Natural language search**: "Show me free food events tonight" (AI version)
- **Smart filtering**: By date, type, location, or tags
- **Personal calendar**: Save events you're interested in
- **Email digests**: Get weekly event recommendations (advanced)

## 🚀 Quick Start

```bash
# 1. Navigate to this directory
cd template-3-event-finder

# 2. Install dependencies
pip install -r requirements.txt

# 3. For AI features: Create .env file
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# 4. Run the app
streamlit run app.py  # Beginner version
streamlit run app_advanced.py  # AI-powered version
```

## 📁 File Structure

```
template-3-event-finder/
├── README.md           # This file
├── app.py             # Beginner version
├── app_advanced.py    # AI-powered version
├── requirements.txt   # Dependencies
├── data/             # Event data (auto-generated)
└── sample_events.json # Sample event data
```

## 🎓 What You'll Learn

### Beginner Version
- Working with JSON data
- Date/time handling
- Search and filtering logic
- Building event calendars
- Streamlit layouts

### Advanced Version
- Claude AI for natural language search
- Intelligent event recommendations
- Semantic search
- Web scraping basics
- API integration patterns

## 🔧 Extension Ideas

### Easy
- Add more event types
- Custom color themes per category
- Export to Google Calendar
- Event reminders

### Medium
- Web scraping Princeton events pages
- Email notifications
- Friend groups (see who's attending)
- Event ratings/reviews

### Advanced
- Real-time updates from Princeton calendars
- Smart recommendations based on interests
- Integration with course schedules
- Social features (comments, RSVPs)

---

**Built with ❤️ for Princeton students**
