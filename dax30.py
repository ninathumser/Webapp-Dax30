import datetime as dt
import numpy as np
import time
import yfinance as yf
import altair as alt
import streamlit as st

st.title('DAX30 Stock Prices')

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
    start_date = st.sidebar.date_input('Start date', dt.datetime(2020, 1, 1))
    end_date = st.sidebar.date_input('End date', today)
    if start_date < end_date:
        st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
    else:
        st.sidebar.error('Error: End date must fall after start date.')
        
    return ticker_symbol, company, start_date, end_date

#define the ticker symbol
tickerSymbol, company, start_date, end_date = user_input_features()

#write subheader
#st.write('Ovarall DAX30 performance between ' + start_date.strftime('%m/%d/%Y') + ' and ' + end_date.strftime('%m/%d/%Y'))

#get data for DAX performance index
if st.checkbox('Show overall DAX30 performance'):
    st.subheader('DAX30 performance between ' + start_date.strftime('%m/%d/%Y') + ' and ' + end_date.strftime('%m/%d/%Y'))
    dax = yf.Ticker('^GDAXI')
    daxDf = dax.history(period='1d', start=start_date, end=end_date)

    dax_chart = alt.Chart(daxDf.reset_index()).mark_line(color='green').encode(
            x=alt.X('Date:T', title=' '),
            y=alt.Y('Close:Q', title=' '),
            ).properties(
                width=600,
                height=370
            )
    chart = st.altair_chart(dax_chart)
    


#write subheader
st.subheader(company + ' closing price and volume between '+ start_date.strftime('%m/%d/%Y') + ' and ' + end_date.strftime('%m/%d/%Y'))

#get data on selected ticker
tickerData = yf.Ticker(tickerSymbol)

#get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)

st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)


status_text = st.empty()
close = st.line_chart(tickerDf.loc[start_date:start_date, 'Close'])
volume = st.line_chart(tickerDf.loc[start_date:start_date, 'Volume'])
i = 0

for idx in tickerDf.index:
    new_close = tickerDf.loc[:idx, 'Close']
    new_volume = tickerDf.loc[:idx, 'Volume']


    # Append data to the chart.
    close.add_rows(new_close)
    volume.add_rows(new_volume)

    i += 1
    status_text.text('{:.2f}% Complete'.format(i/len(tickerDf)*100))
    #time.sleep(0.15)
       
status_text.text('Done!')