import os
import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime
from .portfolio import get_portfolio  # Assuming get_portfolio() is imported

def backtest_portfolio(initial_investment, period='1y', csv_file='portfolio_data.csv'):
    """
    Perform backtest for the given portfolio with the specified investment amount and period.
    """
    # Check if the CSV file exists and if it's older than 24 hours
    if os.path.exists(csv_file) and (datetime.now() - datetime.fromtimestamp(os.path.getmtime(csv_file))).days < 1:
        print("Fetching Portfolio data.")
        stock_weights = pd.read_csv(csv_file)
    else:
        print("Fetching updated portfolio data...")
        stock_weights = get_portfolio()  # Assuming this fetches the portfolio stock data
        stock_weights.to_csv(csv_file, index=False)  # Cache to CSV

    # Prepare the periods and initialize value_data dictionary
    value_data = {'Ticker': stock_weights['Stock'], 'Name': stock_weights['Name'], 'Sector': stock_weights['Sector'],
                  'Market Cap': stock_weights['Market Cap'], 'Revenue': stock_weights['Revenue'], 
                  'Volatility': stock_weights['Volatility'], 'Weights': stock_weights['Stock Allocation Weight (%)']}

    # Loop through the periods and fetch stock data
    stock_prices = {}
    for stock in stock_weights['Stock']:
        try:
            stock_data = yf.Ticker(stock).history(period=period)['Close']
            stock_prices[stock] = stock_data
        except Exception as e:
            stock_prices[stock] = None

    # Convert stock prices to DataFrame
    price_df = pd.DataFrame(stock_prices).dropna(axis=1)
    
    if price_df.empty:
        value_data[f'{period} Value'] = [np.nan] * len(stock_weights)
    else:
        # Normalize the weights
        stock_weights['Normalized Weight'] = stock_weights['Stock Allocation Weight (%)'] / stock_weights['Stock Allocation Weight (%)'].sum()
        weights = stock_weights.set_index('Stock')['Normalized Weight']
        weights = weights.reindex(price_df.columns).fillna(0)

        # Calculate initial stock values and price change ratios
        initial_stock_values = weights * initial_investment
        price_change_ratios = price_df.iloc[-1] / price_df.iloc[0]
        final_stock_values = initial_stock_values * price_change_ratios
        value_data[f'{period} Value'] = final_stock_values.reindex(stock_weights['Stock']).fillna(0).values

    value_data['Initial Value'] = (stock_weights['Stock Allocation Weight (%)'] / 100) * initial_investment
    final_df = pd.DataFrame(value_data)

    # Save the result to CSV for future use
    final_df.to_csv('final_file.csv', index=False)

    # Get the portfolio values for the specified period
    value_after_period = final_df[f'{period} Value'].sum()

    # Calculate percentage return
    percentage_return = (value_after_period - initial_investment) / initial_investment * 100

    # Calculate volatility (standard deviation of returns)
    daily_returns = price_df.pct_change().dropna(axis=0)
    portfolio_daily_returns = daily_returns.sum(axis=1)

    # Annualize volatility based on the number of trading days in a year (252 days)
    annualized_volatility = portfolio_daily_returns.std() * np.sqrt(252)  # Annualized volatility


    # Prepare the result dictionary
    result = {
        'Period': period,
        'Initial Investment': initial_investment,
        'Investment Value After': value_after_period,
        'Percentage Return': percentage_return,
        'Volatility': annualized_volatility
    }

    return result
