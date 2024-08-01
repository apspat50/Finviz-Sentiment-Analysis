import os

def clear_all_csv_files(directory_path: str):
    """ Clears the content of all CSV files in the specified directory. """
    # Check if the specified directory exists
    if os.path.exists(directory_path):
        # Iterate through all files in the directory
        for filename in os.listdir(directory_path):
            # Check if the file has a .csv extension
            if filename.endswith('.csv'):
                # Construct the full file path
                file_path = os.path.join(directory_path, filename)
                # Open the file in write mode (which clears the content)
                with open(file_path, 'w') as file:
                    file.write('')  # Clear the content of the file
                # Print a confirmation message
                print(f"File {file_path} has been cleared.")
    else:
        # Print an error message if the directory does not exist
        print(f"Directory {directory_path} does not exist.")

# Define the path to the directory containing the CSV files
csv_directory = os.path.expanduser(r"/Users/apspa/Documents/PSU/RESEARCH PROJECT/Code/outputs")

# Call the function to clear all CSV files in the directory
clear_all_csv_files(csv_directory)
