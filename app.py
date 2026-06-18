"""
Kalvium Mentor RAG Bot — Main Streamlit Application
Helps mentors explore, understand, and improve course LLDs.
"""

import streamlit as st
import pandas as pd
from config import COURSES
from lld_parser import parse_lld, get_modules, get_lus_for_module, lu_to_text, dataframe_to_chunks
from rag_engine import RAGEngine
from llm_engine import (
    configure_gemini, configure_grok, configure_openai, get_active_provider,
    get_gemini_response, generate_module_insights, generate_lu_breakdown, generate_course_playbook
)

# ─── Page Config ───
st.set_page_config(
    page_title="Kalvium Mentor Bot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .main-header h1 { color: white; margin: 0; font-size: 1.8rem; }
    .main-header p { color: #e0e0ff; margin: 0.3rem 0 0 0; font-size: 0.95rem; }
    .module-card {
        background: #f8f9ff;
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 0.8rem;
    }
    .lu-card {
        background: #fffdf5;
        border-left: 4px solid #f0ad4e;
        padding: 0.8rem 1rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }
    .stat-box {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .stat-box h3 { margin: 0; color: #667eea; font-size: 1.8rem; }
    .stat-box p { margin: 0.2rem 0 0; color: #666; font-size: 0.85rem; }
    div[data-testid="stChatMessage"] { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# ─── Session State Init ───
if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = RAGEngine()
if "lld_data" not in st.session_state:
    st.session_state.lld_data = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "gemini_configured" not in st.session_state:
    st.session_state.gemini_configured = False
if "selected_course" not in st.session_state:
    st.session_state.selected_course = None
if "index_built" not in st.session_state:
    st.session_state.index_built = False


# ─── Sidebar ───
with st.sidebar:
    st.markdown("## 🔑 Setup")

    # LLM Provider Selection
    provider = st.selectbox(
        "LLM Provider",
        ["Google Gemini (Free)", "xAI Grok", "OpenAI"],
        index=0,
        help="Choose your LLM provider"
    )

    if provider == "Google Gemini (Free)":
        api_key = st.text_input("Gemini API Key", type="password", placeholder="AIza...",
                                help="Get free at https://aistudio.google.com/apikey")
        if api_key:
            st.session_state.api_key = api_key
            st.session_state.api_provider = "gemini"
            st.session_state.gemini_configured = True
            st.success("✅ Gemini key set")
        else:
            st.info("🔗 [Get free Gemini API key](https://aistudio.google.com/apikey)")
    elif provider == "xAI Grok":
        api_key = st.text_input("Grok API Key", type="password", placeholder="xai-...",
                                help="Get at https://console.x.ai")
        if api_key:
            st.session_state.api_key = api_key
            st.session_state.api_provider = "grok"
            st.session_state.gemini_configured = True
            st.success("✅ Grok key set")
        else:
            st.info("🔗 [Get Grok API key](https://console.x.ai)")
    elif provider == "OpenAI":
        api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...",
                                help="Get at https://platform.openai.com/api-keys")
        if api_key:
            st.session_state.api_key = api_key
            st.session_state.api_provider = "openai"
            st.session_state.gemini_configured = True
            st.success("✅ OpenAI key set")
        else:
            st.info("🔗 [Get OpenAI API key](https://platform.openai.com/api-keys)")

    # Always re-configure client from session state (survives reruns)
    if st.session_state.get("api_key"):
        _prov = st.session_state.get("api_provider", "gemini")
        if _prov == "gemini":
            configure_gemini(st.session_state.api_key)
        elif _prov == "grok":
            configure_grok(st.session_state.api_key)
        elif _prov == "openai":
            configure_openai(st.session_state.api_key)

    st.divider()

    # Course Selection
    st.markdown("## 📚 Select Course")
    course_options = {k: f"{v['icon']} {v['name']}" for k, v in COURSES.items()}
    course_keys = list(course_options.keys()) + ["__custom__"]
    course_labels = {k: v for k, v in course_options.items()}
    course_labels["__custom__"] = "✏️ Other (type your own)"

    selected = st.radio(
        "Choose a course:",
        options=course_keys,
        format_func=lambda x: course_labels[x],
        index=None,
        help="Select a course or type your own"
    )

    if selected == "__custom__":
        custom_course = st.text_input("Enter course name:", placeholder="e.g., Data Structures, CN, SE...")
        if custom_course:
            st.session_state.selected_course = custom_course
            st.session_state.custom_course_name = custom_course
    elif selected:
        st.session_state.selected_course = selected
        st.session_state.custom_course_name = None
        st.caption(COURSES[selected]["description"])

    st.divider()

    # File Upload
    st.markdown("## 📄 Upload LLD")
    uploaded_file = st.file_uploader(
        "Upload LLD spreadsheet",
        type=["xlsx", "xls", "csv"],
        help="Download your Google Sheet as .xlsx or .csv and upload here"
    )

    if uploaded_file:
        try:
            # Cache file bytes in session state to survive Streamlit reruns
            import io
            file_key = f"_file_{uploaded_file.name}_{uploaded_file.size}"
            if file_key not in st.session_state:
                uploaded_file.seek(0)
                st.session_state[file_key] = uploaded_file.read()
            buffered_file = io.BytesIO(st.session_state[file_key])
            buffered_file.name = uploaded_file.name

            with st.spinner("Parsing LLD..."):
                df = parse_lld(buffered_file)
                st.session_state.lld_data = df

                # Build RAG index
                chunks = dataframe_to_chunks(df)
                n_chunks = st.session_state.rag_engine.build_index(chunks)
                st.session_state.index_built = True

            st.success(f"✅ Parsed {len(df)} LUs → {n_chunks} chunks indexed")

            # Show quick stats
            modules = get_modules(df)
            st.metric("Modules", len(modules))
            st.metric("Total LUs", len(df))

            if "completion_status" in df.columns:
                pending = df["completion_status"].astype(str).str.lower().str.contains("pending").sum()
                done = len(df) - pending
                st.metric("Completed", f"{done}/{len(df)}")

        except Exception as e:
            st.error(f"❌ Error parsing file: {e}")

    st.divider()
    st.caption("Built for Kalvium L&D Team 🚀")
    st.caption("Free tier: Gemini Flash + local embeddings")


# ─── Header ───
st.markdown("""
<div class="main-header">
    <h1>🎓 Kalvium Mentor Bot</h1>
    <p>Your AI-powered course design assistant — upload an LLD, explore modules, and get actionable mentor insights.</p>
</div>
""", unsafe_allow_html=True)

# ─── Pre-flight checks ───
if not st.session_state.gemini_configured:
    st.warning("👈 Please enter your **Gemini API key** in the sidebar to get started.")
    st.stop()

if st.session_state.lld_data is None:
    st.info("👈 Please **select a course** and **upload its LLD** spreadsheet in the sidebar.")

    # Show placeholder with instructions
    col1, col2, col3 = st.columns(3)
    for col, (key, course) in zip([col1, col2, col3], COURSES.items()):
        with col:
            st.markdown(f"""
            <div class="stat-box">
                <h3>{course['icon']}</h3>
                <p><strong>{course['name']}</strong></p>
                <p style="font-size:0.8rem; color:#999;">{course['description']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    ### 📝 How to use:
    1. **Get a free Gemini API key** from [Google AI Studio](https://aistudio.google.com/apikey)
    2. **Select a course** from the sidebar
    3. **Download your LLD** Google Sheet as `.xlsx`
    4. **Upload it** using the file uploader
    5. **Explore** modules, LUs, and chat with the bot!
    """)
    st.stop()

# ─── Main Content ───
df = st.session_state.lld_data
modules = get_modules(df)
course_info = COURSES.get(st.session_state.selected_course, {})

# Handle custom course names
if not course_info and st.session_state.get("custom_course_name"):
    course_info = {
        "name": st.session_state.custom_course_name,
        "icon": "📚",
        "description": f"Custom course: {st.session_state.custom_course_name}"
    }

# Tabs
tab_overview, tab_modules, tab_lu_explorer, tab_playbook, tab_chat = st.tabs([
    "📊 Course Overview", "📦 Module Insights", "🔍 LU Explorer", "📚 Readiness Playbook", "💬 Ask the Bot"
])

# ─── Tab 1: Course Overview ───
with tab_overview:
    st.subheader(f"{course_info.get('icon', '📚')} {course_info.get('name', 'Course')} — Overview")

    # Stats row
    stat_cols = ["📦 Modules", "📝 Total LUs"]
    stat_vals = [len(modules), len(df)]

    if "completion_status" in df.columns:
        pending = df["completion_status"].astype(str).str.lower().str.contains("pending").sum()
        done = len(df) - pending
        stat_cols.append("✅ Completed")
        stat_vals.append(f"{done}/{len(df)}")

    cols = st.columns(len(stat_cols))
    for col, label, val in zip(cols, stat_cols, stat_vals):
        with col:
            st.metric(label, val)

    st.markdown("---")

    # Module breakdown table
    st.markdown("### 📋 Module Breakdown")
    module_summary = []
    for mod in modules:
        mod_df = get_lus_for_module(df, mod)
        row = {"Module": mod, "LUs": len(mod_df)}

        if "fa_type" in mod_df.columns:
            row["Quizzes"] = mod_df["fa_type"].astype(str).str.lower().str.contains("quiz").sum()
            row["Assignments"] = mod_df["fa_type"].astype(str).str.lower().str.contains("assignment").sum()
        if "completion_status" in mod_df.columns:
            row["Pending"] = mod_df["completion_status"].astype(str).str.lower().str.contains("pending").sum()
        module_summary.append(row)

    summary_df = pd.DataFrame(module_summary)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    # Raw data preview
    with st.expander("📄 View Raw LLD Data"):
        display_cols = [c for c in df.columns if c in [
            "module_name", "lu_sequence", "lu_name",
            "learning_objectives", "fa_type", "completion_status", "level_of_effort"
        ]]
        if display_cols:
            st.dataframe(df[display_cols], use_container_width=True, hide_index=True)
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)


# ─── Tab 2: Module Insights ───
with tab_modules:
    st.subheader("🎬 Module Insights — The Big Picture")
    st.caption("A teaser for the module: what it conveys, why it matters, and where students will struggle.")

    selected_module = st.selectbox("Choose a module:", modules, index=0, key="mod_select")

    if selected_module:
        mod_df = get_lus_for_module(df, selected_module)

        # Show LU list for this module
        st.markdown(f"**{selected_module}** — {len(mod_df)} Learning Units")

        for _, row in mod_df.iterrows():
            lu_seq = row.get("lu_sequence", "")
            lu_name = row.get("lu_name", "")
            st.markdown(
                f'<div class="lu-card"><strong>LU {lu_seq}</strong> — {lu_name}</div>',
                unsafe_allow_html=True
            )

        st.markdown("---")

        if st.button("🎬 Generate Module Teaser", key="mod_insights", type="primary"):
            with st.spinner(f"Creating teaser for {selected_module}... (15-20 seconds)"):
                mod_chunks = [c for c in st.session_state.rag_engine.chunks
                              if c["metadata"].get("module") == selected_module]
                if not mod_chunks:
                    mod_chunks = dataframe_to_chunks(mod_df)

                insights = generate_module_insights(selected_module, mod_chunks)
                st.markdown(insights)
                st.session_state[f"insights_{selected_module}"] = insights

        # Show cached insights if available
        cached = st.session_state.get(f"insights_{selected_module}")
        if cached and not st.session_state.get("_just_generated"):
            with st.expander("📄 Previously Generated Insights", expanded=False):
                st.markdown(cached)


# ─── Tab 3: LU Explorer ───
with tab_lu_explorer:
    st.subheader("🔍 LU Explorer — Simplified")
    st.caption("Understand any LU in the simplest terms — and know where students will get stuck.")

    col_mod, col_lu = st.columns([1, 2])

    with col_mod:
        exp_module = st.selectbox("Module:", modules, key="exp_module")

    with col_lu:
        if exp_module:
            mod_df = get_lus_for_module(df, exp_module)
            lu_options = []
            for _, row in mod_df.iterrows():
                seq = row.get("lu_sequence", "")
                name = row.get("lu_name", "Unknown")
                lu_options.append(f"LU {seq} — {name}")

            if lu_options:
                selected_lu = st.selectbox("Learning Unit:", lu_options, key="exp_lu")
                lu_idx = lu_options.index(selected_lu)
            else:
                st.warning("No LUs found for this module.")
                selected_lu = None
                lu_idx = None

    if exp_module and selected_lu and lu_idx is not None:
        lu_row = mod_df.iloc[lu_idx]
        lu_text = lu_to_text(lu_row)

        # Show raw LU data in expandable
        with st.expander("📄 Raw LU Data", expanded=False):
            st.text(lu_text)

        # Learning objectives
        objectives = lu_row.get("learning_objectives", "")
        if pd.notna(objectives) and str(objectives).strip():
            with st.expander("🎯 Learning Objectives", expanded=True):
                st.markdown(str(objectives))

        st.markdown("---")

        # AI breakdown
        if st.button("🧒 Explain This LU Simply", key="lu_breakdown", type="primary"):
            with st.spinner(f"Simplifying {selected_lu}..."):
                breakdown = generate_lu_breakdown(lu_text, selected_lu)
                st.markdown(breakdown)
                st.session_state[f"lu_breakdown_{selected_lu}"] = breakdown

        # Show cached breakdown
        cached_lu = st.session_state.get(f"lu_breakdown_{selected_lu}")
        if cached_lu and not st.session_state.get("_just_generated"):
            with st.expander("📄 Previously Generated Breakdown", expanded=False):
                st.markdown(cached_lu)


# ─── Tab 4: Readiness Playbook ───
with tab_playbook:
    st.subheader("📚 Subject Readiness Playbook")
    st.caption(
        "A breadth-first sweep of the entire course — what's interesting, what's boring, "
        "where to prep more, where to do roleplays. Your mentor cheat sheet."
    )

    course_name = course_info.get('name', st.session_state.selected_course or 'Course')

    # Show module overview
    st.markdown(f"**Course: {course_name}** — {len(modules)} Modules, {len(df)} LUs")
    with st.expander("📦 Modules in this course", expanded=False):
        for i, mod in enumerate(modules, 1):
            mod_lu_count = len(get_lus_for_module(df, mod))
            st.markdown(f"{i}. **{mod}** ({mod_lu_count} LUs)")

    st.markdown("---")

    st.markdown("""
    **This playbook will cover:**
    - 🔥 The interesting parts students will love
    - 😴 The boring parts and how to fix them
    - 📖 Topics that need extra prep (read more than once)
    - ⚡ Quick wins that need minimal effort
    - 🎭 Roleplay & activity opportunities
    - 🧱 Danger zones where students struggle most
    - 📋 Module-by-module readiness checklist
    """)

    gen_col, dl_col = st.columns([2, 1])

    with gen_col:
        if st.button("🚀 Generate Readiness Playbook", key="gen_playbook", type="primary", use_container_width=True):
            with st.spinner(f"Generating full-course playbook for {course_name}... (this may take 30-60 seconds)"):
                all_chunks = st.session_state.rag_engine.chunks
                if not all_chunks:
                    all_chunks = dataframe_to_chunks(df)

                playbook = generate_course_playbook(course_name, all_chunks)
                st.session_state["course_playbook"] = playbook
                st.session_state["course_playbook_name"] = course_name

    # Display playbook
    playbook_content = st.session_state.get("course_playbook")
    if playbook_content:
        st.markdown("---")
        st.markdown(playbook_content)

        # Download button
        st.markdown("---")
        playbook_name = st.session_state.get("course_playbook_name", "Course")
        # Build downloadable text
        download_text = f"# Subject Readiness Playbook\n# Course: {playbook_name}\n# Generated by Kalvium Mentor Bot\n\n{playbook_content}"
        st.download_button(
            label="⬇️ Download Playbook (.md)",
            data=download_text,
            file_name=f"{playbook_name.replace(' ', '_')}_Readiness_Playbook.md",
            mime="text/markdown",
            use_container_width=True,
        )


# ─── Tab 5: Chat ───
with tab_chat:
    st.subheader("💬 Ask the Mentor Bot")
    st.caption("Ask anything about the course. You can go back & forth for up to 5 messages per thread.")

    MAX_CHAT_TURNS = 5  # Max user messages per thread

    # "New Chat" button — always visible at the top when there's history
    if st.session_state.chat_history:
        new_chat_col, info_col = st.columns([1, 3])
        with new_chat_col:
            if st.button("✨ New Chat", key="new_chat_top", type="primary", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
        with info_col:
            user_msg_count = sum(1 for m in st.session_state.chat_history if m["role"] == "user")
            remaining = MAX_CHAT_TURNS - user_msg_count
            if remaining > 0:
                st.caption(f"💬 {user_msg_count}/{MAX_CHAT_TURNS} messages used · {remaining} remaining")
            else:
                st.caption(f"💬 {MAX_CHAT_TURNS}/{MAX_CHAT_TURNS} messages used · Start a new chat to continue")

    # Context selector: Module + LU
    st.markdown("**📍 Set Context (optional):**")
    ctx_col1, ctx_col2 = st.columns([1, 2])
    with ctx_col1:
        chat_module = st.selectbox("Module:", ["— All Modules —"] + modules, key="chat_module")
    with ctx_col2:
        chat_lu = None
        if chat_module and chat_module != "— All Modules —":
            chat_mod_df = get_lus_for_module(df, chat_module)
            chat_lu_options = ["— All LUs —"]
            for _, row in chat_mod_df.iterrows():
                seq = row.get("lu_sequence", "")
                name = row.get("lu_name", "Unknown")
                chat_lu_options.append(f"LU {seq} — {name}")
            chat_lu = st.selectbox("Learning Unit:", chat_lu_options, key="chat_lu")

    st.markdown("---")

    # Quick prompt suggestions
    st.markdown("**Quick prompts:**")
    quick_cols = st.columns(3)
    quick_prompts = [
        "What will students find most difficult in this LU?",
        "Where will students get stuck in this module?",
        "Explain the core concept of this LU simply",
    ]
    for col, prompt in zip(quick_cols, quick_prompts):
        with col:
            if st.button(prompt, key=f"qp_{prompt[:25]}", use_container_width=True):
                st.session_state.pending_prompt = prompt

    st.markdown("---")

    # Count user messages
    user_msg_count = sum(1 for m in st.session_state.chat_history if m["role"] == "user")

    # Chat display
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Check thread limit
    if user_msg_count >= MAX_CHAT_TURNS:
        st.toast("🔄 Start a fresh chat! Smaller context window prevents hallucination.", icon="💡")
        st.info(
            "You've used all **5 messages** in this thread. "
            "Start a new chat for fresh, accurate responses — smaller context = less hallucination! 🎯"
        )
        if st.button("✨ Start New Chat", key="new_thread", type="primary", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    else:
        # Chat input
        remaining = MAX_CHAT_TURNS - user_msg_count
        user_input = st.chat_input(f"Ask about the course... ({remaining} messages remaining)")

        # Handle quick prompt or typed input
        if hasattr(st.session_state, "pending_prompt") and st.session_state.pending_prompt:
            user_input = st.session_state.pending_prompt
            st.session_state.pending_prompt = None

        if user_input:
            # Build context prefix based on module/LU selection
            context_prefix = ""
            module_filter = None
            if chat_module and chat_module != "— All Modules —":
                context_prefix += f"[Context: Module = {chat_module}"
                module_filter = chat_module
                if chat_lu and chat_lu != "— All LUs —":
                    context_prefix += f", {chat_lu}"
                context_prefix += "] "

            display_input = user_input
            augmented_input = context_prefix + user_input if context_prefix else user_input

            # Display user message
            st.session_state.chat_history.append({"role": "user", "content": display_input})
            with st.chat_message("user"):
                st.markdown(display_input)

            # Retrieve relevant context
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    context_chunks = st.session_state.rag_engine.retrieve(
                        augmented_input, top_k=6, module_filter=module_filter
                    )

                    # Build chat history format
                    gemini_history = []
                    for msg in st.session_state.chat_history[:-1]:
                        gemini_history.append({
                            "role": msg["role"] if msg["role"] == "user" else "model",
                            "parts": [msg["content"]]
                        })

                    response = get_gemini_response(augmented_input, context_chunks, gemini_history)
                    st.markdown(response)

                    with st.expander("📎 Source chunks used"):
                        for i, chunk in enumerate(context_chunks, 1):
                            meta = chunk["metadata"]
                            st.caption(
                                f"**Chunk {i}** | Module: {meta.get('module', 'N/A')} | "
                                f"LU: {meta.get('lu_seq', '')} - {meta.get('lu_name', '')} | "
                                f"Score: {chunk['score']:.3f}"
                            )

            st.session_state.chat_history.append({"role": "assistant", "content": response})

            # Show toast on 4th message as a heads-up
            new_count = user_msg_count + 1
            if new_count == MAX_CHAT_TURNS - 1:
                st.toast("⚡ 1 message left in this thread!", icon="⚠️")
            elif new_count >= MAX_CHAT_TURNS:
                st.toast("🔄 Start a fresh chat! Smaller context = less hallucination.", icon="💡")
