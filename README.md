```markdown
# 🔍 AES Task — RAG API (FastAPI + Chroma + Sentence Transformers)

A lightweight, efficient RAG (Retrieval-Augmented Generation) API built with **FastAPI**, **ChromaDB**, and **Sentence Transformers**.  
The API loads knowledge from `knowladge.txt`, performs vector search using MiniLM embeddings, and returns concise extractive answers.

The API is deployed live on Hugging Face and can be tested using Postman or cURL.

---

## 🚀 Live API Endpoint (HuggingFace)

**POST**  
```

[https://ilanthalirs-aes-chatbot.hf.space/ask](https://ilanthalirs-aes-chatbot.hf.space/ask)

````

### Example JSON body:
```json
{
  "question": "What information do you have?"
}
````

---

## 🧪 Postman Collection

You can test the API via Postman using this workspace:

🔗 **Postman Link:**
[https://fintech-9424.postman.co/workspace/Team-Workspace~b3c618e1-f598-44b0-8ccb-399d921682c0/request/46051251-50bcdcbe-5326-46eb-ac6f-8ac3a58dcd85?action=share&creator=46051251&ctx=documentation](https://fintech-9424.postman.co/workspace/Team-Workspace~b3c618e1-f598-44b0-8ccb-399d921682c0/request/46051251-50bcdcbe-5326-46eb-ac6f-8ac3a58dcd85?action=share&creator=46051251&ctx=documentation)

---

## 📦 Features

* Fast, CPU-friendly document embeddings (`all-MiniLM-L6-v2`)
* In-memory vector search using ChromaDB
* Simple extractive answer generation (no GPU or large model required)
* Small codebase, quick to deploy anywhere
* Automatically indexes `knowladge.txt` on startup

---

## 🧰 **Local Development Setup**

### 1. Create & activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 2. Install dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 3. Run the API locally

```bash
uvicorn main:app --reload
```

Your API will be available at:

```
http://127.0.0.1:8000
```

---

## 📡 API Usage

### ▶️ **POST /ask**

**Request body:**

```json
{
  "question": "your question here"
}
```

**Response:**

```json
{
  "response": "Your answer based on knowladge.txt"
}
```

---

## 🧪 cURL Example

```bash
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What are your support hours?\"}"
```

---

## 📁 Project Structure

```
├── main.py               # FastAPI server
├── rag_system.py         # RAG pipeline (Chroma + MiniLM)
├── knowladge.txt         # Your custom knowledge base
├── requirements.txt
├── Dockerfile            # Only for deployment (not required locally)
└── README.md
```

---

## 📝 Notes

* The system uses **extractive RAG**, not generative LLMs.
  This keeps the API extremely fast and low-resource.
* Update `knowladge.txt` any time — the index rebuilds on startup.
* If Chroma shows `Collection already exists`, restart the API.
* No Ollama is used in this build (fully CPU-compatible).

---

## 🛠 Troubleshooting

➤ **Sentence-transformers slow install?**
Ensure you have pip ≥ 23:

```bash
pip install --upgrade pip
```

➤ **Rust-related pip build errors?**
Pin problematic packages or install Rust:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

---

## 📜 License

MIT License © 2025

