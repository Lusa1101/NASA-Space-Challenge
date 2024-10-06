import pandas as pd

# Step 1: Load the CSV file into a DataFrame
csv_file_path = r'C:\Users\omphu\Documents\Hackathon\NASAHackathon\Data\input_file.csv'  # Replace with your CSV file path
try:
    df = pd.read_csv(csv_file_path)
except FileNotFoundError:
    print(f"File not found at the specified location: {csv_file_path}")
    raise

# Step 2: Define the output Excel file path
excel_file_path = r'C:\Users\omphu\Documents\Hackathon\NASAHackathon\Data\output_file.xlsx'  # Replace with your output path

# Step 3: Convert the DataFrame to an Excel file
try:
    df.to_excel(excel_file_path, index=False, engine='openpyxl')  # Explicitly use the 'openpyxl' engine
    print(f"CSV successfully converted to Excel at: {excel_file_path}")
except Exception as e:
    print(f"Error during conversion: {e}")

