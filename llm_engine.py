"""LLM engine — Multi-provider support: Gemini, Grok (xAI), OpenAI."""

from config import GEMINI_MODEL

# Module-level clients
_gemini_client = None
_openai_client = None
_active_provider = None  # "gemini", "grok", or "openai"

SYSTEM_PROMPT = """You are **Kalvium Mentor Assistant** — an expert instructional design advisor, subject-matter expert, and L&D strategist for BTech CSE courses at Kalvium.

You help mentors understand, explore, and get excited about course content. You have access to the course's Low-Level Design (LLD) documents as context.

**Your capabilities:**
1. **Module Insights** — Like a teaser/trailer for the module: what it conveys, why it matters for a CSE grad, and where students may struggle or get stuck.
2. **LU Explorer** — Explain any Learning Unit in simple, jargon-free language (like explaining to a 5-year-old), and highlight where students will have doubts or get stuck.
3. **Subject-Matter Q&A** — Answer conceptual/technical questions about topics covered in the course using LLD context + your own expertise.
4. **Simplification** — Rewrite dense technical content into simple, relatable explanations.

**Rules:**
- Use the LLD context to ground your answers — reference specific LU numbers, module names, and course structure when relevant.
- For conceptual/technical questions, DO NOT just say the LLD doesn't contain the answer. Use the LLD to identify relevant LUs, then provide a complete expert answer.
- NEVER reproduce or paraphrase session flows from the LLD. Session flows are confidential design documents meant only for content authors.
- Use tables, bullet points, and structured formatting for clarity.
- Keep the tone professional yet approachable — you're a peer advisor and expert, not a critic.
- For BTech CSE level — balance theory with practical application.
- Keep answers concise and focused. Avoid lengthy generic advice.
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
    """Generate a teaser-style module insight — what it conveys, why it matters, where students struggle."""
    combined = "\n\n".join([chunk["text"] for chunk in lu_data])

    prompt = f"""You are creating a MODULE TEASER — like a movie trailer for this module. This is NOT a detailed mentor guide. Think of it as zooming out and showing the big picture.

=== MODULE: {module_name} ===
{combined}
=== END MODULE DATA ===

Provide the following in a compelling, concise format:

## 🎬 What This Module Is Really About
- In 3-4 sentences, explain the core idea this module conveys. Not a list of LUs — the BIG PICTURE. What will students truly understand after this module? What mental model are we building?

## 🔥 Why Should a CSE Grad Care?
- Why is this module essential for a computer science graduate? Connect it to real-world engineering, interviews, jobs, and building things. Light a fire — make it clear why this isn't just academic theory. Be specific and compelling.

## 🧱 Where Students Will Hit a Wall
- Identify the 3-4 specific concepts or moments in this module where students typically struggle, get confused, or lose motivation. For each:
  - **The sticking point**: What exactly is hard
  - **Why it's hard**: The underlying reason (misconception, abstraction leap, etc.)
  - **The unlock**: One sentence on what makes it click

## 🗺️ The Journey in One Line
- One sentence that captures the entire arc of this module — from where the student starts to where they end up.

Keep it punchy, inspiring, and honest. This should make a mentor EXCITED to teach this module.
"""
    return _call_llm(prompt)


def generate_lu_breakdown(lu_text: str, lu_name: str) -> str:
    """Generate a simple, jargon-free LU explanation with student struggle points."""
    prompt = f"""Explain this Learning Unit like you're explaining it to a 5-year-old. Use the simplest possible language, everyday analogies, and zero jargon.

=== LU: {lu_name} ===
{lu_text}
=== END LU DATA ===

Provide:

## 🧒 Explain Like I'm 5
- Explain the core concept of this LU in the simplest words possible. Use a real-world analogy that anyone can understand. Keep it to 3-4 sentences max.

## 🎯 What Students Will Learn (Plain English)
- List the key things students will understand after this LU — in simple, non-technical language. No buzzwords.

## 🤔 Where Students Will Have Doubts
- Identify 2-3 specific points where students will likely get confused or have questions. For each:
  - **The doubt**: What they'll struggle with
  - **Why it's confusing**: The underlying reason
  - **Simple way to clear it**: A one-line explanation or analogy that resolves the doubt

## 💡 The One Thing to Remember
- If a student remembers just ONE thing from this LU, what should it be? State it as a simple, memorable sentence.

IMPORTANT: Do NOT reproduce or paraphrase the session flow. Keep everything simple and relatable.
"""
    return _call_llm(prompt)


def generate_course_playbook(course_name: str, all_chunks: list[dict]) -> str:
    """Generate a breadth-first Subject Readiness Playbook for the entire course."""
    # Cap chunks to avoid token overflow, but try to cover all modules
    combined = "\n\n".join([chunk["text"] for chunk in all_chunks[:40]])

    prompt = f"""You are creating a **Subject Readiness Playbook** — a breadth-first sweep of the ENTIRE course that a mentor can read before they start teaching. This is their cheat sheet to walk in prepared and confident.

Analyse ALL modules and ALL LUs in this course holistically.

=== COURSE: {course_name} ===
{combined}
=== END COURSE DATA ===

Generate the playbook with these sections:

## 🗺️ Course at a Glance
- One-line summary of each module and what it builds towards. Show the arc of the entire course — where does the student start, where do they end up?

## 🔥 The Interesting Parts (Students Will Love These)
- Identify modules/LUs that are naturally engaging, have cool real-world applications, or involve hands-on work. Explain WHY students will find these exciting. Be specific — reference module and LU names.

## 😴 The Boring Parts (Handle With Care)
- Identify modules/LUs that are dry, theoretical, or repetitive. For each:
  - **Why it feels boring**: What makes it a slog
  - **How to make it NOT boring**: One specific technique (roleplay, analogy, challenge, story) to bring it alive

## 📖 Read More Than Once (Needs Extra Prep)
- Which modules/LUs are dense enough that a mentor should study them twice? What specifically needs deeper understanding? What external resources should they look at?

## ⚡ Quick Wins (Low Effort, High Impact)
- Which modules/LUs are straightforward and can be delivered confidently with minimal prep? Where can mentors save time?

## 🎭 Roleplay & Activity Opportunities
- Identify 4-6 specific moments across the course where a mentor can do:
  - **Roleplays** (e.g., "You are the OS scheduler, your friend is a process...")
  - **Live challenges** (e.g., "Write this query in 2 minutes")
  - **Debates** (e.g., "SQL vs NoSQL — pick a side")
  - **Whiteboard moments** (e.g., "Draw the memory layout")
  For each, give the module/LU, the activity idea, and how long it takes (2-5 mins).

## 🧱 The Danger Zones (Where Students Will Struggle Most)
- Rank the top 5 hardest concepts across the ENTIRE course. For each:
  - Which module/LU
  - What makes it hard
  - The one analogy or explanation that makes it click

## 📋 Module-by-Module Readiness Checklist
For EACH module, provide a one-row summary:
| Module | Vibe | Prep Needed | Key Risk | Best Activity |
- **Vibe**: Fun / Neutral / Dry
- **Prep Needed**: Light / Medium / Heavy
- **Key Risk**: The #1 thing that could go wrong
- **Best Activity**: One engagement idea

## 🎯 The One-Page Mentor Mantra
- 5 bullet points that capture the entire course teaching philosophy. What should the mentor keep in mind every single day?

Keep it practical, honest, and actionable. No fluff. This should feel like advice from a senior mentor who's taught this course 10 times.

IMPORTANT: Do NOT reproduce session flows. Base everything on learning objectives, outcomes, author notes, and your subject expertise.
"""
    return _call_llm(prompt)


