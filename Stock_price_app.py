# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 10:50:15 2023

@author: akout
"""

import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import date
import plotly.express as px

st.set_page_config(page_title='Stock Price App',  layout='wide')

st.write(""" # Stock Price App""")

st.write(""" 

##### Πεσματζού εδώ να μπαινείς να βλέπεις για τις επενδύσεις σου και OΧΙ στη μαλακία το Binance!

""")



stock_input = st.text_input('Για ποια μετοχή ενδιαφέρεσαι να μάθεις?')   
submitted = st.button('Submit')
if stock_input:
    
    # Retrieve Data
    tickerSymbol = stock_input
    tickerData = yf.Ticker(tickerSymbol)
    tickerName = tickerData.info['longName']
    today = date.today()
    start_date = '2018-1-1'
    tickerDf = yf.download(tickers = tickerSymbol, period = '1d', start = start_date, end = today)
    
    st.write(f' #### Πολύ ωραία, δες τις αποδόσεις σου από {tickerName}')
    

    # Ask about Invested Amount
    investment_input = st.text_input("Πόσα λεφτά είχες επενδύσει?")
    submitted = st.button('Submit Amount')
    if submitted:
        investment = int(investment_input)
        
        # Calculate returns  
        returns = pd.DataFrame(tickerDf)
        returns.reset_index(inplace = True)
        returns = returns[['Date', 'Close']]
        returns['Returns'] = returns.Close.pct_change() 
        returns = returns[1:]
        returns['Cum_Returns'] = (1 + returns.Returns).cumprod() - 1
        returns['Value'] = (returns.Cum_Returns + 1) * investment
        today_cum_return = returns.Cum_Returns.iloc[-1]
        today_cum_value = returns.Value.iloc[-1]
        
        
        negative_returns = returns[returns.Returns < 0]
        probabilities = round((negative_returns.Returns.count() / returns.Returns.count()) * 100, 1)


        # Summary Statistics
        m1, m2, m3, m4, m5 = st.columns((1,1,1,1,1))
        
        m1.metric(label ='Η Αθροιστική σου απόδοση είναι %', value = round(today_cum_return * 100, 1))
        m2.metric(label = f'Η Αξία της επένδυσής σου από {investment}$, σήμερα είναι)', value = int(today_cum_value))
        m3.metric(label = f'Από τις {returns.Returns.count()} ημέρες, αρνητική απόδοση είχες τις', value = int(negative_returns.Returns.count()))
        m4.metric(label = 'Πιθανότητες να έχεις αρνητική ημερήσια απόδοση %', value = int(probabilities))

        # Plot some Data
        
       
        fig = px.line(returns, x= 'Date', y = 'Close')
        fig.update_layout(title_text = f'Η Τιμή της {tickerName} από το {start_date} έως σήμερα', width=1400, height=500)
        st.plotly_chart(fig)
        
        g1, g2= st.columns((1,1))

        fig1 = px.histogram(data_frame = returns[returns.Returns > -20], x = 'Returns')
        fig1.update_layout(title_text="Ιστόγραμμα με Ημερήσιες αποδόσεις",title_x=0, yaxis_title=None, xaxis_title=None)
        g1.plotly_chart(fig1)
    
        fig2 = px.ecdf(returns, x = 'Returns')
        fig2.update_layout(title_text="Αθροιστική καμπύλη πιθανοτήτων ημερήσιων αποδόσεων",title_x=0, yaxis_title=None, xaxis_title=None)
        g2.plotly_chart(fig2)