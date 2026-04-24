"""
Benchmark Script — Lab #17
===========================
Runs 10 multi-turn conversations comparing no-memory vs with-memory agent.
Outputs results to BENCHMARK.md.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path

from rich.console import Console
from rich.progress import track

from agent import chat, chat_no_memory, episodic, long_term, short_term, semantic, seed_semantic_knowledge

console = Console()


# ---------------------------------------------------------------------------
# Benchmark scenario definitions
# ---------------------------------------------------------------------------

@dataclass
class Turn:
    role: str    # "user" | "info"
    content: str

@dataclass
class Scenario:
    id: int
    name: str
    category: str   # profile_recall | conflict_update | episodic_recall | semantic_retrieval | trim_budget
    turns: list[Turn]
    recall_turn: int        # index of the turn that tests recall (0-indexed)
    expected_keyword: str   # keyword expected in with-memory response


SCENARIOS: list[Scenario] = [
    # 1. Profile recall — name
    Scenario(
        id=1, name="Recall user name after 6 turns",
        category="profile_recall",
        turns=[
            Turn("user", "Xin chào! Tôi tên Linh."),
            Turn("user", "Tôi đang học lập trình Python."),
            Turn("user", "Bạn có thể giải thích list comprehension không?"),
            Turn("user", "Cảm ơn! Tiếp tục nào."),
            Turn("user", "Tôi muốn học về decorators."),
            Turn("user", "Bạn nhớ tên tôi không?"),   # ← recall turn
        ],
        recall_turn=5, expected_keyword="linh"
    ),

    # 2. Allergy conflict update
    Scenario(
        id=2, name="Allergy conflict update (sữa bò → đậu nành)",
        category="conflict_update",
        turns=[
            Turn("user", "Tôi dị ứng sữa bò."),
            Turn("user", "Hmm, tôi nhớ nhầm. À nhầm, tôi dị ứng đậu nành chứ không phải sữa bò."),
            Turn("user", "Tôi dị ứng gì vậy bạn?"),  # ← recall turn
        ],
        recall_turn=2, expected_keyword="đậu nành"
    ),

    # 3. Episodic recall — previous debug lesson
    Scenario(
        id=3, name="Recall previous debug lesson (Docker service name)",
        category="episodic_recall",
        turns=[
            Turn("user", "Tôi vừa fix lỗi Docker: dùng service name thay vì localhost. Xong rồi!"),
            Turn("user", "Tốt. Cho tôi hỏi về Python threading."),
            Turn("user", "Cảm ơn. Còn lỗi kết nối Docker thì sao?"),  # ← recall
        ],
        recall_turn=2, expected_keyword="service"
    ),

    # 4. Semantic retrieval — FAQ chunk
    Scenario(
        id=4, name="Semantic retrieval — FAQ on Docker debug",
        category="semantic_retrieval",
        turns=[
            Turn("user", "Làm sao debug lỗi kết nối giữa các container Docker?"),  # ← recall
        ],
        recall_turn=0, expected_keyword="service name"
    ),

    # 5. Token budget / trim test
    Scenario(
        id=5, name="Context window management — trim older turns",
        category="trim_budget",
        turns=[
            Turn("user", "Turn 1: Tôi tên An, làm kỹ sư phần mềm."),
            Turn("user", "Turn 2: Tôi thích Python và machine learning."),
            Turn("user", "Turn 3: Bạn có thể giới thiệu về LangChain không?"),
            Turn("user", "Turn 4: Tôi muốn biết thêm về vector database."),
            Turn("user", "Turn 5: Chromadb có ưu điểm gì?"),
            Turn("user", "Turn 6: So sánh Chroma và FAISS đi."),
            Turn("user", "Turn 7: Tôi đang xây agent hỏi đáp."),
            Turn("user", "Turn 8: Tôi muốn thêm bộ nhớ dài hạn."),
            Turn("user", "Turn 9: Còn bộ nhớ ngắn hạn thì sao?"),
            Turn("user", "Turn 10: Bạn có biết tên và nghề nghiệp của tôi không?"),  # ← recall
        ],
        recall_turn=9, expected_keyword="an"
    ),

    # 6. Profile recall — age
    Scenario(
        id=6, name="Recall user age",
        category="profile_recall",
        turns=[
            Turn("user", "Tôi 25 tuổi và đang học AI."),
            Turn("user", "Bạn nhớ tôi bao nhiêu tuổi không?"),  # ← recall
        ],
        recall_turn=1, expected_keyword="25"
    ),

    # 7. Episodic recall — learning outcome
    Scenario(
        id=7, name="Recall learning outcome from previous session",
        category="episodic_recall",
        turns=[
            Turn("user", "Tôi vừa học xong bài về transformer architecture. Thành công!"),
            Turn("user", "Bạn nhớ tôi học gì gần đây không?"),  # ← recall
        ],
        recall_turn=1, expected_keyword="transformer"
    ),

    # 8. Semantic retrieval — venv setup
    Scenario(
        id=8, name="Semantic retrieval — venv setup guide",
        category="semantic_retrieval",
        turns=[
            Turn("user", "Cách tạo môi trường ảo Python là gì?"),  # ← recall
        ],
        recall_turn=0, expected_keyword="venv"
    ),

    # 9. Profile recall — city + job combo
    Scenario(
        id=9, name="Recall city and job",
        category="profile_recall",
        turns=[
            Turn("user", "Tôi sống ở Hà Nội và làm developer."),
            Turn("user", "Bạn biết gì về tôi không?"),  # ← recall
        ],
        recall_turn=1, expected_keyword="hà nội"
    ),

    # 10. Conflict update — name correction
    Scenario(
        id=10, name="Name conflict update (Minh → Tuấn)",
        category="conflict_update",
        turns=[
            Turn("user", "Tôi tên Minh."),
            Turn("user", "Thực ra tên tôi là Tuấn, không phải Minh."),
            Turn("user", "Bạn nhớ tên tôi là gì?"),  # ← recall
        ],
        recall_turn=2, expected_keyword="tuấn"
    ),
]


# ---------------------------------------------------------------------------
# Result storage
# ---------------------------------------------------------------------------

@dataclass
class TurnResult:
    turn_index: int
    user_input: str
    no_memory_response: str
    with_memory_response: str


@dataclass
class ScenarioResult:
    scenario: Scenario
    turn_results: list[TurnResult] = field(default_factory=list)
    pass_no_memory: bool = False
    pass_with_memory: bool = False
    no_memory_tokens: int = 0
    with_memory_tokens: int = 0

    @property
    def pass_symbol(self) -> str:
        return "✅" if self.pass_with_memory else "❌"

    @property
    def no_mem_pass_symbol(self) -> str:
        return "✅" if self.pass_no_memory else "❌"


# ---------------------------------------------------------------------------
# Run benchmark
# ---------------------------------------------------------------------------

def word_count(text: str) -> int:
    return len(text.split())


def run_benchmark() -> list[ScenarioResult]:
    results: list[ScenarioResult] = []

    for scenario in track(SCENARIOS, description="Running benchmark scenarios..."):
        console.print(f"\n[bold yellow]▶ Scenario {scenario.id}: {scenario.name}[/bold yellow]")

        # Reset agent memory between scenarios for clean test
        short_term.clear()
        # Note: long_term and episodic persist across scenarios intentionally
        # (real-world agents accumulate memory)

        sr = ScenarioResult(scenario=scenario)
        no_mem_responses: list[str] = []
        with_mem_responses: list[str] = []

        for i, turn in enumerate(scenario.turns):
            if turn.role == "info":
                continue

            user_input = turn.content
            console.print(f"  Turn {i+1}: [dim]{user_input[:60]}...[/dim]" if len(user_input) > 60 else f"  Turn {i+1}: [dim]{user_input}[/dim]")

            # No-memory agent
            nm_response = chat_no_memory(user_input)
            no_mem_responses.append(nm_response)

            # With-memory agent
            wm_response = chat(user_input)
            with_mem_responses.append(wm_response)

            sr.turn_results.append(TurnResult(
                turn_index          = i,
                user_input          = user_input,
                no_memory_response  = nm_response,
                with_memory_response= wm_response,
            ))

            sr.no_memory_tokens  += word_count(nm_response)
            sr.with_memory_tokens+= word_count(wm_response)

        # Evaluate recall turn
        if sr.turn_results:
            recall_idx = scenario.recall_turn
            if recall_idx < len(sr.turn_results):
                recall_result = sr.turn_results[recall_idx]
                kw = scenario.expected_keyword.lower()
                sr.pass_no_memory  = kw in recall_result.no_memory_response.lower()
                sr.pass_with_memory= kw in recall_result.with_memory_response.lower()

        results.append(sr)
        status = sr.pass_symbol
        console.print(f"  → With-memory: {status} | No-memory: {sr.no_mem_pass_symbol}")

    return results


# ---------------------------------------------------------------------------
# Generate BENCHMARK.md
# ---------------------------------------------------------------------------

BENCHMARK_MD_TEMPLATE = """\
# BENCHMARK — Lab #17: Multi-Memory Agent

**Mô tả:** So sánh agent có memory và không có memory trên 10 multi-turn conversations.  
**Ngày chạy:** {date}  
**Model:** {model}  
**Tổng số conversations:** 10  

---

## Summary Table

| # | Scenario | Category | No-memory | With-memory | Pass? |
|---|----------|----------|-----------|-------------|-------|
{summary_rows}

**Pass rate (with-memory):** {pass_rate:.0%}  
**Pass rate (no-memory):** {no_mem_pass_rate:.0%}  

---

## Detailed Results

{detail_sections}

---

## Analysis

### Memory Hit Rate
- Scenarios where with-memory agent passed: **{pass_count}/{total}**
- Scenarios where no-memory agent passed: **{no_mem_pass}/{total}** (expected low for context-dependent queries)

### Token / Word Budget Breakdown

| # | No-memory words | With-memory words | Delta |
|---|-----------------|-------------------|-------|
{token_rows}

**Average word count per scenario — No-memory:** {avg_no_mem:.1f}  
**Average word count per scenario — With-memory:** {avg_with_mem:.1f}  

### Context Utilization
- Short-term memory: sliding window (last 10 turns)
- Long-term profile: JSON KV store, conflict-safe (last-write-wins)
- Episodic log: JSON append log, keyword search retrieval
- Semantic store: ChromaDB / keyword fallback, top-3 chunks injected

---

## Reflection — Privacy & Limitations

### 1. Memory nào giúp agent nhất?
**Long-term profile** giúp nhất — lưu thông tin người dùng (tên, dị ứng, nghề nghiệp) và được inject vào mọi prompt, đảm bảo agent luôn biết context cơ bản.

### 2. Memory nào rủi ro nhất nếu retrieve sai?
**Episodic memory** rủi ro nhất — nếu retrieve nhầm episode (ví dụ: lẫn lộn giữa hai user), agent có thể đưa ra lời khuyên sai dựa trên bối cảnh không đúng. **Long-term profile** cũng rủi ro nếu fact bị ghi đè không đúng lúc.

### 3. PII / Privacy risks
- Profile store lưu **PII nhạy cảm**: tên, tuổi, dị ứng, thành phố. Đây là thông tin y tế có thể gây hại nếu bị lộ.
- Episodic log lưu context của từng cuộc hội thoại — tiềm ẩn rủi ro nếu nhiều user dùng chung instance.
- **Biện pháp cần thiết:**
  - TTL (time-to-live) cho từng profile key
  - Deletion API (right-to-be-forgotten — GDPR)
  - Consent flow khi lưu thông tin y tế
  - Mã hóa at-rest cho profile_store.json

### 4. Nếu user yêu cầu xóa memory, xóa ở backend nào?
1. **Long-term profile**: `LongTermProfile.delete(key)` — xóa ngay, ghi file
2. **Episodic log**: filter và rewrite `episodic_log.json` bỏ episodes của user đó
3. **Semantic store**: `collection.delete(ids=[doc_id])` trong Chroma
4. **Short-term**: `short_term.clear()` — đã in-memory, tự mất khi restart

### 5. Limitations kỹ thuật hiện tại
1. **No user isolation** — tất cả profile/episodic dùng chung một file → không dùng được multi-user.
2. **Keyword-based episodic search** — recall kém với paraphrase hoặc tiếng Việt có diacritics.
3. **Regex profile extraction** — dễ miss hoặc overextract; cần LLM-based extraction cho production.
4. **No TTL** — profile facts không tự expire, có thể stale sau nhiều tháng.
5. **Single-node Chroma** — không scale horizontally; cần managed vector DB cho production.
6. **Word-count token approximation** — không chính xác cho tokenizer (tiktoken) thật, có thể over/under-budget.
"""


def generate_benchmark_md(results: list[ScenarioResult]) -> str:
    import datetime
    import os

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    date  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    summary_rows = []
    for sr in results:
        summary_rows.append(
            f"| {sr.scenario.id} | {sr.scenario.name} | {sr.scenario.category} "
            f"| {sr.no_mem_pass_symbol} | {sr.pass_symbol} | {sr.pass_symbol} |"
        )

    detail_sections = []
    for sr in results:
        lines = [f"### Scenario {sr.scenario.id}: {sr.scenario.name}",
                 f"**Category:** {sr.scenario.category}  ",
                 f"**Expected keyword:** `{sr.scenario.expected_keyword}`  ",
                 ""]
        for tr in sr.turn_results:
            lines.append(f"**Turn {tr.turn_index + 1}:** {tr.user_input}")
            lines.append(f"- *No-memory:* {tr.no_memory_response[:200]}{'...' if len(tr.no_memory_response)>200 else ''}")
            lines.append(f"- *With-memory:* {tr.with_memory_response[:200]}{'...' if len(tr.with_memory_response)>200 else ''}")
            lines.append("")
        lines.append(f"**Result:** No-memory {sr.no_mem_pass_symbol} | With-memory {sr.pass_symbol}")
        lines.append("")
        detail_sections.append("\n".join(lines))

    token_rows = []
    for sr in results:
        delta = sr.with_memory_tokens - sr.no_memory_tokens
        delta_str = f"+{delta}" if delta >= 0 else str(delta)
        token_rows.append(f"| {sr.scenario.id} | {sr.no_memory_tokens} | {sr.with_memory_tokens} | {delta_str} |")

    pass_count    = sum(1 for sr in results if sr.pass_with_memory)
    no_mem_pass   = sum(1 for sr in results if sr.pass_no_memory)
    total         = len(results)
    pass_rate     = pass_count / total if total else 0
    no_mem_rate   = no_mem_pass / total if total else 0
    avg_no_mem    = sum(sr.no_memory_tokens for sr in results) / total if total else 0
    avg_with_mem  = sum(sr.with_memory_tokens for sr in results) / total if total else 0

    return BENCHMARK_MD_TEMPLATE.format(
        date             = date,
        model            = model,
        summary_rows     = "\n".join(summary_rows),
        pass_rate        = pass_rate,
        no_mem_pass_rate = no_mem_rate,
        detail_sections  = "\n---\n".join(detail_sections),
        pass_count       = pass_count,
        no_mem_pass      = no_mem_pass,
        total            = total,
        token_rows       = "\n".join(token_rows),
        avg_no_mem       = avg_no_mem,
        avg_with_mem     = avg_with_mem,
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    console.print("[bold green]╔══════════════════════════════════════╗[/bold green]")
    console.print("[bold green]║  Multi-Memory Agent Benchmark        ║[/bold green]")
    console.print("[bold green]╚══════════════════════════════════════╝[/bold green]\n")

    seed_semantic_knowledge()
    results = run_benchmark()

    md_content = generate_benchmark_md(results)
    Path("BENCHMARK.md").write_text(md_content, encoding="utf-8")

    console.print("\n[bold green]✅ BENCHMARK.md written successfully![/bold green]")

    pass_count = sum(1 for sr in results if sr.pass_with_memory)
    console.print(f"\n[bold]Final score: {pass_count}/{len(results)} scenarios passed with memory.[/bold]")
    console.print(f"No-memory baseline: {sum(1 for sr in results if sr.pass_no_memory)}/{len(results)}")
