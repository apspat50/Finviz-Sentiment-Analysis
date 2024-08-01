# Finviz-Sentiment-Analysis

# Stock Sentiment Analysis and Visualization

This repository contains Python scripts for analyzing and visualizing stock news sentiment and price data. The project involves fetching news data using the FinViz API, analyzing sentiment, exporting stock prices, and generating interactive visualizations.

## Project Overview

1. **`get_news.py`**: Fetches the latest news articles for a list of stock tickers from FinViz and saves them to CSV files.
2. **`analyze_sentiment.py`**: Analyzes sentiment of news articles and appends sentiment scores to the corresponding CSV files.
3. **`export.py`**: Exports stock price data from FinViz to a CSV file at regular intervals.
4. **`bothplot.py`**: Plots combined sentiment scores and stock prices over time for multiple tickers.
5. **`clear.py`**: Clears the content of all CSV files in a specified directory.

## Setup

1. **Install Dependencies**:
   Ensure you have the required Python packages installed. You can install them using pip:
   ```bash
   pip install pandas matplotlib requests beautifulsoup4 finvizfinance pyqt5
   
Update FinViz API Token:

Update the export.py script with your FinViz API token. Replace the placeholder token in the URL with your actual token.
Script Details

get_news.py
Fetches news articles for specified stock tickers using the FinViz API and saves them to CSV files.

python get_news.py

Script Details:

Fetches news articles for tickers listed in the tickers variable.
Saves today's articles to individual CSV files for each ticker.
Checks if files already exist and appends data as needed.

analyze_sentiment.py
Analyzes sentiment scores of news articles and appends the results to the existing CSV files.

python analyze_sentiment.py

Script Details:

Reads news articles from CSV files.
Performs sentiment analysis on the article content.
Appends sentiment scores to the existing CSV files.

export.py
Exports stock price data from FinViz to a CSV file at regular intervals.

python export.py

Script Details:

Fetches stock price data from a specified URL.
Appends the data to a CSV file.
Runs periodically based on the specified interval.

bothplot.py
Plots combined sentiment scores and stock prices over time for multiple tickers.

python bothplot.py

Script Details:

Reads sentiment and price data from CSV files.
Plots combined sentiment scores and stock prices for each ticker.
Uses Matplotlib to generate and display the plots.

clear.py
Clears the content of all CSV files in a specified directory. Useful for starting with fresh files each day.

python clear.py

Script Details:

Iterates through all CSV files in the specified directory.
Clears the content of each file.
File Structure
outputs/: Directory where CSV files are saved and cleared. Ensure this path matches the path used in the scripts.
get_news.py: Script to fetch news articles.
analyze_sentiment.py: Script to analyze sentiment.
export.py: Script to export stock price data.
bothplot.py: Script to plot sentiment and price data.
clear.py: Script to clear CSV files.

Notes:

Ensure the output directory specified in the scripts exists.
Adjust time intervals and file paths according to your needs.
Make sure you have the necessary API tokens and permissions to access the FinViz data.
For any issues or feature requests, please open an issue on this repository.

Acknowledgments:

FinViz API
BeautifulSoup
Matplotlib
PyQt5
