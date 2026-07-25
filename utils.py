import re
import streamlit as st
import pandas as pd
import os

from datetime import datetime
from transformers import pipeline

# ============================================================
# LOAD MODELS
# ============================================================

@st.cache_resource
def load_models():

    toxic = pipeline(
        "text-classification",
        model="unitary/toxic-bert",
        truncation=True
    )

    sentiment = pipeline(
        "sentiment-analysis"
    )

    return toxic, sentiment


toxic_model, sentiment_model = load_models()

# ============================================================
# TOXIC WORD LIST
# ============================================================

TOXIC_WORDS = [

    "idiot",
    "stupid",
    "moron",
    "loser",
    "worthless",
    "hate",
    "ugly",
    "pathetic",
    "dumb",
    "fool",
    "trash",
    "garbage",
    "kill",
    "die",
    "useless",
    "disgusting"

]

# ============================================================
# FIND TOXIC WORDS
# ============================================================

def extract_keywords(text):

    found = []

    lower = text.lower()

    for word in TOXIC_WORDS:

        if re.search(r"\b"+re.escape(word)+r"\b", lower):

            found.append(word)

    return found

# ============================================================
# SEVERITY
# ============================================================

def get_severity(score):

    if score >= 0.95:

        return "Critical 🔴"

    elif score >= 0.85:

        return "High 🟠"

    elif score >= 0.70:

        return "Medium 🟡"

    else:

        return "Low 🟢"

# ============================================================
# RECOMMENDATION
# ============================================================

def get_recommendation(prediction):

    if prediction == "TOXIC":

        return """
• Avoid offensive language.

• Respect other users.

• Think before posting.

• Use constructive criticism.

• Encourage positive conversations.
"""

    return """
The message appears respectful.

No harmful language detected.
"""

# ============================================================
# EXPLANATION
# ============================================================

def get_explanation(prediction, keywords):

    if prediction == "TOXIC":

        if len(keywords):

            return (
                "The prediction is based on offensive "
                "language detected in the message.\n\n"
                f"Detected keywords: {', '.join(keywords)}"
            )

        return (
            "The model detected language patterns commonly "
            "associated with insults, harassment, or abusive content."
        )

    return (
        "The model did not detect patterns associated with "
        "cyberbullying or toxic language."
    )

# ============================================================
# ANALYZE
# ============================================================

def analyze_text(text):

    toxic = toxic_model(text)[0]

    sentiment = sentiment_model(text)[0]

    label = toxic["label"].upper()

    score = float(toxic["score"])

    # Normalize prediction
    if "TOXIC" in label:

        prediction = "TOXIC"

    else:

        prediction = "SAFE"

    keywords = extract_keywords(text)

    severity = get_severity(score)

    recommendation = get_recommendation(prediction)

    explanation = get_explanation(
        prediction,
        keywords
    )

    return {

        "prediction": prediction,

        "confidence": score,

        "severity": severity,

        "sentiment": sentiment["label"],

        "keywords": keywords,

        "recommendation": recommendation,

        "explanation": explanation

    }

# ============================================================
# SAVE HISTORY
# ============================================================

def save_history(message, result):

    os.makedirs("history", exist_ok=True)

    file = "history/history.csv"

    row = pd.DataFrame([{

        "Date":
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "Message":
        message,

        "Prediction":
        result["prediction"],

        "Confidence":
        round(result["confidence"] * 100, 2),

        "Severity":
        result["severity"],

        "Sentiment":
        result["sentiment"]

    }])

    if os.path.exists(file):

        try:

            old = pd.read_csv(file)

            df = pd.concat(
                [old, row],
                ignore_index=True
            )

        except:

            df = row

    else:

        df = row

    df.to_csv(file, index=False)

# ============================================================
# LOAD HISTORY
# ============================================================

def load_history():

    file = "history/history.csv"

    if not os.path.exists(file):

        return pd.DataFrame(columns=[

            "Date",

            "Message",

            "Prediction",

            "Confidence",

            "Severity",

            "Sentiment"

        ])

    return pd.read_csv(file)

# ============================================================
# DASHBOARD STATS
# ============================================================

def dashboard_stats():

    df = load_history()

    if df.empty:

        return {

            "total": 0,

            "safe": 0,

            "toxic": 0,

            "average": 0

        }

    total = len(df)

    toxic = len(

        df[df["Prediction"] == "TOXIC"]

    )

    safe = total - toxic

    average = round(

        df["Confidence"].mean(),

        2

    )

    return {

        "total": total,

        "safe": safe,

        "toxic": toxic,

        "average": average

    }