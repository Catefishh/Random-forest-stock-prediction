import functools
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go


app = dash.Dash(__name__)

# Cache fetched stock data to improve performance.
@functools.lru_cache(maxsize=10)
def fetch_stock_data(symbol, period):
    try:
        # Fetch historical data using yfinance.
        stock_data = yf.Ticker(symbol).history(period=period)
        if stock_data.empty:
            raise ValueError("No data found for the given symbol and period.")
        return stock_data
    except Exception as e:
        return str(e)

# Creation of the 4 different charts.
def create_line_chart(data):
    fig = px.line(data, x=data.index, y=['Open', 'Close', 'High', 'Low'])
    fig.update_layout(title='Price Trends', xaxis_title='Date', yaxis_title='Price ($)')
    return fig

def create_candlestick_chart(data):
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close']
    )])
    fig.update_layout(title='Daily Price Changes', xaxis_title='Date', yaxis_title='Price ($)')
    return fig

def create_ohlc_chart(data):
    fig = go.Figure(data=[go.Ohlc(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        increasing_line_color='green',
        decreasing_line_color='red'
    )])
    fig.update_layout(title='OHLC Chart', xaxis_title='Date', yaxis_title='Price ($)')
    return fig

def create_volume_chart(data):
    fig = go.Figure(data=[go.Bar(x=data.index, y=data['Volume'], name='Volume')])
    fig.update_layout(title='Trading Volume', xaxis_title='Date', yaxis_title='Volume')
    return fig

def create_chart(data, chart_type='line'):
    chart_functions = {
        'line': create_line_chart,
        'candlestick': create_candlestick_chart,
        'ohlc': create_ohlc_chart,
        'volume': create_volume_chart
    }

    chart_func = chart_functions.get(chart_type)
    if chart_func:
        return chart_func(data)
    else:
        return go.Figure().add_annotation(
            text=f"Unknown chart type: {chart_type}",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            xanchor='center',
            yanchor='middle',
            showarrow=False
        )

# Dropdown options for periods and chart types
period_options = [
    {'label': '1 Day', 'value': '1d'},
    {'label': '1 Week', 'value': '5d'},
    {'label': '1 Month', 'value': '1mo'},
    {'label': '3 Months', 'value': '3mo'},
    {'label': '6 Months', 'value': '6mo'},
    {'label': '1 Year', 'value': '1y'},
    {'label': '5 Years', 'value': '5y'}
]

chart_type_options = [
    {'label': 'Line Chart', 'value': 'line'},
    {'label': 'Candlestick Chart', 'value': 'candlestick'},
    {'label': 'OHLC Chart', 'value': 'ohlc'},
    {'label': 'Volume Chart', 'value': 'volume'}
]

app.layout = html.Div([
    html.H1('Stock Price Dashboard'),
    html.Div([
        dcc.Input(
            id='symbol-input',
            type='text',
            placeholder='Enter stock symbol (e.g. AAPL)'
        ),
        dcc.Dropdown(
            id='period-dropdown',
            options=period_options,
            value='1mo'
        ),
        dcc.Dropdown(
            id='chart-type-dropdown',
            options=chart_type_options,
            value='line'
        )
    ], style={'width': '300px'}),
    dcc.Graph(id='stock-chart')
])

@app.callback(
    Output('stock-chart', 'figure'),
    [
        Input('symbol-input', 'value'),
        Input('period-dropdown', 'value'),
        Input('chart-type-dropdown', 'value')
    ]
)
def update_chart(symbol, period, chart_type):
    if not symbol:
        return go.Figure().add_annotation(
            text="Please enter a stock symbol.",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            xanchor='center',
            yanchor='middle',
            showarrow=False
        )

    data = fetch_stock_data(symbol.upper(), period)
    if isinstance(data, str):
        return go.Figure().add_annotation(
            text=data,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            xanchor='center',
            yanchor='middle',
            showarrow=False
        )

    return create_chart(data, chart_type)

if __name__ == '__main__':
    app.run_server(debug=True)
