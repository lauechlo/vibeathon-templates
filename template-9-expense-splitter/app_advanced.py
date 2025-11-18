"""
Roommate Expense Splitter - Advanced Version
AI-powered receipt scanning and natural language expense entry!
"""

import streamlit as st
from anthropic import Anthropic
from dotenv import load_dotenv
import os
import base64

load_dotenv()

st.set_page_config(page_title="AI Expense Splitter", page_icon="🤖", layout="wide")


@st.cache_resource
def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("⚠️ ANTHROPIC_API_KEY not found!")
        st.stop()
    return Anthropic(api_key=api_key)


def parse_receipt_image(image_bytes, client):
    """Use Claude Vision to extract items and prices from receipt."""
    # Encode image
    image_data = base64.standard_b64encode(image_bytes).decode("utf-8")

    prompt = """Analyze this receipt and extract:

1. Store name
2. Date
3. List of items with prices (format: "Item - $X.XX")
4. Total amount

Format as:
Store: [name]
Date: [date]
Items:
- [item 1] - $[price]
- [item 2] - $[price]
Total: $[amount]"""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_data
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }]
        )

        return message.content[0].text.strip()

    except Exception as e:
        return f"Error: {e}"


def parse_natural_language_expense(text, client):
    """Parse natural language expense description."""
    prompt = f"""Parse this expense description:

"{text}"

Return JSON with:
- description: brief description
- amount: dollar amount
- category: one of [Groceries, Utilities, Rent, Household, Food, Other]

Example: "I paid $45 for groceries at Trader Joe's"
Result: {{"description": "Groceries at Trader Joe's", "amount": 45.00, "category": "Groceries"}}

Return ONLY valid JSON."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}]
        )

        import json
        result = json.loads(message.content[0].text.strip())
        return result

    except Exception as e:
        return None


def main():
    client = get_client()

    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("🤖 AI Expense Splitter")
        st.markdown("Scan receipts and track expenses with AI!")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("✨ **AI Powered**")

    tab1, tab2 = st.tabs(["📸 Scan Receipt", "💬 Natural Language"])

    with tab1:
        st.header("📸 Receipt Scanner")
        st.markdown("Upload a receipt photo and AI will extract the details!")

        uploaded_file = st.file_uploader("Upload receipt image", type=["jpg", "jpeg", "png"])

        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Receipt", use_column_width=True)

            if st.button("🔍 Scan Receipt", type="primary"):
                with st.spinner("Analyzing receipt..."):
                    image_bytes = uploaded_file.read()
                    result = parse_receipt_image(image_bytes, client)

                    st.divider()
                    st.subheader("Extracted Information")
                    st.text(result)

                    st.info("💡 **Tip**: Copy this information to add the expense in the main app (app.py)")

    with tab2:
        st.header("💬 Natural Language Expense Entry")
        st.markdown("Just describe the expense naturally!")

        with st.expander("See examples"):
            st.write("""
            - "I paid $45 for groceries yesterday"
            - "Spent $120 on utilities this month"
            - "Bought household items for $32.50"
            """)

        expense_text = st.text_input(
            "Describe the expense:",
            placeholder="e.g., 'I spent $50 on groceries at Whole Foods'"
        )

        if st.button("✨ Parse Expense", type="primary", disabled=not expense_text):
            with st.spinner("Understanding your expense..."):
                result = parse_natural_language_expense(expense_text, client)

                if result:
                    st.success("✅ Expense parsed!")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("Description", result.get('description', 'N/A'))
                    with col2:
                        st.metric("Amount", f"${result.get('amount', 0):.2f}")
                    with col3:
                        st.metric("Category", result.get('category', 'Other'))

                    st.info("💡 Use these details to add the expense in the main app!")
                else:
                    st.error("Couldn't parse expense. Try rephrasing!")

    st.divider()
    st.markdown("""
    <div style='text-align: center; color: gray;'>
    <p>🤖 Powered by Claude AI (with Vision!) | Use with <code>app.py</code> for full expense tracking</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
