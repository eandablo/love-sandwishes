# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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
        if len(values) != 6:
            raise ValueError(
                f"exactly 6 values are required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"invalid data {e}, please try again\n")
        return False
    return True

def update_worksheet(data,worksheet):
    """
    updates selected worksheet, adds new row in data
    """
    print(f'updating {worksheet} data\n')
    updated_worksheet=SHEET.worksheet(worksheet)
    updated_worksheet.append_row(data)
    print(f'{worksheet} worsheet updated succesfully\n')

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print('calculating surplus data ...')
    stock=SHEET.worksheet('stock').get_all_values()
    stock_row=stock[-1]
    surplus_data=[]
    for stock,sales in zip(stock_row,sales_row):
        surplus=int(stock)-sales
        surplus_data.append(surplus)
    return surplus_data

def get_last_five_sales_data():
    """
    Collects columns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data
    as a list of list
    """
    sales=SHEET.worksheet('sales')

    columns=[]
    for ind in range(1,7):
        column=sales.col_values(ind)
        columns.append(column[-5:])
    return columns

def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print('calculating stock data')
    new_stock_data=[]
    for column in data:
        int_column=[int(num) for num in column]
        average=sum(int_column)/len(int_column)
        stock_num=1.1*average
        new_stock_data.append(round(stock_num))
    return new_stock_data

def main():
    """
    Runs all program functions
    """
    data=get_sales_data()
    #Converts validated user input data to integers and store it in sales_data array
    sales_data=[int(value) for value in data]
    update_worksheet(sales_data,'sales')
    new_surplus_data=calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data,'surplus')
    sales_columns=get_last_five_sales_data()
    stock_data=calculate_stock_data(sales_columns)
    update_worksheet(stock_data,'stock')

print('welcome to love sandwiches project')
main()
