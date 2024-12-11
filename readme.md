🚗 Tesla Sentiment Dashboard

Analyze sentiment from live tweets about Tesla, Elon Musk, and related topics. This interactive dashboard fetches real-time tweets (or uses fallback mock data) to display sentiment trends, word clouds, and more!

✨ Features

	•	Live Sentiment Analysis:
	•	Fetch live tweets using the Twitter API and analyze sentiment (Positive, Neutral, Negative) with VADER.
	•	Fallback to Mock Data:
	•	If the API fails (e.g., due to rate limits), mock tweet data is loaded seamlessly.
	•	Comprehensive Visualizations:
	•	Pie Chart: Sentiment distribution.
	•	Line Chart: Sentiment trends over time.
	•	Histogram: Sentiment score distribution.
	•	Word Clouds: Frequently used words by sentiment.
	•	Bar Chart: Most common words.
	•	Scatter Plot: Sentiment by tweet popularity.
	•	Tweets per Day: Analyze tweet activity over time.

📊 How It Works

	1.	Input Query:
	•	Enter a search query (e.g., Tesla OR Elon Musk).
	•	Select the number of tweets to fetch (10–100).
	2.	Analyze Tweets:
	•	The app fetches live tweets via the Twitter API or loads mock data if the API fails.
	3.	Visualize Results:
	•	Sentiment trends, score distributions, word clouds, and more are displayed dynamically.

🛠️ Setup & Installation

To run this project locally or make modifications:
	1.	Clone the repository:

git clone https://huggingface.co/spaces/yourusername/tesla-sentiment-dashboard
cd tesla-sentiment-dashboard


	2.	Install the required Python dependencies:

pip install -r requirements.txt


	3.	Create a .env file in the project root and add your Twitter Bearer Token:

BEARER_TOKEN=your_bearer_token_here


	4.	Run the Streamlit app:

streamlit run app.py

🚀 Deployment on Hugging Face Spaces

To deploy this project to Hugging Face Spaces:
	1.	Upload Files:
	•	app.py: The main Streamlit application.
	•	requirements.txt: Dependencies file.
	•	.env (optional for local use, not recommended for production).
	•	mock_tweets.csv: Fallback data file.
	2.	Set Environment Secrets:
	•	Add the Bearer Token as a secret in the Hugging Face Space settings:
	•	Key: BEARER_TOKEN
	•	Value: your_bearer_token_here
	3.	Commit the changes, and your app will be live!

⚠️ Notes & Limitations

	1.	Cashtag Operator:
	•	The free/basic Twitter API tier does not support the $TSLA cashtag. Remove $ from queries to avoid errors.
	•	Default query: Tesla OR Elon Musk.
	2.	Rate Limits:
	•	Twitter API may restrict live tweet fetching if rate limits are exceeded. The app gracefully falls back to mock data in such cases.
	3.	Mock Data:
	•	Mock data (mock_tweets.csv) is included for testing and fallback purposes.

🖼️ Example Visualizations

	•	Sentiment Distribution:

	•	Word Cloud (Positive Tweets):

	•	Sentiment Trends Over Time:

📜 License

This project is licensed under the MIT License. Feel free to use, modify, and share it.

❤️ Acknowledgments

	•	Hugging Face Spaces for hosting the app.
	•	VADER Sentiment Analysis for sentiment scoring.
	•	Tweepy for interfacing with the Twitter API.

Feel free to modify this README to suit your preferences! Let me know if you’d like further help. 🚀
