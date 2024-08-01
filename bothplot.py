import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import datetime

# Define the directory containing the CSV files
input_dir = os.path.expanduser(r"C:/Users/apspa/Documents/PSU/RESEARCH PROJECT/Code/outputs/")

def plot_combined_sentiment_and_price(sentiment_file_paths, price_file_paths):
    """
    Plots combined sentiment scores and stock prices over time for multiple tickers.
    
    Args:
        sentiment_file_paths (list of str): List of file paths for sentiment CSV files.
        price_file_paths (list of str): List of file paths for price CSV files.
    """
    # List to store DataFrames for sentiment
    sentiment_dfs = []

    for file_path in sentiment_file_paths:
        try:
            # Read sentiment data into DataFrame
            df = pd.read_csv(file_path)
            print(f"Columns in sentiment file {file_path}: {df.columns}")
            print(df.head())
            
            # Convert 'Date' to datetime
            df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S')
            df = df.dropna(subset=['Date'])
            
            # Extract time and create a Time_Datetime column
            df['Time'] = df['Date'].dt.time
            df['Time_Datetime'] = df.apply(lambda row: datetime.datetime.combine(datetime.date(1900, 1, 1), row['Time']), axis=1)
            
            # Add a column for the stock ticker
            df['Ticker'] = os.path.basename(file_path).split('_')[0]
            
            sentiment_dfs.append(df)
        except Exception as e:
            print(f"Error processing sentiment file {file_path}: {e}")

    if not sentiment_dfs:
        print("Error: No sentiment data found across all files.")
        return

    # Combine all sentiment data into a single DataFrame and sort by Time_Datetime
    combined_sentiment_df = pd.concat(sentiment_dfs).sort_values('Time_Datetime')

    # List to store DataFrames for stock prices
    price_dfs = []

    for file_path in price_file_paths:
        try:
            # Read price data into DataFrame
            df = pd.read_csv(file_path)
            print(f"Columns in price file {file_path}: {df.columns}")
            print(df.head())
            
            # Convert 'Exported_At' to datetime
            df['Exported_At'] = pd.to_datetime(df['Exported_At'], format='%Y-%m-%d %H:%M:%S.%f')
            df = df.dropna(subset=['Exported_At'])
            
            # Extract time and create a Time_Datetime column
            df['Time'] = df['Exported_At'].dt.time
            df['Time_Datetime'] = df.apply(lambda row: datetime.datetime.combine(datetime.date(1900, 1, 1), row['Time']), axis=1)
            
            # Add a column for the stock ticker
            df['Ticker'] = df['Ticker']
            
            price_dfs.append(df)
        except Exception as e:
            print(f"Error processing price file {file_path}: {e}")

    if not price_dfs:
        print("Error: No price data found across all files.")
        return

    # Combine all price data into a single DataFrame and sort by Time_Datetime
    combined_price_df = pd.concat(price_dfs).sort_values('Time_Datetime')

    # Create individual plots for each ticker
    tickers = combined_sentiment_df['Ticker'].unique()

    for ticker in tickers:
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Plot sentiment data for the current ticker
        ticker_sentiment_df = combined_sentiment_df[combined_sentiment_df['Ticker'] == ticker]
        ax1.plot(ticker_sentiment_df['Time_Datetime'], ticker_sentiment_df['Combined_Sentiment'], label=f"{ticker} Sentiment")

        ax1.set_xlabel('Time')
        ax1.set_ylabel('Combined Sentiment')
        ax1.legend(loc='upper left')
        ax1.grid(True)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        ax1.xaxis.set_major_locator(mdates.HourLocator(interval=1))
        plt.xticks(rotation=45)

        # Create a secondary y-axis for stock price
        ax2 = ax1.twinx()

        # Plot stock price data for the current ticker
        ticker_price_df = combined_price_df[combined_price_df['Ticker'] == ticker]
        ax2.plot(ticker_price_df['Time_Datetime'], ticker_price_df['Price'], label=f"{ticker} Price", linestyle='--')

        ax2.set_ylabel('Stock Price')
        ax2.legend(loc='upper right')

        plt.title(f'Combined Sentiment and Stock Price Over Time for {ticker}')
        plt.tight_layout()

        plt.show()

# List of sentiment CSV file paths
sentiment_file_paths = [os.path.join(input_dir, 'AMZN_today_news_with_sentiment.csv'),
                        os.path.join(input_dir, 'AAPL_today_news_with_sentiment.csv'),
                        os.path.join(input_dir, 'GOOGL_today_news_with_sentiment.csv')]

# List of price CSV file paths
price_file_paths = [os.path.join(input_dir, 'export.csv')]

# Generate the plot
plot_combined_sentiment_and_price(sentiment_file_paths, price_file_paths)
