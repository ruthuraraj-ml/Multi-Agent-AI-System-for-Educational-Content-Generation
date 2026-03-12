import streamlit as st
import os
from crewai import LLM

groq_api_key = st.secrets["GROQ_API_KEY"]
gemini_api_key = st.secrets["GEMINI_API_KEY"]

os.environ["GROQ_API_KEY"] = groq_api_key
os.environ["GEMINI_API_KEY"] = gemini_api_key

# ─────────────────────────────────────────────
# MANAGER → Gemini Flash
# Why: Makes 10+ orchestration calls per run,
#      hits Groq TPM hard. Gemini free tier is
#      much more generous (1M tokens/day free).
#      Also better at strict instruction following.
# ─────────────────────────────────────────────
llm_manager = LLM(
    model="gemini/gemini-3.1-flash-lite-preview",  # gemini/gemini-2.5-flash-lite, gemini/gemini-2.5-flash
    temperature=0.1,
    max_tokens=500,
    respect_context_window=True 
)

# ─────────────────────────────────────────────
# RESEARCH AGENT → Groq 70b
# Why: RAG needs actual reasoning to synthesize
#      retrieved chunks into a coherent summary.
#      70b is the smartest Groq model available.
# ─────────────────────────────────────────────
llm_research = LLM(
    model="groq/llama-3.1-8b-instant",
    max_tokens=500,
    temperature=0.1
)

# ─────────────────────────────────────────────
# REVIEWER AGENT → Groq 8b
# Why: Rewriting/trimming text is a simple task,
#      doesn't need a big model. 8b is fast and
#      cheap on TPM for this mechanical task.
# ─────────────────────────────────────────────
llm_reviewer = LLM(
    model="groq/llama-3.3-70b-versatile",
    max_tokens=1000,
    temperature=0.3
)

# ─────────────────────────────────────────────
# IMAGE AGENT → Groq 8b (minimal tokens)
# Why: This agent just formats a prompt string
#      and calls image_generator tool. It doesn't
#      need intelligence, just tool-calling ability.
#      Lowest token usage of all agents.
# ─────────────────────────────────────────────
llm_image = LLM(
    model="groq/llama-3.1-8b-instant",
    max_tokens=150,
    temperature=0.3
)

