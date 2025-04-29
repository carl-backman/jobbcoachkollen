import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from trend_analysis import gpt_trend_analysis

def render_forecast_and_analysis(dates, historical, future_dates, preds, yrkesomrade):
    col1, col2 = st.columns([1, 1])

    with col1:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(dates, historical, linewidth=3, label="Historisk data", color="dodgerblue")
        ax.plot(future_dates, preds,  '--', linewidth=3, label="Förutsägelse", color="orange")

        all_dates = np.concatenate([dates, future_dates])
        all_values = np.concatenate([historical, preds])
        x_all = mdates.date2num(all_dates)
        z = np.polyfit(x_all, all_values, 1)
        p = np.poly1d(z)
        trend_all = p(x_all)
        ax.plot(all_dates, trend_all, linewidth=2, color="gray", linestyle="--", label="Trendlinje")

        ax.set_title(f"Utveckling av {yrkesomrade.capitalize()}")
        ax.set_ylabel("Antal annonser")
        ax.grid(True)
        ax.legend()
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        fig.autofmt_xdate(rotation=0, ha='center')

        st.pyplot(fig)

    with col2:
        with st.spinner('✍️ AI analyserar jobbtrenden...'):
            analysis_text = gpt_trend_analysis(yrkesomrade, dates, historical, future_dates, preds)

        with st.expander("🧠 Klicka för att läsa AI-analys av trenden", expanded=True):
            st.write(analysis_text)

def render_footer():
    st.markdown("""
        <hr style="margin-top: 3rem; margin-bottom: 1rem">
        <div style='text-align: center; font-size: 0.9rem; color: gray;'>
            © 2025 Göteborgs Universitet – <i>Jobbcoach-kollen</i><br>
            Projektarbete i kursen <b>TIG326: Datadriven Verksamhetsutveckling</b>
        </div>
    """, unsafe_allow_html=True)
