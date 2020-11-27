from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from time import sleep
import os
from datetime import date
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from datetime import time
# import re

def get_sheet_credentials(sheet_name):
    creds = ServiceAccountCredentials.from_json_keyfile_name('<path to json credential>', SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open_by_key('1MdwfFFObicVn9KXEJHgtFL40xgMoWxs-LNQAxxzY4bw').worksheet(sheet_name)
    return sheet

def numberToLetters(q):
    q = q - 1
    result = ''
    while q >= 0:
        remain = q % 26
        result = chr(remain+65) + result;
        q = q//26 - 1
    return result


def insertSpreadsheet(sheet, df):

    columns = df.columns.values.tolist()
    # selection of the range that will be updated
    cell_list = sheet.range('A1:'+numberToLetters(len(columns))+'1')
    # modifying the values in the range
    for cell in cell_list:
        val = columns[cell.col-1]
        if type(val) is str:
            val = val
        cell.value = val
    # update in batch
    sheet.update_cells(cell_list)

    ############## VALUES ##############
    # number of lines and columns
    num_lines, num_columns = df.shape
    # selection of the range that will be updated
    cell_list = sheet.range('A2:'+ numberToLetters(num_columns)+str(num_lines+201))
    # modifying the values in the range
    for cell in cell_list:
        try:
            val = df.iloc[cell.row-2,cell.col-1]
            if type(val) is str:
                val = val

        except:
            val = ""
        cell.value = val
    # update in batch
    sheet.update_cells(cell_list)
    
def clearSpreadsheet(sheet, n_lin, n_col):
    # selection of the range that will be updated
    cell_list = sheet.range('A1:'+numberToLetters(n_col)+str(n_lin))
    # modifying the values in the range
    for cell in cell_list:
        val=""
        cell.value = val
    # update in batch
    sheet.update_cells(cell_list)

def enter_in_website():
    DRIVER.get("https://www.fundsexplorer.com.br")
    sleep(5)
    DRIVER.find_element_by_xpath("//*[@id='btn-signin']").send_keys(Keys.ENTER)


    sleep(5)
    DRIVER.find_element_by_id("email-signin").send_keys(Keys.ENTER)
    DRIVER.find_element_by_id("email-signin").send_keys(USERNAME)
    sleep(5)
    DRIVER.find_element_by_id("password-signin").send_keys(PASSWORD)
    sleep(5)
    DRIVER.find_element_by_id("signin-user").send_keys(Keys.ENTER)

    
def get_df_values(tupla, df_final):
    variavel = tupla[0]
    link = tupla[1]
    
    
    DRIVER.get(link)
    table_id = DRIVER.find_element_by_tag_name("table")
    sleep(20)
    rows_headers = table_id.find_element_by_tag_name("tr")


    lista_headers = []
    lista_values = []

    for words in rows_headers.text.replace('RANKING ', '').split('\n'):
        lista_headers.append(words)

    for words in lista_headers:
        lista_values = words.split('TICKER')


    lista_values[0] = 'TICKER'
    lista_values[1] = lista_values[1].lstrip().rstrip()
    columns = lista_values


    rows_table = table_id.find_element_by_tag_name("tbody")
    rows_table = rows_table.text.replace('R$','').replace(' m²','').replace('m²','').replace('%','').replace('%','').replace('.','').replace(',','.')

    lista_rows = []
    lista_values = []


    for words in rows_table.split('\n'):
        first_4_digits = ''.join([i for i in words[:4] if not i.isdigit()])
        complete = first_4_digits + words[4:]
        tupla_row = [complete[:8].lstrip().rstrip(), complete[8:].lstrip().rstrip()]
        lista_rows.append(tupla_row)

    df = pd.DataFrame(lista_rows, columns = columns)


    df.reset_index(drop=True)
    
    
    if len(df_final.index) > 0:
        df_anterior = df_final
        df_final = pd.merge(df_anterior, df, how='left', on='TICKER')
        return df_final
    
    else:
        return df

start_date=datetime.now()

SCOPE = ['https://spreadsheets.google.com/feeds']

PATH = '<Path to chromedriver>chromedriver'

DRIVER = webdriver.Chrome(PATH)

USERNAME = "<login>"

PASSWORD = "<password>"

enter_in_website()
sleep(5)

df_final = pd.DataFrame()

lista_de_estudos = [['tipo_de_fundo', 'https://www.fundsexplorer.com.br/estudos/1nToUW3V8WmRkpFNqmGXuUgh']
                    ,['inadimplencia', 'https://www.fundsexplorer.com.br/estudos/wYZjo9KP4umD3ypUtMUJbH2C']
                    ,['abl', 'https://www.fundsexplorer.com.br/estudos/ACoGgWk2LqjDRgxWAEFBttxV']
                    ,['patrimonio_liquido', 'https://www.fundsexplorer.com.br/estudos/vKQiRSdeHSTMYyaG9qC2VcFc']
                    ,['dy_acumulado_12_m', 'https://www.fundsexplorer.com.br/estudos/eYRZiNk5YMKnVoE2hJV83mtB']
                    ,['valor_patrimonial', 'https://www.fundsexplorer.com.br/estudos/rzW9sqTR3kc7mGdw1myWtC95']
                    ,['p/vpa', 'https://www.fundsexplorer.com.br/estudos/ue21pWj7TgoWwoF1QjDhbC4P']
                    ,['vacancia_fisica', 'https://www.fundsexplorer.com.br/estudos/b3L55U5ZXRNk53PHyrBWFfbe']
                    ,['valor_mercado',  'https://www.fundsexplorer.com.br/estudos/U8MK4AuhCmbFqJEwcZDHvxCT']
                    ,['liquidez_diaria', 'https://www.fundsexplorer.com.br/estudos/v6pvPMsCFfHtvCuMkSGctQ83']
                    ,['vacancia_financeira', 'https://www.fundsexplorer.com.br/estudos/wiDJWwom8SebGt4TV7Q1zWGB']
                    ,['segmento', 'https://www.fundsexplorer.com.br/estudos/oeM4HRmkVJCGdaxxZBjUKuy8']
                    ,['administrador', 'https://www.fundsexplorer.com.br/estudos/BYgvbVB9iXde16DwZFQxKEY5']
                    ,['quantidade_imoveis', 'https://www.fundsexplorer.com.br/estudos/gCVLwh4KXUoRgNoGPdjsY3Kw']
                    ,['nome', 'https://www.fundsexplorer.com.br/estudos/XrAXUJSEPWBDrK6sPgk5M21o']
                    ,['publico_alvo', 'https://www.fundsexplorer.com.br/estudos/xjNztby8Bn9dxfYjjrkD8rqi']
                    ,['dy_medio_12_m', 'https://www.fundsexplorer.com.br/estudos/aC41vdqRmXso4AKC3zFhQ9RD']
                   ]

df_final = get_df_values(lista_de_estudos[0], df_final)


for tupla in lista_de_estudos[1:]:
    df_final = get_df_values(tupla, df_final)

df_final.fillna('', inplace=True)
    
df_final['ABL'] = df_final['ABL'].map(lambda x: x.replace(' m²', '').replace('m²', ''))

data = datetime.now().date().isoformat()
data = datetime.strptime(data, '%Y-%m-%d').strftime('%d-%m-%Y')

df_final['data_ultima_modificacao'] = data

sheet = get_sheet_credentials('new_API')

clearSpreadsheet(sheet, 300, 26)

insertSpreadsheet(sheet, df_final)

end_date=datetime.now()

print('tempo em segundos: ' + str((end_date - start_date).total_seconds()))

