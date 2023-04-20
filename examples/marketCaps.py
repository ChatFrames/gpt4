import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define a list of company stock symbols and other assets
company_symbols = ['MSFT', 'AAPL', 'GOOGL', 'AMZN', 'FB', '^GSPC', '^IXIC', 'BTC-USD', 'ETH-USD']

# Initialize an empty DataFrame for storing the moving averages and market cap
moving_averages = pd.DataFrame()

# Download historical stock data and calculate the 30-day moving averages for market cap
for symbol in company_symbols:
    stock = yf.Ticker(symbol)
    data = stock.history(period="1y")
    
    if symbol not in ['^GSPC', '^IXIC', 'BTC-USD', 'ETH-USD']:
        data['Market Cap'] = data['Close'] * data['Volume']
        data[f'{symbol} 30-day Market Cap MA'] = data['Market Cap'].rolling(window=30).mean()
        moving_averages = pd.concat([moving_averages, data[f'{symbol} 30-day Market Cap MA']], axis=1)
    else:
        moving_averages = pd.concat([moving_averages, data['Close']], axis=1)
        moving_averages = moving_averages.rename(columns={'Close': f'{symbol} Close'})

# Plot the moving averages for the companies and other assets
plt.figure(figsize=(14, 7))
for symbol in company_symbols:
    if symbol not in ['^GSPC', '^IXIC', 'BTC-USD', 'ETH-USD']:
        plt.plot(moving_averages.index, moving_averages[f'{symbol} 30-day Market Cap MA'], label=f'{symbol} 30-day Market Cap MA', linewidth=2)
    else:
        plt.plot(moving_averages.index, moving_averages[f'{symbol} Close'], label=f'{symbol} Close', linewidth=2)

# Set the title and labels
plt.title('30-day Market Cap Moving Averages and Asset Prices')
plt.xlabel('Date')
plt.ylabel('Market Cap Moving Average (USD)')

# Display the legend and show the plot
plt.legend()
plt.show()
