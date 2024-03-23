import plotly.express as px
import numpy as np


def create_plot(df):
    fig = px.line()
    for i in df.columns[1:]:
        fig.add_scatter(x=df['Date'], y=df[i], name=i)
    return fig

# Normatlization with respect Current price


def normalization(df2):
    df = df2.copy()
    for i in df.columns[1:]:
        curr = df[i][0]
        df[i] = df[i]/curr
    print(df)
    return df

# Daily Basis return (OR Return with respect to previous day)


def daily_return(df):
    daily_return = df.copy()
    for i in df.columns[1:]:
        for j in range(1, len(df)):
            today = df[i][j]
            prev = df[i][j-1]
            daily_return[i][j] = ((today - prev)/prev)*100
        daily_return[i][0] = 0
    return daily_return


def calculate_beta(daily_return, stock):
    rm = daily_return['sp500'].mean()*252
    b, a = np.polyfit(daily_return['sp500'], daily_return[stock], 1)
    return b, a
