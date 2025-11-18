# aes_task — RAG API

Simple FastAPI app that builds a small RAG index (sentence-transformers + Chroma) from `knowladge.txt`
and exposes a POST /ask endpoint. Ollama is optionally used to synthesize answers; otherwise an extractive
answer is returned.

## Prerequisites
- macOS with Python 3.13.5 (or compatible 3.x)
- Homebrew (optional) for pyenv or Python installs
- Recommended: create and activate a venv for the project

## Quick setup
1. Create & activate venv (use your Python 3.13 binary)
```bash
python3.13 -m venv venv
source venv/bin/activate
```

2. Fix requirements typo if present: open `requirements.txt` and replace `unicorn` → `uvicorn`.

3. Install dependencies
```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

4. Build the index (the app does this on startup using `knowladge.txt`).

## Run
Start the server (use the venv python):
```bash
python -m uvicorn main:app --reload
```

Server will be available at: `http://127.0.0.1:8000`

## API
POST /ask
- Payload: JSON { "question": "your question" }
- Response: JSON { "response": "<answer>" }

Example:
```bash
curl -sS -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"what are your support hours?"}' | jq
```

## Notes
- Ollama: if installed and on PATH, the app will attempt to use it for answers. Set `OLLAMA_MODEL` env var to change model name.
- If Chroma reports `Collection already exists`, delete the collection in code or restart with a different `collection_name`.
- Keep `knowladge.txt` updated with domain text you want indexed. The app splits text into chunks and indexes them on startup.
- For portability, prefer using `python -m uvicorn` so the correct interpreter/venv is used.

## Troubleshooting
- `ModuleNotFoundError: langchain.community`: this project does not require langchain; remove it from requirements if unnecessary.
- If pip fails to build packages requiring Rust (e.g., bcrypt), install Rust via rustup or pin to packages with wheels.
