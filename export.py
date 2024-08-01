import datetime
import requests
import os
import pandas as pd
import io
import time
from typing import List
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Define the URL to fetch the data from
URL = "https://elite.finviz.com/export.ashx?v=111&t=AMZN,AAPL,GOOGL&auth=ab4e8b66-99af-4c54-b834-10d199e1e3d5"
# Define the path where the exported data will be saved
EXPORT_FILE_PATH = os.path.expanduser(r"/Users/apspa/Documents/PSU/RESEARCH PROJECT/Code/outputs/export.csv")
# Ensure the directory exists
os.makedirs(os.path.dirname(EXPORT_FILE_PATH), exist_ok=True)

def export_data(url: str, output_path: str):
    """
    Fetches data from the provided URL and appends it to the specified output file.
    If the file already exists, it concatenates the new data with the existing data.
    """
    response = requests.get(url)
    if response.status_code == 200:
        # Load the new data from the response
        new_data = pd.read_csv(io.StringIO(response.text))
        current_datetime = datetime.datetime.now()
        new_data['Exported_At'] = current_datetime
        
        # Check if the output file already exists and is not empty
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            try:
                existing_data = pd.read_csv(output_path)
                combined_data = pd.concat([existing_data, new_data])
            except pd.errors.EmptyDataError:
                # If the file is empty or cannot be read, use only the new data
                combined_data = new_data
        else:
            combined_data = new_data
        
        # Save the combined data to the output file
        combined_data.to_csv(output_path, index=False)
        print(f"Data successfully exported to {output_path}")
    else:
        print(f"Failed to fetch data: {response.status_code}")

def export_data_repeatedly(url: str, output_path: str, duration_minutes: int, interval_minutes: int):
    """
    Repeatedly fetches and appends data to the output file at the specified interval.
    Continues for the given duration in minutes.
    """
    start_time = time.time()
    end_time = start_time + duration_minutes * 60
    
    while time.time() < end_time:
        export_data(url, output_path)
        time.sleep(interval_minutes * 60)  # Wait for the specified interval

class StockPlotter(QMainWindow):
    def __init__(self, csv_file: str):
        """
        Initializes the main window for plotting stock prices.
        """
        super().__init__()
        self.setWindowTitle("Stock Price Plotter")
        self.setGeometry(100, 100, 1200, 800)

        # Create a central widget and set a layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create a matplotlib figure and axis
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        # Plot the data from the CSV file
        self.plot_data(csv_file)

    def plot_data(self, csv_file: str):
        """
        Plots stock prices from the CSV file.
        """
        try:
            # Load data from CSV file
            df = pd.read_csv(csv_file)
        except pd.errors.EmptyDataError:
            print(f"Error: The file {csv_file} is empty or cannot be read.")
            return

        # Convert 'Exported_At' to datetime and drop rows with invalid dates
        df['Exported_At'] = pd.to_datetime(df['Exported_At'], errors='coerce')
        df = df.dropna(subset=['Exported_At'])  # Drop rows where 'Exported_At' is NaT

        # Clear existing plots
        self.ax.clear()

        # Plot stock prices for each ticker
        for ticker in df['Ticker'].unique():
            ticker_df = df[df['Ticker'] == ticker]
            self.ax.plot(ticker_df['Exported_At'], ticker_df['Price'], label=f'{ticker} Price')

        # Set plot labels and title
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Stock Price')
        self.ax.set_title('Stock Prices Over Time')
        self.ax.legend()
        self.figure.tight_layout()
        self.canvas.draw()

def main():
    """
    Main function to run the data export and plotting.
    """
    # Path to the CSV file
    csv_file = os.path.expanduser(r"/Users/apspa/Documents/PSU/RESEARCH PROJECT/Code/outputs/export.csv")
    
    # Export data every 15 minutes for 5 hours (300 minutes)
    export_data_repeatedly(URL, csv_file, duration_minutes=15, interval_minutes=1)
    
    # Initialize and run the PyQt application
    app = QApplication([])
    plotter = StockPlotter(csv_file)
    plotter.show()
    app.exec_()

if __name__ == "__main__":
    main()
