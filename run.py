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
    print('please enter sales data from the last market')
    print('data should be 6 numbers separated by a coma')
    print('Example:20,30,41,18,23,32\n')
    data_str=input('Enter your data here: ')
    print(f'user data provided is {data_str}')

get_sales_data()