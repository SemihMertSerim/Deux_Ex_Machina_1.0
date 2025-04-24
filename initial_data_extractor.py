from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import time
import pandas as pd
import mysql.connector
#to add worksheets
def add_new_worksheet(spreadsheet_id, name_of_the_stock, row_count=200, column_count=5):
    # Authenticate using the credentials file
    try:
        credentials = Credentials.from_service_account_file(
        "../Deux_Ex_Machina_1.0/credentials.json",
            scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"])

    # Build the Sheets API service
        service = build('sheets', 'v4', credentials=credentials)

    # Define the request body for adding a new sheet
        request_body = {
            "requests": [
            {
                    "addSheet": {
                    "properties": {
                        "title": name_of_the_stock,  # Name of the worksheet
                        "sheetType": "GRID",  # Grid type
                        "gridProperties": {
                            "rowCount": row_count,
                            "columnCount": column_count}}}}]}
    # Sets the 100 days stocks closing price data
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=request_body).execute()
    # Extract and print the new sheet's ID
        added_sheet = response.get('replies')[0].get('addSheet').get('properties')
        new_worksheet_properties = [ name_of_the_stock, added_sheet['sheetId']]

    except Exception as e:
        print(f"An error occurred while adding the new worksheet: {e}")
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=f"{name_of_the_stock}!A1",
        valueInputOption="USER_ENTERED",
        body={"values": [
            [f"=GOOGLEFINANCE(\"{name_of_the_stock}\";\"close\" ;TODAY() - 200 ; TODAY()-2)"]]}).execute()
    time.sleep(0.2)
    added_sheet = response.get('replies')[0].get('addSheet').get('properties')
    new_worksheet_properties = [name_of_the_stock, added_sheet['sheetId']]
    return new_worksheet_properties[1]
#return last 10 days price
def google_sheets_ltd_price_recorder(sheet_id,worksheet_name):
    cred = Credentials.from_service_account_file(
        "../Deux_Ex_Machina_1.0/credentials.json",
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"])
    # Sets a name to the sheet
    service = build("sheets", "v4", credentials=cred)
    range_to_fetch = f"{worksheet_name}!B:B"
    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range=range_to_fetch
    ).execute()

    # Extract the values
    values = result.get("values",[])
    last_values_list = values[-10:]
    return_list = []
    for value in last_values_list:
        return_list.append(float(value[0]))
    return return_list
# return the dates of the data
def google_sheets_day_recorder():
    cred = Credentials.from_service_account_file(
        "../Deux_Ex_Machina_1.0/credentials.json",
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"])
    # Sets a name to the sheet
    service = build("sheets", "v4", credentials=cred)
    date_result = service.spreadsheets().values().get(
        spreadsheetId="1Pt3AxCxEiI-Wn4vD6jJNMuUbGzCaKDXUiSC8-u96YsM",
        range=f"Sheet1!A:A").execute()
    date_values = date_result.get("values", [])
    return date_values[-10:]
#to calculate rsi
def calculate_rsi(sheet_id,worksheet_name):
    cred = Credentials.from_service_account_file(
        "../Deux_Ex_Machina_1.0/credentials.json",
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"])
    # Sets a name to the sheet
    sheets_service = build("sheets", "v4", credentials=cred).spreadsheets()
    # to calculate gains
    b_column =sheets_service.values().get(
        spreadsheetId=sheet_id,
        range=f"{worksheet_name}!B2:B",
    ).execute()
    # Extract only the list of data
    try:
        b_column_values = b_column.get('values', [])  # Safely handle if 'values' key is missing
        flat_values = [item[0] for item in b_column_values if item]  # Flatten the list of lists
        # Convert strings to floats
        float_values = [float(value) for value in flat_values if
                        value.replace('.', '', 1).isdigit()]  # Handles valid floats
        differences = [round(float_values[i + 1] - float_values[i],3) for i in range(len(float_values) - 1)]
        # Prepare C and D column data
        gains_column = []  # Will hold values for column C
        loses_column = []  # Will hold values for column D

        for diff in differences:
            if diff > 0:
                gains_column.append(diff)  # Add value to column C
                loses_column.append(0)  # Add 0 to column D
            else:
                gains_column.append(0)  # Add 0 to column C
                loses_column.append(abs(diff))  # Add the absolute value to column D
        average_G =[]
        average_L = []
        for g in range(len(gains_column)+1):
            if g == 14:
                average_G.append(round(sum(gains_column[g-14:g])/14, 8))
            elif g > 14:
                average_G.append(round((average_G[-1]*13+gains_column[g-1])/14, 8))
        for l in range(len(loses_column)+1):
            if l == 14:
                average_L.append(round(sum(loses_column[l-14:l])/14, 8))
            elif l > 14:
                average_L.append(round((average_L[-1] * 13 + loses_column[l - 1])/14, 8))
        rsi = []

        for row in range(len(average_L)):
            rsi.append(round(100 - (100 / (1+(average_G[row] / average_L[row]))), 2))
        last = rsi[-10:]
        last.append(average_G[-1])
        last.append(average_L[-1])
        return last
    except Exception as e:
        print(f"An error occurred while calculating RSI: {e}")
        return 0
#to delete worksheets
def delete_worksheet(spreadsheet_id, Worksheet_id):
    """
    Delete a worksheet from a Google Spreadsheet.
    Args:
        spreadsheet_id: The ID of the spreadsheet.
        sheet_id: The ID of the worksheet to delete.
    """
    # Authenticate using the credentials file
    credentials = Credentials.from_service_account_file(
        "../Deux_Ex_Machina_1.0/credentials.json",
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"])
    service = build("sheets", "v4", credentials=credentials)
    # Define the request body to delete the worksheet
    request_body = {
        "requests": [
            {"deleteSheet": {
                    "sheetId": Worksheet_id}}]}
    try:
        # Execute the batchUpdate request
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=request_body
        ).execute()
    except Exception as e:
        print(f"An error occurred while deleting the worksheet: {e}")
#to calculate initial 10 days stock datas
def initial_10_days_stock_datas(sheet_id,name_of_the_stock):
    the_list = []
    the_list.append(f"{name_of_the_stock}")
    worksheet_id = add_new_worksheet(sheet_id,name_of_the_stock)
    the_list.extend(google_sheets_ltd_price_recorder(sheet_id,name_of_the_stock))
    the_list.extend(calculate_rsi(sheet_id,name_of_the_stock))
    delete_worksheet(sheet_id,worksheet_id)
    time.sleep(0.7)
    return the_list
#adds a new row to the database
def filling_row(the_names_list,table_name):
    '''
        the_names_list = "the_names_list.csv"
        table_name = "the_table_name"
       This function adds a new row to the database
       the_filling_list = [Symbol,Price10th,Price9th,Price8th,Price7th,Price6th,Price5th,Price4th,Price3th,Price2th,Price1th,Rsi10th,Rsi9th,Rsi8th,Rsi7th,Rsi6th,Rsi5th,Rsi4th,Rsi3th,Rsi2th,Rsi1th,AG,AL]
       '''

    print("Are you sure the stock market you want to access is closed ? yes/no")
    answer = input()
    if answer == "yes":
        pass
    else:
        return 0
    sheet_id = pd.read_csv("google_sheet_IDs.csv")["Id"][0]
    name_of_the_stoc = pd.read_csv(the_names_list)["Symbol"]
    myDB = mysql.connector.connect(host='localhost',
                                   user='root', passwd='Yuceisa@jaruselam0000', port='3306',
                                   database='deux')
    mycursor = myDB.cursor()
    for name in name_of_the_stoc:
        try:
            the_filling_list = initial_10_days_stock_datas(sheet_id=sheet_id,name_of_the_stock=name)
            mycursor.execute(f"INSERT INTO {table_name} (queue,Symbol,Price10th,Price9th,Price8th,Price7th,Price6th,Price5th,Price4th,Price3th,Price2th,Price1th,Rsi10th,Rsi9th,Rsi8th,Rsi7th,Rsi6th,Rsi5th,Rsi4th,Rsi3th,Rsi2th,Rsi1th,AG,AL)"
                     f"VALUES (DEFAULT,"
                     f"'{the_filling_list[0]}',"
                     f"{the_filling_list[1]},"
                     f"{the_filling_list[2]},"
                     f"{the_filling_list[3]},"
                     f"{the_filling_list[4]},"
                     f"{the_filling_list[5]},"
                     f"{the_filling_list[6]},"
                     f"{the_filling_list[7]},"
                     f"{the_filling_list[8]},"
                     f"{the_filling_list[9]},"
                     f"{the_filling_list[10]},"
                     f"{the_filling_list[11]},"
                     f"{the_filling_list[12]},"
                     f"{the_filling_list[13]},"
                     f"{the_filling_list[14]},"
                     f"{the_filling_list[15]},"
                     f"{the_filling_list[16]},"
                     f"{the_filling_list[17]},"
                     f"{the_filling_list[18]},"
                     f"{the_filling_list[19]},"
                     f"{the_filling_list[20]},"
                     f"{the_filling_list[21]},"
                     f"{the_filling_list[22]})")
        except Exception as e:
            print("There is an error:", e)
    myDB.commit()
    mycursor.close()
    myDB.close()