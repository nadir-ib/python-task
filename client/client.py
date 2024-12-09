import argparse
import requests
import pandas as pd
from datetime import datetime
from config.config import SERVER_URL
from utils.excel_utils import generate_excel

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process vehicle CSV and generate Excel file.")
    parser.add_argument("-k", "--keys", nargs="+", required=True, help="Keys to include as additional columns")
    parser.add_argument("-c", "--colored", action="store_true", help="Enable row coloring")
    parser.add_argument("csv_file", help="Path to the CSV file")
    return parser.parse_args()

def send_csv_to_server(csv_path):
    with open(csv_path, 'rb') as file:
        response = requests.post(SERVER_URL, files={"file": file})
    response.raise_for_status()


   
    return response.json()
    # return res


if __name__ == "__main__":
    args = parse_arguments()

    try:
        # Send CSV to the server
        server_response = send_csv_to_server(args.csv_file)
        # Generate Excel file
        output_file = f"vehicles_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
        generate_excel(server_response, args.keys, args.colored, output_file)
        print(f"Excel file generated: {output_file}")
    except Exception as e:
        print(f"Error: {e}")

