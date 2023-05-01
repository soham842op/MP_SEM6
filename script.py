from flask import Flask, render_template, request
from flask import  jsonify
import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from flask import Blueprint, flash
from flask_login import login_required, current_user
from newsapi import NewsApiClient

app = Flask(__name__)

# Init news api
newsapi = NewsApiClient(api_key='a9db33fcf55946eb8cec5b97302bbbf2')

# helper function
def get_sources_and_domains():
	# Get all financial news sources
	financial_sources = ['bloomberg', 'cnbc', 'financial-post', 'financial-times', 'reuters']
	
	# Get domains for each source
	domains = [newsapi.get_source(s)['url'] for s in financial_sources]
	domains = [d.replace("http://", "").replace("https://", "").replace("www.", "") for d in domains]
	
	# Join sources and domains
	sources = ",".join(financial_sources)
	domains = ",".join(domains)
	
	return sources, domains

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/index")
def index():
    # Scrape data from Yahoo Finance
    url = "https://finance.yahoo.com/trending-tickers"
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'html.parser')
    table = soup.find('table', class_='W(100%)')

    # Create DataFrame
    df = pd.DataFrame(columns=['Symbol', 'Name', 'Last Price', 'Market Time', 'Change', '% Change','Volume', 'Market Cap'])

    for row in table.tbody.find_all('tr'):    
        # Find all data for each column
        columns = row.find_all('td')

        if(columns != []):
            Symbol = columns[0].text.strip()
            Name = columns[1].text.strip()
            LastPrice = columns[2].find('fin-streamer').contents[0].strip('&0.') if columns[2].find('fin-streamer') is not None else ""
            MarketTime = columns[3].find('fin-streamer').contents[0].strip('&0.') if columns[3].find('fin-streamer') is not None else ""
            Change = columns[4].find('span').contents[0].strip('&0.') if columns[4].find('span') is not None else ""
            PChange = columns[5].find('span').contents[0].strip('&0.') if columns[5].find('span') is not None else ""
            Volume = columns[6].find('fin-streamer').contents[0].strip('&0.') if columns[6].find('fin-streamer') is not None else ""
            MarketCap = columns[7].find('fin-streamer').contents[0].strip('&0.') if columns[7].find('fin-streamer') is not None else ""

            df = pd.concat([df, pd.DataFrame({'Symbol': Symbol, 'Name': Name, 'Last Price': LastPrice , 'Market Time': MarketTime, 'Change': Change, '% Change': PChange, 'Volume': Volume, 'Market Cap': MarketCap}, index=[0])], ignore_index=True)

    # Convert DataFrame to HTML table
    table_html = df.to_html(index=False)
    return render_template("integer.html", table=table_html)




@app.route("/news",  methods=['GET', 'POST'])
def news():
	if request.method == "POST":
		sources, domains = get_sources_and_domains()
		keyword = request.form["keyword"]
		related_news = newsapi.get_everything(q=keyword,
									sources=sources,
									domains=domains,
									language='en',
									sort_by='relevancy',
									category='business')
		no_of_articles = related_news['totalResults']
		if no_of_articles > 100:
			no_of_articles = 100
		all_articles = newsapi.get_everything(q=keyword,
									sources=sources,
									domains=domains,
									language='en',
									sort_by='relevancy',
									category='business',
									page_size = no_of_articles)['articles']
		return render_template("news.html", all_articles = all_articles,
							keyword=keyword)
	else:
		top_headlines = newsapi.get_top_headlines(country="us", language="en", category='business')
		total_results = top_headlines['totalResults']
		if total_results > 100:
			total_results = 100
		all_headlines = newsapi.get_top_headlines(country="us",
													language="en",
													category='business',
													page_size=total_results)['articles']
		return render_template("news.html", all_headlines = all_headlines)
	return render_template("news.html")

# API Route for pulling the stock quote
@app.route("/quote")
def display_quote():
	# get a stock ticker symbol from the query string
	# default to AAPL
	symbol = request.args.get('symbol', default="AAPL")
	period = request.args.get('period', default="1y")
	interval = request.args.get('interval', default="1mo")

	# pull the stock quote
	quote = yf.Ticker(symbol)

	#return the object via the HTTP Response
	return jsonify(quote.info)

# API route for pulling the stock history
@app.route("/history")
def display_history():
	#get the query string parameters
	symbol = request.args.get('symbol', default="AAPL")
	period = request.args.get('period', default="1y")
	interval = request.args.get('interval', default="1mo")

	#pull the quote
	quote = yf.Ticker(symbol)	
	#use the quote to pull the historical data from Yahoo finance
	hist = quote.history(period=period, interval=interval)
	#convert the historical data to JSON
	data = hist.to_json()
	#return the JSON in the HTTP response
	return data

# This is the / route, or the main landing page route.
@app.route("/ind")
def homepage():
	# we will use Flask's render_template method to render a website template.
    return render_template("chart.html")

@app.route("/analysis")
def analysis():
<<<<<<< HEAD
    return "analysis"
=======
    return render_template("analysis.html")

@app.route("/yesbank")
def yesbank():
    return render_template("yesbank.html")

@app.route("/bsesn")
def bsesn():
    return render_template("BSESN.html")
>>>>>>> 4a478e9 (Final Frontend commit)

if __name__ == '__main__':
    app.run(debug=True)