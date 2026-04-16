import streamlit as st
import requests

# Use your actual key here
API_KEY = "BLBNANMWHGOJKXF2"

st.set_page_config(page_title="FX Sentinel", layout="wide")

# Custom CSS to make it look like your dark dashboard
st.markdown("""
    <style>
    .main { background-color: #131722; color: white; }
    .card { background-color: #1e2124; padding: 20px; border-radius: 15px; border: 1px solid #333; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("B MARKET SENTINEL V1.0")

if st.button('SYNC GLOBAL DATA'):
    # Fetching the USD rate just like before
    url = f'https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=monthly&apikey={API_KEY}'
    data = requests.get(url).json()
    rate = float(data['data'][0]['value'])
    strength = int((rate/10)*100)

    # Creating the "Cards" using Streamlit columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='card'><h3>USD</h3><h1>{strength}%</h1><p>UP</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card'><h3>EUR</h3><h1>42%</h1><p>DOWN</p></div>", unsafe_allow_html=True)
    # ... and so on for others