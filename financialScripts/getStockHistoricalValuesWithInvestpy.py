##### Calling libraries

import investpy

##### Code

#Functions

def get_historical_cotation(stock, country, from_date, to_date):
    df = investpy.get_stock_historical_data(stock,
                                            country,
                                            from_date,
                                            to_date
                                           ).reset_index()
    df = df[['Date', 'Close']]

    df = df.rename(columns={"Date":"data",
              "Close": "valor"})

    df['ticker'] = stock

    df = df[[ 'data', 'ticker', 'valor']]
    
    return df
    

df = get_historical_cotation('BRML3', "BRAZIL", '20/01/2020', '20/09/2020')

# df