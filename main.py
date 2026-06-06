import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from utils import load_artifacts, preprocess_input

DB_PATH = "data/predictions.db"

def setup_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                remaining_contract REAL,
                download_avg REAL,
                upload_avg REAL,
                subscription_age REAL,
                prediction REAL
            )
        ''')

setup_db()

@st.cache_resource
def get_model_and_scaler():
    return load_artifacts()

model, scaler = get_model_and_scaler()

st.title("Churn Prediction")

tab_pred, tab_hist = st.tabs(["Prediction", "History"])

with tab_pred:
    col1, col2 = st.columns(2)
    
    with col1:
        rem_contract = st.number_input("Remaining Contract (months)", min_value=0.0, value=1.0)
        has_contract = 1 if st.selectbox("Has Contract", ["Yes", "No"]) == "Yes" else 0
        dl_avg = st.number_input("Download Avg", min_value=0.0, value=20.0)
        ul_avg = st.number_input("Upload Avg", min_value=0.0, value=10.0)
        sub_age = st.number_input("Subscription Age", min_value=0.0, value=12.0)

    with col2:
        tv_sub = 1 if st.selectbox("TV Subscriber", ["Yes", "No"]) == "Yes" else 0
        movie_sub = 1 if st.selectbox("Movie Package", ["Yes", "No"]) == "Yes" else 0
        failures = st.number_input("Service Failures", min_value=0, value=0)
        bill = st.number_input("Average Bill", min_value=0.0, value=25.0)
        dl_limit = st.number_input("Download Over Limit", min_value=0.0, value=0.0)

    if st.button("Predict"):
        data = {
            'remaining_contract': rem_contract,
            'has_contract': has_contract,
            'download_avg': dl_avg,
            'upload_avg': ul_avg,
            'is_tv_subscriber': tv_sub,
            'is_movie_package_subscriber': movie_sub,
            'subscription_age': sub_age,
            'service_failure_count': failures,
            'bill_avg': bill,
            'download_over_limit': dl_limit
        }
        
        features = preprocess_input(data, scaler)
        pred = float(model.predict(features)[0][0])
        
        if pred > 0.5:
            st.error(f"High risk of churn: {pred:.2f}")
        else:
            st.success(f"Low risk: {pred:.2f}")
            
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                '''INSERT INTO logs 
                   (timestamp, remaining_contract, download_avg, upload_avg, subscription_age, prediction) 
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (datetime.now().strftime("%Y-%m-%d %H:%M"), rem_contract, dl_avg, ul_avg, sub_age, pred)
            )

with tab_hist:
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql("SELECT * FROM logs ORDER BY id DESC", conn)
    
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.line_chart(df.set_index('timestamp')['prediction'])
    else:
        st.write("No predictions logged yet.")