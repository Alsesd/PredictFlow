import pandas as pd
import numpy as np
import joblib
import tensorflow as tf

def load_artifacts(model_path='models/churn_model.keras', scaler_path='models/scaler.pkl'):
    model = tf.keras.models.load_model(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler
    
def preprocess_input(data, scaler):
    df = pd.DataFrame([data])
    
    features = [
        'remaining_contract', 'has_contract', 'download_avg', 'upload_avg',
        'is_tv_subscriber', 'is_movie_package_subscriber', 'subscription_age',
        'service_failure_count', 'bill_avg', 'download_over_limit'
    ]
    
    df = df.reindex(columns=features)
    
    df['remaining_contract'] = df['remaining_contract'].fillna(0)
    
    dl_median = df['download_avg'].median() if not df['download_avg'].isna().all() else 15.0
    df['download_avg'] = df['download_avg'].fillna(dl_median)
    
    ul_median = df['upload_avg'].median() if not df['upload_avg'].isna().all() else 5.0
    df['upload_avg'] = df['upload_avg'].fillna(ul_median)
    
    df = df.fillna(0)
    
    return scaler.transform(df)