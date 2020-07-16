import datetime as dt
import yfinance as yf
import streamlit as st

st.sidebar.header('User Input Features')

def user_input_features():
    dax_companies = {'Adidas': 'ADS.DE',
                     'Allianz': 'ALV.DE',
                     'BASF': 'BAS.DE',
                     'Bayer': 'BAYN.DE',
                     'Beiersdorf': 'BEI.DE',
                     'BMW': 'BMW.DE',
                     'Continental': 'CON.DE',
                     'Covestro': '1COV.DE',
                     'Daimler': 'DAI.DE',
                     'Deutsche Bank': 'DBK.DE',
                     'Deutsche Börse': 'DB1.DE',
                     'Deutsche Post': 'DPW.DE',
                     'Deutsche Telekom': 'DTE.DE',
                     'Deutsche Wohnen': 'DWNI.DE',
                     'E.ON': 'EOAN.DE',
                     'Fresenius': 'FRE.DE',
                     'Fresenius Medical': 'FME.DE',
                     'Heidelberg Cement': 'HEI.DE',
                     'Henkel': 'HEN3.DE',
                     'Infineon': 'IFX.DE',
                     'Linde': 'LIN.DE',
                     'Merck': 'MRK.DE',
                     'MTU': 'MTX.DE',
                     'Münchner Rück': 'MUV2.DE',
                     'RWE': 'RWE.DE',
                     'SAP': 'SAP.DE',
                     'Siemens': 'SIE.DE',
                     'Volkswagen': 'VOW3.DE',
                     'Vonovia': 'VNA.DE',
                     'Wirecard': 'WDI.DE'}
    company = st.sidebar.selectbox('DAX30 Company', ('Adidas', 'Allianz', 'BASF', 'Bayer', 'Beiersdorf', 'BMW',
                                                             'Continental', 'Covestro', 'Daimler', 'Deutsche Bank',
                                                             'Deutsche Börse', 'Deutsche Post', 'Deutsche Telekom',
                                                             'Deutsche Wohnen', 'E.ON', 'Fresenius', 'Fresenius Medical',
                                                             'Heidelberg Cement', 'Henkel', 'Infineon', 'Linde', 'Merck',
                                                             'MTU', 'Münchner Rück', 'RWE', 'SAP', 'Siemens', 'Volkswagen',
                                                             'Vonovia', 'Wirecard'))
    ticker_symbol = dax_companies[company]
    
    today = dt.date.today()
    start_date = st.sidebar.date_input('Start date', dt.datetime(2010, 5, 31))
    end_date = st.sidebar.date_input('End date', today)
    if start_date < end_date:
        st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
    else:
        st.sidebar.error('Error: End date must fall after start date.')
        
    return ticker_symbol, company, start_date, end_date

#define the ticker symbol
tickerSymbol, company, start_date, end_date = user_input_features()

st.write("""
# DAX30 Stock Prices
Shown are the stock closing price and volume for 
""" + company + '!')

#get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

#get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)
# Open	High	Low	Close	Volume	Dividends	Stock Splits

st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)