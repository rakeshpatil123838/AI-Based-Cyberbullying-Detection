import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Analytics Dashboard")

st.write(
    "Visual insights from previous cyberbullying analyses."
)

FILE = "history/history.csv"

# =====================================================
# LOAD DATA
# =====================================================

if not os.path.exists(FILE):
    st.warning("No history available.")
    st.stop()

try:
    df = pd.read_csv(FILE)
except Exception:
    st.error("Unable to read history file.")
    st.stop()

if df.empty:
    st.warning("History is empty.")
    st.stop()

# =====================================================
# CLEAN DATA
# =====================================================

df["Prediction"] = df["Prediction"].astype(str).str.upper()

df["Confidence"] = pd.to_numeric(
    df["Confidence"],
    errors="coerce"
)

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

df["Day"] = df["Date"].dt.date

# =====================================================
# SUMMARY
# =====================================================

total = len(df)

toxic = len(df[df["Prediction"] == "TOXIC"])

safe = total - toxic

avg = round(df["Confidence"].mean(), 2)

col1, col2, col3, col4 = st.columns(4)

col1.metric("📨 Total Messages", total)

col2.metric("✅ Safe", safe)

col3.metric("🚫 Toxic", toxic)

col4.metric("🎯 Avg Confidence", f"{avg}%")

st.markdown("---")

# =====================================================
# DONUT CHART
# =====================================================

left, right = st.columns(2)

with left:

    pie = px.pie(
        names=["Safe", "Toxic"],
        values=[safe, toxic],
        hole=0.55,
        title="Safe vs Toxic"
    )

    st.plotly_chart(
        pie,
        use_container_width=True
    )

# =====================================================
# SEVERITY
# =====================================================

with right:

    sev = (
        df["Severity"]
        .value_counts()
        .reset_index()
    )

    sev.columns = [
        "Severity",
        "Count"
    ]

    fig = px.bar(
        sev,
        x="Severity",
        y="Count",
        color="Severity",
        text="Count",
        title="Severity Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")

# =====================================================
# SENTIMENT
# =====================================================

left, right = st.columns(2)

with left:

    sentiment = (
        df["Sentiment"]
        .value_counts()
        .reset_index()
    )

    sentiment.columns = [
        "Sentiment",
        "Count"
    ]

    fig = px.bar(
        sentiment,
        x="Sentiment",
        y="Count",
        color="Sentiment",
        text="Count",
        title="Sentiment Analysis"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# CONFIDENCE HISTOGRAM
# =====================================================

with right:

    fig = px.histogram(
        df,
        x="Confidence",
        nbins=15,
        title="Confidence Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")

# =====================================================
# DAILY ACTIVITY
# =====================================================

daily = (
    df.groupby("Day")
    .size()
    .reset_index(name="Messages")
)

fig = px.line(
    daily,
    x="Day",
    y="Messages",
    markers=True,
    title="Daily Analysis Activity"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# TOXIC VS SAFE BAR
# =====================================================

summary = pd.DataFrame({

    "Category": [

        "Safe",

        "Toxic"

    ],

    "Count": [

        safe,

        toxic

    ]

})

fig = px.bar(

    summary,

    x="Category",

    y="Count",

    color="Category",

    text="Count",

    title="Overall Detection Summary"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.markdown("---")

# =====================================================
# RECENT RECORDS
# =====================================================

st.subheader("📝 Recent Analyses")

st.dataframe(

    df.tail(10),

    use_container_width=True,

    height=350

)

# =====================================================
# DOWNLOAD
# =====================================================

csv = df.to_csv(index=False)

st.download_button(

    "📥 Download Analytics CSV",

    csv,

    file_name="analytics.csv",

    mime="text/csv"

)