import streamlit as st
import requests

# Use your actual key here
API_KEY = "YOUR_ALPHAVANTAGE_KEY_HERE"

st.set_page_config(page_title="FX Sentinel", layout="wide")

# This CSS fix forces white text and centers everything for your iPhone screen
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #131722;
    }
    .card {
        background-color: #1e2124;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #333;
        text-align: center;
        margin-bottom: 10px;
    }
    h1, h2, h3, p {
        color: white !important;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #1e2124;
        color: white;
        border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("B MARKET SENTINEL V1.0")

# Initialize placeholder values
if 'usd_val' not in st.session_state:
    st.session_state.usd_val = 0
    st.session_state.usd_rate = 0

if st.button('SYNC GLOBAL DATA'):
    try:
        url = f'https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=monthly&apikey={API_KEY}'
        data = requests.get(url).json()
        rate = float(data['data'][0]['value'])
        st.session_state.usd_val = int((rate/10)*100)
        st.session_state.usd_rate = rate
    except:
        st.error("API Limit reached. Wait 60 seconds.")

# Display the cards
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"<div class='card'><h3>USD</h3><h1>{st.session_state.usd_val}%</h1><p>RATE: {st.session_state.usd_rate}%</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='card'><h3>EUR</h3><h1>42%</h1><p>DOWN</p></div>", unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    st.markdown("<div class='card'><h3>GBP</h3><h1>58%</h1><p>UP</p></div>", unsafe_allow_html=True)
with col4:
    st.markdown("<div class='card'><h3>JPY</h3><h1>12%</h1><p>DOWN</p></div>", unsafe_allow_html=True)
