# Lab #17 — Multi-Memory Agent với LangGraph

> **Mục tiêu:** Build Multi-Memory Agent với LangGraph  
> **Deliverable:** Agent với full memory stack + benchmark report: so sánh agent có/không memory trên 10 multi-turn conversations

---

## 📦 Cấu trúc project

```
lab17/
├── src/
│   ├── memory_backends.py # 4 memory backends (short/long/episodic/semantic)
│   └── agent.py           # LangGraph state/router + prompt injection
├── scripts/
│   └── benchmark.py       # Benchmark 10 multi-turn conversations
├── data/
│   ├── profile_store.json     # Long-term profile (auto-generated)
│   ├── episodic_log.json      # Episodic memory log (auto-generated)
│   └── semantic_fallback.json # Semantic fallback store (auto-generated)
├── docs/
│   ├── day02-assess-01-rubric-guidance.md
│   └── day02-memory-systems-for-agents.pdf
├── BENCHMARK.md           # Output benchmark report
├── chroma_store/          # ChromaDB persistent store (auto-generated)
├── requirements.txt
├── .env                   # OPENAI_API_KEY (copy từ .env.example)
└── .env.example
```

---

## 🚀 Setup

```bash
# 1. Clone / cd vào thư mục
cd lab17

# 2. Tạo venv (đã có sẵn)
python3.11 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy .env và điền API key
cp .env.example .env
# Sửa .env: OPENAI_API_KEY=sk-...
```

---

## 🧠 Kiến trúc Memory Stack

| Memory Type | Backend | Vai trò |
|-------------|---------|---------|
| **Short-term** | Sliding-window list (RAM) | Lưu 10 turn gần nhất trong session |
| **Long-term Profile** | JSON KV store (`profile_store.json`) | Tên, tuổi, dị ứng, thành phố, nghề nghiệp |
| **Episodic** | JSON append log (`episodic_log.json`) | Ghi lại task đã hoàn thành + outcome |
| **Semantic** | ChromaDB (fallback: keyword search) | FAQ / knowledge chunks, top-3 retrieval |

### LangGraph Flow

```
[User Input]
     │
     ▼
┌─────────────────┐
│ retrieve_memory │  ← pull từ 4 backends vào MemoryState
└────────┬────────┘
         │
         ▼
┌──────────────────────┐
│  generate_response   │  ← build system prompt với 4 memory sections
└──────────┬───────────┘
           │
           ▼
┌──────────────────┐
│   save_memory    │  ← update profile, log episode nếu task done
└──────────────────┘
```

### MemoryState (TypedDict)

```python
class MemoryState(TypedDict):
    messages: list
    user_profile: dict
    episodes: list[dict]
    semantic_hits: list[str]
    memory_budget: int
    user_input: str
    response: str
    save_episode: bool
```

---

## ⚙️ Chạy

### Chat interactive

```bash
source venv/bin/activate
export PYTHONPATH=src:$PYTHONPATH
python src/agent.py
```

### Chạy benchmark

```bash
source venv/bin/activate
export PYTHONPATH=src:$PYTHONPATH
python scripts/benchmark.py
# → Tạo ra BENCHMARK.md
```

---

## 🔒 Conflict Handling

Profile store dùng **last-write-wins** per key:

```
User: "Tôi dị ứng sữa bò."       → allergy = "sữa bò"
User: "À nhầm, tôi dị ứng đậu nành." → allergy = "đậu nành"  ✅
```

Audit trail được lưu trong `profile_store.json` dưới key `"history"`.

---

## 📊 Benchmark

Chạy `benchmark.py` sẽ tạo `BENCHMARK.md` với:
- 10 multi-turn conversations
- So sánh no-memory vs with-memory
- Phân loại: profile_recall, conflict_update, episodic_recall, semantic_retrieval, trim_budget
- Word count / token budget breakdown
- Reflection về privacy & limitations

---

## 🔑 Environment Variables

| Variable | Mô tả | Default |
|----------|-------|---------|
| `OPENAI_API_KEY` | OpenAI API key | (bắt buộc) |
| `OPENAI_MODEL` | Model sử dụng | `gpt-4o-mini` |
