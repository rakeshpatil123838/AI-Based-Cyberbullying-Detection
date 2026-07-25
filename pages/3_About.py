import streamlit as st

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide"
)

# =========================================================
# HEADER
# =========================================================

st.title("🛡 About AI-Based Cyberbullying Detection Tool")

st.markdown("""
Welcome to the **AI-Based Cyberbullying Detection Tool**, an intelligent web
application that detects harmful, abusive, and toxic language using
Artificial Intelligence and Natural Language Processing (NLP).

The system is designed to help create safer online communities by identifying
cyberbullying in real time.
""")

st.markdown("---")

# =========================================================
# PROJECT OVERVIEW
# =========================================================

st.header("📖 Project Overview")

st.info("""
This application uses a Transformer-based AI model to analyze user messages.

The AI predicts whether the message is:

• ✅ Safe

• 🚫 Toxic

It also performs:

• 😊 Sentiment Analysis

• ⚠️ Severity Prediction

• 📊 Confidence Scoring

• 💾 History Storage

• 📈 Analytics Visualization
""")

st.markdown("---")

# =========================================================
# SYSTEM WORKFLOW
# =========================================================

st.header("⚙️ System Workflow")

st.code("""
User Input
     │
     ▼
Text Preprocessing
     │
     ▼
Transformer AI Model
     │
     ▼
Toxicity Detection
     │
     ▼
Sentiment Analysis
     │
     ▼
Severity Calculation
     │
     ▼
Store Result
     │
     ▼
Analytics Dashboard
""")

st.markdown("---")

# =========================================================
# FEATURES
# =========================================================

st.header("✨ Key Features")

col1, col2 = st.columns(2)

with col1:

    st.success("""
✔ AI Toxicity Detection

✔ Cyberbullying Detection

✔ Sentiment Analysis

✔ Severity Level

✔ Confidence Score
""")

with col2:

    st.success("""
✔ Analytics Dashboard

✔ Search History

✔ CSV Export

✔ Modern User Interface

✔ Real-Time Detection
""")

st.markdown("---")

# =========================================================
# TECHNOLOGY STACK
# =========================================================

st.header("🛠 Technology Stack")

tech = {
    "Programming Language": "Python",
    "Framework": "Streamlit",
    "AI Library": "Hugging Face Transformers",
    "Deep Learning": "PyTorch",
    "Data Processing": "Pandas",
    "Visualization": "Plotly",
    "Machine Learning": "Transformer Models"
}

for key, value in tech.items():
    st.write(f"**{key}:** {value}")

st.markdown("---")

# =========================================================
# AI MODEL
# =========================================================

st.header("🤖 AI Model")

st.info("""
**Model Used**

unitary/toxic-bert

This Transformer model detects:

• Toxic Language

• Insults

• Threats

• Hate Speech

• Offensive Content

It is powered by Hugging Face Transformers.
""")

st.markdown("---")

# =========================================================
# APPLICATIONS
# =========================================================

st.header("🌍 Applications")

apps = [

    "Social Media Platforms",

    "Educational Institutions",

    "Discussion Forums",

    "Online Gaming",

    "Corporate Communication",

    "Community Moderation",

    "Chat Applications",

    "Content Moderation Systems"

]

for app in apps:
    st.write("✅", app)

st.markdown("---")

# =========================================================
# FUTURE ENHANCEMENTS
# =========================================================

st.header("🚀 Future Scope")

future = [

    "Multilingual Detection",

    "Voice Chat Analysis",

    "Image Cyberbullying Detection",

    "Video Comment Analysis",

    "Emotion Recognition",

    "Live Moderation",

    "Cloud Deployment",

    "Mobile Application",

    "Admin Dashboard"

]

for item in future:
    st.write("🔹", item)

st.markdown("---")

# =========================================================
# DEVELOPER
# =========================================================

st.header("👨‍💻 Developer")

st.markdown("""
**Project:** AI-Based Cyberbullying Detection Tool

**Domain:** Artificial Intelligence & NLP

**Framework:** Streamlit

**Purpose:** VTU Mini Project

**Version:** 2.0
""")

st.markdown("---")

# =========================================================
# DISCLAIMER
# =========================================================

st.warning("""
This application is intended for educational and research purposes.

AI predictions may occasionally produce false positives or false negatives.
Human moderation should always be used for important decisions.
""")

st.markdown("---")

# =========================================================
# FOOTER
# =========================================================

st.success("Thank you for using the AI-Based Cyberbullying Detection Tool!")

st.caption("© 2026 AI-Based Cyberbullying Detection Tool | Built with ❤️ using Streamlit and Hugging Face")