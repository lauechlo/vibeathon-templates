"""
Princeton Late Meal Tracker - Beginner Version
A simple Streamlit app to track late meal purchases and stay within budget.

This version doesn't require Claude API - perfect for getting started!
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import json

# Configure the page
st.set_page_config(
    page_title="Late Meal Tracker",
    page_icon="🍕",
    layout="wide"
)

# Constants
PRICE_LIMIT = 10.00  # Princeton late meal limit
DATA_DIR = "data"
PURCHASES_FILE = os.path.join(DATA_DIR, "purchases.csv")

# Princeton Late Meal Menu (typical items and prices)
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


def initialize_data_dir():
    """Create data directory if it doesn't exist."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Created {DATA_DIR} directory")


def load_purchases():
    """Load purchase history from CSV file."""
    initialize_data_dir()

    if os.path.exists(PURCHASES_FILE):
        try:
            df = pd.read_csv(PURCHASES_FILE)
            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except Exception as e:
            st.error(f"Error loading purchases: {e}")
            return pd.DataFrame(columns=['timestamp', 'items', 'total', 'over_limit'])
    else:
        # Create empty DataFrame with correct columns
        return pd.DataFrame(columns=['timestamp', 'items', 'total', 'over_limit'])


def save_purchase(items_dict, total, over_limit):
    """
    Save a purchase to the CSV file.

    Args:
        items_dict: Dictionary of {item_name: quantity}
        total: Total price
        over_limit: Boolean indicating if over $10 limit
    """
    initialize_data_dir()

    # Create purchase record
    purchase = {
        'timestamp': datetime.now(),
        'items': json.dumps(items_dict),  # Convert dict to JSON string
        'total': total,
        'over_limit': over_limit
    }

    # Load existing data
    df = load_purchases()

    # Append new purchase
    df = pd.concat([df, pd.DataFrame([purchase])], ignore_index=True)

    # Save to CSV
    df.to_csv(PURCHASES_FILE, index=False)


def calculate_total(selected_items):
    """
    Calculate total price for selected items.

    Args:
        selected_items: Dictionary of {item_name: quantity}

    Returns:
        float: Total price
    """
    total = 0
    for item, quantity in selected_items.items():
        if quantity > 0:
            total += MENU[item] * quantity
    return total


def get_weekly_summary():
    """
    Get summary statistics for the past week.

    Returns:
        dict: Summary statistics
    """
    df = load_purchases()

    if df.empty:
        return None

    # Filter to last 7 days
    week_ago = datetime.now() - timedelta(days=7)
    weekly_df = df[df['timestamp'] >= week_ago]

    if weekly_df.empty:
        return None

    # Calculate statistics
    summary = {
        'total_spent': weekly_df['total'].sum(),
        'num_purchases': len(weekly_df),
        'avg_purchase': weekly_df['total'].mean(),
        'times_over_limit': weekly_df['over_limit'].sum(),
        'favorite_items': get_favorite_items(weekly_df),
    }

    return summary


def get_favorite_items(df, top_n=3):
    """
    Find most frequently purchased items.

    Args:
        df: DataFrame of purchases
        top_n: Number of top items to return

    Returns:
        list: Top items and their counts
    """
    all_items = []

    # Parse items from each purchase
    for items_json in df['items']:
        try:
            items_dict = json.loads(items_json)
            for item, qty in items_dict.items():
                all_items.extend([item] * qty)
        except:
            continue

    if not all_items:
        return []

    # Count items
    item_counts = pd.Series(all_items).value_counts()
    return list(item_counts.head(top_n).items())


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Header
    st.title("🍕 Princeton Late Meal Tracker")
    st.markdown("Track your late meal spending and stay within the $10 limit!")

    # Sidebar for weekly summary
    with st.sidebar:
        st.header("📊 Weekly Summary")
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
        else:
            st.info("No purchases yet! Add your first meal below.")

    # Main content - two columns
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("Add Late Meal Purchase")

        # Display menu and allow item selection
        st.subheader("Select Items")
        selected_items = {}

        # Create a nice grid layout for menu items
        for i in range(0, len(MENU), 3):
            cols = st.columns(3)
            items_slice = list(MENU.items())[i:i+3]

            for col, (item, price) in zip(cols, items_slice):
                with col:
                    # Use number input for quantity
                    qty = st.number_input(
                        f"{item} (${price:.2f})",
                        min_value=0,
                        max_value=10,
                        value=0,
                        step=1,
                        key=item
                    )
                    if qty > 0:
                        selected_items[item] = qty

        # Calculate and display total
        if selected_items:
            total = calculate_total(selected_items)
            over_limit = total > PRICE_LIMIT

            st.divider()
            st.subheader("Purchase Summary")

            # Display selected items
            for item, qty in selected_items.items():
                item_total = MENU[item] * qty
                st.write(f"- {qty}x {item}: ${item_total:.2f}")

            # Display total with color coding
            if over_limit:
                st.error(f"### Total: ${total:.2f} ⚠️ Over limit by ${total - PRICE_LIMIT:.2f}")
            else:
                st.success(f"### Total: ${total:.2f} ✅ Under limit!")

            # Save button
            if st.button("💾 Save Purchase", type="primary", use_container_width=True):
                save_purchase(selected_items, total, over_limit)
                st.success("Purchase saved! Check your weekly summary in the sidebar.")
                st.balloons()
                # Force refresh
                st.rerun()
        else:
            st.info("Select items to see your total.")

    with col2:
        st.header("💡 Quick Stats")

        # Display the menu with prices for reference
        with st.expander("📋 Full Menu", expanded=False):
            menu_df = pd.DataFrame([
                {"Item": item, "Price": f"${price:.2f}"}
                for item, price in MENU.items()
            ])
            st.dataframe(menu_df, hide_index=True, use_container_width=True)

        # Tips
        with st.expander("💰 Budget Tips", expanded=True):
            st.write("""
            - The limit is $10 per purchase
            - Combo meals (burger + fries) often go over
            - Consider sharing with a friend!
            - Salads and grilled cheese are budget-friendly
            """)

    # Purchase history
    st.divider()
    st.header("📜 Purchase History")

    df = load_purchases()
    if not df.empty:
        # Show last 10 purchases
        recent = df.sort_values('timestamp', ascending=False).head(10).copy()

        # Format for display
        recent['timestamp'] = recent['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        recent['total'] = recent['total'].apply(lambda x: f"${x:.2f}")
        recent['over_limit'] = recent['over_limit'].apply(lambda x: "❌ Yes" if x else "✅ No")

        # Parse items for display
        recent['items_display'] = recent['items'].apply(
            lambda x: ', '.join([f"{k}({v})" for k, v in json.loads(x).items()])
        )

        # Display table
        display_df = recent[['timestamp', 'items_display', 'total', 'over_limit']]
        display_df.columns = ['Date/Time', 'Items', 'Total', 'Over Limit?']

        st.dataframe(display_df, hide_index=True, use_container_width=True)

        # Clear history button
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
    <p>💡 <b>Tip:</b> Want to add natural language input? Check out <code>app_advanced.py</code>!</p>
    <p>Built with ❤️ for Princeton students | <a href='https://docs.anthropic.com/' target='_blank'>Powered by Claude</a></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
