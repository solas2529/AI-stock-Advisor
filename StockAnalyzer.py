import os
import google.generativeai as genai
import yfinance as yf
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key='API_KEY (INSERT YOUR OWN)') # I used my own API KEY, but use your own (it is free)

# Create the model
generation_config = {
  "temperature": 2,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

# Model 2
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
  system_instruction="You are a financial proffesional, not an AI chat bot.",
)
model_2 = genai.GenerativeModel(
  model_name="gemini-2.0-flash",
  generation_config=generation_config_2,
  system_instruction="Find the ticker of the company, if you cannot find the ticker, respond with just the letter x, also do not add the",
)

chat_session = model.start_chat(
    history = []
  ) 

what_stock = model_2.start_chat(
    history = []
)
dont_run = False
fortune_500_top_100 = input("Enter Stock Name or Ticker: ")
response = ""
try: # If they give a ticker it will not raise an exception
    ticker = yf.Ticker(fortune_500_top_100)
    financials = ticker.financials
    if (financials.empty):
       raise RuntimeError("Empty Frame")
    current_price = ticker.history(period="1d")["Close"].iloc[-1]
    term = input("Term: ")
    userinput = f"Here is the current price and  the financials of {current_price} and {fortune_500_top_100}. {financials}. Along with this information, do resarch on current market trends as a macroeconomy and microeconomy as well as research recent news (up to a year ago) and give me a letter grade on whether it is ideal to invest in the {term} term."
    response = chat_session.send_message(userinput)
    print("\nFinancials:")
    print(financials)
    response = response.text
except: #names are proccesed through here
    
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
        userinput = f"Here is the current price and  the financials of {current_price} and {fortune_500_top_100}. {financials}. Along with this information, do resarch on current market trends as a macroeconomy and microeconomy as well as research recent news (up to a year ago) and give me a letter grade on whether it is ideal to invest in the {term} term."
        response = chat_session.send_message(userinput)
        print("\nFinancials:")
        print(financials)
        response = response.text

print("\n\n\n\n\n\n\n")
if dont_run == False:
    print(response)
    with open(r"C:\Users\Ishaan\Desktop\Python\stock_grades.txt", "w") as file: # it will write a txt file because the console is not ideal, and a docs is too inconsistent for something like this
      file.write(f"{response}\n\n")

else:
    print("Code did not run")


