import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import joblib
import os

# --- Dynamisk mapp ---
current_dir = os.path.dirname(__file__)

# --- Förbered modell och scaler ---
model = None
scaler = None

model_path = os.path.join(current_dir, 'rnn_model.keras')
scaler_path = os.path.join(current_dir, 'scaler.save')

# --- Ladda modell och scaler om de finns ---
if os.path.exists(model_path) and os.path.exists(scaler_path):
    model = tf.keras.models.load_model(model_path)
    scaler = joblib.load(scaler_path)

# --- Ladda data ---
data_path = os.path.join(current_dir, 'AllaJobb.csv')

if os.path.exists(data_path):
    df = pd.read_csv(data_path, skiprows=8)
    df = df.dropna(how='all', axis=1)
    df = df.dropna(subset=['YRKESOMRÅDE'])
    df = df.fillna(0)

    time_cols = [col for col in df.columns if '-' in str(col)]
    dates = pd.to_datetime(time_cols)
else:
    df = None
    dates = None

window_size = 12

def predict_future(yrkesomrade_input, manader_input):
    if model is None or scaler is None or df is None:
        return None, None, None  # Modell, scaler eller data saknas
    
    yrkesomrade_input = yrkesomrade_input.strip().lower()

    match = None
    for yrke in df['YRKESOMRÅDE'].unique():
        if yrke.lower() == yrkesomrade_input:
            match = yrke
            break

    if match is None:
        return None, None, None

    row = df[df['YRKESOMRÅDE'] == match]
    original_values = row[time_cols].values.flatten().astype(float)

    scaled_values = scaler.transform([original_values])[0]
    sequence = scaled_values[-window_size:]
    preds_scaled = []

    for _ in range(manader_input):
        input_seq = np.expand_dims(sequence, axis=(0, -1))
        pred = model.predict(input_seq, verbose=0)[0, 0]
        preds_scaled.append(pred)
        sequence = np.append(sequence[1:], pred)

    preds_scaled = np.array(preds_scaled).reshape(1, -1)
    future_original = scaler.inverse_transform(
        np.pad(preds_scaled, ((0, 0), (len(scaled_values) - preds_scaled.shape[1], 0)), mode='constant')
    )[0][-manader_input:]

    historical = original_values
    future = future_original

    future_dates = pd.date_range(start=dates[-1] + pd.DateOffset(months=1), periods=manader_input, freq='MS')

    return dates, historical, (future_dates, future)