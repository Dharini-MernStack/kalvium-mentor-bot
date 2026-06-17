"""Configuration for Kalvium Mentor RAG Bot"""

# Supported courses
COURSES = {
    "DBMS": {
        "name": "Database Management Systems",
        "icon": "🗄️",
        "description": "Covers relational databases, SQL, normalization, transactions, indexing and more."
    },
    "COA": {
        "name": "Computer Organisation & Architecture",
        "icon": "🖥️",
        "description": "Covers digital logic, processor design, memory hierarchy, pipelining and more."
    },
    "OS": {
        "name": "Operating Systems",
        "icon": "⚙️",
        "description": "Covers Linux administration, process management, file systems, networking, security."
    }
}

# LLD column mapping — maps expected column names to normalized keys
LLD_COLUMNS = {
    "module_name":       ["Module Name", "module_name", "Module"],
    "lu_sequence":       ["LU sequence", "lu_sequence", "LU Sequence", "LU No", "LU Number"],
    "lu_name":           ["LU Name", "lu_name", "LU Title"],
    "slugs":             ["Slugs", "slugs", "Slug"],
    "learning_path":     ["Learning Path", "learning_path", "Path"],
    "learning_objectives": ["Learning Objectives", "learning_objectives", "Objectives"],
    "learning_outcomes": ["Learning Outcomes", "learning_outcomes", "Outcomes"],
    "bridge_prev":       ["Bridge from Previous LU", "bridge_prev", "Bridge From"],
    "bridge_next":       ["Bridge to Next LU", "bridge_next", "Bridge To"],
    "session_flow":      ["Session Flow (45 mins)", "session_flow", "Session Flow"],
    "fa_type":           ["FA Type", "fa_type", "Assessment Type"],
    "assessment_details":["Assessment Details", "assessment_details", "Assessment"],
    "references":        ["References & Resources", "references", "References"],
    "hld_mapping":       ["HLD mapping", "hld_mapping", "HLD Mapping"],
    "level_of_effort":   ["Level of effort", "level_of_effort", "Effort"],
    "note_for_authors":  ["Note for authors", "note_for_authors", "Author Notes", "Notes"],
    "completion_status": ["Completeion status", "Completion status", "completion_status", "Status"]
}

# Embedding model (runs locally, free)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Chunk settings for RAG
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

# Gemini model
GEMINI_MODEL = "gemini-2.5-flash"
