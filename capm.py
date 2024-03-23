import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import pandas_datareader as web
import capm_functions as cf

st.set_page_config(page_title="CAP Model", layout='wide')
st.write('### [ Finance Analysis ]')
st.title('Capital Assest Price Model')

col1, col2 = st.columns([1, 1])
with col1:
    selected_stocks_list = st.multiselect('Choose Stocks (Multiselect possible)', ('NVDA', 'GOOGL', 'TSLA', 'AMZN',
                                                                                   'AAPL', 'NFLX', 'MSFT', 'MGM'), ['NVDA', 'AAPL', 'AMZN', 'MSFT'])
with col2:
    year = st.number_input("Number of Years ", 1, 10)


# downloading Data for SP500
end = datetime.date.today()
# today's date , month , year
tm = datetime.date.today().month
ty = datetime.date.today().year
td = datetime.date.today().day
start = datetime.date(ty-year, tm, td)

# Reading data from web Federal Reserve Economic Data (FRED)
SP500 = web.DataReader(['sp500'], 'fred', start, end)

stocks_df = pd.DataFrame()

for stock in selected_stocks_list:
    data = yf.download(stock, period=f'{year}y')
    # only Closing value in needed
    stocks_df[stock] = data['Close']

stocks_df.reset_index(inplace=True)
SP500.reset_index(inplace=True)

col1, col2 = st.columns([1, 1])
with col1:
    st.write("SP500 Data")
    st.dataframe(SP500.head())
with col2:
    st.write("Recent Days")
    st.dataframe(SP500.tail())

SP500.columns = ['Date', 'sp500']
stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')
stocks_df['Date'] = stocks_df['Date'].apply(lambda x: str(x)[:10])
stocks_df['Date'] = stocks_df['Date'].astype('datetime64[ns]')

# Stocks data View
col1, col2 = st.columns([1, 1])
with col1:
    st.write('### Stocks head')
    st.dataframe(stocks_df.head())
with col2:
    st.write('### Recent Days Stocks')
    st.dataframe(stocks_df.tail())

# variation
st.write('### Price variation of All Stocks')
st.plotly_chart(cf.create_plot(stocks_df))

st.write('### Price variation of After Normalization')
st.plotly_chart(cf.create_plot((cf.normalization(stocks_df))))


stocks_daily_return = cf.daily_return(stocks_df)
print(stocks_daily_return.head())

beta = {}
alpha = {}

for i in stocks_daily_return.columns:
    if i != 'Date' and i != 'sp500':
        b, a = cf.calculate_beta(stocks_daily_return, i)
        alpha[i] = a
        beta[i] = b
print(beta, alpha)

beta_df = pd.DataFrame(columns=['Stock', 'Beta Value'])
beta_df['Stock'] = beta.keys()
beta_df['Beta Value'] = [str(round(i, 2)) for i in beta.values()]

rf = 0
rm = stocks_daily_return['sp500'].mean()*252
return_df = pd.DataFrame()
return_value = []
for stock, value in beta.items():
    return_value.append(str(round(rf+(value*(rm-rf)), 2)))

return_df['Stock'] = selected_stocks_list
return_df['Return Value'] = return_value

col1, col2 = st.columns([1, 1])
with col1:
    st.markdown('### Calculated Beta Value')
    st.dataframe(beta_df)
with col2:
    st.markdown('### Calculated Return using CAPM')
    st.dataframe(return_df)
