import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="API Throttle Monitor", layout="wide")
st.title("🎯 API Rate Limit & Throttle Monitor")

# --- Sidebar: Define your Goal ---
st.sidebar.header("Target Rate Limit")
limit_val = st.sidebar.number_input("How many requests?", min_value=1, value=20)
limit_period = st.sidebar.selectbox("In what timeframe?", 
                                    options=["1 second", "5 seconds", "10 seconds", "30 seconds", "60 seconds"])

# --- Math: Convert Goal to RPS ---
# Example: 20 requests per 5 seconds = 4.0 RPS
period_map = {"1 second": 1, "5 seconds": 5, "10 seconds": 10, "30 seconds": 30, "60 seconds": 60}
target_rps = limit_val / period_map[limit_period]

st.sidebar.info(f"Targeting: {target_rps} Requests Per Second")

if st.sidebar.button("🗑️ Reset Stats"):
    st.session_state.history = pd.DataFrame(columns=['Time', 'Actual RPS', 'Target RPS'])
    st.rerun()

# --- Metrics Display ---
col1, col2 = st.columns(2)
total_metric = col1.empty()
rps_metric = col2.empty()

chart_placeholder = st.empty()

if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['Time', 'Actual RPS', 'Target RPS'])

while True:
    try:
        # Get the 1-second real-time data from backend
        data = requests.get("http://localhost:8000/stats", timeout=1).json()
        current_rps = data.get('current_rps', 0)
        
        # Update Metrics
        total_metric.metric("Total Requests", data['total_requests'])
        
        # Show if we are over or under the target
        rps_metric.metric("Current RPS", f"{current_rps}", 
                          delta=round(current_rps - target_rps, 2), 
                          delta_color="inverse")
        
        # Update Chart Data
        new_row = pd.DataFrame({
            'Time': [pd.Timestamp.now()],
            'Actual RPS': [current_rps],
            'Target RPS': [target_rps] # The "Red Line"
        })
        
        st.session_state.history = pd.concat([st.session_state.history, new_row]).iloc[-60:]
        
        # Plotting
        chart_placeholder.line_chart(
            st.session_state.history.set_index('Time'), 
            color=["#29b5e8", "#FF4B4B"] # Blue for you, Red for the limit
        )
        
    except Exception:
        st.warning("🔄 Connecting to API...")
    
    time.sleep(1)