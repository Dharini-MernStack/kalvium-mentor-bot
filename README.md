# 🎓 Kalvium Mentor RAG Bot

AI-powered course design assistant for Kalvium mentors. Upload a course LLD (Low-Level Design) spreadsheet, explore modules and learning units, and get actionable mentoring insights — all powered by RAG (Retrieval-Augmented Generation).

## 🚀 Features

| Feature | Description |
|---------|-------------|
| **📊 Course Overview** | Auto-generated stats — modules, LUs, core vs bonus, assessment types, completion status |
| **📦 Module Insights** | AI-analysed module summaries with engagement tips, gap analysis, and mentor watch-outs |
| **🔍 LU Explorer** | Deep-dive any Learning Unit — session flow, assessments, author notes, and AI-generated mentor prep guide |
| **💬 Chat with Bot** | Ask anything about the course — the bot answers grounded in your uploaded LLD data |
| **🔗 Cross-LU Bridges** | Understand how LUs and modules connect, prerequisites, and knowledge flow |
| **🎮 Engagement Ideas** | Get specific suggestions to make each session interesting — analogies, activities, hooks |

## 📚 Supported Courses

1. **🗄️ DBMS** — Database Management Systems
2. **🖥️ COA** — Computer Organisation & Architecture
3. **⚙️ OS** — Operating Systems

## 🛠️ Tech Stack (100% Free)

| Layer | Tool |
|-------|------|
| Frontend | Streamlit |
| LLM | Google Gemini 2.0 Flash (free tier) |
| Embeddings | `all-MiniLM-L6-v2` (HuggingFace, local) |
| Vector Store | FAISS (local) |
| File Parsing | pandas + openpyxl |

## ⚡ Quick Start

### 1. Get a Gemini API Key (free)
→ [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)

### 2. Install dependencies
```bash
cd kalvium-mentor-bot
pip3 install -r requirements.txt
```

### 3. Run locally
```bash
streamlit run app.py
```

### 4. Use it
1. Paste your Gemini API key in the sidebar
2. Select a course (e.g., Malware Analysis, COA, OS)
3. Explore the tabs — LLD is auto-loaded!

### Adding new course LLDs
1. Place the `.xlsx` file in `data/` (e.g., `data/DBMS_lld.xlsx`)
2. Add the mapping in `config.py` under `COURSE_LLD_FILES`
3. Deploy!

## 📄 LLD Format Expected

Your spreadsheet should have these columns (flexible naming):

| Column | Description |
|--------|-------------|
| Module Name | e.g., "Linux Foundations & Command Line Mastery" |
| LU sequence | e.g., 1.8, 2.12 |
| LU Name | e.g., "Shell Scripting Fundamentals" |
| Learning Path | Core / Bonus |
| Learning Objectives | What students should understand |
| Learning Outcomes | What students will be able to do |
| Session Flow (45 mins) | Minute-by-minute session plan |
| FA Type | Quiz / Assignment |
| Assessment Details | What students submit, passing bar |
| Note for authors | Misconceptions, tips, cross-LU bridges |
| Completion status | Pending / Complete |

A sample LLD is included at `data/sample_os_lld.xlsx`.

## 🌐 Deploy to Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo, set `app.py` as main file
4. Add `GEMINI_API_KEY` as a secret (optional — users can enter in sidebar)
5. Deploy!

## 📁 Project Structure

```
kalvium-mentor-bot/
├── app.py                  # Main Streamlit application
├── config.py               # Course configs, column mappings
├── lld_parser.py           # Spreadsheet parsing & normalization
├── rag_engine.py           # FAISS + sentence-transformers
├── llm_engine.py           # Gemini API integration
├── requirements.txt        # Python dependencies
├── create_sample_lld.py    # Generate sample test data
├── .streamlit/config.toml  # Theme & server config
├── data/
│   └── sample_os_lld.xlsx  # Sample OS course LLD
└── README.md
```

---

Built for the **Kalvium L&D Team** 🚀
