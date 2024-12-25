import os
import time
import yfinance as yf
import numpy as np
import pandas as pd
from finvizfinance.screener.overview import Overview

#Stock picking algorithm is proprietary and removed from public code, please reach out if you want to learn more about the algo

CSV_FILE_PATH = "./portfolio_data.csv"
EXPIRATION_TIME = 86400  # 24 hours in seconds

def get_distinct_tickers():
    all_tickers = [
    "NVDA", "NFLX", "NOW", "SHOP", "APP", "AXON", "SMCI", "MPWR", 
    "TOST", "SOFI", "AFRM", "JEF", "RL", "NBIX", "DUOL", "TKO", 
    "FOUR", "SHC", "RELY", "ALKT", "GRND", "RSI", "CLSK", "VCYT", 
    "AMBA", "TWST", "QUBT", "TARS", "WGS", "DXPE", "INOD", "WISA"]
    
    return all_tickers

def calculate_portfolio():
    stock_tickers = get_distinct_tickers()
    data = []
    for ticker in stock_tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="1y")
            data.append({
                'Stock': ticker,
                'Name': info.get('shortName', 'N/A'),
                'Country': info.get('country', 'N/A'),
                'Sector': info.get('sector', 'N/A'),
                'Market Cap': info.get('marketCap', 0),
                'Revenue': info.get('totalRevenue', 0),
                'Volatility': np.std(hist['Close'])
            })
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
    
    df = pd.DataFrame(data)
    df = df[df['Country'].isin(['United States', 'Canada'])]
    total_market_cap = df['Market Cap'].sum()
    df['Market Cap Weight'] = df['Market Cap'] / total_market_cap
    num_stocks = len(stock_tickers)
    df['Equal Weight'] = 1 / num_stocks
    total_revenue = df['Revenue'].sum()
    df['Fundamental Weight'] = df['Revenue'] / total_revenue
    df['Inverse Volatility'] = 1 / df['Volatility']
    total_inverse_vol = df['Inverse Volatility'].sum()
    df['Volatility Weight'] = df['Inverse Volatility'] / total_inverse_vol
    df['Log Market Cap'] = np.log(df['Market Cap'] + 1)
    df['Log Market Cap Weight'] = df['Log Market Cap'] / df['Log Market Cap'].sum()
    total_capped_weight = df['Log Market Cap Weight'].sum()
    df['Final Capped Weight'] = (df['Log Market Cap Weight'] / total_capped_weight) * 100

    df['Adjusted Weight'] = (
        df['Final Capped Weight'] * 0.3 +
        df['Equal Weight'] * 0.15 +
        df['Volatility Weight'] * 0.15 +
        df['Fundamental Weight'] * 0.4
    )

    total_adjusted_weight = df['Adjusted Weight'].sum()
    df['Stock Allocation Weight (%)'] = (df['Adjusted Weight'] / total_adjusted_weight) * 100

    final_df = df[['Stock', 'Name', 'Country', 'Sector', 'Market Cap', 'Revenue', 'Volatility', 'Stock Allocation Weight (%)']]
    return final_df.sort_values(by='Stock Allocation Weight (%)', ascending=False)


def get_portfolio():
    # Check if the CSV file exists
    if os.path.exists(CSV_FILE_PATH):
        # Check the file modification time
        file_mod_time = os.path.getmtime(CSV_FILE_PATH)
        current_time = time.time()
        
        if current_time - file_mod_time < EXPIRATION_TIME:
            # If file is less than 24 hours old, load from CSV
            print("Loading portfolio data.")
            print("Please note that the portfolio you are querying is a model portfolio as of December 1, 2024, and does not reflect the updated and rebalanced portfolio as of today. This model excludes the proprietary strategy employed in selecting these stocks. For access to the real-time, updated portfolio, please contact us directly.")

            return pd.read_csv(CSV_FILE_PATH)
        else:
            # If file is older than 24 hours, update the CSV
            print("Portfolio data is older than 24 hours. Fetching new data.")
            print("Please note that the portfolio you are querying is a model portfolio as of December 1, 2024, and does not reflect the updated and rebalanced portfolio as of today. This model excludes the proprietary strategy employed in selecting these stocks. For access to the real-time, updated portfolio, please contact us directly.")

            portfolio_data = calculate_portfolio()
            portfolio_data.to_csv(CSV_FILE_PATH, index=False)
            return portfolio_data
    else:
        # If file doesn't exist, create it
        print("Fetching data and creating a cache for the next 24 hours.")
        print("Please note that the portfolio you are querying is a model portfolio as of December 1, 2024, and does not reflect the updated and rebalanced portfolio as of today. This model excludes the proprietary strategy employed in selecting these stocks. For access to the real-time, updated portfolio, please contact us directly.")

        portfolio_data = calculate_portfolio()
        portfolio_data.to_csv(CSV_FILE_PATH, index=False)
        return portfolio_data
