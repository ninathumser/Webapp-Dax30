import altair as alt
import datetime as dt
import numpy as np
import streamlit as st
import yfinance as yf


# FUNCTIONS #

def user_input_features():
    dax_companies = {'Adidas': 'ADS.DE', 'Allianz': 'ALV.DE', 'BASF': 'BAS.DE', 'Bayer': 'BAYN.DE',
                     'Beiersdorf': 'BEI.DE', 'BMW': 'BMW.DE', 'Continental': 'CON.DE', 'Covestro': '1COV.DE',
                     'Daimler': 'DAI.DE', 'Deutsche Bank': 'DBK.DE', 'Deutsche Börse': 'DB1.DE', 'Deutsche Post': 'DPW.DE',
                     'Deutsche Telekom': 'DTE.DE', 'Deutsche Wohnen': 'DWNI.DE', 'E.ON': 'EOAN.DE', 'Fresenius': 'FRE.DE',
                     'Fresenius Medical': 'FME.DE', 'Heidelberg Cement': 'HEI.DE', 'Henkel': 'HEN3.DE', 'Infineon': 'IFX.DE',
                     'Linde': 'LIN.DE', 'Merck': 'MRK.DE', 'MTU': 'MTX.DE', 'Münchner Rück': 'MUV2.DE',
                     'RWE': 'RWE.DE', 'SAP': 'SAP.DE', 'Siemens': 'SIE.DE', 'Volkswagen': 'VOW3.DE',
                     'Vonovia': 'VNA.DE', 'Wirecard': 'WDI.DE'}
    company = st.sidebar.selectbox('DAX30 Company', ('Adidas', 'Allianz', 'BASF', 'Bayer', 'Beiersdorf', 'BMW',
                                                     'Continental', 'Covestro', 'Daimler', 'Deutsche Bank',
                                                     'Deutsche Börse', 'Deutsche Post', 'Deutsche Telekom',
                                                     'Deutsche Wohnen', 'E.ON', 'Fresenius', 'Fresenius Medical',
                                                     'Heidelberg Cement', 'Henkel', 'Infineon', 'Linde', 'Merck',
                                                     'MTU', 'Münchner Rück', 'RWE', 'SAP', 'Siemens', 'Volkswagen',
                                                     'Vonovia', 'Wirecard'))
    ticker_symbol = dax_companies[company]
    
    today = dt.date.today()
    start_date = st.sidebar.date_input('Start date', dt.date(2020, 1, 1))
    end_date = st.sidebar.date_input('End date', today)
    if start_date < end_date:
        st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
    else:
        st.sidebar.error('Error: End date must fall after start date.')
        
    return ticker_symbol, company, start_date, end_date


def create_tickerDf():
    #get data on selected ticker
    tickerData = yf.Ticker(ticker_symbol)
    
    #create dataframe of historical prices for this ticker using data from user input
    tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)
    
    return tickerDf


def ticker_graph_dynamic():
    #displays dynamic graph
    status_text = st.empty()

    #start dynamic graph with only one line (start date)
    close = st.line_chart(tickerDf.loc[start_date:start_date, 'Close'])
    volume = st.line_chart(tickerDf.loc[start_date:start_date, 'Volume'])
    i = 0

    #iterate over date indexes to isolate data from individual day
    for idx in tickerDf.index:
        #append each day(index) individually to the chart
        new_close = tickerDf.loc[:idx, 'Close']
        new_volume = tickerDf.loc[:idx, 'Volume']
        close.add_rows(new_close)
        volume.add_rows(new_volume)

        #calculate and display progress
        i += 1
        status_text.text('{:.2f}% Complete'.format(i/len(tickerDf)*100))

    status_text.text('Done!')

    st.button("Re-run")

    
def ticker_graph_static():
    st.line_chart(tickerDf.Close)
    st.line_chart(tickerDf.Volume)
        
                
def dax_graph():
    dax = yf.Ticker('^GDAXI')
    daxDf = dax.history(period='1d', start=start_date, end=end_date)

    dax_chart = alt.Chart(daxDf.reset_index()).mark_line(color='green').encode(      #reset index to be able to use Date as x
            x=alt.X('Date:T', title=' '),         #identify column Date as time (:T), title ' ' to hide axis title
            y=alt.Y('Close:Q', title=' '),        #identify column Close as quantitative (:Q)
            ).properties(
                width=600,
                height=370
            )
    chart = st.altair_chart(dax_chart)

    
########################################################################################


# WEBAPP #


st.title('DAX30 Stock Prices')

st.sidebar.header('User Input Features')

#define the ticker symbol and create the dataframe
ticker_symbol, company, start_date, end_date = user_input_features()
tickerDf = create_tickerDf()

#plot graph for required ticker
if st.checkbox('Show overall DAX30 performance'):
    st.subheader('DAX30 performance between ' + start_date.strftime('%m/%d/%Y') + ' and ' + end_date.strftime('%m/%d/%Y'))
    dax_graph()

#write subheader
st.subheader(company + ' closing price and volume between '+ start_date.strftime('%m/%d/%Y') + ' and ' + end_date.strftime('%m/%d/%Y'))

#plot graph for requested ticker
if st.checkbox('Show dynamic graph'):
    if (end_date-start_date) > dt.timedelta(365):
        st.error('Performance warning: Dynamic graph only available for max. 365 days!')
    else:
        ticker_graph_dynamic()
else:    
    ticker_graph_static()