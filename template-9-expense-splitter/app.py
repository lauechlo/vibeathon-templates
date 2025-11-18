"""
Roommate Expense Splitter - Beginner Version
Track shared expenses and settle up fairly!
"""

import streamlit as st
import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict

st.set_page_config(page_title="Expense Splitter", page_icon="💰", layout="wide")

DATA_DIR = "data"
EXPENSES_FILE = os.path.join(DATA_DIR, "expenses.json")
ROOMMATES_FILE = os.path.join(DATA_DIR, "roommates.json")


@dataclass
class Expense:
    id: str
    description: str
    amount: float
    paid_by: str
    split_with: List[str]
    date: str
    category: str = "Other"


def init_data():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_expenses():
    init_data()
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, 'r') as f:
            return [Expense(**e) for e in json.load(f)]
    return []


def save_expenses(expenses):
    with open(EXPENSES_FILE, 'w') as f:
        json.dump([asdict(e) for e in expenses], f, indent=2)


def load_roommates():
    init_data()
    if os.path.exists(ROOMMATES_FILE):
        with open(ROOMMATES_FILE, 'r') as f:
            return json.load(f)
    return []


def save_roommates(roommates):
    with open(ROOMMATES_FILE, 'w') as f:
        json.dump(roommates, f, indent=2)


def calculate_balances(expenses, roommates):
    """Calculate who owes whom."""
    balances = {person: 0.0 for person in roommates}

    for expense in expenses:
        # Person who paid gets credited
        balances[expense.paid_by] += expense.amount

        # Split the cost
        split_amount = expense.amount / len(expense.split_with)

        for person in expense.split_with:
            balances[person] -= split_amount

    return balances


def calculate_settlements(balances):
    """Calculate minimum transactions to settle all debts."""
    creditors = [(person, amount) for person, amount in balances.items() if amount > 0.01]
    debtors = [(person, -amount) for person, amount in balances.items() if amount < -0.01]

    creditors.sort(key=lambda x: x[1], reverse=True)
    debtors.sort(key=lambda x: x[1], reverse=True)

    settlements = []

    i, j = 0, 0
    while i < len(creditors) and j < len(debtors):
        creditor, credit = creditors[i]
        debtor, debt = debtors[j]

        amount = min(credit, debt)

        settlements.append({
            'from': debtor,
            'to': creditor,
            'amount': amount
        })

        creditors[i] = (creditor, credit - amount)
        debtors[j] = (debtor, debt - amount)

        if creditors[i][1] < 0.01:
            i += 1
        if debtors[j][1] < 0.01:
            j += 1

    return settlements


def main():
    st.title("💰 Roommate Expense Splitter")
    st.markdown("Track shared expenses and settle up easily!")

    if 'expenses' not in st.session_state:
        st.session_state.expenses = load_expenses()

    if 'roommates' not in st.session_state:
        st.session_state.roommates = load_roommates()

    expenses = st.session_state.expenses
    roommates = st.session_state.roommates

    # Sidebar - Setup roommates
    with st.sidebar:
        st.header("👥 Roommates")

        if not roommates:
            st.info("Add roommates to get started!")

        new_roommate = st.text_input("Add roommate", placeholder="Name")
        if st.button("➕ Add") and new_roommate:
            if new_roommate not in roommates:
                roommates.append(new_roommate)
                save_roommates(roommates)
                st.rerun()

        if roommates:
            st.write("**Current roommates:**")
            for person in roommates:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"• {person}")
                with col2:
                    if st.button("🗑️", key=f"remove_{person}"):
                        roommates.remove(person)
                        save_roommates(roommates)
                        st.rerun()

        st.divider()

        # Quick stats
        if expenses and roommates:
            balances = calculate_balances(expenses, roommates)

            st.subheader("💵 Current Balances")
            for person, balance in balances.items():
                if balance > 0.01:
                    st.success(f"{person}: +${balance:.2f}")
                elif balance < -0.01:
                    st.error(f"{person}: -${abs(balance):.2f}")
                else:
                    st.info(f"{person}: $0.00")

    if not roommates:
        st.warning("⚠️ Please add roommates in the sidebar first!")
        return

    tab1, tab2, tab3 = st.tabs(["➕ Add Expense", "💵 Settle Up", "📊 History"])

    # TAB 1: Add Expense
    with tab1:
        st.header("Add New Expense")

        with st.form("add_expense"):
            description = st.text_input("Description *", placeholder="Groceries from Whole Foods")
            amount = st.number_input("Amount ($) *", min_value=0.01, step=0.01)

            col1, col2 = st.columns(2)

            with col1:
                paid_by = st.selectbox("Paid by *", roommates)

            with col2:
                category = st.selectbox("Category", ["Groceries", "Utilities", "Rent", "Household", "Food", "Other"])

            split_with = st.multiselect("Split with *", roommates, default=roommates)

            if st.form_submit_button("Add Expense", type="primary"):
                if description and amount > 0 and paid_by and split_with:
                    new_expense = Expense(
                        id=str(len(expenses) + 1),
                        description=description,
                        amount=amount,
                        paid_by=paid_by,
                        split_with=split_with,
                        date=datetime.now().isoformat(),
                        category=category
                    )
                    expenses.append(new_expense)
                    save_expenses(expenses)
                    st.success(f"✅ Added ${amount:.2f} expense!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields!")

    # TAB 2: Settle Up
    with tab2:
        st.header("💵 How to Settle Up")

        if expenses:
            balances = calculate_balances(expenses, roommates)
            settlements = calculate_settlements(balances)

            if not settlements:
                st.success("🎉 All settled up! No one owes anyone.")
            else:
                st.write("**Minimum transactions needed:**")

                for settlement in settlements:
                    st.write(f"**{settlement['from']}** pays **{settlement['to']}**: ${settlement['amount']:.2f}")

                st.divider()

                st.info("💡 **Tip**: Use Venmo, Zelle, or cash to settle these payments, then mark them as paid.")

                if st.button("✅ Clear All Balances"):
                    st.session_state.expenses = []
                    save_expenses([])
                    st.success("All expenses cleared!")
                    st.rerun()
        else:
            st.info("No expenses yet. Add some in the first tab!")

    # TAB 3: History
    with tab3:
        st.header("📊 Expense History")

        if expenses:
            # Total spent
            total = sum(e.amount for e in expenses)
            st.metric("Total Expenses", f"${total:.2f}")

            st.divider()

            # Filter
            filter_person = st.selectbox("Filter by person", ["All"] + roommates)

            filtered = expenses if filter_person == "All" else [e for e in expenses if e.paid_by == filter_person]

            # Display expenses
            for expense in reversed(filtered):
                with st.expander(f"${expense.amount:.2f} - {expense.description}"):
                    st.write(f"**Paid by:** {expense.paid_by}")
                    st.write(f"**Split with:** {', '.join(expense.split_with)}")
                    st.write(f"**Category:** {expense.category}")
                    st.write(f"**Date:** {datetime.fromisoformat(expense.date).strftime('%Y-%m-%d %H:%M')}")

                    if st.button(f"🗑️ Delete", key=f"del_{expense.id}"):
                        expenses.remove(expense)
                        save_expenses(expenses)
                        st.rerun()

            # Export
            st.divider()

            export_text = "EXPENSE REPORT\n" + "="*50 + "\n\n"
            for expense in expenses:
                export_text += f"{expense.date[:10]} | {expense.description} | ${expense.amount:.2f} | Paid by {expense.paid_by}\n"

            st.download_button(
                "📥 Download Report",
                data=export_text,
                file_name="expense_report.txt",
                mime="text/plain"
            )
        else:
            st.info("No expenses yet!")


if __name__ == "__main__":
    main()
