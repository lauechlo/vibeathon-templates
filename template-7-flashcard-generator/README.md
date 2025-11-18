# 🎴 Flashcard Generator from Notes

**Turn your notes into effective study flashcards automatically!**

Creating flashcards is time-consuming. This app uses AI to auto-generate flashcards from your lecture notes, textbook passages, or study materials. Features spaced repetition to optimize learning.

## 🎯 What This App Does

- **Auto-generate flashcards**: Upload notes → get Q&A pairs instantly
- **Multiple question types**: Multiple choice, short answer, true/false
- **Spaced repetition**: Review cards at optimal intervals
- **Track progress**: See which concepts you've mastered
- **Export**: Share decks or export to Anki/Quizlet
- **Study modes**: Learn new cards, review, or test yourself

## 🚀 Quick Start

```bash
cd template-7-flashcard-generator
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=your_key_here" > .env  # For AI features
streamlit run app.py  # Beginner version
streamlit run app_advanced.py  # AI-powered generation
```

## 📁 File Structure

```
template-7-flashcard-generator/
├── README.md           # This file
├── app.py             # Beginner: manual flashcard creation
├── app_advanced.py    # AI: auto-generate from notes
├── requirements.txt   # Dependencies
└── data/             # Your flashcard decks
```

## 🎓 What You'll Learn

### Beginner Version
- CRUD operations for flashcards
- Spaced repetition algorithm (SM-2)
- Session state management
- Progress tracking
- Data export/import

### Advanced Version
- Claude AI for content extraction
- Question generation techniques
- Concept identification
- Multiple question type generation
- Difficulty assessment

## 🔧 Extension Ideas

### Easy
- Add images to flashcards
- Tags and categories
- Daily streak tracking
- Dark mode

### Medium
- Import from Anki/Quizlet
- Collaborative decks
- Share with classmates
- Mobile-friendly UI

### Advanced
- Image occlusion (for diagrams)
- Text-to-speech for language learning
- Adaptive difficulty
- ML-based retention prediction
- Integration with course materials

## 📊 Spaced Repetition

This app uses the **SM-2 algorithm** for optimal review timing:

- **New cards**: Review after 1 day
- **Easy cards**: Interval increases (3d → 7d → 14d → 30d)
- **Hard cards**: Interval resets
- **Forgot cards**: Start over

This is scientifically proven to improve long-term retention!

## 💡 Study Tips

### Creating Good Flashcards
- **One concept per card**: Don't combine multiple ideas
- **Use active recall**: Questions should require thinking
- **Be specific**: Avoid vague questions
- **Use your own words**: Better retention than copy-paste
- **Include context**: Help trigger memory

### Effective Studying
- **Review daily**: Even 10-15 minutes helps
- **Don't cram**: Spaced repetition beats marathon sessions
- **Test yourself**: Use "hard" honestly to improve retention
- **Mix subjects**: Interleaving improves learning
- **Review before exams**: But don't wait until the last minute

## 🎯 Use Cases

**Use Case 1: Exam Prep**
1. Upload lecture notes from last week
2. AI generates 20-30 flashcards
3. Study 10 minutes daily
4. By exam time, you've mastered the material

**Use Case 2: Language Learning**
1. Create vocabulary flashcards
2. Practice daily with spaced repetition
3. Track progress over weeks
4. Export to mobile app for on-the-go study

**Use Case 3: Medical/STEM**
1. Upload textbook passages
2. Generate definition and concept cards
3. Mix question types (fill-in-blank, multiple choice)
4. Master complex material systematically

## 🐛 Troubleshooting

**Cards not saving**: Check that the `data/` folder exists and has write permissions

**Spaced repetition not working**: Make sure you're marking cards honestly (Easy/Hard/Forgot)

**AI not generating good cards**: Try pasting cleaner, more structured notes

## 📚 Resources

- [Spaced Repetition Research](https://www.gwern.net/Spaced-repetition)
- [SM-2 Algorithm](https://super-memory.com/english/ol/sm2.htm)
- [Anki Manual](https://docs.ankiweb.net/)

---

**Study smarter, not harder!**

Questions? Check the main repository README or visit [Anthropic's docs](https://docs.anthropic.com/).
