"""
LangGraph Multi-Memory Agent — Lab #17
=======================================
State/Router + Prompt Injection
"""

from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Literal

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict

# Project root = parent of src/
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR     = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

# Ensure src/ is on path (needed when run via scripts/)
if str(Path(__file__).parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent))

from memory_backends import EpisodicMemory, LongTermProfile, SemanticMemory, ShortTermMemory  # noqa: E402

# Load .env from project root
load_dotenv(PROJECT_ROOT / ".env")

# ---------------------------------------------------------------------------
# MemoryState — rubric-required shape
# ---------------------------------------------------------------------------

class MemoryState(TypedDict):
    messages: list                  # conversation messages (HumanMessage / AIMessage)
    user_profile: dict              # long-term profile facts
    episodes: list[dict]            # relevant episodic memories
    semantic_hits: list[str]        # relevant knowledge chunks
    memory_budget: int              # token budget remaining for memory section
    user_input: str                 # latest user turn
    response: str                   # latest agent response
    save_episode: bool              # flag: should we save an episode after this turn?


# ---------------------------------------------------------------------------
# Global memory instances (shared across graph invocations)
# ---------------------------------------------------------------------------

short_term  = ShortTermMemory(max_turns=10)
long_term   = LongTermProfile(path=str(DATA_DIR / "profile_store.json"))
episodic    = EpisodicMemory(path=str(DATA_DIR / "episodic_log.json"))
semantic    = SemanticMemory(
    persist_dir=str(PROJECT_ROOT / "chroma_store"),
)

# Seed some FAQ knowledge into semantic store
_FAQ_SEEDED = False
def seed_semantic_knowledge() -> None:
    global _FAQ_SEEDED
    if _FAQ_SEEDED:
        return
    faq_docs = [
        ("docker-service", "Khi debug lỗi Docker, dùng service name thay vì localhost để container giao tiếp nội bộ."),
        ("venv-setup", "Tạo virtual environment bằng python3 -m venv venv, sau đó activate bằng source venv/bin/activate."),
        ("langgraph-state", "LangGraph state được truyền giữa các node như một TypedDict, cập nhật qua return dict."),
        ("memory-types", "4 loại memory agent: short-term (buffer), long-term (profile), episodic (log), semantic (vector search)."),
        ("conflict-resolution", "Khi user cập nhật profile fact, luôn ưu tiên giá trị mới nhất (last-write-wins)."),
        ("token-budget", "Context window management: ưu tiên system prompt > profile > semantic > episodic > conversation buffer."),
        ("pii-risk", "Profile store chứa PII như tên, dị ứng, sở thích. Cần TTL và deletion API để bảo vệ quyền riêng tư."),
        ("chroma-usage", "ChromaDB là vector database in-process, phù hợp cho semantic search trong các agent nhỏ."),
        ("allergy-protocol", "Khi user khai báo dị ứng thực phẩm, lưu vào profile và ưu tiên fact mới nhất nếu có conflict."),
        ("benchmark-design", "Benchmark agent: so sánh no-memory vs with-memory trên các kịch bản: profile recall, conflict, episodic, semantic."),
    ]
    for doc_id, text in faq_docs:
        semantic.add_document(doc_id, text)
    _FAQ_SEEDED = True


# ---------------------------------------------------------------------------
# LLM
# ---------------------------------------------------------------------------

def get_llm() -> ChatOpenAI:
    api_key = os.getenv("OPENAI_API_KEY", "")
    model   = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    return ChatOpenAI(model=model, api_key=api_key, temperature=0.3)


# ---------------------------------------------------------------------------
# Profile extraction helpers
# ---------------------------------------------------------------------------

PROFILE_PATTERNS = [
    # name
    (r"(?:tên|tên tôi là|tôi tên|my name is|I am|I'm)\s+([A-ZÀ-Ỹa-zà-ỹ][A-ZÀ-Ỹa-zà-ỹ\s]{1,30})", "name"),
    # age
    (r"(?:tôi|i am|i'm)?\s*(\d{1,3})\s*(?:tuổi|years? old)", "age"),
    # allergy — multi-pattern, priority: latest match wins
    (r"(?:dị ứng|allerg(?:ic to|y to?)?)\s+([^\.\,\!\?]{3,50})", "allergy"),
    # city
    (r"(?:ở|sống ở|tôi ở|live in|from)\s+([A-ZÀ-Ỹa-zà-ỹ][a-zà-ỹA-ZÀ-Ỹ\s]{1,30})", "city"),
    # job
    (r"(?:làm|là|work as|i am a|i'm a)\s+(developer|engineer|designer|teacher|student|bác sĩ|lập trình viên|kỹ sư|giáo viên|sinh viên)", "job"),
]

def extract_profile_facts(text: str) -> dict[str, str]:
    """Extract profile facts from user text via regex."""
    facts: dict[str, str] = {}
    for pattern, key in PROFILE_PATTERNS:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            facts[key] = m.group(1).strip().rstrip(".")
    return facts


# ---------------------------------------------------------------------------
# Token budget helpers (word-count approximation, rubric allows this)
# ---------------------------------------------------------------------------

MEMORY_BUDGET_TOKENS = 800  # reserve for memory injection in context

def word_count(text: str) -> int:
    return len(text.split())

def trim_to_budget(items: list[str], budget_words: int) -> list[str]:
    """Return items that fit within budget_words total."""
    used = 0
    result = []
    for item in items:
        wc = word_count(item)
        if used + wc > budget_words:
            break
        result.append(item)
        used += wc
    return result


# ---------------------------------------------------------------------------
# Node 1: retrieve_memory
# ---------------------------------------------------------------------------

def retrieve_memory(state: MemoryState) -> dict:
    """Pull relevant memories from all 4 backends into state."""
    user_input = state["user_input"]

    # Long-term profile
    profile = long_term.get_all()

    # Episodic: search by current user input
    episodes = episodic.search(user_input, top_k=3)
    if not episodes:
        episodes = episodic.get_recent(n=2)

    # Semantic: search by current user input
    semantic_hits = semantic.search(user_input, top_k=3)

    # Token budget: profile + episodes + semantic should fit MEMORY_BUDGET_TOKENS
    profile_text   = " ".join(f"{k}={v}" for k, v in profile.items())
    episode_texts  = [f"{ep['task']}: {ep['outcome']}" for ep in episodes]
    all_texts      = [profile_text] + episode_texts + semantic_hits
    trimmed        = trim_to_budget(all_texts, MEMORY_BUDGET_TOKENS)

    memory_budget = MEMORY_BUDGET_TOKENS - sum(word_count(t) for t in trimmed)

    return {
        "user_profile":   profile,
        "episodes":       episodes,
        "semantic_hits":  semantic_hits,
        "memory_budget":  memory_budget,
    }


# ---------------------------------------------------------------------------
# Node 2: generate_response
# ---------------------------------------------------------------------------

def build_system_prompt(state: MemoryState) -> str:
    """Inject all memory sections into system prompt."""
    parts = ["Bạn là trợ lý AI thông minh với khả năng ghi nhớ lâu dài.\n"]

    # --- Profile section ---
    profile = state["user_profile"]
    if profile:
        parts.append("## Thông tin người dùng (Long-term Profile)")
        for k, v in profile.items():
            parts.append(f"- {k}: {v}")
        parts.append("")

    # --- Episodic section ---
    episodes = state["episodes"]
    if episodes:
        parts.append("## Ký ức sự kiện trước (Episodic Memory)")
        for ep in episodes:
            parts.append(f"- [{ep.get('date','?')}] Task: {ep['task']} → Outcome: {ep['outcome']}")
        parts.append("")

    # --- Semantic section ---
    hits = state["semantic_hits"]
    if hits:
        parts.append("## Kiến thức liên quan (Semantic Memory)")
        for chunk in hits:
            parts.append(f"- {chunk}")
        parts.append("")

    # --- Recent conversation section ---
    recent = short_term.get_recent(n_turns=5)
    if recent:
        parts.append("## Cuộc trò chuyện gần đây (Short-term Memory)")
        for msg in recent[-6:]:   # last 3 pairs
            role = "User" if msg["role"] == "user" else "Assistant"
            parts.append(f"{role}: {msg['content']}")
        parts.append("")

    parts.append(f"[Remaining memory budget: ~{state['memory_budget']} words]")
    parts.append("\nHãy trả lời bằng tiếng Việt, ngắn gọn và chính xác.")

    return "\n".join(parts)


def generate_response(state: MemoryState) -> dict:
    """Call LLM with memory-injected prompt, update short-term buffer."""
    system_prompt = build_system_prompt(state)
    user_input    = state["user_input"]

    llm = get_llm()
    lc_messages = [SystemMessage(content=system_prompt),
                   HumanMessage(content=user_input)]

    ai_msg   = llm.invoke(lc_messages)
    response = ai_msg.content

    # Update short-term
    short_term.add("user",      user_input)
    short_term.add("assistant", response)

    return {"response": response, "messages": state["messages"] + [
        HumanMessage(content=user_input),
        AIMessage(content=response)
    ]}


# ---------------------------------------------------------------------------
# Node 3: save_memory
# ---------------------------------------------------------------------------

def save_memory(state: MemoryState) -> dict:
    """
    Extract profile facts from user input, apply conflict-safe update.
    Save episodic memory when task completion is detected.
    """
    user_input = state["user_input"]
    response   = state["response"]

    # --- Profile update (conflict resolution: new value wins) ---
    new_facts = extract_profile_facts(user_input)
    for key, value in new_facts.items():
        long_term.update(key, value, source="user_input")

    # --- Episodic save: detect task completion keywords ---
    task_done_keywords = [
        "xong", "done", "hoàn thành", "solved", "fixed", "worked",
        "cảm ơn", "thanks", "thank you", "thành công", "success"
    ]
    combined_text = (user_input + " " + response).lower()
    if any(kw in combined_text for kw in task_done_keywords):
        task_summary = user_input[:80]
        outcome      = response[:100] if response else "Completed"
        episodic.add_episode(
            task    = task_summary,
            outcome = outcome,
            context = f"Profile snapshot: {long_term.get_all()}"
        )

    return {"user_profile": long_term.get_all()}


# ---------------------------------------------------------------------------
# Router — decide whether to save memory or go to END
# ---------------------------------------------------------------------------

def should_save(state: MemoryState) -> Literal["save_memory", "end"]:
    return "save_memory"   # always save after response


# ---------------------------------------------------------------------------
# Build LangGraph
# ---------------------------------------------------------------------------

def build_graph() -> Any:
    seed_semantic_knowledge()

    builder = StateGraph(MemoryState)

    builder.add_node("retrieve_memory",  retrieve_memory)
    builder.add_node("generate_response", generate_response)
    builder.add_node("save_memory",       save_memory)

    builder.set_entry_point("retrieve_memory")
    builder.add_edge("retrieve_memory",   "generate_response")
    builder.add_conditional_edges(
        "generate_response",
        should_save,
        {"save_memory": "save_memory", "end": END}
    )
    builder.add_edge("save_memory", END)

    return builder.compile()


# ---------------------------------------------------------------------------
# Public chat interface
# ---------------------------------------------------------------------------

_graph = None

def chat(user_input: str) -> str:
    global _graph
    if _graph is None:
        _graph = build_graph()

    initial_state: MemoryState = {
        "messages":     [],
        "user_profile": long_term.get_all(),
        "episodes":     [],
        "semantic_hits": [],
        "memory_budget": MEMORY_BUDGET_TOKENS,
        "user_input":   user_input,
        "response":     "",
        "save_episode": False,
    }

    result = _graph.invoke(initial_state)
    return result["response"]


def chat_no_memory(user_input: str) -> str:
    """Baseline: call LLM without any memory injection."""
    llm = get_llm()
    msg = llm.invoke([
        SystemMessage(content="Bạn là trợ lý AI. Hãy trả lời bằng tiếng Việt."),
        HumanMessage(content=user_input)
    ])
    return msg.content


if __name__ == "__main__":
    from rich.console import Console
    from rich.panel import Panel

    console = Console()
    console.print(Panel("[bold green]Multi-Memory Agent — Lab #17[/bold green]\nGõ 'exit' để thoát."))

    while True:
        try:
            user_in = input("\n[You]: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if user_in.lower() in ("exit", "quit", "thoát"):
            break
        if not user_in:
            continue

        response = chat(user_in)
        console.print(f"\n[bold cyan][Agent]:[/bold cyan] {response}")
