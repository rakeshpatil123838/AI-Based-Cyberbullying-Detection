import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="History",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Analysis History")

FILE = "history/history.csv"

# ====================================================
# LOAD DATA
# ====================================================

if not os.path.exists(FILE):

    st.warning("No history found.")

    st.stop()

try:

    df = pd.read_csv(FILE)

except Exception:

    st.error("Unable to read history file.")

    st.stop()

if df.empty:

    st.warning("History is empty.")

    st.stop()

# ====================================================
# FORMAT DATA
# ====================================================

df["Prediction"] = df["Prediction"].astype(str).str.upper()

df["Confidence"] = pd.to_numeric(
    df["Confidence"],
    errors="coerce"
)

# ====================================================
# SEARCH
# ====================================================

st.subheader("🔍 Search")

keyword = st.text_input(
    "Search by message..."
)

if keyword:

    df = df[
        df["Message"]
        .str.contains(
            keyword,
            case=False,
            na=False
        )
    ]

# ====================================================
# FILTER
# ====================================================

prediction_filter = st.selectbox(

    "Prediction",

    [

        "All",

        "SAFE",

        "TOXIC"

    ]

)

if prediction_filter != "All":

    df = df[
        df["Prediction"] == prediction_filter
    ]

# ====================================================
# SUMMARY
# ====================================================

total = len(df)

safe = len(
    df[df["Prediction"] == "SAFE"]
)

toxic = len(
    df[df["Prediction"] == "TOXIC"]
)

avg = round(
    df["Confidence"].mean(),
    2
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Messages",
    total
)

c2.metric(
    "Safe",
    safe
)

c3.metric(
    "Toxic",
    toxic
)

c4.metric(
    "Avg Confidence",
    f"{avg}%"
)

st.markdown("---")

# ====================================================
# TABLE
# ====================================================

st.subheader("📋 Analysis Records")

st.dataframe(

    df,

    use_container_width=True,

    height=500

)

# ====================================================
# DOWNLOAD
# ====================================================

csv = df.to_csv(index=False)

st.download_button(

    "📥 Download CSV",

    csv,

    file_name="history.csv",

    mime="text/csv"

)

# ====================================================
# DELETE HISTORY
# ====================================================

st.markdown("---")

st.subheader("🗑 Manage History")

with st.expander("Danger Zone"):

    st.warning(
        "Deleting history cannot be undone."
    )

    if st.button(
        "Delete Entire History"
    ):

        empty = pd.DataFrame(columns=[

            "Date",

            "Message",

            "Prediction",

            "Confidence",

            "Severity",

            "Sentiment"

        ])

        empty.to_csv(
            FILE,
            index=False
        )

        st.success(
            "History deleted successfully."
        )

        st.rerun()