# Sickafaitradingbotbishes
import cbpro
import openai
import os
import requests

# Ensure your OpenAI and NewsAPI keys are set in your environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
NEWSAPI_API_KEY = os.getenv("NEWSAPI_API_KEY")

class TradingBot:
    def __init__(self, api_key, api_secret, api_passphrase):
        self.client = cbpro.AuthenticatedClient(api_key, api_secret, api_passphrase)

    def fetch_latest_news(self):
        """
        Fetches the latest crypto news using NewsAPI.
        """
        url = f'https://newsapi.org/v2/everything?q=cryptocurrency&sortBy=publishedAt&apiKey={NEWSAPI_API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            news_data = response.json()
            # Extracting the title of the first news article as an example
            first_news_title = news_data['articles'][0]['title']
            return first_news_title
        else:
            print("Failed to fetch news")
            return None

    def analyze_sentiment_with_gpt(self, news_text):
        """
        Analyzes the sentiment of the given news text using OpenAI's GPT.
        """
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use the appropriate engine for your use case
            prompt=f"What is the sentiment of this text? Positive, Negative, or Neutral?\n\n\"{news_text}\"",
            max_tokens=60
        )
        sentiment = response.choices[0].text.strip().lower()
        print(f"News: {news_text}\nSentiment Analysis Result: {sentiment}")

        if "positive" in sentiment:
            return 0.7
        elif "negative" in sentiment:
            return -0.7
        else:
            return 0

    def decide_trade_action(self, sentiment_score):
        """
        Decides whether to buy, sell, or hold based on the sentiment score.
        """
        if sentiment_score > 0.5:
            return 'buy'
        elif sentiment_score < -0.5:
            return 'sell'
        else:
            return 'hold'

    def place_order(self, action, product_id='BTC-USD', amount='0.01'):
        """
        Places a buy or sell order on the Coinbase Pro market.
        """
        if action == 'buy':
            order = self.client.buy(price=None,  # Market order
                                    size=amount,  # Amount in BTC
                                    order_type='market',
                                    product_id=product_id)
        elif action == 'sell':
            order = self.client.sell(price=None,  # Market order
                                     size=amount,  # Amount in BTC
                                     order_type='market',
                                     product_id=product_id)
        else:
            print("Hold, no action taken.")
            return

        print(f"Order response: {order}")

def main():
    # Ensure your Coinbase Pro API credentials are set correctly
    api_key = 'YOUR_API_KEY'
    api_secret = 'YOUR_API_SECRET'
    api_passphrase = 'YOUR_API_PASSPHRASE'

    bot = TradingBot(api_key, api_secret, api_passphrase)
    
    # Fetching the latest cryptocurrency news
    latest_news = bot.fetch_latest_news()
    if latest_news:
        sentiment_score = bot.analyze_sentiment_with_gpt(latest_news)
        print("Sentiment score:", sentiment_score)

        action = bot.decide_trade_action(sentiment_score)
        print("Trade action decided:", action)

        # Place an order based on the sentiment analysis (for demonstration; adjust the logic as needed)
        bot.place_order(action)

if __name__ == "__main__":
    main()
