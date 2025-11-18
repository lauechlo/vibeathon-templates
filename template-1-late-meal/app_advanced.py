"""
Princeton Late Meal Tracker - Advanced Version
Uses Claude AI for natural language input and personalized insights!

Features:
- Natural language input ("I had a burger and fries")
- AI-generated spending insights
- Smart recommendations
- Weekly wrapped with AI commentary
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import json
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="Late Meal Tracker AI",
    page_icon="🍕",
    layout="wide"
)

# Constants
PRICE_LIMIT = 10.00
DATA_DIR = "data"
PURCHASES_FILE = os.path.join(DATA_DIR, "purchases.csv")

# Princeton Late Meal Menu
MENU = {
    "Cheeseburger": 6.50,
    "Hamburger": 6.00,
    "Chicken Sandwich": 6.50,
    "Veggie Burger": 6.00,
    "Grilled Cheese": 4.50,
    "Fries": 3.50,
    "Onion Rings": 4.00,
    "Mozzarella Sticks": 4.50,
    "Chicken Tenders": 7.00,
    "Caesar Salad": 5.50,
    "Garden Salad": 5.00,
    "Pizza Slice": 3.50,
    "Soda": 2.00,
    "Bottled Water": 1.50,
    "Chips": 1.50,
    "Cookie": 2.00,
    "Ice Cream": 3.00,
}

# Initialize Anthropic client
@st.cache_resource
def get_anthropic_client():
    """Initialize and cache the Anthropic client."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("⚠️ ANTHROPIC_API_KEY not found in .env file!")
        st.stop()
    return Anthropic(api_key=api_key)


def initialize_data_dir():
    """Create data directory if it doesn't exist."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_purchases():
    """Load purchase history from CSV file."""
    initialize_data_dir()

    if os.path.exists(PURCHASES_FILE):
        try:
            df = pd.read_csv(PURCHASES_FILE)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except Exception as e:
            st.error(f"Error loading purchases: {e}")
            return pd.DataFrame(columns=['timestamp', 'items', 'total', 'over_limit'])
    else:
        return pd.DataFrame(columns=['timestamp', 'items', 'total', 'over_limit'])


def save_purchase(items_dict, total, over_limit):
    """Save a purchase to the CSV file."""
    initialize_data_dir()

    purchase = {
        'timestamp': datetime.now(),
        'items': json.dumps(items_dict),
        'total': total,
        'over_limit': over_limit
    }

    df = load_purchases()
    df = pd.concat([df, pd.DataFrame([purchase])], ignore_index=True)
    df.to_csv(PURCHASES_FILE, index=False)


def parse_natural_language_input(text, client):
    """
    Use Claude to parse natural language input and identify menu items.

    Args:
        text: User's natural language description
        client: Anthropic client

    Returns:
        dict: Parsed items with quantities
    """
    menu_list = "\n".join([f"- {item}: ${price:.2f}" for item, price in MENU.items()])

    prompt = f"""You are a helpful assistant for a Princeton late meal ordering system.

The user will describe what they ordered in natural language. Your job is to parse their input and return ONLY a valid JSON object mapping menu items to quantities.

Available menu items:
{menu_list}

User input: "{text}"

Return ONLY a JSON object like this (no other text):
{{"Cheeseburger": 1, "Fries": 1}}

If an item isn't on the menu, use the closest match or omit it.
If you can't parse the input, return an empty object: {{}}
"""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the response text
        response_text = message.content[0].text.strip()

        # Try to parse as JSON
        items_dict = json.loads(response_text)

        # Validate that items are in menu
        validated_items = {}
        for item, qty in items_dict.items():
            if item in MENU and isinstance(qty, int) and qty > 0:
                validated_items[item] = qty

        return validated_items

    except Exception as e:
        st.error(f"Error parsing input: {e}")
        return {}


def generate_weekly_insights(summary_data, client):
    """
    Use Claude to generate personalized insights about spending habits.

    Args:
        summary_data: Dictionary with weekly summary statistics
        client: Anthropic client

    Returns:
        str: AI-generated insights
    """
    prompt = f"""You are a friendly financial advisor for college students.

Based on their late meal spending this week, provide brief, encouraging insights and tips.

Weekly stats:
- Total spent: ${summary_data['total_spent']:.2f}
- Number of purchases: {summary_data['num_purchases']}
- Average per purchase: ${summary_data['avg_purchase']:.2f}
- Times over $10 limit: {summary_data['times_over_limit']}
- Favorite items: {', '.join([item for item, count in summary_data['favorite_items']])}

Write 2-3 short, friendly bullet points with insights and suggestions. Keep it casual and encouraging!
"""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=512,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text.strip()

    except Exception as e:
        return f"Error generating insights: {e}"


def calculate_total(selected_items):
    """Calculate total price for selected items."""
    total = 0
    for item, quantity in selected_items.items():
        if quantity > 0 and item in MENU:
            total += MENU[item] * quantity
    return total


def get_weekly_summary():
    """Get summary statistics for the past week."""
    df = load_purchases()

    if df.empty:
        return None

    week_ago = datetime.now() - timedelta(days=7)
    weekly_df = df[df['timestamp'] >= week_ago]

    if weekly_df.empty:
        return None

    # Get favorite items
    all_items = []
    for items_json in weekly_df['items']:
        try:
            items_dict = json.loads(items_json)
            for item, qty in items_dict.items():
                all_items.extend([item] * qty)
        except:
            continue

    favorite_items = []
    if all_items:
        item_counts = pd.Series(all_items).value_counts()
        favorite_items = list(item_counts.head(3).items())

    summary = {
        'total_spent': weekly_df['total'].sum(),
        'num_purchases': len(weekly_df),
        'avg_purchase': weekly_df['total'].mean(),
        'times_over_limit': weekly_df['over_limit'].sum(),
        'favorite_items': favorite_items,
    }

    return summary


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Initialize Claude client
    client = get_anthropic_client()

    # Header with AI badge
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("🍕 Princeton Late Meal Tracker")
        st.markdown("Track your late meal spending with **AI-powered insights**!")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("🤖 **AI Enhanced**")

    # Sidebar for weekly summary with AI insights
    with st.sidebar:
        st.header("📊 Weekly Wrapped")
        summary = get_weekly_summary()

        if summary:
            st.metric("Total Spent This Week", f"${summary['total_spent']:.2f}")
            st.metric("Number of Purchases", summary['num_purchases'])
            st.metric("Average Purchase", f"${summary['avg_purchase']:.2f}")
            st.metric("Times Over Limit", int(summary['times_over_limit']))

            if summary['favorite_items']:
                st.subheader("🌟 Your Favorites")
                for item, count in summary['favorite_items']:
                    st.write(f"- {item} ({count}x)")

            # AI-generated insights
            st.divider()
            st.subheader("🤖 AI Insights")
            with st.spinner("Generating personalized insights..."):
                insights = generate_weekly_insights(summary, client)
                st.markdown(insights)
        else:
            st.info("No purchases yet! Add your first meal below.")

    # Main content
    st.header("Add Purchase")

    # Tab interface for different input methods
    tab1, tab2 = st.tabs(["🤖 Natural Language (AI)", "📝 Manual Selection"])

    with tab1:
        st.markdown("**Just describe what you ordered!** Try: *'I got a burger, fries, and a soda'*")

        # Natural language input
        user_input = st.text_input(
            "What did you order?",
            placeholder="I had a chicken sandwich and fries",
            key="nl_input"
        )

        if st.button("✨ Parse with AI", type="primary", disabled=not user_input):
            with st.spinner("🤖 Understanding your order..."):
                parsed_items = parse_natural_language_input(user_input, client)

                if parsed_items:
                    st.success("✅ Order recognized!")

                    # Display parsed items
                    total = calculate_total(parsed_items)
                    over_limit = total > PRICE_LIMIT

                    st.subheader("Parsed Items:")
                    for item, qty in parsed_items.items():
                        item_total = MENU[item] * qty
                        st.write(f"- {qty}x {item}: ${item_total:.2f}")

                    # Display total
                    if over_limit:
                        st.error(f"### Total: ${total:.2f} ⚠️ Over limit by ${total - PRICE_LIMIT:.2f}")
                    else:
                        st.success(f"### Total: ${total:.2f} ✅ Under limit!")

                    # Confirm and save
                    if st.button("💾 Confirm & Save", type="primary"):
                        save_purchase(parsed_items, total, over_limit)
                        st.success("Purchase saved!")
                        st.balloons()
                        st.rerun()
                else:
                    st.warning("Couldn't parse your order. Try being more specific or use manual selection.")

    with tab2:
        st.markdown("**Select items manually from the menu**")

        selected_items = {}

        # Create grid layout for menu items
        for i in range(0, len(MENU), 3):
            cols = st.columns(3)
            items_slice = list(MENU.items())[i:i+3]

            for col, (item, price) in zip(cols, items_slice):
                with col:
                    qty = st.number_input(
                        f"{item} (${price:.2f})",
                        min_value=0,
                        max_value=10,
                        value=0,
                        step=1,
                        key=f"manual_{item}"
                    )
                    if qty > 0:
                        selected_items[item] = qty

        if selected_items:
            total = calculate_total(selected_items)
            over_limit = total > PRICE_LIMIT

            st.divider()
            st.subheader("Purchase Summary")

            for item, qty in selected_items.items():
                item_total = MENU[item] * qty
                st.write(f"- {qty}x {item}: ${item_total:.2f}")

            if over_limit:
                st.error(f"### Total: ${total:.2f} ⚠️ Over limit by ${total - PRICE_LIMIT:.2f}")
            else:
                st.success(f"### Total: ${total:.2f} ✅ Under limit!")

            if st.button("💾 Save Purchase", type="primary", key="manual_save"):
                save_purchase(selected_items, total, over_limit)
                st.success("Purchase saved!")
                st.balloons()
                st.rerun()
        else:
            st.info("Select items to see your total.")

    # Purchase history
    st.divider()
    st.header("📜 Purchase History")

    df = load_purchases()
    if not df.empty:
        recent = df.sort_values('timestamp', ascending=False).head(10).copy()

        recent['timestamp'] = recent['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        recent['total'] = recent['total'].apply(lambda x: f"${x:.2f}")
        recent['over_limit'] = recent['over_limit'].apply(lambda x: "❌ Yes" if x else "✅ No")
        recent['items_display'] = recent['items'].apply(
            lambda x: ', '.join([f"{k}({v})" for k, v in json.loads(x).items()])
        )

        display_df = recent[['timestamp', 'items_display', 'total', 'over_limit']]
        display_df.columns = ['Date/Time', 'Items', 'Total', 'Over Limit?']

        st.dataframe(display_df, hide_index=True, use_container_width=True)

        if st.button("🗑️ Clear History"):
            if os.path.exists(PURCHASES_FILE):
                os.remove(PURCHASES_FILE)
                st.success("History cleared!")
                st.rerun()
    else:
        st.info("No purchase history yet. Add your first meal above!")

    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: gray;'>
    <p>🤖 <b>AI-Powered</b> by Claude | Built with ❤️ for Princeton students</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
