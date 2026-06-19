"""Configuration for Kalvium Mentor RAG Bot"""

import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# Supported courses — all 30 technical subjects for early-start campuses
COURSES = {
    "DBMS": {
        "name": "Database Management Systems",
        "icon": "",
        "description": "Covers relational databases, SQL, normalization, transactions, indexing and more."
    },
    "DBMS_LAB": {
        "name": "Database Management Systems — Lab",
        "icon": "",
        "description": "Hands-on lab for DBMS — SQL queries, schema design, normalization exercises."
    },
    "COA": {
        "name": "Computer Organisation & Architecture",
        "icon": "",
        "description": "Covers digital logic, processor design, memory hierarchy, pipelining and more."
    },
    "OS": {
        "name": "Operating Systems",
        "icon": "",
        "description": "Covers Linux administration, process management, file systems, networking, security."
    },
    "OOP": {
        "name": "Object Oriented Programming",
        "icon": "",
        "description": "Classes, objects, inheritance, polymorphism, abstraction, encapsulation and design patterns."
    },
    "OOP_LAB": {
        "name": "Object Oriented Programming — Lab",
        "icon": "",
        "description": "Hands-on OOP lab — coding exercises in Java/C++ with real-world modeling."
    },
    "DAA": {
        "name": "Design and Analysis of Algorithms",
        "icon": "",
        "description": "Sorting, searching, graph algorithms, dynamic programming, greedy methods, complexity analysis."
    },
    "DAA_LAB": {
        "name": "Design and Analysis of Algorithms — Lab",
        "icon": "",
        "description": "Hands-on algorithm implementation, time complexity benchmarking, problem-solving."
    },
    "ADS": {
        "name": "Advanced Database Systems",
        "icon": "",
        "description": "NoSQL, distributed databases, query optimization, transactions at scale, CAP theorem."
    },
    "ADS_LAB": {
        "name": "Advanced Database Systems — Lab",
        "icon": "",
        "description": "Hands-on lab for advanced DB — MongoDB, Redis, query tuning, replication."
    },
    "FLAT": {
        "name": "Formal Language and Automata Theory",
        "icon": "",
        "description": "Finite automata, regular expressions, context-free grammars, Turing machines, computability."
    },
    "FSWD": {
        "name": "Full Stack Web Development",
        "icon": "",
        "description": "Frontend (HTML/CSS/JS/React), backend (Node/Express), APIs, deployment, full-stack projects."
    },
    "FSWD_LAB": {
        "name": "Full Stack Web Development — Lab",
        "icon": "",
        "description": "Hands-on full-stack lab — build and deploy web applications end to end."
    },
    "ELEMENTS_AI": {
        "name": "Elements of AI — Building AI",
        "icon": "",
        "description": "AI fundamentals, search algorithms, machine learning basics, neural network concepts."
    },
    "ELEMENTS_AI_LAB": {
        "name": "Elements of AI — Building AI — Lab",
        "icon": "",
        "description": "Hands-on AI lab — implement search, train simple models, experiment with AI tools."
    },
    "CLOUD": {
        "name": "Cloud Computing",
        "icon": "",
        "description": "Cloud service models (IaaS/PaaS/SaaS), AWS/GCP basics, containers, serverless, deployment."
    },
    "SYSDES": {
        "name": "System Design",
        "icon": "",
        "description": "Scalability, load balancing, caching, database sharding, microservices, design interviews."
    },
    "DEVOPS": {
        "name": "DevOps Foundations",
        "icon": "",
        "description": "CI/CD pipelines, Docker, Kubernetes basics, monitoring, infrastructure as code."
    },
    "DIST_SYS": {
        "name": "Distributed Systems",
        "icon": "",
        "description": "Consensus algorithms, replication, fault tolerance, distributed storage, MapReduce."
    },
    "DSA2": {
        "name": "Data Structures and Algorithms — 2",
        "icon": "",
        "description": "Advanced trees, graphs, tries, segment trees, heaps, advanced DP and competitive patterns."
    },
    "DSA2_LAB": {
        "name": "Data Structures and Algorithms — 2 Lab",
        "icon": "",
        "description": "Hands-on advanced DSA lab — contest-style problems, timed practice."
    },
    "LINUX": {
        "name": "Linux Administration",
        "icon": "",
        "description": "Shell scripting, file systems, user management, networking, process management, security."
    },
    "ML": {
        "name": "Machine Learning",
        "icon": "",
        "description": "Supervised/unsupervised learning, regression, classification, clustering, model evaluation."
    },
    "MALWARE": {
        "name": "Malware Analysis",
        "icon": "",
        "description": "Static/dynamic analysis, reverse engineering, threat detection, sandboxing, security tools."
    },
    "UIUX": {
        "name": "UI and UX Design for CSE",
        "icon": "",
        "description": "Design thinking, wireframing, prototyping, usability testing, Figma, user research."
    },
    "CODING_SKILLS": {
        "name": "Coding Skills for Placements — 1",
        "icon": "",
        "description": "Arrays, strings, recursion, basic DP, sliding window — placement-focused problem solving."
    },
    "INTRO_DS": {
        "name": "Introduction to Data Science",
        "icon": "",
        "description": "Data wrangling, EDA, pandas, visualization, basic statistics, storytelling with data."
    },
    "WORK_INT": {
        "name": "Work Integration",
        "icon": "",
        "description": "Project-based learning — MERN stack project track, real-world software engineering practices."
    },
    "SW_SEM3": {
        "name": "Simulated Work — Sem 3",
        "icon": "",
        "description": "Industry-simulated project work for Semester 3 — teamwork, agile, deliverables."
    },
    "SW_SEM57": {
        "name": "Simulated Work — Sem 5/7",
        "icon": "",
        "description": "Advanced simulated work for Sem 5 & 7 — complex projects, client interaction, production code."
    },
}

# ─── Course → LLD file mapping (hardcoded backend data) ───
# Only courses with a file entry here will show as "ready" to mentors.
# Add new courses by placing the .xlsx in data/ and adding the key here.
COURSE_LLD_FILES = {
    "MALWARE": os.path.join(DATA_DIR, "MALWARE_lld.xlsx"),
    "COA": os.path.join(DATA_DIR, "COA_lld.xlsx"),
    "DSA2": os.path.join(DATA_DIR, "DSA2_lld.xlsx"),
}

# LLD column mapping — maps expected column names to normalized keys
LLD_COLUMNS = {
    "module_name":       ["Module Name", "module_name", "Module"],
    "lu_sequence":       ["LU sequence", "lu_sequence", "LU Sequence", "LU No", "LU Number"],
    "lu_name":           ["LU Name", "lu_name", "LU Title", "Learning Unit Name"],
    "slugs":             ["Slugs", "slugs", "Slug", "LU Slug"],"session_type":      ["Session Type", "session_type", "Sync/Async"],
    "learning_path":     ["Learning Path", "learning_path", "Path"],
    "learning_objectives": ["Learning Objectives", "learning_objectives", "Objectives"],
    "learning_outcomes": ["Learning Outcomes", "learning_outcomes", "Outcomes"],
    "bridge_prev":       ["Bridge from Previous LU", "bridge_prev", "Bridge From"],
    "bridge_next":       ["Bridge to Next LU", "bridge_next", "Bridge To"],
    "session_flow":      ["Session Flow (45 mins)", "session_flow", "Session Flow"],
    "fa_type":           ["FA Type", "fa_type", "Assessment Type", "Formative Assessment Type"],"course_name":       ["Name of the course", "course_name", "Course Name"],
    "course_slug":       ["Course Slug", "course_slug"],
    "assessment_details":["Assessment Details", "assessment_details", "Assessment"],
    "references":        ["References & Resources", "references", "References"],
    "hld_mapping":       ["HLD mapping", "hld_mapping", "HLD Mapping"],
    "level_of_effort":   ["Level of effort", "level_of_effort", "Effort"],
    "note_for_authors":  ["Note for authors", "note_for_authors", "Author Notes", "Notes"],
    "completion_status": ["Completeion status", "Completion status", "completion_status", "Status", "Status of publication"]
}

# Embedding model (runs locally, free)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Chunk settings for RAG
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

# Gemini model
GEMINI_MODEL = "gemini-2.5-flash"
