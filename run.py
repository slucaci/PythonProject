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
# Dictionary to check the input for the month
MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12
}


class MoneyMonitor:
    def __init__(self):
        self.setup_worksheets()
        # Dictionary for Money Allocation rules
        self.money_rules = {
            '50-30-20': {'needs': 0.50, 'wants': 0.30, 'savings': 0.20},
            '75-15-10': {'needs': 0.75, 'wants': 0.10, 'savings': 0.15},
            '80-20': {'needs': 0.80, 'wants': 0.00, 'savings': 0.20},
            '60-20-20': {'needs': 0.60, 'wants': 0.20, 'savings': 0.20},
            '70-20-10': {'needs': 0.70, 'wants': 0.20, 'savings': 0.10},
            '60-30-10': {'needs': 0.60, 'wants': 0.30, 'savings': 0.10}
        }

    def setup_worksheets(self):
        """
        Create worksheets with headers.
        """
        headers = ["Year", "Month", "Income", "Needs", "Wants", "Savings"]
        sheet_names = ['50-30-20', '75-15-10', '80-20',
                       '60-20-20', '70-20-10', '60-30-10']

        for sheet_name in sheet_names:
            try:
                worksheet = SHEET.worksheet(sheet_name)
                if len(worksheet.get_all_values()) == 0:
                    worksheet.append_row(headers)
                    print(f"Headers added to {sheet_name} worksheet. \n")
            except gspread.exceptions.WorksheetNotFound:
                worksheet = SHEET.add_worksheet(title=sheet_name,
                                                rows=100, cols=20)
                worksheet.append_row(headers)
                print(f"Worksheet {sheet_name} created and headers added. \n")

    def get_input(self):
        """
        Get monthly income, year, and month input from the user.
          Run the while loop to collect a valid year,
          a valid income(which should be greater than 0)
          and a valid month.
        """
        while True:
            try:
                year = input("Please enter the year(e.g. 2024):\n").strip()
                # Checks if the user types an empty input
                if len(year) == 0:
                    raise ValueError("You must enter a valid year")
                year = int(year)
                if year < 2000 or year > datetime.now().year:
                    raise ValueError
                    ("Year must be between 2000 and the current year.")
                break
            # prints a message for invalid number
            except ValueError as e:
                print(f"Invalid input: {e}, please enter a number"
                      " between 2000 and the current year.  \n")
        while True:
            try:
                month = input("Please enter the month(e.g.,"
                              "January, February):\n").strip().lower()
                # Checks if the user types a valid month
                if month not in MONTHS:
                    raise ValueError("Month must be a valid month name")
                break
            # prints a message for invalid month
            except ValueError as e:
                print(f"Invalid input: {e}, please enter a valid month. \n")

        while True:
            try:
                income = input("Please enter your monthly income:\n")
                # Checks if the user types an empty input
                if income == "":
                    raise ValueError("Cannot be left blank")
                income = float(income)
                # Checks if the user types a negative input
                if income <= 0:
                    raise ValueError("Income must be greater than zero")
                break
            # prints a message for invalid number
            except ValueError as e:
                print(f"Invalid input: {e}, "
                      "please enter a positive number. \n")
        return year, month.capitalize(), income

    def calculate_rule(self, income, rule):
        """
        Calculate the amount of money alocation based on each rule.
        """
        needs = income * rule['needs']
        wants = income * rule['wants']
        savings = income * rule['savings']
        return [income, needs, wants, savings]

    def update_worksheet(self, data, worksheet_name):
        """
        Receives a list of integers to be inserted into a worksheet
        Update the relevant worksheet with the data provided
        """

        worksheet_to_update = SHEET.worksheet(worksheet_name)
        # Gets all the values from the worksheet
        year_month_already = worksheet_to_update.get_all_values()
        year = str(data[0])
        month = data[1].lower()
        data_check = False
        """Check if the data is already in the worksheet file,
        if it is, a message will be displayed"""
        for worksheet in year_month_already:
            if worksheet[0] == year and worksheet[1].lower() == month:
                data_check = True
                break
        if not data_check:
            print(f"Updating {worksheet_name} worksheet... \n")
            worksheet_to_update.append_row(data)
            print(f"{worksheet_name} worksheet updated successfully. \n")
            return True
        return False

    def update_categories(self, year, month, income, rule_name, rule):
        """
        Update the amount of money in the corresponding rule worksheet.
        """
        needs = income * rule['needs']
        wants = income * rule['wants']
        savings = income * rule['savings']
        data = [year, month, income, needs, wants, savings]
        self.update_worksheet(data, rule_name)

    def main(self):
        """Run all program functions"""
        print("Welcome to Money Monitor Data Automation. \n")
        year, month, income = self.get_input()
        # Calculate the amount of money for all rules.
        data_updated = False
        for money_rule, rule in self.money_rules.items():
            money = self.calculate_rule(income, rule)
            row_money = [year, month] + [money_rule]
            if self.update_categories(year, month, income, money_rule, rule):
                data_updated = True
        if not data_updated:
            print(f"Budget rules for {year} and {month} already exist.\n")
            return


money_monitor = MoneyMonitor()
money_monitor.main()
