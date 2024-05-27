import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('money-monitor')

def get_input():
    """
     Get monthly income, year, and month input from the user"""
    while True:
        try:
            year = input("Please enter the year:")
            break
        except ValueError as e:
            print(f"Invalit input: {e}, enter another one")
    
    while True:
        try:
            month = input("Please enter the month")
            break
        except ValueError as e:
            print(f"Invalid input: {e}, please enter another one")
    while True:
        try:
            income = input("Please enter your monthly income")
            break
        except ValueError as e:
            print(f"Invalid input: {e}, please enter another one")
    return year, month, income

def main():
    """Run all program functions"""
    data = get_input()
    print(data)

main()