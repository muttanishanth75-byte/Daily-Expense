
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# PAGE SETTINGS
# =========================
st.set_page_config(
    page_title="Daily Expense",
    layout="centered"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

.stApp {
    background:
    linear-gradient(
        rgba(255,255,255,0.88),
        rgba(255,255,255,0.88)
    ),
    url("https://images.unsplash.com/photo-1554224155-6726b3ff858f");
    
    background-size: cover;
    background-position: center;
}

.main-heading{
    color:#1e293b;
    font-size:65px;
    font-weight:800;
    text-align:center;
    letter-spacing:-2px;
    margin-bottom:0px;
}

.brand-name{
    color:#3b82f6;
    font-size:12px;
    font-weight:800;
    letter-spacing:5px;
    text-align:center;
    text-transform:uppercase;
}

div.stButton > button{
    background-color:#1e293b;
    color:white;
    border:none;
    border-radius:12px;
    height:55px;
    font-weight:bold;
}

div.stButton > button:hover{
    background-color:#334155;
}

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.title("⚙️ Settings")

    if st.button("🗑️ Reset All Data"):
        st.session_state["expenses"] = []
        st.success("All data cleared!")
        st.rerun()

# =========================
# HEADING
# =========================
st.markdown(
    '<p class="brand-name">MUTTA NISHANTH PRESENTS</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="main-heading">DAILY   EXPENSE</p>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style='text-align:center;
              color:#334155;
              font-size:18px;
              font-weight:600;'>
    Your Path to Financial Freedom
    </p>
    """,
    unsafe_allow_html=True
)

# =========================
# SESSION STATE
# =========================
if "expenses" not in st.session_state:
    st.session_state["expenses"] = []

st.write("")

# =========================
# INPUT SECTION
# =========================
col1, col2 = st.columns(2)

with col1:
    amt = st.number_input(
        "Amount (₹)",
        min_value=0,
        step=100
    )

    cat = st.selectbox(
        "Category",
        [
            "🍔 Food",
            "🚗 Travel",
            "🛍️ Shopping",
            "💡 Bills",
            "💊 Health",
            "✨ Other"
        ]
    )

with col2:
    note = st.text_input(
        "Note",
        placeholder="Example: Coffee"
    )

    date = st.date_input("Date")

# =========================
# ADD EXPENSE
# =========================
if st.button(
    "LOG TRANSACTION",
    use_container_width=True
):

    if amt > 0:

        st.session_state["expenses"].append({
            "Date": date,
            "Category": cat,
            "Amount": amt,
            "Note": note
        })

        st.success("Expense Saved Successfully!")

# =========================
# ANALYTICS
# =========================
if st.session_state["expenses"]:

    df = pd.DataFrame(
        st.session_state["expenses"]
    )

    st.divider()

    # DOWNLOAD CSV
    csv = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "📥 Download Expense Report",
        csv,
        "daily_expenses.csv",
        "text/csv",
        use_container_width=True
    )

    st.divider()

    colA, colB = st.columns([1, 2])

    with colA:

        st.metric(
            "TOTAL SPENT",
            f"₹{df['Amount'].sum():,.0f}"
        )

        st.dataframe(
            df[["Category", "Amount"]],
            hide_index=True,
            use_container_width=True
        )

    with colB:

        chart_data = (
            df.groupby("Category")["Amount"]
            .sum()
        )

        fig, ax = plt.subplots(
            figsize=(5, 5)
        )

        colors = [
            "#fde047",
            "#94a3b8",
            "#cbd5e1",
            "#475569",
            "#1e293b",
            "#64748b"
        ]

        ax.pie(
            chart_data,
            labels=chart_data.index,
            autopct="%1.1f%%",
            startangle=140,
            colors=colors
        )

        ax.set_title("Expense Breakdown")

        st.pyplot(fig)

# =========================
# TRANSACTION LOGS
# =========================
if st.session_state["expenses"]:

    st.divider()

    st.subheader("📝 Transaction Logs")

    df = pd.DataFrame(
        st.session_state["expenses"]
    )

    display_df = df.copy()

    display_df.insert(
        0,
        "Delete",
        False
    )

    edited_df = st.data_editor(
        display_df,
        hide_index=True,
        use_container_width=True,
        key="expense_editor"
    )

    if st.button(
        "🗑️ Delete Selected Transactions",
        use_container_width=True
    ):

        remaining_rows = edited_df[
            edited_df["Delete"] == False
        ]

        remaining_rows = remaining_rows.drop(
            columns=["Delete"]
        )

        st.session_state["expenses"] = (
            remaining_rows.to_dict(
                "records"
            )
        )

        st.success(
            "Selected transactions deleted!"
        )

        st.rerun()

