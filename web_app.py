import streamlit as st
import requests

API_KEY = "YOUR_ALPHAVANTAGE_KEY_HERE"

st.set_page_config(page_title="FX Sentinel", layout="wide")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #131722; }
    .card {
        background-color: #1e2124;
        padding: 15px;
        border-radius: 15px;
        border: 1px solid #333;
        margin-bottom: 15px;
    }
    .border-green { border-top: 5px solid #00ff88; }
    .border-red { border-top: 5px solid #ff4444; }
    
    .curr-name { color: #888 !important; font-size: 18px; font-weight: bold; letter-spacing: 1px; }
    .main-val { color: white !important; font-size: 38px !important; margin: 0; font-weight: bold; }
    
    .metric-row { display: flex; justify-content: space-between; margin-top: 10px; border-top: 1px solid #333; padding-top: 10px; }
    .metric-item { text-align: center; flex: 1; }
    .metric-label { color: #555 !important; font-size: 10px; text-transform: uppercase; }
    .metric-val { color: white !important; font-size: 12px; font-weight: bold; }
    
    .stButton>button {
        width: 100%; border-radius: 10px; background-color: #2962ff;
        color: white; border: none; font-weight: bold; height: 45px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("B MARKET SENTINEL V1.0")

# Initialize Session States
if 'metrics' not in st.session_state:
    st.session_state.metrics = {"USD": {"rate": 0, "gdp": 0, "inf": 0, "job": 0, "score": 0}}

def fetch_usd_data():
    try:
        # 1. Interest Rate
        r = requests.get(f'https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=monthly&apikey={API_KEY}').json()
        rate = float(r['data'][0]['value'])
        
        # 2. GDP Growth (Annual Query)
        g = requests.get(f'https://www.alphavantage.co/query?function=REAL_GDP&interval=annual&apikey={API_KEY}').json()
        gdp = float(g['data'][0]['value']) / 1000 # Scaling for display
        
        # 3. Inflation (CPI)
        i = requests.get(f'https://www.alphavantage.co/query?function=CPI&interval=monthly&apikey={API_KEY}').json()
        inf = float(i['data'][0]['value'])
        
        # 4. Jobless Rate
        j = requests.get(f'https://www.alphavantage.co/query?function=UNEMPLOYMENT&apikey={API_KEY}').json()
        job = float(j['data'][0]['value'])

        # Simple Strength Score Logic
        score = int(((rate + gdp) - (inf + job)) * 5) + 50
        
        st.session_state.metrics["USD"] = {"rate": rate, "gdp": 2.4, "inf": inf, "job": job, "score": score}
    except:
        st.error("API limit reached or data error.")

if st.button('SYNC FUNDAMENTALS'):
    fetch_usd_data()

def render_metric_card(name, m):
    sentiment = "border-green" if m['score'] > 50 else "border-red"
    st.markdown(f"""
        <div class='card {sentiment}'>
            <div class='curr-name'>{name}</div>
            <div class='main-val'>{m['score']}%</div>
            <div class='metric-row'>
                <div class='metric-item'><div class='metric-label'>GDP</div><div class='metric-val'>{m['gdp']}%</div></div>
                <div class='metric-item'><div class='metric-label'>Rate</div><div class='metric-val'>{m['rate']}%</div></div>
                <div class='metric-item'><div class='metric-label'>CPI</div><div class='metric-val'>{m['inf']}%</div></div>
                <div class='metric-item'><div class='metric-label'>Jobs</div><div class='metric-val'>{m['job']}%</div></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Layout
c1, c2 = st.columns(2)
with c1: render_metric_card("USD", st.session_state.metrics["USD"])
with c2: render_metric_card("EUR", {"score": 42, "gdp": 1.1, "rate": 3.2, "inf": 2.5, "job": 6.4})

c3, c4 = st.columns(2)
with c3: render_metric_card("GBP", {"score": 58, "gdp": 0.5, "rate": 5.2, "inf": 3.1, "job": 4.2})
with c4: render_metric_card("JPY", {"score": 12, "gdp": 0.8, "rate": 0.1, "inf": 2.2, "job": 2.5})
