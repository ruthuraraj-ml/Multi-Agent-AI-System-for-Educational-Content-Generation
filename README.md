# 🤖 AI Content Studio
### Multi-Agent AI System for Educational Content Generation

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-6C63FF?style=flat)
![Groq](https://img.shields.io/badge/Groq-LLM-F55036?style=flat)
![Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?style=flat&logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-Educational-green?style=flat)

> An interactive multi-agent AI application that generates structured educational explanations and diagrams through coordinated AI agent collaboration.

---

## 📌 Overview

AI Content Studio demonstrates a **hierarchical multi-agent orchestration system** where specialized AI agents work together to produce high-quality educational content on any topic.

The system coordinates:
- A **Manager Agent** (Google Gemini Flash) that orchestrates the entire workflow
- A **Research Agent** (Groq Llama-3 70B) that retrieves knowledge via RAG
- An **Image Agent** (Groq Llama-3 8B → HuggingFace FLUX) that generates educational diagrams
- A **Reviewer Agent** (Groq Llama-3 8B) that refines and structures the final explanation

---

## 🧠 System Architecture

```
User Input (Topic)
        │
        ▼
┌───────────────────────┐
│   Manager Agent       │  ← Google Gemini Flash
│   (Orchestrator)      │    Hierarchical delegation
└──────────┬────────────┘
           │
     ┌─────┴──────┬──────────────┐
     ▼            ▼              ▼
┌─────────┐  ┌─────────┐  ┌──────────┐
│Research │  │  Image  │  │Reviewer  │
│ Agent   │  │  Agent  │  │  Agent   │
│Groq 70B │  │Groq 8B  │  │Groq  8B  │
│+ RAG    │  │+ FLUX   │  │          │
└────┬────┘  └────┬────┘  └────┬─────┘
     │            │             │
     ▼            ▼             ▼
  Facts      Diagram PNG    Structured
                            Explanation
                │
                ▼
        ┌───────────────┐
        │ Final Output  │
        │ Explanation + │
        │ Diagram       │
        └───────────────┘
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 Multi-Agent Orchestration | Hierarchical CrewAI system with a manager coordinating 3 specialists |
| 🔀 Multi-LLM Architecture | Gemini + Groq 70B + Groq 8B assigned by task complexity |
| 📚 RAG Knowledge Base | ChromaDB + Sentence Transformers for domain-specific retrieval |
| 🎨 AI Diagram Generation | HuggingFace FLUX.1-schnell for educational visual diagrams |
| 📊 Live Agent Logs | Real-time agent activity visible in the Streamlit UI |
| ⚡ Token-Optimised | Smart model assignment minimises API rate limit issues |

---

## 📦 Project Structure

```
ai-content-studio/
│
├── app.py              # Streamlit UI + logger
├── crew_setup.py       # CrewAI Crew + Task definition
├── agents.py           # Agent roles, goals, LLM assignments
├── llm.py              # Multi-LLM configuration (Gemini + Groq)
├── tools.py            # RAG search + image generation tools
├── rag_system.py       # ChromaDB knowledge base indexing
│
├── data/
│   └── ai_combined_notes.txt   # Source knowledge base text
│
├── chroma_db/          # Persistent vector store (auto-generated)
│
├── .streamlit/
│   └── secrets.toml    # API keys (never commit this)
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/ai-content-studio
cd ai-content-studio
```

**2. Create a virtual environment**

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

---

## 🔑 API Keys

You need three free API keys:

| Key | Where to get it |
|---|---|
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) |
| `GEMINI_API_KEY` | [aistudio.google.com](https://aistudio.google.com) |
| `HF_TOKEN` | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) |

**For Streamlit (recommended):**

Create `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "gsk_..."
GEMINI_API_KEY = "AIza..."
HF_TOKEN = "hf_..."
```

**For local development:**

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

---

## 🗄️ Setting Up the Knowledge Base

Before running the app, index your knowledge base:

```bash
python rag_system.py
```

This reads `data/ai_combined_notes.txt`, chunks it, and stores embeddings in `chroma_db/`.

> Only needs to be run once. Subsequent runs skip re-indexing automatically.

---

## ▶️ Running the App

```bash
streamlit run app.py
```

Open your browser at:

```
http://localhost:8501
```

Enter any AI topic and click **Generate Content**.

---

## 🖥️ Example Output

**Input:** `Reinforcement Learning`

**Output:**
- ✅ Structured 200-word explanation (Concept / Core Idea / How It Works / Why It Matters / Application)
- ✅ AI-generated educational diagram (text-free, isometric, colourful)
- ✅ Live agent activity log in the sidebar

---

## 🔧 Multi-LLM Design

One of the core design decisions in this project is **assigning different LLMs to different agents based on task complexity**, reducing token usage and avoiding rate limits:

```python
# Manager — Gemini Flash (generous free tier, good at delegation)
llm_manager  = LLM(model="gemini/gemini-2.0-flash")

# Research — Groq 70B (needs reasoning to synthesise RAG chunks)
llm_research = LLM(model="groq/llama-3.3-70b-versatile")

# Reviewer + Image — Groq 8B (simple tasks, fast and token-efficient)
llm_reviewer = LLM(model="groq/llama-3.1-8b-instant")
llm_image    = LLM(model="groq/llama-3.1-8b-instant")
```

---

## 🎓 Workshop Use

This project is designed for **hands-on Agentic AI workshops**.

Each participant should:

1. Fork or clone the repository
2. Add their own API keys to `.streamlit/secrets.toml`
3. Run `python rag_system.py` once to index the knowledge base
4. Run `streamlit run app.py`

Using individual keys avoids shared rate limit issues during live sessions.

---

## 🔧 Possible Extensions

- Add more specialist agents (fact-checker, summariser, quiz generator)
- Support local LLMs via Ollama or LM Studio
- Expand the RAG knowledge base with your own documents
- Deploy to Streamlit Cloud or Hugging Face Spaces
- Add topic history and session persistence

---

## 📚 Tech Stack

- [CrewAI](https://github.com/joaomdmoura/crewAI) — Multi-agent orchestration
- [Streamlit](https://streamlit.io) — Interactive web UI
- [Groq](https://groq.com) — Fast LLM inference (Llama 3)
- [Google Gemini](https://ai.google.dev) — Manager agent LLM
- [HuggingFace](https://huggingface.co) — FLUX image generation + embeddings
- [ChromaDB](https://www.trychroma.com) — Vector database for RAG
- [Sentence Transformers](https://www.sbert.net) — Text embeddings

---

## 🤝 Contributing

Contributions welcome. Areas to improve:

- Better prompt engineering for agents
- New tools for agents to use
- UI improvements
- Additional LLM provider support

---

## 📜 License

Open-source for educational and research use.

---

## ⭐ Acknowledgements

Built using CrewAI, Groq, Google Gemini, Hugging Face, and Streamlit.
