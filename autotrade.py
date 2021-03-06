# Raw Package
import numpy as np
import pandas as pd
from plotly.graph_objs import layout

#Data Source
import yfinance as yf

#Data viz
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#from webull import webull

def get_macd(price, slow, fast, smooth):
    exp1 = price.ewm(span = fast, adjust = False).mean()
    exp2 = price.ewm(span = slow, adjust = False).mean()
    macd = pd.DataFrame(exp1 - exp2).rename(columns = {'Close':'macd'})
    signal = pd.DataFrame(macd.ewm(span = smooth, adjust = False).mean()).rename(columns = {'macd':'signal'})
    hist = pd.DataFrame(macd['macd'] - signal['signal']).rename(columns = {0:'hist'})
    frames = [macd, signal, hist]
    df = pd.concat(frames, join = 'inner', axis = 1)
    return df

def get_data(short, range, tick):
    data = yf.download(tickers=tick, period=range, interval=short)
    data_macd = get_macd(data['Close'], 26, 12, 9)
    data_macd['Color'] = np.where(data_macd['hist']<0, 'red', 'green')
    data_macd.tail()
    return pd.concat([data,data_macd], axis=1)

btc_data = get_data("1h", "1d", "BTC-USD")
print(btc_data)
#print(data)
fig = make_subplots(vertical_spacing = 0, shared_xaxes=True, rows=2, cols=1, row_heights=[0.6, 0.4])
fig.add_trace(go.Scatter(x=btc_data.index,
                y=btc_data['Close'], name = 'trend'),
                row=1,col=1)
fig.add_trace(go.Scatter(x=btc_data.index,
                y=btc_data['macd'], name = 'macd'),
                row=2,col=1)
fig.add_trace(go.Scatter(x=btc_data.index,
                y=btc_data['signal'], name = 'signal'),
                row=2,col=1)
fig.add_trace(go.Bar(x=btc_data.index,
                y=btc_data['hist'], name = 'histogram', marker_color = btc_data['Color']),
                row=2,col=1)
# Add titles
fig.update_layout(
    xaxis_rangeslider_visible=False,
    title='Bitcoin Price',
    yaxis_title='Stock Price (USD per Shares)',
    xaxis=dict(zerolinecolor='black', showticklabels=False),
    xaxis2=dict(showticklabels=True))

# X-Axes
fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)

#Show
fig.show()
#k=input("press close to exit") 