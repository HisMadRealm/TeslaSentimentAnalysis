import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import tweepy
import re
from collections import Counter
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Authenticate with the Twitter API
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Path to the mock tweets file
MOCK_TWEETS_FILE = "mock_tweets.csv"

# Helper functions
def clean_text(text):
    """Clean tweet text by removing URLs, mentions, hashtags, and special characters."""
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
    text = re.sub(r"@\w+|#\w+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = text.lower()
    return text

def analyze_sentiment(text):
    """Analyze sentiment using VADER and return sentiment score and label."""
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(text)["compound"]
    if score >= 0.05:
        sentiment = "Positive"
    elif score <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    return score, sentiment

def fetch_tweets(query, max_results=100):
    """Fetch tweets using Twitter API with Bearer Token."""
    try:
        response = client.search_recent_tweets(
            query=query,
            max_results=max_results,
            tweet_fields=["created_at", "text"],
        )
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error fetching tweets from the API: {e}")
        return []

def load_mock_data():
    """Load mock tweets from a CSV file."""
    if os.path.exists(MOCK_TWEETS_FILE):
        st.warning("Using fallback mock tweets data.")
        try:
            df = pd.read_csv(MOCK_TWEETS_FILE)
            st.write("Loaded mock data:", df.head())  # Debugging: Display mock data
            if "text" not in df.columns:
                st.error("Mock data file is missing the 'text' column.")
                return pd.DataFrame()
            return df
        except Exception as e:
            st.error(f"Error reading mock data file: {e}")
            return pd.DataFrame()
    else:
        st.error(f"Mock tweets file '{MOCK_TWEETS_FILE}' not found.")
        return pd.DataFrame()

def process_tweets(df):
    """Process tweets into a DataFrame."""
    st.info("Processing tweets for sentiment analysis...")
    df["cleaned_text"] = df["text"].apply(clean_text)
    df["sentiment_score"] = df["cleaned_text"].apply(lambda x: analyze_sentiment(x)[0])
    df["sentiment"] = df["cleaned_text"].apply(lambda x: analyze_sentiment(x)[1])
    st.write("Processed DataFrame:", df.head())  # Debugging: Display processed DataFrame
    return df

# Streamlit UI
st.title("Tesla Sentiment Dashboard")
st.markdown("Analyze sentiment from live tweets about Tesla and Elon Musk.")

# Input form
query = st.text_input("Enter search query (e.g., Tesla OR Elon Musk):", "Tesla OR Elon Musk OR $TSLA")
max_results = st.slider("Number of tweets to fetch:", min_value=10, max_value=100, value=50)

if st.button("Fetch and Analyze Tweets"):
    # Fetch tweets from API
    tweets = fetch_tweets(query, max_results)

    # Check if tweets were fetched; if not, load fallback data
    if not tweets:
        st.warning("No tweets fetched from the API. Loading fallback mock tweets.")
        tweet_df = load_mock_data()
        if not tweet_df.empty:
            st.info("Processing fallback mock tweets...")
            tweet_df = process_tweets(tweet_df)
    else:
        st.info("Processing live tweets from the API...")
        tweet_df = pd.DataFrame([
            {
                "id": tweet.id,
                "text": tweet.text,
                "created_at": tweet.created_at,
            } for tweet in tweets
        ])
        tweet_df = process_tweets(tweet_df)

    if not tweet_df.empty:
        # Display processed data
        st.subheader("Processed Data")
        st.write(tweet_df)

        # Sentiment Distribution (Pie Chart)
        st.subheader("Sentiment Distribution")
        if "sentiment" in tweet_df.columns:
            sentiment_counts = tweet_df["sentiment"].value_counts()
            fig, ax = plt.subplots()
            sentiment_counts.plot(kind="pie", autopct="%1.1f%%", startangle=90, ax=ax)
            ax.set_ylabel("")
            ax.set_title("Sentiment Distribution")
            st.pyplot(fig)

        # Sentiment Trends Over Time (Line Chart)
        st.subheader("Sentiment Trends Over Time")
        if "created_at" in tweet_df.columns:
            tweet_df["created_at"] = pd.to_datetime(tweet_df["created_at"])
            trends = tweet_df.groupby([tweet_df["created_at"].dt.date, "sentiment"]).size().unstack(fill_value=0)
            fig, ax = plt.subplots(figsize=(10, 5))
            trends.plot(ax=ax, marker="o")
            ax.set_title("Sentiment Trends Over Time")
            ax.set_xlabel("Date")
            ax.set_ylabel("Tweet Count")
            st.pyplot(fig)

        # Sentiment Score Distribution (Histogram)
        st.subheader("Sentiment Score Distribution")
        if "sentiment_score" in tweet_df.columns:
            fig, ax = plt.subplots()
            tweet_df["sentiment_score"].plot(kind="hist", bins=20, ax=ax, edgecolor="black")
            ax.set_title("Sentiment Score Distribution")
            ax.set_xlabel("Sentiment Score")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)

        # Word Clouds by Sentiment
        st.subheader("Word Clouds by Sentiment")
        for sentiment in ["Positive", "Neutral", "Negative"]:
            sentiment_text = " ".join(tweet_df[tweet_df["sentiment"] == sentiment]["cleaned_text"].tolist())
            if sentiment_text:
                wordcloud = WordCloud(width=800, height=400, background_color="white").generate(sentiment_text)
                st.image(wordcloud.to_array(), caption=f"Word Cloud - {sentiment} Tweets")

        # Most Common Words (Bar Chart)
        st.subheader("Most Common Words")
        all_words = " ".join(tweet_df["cleaned_text"].tolist()).split()
        common_words = pd.DataFrame(Counter(all_words).most_common(10), columns=["Word", "Frequency"])
        fig, ax = plt.subplots(figsize=(10, 5))
        common_words.plot(kind="bar", x="Word", y="Frequency", ax=ax, legend=False)
        ax.set_title("Most Common Words in Tweets")
        ax.set_xlabel("Word")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
    else:
        st.warning("No valid data for sentiment analysis.")
