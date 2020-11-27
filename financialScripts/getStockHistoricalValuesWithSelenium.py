#Calling libraries
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import datetime
import pandas as pd


startTimestamp = datetime.datetime.now()

ticker = 'GOOG'
startDate = '01/01/2020'
endDate = '12/09/2020'
pathToChromedriver = '/home/iazzari/repositorios/scripts/scripts_investimento/chromedriver'
DRIVER = webdriver.Chrome(pathToChromedriver)

def closeCookiesAndPopup(timeSleep=20):
    sleep(5)
    try:
        #click in accept terms of cookies
        acceptCookies = WebDriverWait(DRIVER, timeSleep).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/div[2]/i")))
        acceptCookies.click()
    except:
        pass
    
    #Close popup, sometimes the popup dont appear, because of this, the try
    try:
        acceptCookies = WebDriverWait(DRIVER, timeSleep).until(
        EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
        acceptCookies.click()

    except:
        pass
    
def getHistoricalData(ticker):
    
    #entering in website
    DRIVER.get('https://br.investing.com/search/?q={}&tab=quotes'.format(ticker))

    closeCookiesAndPopup() 

    #Because the link is associate with the company name, is difficult go directly to historical data
    #so I search the ticker and use the first result
    searchLinks = DRIVER.find_element_by_xpath('//*[@id="fullColumn"]/div/div[3]/div[3]/div/a')
    historicalDataLink = searchLinks.get_attribute('href')

    #Go to link
    DRIVER.get(historicalDataLink + '-historical-data')

    sleep(5)

    closeCookiesAndPopup() 

    #Click to input date range
    dateInput = DRIVER.find_element_by_id("widgetFieldDateRange")
    DRIVER.execute_script("arguments[0].click();", dateInput)
    dateInput.click()

    try:
        #Input inicial date
        startDateInput = DRIVER.find_element_by_id("startDate")
        startDateInput.clear()
        startDateInput.send_keys(startDate)

    except:
        closeCookiesAndPopup(timeSleep=5) 

        #Click to input date range
        dateInput = DRIVER.find_element_by_id("widgetFieldDateRange")
        # DRIVER.execute_script("arguments[0].click();", dateInput)
        dateInput.click()

        #Input inicial date
        startDateInput = DRIVER.find_element_by_id("startDate")
        startDateInput.clear()
        startDateInput.send_keys(startDate)

    try:
        #Input end date
        endDateInput = DRIVER.find_element_by_id("endDate")
        endDateInput.clear()
        endDateInput.send_keys(endDate)

    except:
        closeCookiesAndPopup(timeSleep=5) 

        #Click to input date range
        dateInput = DRIVER.find_element_by_id("widgetFieldDateRange")
        # DRIVER.execute_script("arguments[0].click();", dateInput)
        dateInput.click()

        #Input end date
        endDateInput = DRIVER.find_element_by_id("endDate")
        closeCookiesAndPopup(timeSleep=1)
        endDateInput.clear()
        endDateInput.send_keys(endDate)

    #Click in apply button to get range
    dateApplyButton = DRIVER.find_element_by_id("applyBtn")
    dateApplyButton.click()

    closeCookiesAndPopup(timeSleep=5)

    #Get historical date
    tableId = DRIVER.find_element_by_xpath("/html/body/div[5]/section/div[9]/table[1]")
    rowsTable = tableId.find_element_by_tag_name("tbody")

    #Rows of table of historical data
    rowsTable = rowsTable.text.replace('R$','').replace('%','').replace('%','').replace('.','').replace(',','.').split('\n')

    rowContent = []

    #Accessing the row text and iterating and entering future columns
    for row in rowsTable:
        values = row.split(' ')
        values[0] = datetime.datetime.strptime(values[0], '%d%m%Y').strftime('%d.%m.%Y')
        rowContent.append(values[:2])

    #Names of dataframe columns
    rowsHeaders = ['Data', 'Ultimo']

    #Creating dataframe
    df = pd.DataFrame(rowContent, columns = rowsHeaders)
    
    return df

endTimestamp = datetime.datetime.now()

df = getHistoricalData(ticker)

#df