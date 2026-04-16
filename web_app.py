import streamlit as st
import requests

# Use your actual key here
API_KEY = "YOUR_ALPHAVANTAGE_KEY_HERE"

st.set_page_config(page_title="FX Sentinel", layout="wide")

# CSS for Dark Mode and Sentiment Colors
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
    }
    /* Sentiment Border Colors */
    .border-green { border-top: 5px solid #00ff88; }
    .border-red { border-top: 5px solid #ff4444; }
    
    h1 { color: white !important; margin: 10px 0; font-size: 40px !important; }
    h3 { color: #888 !important; margin-bottom: 0px; letter-spacing: 1px; }
    
    .text-green { color: #00ff88 !important; font-weight: bold; }
    .text-red { color: #ff4444 !important; font-weight: bold; }
    
    .stButton>button {
        width: 100%; border-radius: 10px; background-color: #2962ff;
        color: white; border: none; font-weight: bold; height: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("B MARKET SENTINEL V1.0")

# Session State for Data persistence
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

# Helper function to create colorized cards
def render_card(name, value, trend, label):
    color_class = "border-green" if trend == "UP" else "border-red"
    text_class = "text-green" if trend == "UP" else "text-red"
    arrow = "▲" if trend == "UP" else "▼"
    
    st.markdown(f"""
        <div class='card {color_class}'>
            <h3>{name}</h3>
            <h1>{value}%</h1>
            <p class='{text_class}'>{arrow} {trend} ({label})</p>
        </div>
    """, unsafe_allow_html=True)

# 2x2 Grid Layout
col1, col2 = st.columns(2)
with col1:
    render_card("USD", st.session_state.usd_val, "UP", f"RATE: {st.session_state.usd_rate}%")
with col2:
    render_card("EUR", 42, "DOWN", "3.25%")

col3, col4 = st.columns(2)
with col3:
    render_card("GBP", 58, "UP", "5.25%")
with col4:
    render_card("JPY", 12, "DOWN", "0.10%")
