import os
import google.generativeai as genai
import yfinance as yf
import requests
import feedparser
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key='#PUT YOUR OWN IT IS 100% FREE')

# Create the model
generation_config = {
  "temperature": 2,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
generation_config_2 = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash",
  generation_config=generation_config,
  #system_instruction="You are a financial proffesional, not an AI chat bot.",
  system_instruction="No instructions"
)
model_2 = genai.GenerativeModel(
  model_name="gemini-2.0-flash",
  generation_config=generation_config_2,
  system_instruction="Find the ticker of the company, if you cannot find the ticker, respond with just the letter x, also do not add the",
)

chat_session = model.start_chat(
    history=[
    ]
  ) 

what_stock = model_2.start_chat(
    history = []
)





dont_run = False
fortune_500_top_100 = input("Enter Stock Name or Ticker: ")

query = f"{fortune_500_top_100}+stock+market"    #Some models cannot access recent news, here it can using scrapers
rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
feed = feedparser.parse(rss_url)

news_list = []

for entry in feed.entries[:50]:  # Get the latest 50 articles
    article_url = entry.link
    response = requests.get(article_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Step 2: Try extracting the article content
    paragraphs = soup.find_all("p")  # Most articles use <p> for content
    article_body = "\n".join([p.text for p in paragraphs[:5]])  # Get first 5 paragraphs

    news_article = {
        "title": entry.title,
        "source": entry.source.title if hasattr(entry, 'source') else "Unknown",
        "url": article_url,
        "body": article_body
    }
    news_list.append(news_article)








response = ""
try:
    ticker = yf.Ticker(fortune_500_top_100)
    financials = ticker.financials
    if (financials.empty):
       raise RuntimeError("Empty Frame")
    current_price = ticker.history(period="1d")["Close"].iloc[-1]
    term = input("Term: ")
    userinput = f"Here is the current price, recent news articles, and the financials of {current_price} and {fortune_500_top_100}. {financials}. {news_list}. Along with this information, do resarch on current market trends as a macroeconomy and microeconomy as well as research recent news (up to a year ago) and give me a letter grade on whether it is ideal to invest in the {term} term."
    response = chat_session.send_message(userinput)
    print("\nFinancials:")
    print(financials)
    response = response.text
except:
    
    ticker_form = what_stock.send_message(fortune_500_top_100)
    response = ticker_form.text
    response = response.replace("\n", "")
    if (ticker_form.text.upper() == "X"):
      print("Stock does not exist")
      dont_run = True
    else:
        ticker = yf.Ticker(str(response))
        financials = ticker.financials
        current_price = ticker.history(period="1d")["Close"].iloc[-1]
        term = input("Term: ")
        userinput = f"Here is the current price, recent news articles, and the financials of {current_price} and {fortune_500_top_100}. {financials}. {news_list}. Along with this information, do resarch on current market trends as a macroeconomy and microeconomy as well as research recent news (up to a year ago) and give me a letter grade on whether it is ideal to invest in the {term} term."        response = chat_session.send_message(userinput)
        print("\nFinancials:")
        print(financials)
        response = response.text

print("\n\n\n\n\n\n\n")
if dont_run == False:
    print(response)
    with open(r"C:\Users\Ishaan\Desktop\Python\stock_grades.txt", "w") as file:
      file.write(f"{response}\n\n")

else:
    print("Code did not run")


