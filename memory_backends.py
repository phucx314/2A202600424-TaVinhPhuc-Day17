"""
Memory Backends — Lab #17: Multi-Memory Agent
==============================================
4 backends:
  1. ShortTermMemory   — sliding-window conversation buffer
  2. LongTermProfile   — JSON key-value profile store w/ conflict handling
  3. EpisodicMemory    — JSON list/log of completed tasks & outcomes
  4. SemanticMemory    — Chroma vector store (falls back to keyword search)
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# 1. Short-Term Memory (conversation buffer / sliding window)
# ---------------------------------------------------------------------------

class ShortTermMemory:
    """Sliding-window conversation buffer kept in RAM."""

    def __init__(self, max_turns: int = 10):
        self.max_turns = max_turns
        self._buffer: list[dict] = []   # [{"role": "user"|"assistant", "content": ...}]

    def add(self, role: str, content: str) -> None:
        self._buffer.append({"role": role, "content": content, "ts": time.time()})
        # sliding window — drop oldest pair
        while len(self._buffer) > self.max_turns * 2:
            self._buffer.pop(0)

    def get_recent(self, n_turns: int | None = None) -> list[dict]:
        limit = (n_turns or self.max_turns) * 2
        return self._buffer[-limit:]

    def clear(self) -> None:
        self._buffer.clear()

    def __len__(self) -> int:
        return len(self._buffer)


# ---------------------------------------------------------------------------
# 2. Long-Term Profile Store (JSON KV store, conflict-safe update)
# ---------------------------------------------------------------------------

class LongTermProfile:
    """
    Persistent JSON key-value profile.
    Conflict rule: newer value always wins (last-write-wins per key).
    """

    def __init__(self, path: str = "profile_store.json"):
        self._path = Path(path)
        self._data: dict[str, Any] = {}
        self._history: dict[str, list] = {}   # audit trail per key
        self._load()

    def _load(self) -> None:
        if self._path.exists():
            with open(self._path, "r", encoding="utf-8") as f:
                saved = json.load(f)
                self._data = saved.get("data", {})
                self._history = saved.get("history", {})

    def _save(self) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump({"data": self._data, "history": self._history}, f,
                      ensure_ascii=False, indent=2)

    def update(self, key: str, value: Any, source: str = "user") -> None:
        """Update a profile fact. Overwrites old value (conflict resolution)."""
        old = self._data.get(key)
        self._data[key] = value
        if key not in self._history:
            self._history[key] = []
        self._history[key].append({
            "old": old, "new": value,
            "source": source, "ts": time.time()
        })
        self._save()

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def get_all(self) -> dict:
        return dict(self._data)

    def delete(self, key: str) -> None:
        """Privacy/right-to-forget support."""
        self._data.pop(key, None)
        self._history.pop(key, None)
        self._save()

    def get_history(self, key: str) -> list:
        return self._history.get(key, [])


# ---------------------------------------------------------------------------
# 3. Episodic Memory (JSON append log)
# ---------------------------------------------------------------------------

class EpisodicMemory:
    """
    Log of completed tasks / notable interactions.
    Each episode: {task, outcome, context, ts}
    """

    def __init__(self, path: str = "episodic_log.json"):
        self._path = Path(path)
        self._episodes: list[dict] = []
        self._load()

    def _load(self) -> None:
        if self._path.exists():
            with open(self._path, "r", encoding="utf-8") as f:
                self._episodes = json.load(f)

    def _save(self) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(self._episodes, f, ensure_ascii=False, indent=2)

    def add_episode(self, task: str, outcome: str, context: str = "") -> None:
        ep = {
            "task": task,
            "outcome": outcome,
            "context": context,
            "ts": time.time(),
            "date": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self._episodes.append(ep)
        self._save()

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        """Simple keyword search over episodes."""
        q = query.lower()
        scored = []
        for ep in self._episodes:
            text = f"{ep['task']} {ep['outcome']} {ep['context']}".lower()
            score = sum(1 for word in q.split() if word in text)
            if score > 0:
                scored.append((score, ep))
        scored.sort(key=lambda x: (-x[0], -x[1]["ts"]))
        return [ep for _, ep in scored[:top_k]]

    def get_recent(self, n: int = 3) -> list[dict]:
        return self._episodes[-n:]

    def clear(self) -> None:
        self._episodes.clear()
        self._save()


# ---------------------------------------------------------------------------
# 4. Semantic Memory (Chroma vector store + keyword fallback)
# ---------------------------------------------------------------------------

class SemanticMemory:
    """
    Vector store for FAQ / knowledge chunks.
    Primary: ChromaDB. Falls back to keyword search if Chroma unavailable.
    """

    def __init__(self, collection_name: str = "lab17_semantic",
                 persist_dir: str = "./chroma_store"):
        self._collection_name = collection_name
        self._persist_dir = persist_dir
        self._chroma_ok = False
        self._collection = None
        self._fallback_docs: list[dict] = []
        self._fallback_path = Path("semantic_fallback.json")
        self._init_chroma()
        self._load_fallback()

    def _init_chroma(self) -> None:
        try:
            import chromadb
            from chromadb.utils import embedding_functions

            client = chromadb.PersistentClient(path=self._persist_dir)
            # Use default embedding (sentence-transformers or API key based)
            ef = embedding_functions.DefaultEmbeddingFunction()
            self._collection = client.get_or_create_collection(
                self._collection_name,
                embedding_function=ef
            )
            self._chroma_ok = True
        except Exception as e:
            print(f"[SemanticMemory] Chroma init failed ({e}), using keyword fallback.")

    def _load_fallback(self) -> None:
        if self._fallback_path.exists():
            with open(self._fallback_path, "r", encoding="utf-8") as f:
                self._fallback_docs = json.load(f)

    def _save_fallback(self) -> None:
        with open(self._fallback_path, "w", encoding="utf-8") as f:
            json.dump(self._fallback_docs, f, ensure_ascii=False, indent=2)

    def add_document(self, doc_id: str, text: str, metadata: dict | None = None) -> None:
        meta = metadata or {}
        # Chroma requires non-empty metadata dict
        if not meta:
            meta = {"source": "default"}
        if self._chroma_ok and self._collection is not None:
            try:
                self._collection.upsert(
                    ids=[doc_id],
                    documents=[text],
                    metadatas=[meta]
                )
                return
            except Exception as e:
                print(f"[SemanticMemory] Chroma upsert failed ({e}), falling back.")
        # fallback
        entry = {"id": doc_id, "text": text, "metadata": meta}
        self._fallback_docs = [d for d in self._fallback_docs if d["id"] != doc_id]
        self._fallback_docs.append(entry)
        self._save_fallback()

    def search(self, query: str, top_k: int = 3) -> list[str]:
        if self._chroma_ok and self._collection is not None:
            try:
                results = self._collection.query(
                    query_texts=[query],
                    n_results=min(top_k, max(1, self._collection.count()))
                )
                docs = results.get("documents", [[]])[0]
                return docs
            except Exception as e:
                print(f"[SemanticMemory] Chroma query failed ({e}), using fallback.")
        # keyword fallback
        q = query.lower()
        scored = []
        for doc in self._fallback_docs:
            score = sum(1 for word in q.split() if word in doc["text"].lower())
            if score > 0:
                scored.append((score, doc["text"]))
        scored.sort(key=lambda x: -x[0])
        return [text for _, text in scored[:top_k]]

    def count(self) -> int:
        if self._chroma_ok and self._collection is not None:
            try:
                return self._collection.count()
            except Exception:
                pass
        return len(self._fallback_docs)
