#from expense import Expense
from clean_file import clean_excel
from intesa import redirect_to_intesa_online_banking
from unicredit import redirect_to_unicredit_online_banking
import calendar
import datetime
import os
import csv
import pandas as pd

def main():
    print(f"Running Expense Tracker!")
    expense_file_path = "expenses.csv"

    #get user banking service
    banking_service = ask_banking_service()
    if banking_service == "intesa":

        redirect_to_intesa_online_banking()

    elif banking_service == "unicredit":

        redirect_to_unicredit_online_banking()
    
    #get user balance and last month expenses
    total_balance,past_expenses= ask_account_balance_and_past_expenses()
    # Get user input for expense.
    choice=input("Do you want to add any new expense?")

    if choice== "yes":
        data=input("Expense date: ")

        location=input("Location: ")

        category=input("Category: ")

        currency=input("Currency: ")
        
        importo=float(input("Amount: "))

        new_expense=Expense(data,location,category,currency,importo)
        get_user_expense(past_expenses,new_expense)
    # else:
    #     # Read file and summarize expenses.
    #     summarize_expenses(expense_file_path, balance)

def ask_banking_service():
    """
    Prompt the user to select their banking service.
    Returns:
        str: The chosen banking service ('intesa' or 'unicredit').
    """
    print("Please select your online banking service:")
    print("  1. Intesa Sanpaolo")
    print("  2. Unicredit")
    while True:
        choice = input("Enter the number of your choice: ").strip()
        if choice == "1":
            return "intesa"
        elif choice == "2":
            return "unicredit"
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")

import os
import pandas as pd

def ask_account_balance_and_past_expenses():
    """
    Prompt the user to enter their current account balance and the path to their last month's expenses CSV file.
    Creates a new CSV file incorporating the data from the input file and returns the balance.
    Returns:
        float: The entered account balance.
    """
    while True:
        # Prompt for account balance
        try:
            balance = float(input("Please enter your current account balance (in €): ").strip())
            if balance < 0:
                raise ValueError("Account balance cannot be negative.")
        except ValueError as e:
            print(f"\u274c Invalid input: {e}")
            continue  # Re-prompt for balance

        # Prompt for file path
        while True:
            
            file_path_ex = input("Please enter the path to your last month's expenses: ").strip()
            #clean the file and bring it into a csv file with just the essential data
            file_path=clean_excel(file_path_ex)
            if os.path.exists(file_path):
                return balance, file_path
            else:
                print(f"\u274c File not found: {file_path}. Please try again.")

    
import csv

def get_user_expense(expense_file_path, expense):
    """
    Adds a new expense to the provided expense CSV file.

    Parameters:
    - expense_file_path (str): Path to the expense CSV file.
    - expense (Expense): An instance of the Expense class to add.
    """
    try:
        # Open the file in append mode
        with open(expense_file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Append the expense fields as a new row
            writer.writerow([
                str(expense.data),       # Date in 'YYYY-MM-DD' format
                str(expense.operazione),   # Location
                str(expense.categoria),   # Category
                str(expense.valuta),   # Currency
                str(expense.importo)      # Amount
            ])
        
        print(f"Expense for '{expense.data}' at '{expense.operazione}' added successfully.")
    
    except Exception as e:
        print(f"Error adding expense: {e}")


def update_expenses_from_excel(new_file_path, existing_file_path="expenses.csv"):
    """
    Updates the expenses CSV file using data from a structured Excel file.

    Args:
        new_file_path (str): Path to the Excel file with new transactions.
        existing_file_path (str): Path to the preexisting CSV file (default: 'expenses.csv').
    """
    # Load the Excel file and identify the correct header row
    df = pd.read_excel(new_file_path, sheet_name="Lista Operazione", skiprows=17)
    df = df.dropna(subset=["Data", "Operazione", "Importo"])  # Keep rows with meaningful data

    # Select relevant columns
    df = df[["Data", "Operazione", "Categoria", "Importo"]]
    df.columns = ["Date", "Description", "Category", "Amount"]  # Standardize column names

    # Format the "Amount" column to ensure numeric values
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Check if the existing CSV file exists
    if os.path.exists(existing_file_path):
        # Load the existing file
        existing_df = pd.read_csv(existing_file_path)
        # Append new data
        combined_df = pd.concat([existing_df, df], ignore_index=True)
    else:
        # No existing file, use new data only
        print("No preexisting file found. Creating a new one.")
        combined_df = df

    # Save the updated data back to the CSV
    combined_df.to_csv(existing_file_path, index=False)
    print(f"✅ Expenses updated successfully! File saved at {existing_file_path}")



def green(text):
    return f"\033[92m{text}\033[0m"


if __name__ == "__main__":
    main()