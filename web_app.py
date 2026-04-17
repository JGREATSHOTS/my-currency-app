import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# 1. Your Google Sheets Link
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1Kpvnptn26dtSveU1JES2RHp24A9DFXOvYEomXyvjf4k/export?format=csv&gid=0"

st.set_page_config(page_title="FX Sentinel", layout="wide")

# Custom CSS for your dark dashboard
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #131722; color: white; }
    .matrix-container { overflow-x: auto; }
    table { width: 100%; border-collapse: collapse; font-family: sans-serif; font-size: 12px; border: 1px solid #333; }
    th { background-color: #1e2124; color: #888; padding: 10px; border: 1px solid #333; text-transform: uppercase; }
    .side-header { background-color: #fff3cd; color: black; font-weight: bold; border: 1px solid #333; text-align: center; }
    .buy { background-color: #d4edda; color: #155724; font-weight: bold; text-align: center; height: 40px; }
    .sell { background-color: #f8d7da; color: #721c24; font-weight: bold; text-align: center; height: 40px; }
    .neutral { background-color: #1e2124; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("B MARKET SENTINEL: SEASONALITY MATRIX")

@st.cache_data(ttl=86400)
def get_seasonality(curr):
    if curr == "USD": return 5.0
    try:
        # Pulls 20 years of data against USD
        ticker = f"{curr}USD=X" if curr != "EUR" else "EURUSD=X"
        data = yf.download(ticker, period="20y", interval="1mo", progress=False)
        current_month = datetime.now().month
        returns = data['Close'].pct_change()
        monthly_returns = returns[returns.index.month == current_month]
        win_rate = (len(monthly_returns[monthly_returns > 0]) / len(monthly_returns)) * 10
        return round(win_rate, 1)
    except:
        return 5.0

try:
    df = pd.read_csv(SHEET_CSV_URL)
    df.set_index('Currency', inplace=True)
    
    if st.button('🚀 RUN FULL ANALYSIS'):
        with st.spinner('Calculating 20-year seasonality patterns...'):
            # Build the matrix
            currencies = ["AUD", "GBP", "CAD", "EUR", "JPY", "NZD", "CHF", "USD"]
            
            # Calculate Scores
            scores = {}
            for c in currencies:
                s_score = get_seasonality(c)
                # Formula: (GDP + Rate + Seasonality) - (CPI + Jobs)
                f_score = (df.loc[c, 'GDP'] + df.loc[c, 'Rate'] + s_score) - (df.loc[c, 'CPI'] + df.loc[c, 'Jobs'])
                scores[c] = f_score

            # Generate Table
            html = "<table><tr><th>1 WEEK</th>"
            for c in currencies: html += f"<th>{c}</th>"
            html += "</tr>"

            for r_curr in currencies:
                html += f"<tr><td class='side-header'>{r_curr}</td>"
                for c_curr in currencies:
                    if r_curr == c_curr:
                        html += "<td class='neutral'></td>"
                    else:
                        if scores[r_curr] >= scores[c_curr]:
                            html += "<td class='buy'>BUY</td>"
                        else:
                            html += "<td class='sell'>SELL</td>"
                html += "</tr></table>"
            
            st.markdown(html, unsafe_allow_html=True)
    else:
        st.info("Tap the button above to generate the matrix.")

except Exception as e:
    st.error(f"Waiting for data... Ensure Google Sheet is Published as CSV. Error: {e}")
