import requests
import os
from twilio.rest import Client

#twilio recovery pass: NJfhVyFPAmWqvDVpff9tdrluvl14A0uydLZI57-e

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

api_key_stock = "LCOUQASCO86NB137"
api_key_news = "febe9a186c864537ad54f338d435cfaa"

account_sid = "AC9b8421bb6ad1109c913574e24061f16c"
auth_token = "a14dab73e38e4a41ff20080850ada7d9"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": api_key_stock,
}

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query'
r = requests.get(url, params = stock_params)
data = r.json()['Time Series (Daily)']

#Transformar o data em uma lista pra poder acessar as datas por index
data_list = [value for (keys, value) in data.items()]

close_price = data_list[0]['4. close'] #referente à ontem
close_price_ontem = data_list[1]['4. close'] #referente à antes de ontem

variation_flag = False

#Caso variação maior que 5%
variation = (abs(((float(close_price)/float(close_price_ontem))) -1)*100)

if variation >= 5:
    variation_flag = True
    print("Get News")
#else:
#    print("Everything Okay")

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

news_params = {
    "apiKey": api_key_news,
    "q": COMPANY_NAME,      
}

url_news = ('https://newsapi.org/v2/everything?')


response = requests.get(url_news, params = news_params)
data_news = response.json()['articles']

articles = data_news[:3]

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

formatted_articles = [f"Headline: {article['title']} %\nBrief: {article['description']}" for article in articles]

# Set environment variables for your credentials
# Read more at http://twil.io/secure
client = Client(account_sid, auth_token)
for article in formatted_articles:
    message = client.messages.create(
    body = article,
    from_="+15075545862",
    to="+5561998698261"
    )
print(message.sid)


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

