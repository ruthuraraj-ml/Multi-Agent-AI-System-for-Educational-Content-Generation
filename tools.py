import streamlit as st
import time
import requests
import chromadb
from chromadb.utils import embedding_functions
from huggingface_hub import login 
from crewai.tools import tool

# 1. SETUP AUTHENTICATION
# Pull the token and log in immediately so the embedding function has access
HF_TOKEN = st.secrets["HF_TOKEN"]
login(token=HF_TOKEN)

# 2. DEFINE THE EMBEDDING FUNCTION
# You were missing this definition! This is the 'hf_ef' variable.
hf_ef = embedding_functions.HuggingFaceEmbeddingFunction(
    api_key=HF_TOKEN,
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 3. INITIALIZE CHROMADB
# Now that hf_ef is defined, we can pass it to the collection
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="ai_knowledge", 
    embedding_function=hf_ef
)

# --- TOOLS ---

@tool
def rag_search(query: str) -> str:
    """
    Search the AI knowledge base for specific technical details or context.
    Use this when you need facts that aren't in your general training data.
    """
    try:
        results = collection.query(
            query_texts=[query],
            n_results=1
        )

        if not results["documents"] or not results["documents"][0]:
            return "No relevant information found in the local database."

        context = "\n---\n".join(results["documents"][0])
        return f"Relevant Information Found:\n{context}"

    except Exception as e:
        return f"Search Error: {str(e)}"

@tool
def image_generator(prompt: str) -> str:
    """Generate a text-free minimal educational diagram using the HuggingFace Inference API."""
    
    print(f"🎨 Image Agent: Generating diagram for: {prompt}")
    
    model_id = "black-forest-labs/FLUX.1-schnell"
    # UPDATED: Use the router endpoint instead of the legacy inference endpoint
    API_URL = f"https://router.huggingface.co/hf-inference/models/{model_id}"
    
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
    "inputs": (
        f"{prompt}. "
        "High fidelity scientific educational diagram. "
        "isometric perspective, white background, "
        "Vibrant and technical palette, "
        "soft lighting, ultra sharp focus. "
        "NO TEXT, NO LABELS, NO LETTERS, NO NUMBERS, "
        "NO TYPOGRAPHY, NO SYMBOLS, NO GARBLED CHARACTERS."
        )
    }

    try:
        # It's often good practice to ensure the session is handled or 
        # use a longer timeout for image models like FLUX
        response = requests.post(API_URL, headers=headers, json=payload, timeout=90)
        
        if response.status_code == 200:
            file_name = f"diagram_{int(time.time())}.png"
            with open(file_name, "wb") as f:
                f.write(response.content)
            return f"Image generated successfully and saved as: {file_name}"
            
        else:
            # Added a more descriptive error message for debugging
            return f"Image generation failed: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"An error occurred during image generation: {str(e)}"