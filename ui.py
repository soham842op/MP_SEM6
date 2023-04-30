import dash
from dash import dcc
from dash import html
from dash.dependencies import Input,Output,State
from dash.exceptions import PreventUpdate
import plotly.express as px
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn import metrics 
from keras.models import Sequential
from keras.layers import Dense, LSTM
import math
from datetime import datetime
import datetime as dt


def get_historical(quote):
    end = datetime(2020,12,30)
    start = datetime(2001,1,2)
    data = yf.download(quote, start=start, end=end)
    df = pd.DataFrame(data=data)
    df.to_csv(''+quote+'.csv')
    if(df.empty):
        ts = TimeSeries(key='N6A6QT6IBFJOPJ70',output_format='pandas')
        data, meta_data = ts.get_daily_adjusted(symbol='NSE:'+quote, outputsize='full')
        #Format df
        #Last 2 yrs rows => 502, in ascending order => ::-1
        data=data.head(503).iloc[::-1]
        data=data.reset_index()
        #Keep Required cols only
        df=pd.DataFrame()
        df['Date']=data['date']
        df['Open']=data['1. open']
        df['High']=data['2. high']
        df['Low']=data['3. low']
        df['Close']=data['4. close']
        df['Adj Close']=data['5. adjusted close']
        df['Volume']=data['6. volume']
        df.to_csv(''+quote+'.csv',index=False)
    return

app=dash.Dash()
server=app.server


app.layout = html.Div(
    [  
        html.Div(
            [
                html.H1('StockIQ',className='heading'),
                html.H2("Welcome to the Stock Trend Prediction App!", className="heading"),
                html.Div(
                    [
                    # Input box for to enter stock ticker, default value will be 'SBIN.NS'
                    dcc.Input(id='stock_symbol', value= '',placeholder= 'Input Stock Ticker here', type= 'text', className='inputs'),
                    html.Button('Submit', id='submit-stock', className='buttons', n_clicks=0)

                    ],className=''
                ),

                
            ],className='nav'
        ),

        # 2nd part, RHS of the screen , Graph display

        html.Div(
            [
            dcc.Loading( id='loading1', color='#3b3b3b',children=[html.Div(
                [
                    html.Img(id='logo', className='imglogo'),
                    html.H2(id='ticker')
                ],className='header'
            ),
            html.Div(id='description', className='info')], type='circle'),
            dcc.Loading(children=[html.Div([], id='stonks-graph', className='graphs')], id='loading2', type='graph'),
            dcc.Loading(id='loading3',
                children=[html.Div([], id='forecast-graph', className='graphs')],
                type='graph')


            ],className='outputContainer'
        )
    ], className='container')


@app.callback([
    Output('logo', 'src'),
    Output('ticker', 'children'),
    Output('description', 'children')],
    [Input('submit-stock', 'n_clicks')],
    [State('stock_symbol', 'value')]
)

def update_data(n,stock_symbol):
    get_historical(stock_symbol)
        
    
app.run_server(debug=True)



