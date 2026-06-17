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
    get_gemini_response, generate_module_insights, generate_lu_breakdown, generate_srd_playbook
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
    selected = st.radio(
        "Choose a course:",
        options=list(course_options.keys()),
        format_func=lambda x: course_options[x],
        index=None,
        help="Select the course whose LLD you want to analyse"
    )

    if selected:
        st.session_state.selected_course = selected
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

# Tabs
tab_overview, tab_modules, tab_lu_explorer, tab_srd, tab_chat = st.tabs([
    "📊 Course Overview", "📦 Module Insights", "🔍 LU Explorer", "🎯 SRD Playbook", "💬 Ask the Bot"
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
    st.subheader("📦 Module-Level Insights")
    st.caption("Select a module to get AI-generated insights for mentors.")

    selected_module = st.selectbox("Choose a module:", modules, index=0)

    if selected_module:
        mod_df = get_lus_for_module(df, selected_module)

        # Show LU list for this module
        st.markdown(f"**{selected_module}** — {len(mod_df)} Learning Units")

        for _, row in mod_df.iterrows():
            lu_seq = row.get("lu_sequence", "")
            lu_name = row.get("lu_name", "")
            fa = row.get("fa_type", "")
            st.markdown(
                f'<div class="lu-card"><strong>LU {lu_seq}</strong> — {lu_name} '
                f'&nbsp; <code>📝 {fa}</code></div>',
                unsafe_allow_html=True
            )

        st.markdown("---")

        if st.button("🤖 Generate Module Insights", key="mod_insights", type="primary"):
            with st.spinner(f"Analysing {selected_module}... (this may take 15-20 seconds)"):
                # Get all chunks for this module
                mod_chunks = [c for c in st.session_state.rag_engine.chunks
                              if c["metadata"].get("module") == selected_module]
                if not mod_chunks:
                    # Fallback: generate from dataframe
                    mod_chunks = dataframe_to_chunks(mod_df)

                insights = generate_module_insights(selected_module, mod_chunks)
                st.markdown(insights)

                # Store in session for reference
                st.session_state[f"insights_{selected_module}"] = insights

        # Show cached insights if available
        cached = st.session_state.get(f"insights_{selected_module}")
        if cached and not st.session_state.get("_just_generated"):
            with st.expander("📄 Previously Generated Insights", expanded=False):
                st.markdown(cached)


# ─── Tab 3: LU Explorer ───
with tab_lu_explorer:
    st.subheader("🔍 LU Deep-Dive Explorer")
    st.caption("Select any LU to get a mentor-ready breakdown with engagement tips.")

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

        # Quick info cards
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Assessment:** {lu_row.get('fa_type', 'N/A')}")
        with col2:
            st.info(f"**Status:** {lu_row.get('completion_status', 'N/A')}")

        # Learning objectives & outcomes
        objectives = lu_row.get("learning_objectives", "")
        if pd.notna(objectives) and str(objectives).strip():
            with st.expander("🎯 Learning Objectives", expanded=True):
                st.markdown(str(objectives))

        outcomes = lu_row.get("learning_outcomes", "")
        if pd.notna(outcomes) and str(outcomes).strip():
            with st.expander("📈 Learning Outcomes", expanded=False):
                st.markdown(str(outcomes))

        # Assessment details
        assess = lu_row.get("assessment_details", "")
        if pd.notna(assess) and str(assess).strip():
            with st.expander("📝 Assessment Details", expanded=False):
                st.markdown(str(assess))

        # Author notes
        notes = lu_row.get("note_for_authors", "")
        if pd.notna(notes) and str(notes).strip():
            with st.expander("📝 Author Notes & Watch-outs", expanded=False):
                st.warning(str(notes))

        st.markdown("---")

        # AI breakdown
        if st.button("🤖 Generate Mentor Breakdown", key="lu_breakdown", type="primary"):
            with st.spinner(f"Creating mentor guide for {selected_lu}..."):
                breakdown = generate_lu_breakdown(lu_text, selected_lu)
                st.markdown(breakdown)


# ─── Tab 4: SRD Playbook ───
with tab_srd:
    st.subheader("🎯 Subject Readiness Day (SRD) Playbook Generator")
    st.caption(
        "Generate bootcamp materials for mentor readiness days. "
        "Choose a component or generate the full playbook."
    )

    srd_type = st.radio(
        "What do you want to generate?",
        ["📋 Full SRD Playbook", "⏱️ Breadth Sweep Script", "🔬 Deep Dive Topics", "🧪 Practice Self-Check"],
        horizontal=True,
        help="Full playbook includes all components. Or generate individual sections. Note: Actual readiness assessments are conducted separately by L&D — not generated here."
    )

    srd_type_map = {
        "📋 Full SRD Playbook": "full",
        "⏱️ Breadth Sweep Script": "breadth_sweep",
        "🔬 Deep Dive Topics": "deep_dive",
        "🧪 Practice Self-Check": "practice",
    }

    # Optional: select specific modules to include
    st.markdown("---")
    srd_scope = st.multiselect(
        "Scope — select modules to include (leave empty for all):",
        modules,
        default=[],
        help="Select specific modules or leave empty to include the entire course"
    )

    course_name = course_info.get('name', 'Course')

    if st.button("🚀 Generate SRD Content", key="srd_gen", type="primary"):
        with st.spinner(f"Generating {srd_type.split(' ', 1)[1]}... (this may take 30-60 seconds)"):
            # Get chunks for selected scope
            if srd_scope:
                srd_chunks = [c for c in st.session_state.rag_engine.chunks
                              if c["metadata"].get("module") in srd_scope]
            else:
                srd_chunks = st.session_state.rag_engine.chunks

            if not srd_chunks:
                srd_chunks = dataframe_to_chunks(df)

            result = generate_srd_playbook(
                course_name,
                srd_chunks,
                srd_type=srd_type_map[srd_type]
            )
            st.markdown(result)

            # Cache result
            st.session_state[f"srd_{srd_type_map[srd_type]}"] = result

    # Show cached results
    for key, label in [("srd_full", "Full Playbook"), ("srd_breadth_sweep", "Breadth Sweep"),
                        ("srd_deep_dive", "Deep Dives"), ("srd_practice", "Practice Self-Check")]:
        cached = st.session_state.get(key)
        if cached:
            with st.expander(f"📄 Previously Generated: {label}", expanded=False):
                st.markdown(cached)


# ─── Tab 5: Chat ───
with tab_chat:
    st.subheader("💬 Ask the Mentor Bot")
    st.caption("Ask anything about the course design, specific LUs, pedagogy ideas, or troubleshooting.")

    # Quick prompt suggestions
    st.markdown("**Quick prompts:**")
    quick_cols = st.columns(4)
    quick_prompts = [
        "Summarise all modules in this course",
        "Which LUs might be hardest for students?",
        "Suggest 3 ways to make Module 1 more engaging",
        "What are the cross-module bridges?"
    ]
    for col, prompt in zip(quick_cols, quick_prompts):
        with col:
            if st.button(prompt, key=f"qp_{prompt[:20]}", use_container_width=True):
                st.session_state.pending_prompt = prompt

    st.markdown("---")

    # Chat display
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input("Ask about the course LLD...")

    # Handle quick prompt or typed input
    if hasattr(st.session_state, "pending_prompt") and st.session_state.pending_prompt:
        user_input = st.session_state.pending_prompt
        st.session_state.pending_prompt = None

    if user_input:
        # Display user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Retrieve relevant context
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                context_chunks = st.session_state.rag_engine.retrieve(user_input, top_k=6)

                # Build Gemini chat history format
                gemini_history = []
                for msg in st.session_state.chat_history[:-1]:  # Exclude current
                    gemini_history.append({
                        "role": msg["role"] if msg["role"] == "user" else "model",
                        "parts": [msg["content"]]
                    })

                response = get_gemini_response(user_input, context_chunks, gemini_history)
                st.markdown(response)

                # Show source chunks
                with st.expander("📎 Source chunks used for this answer"):
                    for i, chunk in enumerate(context_chunks, 1):
                        meta = chunk["metadata"]
                        st.caption(
                            f"**Chunk {i}** | Module: {meta.get('module', 'N/A')} | "
                            f"LU: {meta.get('lu_seq', '')} - {meta.get('lu_name', '')} | "
                            f"Score: {chunk['score']:.3f}"
                        )

        st.session_state.chat_history.append({"role": "assistant", "content": response})

    # Clear chat button
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()
