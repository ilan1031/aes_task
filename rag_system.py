import os
import re
import subprocess
from typing import List, Dict, Any

import chromadb
from sentence_transformers import SentenceTransformer


def load_and_split_documents(file_path: str, chunk_size: int = 1000) -> List[Dict[str, str]]:
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read().strip()
    if not text:
        return []
    sents = re.split(r'(?<=[\.\?\!])\s+', text)
    chunks, cur, cur_len, idx = [], [], 0, 0
    for s in sents:
        s = s.strip()
        if not s:
            continue
        if cur_len + len(s) + 1 <= chunk_size:
            cur.append(s); cur_len += len(s) + 1
        else:
            chunks.append({"id": str(idx), "text": " ".join(cur).strip()}); idx += 1
            cur, cur_len = [s], len(s) + 1
    if cur:
        chunks.append({"id": str(idx), "text": " ".join(cur).strip()})
    return chunks


def create_vector_store(chunks: List[Dict[str, str]], collection_name: str = "documents") -> Dict[str, Any]:
    if not chunks:
        raise ValueError("No chunks to index")
    texts = [c["text"] for c in chunks]
    ids = [c["id"] for c in chunks]
    model = SentenceTransformer("all-MiniLM-L6-v2")
    emb = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    emb_list = emb.tolist() if hasattr(emb, "tolist") else [list(map(float, e)) for e in emb]
    client = chromadb.Client()
    try:
        client.delete_collection(name=collection_name)
    except Exception:
        pass
    coll = client.create_collection(name=collection_name)
    coll.add(ids=ids, documents=texts, embeddings=emb_list)
    return {"collection": coll, "model": model}


def _call_ollama(prompt: str, model_name: str = "llama2") -> str:
    cmd = ["ollama", "generate", model_name, prompt]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "ollama failed")
    return (proc.stdout or proc.stderr).strip()


def setup_rag_chain(vector_store: Dict[str, Any], top_k: int = 3, prefer_ollama: bool = True):
    coll = vector_store["collection"]
    model = vector_store["model"]

    def _extractive(q: str, docs: List[str]) -> str:
        qt = set(re.findall(r"\w+", q.lower()))
        scored = []
        for d in docs:
            for s in re.split(r'(?<=[\.\?\!])\s+', d):
                toks = re.findall(r"\w+", s.lower())
                if not toks:
                    continue
                scored.append((len(qt & set(toks)) / (len(toks) + 1e-9), s.strip()))
        scored.sort(key=lambda x: x[0], reverse=True)
        picks = [s for sc, s in scored if sc > 0][:2]
        if picks:
            return " ".join(picks)
        return (re.split(r'(?<=[\.\?\!])\s+', docs[0])[0].strip() if docs else "No relevant information found.")

    def qa_chain(question: str) -> Dict[str, str]:
        q_emb = model.encode([question], show_progress_bar=False, convert_to_numpy=True)
        qv = q_emb.tolist() if hasattr(q_emb, "tolist") else [float(x) for x in q_emb]
        res = coll.query(query_embeddings=qv, n_results=top_k, include=["documents"])
        docs = res.get("documents", [[]])[0] if res.get("documents") is not None else []
        if prefer_ollama and docs:
            ctx = "\n\n---\n\n".join(f"Source {i+1}:\n{d}" for i, d in enumerate(docs))
            prompt = f"Context:\n{ctx}\n\nQuestion: {question}\n\nAnswer concisely and cite source numbers."
            try:
                return {"result": _call_ollama(prompt, model_name=os.getenv("OLLAMA_MODEL", "llama2"))}
            except Exception:
                pass
        return {"result": _extractive(question, docs)}

    return qa_chain