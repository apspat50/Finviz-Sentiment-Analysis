import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
from finvader import finvader
import time

# Define the input directory containing CSV files for each ticker
input_dir = os.path.expanduser(r"/Users/apspa/Documents/PSU/RESEARCH PROJECT/Code/outputs/")

# Define the output directory to save sentiment analysis results
output_dir = os.path.expanduser(r"/Users/apspa/Documents/PSU/RESEARCH PROJECT/Code/outputs/")

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Function to analyze sentiment of text
def analyze_sentiment(text: str) -> float:
    """
    Analyze the sentiment of the given text and return the sentiment score.
    
    Args:
        text (str): The text to analyze.
    
    Returns:
        float: The sentiment score.
    """
    # Perform sentiment analysis using Finvader
    sentiment_result = finvader(text, use_sentibignomics=True, use_henry=True, indicator='compound')
    
    # Check if the result is a dictionary and contains 'compound' key
    if isinstance(sentiment_result, dict) and 'compound' in sentiment_result:
        return sentiment_result['compound']
    return sentiment_result if isinstance(sentiment_result, float) else 0.0

# Function to fetch article content from a URL
def fetch_article_content(url: str) -> str:
    """
    Fetch the content of an article from a given URL.
    
    Args:
        url (str): The URL of the article.
    
    Returns:
        str: The content of the article.
    """
    # Define headers to mimic a real browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        # Make a request to the article URL
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract all paragraph text from the article
            paragraphs = soup.find_all('p')
            article_text = ' '.join([para.get_text() for para in paragraphs])
            return article_text
        else:
            print(f"Failed to fetch article from {url}: {response.status_code}")
            return ""
    except Exception as e:
        print(f"Error fetching article from {url}: {e}")
        return ""

# Process each CSV file in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.csv') and not filename.endswith('_with_sentiment.csv'):
        # Define the input and output file paths
        input_file_path = os.path.join(input_dir, filename)
        output_file_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_with_sentiment.csv")
        
        # Print debugging information
        print(f"Processing file: {input_file_path}")
        print(f"Output file path: {output_file_path}")
        
        # Read the CSV file into a DataFrame
        try:
            news_df = pd.read_csv(input_file_path)
        except pd.errors.EmptyDataError:
            print(f"Skipping empty file: {input_file_path}")
            continue
        
        # Print the column names to debug
        print(f"Columns in {filename}: {news_df.columns.tolist()}")

        # Check if required columns exist
        required_columns = ['Link', 'Title']
        missing_columns = [col for col in required_columns if col not in news_df.columns]

        if missing_columns:
            print(f"Missing columns {missing_columns} in {filename}")
            continue  # Skip this file or handle it as needed

        # Initialize lists to store sentiment scores
        title_sentiments = []
        content_sentiments = []
        combined_sentiments = []

        # Loop through each URL in the DataFrame
        for index, row in news_df.iterrows():
            try:
                url = row['Link']
                title = row['Title']
                print(f"Processing URL: {url}")
                
                # Fetch article content
                content = fetch_article_content(url)
                
                if content and title:
                    # Analyze sentiment for title and content
                    title_sentiment = analyze_sentiment(title)
                    content_sentiment = analyze_sentiment(content)
                    
                    # Calculate combined sentiment as the average of title and content sentiments
                    combined_sentiment = (title_sentiment + content_sentiment) / 2
                    
                    # Append results to lists
                    title_sentiments.append(title_sentiment)
                    content_sentiments.append(content_sentiment)
                    combined_sentiments.append(combined_sentiment)
                else:
                    # Handle cases where content could not be fetched
                    title_sentiments.append(None)
                    content_sentiments.append(None)
                    combined_sentiments.append(None)
                
                # Optional: delay to avoid overwhelming the server
                time.sleep(1)  # Adjust delay as needed
            except KeyError as e:
                print(f"Error processing row {index}: {e}")
                continue

        # Add sentiment scores to DataFrame
        news_df['Title_Sentiment'] = title_sentiments
        news_df['Content_Sentiment'] = content_sentiments
        news_df['Combined_Sentiment'] = combined_sentiments

        # Check if the output file exists and is not empty
        if os.path.isfile(output_file_path):
            if os.stat(output_file_path).st_size == 0:
                print(f"File is empty, writing new data: {output_file_path}")
                news_df.to_csv(output_file_path, index=False)
            else:
                print(f"Appending to existing file: {output_file_path}")
                # If the file exists and is not empty, read it first
                existing_df = pd.read_csv(output_file_path)
                # Concatenate the new data with the existing data
                combined_df = pd.concat([existing_df, news_df], ignore_index=True)
                # Save the combined data to the file, overwriting it
                combined_df.to_csv(output_file_path, index=False)
        else:
            print(f"Creating new file: {output_file_path}")
            # If the file doesn't exist, just save the new data
            news_df.to_csv(output_file_path, index=False)

print("All sentiment analyses have been completed and saved.")
