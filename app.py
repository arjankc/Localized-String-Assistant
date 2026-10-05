import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

PROVIDERS = {
    "groq": {
        "label": "Groq (hosted open-weight model)",
        "base_url": "https://api.groq.com/openai/v1",
        "model_env": "GROQ_MODEL",
        "default_model": "llama-3.3-70b-versatile",
    },
    "ollama": {
        "label": "Ollama (local, offline)",
        "base_url_env": "OLLAMA_BASE_URL",
        "base_url": "http://localhost:11434/v1",
        "model_env": "OLLAMA_MODEL",
        "default_model": "gemma2:9b",
    },
}

SYSTEM_PROMPT = """You are an expert English-to-Nepali software localization translator.
You translate isolated English UI strings from open-source software (such as KoboToolbox) into Nepali.

You will receive an English UI string and, optionally, context describing where it appears in the interface.
Use the context to pick the right meaning, grammatical form, and tone.

Rules:
- Preserve placeholders, variables, and markup exactly as written (e.g. {name}, %s, %(count)d, {{count}}, <b>, </a>).
- Keep translations concise and appropriate for UI text (buttons, labels, messages).
- Return EXACTLY three translation options, using EXACTLY this Markdown template and nothing else:

### 1. Formal
**<translation in standard written Nepali>**

<one short sentence on when to use it, e.g. official documentation or strict UI>

### 2. Colloquial
**<translation in natural, conversational Nepali>**

<one short sentence on when to use it, e.g. user-friendly everyday app usage>

### 3. Transliterated/Hybrid
**<translation keeping technical terms in English, written in Devanagari (e.g. "सबमिट", "सर्भर"), or kept in Latin script where a Nepali translation would lose the technical meaning>**

<one short sentence explaining which terms were kept in English and why>

Do not add any preamble before the first heading or any extra sections after the third option."""


def build_user_message(text: str, context: str) -> str:
    context = context.strip() or "Not provided"
    return f'English UI string: "{text.strip()}"\nContext: {context}'


def translate(base_url: str, api_key: str, model: str, text: str, context: str) -> str:
    client = OpenAI(base_url=base_url, api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        temperature=0.3,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_message(text, context)},
        ],
    )
    return response.choices[0].message.content


st.set_page_config(page_title="Nepali String Localizer", page_icon="🇳🇵", layout="centered")
load_dotenv()

default_provider = os.getenv("LLM_PROVIDER", "groq").strip().lower()
if default_provider not in PROVIDERS:
    default_provider = "groq"

with st.sidebar:
    st.header("Settings")
    provider = st.radio(
        "Provider",
        options=list(PROVIDERS),
        index=list(PROVIDERS).index(default_provider),
        format_func=lambda key: PROVIDERS[key]["label"],
    )
    config = PROVIDERS[provider]
    model = os.getenv(config["model_env"], "").strip() or config["default_model"]
    base_url = os.getenv(config.get("base_url_env", ""), "").strip() or config["base_url"]

    if provider == "groq":
        api_key = os.getenv("GROQ_API_KEY", "").strip()
    else:
        # Ollama ignores the key, but the OpenAI client requires a non-empty one.
        api_key = "ollama"

    st.markdown(f"**Model:** `{model}`")
    if provider == "groq":
        if api_key:
            st.success("GROQ_API_KEY is set")
        else:
            st.error("GROQ_API_KEY is missing")
    else:
        st.info(f"Using local Ollama at `{base_url}`. Run `ollama pull {model}` first.")

st.title("Nepali String Localizer")
st.subheader("Context-Aware UI Translation for Open Source")
st.caption(
    "Translate isolated English UI strings into Nepali for software localization "
    "projects like KoboToolbox. Add context so the translation fits where the string appears."
)

source_text = st.text_area(
    "English UI String",
    placeholder='e.g. "Deploy Form" or "Data validation failed"',
    height=100,
)
context = st.text_input(
    "Context",
    placeholder="e.g. Primary call-to-action button on the server settings page",
)

if st.button("Translate to Nepali", type="primary", use_container_width=True):
    if not source_text.strip():
        st.warning("Please enter an English UI string to translate.")
    elif not api_key:
        st.error(
            "GROQ_API_KEY is not set. Create a `.env` file next to `app.py` containing "
            "`GROQ_API_KEY=your_key_here`, then restart the app. "
            "Or switch to the local Ollama provider in the sidebar."
        )
    else:
        try:
            with st.spinner(f"Translating with {model}..."):
                result = translate(base_url, api_key, model, source_text, context)
        except Exception as e:
            st.error(f"Translation failed: {e}")
        else:
            st.divider()
            st.markdown(result)
            with st.expander("Raw output (copy-friendly)"):
                st.code(result, language="markdown")
