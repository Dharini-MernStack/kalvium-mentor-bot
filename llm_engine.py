"""LLM engine — Multi-provider support: Gemini, Grok (xAI), OpenAI."""

from config import GEMINI_MODEL

# Module-level clients
_gemini_client = None
_openai_client = None
_active_provider = None  # "gemini", "grok", or "openai"

SYSTEM_PROMPT = """You are **Kalvium Mentor Assistant** — an expert instructional design advisor, subject-matter expert, and L&D strategist for BTech CSE courses at Kalvium.

You help mentors understand, improve, and deliver course content. You also help the L&D team create Subject Readiness Day (SRD) bootcamp playbooks. You have access to the course's Low-Level Design (LLD) documents as context.

**Your capabilities:**
1. **Module Insights** — Summarise modules: total LUs, learning paths, coverage gaps, effort distribution.
2. **LU Deep-Dive** — For any Learning Unit, explain objectives, assessment, author notes, and engagement tips in mentor-friendly language. Do NOT reproduce session flows — those are confidential design assets.
3. **Making LUs Interesting** — Suggest pedagogy improvements: real-world hooks, analogies, gamification, active-learning techniques, Socratic questioning, pair-programming prompts.
4. **Simplification** — Rewrite dense technical content into mentor-ready talking points and student-facing explanations.
5. **Cross-LU Bridges** — Identify how LUs connect, prerequisites, and knowledge gaps.
6. **Assessment Guidance** — Evaluate assessment quality, suggest rubrics, and identify missing evaluation criteria.
7. **Subject-Matter Q&A** — Answer conceptual/technical questions about topics covered in the course using LLD context + your own expertise.
8. **SRD Playbook Generation** — Create Subject Readiness Day bootcamp playbooks for mentors. Generate breadth sweep scripts, deep dive topic guides, assessment banks, and facilitator runsheets based on course LLD data.

**Rules:**
- Use the LLD context to ground your answers — reference specific LU numbers, module names, and course structure when relevant.
- For conceptual/technical questions, DO NOT just say the LLD doesn't contain the answer. Use the LLD to identify relevant LUs, then provide a complete expert answer.
- NEVER reproduce or paraphrase session flows from the LLD. Session flows are confidential design documents meant only for content authors. Instead, focus on learning objectives, outcomes, assessment details, and author notes.
- When generating SRD content, structure it as actionable facilitator materials — not academic documents.
- Use tables, bullet points, and structured formatting for clarity.
- Keep the tone professional yet approachable — you're a peer advisor and expert, not a critic.
- For BTech CSE level — balance theory with practical application.
"""


def configure_gemini(api_key: str):
    """Configure the Gemini API with the provided key."""
    global _gemini_client, _active_provider
    from google import genai
    _gemini_client = genai.Client(api_key=api_key)
    _active_provider = "gemini"


def configure_grok(api_key: str):
    """Configure xAI Grok API (OpenAI-compatible)."""
    global _openai_client, _active_provider
    from openai import OpenAI
    _openai_client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    _active_provider = "grok"


def configure_openai(api_key: str):
    """Configure OpenAI API."""
    global _openai_client, _active_provider
    from openai import OpenAI
    _openai_client = OpenAI(api_key=api_key)
    _active_provider = "openai"


def get_active_provider():
    return _active_provider


def _call_llm(prompt: str, chat_history: list = None) -> str:
    """Unified LLM call — routes to active provider."""
    if _active_provider == "gemini":
        return _call_gemini(prompt, chat_history)
    elif _active_provider in ("grok", "openai"):
        return _call_openai_compatible(prompt, chat_history)
    else:
        return "❌ No LLM provider configured. Please enter an API key in the sidebar."


def _call_gemini(prompt: str, chat_history: list = None) -> str:
    from google.genai import types
    contents = []
    if chat_history:
        for msg in chat_history[-10:]:
            role = msg.get("role", "user")
            if role == "assistant":
                role = "model"
            text = msg.get("content") or (msg.get("parts", [""])[0] if msg.get("parts") else "")
            contents.append(types.Content(role=role, parts=[types.Part.from_text(text=text)]))
    contents.append(types.Content(role="user", parts=[types.Part.from_text(text=prompt)]))
    try:
        response = _gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        )
        return response.text
    except Exception as e:
        return f"❌ Error from Gemini API: {str(e)}"


def _call_openai_compatible(prompt: str, chat_history: list = None) -> str:
    model = "grok-3-mini" if _active_provider == "grok" else "gpt-4o-mini"
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if chat_history:
        for msg in chat_history[-10:]:
            role = msg.get("role", "user")
            text = msg.get("content", "")
            messages.append({"role": role, "content": text})
    messages.append({"role": "user", "content": prompt})
    try:
        response = _openai_client.chat.completions.create(model=model, messages=messages)
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error from {'Grok' if _active_provider == 'grok' else 'OpenAI'} API: {str(e)}"


# ─── Public API ───

def get_gemini_response(query: str, context_chunks: list[dict], chat_history: list = None) -> str:
    """Generate a response using active LLM with RAG context."""
    context_parts = []
    for i, chunk in enumerate(context_chunks, 1):
        meta = chunk["metadata"]
        context_parts.append(
            f"--- Context Chunk {i} (Module: {meta.get('module', 'N/A')}, "
            f"LU: {meta.get('lu_seq', 'N/A')} - {meta.get('lu_name', 'N/A')}) ---\n"
            f"{chunk['text']}\n"
        )
    context_str = "\n".join(context_parts)

    prompt = f"""You have access to the following LLD (Low-Level Design) course data as context.

=== COURSE LLD CONTEXT ===
{context_str}
=== END CONTEXT ===

**Mentor's Question:** {query}

**Instructions:**
- If the question is about course structure, LUs, or modules — answer primarily from the LLD context.
- If the question is conceptual/technical — mention relevant LUs, then provide a thorough expert answer.
- NEVER reproduce session flows. Focus on objectives, outcomes, assessments, and author notes.
- Always provide a detailed, structured, and actionable response."""

    return _call_llm(prompt, chat_history)


def generate_module_insights(module_name: str, lu_data: list[dict]) -> str:
    """Generate comprehensive insights for an entire module."""
    combined = "\n\n".join([chunk["text"] for chunk in lu_data])

    prompt = f"""Analyse the following module from the course LLD and provide comprehensive mentor insights.

=== MODULE: {module_name} ===
{combined}
=== END MODULE DATA ===

Provide the following analysis in a well-structured format:

## 📊 Module Overview
- Total LUs, key topics covered, overall difficulty progression

## 🎯 Learning Objectives & Outcomes Summary
- Map objectives to outcomes across LUs. Identify gaps or overlaps.

## 🔗 LU Flow & Bridges
- How LUs connect, cross-module bridges, prerequisite chain

## 💡 Engagement Opportunities
- Which LUs could be more interactive, specific suggestions

## 📝 Assessment Analysis
- Types used, alignment with outcomes, improvement suggestions

## ⚠️ Mentor Watch-outs
- Common misconceptions from author notes, tricky concepts, time management tips

## 📈 Effort Distribution
- Level of effort across LUs, completion status overview
"""
    return _call_llm(prompt)


def generate_lu_breakdown(lu_text: str, lu_name: str) -> str:
    """Generate a detailed mentor-friendly breakdown of a single LU (WITHOUT session flow)."""
    prompt = f"""Break down this Learning Unit for a mentor who needs to deliver it in a 45-minute session.

=== LU: {lu_name} ===
{lu_text}
=== END LU DATA ===

Provide:

## 🎯 What This LU Is About (2-line summary)

## 📋 Mentor Prep Checklist
- What to set up before the session
- Key concepts to review
- Common student questions to prepare for

## 🎮 Making It Interesting
- 3 specific techniques to make this LU engaging
- Real-world analogies students will relate to
- Quick interactive activities (under 5 mins each)

## ⚡ Key Takeaways for Students
- Top 3 things students MUST leave knowing
- One-liner summary they can write in their notes

## 🚨 Watch-outs
- Misconceptions from author notes
- Where students typically get stuck
- How to handle "I don't get it" moments

IMPORTANT: Do NOT reproduce or paraphrase the session flow. Focus only on objectives, outcomes, assessments, and mentor preparation guidance.
"""
    return _call_llm(prompt)


def generate_srd_playbook(course_name: str, all_chunks: list[dict], srd_type: str = "full") -> str:
    """Generate an SRD (Subject Readiness Day) bootcamp playbook."""
    combined = "\n\n".join([chunk["text"] for chunk in all_chunks[:30]])  # Cap to avoid token overflow

    if srd_type == "breadth_sweep":
        prompt = f"""Using the following course LLD data, create a **Breadth Sweep Script** for a Subject Readiness Day bootcamp.

=== COURSE: {course_name} ===
{combined}
=== END COURSE DATA ===

Create a 90-minute breadth sweep script that covers the ENTIRE course at a high level:

## ⏱️ Breadth Sweep Script (90 minutes)

For each module, provide:
- **Time block** (e.g., 0-15 min)
- **Module name and key topics** covered
- **1-2 sentence summary**: what this covers and why it matters
- **Key bridge**: how this connects to the next module

The goal is: mentors see the ENTIRE terrain of the subject in 90 minutes. No deep dives — just the map.
End with a 5-min connections recap showing how all modules fit together.

IMPORTANT: Do NOT reproduce session flows. Use learning objectives and outcomes to describe what each module covers."""

    elif srd_type == "deep_dive":
        prompt = f"""Using the following course LLD data, identify the **Deep Dive Topics** for a Subject Readiness Day bootcamp.

=== COURSE: {course_name} ===
{combined}
=== END COURSE DATA ===

Identify the 4-6 HARDEST / most conceptually tricky topics across the entire course. For each topic:

## 🔬 Deep Dive Topics

For each topic provide:
### Topic: [Name]
- **Which LU(s)**: Reference specific LU numbers
- **Why it's hard**: Common student misconceptions and confusion points (use author notes if available)
- **The 'aha moment'**: What makes this concept click
- **How to explain it**: A clear analogy or worked example
- **5-minute teach-back prompt**: A question a mentor could use to explain this to verify understanding

Focus on topics where author notes mention misconceptions or where the content is conceptually dense."""

    elif srd_type == "assessment":
        prompt = f"""Using the following course LLD data, create a **Readiness Assessment Bank** for a Subject Readiness Day bootcamp.

=== COURSE: {course_name} ===
{combined}
=== END COURSE DATA ===

Create an assessment that is 1 BAR ABOVE student level:

## 📝 SRD Readiness Assessment

### Part A: Objective (45 minutes)
Generate 15 MCQs covering all modules. Each MCQ should:
- Test conceptual understanding, not rote memory
- Be harder than what students would face
- Include 4 options with one clearly correct answer
- Cover the breadth of the course

### Part B: Subjective (15 minutes)
Provide 3 teach-back prompts:
- "Explain [concept] to a student who has zero context, in under 5 minutes"
- Each prompt should target a different module

### Scoring Rubric
- 🟢 GREEN (Ready): ≥ 80% MCQ + clear, accurate teach-back
- 🟡 AMBER (Conditional): 60-79% MCQ or partially clear teach-back
- 🔴 RED (Not Ready): < 60% MCQ or inaccurate teach-back

Base all questions on the actual course content from the LLD."""

    else:  # full playbook
        prompt = f"""Using the following course LLD data, create a complete **Subject Readiness Day (SRD) Playbook** for mentors.

=== COURSE: {course_name} ===
{combined}
=== END COURSE DATA ===

Generate a full SRD playbook with these sections:

## 📊 Section 1: Course Landscape
- Total modules, total LUs, key topic arc
- How modules connect (prerequisites, bridges)
- One-line summary per module

## ⏱️ Section 2: Breadth Sweep Script (90 mins)
- Time-blocked coverage of ALL modules
- 1-2 sentences per topic block: what it covers and why
- Key bridges between modules

## 🔬 Section 3: Deep Dive Topics (2 hours)
- 4-6 hardest topics with:
  - Why it's hard (misconceptions from author notes)
  - Clear analogy or worked example
  - 5-min teach-back prompt

## 📝 Section 4: Readiness Assessment
- 10 MCQs (1 bar above student level)
- 2 teach-back prompts
- Green/Amber/Red scoring rubric

## 🎮 Section 5: Pedagogy Cheat Sheet
- Best analogies for this course's concepts
- Common "I don't get it" moments and how to handle them
- 3 engagement techniques for this type of content

## 📋 Section 6: Facilitator Runsheet
- Minute-by-minute SRD agenda:
  - 9:00-10:30 Breadth Sweep
  - 10:45-12:30 Deep Dive #1
  - 1:30-3:00 Deep Dive #2 + Pedagogy
  - 3:15-4:30 Assessment
  - 4:30-5:00 Wrap-up

IMPORTANT: Do NOT reproduce session flows from the LLD. Use learning objectives, outcomes, and author notes to build the playbook."""

    return _call_llm(prompt)
