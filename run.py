# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
# SCOPE is a constant, thus is written in all capitals
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS=Credentials.from_service_account_file('creds.json')
SCOPED_CREDS=CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT=gspread.authorize(SCOPED_CREDS)
SHEET=GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    get sales figures input from user
    """
    while True:
        print('please enter sales data from the last market')
        print('data should be 6 numbers separated by a coma')
        print('Example:20,30,41,18,23,32\n')
        data_str=input('Enter your data here: ')
        sales_data=data_str.split(',')
        
        if validate_data(sales_data):
            print('data is valid')
            break
    return sales_data

def validate_data(values):
    """
    Validates user data by checking it consist of 6 elements
    transforms string values into integers
    """
    try:
        [int(value) for value in values]
        if len(values)!=6:
            raise ValueError(
                f"exactly 6 values are required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"invalid data {e}, please try again\n")
        return False
    return True

def update_sales_worksheet(data):
    """
    updates sales data worksheet, adds new row with user data
    """
    print('updating sales data\n')
    sales_worksheet=SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print('sales worsheet updated succesfully\n')

data=get_sales_data()
#Converts validated user input data to integers and store it in sales_data array
sales_data=[int(value) for value in data]
update_sales_worksheet(sales_data)