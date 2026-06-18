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

#  Page Config 
st.set_page_config(
    page_title="Kalvium Mentor Bot",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

#  Custom CSS 
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

#  Session State Init 
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


#  Sidebar 
with st.sidebar:
    st.markdown("##  Setup")

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
            st.success(" Gemini key set")
        else:
            st.info(" [Get free Gemini API key](https://aistudio.google.com/apikey)")
    elif provider == "xAI Grok":
        api_key = st.text_input("Grok API Key", type="password", placeholder="xai-...",
                                help="Get at https://console.x.ai")
        if api_key:
            st.session_state.api_key = api_key
            st.session_state.api_provider = "grok"
            st.session_state.gemini_configured = True
            st.success(" Grok key set")
        else:
            st.info(" [Get Grok API key](https://console.x.ai)")
    elif provider == "OpenAI":
        api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...",
                                help="Get at https://platform.openai.com/api-keys")
        if api_key:
            st.session_state.api_key = api_key
            st.session_state.api_provider = "openai"
            st.session_state.gemini_configured = True
            st.success(" OpenAI key set")
        else:
            st.info(" [Get OpenAI API key](https://platform.openai.com/api-keys)")

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
    st.markdown("##  Select Course")
    course_options = {k: v['name'] for k, v in COURSES.items()}
    course_keys = list(course_options.keys()) + ["__custom__"]
    course_labels = {k: v for k, v in course_options.items()}
    course_labels["__custom__"] = " Other (type your own)"

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
    st.markdown("##  Upload LLD")
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

            st.success(f" Parsed {len(df)} LUs  {n_chunks} chunks indexed")

            # Show quick stats
            modules = get_modules(df)
            st.metric("Modules", len(modules))
            st.metric("Total LUs", len(df))

            if "completion_status" in df.columns:
                pending = df["completion_status"].astype(str).str.lower().str.contains("pending").sum()
                done = len(df) - pending
                st.metric("Completed", f"{done}/{len(df)}")

        except Exception as e:
            st.error(f" Error parsing file: {e}")

    st.divider()
    st.caption("Built for Kalvium L&D Team ")
    st.caption("Free tier: Gemini Flash + local embeddings")


#  Header 
st.markdown("""
<div class="main-header">
    <h1> Kalvium Mentor Bot</h1>
    <p>Your AI-powered course design assistant — upload an LLD, explore modules, and get actionable mentor insights.</p>
</div>
""", unsafe_allow_html=True)

#  Pre-flight checks 
if not st.session_state.gemini_configured:
    st.warning(" Please enter your **Gemini API key** in the sidebar to get started.")
    st.stop()

if st.session_state.lld_data is None:
    st.info(" Please **select a course** and **upload its LLD** spreadsheet in the sidebar.")

    # Show placeholder with instructions
    col1, col2, col3 = st.columns(3)
    for col, (key, course) in zip([col1, col2, col3], COURSES.items()):
        with col:
            st.markdown(f"""
            <div class="stat-box">
                <h3>{key}</h3>
                <p><strong>{course['name']}</strong></p>
                <p style="font-size:0.8rem; color:#999;">{course['description']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    ###  How to use:
    1. **Get a free Gemini API key** from [Google AI Studio](https://aistudio.google.com/apikey)
    2. **Select a course** from the sidebar
    3. **Download your LLD** Google Sheet as `.xlsx`
    4. **Upload it** using the file uploader
    5. **Explore** modules, LUs, and chat with the bot!
    """)
    st.stop()

#  Main Content 
df = st.session_state.lld_data
modules = get_modules(df)
course_info = COURSES.get(st.session_state.selected_course, {})

# Handle custom course names
if not course_info and st.session_state.get("custom_course_name"):
    course_info = {
        "name": st.session_state.custom_course_name,
        "icon": "",
        "description": f"Custom course: {st.session_state.custom_course_name}"
    }

# Tabs
tab_overview, tab_modules, tab_lu_explorer, tab_readiness_map, tab_playbook, tab_chat = st.tabs([
    " Course Overview", " Module Insights", " LU Explorer", " Subject Readiness Map", " Readiness Playbook", " Ask the Bot"
])

#  Tab 1: Course Overview 
with tab_overview:
    st.subheader(f"{course_info.get('name', 'Course')} — Overview")

    # Stats row
    stat_cols = [" Modules", " Total LUs"]
    stat_vals = [len(modules), len(df)]

    if "completion_status" in df.columns:
        pending = df["completion_status"].astype(str).str.lower().str.contains("pending").sum()
        done = len(df) - pending
        stat_cols.append(" Completed")
        stat_vals.append(f"{done}/{len(df)}")

    cols = st.columns(len(stat_cols))
    for col, label, val in zip(cols, stat_cols, stat_vals):
        with col:
            st.metric(label, val)

    st.markdown("---")

    # Module breakdown table
    st.markdown("###  Module Breakdown")
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
    with st.expander(" View Raw LLD Data"):
        display_cols = [c for c in df.columns if c in [
            "module_name", "lu_sequence", "lu_name",
            "learning_objectives", "fa_type", "completion_status", "level_of_effort"
        ]]
        if display_cols:
            st.dataframe(df[display_cols], use_container_width=True, hide_index=True)
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)


#  Tab 2: Module Insights 
with tab_modules:
    st.subheader(" Module Insights — The Big Picture")
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

        if st.button(" Generate Module Teaser", key="mod_insights", type="primary"):
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
            with st.expander(" Previously Generated Insights", expanded=False):
                st.markdown(cached)


#  Tab 3: LU Explorer 
with tab_lu_explorer:
    st.subheader(" LU Explorer — Simplified")
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
        with st.expander(" Raw LU Data", expanded=False):
            st.text(lu_text)

        # Learning objectives
        objectives = lu_row.get("learning_objectives", "")
        if pd.notna(objectives) and str(objectives).strip():
            with st.expander(" Learning Objectives", expanded=True):
                st.markdown(str(objectives))

        st.markdown("---")

        # AI breakdown
        if st.button(" Explain This LU Simply", key="lu_breakdown", type="primary"):
            with st.spinner(f"Simplifying {selected_lu}..."):
                breakdown = generate_lu_breakdown(lu_text, selected_lu)
                st.markdown(breakdown)
                st.session_state[f"lu_breakdown_{selected_lu}"] = breakdown

        # Show cached breakdown
        cached_lu = st.session_state.get(f"lu_breakdown_{selected_lu}")
        if cached_lu and not st.session_state.get("_just_generated"):
            with st.expander(" Previously Generated Breakdown", expanded=False):
                st.markdown(cached_lu)


#  Tab 4: Subject Readiness Map 
with tab_readiness_map:
    st.subheader(" Subject Readiness Map — Early-Start Campuses")
    st.caption("L&D handout delivery schedule, campus-subject mapping, buddy mentor likelihood, and mentor classification framework.")

    #  Campus-Subject Overview 
    st.markdown("###  Campus Start Dates & Technical Subject Count")

    CAMPUS_DATA = {
        "TAU": {
            "full_name": "The Apollo University",
            "start_date": "1st July 2026",
            "semesters": "Sem 5, Sem 7",
            "program": "SPE",
            "subjects": {
                "Sem 5": [
                    ("Computer Organisation & Architecture", "coa4_v3", "Completely New", "Low"),
                    ("Design and Analysis of Algorithms", "daa5_v3", "Completely New", "Low"),
                    ("Formal Language and Automata Theory", "flat_spe5_v1", "Minor Revamp", "High"),
                    ("Simulated Work Sem 5/7", "sw_sem57_2026", "Completely New", "Low"),
                ],
                "Sem 7": [
                    ("Cloud Computing", "cloudcom5_v1", "Completely New", "Low"),
                    ("System Design", "sys_des5_v1", "Completely New", "Low"),
                    ("Simulated Work Sem 5/7", "sw_sem57_2026", "Completely New", "Low"),
                ],
            },
            "total": 7,
            "buddy_likelihood": "Low (mostly new courses, 1 revamp — FLAT)",
        },
        "SGT": {
            "full_name": "SGT University",
            "start_date": "1st July 2026",
            "semesters": "Sem 3",
            "program": "SPE & AIFT",
            "subjects": {
                "Sem 3": [
                    ("Advanced Database Systems (Theory)", "advdbtheory3_v2", "Completely New", "Medium"),
                    ("Advanced Database Systems (Lab)", "advdblab3_v2", "Completely New", "Medium"),
                    ("Elements of AI — Building AI (Theory)", "elements_ai_theory3_v2", "Completely New", "Low"),
                    ("Elements of AI — Building AI (Lab)", "elements_ai_lab2_v2", "Completely New", "Low"),
                    ("Full Stack Web Development (Theory)", "fswdtheory4_v2", "Completely New", "Low"),
                    ("Full Stack Web Development (Lab)", "fswdlab6_v2", "Completely New", "Low"),
                    ("Object Oriented Programming (Theory)", "ooptheory3_v2", "Completely New", "Medium"),
                    ("Object Oriented Programming (Lab)", "ooplab2_v2", "Completely New", "Medium"),
                    ("Database Management Systems (Theory)", "dbmstheory_spe3_v2", "Minor Revamp", "High"),
                    ("Database Management Systems (Lab)", "dbmslab_spe2_v2", "Minor Revamp", "High"),
                    ("Simulated Work Sem 3", "sw_sem3_2026", "Completely New", "Low"),
                ],
            },
            "total": 11,
            "buddy_likelihood": "Low-Medium (2 revamp subjects — DBMS)",
        },
        "AMET": {
            "full_name": "AMET University",
            "start_date": "1st July 2026",
            "semesters": "Sem 3, Sem 5",
            "program": "AI & DS, AI & ML, Cybersecurity",
            "subjects": {
                "Sem 3": [
                    ("Computer Organisation & Architecture", "coa4_v3", "Completely New", "Medium"),
                    ("UI and UX Design for CSE", "uiux5_v3", "Completely New", "Low"),
                    ("Operating Systems", "os5_v2", "Major Revamp", "High"),
                    ("Coding Skills for Placements — 1", "coding_skills2_v1", "Completely New", "Low"),
                ],
                "Sem 5": [
                    ("Linux Administration", "linux_administration_5_v1", "Minor Revamp", "High"),
                    ("Data Structures & Algorithms 2 (Theory)", "dsa2theory3_v1", "Minor Revamp", "High"),
                    ("Data Structures & Algorithms 2 (Lab)", "dsa2lab2_v1", "Minor Revamp", "High"),
                    ("Advanced Database Systems", "advdb6_v2", "Completely New", "Medium"),
                    ("Coding Skills for Placements — 1", "coding_skills2_v1", "Completely New", "Low"),
                    ("Work Integration", "projtrack_mern_lvl1", "Completely New", "Low"),
                    ("Introduction to Data Science", "intro_ds5_v1", "Minor Revamp", "High"),
                    ("Machine Learning", "ml5_v1", "Completely New", "Low"),
                    ("Malware Analysis", "malware_analysis5_v1", "Completely New", "Low"),
                ],
            },
            "total": 13,
            "buddy_likelihood": "Medium (5 revamp subjects — OS, DSA2, Linux, DBMS, Intro DS)",
        },
        "MIT": {
            "full_name": "MIT ADT University",
            "start_date": "1st July 2026",
            "semesters": "Sem 3, Sem 5, Sem 7",
            "program": "SPE",
            "subjects": {
                "Sem 3": [
                    ("Database Management Systems (Theory)", "dbmstheory_spe3_v2", "Minor Revamp", "High"),
                    ("Database Management Systems (Lab)", "dbmslab_spe2_v2", "Minor Revamp", "High"),
                    ("Object Oriented Programming (Theory)", "ooptheory3_v2", "Completely New", "Medium"),
                    ("Object Oriented Programming (Lab)", "ooplab2_v2", "Completely New", "Medium"),
                    ("Simulated Work Sem 3", "sw_sem3_2026", "Completely New", "Low"),
                ],
                "Sem 5": [
                    ("Computer Organisation & Architecture", "coa4_v3", "Completely New", "Medium"),
                    ("Design and Analysis of Algorithms (Theory)", "daatheory3_v2", "Completely New", "Low"),
                    ("Design and Analysis of Algorithms (Lab)", "daalab2_v2", "Completely New", "Low"),
                    ("DevOps Foundations", "devops5_v1", "Completely New", "Low"),
                    ("Simulated Work Sem 5/7", "sw_sem57_2026", "Completely New", "Low"),
                ],
                "Sem 7": [
                    ("Cloud Computing", "cloudcom5_v1", "Completely New", "Low"),
                    ("System Design", "sys_des5_v1", "Completely New", "Low"),
                    ("Simulated Work Sem 5/7", "sw_sem57_2026", "Completely New", "Low"),
                ],
            },
            "total": 13,
            "buddy_likelihood": "Low-Medium (2 revamp — DBMS)",
        },
        "VELS": {
            "full_name": "Vels University",
            "start_date": "2nd July 2026",
            "semesters": "Sem 3, Sem 5, Sem 7",
            "program": "SPE",
            "subjects": {
                "Sem 3": [
                    ("Database Management Systems (Theory)", "dbmstheory_spe3_v2", "Minor Revamp", "High"),
                    ("Database Management Systems (Lab)", "dbmslab_spe2_v2", "Minor Revamp", "High"),
                    ("Object Oriented Programming (Theory)", "ooptheory3_v2", "Completely New", "Medium"),
                    ("Object Oriented Programming (Lab)", "ooplab2_v2", "Completely New", "Medium"),
                    ("Simulated Work Sem 3", "sw_sem3_2026", "Completely New", "Low"),
                ],
                "Sem 5": [
                    ("Computer Organisation & Architecture", "coa4_v3", "Completely New", "Medium"),
                    ("Design and Analysis of Algorithms (Theory)", "daatheory3_v2", "Completely New", "Low"),
                    ("Design and Analysis of Algorithms (Lab)", "daalab2_v2", "Completely New", "Low"),
                    ("Formal Language and Automata Theory", "flat_spe5_v1", "Minor Revamp", "High"),
                    ("Simulated Work Sem 5/7", "sw_sem57_2026", "Completely New", "Low"),
                ],
                "Sem 7": [
                    ("Distributed Systems", "distributed_systems5_v1", "Completely New", "Low"),
                    ("System Design", "sys_des5_v1", "Completely New", "Low"),
                    ("Simulated Work Sem 5/7", "sw_sem57_2026", "Completely New", "Low"),
                ],
            },
            "total": 13,
            "buddy_likelihood": "Low-Medium (3 revamp — DBMS, FLAT)",
        },
    }

    # Summary cards
    campus_cols = st.columns(5)
    for col, (code, info) in zip(campus_cols, CAMPUS_DATA.items()):
        with col:
            st.markdown(f"""
            <div class="stat-box">
                <h3>{info['total']}</h3>
                <p><strong>{code}</strong></p>
                <p style="font-size:0.75rem; color:#999;">{info['start_date']}<br>{info['semesters']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    #  Expandable campus details 
    st.markdown("###  Campus-wise Subject Details")
    for code, info in CAMPUS_DATA.items():
        with st.expander(f"**{code} — {info['full_name']}**  |  {info['start_date']}  |  {info['total']} subjects  |  Buddy: {info['buddy_likelihood']}", expanded=False):
            st.markdown(f"**Program:** {info['program']}  |  **Semesters:** {info['semesters']}")
            for sem, subjects in info["subjects"].items():
                st.markdown(f"**{sem}** ({len(subjects)} subjects)")
                sem_df = pd.DataFrame(subjects, columns=["Subject", "Course Slug", "Nature", "Buddy Likelihood"])
                st.dataframe(sem_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    #  Handout Delivery Schedule 
    st.markdown("###  Handout Delivery Schedule (22–25 June 2026)")
    st.info("L&D delivers breadth-first sweep handouts sequentially. All handouts also available on this bot for download.")

    HANDOUT_SCHEDULE = {
        "Day 1 — Mon 22 Jun": {
            "theme": "Core CS Fundamentals (widest campus reach first)",
            "subjects": [
                ("Computer Organisation & Architecture", "coa4_v3", "TAU, AMET, MIT, VELS"),
                ("Object Oriented Programming (Theory)", "ooptheory3_v2", "SGT, MIT, VELS"),
                ("Object Oriented Programming (Lab)", "ooplab2_v2", "SGT, MIT, VELS"),
                ("Database Management Systems (Theory)", "dbmstheory_spe3_v2", "SGT, MIT, VELS"),
                ("Database Management Systems (Lab)", "dbmslab_spe2_v2", "SGT, MIT, VELS"),
                ("Operating Systems", "os5_v2", "AMET"),
                ("Formal Language and Automata Theory", "flat_spe5_v1", "TAU, VELS"),
                ("Coding Skills for Placements — 1", "coding_skills2_v1", "AMET"),
            ]
        },
        "Day 2 — Tue 23 Jun": {
            "theme": "Algorithms, Databases & Web Development",
            "subjects": [
                ("Design & Analysis of Algorithms (Theory)", "daa5_v3 / daatheory3_v2", "TAU, MIT, VELS"),
                ("Design & Analysis of Algorithms (Lab)", "daalab2_v2", "MIT, VELS"),
                ("Advanced Database Systems (Theory)", "advdbtheory3_v2", "SGT, AMET"),
                ("Advanced Database Systems (Lab)", "advdblab3_v2", "SGT"),
                ("Data Structures & Algorithms 2 (Theory)", "dsa2theory3_v1", "AMET"),
                ("Data Structures & Algorithms 2 (Lab)", "dsa2lab2_v1", "AMET"),
                ("Full Stack Web Development (Theory)", "fswdtheory4_v2", "SGT"),
                ("Full Stack Web Development (Lab)", "fswdlab6_v2", "SGT"),
            ]
        },
        "Day 3 — Wed 24 Jun": {
            "theme": "Systems, Cloud, DevOps & AI Foundations",
            "subjects": [
                ("Cloud Computing", "cloudcom5_v1", "TAU, MIT"),
                ("System Design", "sys_des5_v1", "TAU, MIT, VELS"),
                ("DevOps Foundations", "devops5_v1", "MIT"),
                ("Distributed Systems", "distributed_systems5_v1", "VELS"),
                ("Linux Administration", "linux_administration_5_v1", "AMET"),
                ("Elements of AI — Building AI (Theory)", "elements_ai_theory3_v2", "SGT"),
                ("Elements of AI — Building AI (Lab)", "elements_ai_lab2_v2", "SGT"),
            ]
        },
        "Day 4 — Thu 25 Jun": {
            "theme": "Specializations, Applied Subjects & Simulated Work",
            "subjects": [
                ("Machine Learning", "ml5_v1", "AMET"),
                ("Malware Analysis", "malware_analysis5_v1", "AMET"),
                ("UI and UX Design for CSE", "uiux5_v3", "AMET"),
                ("Introduction to Data Science", "intro_ds5_v1", "AMET"),
                ("Work Integration", "projtrack_mern_lvl1", "AMET"),
                ("Simulated Work — Sem 3", "sw_sem3_2026", "SGT, MIT, VELS"),
                ("Simulated Work — Sem 5/7", "sw_sem57_2026", "TAU, MIT, VELS"),
            ]
        },
    }

    for day, data in HANDOUT_SCHEDULE.items():
        with st.expander(f"**{day}** — {len(data['subjects'])} subjects | _{data['theme']}_", expanded=False):
            day_df = pd.DataFrame(data["subjects"], columns=["Subject", "Course Slug", "Campuses Receiving"])
            st.dataframe(day_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    #  Self-Study & Buddy Mentors 
    st.markdown("###  Buddy Mentor & Self-Study Framework")

    bm_col1, bm_col2 = st.columns(2)
    with bm_col1:
        st.markdown("**Self-Study Window**")
        st.markdown("""
        | Handout Day | Study Window to Assessment |
        |---|---|
        | Day 1 (22 Jun) | 7 days |
        | Day 2 (23 Jun) | 6 days |
        | Day 3 (24 Jun) | 5 days |
        | Day 4 (25 Jun) | 4 days |
        """)

    with bm_col2:
        st.markdown("**Buddy Mentor Likelihood by Subject**")
        st.markdown("""
        | Subject | Likelihood |
        |---|---|
        | DBMS, FLAT, OS | 🟢 High |
        | DSA2, Linux, Intro DS | 🟢 High |
        | OOP, COA, Adv DB | 🟡 Medium |
        | All new courses |  Low |
        """)

    st.markdown("---")

    #  Assessment & Classification 
    st.markdown("###  Assessment & Mentor Classification (29–30 June)")

    ac_col1, ac_col2 = st.columns(2)
    with ac_col1:
        st.markdown("**29th June — Module 1 Practice Assessment**")
        st.markdown("""
        - **Duration:** 75 minutes (proctored)
        - **Sections:** MCQ (40%) + Applied (40%) + Pedagogy (20%)
        - **Pass:** 60% overall, no section below 40%
        - **Source:** Training handouts + Module 1 content
        """)

    with ac_col2:
        st.markdown("**30th June — Presentation Demo**")
        st.markdown("""
        - **Duration:** 15 min teaching + 5 min Q&A
        - **Criteria:** Content Accuracy (30%), Clarity (25%), Engagement (25%), Presence (20%)
        - **Panel:** 2–3 L&D evaluators
        """)

    st.markdown("")
    st.markdown("**Mentor Classification (Post-Assessment)**")
    class_df = pd.DataFrame([
        ["O (Outstanding)", "85%+", " Fully ready. Minimal oversight. Can buddy-mentor others.", "🟢"],
        ["A (Proficient)", "70–84%", " Ready with minor guidance. Standard check-ins.", ""],
        ["B (Developing)", "60–69%", " Weekly L&D check-ins, content reinforcement, observation.", "🟡"],
        ["C (At Risk)", "Below 60%", " Daily check-ins, co-teaching, intensive L&D support.", ""],
    ], columns=["Tier", "Score", "Action Plan", "Flag"])
    st.dataframe(class_df, use_container_width=True, hide_index=True)

    st.markdown("")
    st.warning(
        "**No AI-assisted support at this stage** due to infrastructure constraints. "
        "Mentors who fail will receive direct L&D intervention. B & C tier mentors are the primary focus area."
    )

    st.markdown("---")

    #  Key Milestones 
    st.markdown("###  Key Milestones")
    milestones_df = pd.DataFrame([
        ["18–21 Jun", "L&D finalizes handouts + buddy matching", "Preparation"],
        ["22 Jun (Mon)", "Handout Day 1 — 8 subjects released", "Core CS"],
        ["23 Jun (Tue)", "Handout Day 2 — 8 subjects released", "Algo, DB, Web"],
        ["24 Jun (Wed)", "Handout Day 3 — 7 subjects released", "Systems, Cloud, AI"],
        ["25 Jun (Thu)", "Handout Day 4 — ALL 30 handouts done ", "Specializations"],
        ["26–28 Jun", "Self-study + Buddy sessions + Doubt clearing", "Mentor prep"],
        ["29 Jun (Sun)", "MODULE 1 ASSESSMENT", "75-min test"],
        ["30 Jun (Mon)", "DEMO + CLASSIFICATION", "O/A/B/C finalized"],
        ["1 Jul (Tue)", "Campus start — TAU, SGT, AMET, MIT", "Semester begins"],
        ["2 Jul (Wed)", "Campus start — VELS", "Semester begins"],
    ], columns=["Date", "Milestone", "Notes"])
    st.dataframe(milestones_df, use_container_width=True, hide_index=True)


#  Tab 5: Readiness Playbook 
with tab_playbook:
    st.subheader(" Subject Readiness Playbook")
    st.caption(
        "A breadth-first sweep of the entire course — what's interesting, what's boring, "
        "where to prep more, where to do roleplays. Your mentor cheat sheet."
    )

    course_name = course_info.get('name', st.session_state.selected_course or 'Course')

    # Show module overview
    st.markdown(f"**Course: {course_name}** — {len(modules)} Modules, {len(df)} LUs")
    with st.expander(" Modules in this course", expanded=False):
        for i, mod in enumerate(modules, 1):
            mod_lu_count = len(get_lus_for_module(df, mod))
            st.markdown(f"{i}. **{mod}** ({mod_lu_count} LUs)")

    st.markdown("---")

    st.markdown("""
    **This playbook will cover:**
    -  The interesting parts students will love
    -  The boring parts and how to fix them
    -  Topics that need extra prep (read more than once)
    -  Quick wins that need minimal effort
    -  Roleplay & activity opportunities
    -  Danger zones where students struggle most
    -  Module-by-module readiness checklist
    """)

    gen_col, dl_col = st.columns([2, 1])

    with gen_col:
        if st.button(" Generate Readiness Playbook", key="gen_playbook", type="primary", use_container_width=True):
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
            label=" Download Playbook (.md)",
            data=download_text,
            file_name=f"{playbook_name.replace(' ', '_')}_Readiness_Playbook.md",
            mime="text/markdown",
            use_container_width=True,
        )


#  Tab 5: Chat 
with tab_chat:
    st.subheader(" Ask the Mentor Bot")
    st.caption("Ask anything about the course. You can go back & forth for up to 5 messages per thread.")

    MAX_CHAT_TURNS = 5  # Max user messages per thread

    # "New Chat" button — always visible at the top when there's history
    if st.session_state.chat_history:
        new_chat_col, info_col = st.columns([1, 3])
        with new_chat_col:
            if st.button(" New Chat", key="new_chat_top", type="primary", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
        with info_col:
            user_msg_count = sum(1 for m in st.session_state.chat_history if m["role"] == "user")
            remaining = MAX_CHAT_TURNS - user_msg_count
            if remaining > 0:
                st.caption(f" {user_msg_count}/{MAX_CHAT_TURNS} messages used · {remaining} remaining")
            else:
                st.caption(f" {MAX_CHAT_TURNS}/{MAX_CHAT_TURNS} messages used · Start a new chat to continue")

    # Context selector: Module + LU
    st.markdown("** Set Context (optional):**")
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
        st.toast("Start a fresh chat! Smaller context window prevents hallucination.")
        st.info(
            "You've used all **5 messages** in this thread. "
            "Start a new chat for fresh, accurate responses — smaller context = less hallucination! "
        )
        if st.button(" Start New Chat", key="new_thread", type="primary", use_container_width=True):
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

                    with st.expander(" Source chunks used"):
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
                st.toast("1 message left in this thread!")
            elif new_count >= MAX_CHAT_TURNS:
                st.toast("Start a fresh chat! Smaller context = less hallucination.")
