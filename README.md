# Nepali String Localizer

Context-aware English-to-Nepali UI string translation for open-source localization (e.g. KoboToolbox). Gives three options per string: Formal, Colloquial, and Transliterated/Hybrid.

## Run locally

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Get a free API key at [console.groq.com](https://console.groq.com/keys) and create a `.env` file next to `app.py`:

   ```
   GROQ_API_KEY=gsk_your_key_here
   ```

   Optionally set `GROQ_MODEL=` to use a different Groq model (default: `llama-3.3-70b-versatile`).

4. Start the app:

   ```bash
   streamlit run app.py
   ```

   Then open http://localhost:8501.
