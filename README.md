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

The tool only uses **open-weight models**. It comes in two forms that share the same prompt:

| Version | Where the model runs | Model (default) | Needs internet | Needs install or key |
| --- | --- | --- | --- | --- |
| Browser (`docs/index.html`) | In your browser via WebGPU | Gemma 2 2B | Only for the first model download | No |
| Streamlit + Ollama | Local CPU via Ollama | `gemma3:4b` | No | Python + Ollama |
| Streamlit + Groq | Groq's servers | `llama-3.3-70b-versatile` | Yes | Free API key |

Because every model is open-weight, you can swap models, run fully offline on a laptop, or fine-tune on your project's existing Nepali translations.

## Browser version (zero install)

[docs/index.html](docs/index.html) is a single static page that runs the model inside the browser with [WebLLM](https://github.com/mlc-ai/web-llm). There's no backend, and strings never leave the device.

- **Try it locally:** run `python -m http.server 8000 --directory docs`, then open http://localhost:8000. The page must be served over HTTP; opening the file directly won't work.
- **Host it for free:** in your GitHub repo, open Settings, then Pages, and choose Deploy from a branch, `main`, `/docs`. Share the resulting URL with your translator friend.
- **Requirements:** a WebGPU browser, such as recent Chrome or Edge on desktop. It works on integrated graphics; it was tested on Intel UHD 620. The first translation downloads the model (about 1 to 1.5 GB) into the browser cache; after that the page works offline.
- **Models:** Gemma 2 2B (default, best Nepali), Qwen 2.5 1.5B, and Llama 3.2 1B (fastest, weakest Nepali). The page picks 16-bit or 32-bit builds automatically depending on what the GPU supports.

The prompt in `docs/index.html` is a copy of `SYSTEM_PROMPT` in `app.py`. If you change one, update the other.

## Run the Streamlit app locally

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
   ollama pull gemma3:4b
   ```

   Create a `.env` file containing `LLM_PROVIDER=ollama`, or just select Ollama in the sidebar.

   No GPU is needed: Ollama runs on the CPU. See [Choosing a local model](#choosing-a-local-model) if your laptop is slow.

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
| `OLLAMA_MODEL` | `gemma3:4b` | Any model you have pulled locally (see below) |
| `OLLAMA_BASE_URL` | `http://localhost:11434/v1` | Point at an Ollama server on another machine |

## Choosing a local model

The default, `gemma3:4b`, is built to run on an ordinary laptop. It was developed on a 2018 i5 laptop with 16 GB of RAM and integrated Intel graphics, with no dedicated GPU. Small models vary a lot in how well they handle Nepali, so choose deliberately:

| Model | Download | Nepali quality | When to use |
| --- | --- | --- | --- |
| `gemma3:4b` | ~3.3 GB | Good for its size (trained on 140+ languages) | Default. Best balance on a CPU-only laptop. |
| `gemma2:2b` | ~1.6 GB | Fair | Very slow machines or 8 GB of RAM |
| `gemma3:12b` | ~8 GB | Better | 16 GB+ RAM and a GPU, or when you can wait |
| `llama3.2:3b`, `qwen2.5:3b` | ~2 GB | Weak | Not recommended for Nepali |
| Models of 1B or smaller | under 1 GB | Poor | Not recommended for Nepali |

To switch, run `ollama pull <model>`, then set `OLLAMA_MODEL=<model>` in `.env`.

If the machine is too slow even for these, use Groq: the same open-weight approach, served remotely on a free tier.

## Project layout

- `app.py`: the whole Streamlit app (UI, system prompt, provider config and LLM call)
- `docs/index.html`: the zero-install browser version (WebLLM + WebGPU), servable by GitHub Pages
- `requirements.txt`: `streamlit`, `openai`, `python-dotenv`
- `.env.example`: template for your `.env`
- `SUBMISSION.md`: draft post for the DEV Hacktoberfest Weekend Challenge
