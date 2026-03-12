from crewai import LLM, Agent, Task, Crew
import langchain_text_splitters
from sentence_transformers import SentenceTransformer
import chromadb


with open(r"C:\Users\ruthu\OneDrive\Desktop\AI Content Studio-Multi Agent System\data\ai_combined_notes.txt", "r", encoding="utf-8") as f:
    text = f.read()

splitter = CharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = splitter.split_text(text)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = embedding_model.encode(chunks)


# 1. Point to a folder on your computer
client = chromadb.PersistentClient(path="./chroma_db")

# 2. Use 'get_or_create' so it doesn't crash on the second run
collection = client.get_or_create_collection("ai_knowledge")

# 3. Only add data if the database is currently empty
if collection.count() == 0:
    print("Database empty. Indexing chunks...")
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[str(i)]
        )
    print("Indexing complete.")
else:
    print(f"Database already contains {collection.count()} chunks. Skipping indexing.")


