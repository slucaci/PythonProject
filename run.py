import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('money-monitor')


MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12
}

class MoneyMonitor:
    def __init__(self):
        self.setup_worksheets()

    def setup_worksheets(self):
        """
        Create worksheets with headers.
        """
        headers = ["Year", "Month", "Income", "Needs", "Wants", "Savings"]
        sheet_names = ['50-30-20', '75-15-10', '80-20', '60-20-20', '70-20-10', '60-30-10']

        for sheet_name in sheet_names:
            try:
                worksheet = SHEET.worksheet(sheet_name)
                if len(worksheet.get_all_values()) == 0:
                    worksheet.append_row(headers)
                    print(f"Headers added to {sheet_name} worksheet")
            except gspread.exceptions.WorksheetNotFound:
                worksheet = SHEET.add_worksheet(title=sheet_name, rows=100, cols=20)
                worksheet.append_row(headers)
                print(f"Worksheet {sheet_name} created and headers added")
    def get_input(self):
        """
        Get monthly income, year, and month input from the user.
        """
        while True:
            try:
                year = int(input("Please enter the year(e.g. 2024): "))
                if year < 2000 or year > datetime.now().year:
                    raise ValueError("Year must be between 2000 and the current year.")
                break
            except ValueError as e:
                print(f"Invalid input: {e}, please enter a valid year")
        
        while True:
            try:
                month = input("Please enter the month(e.g., January, February): ").strip().lower()
                if month not in MONTHS:
                    raise ValueError("Month must be a valid month name.")
                break
            except ValueError as e:
                print(f"Invalid input: {e}, please enter a valid month")
        while True:
            try:
                income = float(input("Please enter your monthly income: "))
                if income <=0:
                    raise ValueError("Income must be greater than zero.")
                break
            except ValueError as e:
                print(f"Invalid input: {e}, please enter another one")
        return year, month, income

    def main(self):
        """Run all program functions"""
        data = self.get_input()
        print(data)

print("Welcome to Money Monitor Data Automation.")
money_monitor = MoneyMonitor()
money_monitor.main()