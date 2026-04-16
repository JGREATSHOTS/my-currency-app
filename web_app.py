import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# 1. Your Google Sheets Link for the 4 Fundamentals (GDP, Rate, CPI, Jobs)
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT5GylFqdLzvcmLMM4uL-CwAZHnPmsG_CSAUpBMlA5TERubmsMe3Z57gROgDbZY16BYDI90irCe8GA3/pub?gid=136390075&single=true&output=csv"

st.set_page_config(page_title="Auto-Seasonality Matrix", layout="wide")

# (Keep your existing CSS here...)

@st.cache_data(ttl=86400) # Cache data for 24 hours
def get_auto_seasonality(ticker):
    """Calculates seasonality score based on 20-year historical win rate for current month."""
    try:
        data = yf.download(f"{ticker}=X", period="22y", interval="1mo")
        current_month = datetime.now().month
        
        # Calculate monthly returns
        data['Return'] = data['Close'].pct_change()
        # Filter for the current month across all years
        monthly_data = data[data.index.month == current_month]
        
        wins = len(monthly_data[monthly_data['Return'] > 0])
        total_years = len(monthly_data)
        win_rate = (wins / total_years) * 100
        
        # Convert win rate to a 1-10 score (50% win rate = 5 score)
        return round(win_rate / 10, 1)
    except:
        return 5.0 # Neutral fallback

st.title("Auto-Seasonality & Fundamentals Matrix")

try:
    # Load Fundamentals from Google Sheets
    df = pd.read_csv(SHEET_CSV_URL)
    df.set_index('Currency', inplace=True)

    # 2. AUTO-CALCULATE SEASONALITY
    if st.button('CALCULATE LIVE SEASONALITY'):
        with st.spinner('Analyzing 20 years of historical data...'):
            for curr in df.index:
                if curr != "USD": # yfinance uses USD as base (e.g. GBPUSD)
                    df.at[curr, 'Seasonality'] = get_auto_seasonality(curr)
                else:
                    df.at[curr, 'Seasonality'] = 5.0 # USD is the baseline
            
    # Calculate Final Strength Score
    df['Score'] = (df['GDP'] + df['Rate'] + df['Seasonality']) - (df['CPI'] + df['Jobs'])

    # (Keep your existing Matrix Table generation code here...)

except Exception as e:
    st.error("Setup required: Add your CSV link and update requirements.txt")
