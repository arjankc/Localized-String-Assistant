# Nepali String Localizer

Context-aware English-to-Nepali UI string translation for open-source localization projects like KoboToolbox.

Paste an isolated UI string (for example `Deploy Form`), describe where it appears, and get three Nepali options:

1. **Formal**: standard written Nepali, for documentation or strict UI.
2. **Colloquial**: natural, conversational Nepali, for friendly everyday app text.
3. **Transliterated/Hybrid**: technical terms kept in English, written in Devanagari (सबमिट, सर्भर) or left in Latin script when translating them would lose the meaning.

Placeholders such as `{name}`, `%s`, `%(count)d` and HTML tags are preserved as-is.

## Why it exists

Volunteer translators on platforms like Transifex or Weblate see strings one at a time, with little or no context. "Deploy" on a button, "Deploy" in a status message, and "Deploy" in docs often need different Nepali wording. This tool gives a translator three context-aware candidates to pick from or edit, so they spend their time reviewing instead of starting from a blank box.

## Open-source AI at its core

The app only talks to **open-weight models**, through one OpenAI-compatible client. You can pick from two providers in the sidebar:

| Provider | Model (default) | Needs internet | Needs API key |
| --- | --- | --- | --- |
| Ollama (local) | `gemma2:9b` | No | No |
| Groq (hosted) | `llama-3.3-70b-versatile` | Yes | Yes (free tier) |

Both models are open-weight, so you can swap models, run fully offline on a laptop, or fine-tune on your project's existing Nepali translations without changing any code.

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

3. Choose a provider.

   **Option A: Local and offline with Ollama**

   Install [Ollama](https://ollama.com), then pull the model:

   ```bash
   ollama pull gemma2:9b
   ```

   Create a `.env` file containing `LLM_PROVIDER=ollama`, or just select Ollama in the sidebar.

   **Option B: Hosted with Groq**

   Get a free API key at [console.groq.com](https://console.groq.com/keys), then create a `.env` file next to `app.py`:

   ```
   GROQ_API_KEY=gsk_your_key_here
   ```

4. Start the app:

   ```bash
   streamlit run app.py
   ```

   Then open http://localhost:8501.

## Configuration

All settings are optional environment variables, read from `.env` (see [.env.example](.env.example)):

| Variable | Default | Purpose |
| --- | --- | --- |
| `LLM_PROVIDER` | `groq` | Provider selected in the sidebar when the app starts (`groq` or `ollama`) |
| `GROQ_API_KEY` | none | Required only for the Groq provider |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | Any chat model available on Groq |
| `OLLAMA_MODEL` | `gemma2:9b` | Any model you have pulled locally (for example `llama3.1:8b`, `qwen2.5:7b`) |
| `OLLAMA_BASE_URL` | `http://localhost:11434/v1` | Point at an Ollama server on another machine |

## Project layout

- `app.py`: the whole Streamlit app (UI, system prompt, provider config and LLM call)
- `requirements.txt`: `streamlit`, `openai`, `python-dotenv`
- `.env.example`: template for your `.env`
- `SUBMISSION.md`: draft post for the DEV Hacktoberfest Weekend Challenge
