import streamlit as st
import requests

API_KEY = "YOUR_ALPHAVANTAGE_KEY_HERE"

st.set_page_config(page_title="FX Sentinel", layout="wide")

# CSS for Sentiment Colors and Professional Layout
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #131722; }
    .card {
        background-color: #1e2124;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #333;
        text-align: center;
        margin-bottom: 15px;
        position: relative;
    }
    /* Dynamic Color Strips */
    .strip-green { border-top: 5px solid #00ff88; }
    .strip-red { border-top: 5px solid #ff4444; }
    
    h1 { color: white !important; margin: 5px 0; font-size: 42px !important; }
    h3 { color: #888 !important; margin-bottom: 0px; letter-spacing: 2px; }
    
    .trend-up { color: #00ff88 !important; font-weight: bold; font-size: 14px; }
    .trend-down { color: #ff4444 !important; font-weight: bold; font-size: 14px; }
    
    .stButton>button {
        width: 100%; border-radius: 10px; background-color: #2962ff;
        color: white; border: none; font-weight: bold; height: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("B MARKET SENTINEL V1.0")

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
        st.error("API Limit reached.")

# Helper function to render cards with colors
def render_card(name, value, trend, label):
    sentiment_class = "strip-green" if trend == "UP" or value > 50 else "strip-red"
    trend_class = "trend-up" if trend == "UP" else "trend-down"
    arrow = "▲" if trend == "UP" else "▼"
    
    st.markdown(f"""
        <div class='card {sentiment_class}'>
            <h3>{name}</h3>
            <h1>{value}%</h1>
            <p class='{trend_class}'>{arrow} {trend} ({label})</p>
        </div>
    """, unsafe_allow_html=True)

# 2x2 Grid Layout
row1_col1, row1_col2 = st.columns(2)
with row1_col1:
    render_card("USD", st.session_state.usd_val, "UP", f"{st.session_state.usd_rate}%")
with row1_col2:
    render_card("EUR", 42, "DOWN", "3.25%")

row2_col1, row2_col2 = st.columns(2)
with row2_col1:
    render_card("GBP", 58, "UP", "5.25%")
with row2_col2:
    render_card("JPY", 12, "DOWN", "0.10%")unsafe_allow_html=True)
