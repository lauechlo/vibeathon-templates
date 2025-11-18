# 🍕 Princeton Late Meal Tracker

**Track your late meal spending and stay within budget!**

Inspired by the winning project from Princeton's Vibe Coding event, this app helps you track late meal purchases, calculate if you're exceeding the price limit, and generate a fun "weekly wrapped" summary.

## 🎯 What This App Does

- **Track purchases**: Add items from Princeton's late meal menu
- **Auto-calculate totals**: Know instantly if you're over the $10 limit
- **Weekly summary**: Get a "Spotify Wrapped"-style summary of your eating habits
- **Natural language input**: Type "I had a chicken sandwich and fries" (advanced version)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- A Claude API key ([get one here](https://console.anthropic.com/))

### Installation

```bash
# 1. Navigate to this directory
cd template-1-late-meal

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create a .env file with your API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# 4. Run the beginner version
streamlit run app.py

# OR run the advanced version
streamlit run app_advanced.py
```

## 📁 File Structure

```
template-1-late-meal/
├── README.md           # This file
├── app.py             # Beginner version (no AI needed)
├── app_advanced.py    # Advanced version (with Claude integration)
├── requirements.txt   # Python dependencies
└── data/             # Created automatically to store purchase history
```

## 🎓 What You'll Learn

### Beginner Version (`app.py`)
- Building web apps with Streamlit
- Working with forms and user input
- Storing data in CSV files
- Creating data visualizations
- Session state management

### Advanced Version (`app_advanced.py`)
- Integrating Claude API
- Natural language processing
- Vision API for receipt scanning (coming soon!)
- Generating personalized insights with AI
- Advanced data analysis

## 🔧 Customization Ideas

### Easy
- Change the price limit ($10 → your budget)
- Add more menu items
- Customize the "weekly wrapped" design
- Add different dining halls

### Medium
- Add user authentication (multiple people)
- Export data to Google Sheets
- Email weekly summaries
- Add meal plan integration

### Advanced
- Receipt photo scanning with Claude Vision
- Budget recommendations based on spending patterns
- Integration with Princeton dining API
- Predictive analytics for weekly spending

## 📊 How It Works

### Beginner Version Flow
1. User selects items from dropdown menu
2. App calculates total price
3. Stores purchase in CSV file
4. Displays weekly summary with charts

### Advanced Version Flow
1. User types in natural language: "I got a burger and fries"
2. Claude parses the text and identifies menu items
3. App calculates total and stores data
4. Claude generates personalized insights
5. Weekly summary includes AI-generated recommendations

## 🐛 Troubleshooting

**Streamlit won't start**: Make sure you installed all dependencies with `pip install -r requirements.txt`

**API key error**: Check that your `.env` file exists and contains `ANTHROPIC_API_KEY=your_key`

**Data not saving**: The app creates a `data/` folder automatically. Make sure you have write permissions.

**Import errors**: Ensure you're using Python 3.8+: `python --version`

## 💡 Extension Ideas

1. **Multi-user support**: Add login system so roommates can track separately
2. **Budget alerts**: Get notified when approaching weekly limit
3. **Nutrition tracking**: Add calorie/macro information
4. **Social features**: Compare spending with friends (anonymously)
5. **Receipt scanning**: Take a photo instead of manual entry
6. **Meal recommendations**: AI suggests items based on budget remaining

## 📚 Code Walkthrough

### Key Components

**Beginner Version**:
- `load_menu()`: Loads Princeton late meal menu items and prices
- `save_purchase()`: Saves purchase to CSV file
- `get_weekly_summary()`: Calculates weekly spending statistics
- `display_weekly_wrapped()`: Creates fun summary visualization

**Advanced Version**:
- `parse_natural_language()`: Uses Claude to understand user input
- `generate_insights()`: Creates personalized recommendations
- `analyze_spending_patterns()`: AI-powered trend analysis

## 🎨 UI Customization

The app uses Streamlit's default styling. To customize:

```python
# Add to the top of app.py
st.set_page_config(
    page_title="Late Meal Tracker",
    page_icon="🍕",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    </style>
""", unsafe_allow_html=True)
```

## 🤝 Contributing

Found a bug? Have an improvement? Feel free to modify and share!

## 📄 License

MIT License - use this template for any purpose!

---

**Built with ❤️ for Princeton students**

Questions? Check out the main repository README or [Anthropic's documentation](https://docs.anthropic.com/).
