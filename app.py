import streamlit as st
import os
from importlib import reload

# --- Grundinställningar ---
st.set_page_config(page_title="Jobbcoach-kollen", page_icon="📊", layout="wide")

# --- Kontrollera och bygg modell om den saknas ---
MODEL_FILE = "rnn_model.keras"
SCALER_FILE = "scaler.save"

if not os.path.exists(MODEL_FILE) or not os.path.exists(SCALER_FILE):
    with st.spinner("🛠 Ingen AI-modell hittades – bygger en ny modell..."):
        import train_model
    # Ladda om ai_predictor efter träning
    import ai_predictor
    reload(ai_predictor)
    from ai_predictor import predict_future
else:
    from ai_predictor import predict_future

from data_loader import load_and_prepare_data
from layout import render_forecast_and_analysis, render_footer

# --- Begränsa sidbredden ---
st.markdown("""
    <style>
        .block-container {
            max-width: 1200px;
            padding-left: 2rem;
            padding-right: 2rem;
            margin: auto;
        }
    </style>
""", unsafe_allow_html=True)

# --- Kontrollera att datafilen finns ---
DATA_FILE = "AllaJobb.csv"
if not os.path.exists(DATA_FILE):
    st.error(f"🚫 Datafilen '{DATA_FILE}' hittades inte. Kontrollera filnamnet och lägg filen i rätt mapp.")
    st.stop()

# --- Ladda data ---
df_long = load_and_prepare_data(DATA_FILE)
yrkesomraden = sorted(df_long['YRKESOMRÅDE'].unique())

# --- Appens titel ---
st.title("📊 Jobbcoach-kollen")
st.markdown("Hjälper jobbcoacher att förstå trender på arbetsmarknaden baserat på AI-prediktioner.")
st.divider()

# --- Yrkesområde och antal månader ---
val = st.selectbox("📚 Välj kundens yrkesområde:", yrkesomraden)
manader = st.number_input("📅 Hur många månader vill du förutspå?", min_value=1, max_value=24, value=6, step=1)

# --- Förutspå-knapp ---
if st.button("🔮 Förutspå framtid"):
    with st.spinner('🔍 AI-modellen förutspår framtiden...'):
        dates, historical, future = predict_future(val, manader)

    if dates is None:
        st.error("⚠️ Yrkesområdet hittades inte i AI-modellen eller modellen är inte laddad. Försök igen.")
    else:
        future_dates, preds = future
        st.subheader("📈 Prognos och AI-analys")
        render_forecast_and_analysis(dates, historical, future_dates, preds, val)

# --- Footer ---
render_footer()