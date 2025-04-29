import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.callbacks import EarlyStopping
import random
import os
import joblib
import streamlit as st

# --- Säkerställ reproducerbarhet ---
SEED = 42
tf.random.set_seed(SEED)
np.random.seed(SEED)
random.seed(SEED)
os.environ['PYTHONHASHSEED'] = str(SEED)

# --- Dynamisk sökväg till projektfiler ---
current_dir = os.path.dirname(__file__)
data_path = os.path.join(current_dir, 'AllaJobb.csv')

# --- Ladda och förbered data ---
st.toast("📄 Läser in och förbereder data...", icon="📄")
df = pd.read_csv(data_path, skiprows=8)
df = df.dropna(how='all', axis=1)
df = df.dropna(subset=['YRKESOMRÅDE'])
df = df.fillna(0)

time_cols = [col for col in df.columns if '-' in str(col)]

all_series = []
for _, row in df.iterrows():
    values = row[time_cols].values.astype(float)
    all_series.append(values)

all_series = np.array(all_series)
scaler = MinMaxScaler()
normalized_data = scaler.fit_transform(all_series)

# Sliding windows
window_size = 12
X, y = [], []
for serie in normalized_data:
    for i in range(len(serie) - window_size):
        X.append(serie[i:i+window_size])
        y.append(serie[i+window_size])

X = np.array(X)
y = np.array(y)
X = np.expand_dims(X, axis=-1)

print(f"🔍 Antal träningssekvenser: {X.shape[0]}")

# --- Bygg modellen ---
st.toast("🔧 Bygger LSTM-modellen...", icon="🔧")
model = Sequential([
    LSTM(64, activation='tanh', input_shape=(window_size, 1)),
    Dropout(0.2),
    Dense(1)
])
model.compile(optimizer='adam', loss='mse')

# --- Early stopping ---
early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=20,
    restore_best_weights=True,
    verbose=0
)

# --- Träna modellen ---
st.toast("🏋️ Tränar modellen... detta kan ta en stund ⏳", icon="🏋️")
history = model.fit(
    X, y,
    validation_split=0.1,
    epochs=100,
    batch_size=32,
    callbacks=[early_stopping],
    verbose=0
)

# --- Spara modell och scaler ---
model.save(os.path.join(current_dir, 'rnn_model.keras'))
joblib.dump(scaler, os.path.join(current_dir, 'scaler.save'))

# --- Slutlig feedback (terminal, inte webben) ---
best_val_loss = min(history.history['val_loss'])
print(f"✅ Träning klar! Bästa valideringsförlust: {best_val_loss:.6f}")