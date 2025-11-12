import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# ====================== PAGE CONFIG ======================
st.set_page_config(page_title="Expense Splitter", layout="wide", page_icon="moneybag")

# ====================== BLACK & WHITE THEME ======================
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: #ffffff;
        color: #000000;
    }

    /* Sidebar */
    .css-1d391kg {
        background: #f0f0f0;
    }

    /* Headers */
    h1, h2, h3 {
        color: #000000 !important;
        font-family: 'Helvetica', sans-serif;
    }

    /* Input boxes */
    .stTextInput > div > div > input {
        border: 2px solid #000000;
        border-radius: 8px;
        padding: 10px;
        font-weight: 500;
    }

    /* Buttons */
    .stButton > button {
        background: #000000;
        color: #ffffff;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        border: 2px solid #000000;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background: #333333;
        border: 2px solid #333333;
    }

    /* Dataframes */
    .dataframe {
        border: 2px solid #000;
        border-radius: 8px;
    }

    /* Success message */
    .stSuccess {
        background: #000;
        color: #fff;
        padding: 15px;
        border-radius: 10px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ====================== TITLE & ICONS ======================
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <h1 style='font-size: 48px; margin:0;'>Expense Splitter</h1>
    <p style='font-size: 20px; color: #555; margin:5px 0 20px;'>Split bills fairly • Track who owes whom</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ====================== SESSION STATE INIT ======================
if 'people' not in st.session_state:
    st.session_state.people = []
if 'expenses' not in st.session_state:
    st.session_state.expenses = []
if 'df_expenses' not in st.session_state:
    st.session_state.df_expenses = pd.DataFrame(columns=['Paid By', 'Amount', 'Description', 'Date', 'Split Among'])

# ====================== SIDEBAR: ADD PEOPLE ======================
with st.sidebar:
    st.header("Manage Participants")
    new_person = st.text_input("Add Person", placeholder="e.g. Alex")
    if st.button("Add Person"):
        if new_person.strip() and new_person.strip() not in st.session_state.people:
            st.session_state.people.append(new_person.strip())
            st.success(f"{new_person.strip()} added!")
        elif new_person.strip() in st.session_state.people:
            st.warning("Person already exists!")
    
    st.markdown("---")
    st.subheader("Current Participants")
    if st.session_state.people:
        for i, person in enumerate(st.session_state.people):
            col1, col2 = st.columns([3, 1])
            col1.write(f"**{person}**")
            if col2.button("Remove", key=f"rm_{i}"):
                st.session_state.people.pop(i)
                st.rerun()
    else:
        st.info("No participants yet.")

# ====================== MAIN: ADD EXPENSE ======================
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Add New Expense")
    with st.form("expense_form", clear_on_submit=True):
        paid_by = st.selectbox("Paid By", options=st.session_state.people, index=None, placeholder="Select payer")
        amount = st.number_input("Amount (₹)", min_value=0.01, step=0.01, format="%.2f")
        desc = st.text_input("Description", placeholder="e.g. Dinner at BBQ Nation")
        split_among = st.multiselect("Split Among", options=st.session_state.people, default=st.session_state.people)

        submitted = st.form_submit_button("Add Expense")

        if submitted:
            if not paid_by or not split_among:
                st.error("Select payer and at least one person to split!")
            elif amount <= 0:
                st.error("Amount must be positive!")
            else:
                new_expense = {
                    "Paid By": paid_by,
                    "Amount": amount,
                    "Description": desc,
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Split Among": ", ".join(split_among)
                }
                st.session_state.expenses.append(new_expense)
                new_df = pd.DataFrame([new_expense])
                st.session_state.df_expenses = pd.concat([st.session_state.df_expenses, new_df], ignore_index=True)
                st.success(f"Expense of ₹{amount:.2f} added!")
                st.balloons()

with col2:
    st.subheader("Recent Expenses")
    if not st.session_state.df_expenses.empty:
        display_df = st.session_state.df_expenses.copy()
        display_df["Amount"] = display_df["Amount"].apply(lambda x: f"₹{x:,.2f}")
        st.dataframe(display_df[["Paid By", "Amount", "Description", "Date"]], use_container_width=True)
    else:
        st.info("No expenses added yet.")

# ====================== CALCULATE SPLIT ======================
if st.session_state.people and st.session_state.expenses:
    st.markdown("---")
    st.subheader("Balance Summary")

    # Calculate total spent per person
    total_spent = {p: 0.0 for p in st.session_state.people}
    for exp in st.session_state.expenses:
        total_spent[exp["Paid By"]] += exp["Amount"]

    # Calculate per person share
    total_amount = sum(total_spent.values())
    n = len(st.session_state.people)
    per_person = total_amount / n if n > 0 else 0

    # Calculate net balance
    balance = {p: total_spent[p] - per_person for p in st.session_state.people}

    # Prepare transactions (who owes whom)
    creditors = {k: v for k, v in balance.items() if v > 0.01}
    debtors = {k: -v for k, v in balance.items() if v < -0.01}

    transactions = []
    for debtor, owes in debtors.items():
        for creditor, owed in creditors.items():
            if owes > 0 and owed > 0:
                transfer = min(owes, owed)
                transactions.append({
                    "From": debtor,
                    "To": creditor,
                    "Amount": transfer
                })
                debtors[debtor] -= transfer
                owes -= transfer
                creditors[creditor] -= transfer
                owed -= transfer
                if owes <= 0.01:
                    break
        if owes <= 0.01:
            continue

    # Display results
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### Net Balance")
        balance_df = pd.DataFrame([
            {"Person": p, "Balance": f"₹{b:,.2f}" if b >= 0 else f"-₹{-b:,.2f}"}
            for p, b in balance.items()
        ])
        st.dataframe(balance_df, use_container_width=True, hide_index=True)

    with col_b:
        st.markdown("#### Transactions")
        if transactions:
            trans_df = pd.DataFrame(transactions)
            trans_df["Amount"] = trans_df["Amount"].apply(lambda x: f"₹{x:,.2f}")
            st.dataframe(trans_df, use_container_width=True, hide_index=True)
        else:
            st.success("All settled!")

    # ====================== BAR CHART ======================
    st.markdown("---")
    st.subheader("Spending Overview")

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#000000' if x >= 0 else '#888888' for x in balance.values()]
    bars = ax.bar(balance.keys(), balance.values(), color=colors, edgecolor='black', linewidth=1.5)
    ax.set_ylabel("Net Balance (₹)", fontsize=12, fontweight='bold')
    ax.set_title("Who Owes / Is Owed", fontsize=16, fontweight='bold', pad=20)
    ax.axhline(0, color='black', linewidth=1)
    ax.grid(True, axis='y', linestyle='--', alpha=0.3)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + (0.01 if height >= 0 else -0.01),
                f'₹{abs(height):.2f}', ha='center', va='bottom' if height >= 0 else 'top',
                fontweight='bold', fontsize=10)

    st.pyplot(fig)

    # ====================== TOTAL SPENT CHART ======================
    st.markdown("#### Total Spent by Each Person")
    spent_df = pd.DataFrame(list(total_spent.items()), columns=['Person', 'Spent'])
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=spent_df, x='Person', y='Spent', palette='Greys', ax=ax2)
    ax2.set_ylabel("Amount (₹)")
    ax2.set_title("Total Amount Paid")
    for i, v in enumerate(spent_df['Spent']):
        ax2.text(i, v + 0.01, f"₹{v:,.2f}", ha='center', fontweight='bold')
    st.pyplot(fig2)

    # ====================== DOWNLOAD RESULTS ======================
    result_df = pd.DataFrame([
        {"Person": p, "Total Paid": total_spent[p], "Should Pay": per_person, "Net": balance[p]}
        for p in st.session_state.people
    ])
    csv = result_df.to_csv(index=False).encode()
    st.download_button(
        "Download Summary (CSV)",
        csv,
        "expense_summary.csv",
        "text/csv",
        help="Download full balance report"
    )

else:
    st.info("Add participants and expenses to see the split!")

# ====================== FOOTER ======================
st.markdown("""
---
<div style='text-align: center; padding: 20px; color: #666; font-size: 14px;'>
    Made with <span style='color: #000;'>Streamlit</span> • 
    Black & White Minimal Design
</div>
""", unsafe_allow_html=True)
