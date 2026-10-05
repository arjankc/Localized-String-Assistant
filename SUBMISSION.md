---
title: Nepali String Localizer, context-aware UI translation for my friend who localizes open-source tools
published: false
tags: devchallenge, hacktoberfest, opensource, ai
---

*This is a submission for the [Hacktoberfest Weekend Challenge: Build for a Friend](https://dev.to/challenges/hacktoberfest-weekend-2026-10-01)*

<!-- TODO before publishing: replace every [TODO ...] marker, then delete this comment. -->

## What I Built

**Nepali String Localizer** is a small Streamlit app that translates isolated English UI strings into Nepali, using context about where the string appears.

I built it for **[TODO: friend's name]**, who volunteers translating open-source software into Nepali, including KoboToolbox, the data-collection platform that NGOs and field teams in Nepal use for surveys and humanitarian work.

**The problem:** on localization platforms, a translator sees strings one at a time with almost no context. Take `Deploy`. Is it a button, a status message, or a heading in the docs? Each one needs different Nepali. A technical word like "Server" or "Submit" also raises a question: should it be translated, transliterated into Devanagari, or left in English? [TODO: friend's name] was making that call hundreds of times per project, often by switching between a dictionary, a chat window, and the live app to guess the context.

**What it does:** paste the string, add a line of context (for example *"Primary call-to-action button on the server settings page"*), and get three options:

1. **Formal**: standard written Nepali, for docs and strict UI.
2. **Colloquial**: natural, conversational Nepali, for friendly everyday app text.
3. **Transliterated/Hybrid**: technical terms kept in English, written in Devanagari (सबमिट, सर्भर) or left in Latin script when translating them would lose the meaning.

Placeholders like `{name}`, `%s` and HTML tags come back untouched, so a translation never breaks the app.

[TODO: what your friend said when you handed it over. One honest quote is better than a paragraph.]

## Demo

**Try it in your browser:** [TODO: GitHub Pages URL, e.g. https://your-username.github.io/nepali-string-localizer/]. No install and no API key. The first translation downloads a ~1.5 GB open model into your browser cache.

[TODO: short video or GIF: type "Deploy Form", add context, click Translate, show the three options. Turning Wi-Fi off after the model loads is the best proof that it runs offline.]

## Code

[TODO: GitHub repo link or embed, e.g. {% github your-username/nepali-string-localizer %}]

There are two front ends that share one prompt:

- `docs/index.html`: a single static page that runs the model in the browser (WebLLM + WebGPU).
- `app.py`: a ~140-line Streamlit app that talks to a local Ollama server or Groq.

## How I Built It

I built this on a 2018 laptop: an i5-8265U with 16 GB of RAM, integrated Intel UHD 620 graphics and no dedicated GPU. That constraint shaped everything. If it runs on this machine, it runs on my friend's.

- **In-browser inference:** [WebLLM](https://github.com/mlc-ai/web-llm) compiles open-weight models to WebGPU, so **Gemma 2 2B** runs inside a browser tab on integrated graphics. The page checks whether the GPU supports 16-bit float shaders and picks the matching build. Qwen 2.5 1.5B and Llama 3.2 1B are there as lighter options. There's no backend at all: GitHub Pages serves one HTML file, and the model is cached in the browser after the first load.
- **Local inference with Ollama:** for translators who prefer a desktop setup, the Streamlit app runs **Gemma 3 4B** on the CPU through [Ollama](https://ollama.com). Ollama exposes an OpenAI-compatible endpoint, so the standard `openai` Python client talks to it, or to **Llama 3.3 70B** on Groq when more quality is needed. Switching between them only changes the `base_url`.
- **Choosing small models for Nepali:** this was the interesting part. Most tiny models are weak at Nepali. Gemma (trained on 140+ languages) was clearly the best family at 2B to 4B, while 1B models mostly produced broken Devanagari or Hindi. [TODO: confirm or adjust this from your own testing.]
- **Prompting:** one prompt does the heavy lifting. It makes the model act as an English-to-Nepali software localization expert, keep placeholders like `{name}` and `%s` intact, stay short enough for UI text, and return exactly three options in a fixed Markdown template. A low temperature (0.3) keeps the output consistent from string to string. Gemma's chat format has no system role, so the browser version sends the instructions in the user turn.

```mermaid
flowchart LR
    user[Translator] --> web["Browser page: WebLLM + WebGPU"]
    user --> st[Streamlit app]
    web --> gemma2["Gemma 2 2B in the browser tab"]
    st -->|offline| ollama["Ollama: Gemma 3 4B on CPU"]
    st -->|online| groq["Groq: Llama 3.3 70B"]
    gemma2 --> out[Formal / Colloquial / Hybrid]
    ollama --> out
    groq --> out
```

## Why Does Open Innovation Matter?

**It runs on an old laptop, in a browser tab, with no internet.** Volunteer localization doesn't happen on fast office machines. Because the weights are open, a 2B model can be compiled to WebGPU and shipped as a static web page. After the first load, [TODO: friend's name] can translate on a bus, during a load-shedding power cut on battery, or anywhere connectivity is patchy. A closed API simply stops working there.

**Zero setup for the person I built it for.** My friend doesn't need Python, Ollama or an API key. They open a link. A closed model can't be shipped like that; it can only be rented through someone's server.

**It costs nothing to run.** This is volunteer work. Nobody is going to put a credit card on file for a per-token API to translate KoboToolbox strings for free. There's no server to pay for either: GitHub Pages hosts the page, and the visitor's own GPU does the inference.

**Unreleased strings stay on the translator's machine.** Strings from unreleased features and internal admin screens never leave the device in the browser and Ollama versions.

**We can swap models, and eventually fine-tune.** Nepali is a lower-resource language, and different open models handle Devanagari very differently. Because the app only depends on an OpenAI-compatible endpoint, switching from Gemma to Llama to Qwen is a config change, not a rewrite. The next step is fine-tuning a small open model on the existing, human-reviewed Nepali translations from KoboToolbox's own translation files, so it learns the project's established terms. That is only possible because the weights are open.

**Open tools for open tools.** KoboToolbox is open source, and the people translating it are volunteers. It felt right that the tool helping them is open too, so any other localization community (Maithili, Newari, Tamang...) can fork it, change the prompt, and point it at whichever open model handles their language best.

[TODO: one concrete comparison if you have it, e.g. "Gemma kept 'Server' as सर्भर while [closed model] translated it literally", or "worked offline during a power cut".]

## My Agent Session

[TODO: DevRelay agent session embed or link]

## Prize Categories

[TODO: list the partner categories you're entering, or delete this section]
