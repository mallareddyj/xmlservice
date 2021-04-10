import csv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle


def get_key(url):
    key = url.split("/d/")[-1]
    if "/" in key:
        key = key.split("/")[0]
    return str(key)

def get_csv(url, output_file):

    # global values_input, service
    SAMPLE_SPREADSHEET_ID_input = get_key(url)
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)


    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    res = service.spreadsheets().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input, fields='sheets(data/rowData/values/userEnteredValue,properties(index,sheetId,title))').execute()
    sheetIndex = 0
    sheetName = res['sheets'][sheetIndex]['properties']['title']
    lastRow = len(res['sheets'][sheetIndex]['data'][0]['rowData'])
    lastColumn = max([len(e['values']) for e in res['sheets'][sheetIndex]['data'][0]['rowData'] if e])
    sheet = service.spreadsheets()
    # print("lastRow = " + str(lastRow) + " lastColumn = " + str(lastColumn))
    SAMPLE_RANGE_NAME = 'A1:AA{lastRow}'.format(lastRow = lastRow)
    # print(SAMPLE_RANGE_NAME)
    # result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,range=SAMPLE_RANGE_NAME).execute()
    result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,range = SAMPLE_RANGE_NAME).execute()
    values_input = result_input.get('values', [])

    if not values_input and not values_expansion:
        print('No data found.')
    
    with open(output_file, 'w') as f:
        write = csv.writer(f)
        write.writerow(values_input[0])
        write.writerows(values_input[1:])


if __name__ == '__main__':

    # SAMPLE_RANGE_NAME = 'A1:AA1000'
    # here enter the id of your google sheet
    SAMPLE_SPREADSHEET_ID_input = '1twixOICCAo5eChSu5lCO5VT9Zrc2W4PPlva6axmhgyU'
    output_file = "test.csv"
    get_csv("https://docs.google.com/spreadsheets/d/1qUittqVFvhsIY4JJvqTpkYtOrq6Ws9TZWu1m1Sd07M8/edit#gid=147909294", output_file)
