import plotly.graph_objects as go
import dateutil
import pandas_ta as pta
import datetime

def plotly_table(dataframe):
    headerColor='grey'
    rowEvenColor='#f8fafd'
    rowOddColor='#e1efff'
    fig=go.Figure(data=[go.Table(
    header=dict(
        values=["<b>Index</b>"]+["<b>"+str(i)[:10]+"</b>" for i in dataframe.columns],
        line_color='#0078ff', fill_color='#0078ff',
        align='center', font=dict(color='white', size=15), height=35,        
    ),
    cells=dict(
        values=[[str(i) for i in dataframe.index]] + [dataframe[i].tolist() for i in dataframe.columns],
        fill_color=[ [rowOddColor if i%2 else rowEvenColor for i in range(len(dataframe))] ] * (len(dataframe.columns)+1),
        align='left', line_color='white', font=dict(color="black", size=15)
    )
    )])
    fig.update_layout(height=350, margin=dict(l=0,r=0,t=0,b=0))
    return fig
    

def filter_data(dataframe, num_period):
    if num_period == '1mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-1)
    elif num_period == '5d':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(days=-5)
    elif num_period == '6mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-6)
    elif num_period == '1y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-1)
    elif num_period == '5y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-5)
    elif num_period == 'ytd':
        date = datetime.datetime(dataframe.index[-1].year, 1, 1).strftime('%Y-%m-%d')
    else:
        date = dataframe.index[0]

    return dataframe.reset_index()[dataframe.reset_index()['Date'] > date]

def close_chart(dataframe,num_period=False):
    if num_period:
        dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'],
                             mode='lines',
                             name='Open', line=dict(width=2, color='#5ab7ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],
                             mode='lines',
                             name='Close', line=dict(width=2, color='black')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'],
                             mode='lines', name='High', line=dict(width=2, color='#0078ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'],
                             mode='lines', name='Low', line=dict(width=2, color='red')))
    
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height=500, margin=dict(l=0, r=20, t=20, b=0),
                      plot_bgcolor='white', paper_bgcolor='#e1efff',
                      legend=dict(yanchor="top", xanchor="right"))
    
    return fig

def candlestick(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=dataframe['Date'],
                                 open=dataframe['Open'], high=dataframe['High'],
                                 low=dataframe['Low'], close=dataframe['Close']))
    
    fig.update_layout(showlegend=False, height=500, margin=dict(l=0, r=20, t=20, b=0),
                      plot_bgcolor='white', paper_bgcolor='#e1efff')
    return fig

def RSI(dataframe, num_period):
    import plotly.graph_objects as go
    import pandas_ta as ta

    dataframe['RSI'] = ta.rsi(dataframe['Close'], length=14)
    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['RSI'],
        name='RSI',
        line=dict(color='blue')
    ))

    fig.update_layout(
        yaxis_range=[0, 100],
        height=200,
        plot_bgcolor='white',
        paper_bgcolor='#f0f2f6',
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    return fig

def Moving_average(dataframe,num_period):
    dataframe['SMA_50'] = pta.sma(dataframe['Close'],50)
    dataframe = filter_data(dataframe,num_period)
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'],
        mode='lines',
        name='Open', line = dict( width=2,color = '#5ab7ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],
        mode='lines',
        name='Close', line = dict( width=2,color = 'black')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'],
        mode='lines', name='High', line = dict( width=2,color = '#0078ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'],
        mode='lines', name='Low', line = dict( width=2,color = 'red')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['SMA_50'],
        mode='lines', name='SMA 50', line = dict( width=2,color = 'purple')))

    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height = 500, margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor = 'white',paper_bgcolor = '#e1efff',legend=dict(
        yanchor="top",
        xanchor="right"
    ))
    return fig

def MACD(dataframe, num_period):
    macd = pta.macd(dataframe['Close']).iloc[:,0]
    macd_signal = pta.macd(dataframe['Close']).iloc[:,1]
    macd_hist = pta.macd(dataframe['Close']).iloc[:,2]
    dataframe['MACD'] = macd
    dataframe['MACD Signal'] = macd_signal
    dataframe['MACD Hist'] = macd_hist
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['MACD'], name = 'RSI', marker_color='orange', line = dict( width=2,color = 'orange'),
    ))
    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['MACD Signal'], name = 'Overbought', marker_color='red', line = dict( width=2,color = 'red',dash="dash"),
    ))
    c = ['red' if cl < 0 else 'green' for cl in macd_hist]
    fig.update_layout(
        height=200, plot_bgcolor = 'white', paper_bgcolor = "#e1efff", margin=dict(l=0, r=0, t=0, b=0), legend=dict(orientation="h", y=1.02, 
        yanchor="top", x=1, xanchor="right")
    )
    return fig

def Moving_average_forecast(forecast):
    fig=go.Figure()

    fig.add_trace(go.Scatter(x=forecast.index[:-30],y=forecast['Close'].iloc[:-30],
                mode='lines',
                name='Close price',line=dict(width=2,color='black')))
    fig.add_trace(go.Scatter(x=forecast.index[-31:],y=forecast['Close'].iloc[-31:],
                mode='lines',
                name='Future Close price',line=dict(width=2,color='red')))
    
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height=500,margin=dict(l=0,r=20,b=20),plot_bgcolor='#e1efff',legend=dict(
        yanchor="top",
        xanchor="right"
    ))
    return fig