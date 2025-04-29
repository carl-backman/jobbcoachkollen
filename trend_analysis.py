import openai
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gpt_trend_analysis(yrkesomrade, dates, historical, future_dates, preds):
    historical_start = historical[0]
    historical_end = historical[-1]
    future_end = preds[-1]

    prompt = f"""
    Du är en expert på arbetsmarknadstrender i Sverige och agerar som en rådgivande röst till jobbcoacher.

    Analysen gäller yrkesområdet: {yrkesomrade}.

    Historiskt har antalet jobbannonser i detta område gått från {int(historical_start)} till {int(historical_end)} per månad.
    Den senaste prognosen visar en förväntad nivå runt {int(future_end)} jobbannonser per månad.

    Skriv ett sammanfattande textstycke på svenska, riktat till en jobbcoach.  
    Texten ska vara informativ, saklig och professionell – inte reklamliknande.  
    Undvik utropstecken och overly positive språk.  
    Du får gärna använda lätt punktform, men utan numrering.

    Fokusera på:
    - Vad trenden tyder på
    - Vad som kan påverka den
    - Vad coachen konkret kan tänka på eller föra vidare till sin klient

    Max 12 meningar totalt. Använd styckesindelning eller punktform för att göra texten mer läsbar och strukturerad.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du är en hjälpsam expert på arbetsmarknadstrender och rådgivning till jobbcoacher."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=400,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Fel vid GPT-anrop: {e}")
        return "❌ Kunde inte analysera trenden (OpenAI API-fel)."
