import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import pandas as pd

SCOPE = ['https://spreadsheets.google.com/feeds']

def getSheetCredentials(pathAPIJson):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name(pathAPIJson, scope)

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    
    return sheet

def numberToLetters(q):
    q = q - 1
    result = ''
    while q >= 0:
        remain = q % 26
        result = chr(remain+65) + result;
        q = q//26 - 1
    return result

def getSpreadsheet(sheet, spreadsheetId, sheetName):
    result = sheet.values().get(spreadsheetId=spreadsheetId,
                                    range=sheetName+"!A1:Z1000").execute()
    values = result.get('values', [])

    dataframe = pd.DataFrame(values[1:], columns=values[0])

    return dataframe

def insertSpreadsheet(sheet, df):

    columns = df.columns.values.tolist()
    # selection of the range that will be updated
    cellList = sheet.range('A1:'+numberToLetters(len(columns))+'1')
    # modifying the values in the range
    for cell in cellList:
        val = columns[cell.col-1]
        if type(val) is str:
            val = val
        cell.value = val
    # update in batch
    sheet.update_cells(cellList)

    ############## VALUES ##############
    # number of lines and columns
    numLines, numColumns = df.shape
    # selection of the range that will be updated
    cell_list = sheet.range('A2:'+ numberToLetters(numColumns)+str(numLines+201))
    # modifying the values in the range
    for cell in cellList:
        try:
            val = df.iloc[cell.row-2,cell.col-1]
            if type(val) is str:
                val = val

        except:
            val = ""
        cell.value = val
    # update in batch
    sheet.update_cells(cellList)
    
def clearSpreadsheet(sheet, nLin, nCol):
    # selection of the range that will be updated
    cellList = sheet.range('A1:'+numberToLetters(nCol)+str(nLin))
    # modifying the values in the range
    for cell in cellList:
        val=""
        cell.value = val
    # update in batch
    sheet.update_cells(cellList)

#get sheet credentials
sheet = getSheetCredentials('/home/iazzari/repositorios/scripts/scripts_investimento/google_sheet.json')

#using my sheet: https://docs.google.com/spreadsheets/d/1MdwfFFObicVn9KXEJHgtFL40xgMoWxs-LNQAxxzY4bw/edit#gid=0

#get df of sheet values 
df = getSpreadsheet(sheet, '1MdwfFFObicVn9KXEJHgtFL40xgMoWxs-LNQAxxzY4bw', 'new_API')

#df