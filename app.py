import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from datetime import datetime
from utils import analyze_text, save_history

# --------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------

st.set_page_config(
    page_title="AI-Based Cyberbullying Detection Tool",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------------
# LOAD CSS
# --------------------------------------------------------

def load_css():
    if os.path.exists("style.css"):
        with open("style.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )

load_css()

# --------------------------------------------------------
# SIDEBAR
# --------------------------------------------------------

with st.sidebar:

    if os.path.exists("assets/logo.png"):
        st.image("assets/logo.png", width=180)

    st.markdown("## 🛡 AI Status")

    st.success("Model Online")

    st.info("Toxic-BERT")

    st.markdown("---")

    st.markdown("### Technologies")

    st.write("✔ Streamlit")
    st.write("✔ Hugging Face")
    st.write("✔ Transformers")
    st.write("✔ PyTorch")
    st.write("✔ Plotly")

    st.markdown("---")

    st.caption("Version 2.0")

# --------------------------------------------------------
# HISTORY STATS
# --------------------------------------------------------

total = 0
safe = 0
toxic = 0
avg_conf = 0

history_file = "history/history.csv"

if os.path.exists(history_file):

    try:

        df = pd.read_csv(history_file)

        if len(df):

            total = len(df)

            toxic = len(
                df[df["Prediction"].str.upper() == "TOXIC"]
            )

            safe = total - toxic

            avg_conf = df["Confidence"].mean()

    except:
        pass

# --------------------------------------------------------
# HERO
# --------------------------------------------------------

st.markdown("""
# 🛡 AI-Based Cyberbullying Detection Tool

### Intelligent Online Content Moderation

Detect cyberbullying, toxic language, harassment,
hate speech and offensive content using Artificial Intelligence.
""")

st.markdown("---")

# --------------------------------------------------------
# LIVE METRICS
# --------------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric("📨 Messages", total)

c2.metric("✅ Safe", safe)

c3.metric("🚫 Toxic", toxic)

c4.metric(
    "🎯 Avg Confidence",
    f"{avg_conf:.1f}%"
)

st.markdown("---")

# --------------------------------------------------------
# USER INPUT
# --------------------------------------------------------

st.subheader("💬 Analyze Message")

message = st.text_area(

    "",

    height=170,

    placeholder="Enter any message..."

)

analyze = st.button(
    "🔍 Analyze",
    use_container_width=True
)

# --------------------------------------------------------
# ANALYSIS
# --------------------------------------------------------

if analyze:

    if message.strip() == "":

        st.warning("Please enter a message.")

    else:

        with st.spinner("🤖 AI is analyzing..."):

            result = analyze_text(message)

        prediction = result["prediction"]

        confidence = result["confidence"]

        severity = result["severity"]

        sentiment = result["sentiment"]

        recommendation = result["recommendation"]

        save_history(message, result)

        st.markdown("---")

        st.subheader("📊 AI Report")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Prediction",
            prediction
        )

        col2.metric(
            "Confidence",
            f"{confidence:.2f}%"
        )

        col3.metric(
            "Severity",
            severity
        )

        col4.metric(
            "Sentiment",
            sentiment
        )

        st.markdown("---")

        # ==========================================
        # Confidence Gauge
        # ==========================================

        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=confidence ,
            number={"suffix": "%"},
            title={"text": "AI Confidence"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#2563EB"},
                "steps": [
                    {"range": [0, 50], "color": "#22C55E"},
                    {"range": [50, 80], "color": "#F59E0B"},
                    {"range": [80, 100], "color": "#EF4444"},
                ]
            }
        ))

        st.plotly_chart(
            gauge,
            use_container_width=True
        )

        # ==========================================
        # Prediction Card
        # ==========================================

        if prediction.upper() == "TOXIC":

            st.error("🚫 TOXIC MESSAGE DETECTED")

        else:

            st.success("✅ SAFE MESSAGE")

        # ==========================================
        # AI Explanation
        # ==========================================

        st.subheader("🤖 AI Explanation")

        st.info(result["explanation"])

        # ==========================================
        # Original Message
        # ==========================================

        st.subheader("📝 Original Message")

        toxic_words = [
            "idiot",
            "stupid",
            "loser",
            "worthless",
            "hate",
            "ugly",
            "fool",
            "dumb",
            "moron",
            "pathetic"
        ]

        import re

        highlighted = message

       for word in toxic_words:
           highlighted = re.sub(
               rf"\b({re.escape(word)})\b",
               r"🔴 **\1**",
               highlighted,
               flags=re.IGNORECASE
          )

        st.markdown(highlighted)

        # ==========================================
        # Recommendation
        # ==========================================

        st.subheader("💡 AI Recommendation")

        st.info(recommendation)

        # ==========================================
        # Download Report
        # ==========================================

        report = f"""
AI-Based Cyberbullying Detection Report

-------------------------------------

Message

{message}

-------------------------------------

Prediction

{prediction}

Confidence

{confidence:.2f} %

Severity

{severity}

Sentiment

{sentiment}

Recommendation

{recommendation}
"""

        st.download_button(
            "📥 Download Report",
            report,
            file_name="AI_Report.txt"
        )

# ==========================================
# Workflow
# ==========================================

st.markdown("---")

st.header("⚙ AI Workflow")

st.markdown("""
```text
User Message
      │
      ▼
Text Preprocessing
      │
      ▼
Toxic-BERT Model
      │
      ▼
Sentiment Analysis
      │
      ▼
Severity Calculation
      │
      ▼
Prediction
      │
      ▼
History Storage
      │
      ▼
Analytics Dashboard

""")

# ==========================================
# Recent History
# ==========================================

if os.path.exists(history_file):

    try:

        df = pd.read_csv(history_file)

        if len(df):

            st.markdown("---")

            st.subheader("🕒 Recent Analyses")

            st.dataframe(
                df.tail(5),
                use_container_width=True
            )

    except Exception:
        pass


# ==========================================
# Footer
# ==========================================

st.markdown("---")

st.caption(
    "© 2026 AI-Based Cyberbullying Detection Tool | Powered by Streamlit, Hugging Face Transformers and PyTorch"
)
