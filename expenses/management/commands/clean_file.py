import pandas as pd
import sys
import os

def clean_excel(input_file):
    output_file='expense_out.csv'
    try:
        # Check if input file exists
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file '{input_file}' not found.")
        
        # Handle Excel file (.xlsx) or CSV file (.csv)
        if input_file.lower().endswith('.xlsx'):
            print("Reading Excel file...")
            df = pd.read_excel(input_file, header=None)  # Read without header
        elif input_file.lower().endswith('.csv'):
            print("Reading CSV file...")
            df = pd.read_csv(input_file, header=None)  # Read without header
        else:
            raise ValueError("Unsupported file format. Only .xlsx and .csv are supported.")
        
        # Find the row index containing the word 'Data'
        header_row_index = df[df.apply(lambda row: row.astype(str).str.contains("Data").any(), axis=1)].index[0]
        
        # Re-read the data starting from the header row
        df_cleaned = pd.read_excel(input_file, header=header_row_index) if input_file.lower().endswith('.xlsx') \
            else pd.read_csv(input_file, header=header_row_index)

        # Drop the third and fourth columns (zero-indexed: columns 2 and 3)
        df_cleaned = df_cleaned.drop(df_cleaned.columns[[2, 3]], axis=1)

        # Drop the column where the header is 'Contabilizzato'
        if 'Contabilizzazione' in df_cleaned.columns:
            df_cleaned = df_cleaned.drop(columns=['Contabilizzazione'])
        
        # Save the cleaned data to the output CSV file
        df_cleaned.to_csv(output_file, index=False)
        print(f"Cleaned file saved to: {output_file}")

    except Exception as e:
        print(f"Error: {e}")
    return output_file

# if __name__ == "__main__":
#     if len(sys.argv) != 3:
#         print("Usage: python3 clean_excel.py <input_file_path> <output_file_path>")
#     else:
#         input_file = sys.argv[1]
#         output_file = sys.argv[2]
#         clean_excel(input_file, output_file)
