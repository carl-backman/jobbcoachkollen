
# 📊 Jobbcoach-kollen

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button.svg)](https://classroom.github.com/a/rjgbNS53)

## 🚀 Projektbeskrivning

Jobbcoach-kollen är en AI-baserad Streamlit-applikation som hjälper jobbcoacher att analysera och förutspå trender på arbetsmarknaden i Sverige.

Projektet kombinerar:
- En egenutvecklad RNN-modell för prediktion av framtida jobbannonser.
- En GPT-modell från OpenAI för generering av trendanalyser och rekommendationer.

## 🛠️ Funktioner

- 📚 Välj yrkesområde och period för framtidsprognos.
- 📈 Visualisera historisk och framtida utveckling av jobbannonser.
- 🧠 Få AI-genererade rekommendationer för jobbcoaching.
- 🔄 Möjlighet att träna om AI-modellen.

## 📦 Installation

1. **Klona eller ladda ner projektet**:
   ```bash
   git clone https://github.com/SVP-GU/group-project-edvicaga.git
   cd group-project-edvicaga/Jobbtrend-analys
   ```

2. **Installera beroenden**:

   - Med klassisk `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

   - Eller med modern `pyproject.toml` (om du använder t.ex. pip 23+):
     ```bash
     pip install .
     ```

3. **Skapa en `.env`-fil** i mappen och lägg till din OpenAI API-nyckel:

   ```plaintext
   OPENAI_API_KEY=sk-din-nyckel-här
   ```

## 📊 Användning

- Kör applikationen med:

   ```bash
   streamlit run app.py
   ```

- Välj ett yrkesområde och antal månader att förutspå.
- Titta på historisk utveckling och framtidsprognos i grafen.
- Läs AI-genererade trendanalyser för att ge bättre stöd till dina arbetssökande.

## 🧠 AI-komponenter

- **Tensorflow RNN** för sekvensprediktion av jobbannonser.
- **OpenAI GPT-3.5-turbo** för naturlig språkförståelse och textgenerering.
- Modellen normaliserar data med **MinMaxScaler** och sparar både modell och scaler.

---

## 📅 Kursinfo

Projektet genomförs som en del av kursen **TIG326: Datadriven Verksamhetsutveckling** vid **Göteborgs Universitet**.

---

# 📬 Kontakt

Vid frågor, kontakta projektgruppen eller handledare via Canvas.
