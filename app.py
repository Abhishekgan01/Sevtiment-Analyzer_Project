import streamlit as st
from pymongo import MongoClient
from textblob import TextBlob
from datetime import datetime

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/") 
db = client["feedback_db"]  # Database
feedback_collection = db["feedback"]  # Collection

# Function to analyze sentiment
def analyze_sentiment(feedback_text):
    blob = TextBlob(feedback_text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Streamlit UI
st.title("Feedback Sentiment Analyzer")

# Input form for user feedback
st.header("Submit Feedback")
user_name = st.text_input("Your Name")
feedback_text = st.text_area("Your Feedback")

if st.button("Submit"):
    if user_name and feedback_text:
        sentiment = analyze_sentiment(feedback_text)
        feedback = {
            "user_name": user_name,
            "feedback_text": feedback_text,
            "sentiment": sentiment,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        feedback_collection.insert_one(feedback)
        st.success(f"Feedback submitted! Sentiment: {sentiment}")
    else:
        st.error("Please provide both name and feedback.")

# Display all feedback
st.header("View Submitted Feedback")
feedback_list = list(feedback_collection.find({}))

if feedback_list:
    for feedback in feedback_list:
        st.subheader(feedback["user_name"])
        st.write(f"Feedback: {feedback['feedback_text']}")
        st.write(f"Sentiment: {feedback['sentiment']}")
        st.write(f"Submitted on: {feedback['timestamp']}")
        st.write("---")  # Separator
else:
    st.info("No feedback submitted yet.")

# Option to delete all feedback
if st.button("Delete All Feedback"):
    feedback_collection.delete_many({})
    st.warning("All feedback deleted.")