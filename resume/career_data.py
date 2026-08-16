"""
Static knowledge base used to build career-path roadmaps.
Later this can be swapped for an LLM call (see career_prompt.py),
same way analyzer.py is meant to move to Gemini.
"""

# Target roles a user can plan toward, and the skills each one expects.
# Order matters loosely (earlier = more foundational for that role).
ROLE_SKILL_MAP = {
    "Full Stack Developer": [
        "html", "css", "javascript", "react", "node.js", "sql",
        "git", "rest api", "mongodb", "docker", "aws"
    ],
    "MERN Stack Developer": [
        "html", "css", "javascript", "react", "node.js", "mongodb",
        "rest api", "git", "docker"
    ],
    "Backend Developer": [
        "python", "sql", "django", "flask", "rest api", "git",
        "docker", "kubernetes", "aws"
    ],
    "Python Developer": [
        "python", "sql", "django", "flask", "git", "rest api", "docker"
    ],
    "Web Developer": [
        "html", "css", "javascript", "react", "git", "rest api"
    ],
    "DevOps Engineer": [
        "linux", "git", "docker", "kubernetes", "aws", "rest api",
        "python", "ci/cd"
    ],
    "Java Developer": [
        "java", "sql", "git", "rest api", "docker", "kubernetes"
    ],
    "Data Analyst": [
        "excel", "sql", "python", "pandas", "numpy", "power bi",
        "tableau", "data analysis"
    ],
    "Machine Learning Engineer": [
        "python", "pandas", "numpy", "machine learning", "tensorflow",
        "sql", "git", "docker", "aws"
    ],
}

# Learning resource + rough time estimate per skill.
# category: "course" | "project" | "certification"
SKILL_RESOURCES = {
    "html":            {"resource": "MDN Web Docs – HTML basics", "weeks": 1, "category": "course"},
    "css":             {"resource": "MDN Web Docs – CSS + a Flexbox/Grid practice project", "weeks": 1, "category": "course"},
    "javascript":      {"resource": "JavaScript.info + build 2-3 small DOM projects", "weeks": 3, "category": "course"},
    "react":           {"resource": "Official React docs tutorial + a CRUD project", "weeks": 3, "category": "project"},
    "node.js":         {"resource": "Node.js + Express crash course, build a REST API", "weeks": 2, "category": "project"},
    "sql":             {"resource": "SQL for Data Analysis (Mode/SQLZoo) + practice queries", "weeks": 2, "category": "course"},
    "mongodb":         {"resource": "MongoDB University free M001 course", "weeks": 1, "category": "certification"},
    "django":          {"resource": "Django official tutorial + build a small web app", "weeks": 3, "category": "project"},
    "flask":           {"resource": "Flask Mega-Tutorial (Miguel Grinberg)", "weeks": 2, "category": "course"},
    "git":             {"resource": "Git & GitHub basics, practice branching/PR workflow", "weeks": 1, "category": "course"},
    "docker":          {"resource": "Docker for beginners + containerize one of your projects", "weeks": 2, "category": "project"},
    "kubernetes":      {"resource": "Kubernetes basics (kubernetes.io tutorials)", "weeks": 3, "category": "course"},
    "aws":              {"resource": "AWS Cloud Practitioner path + free-tier hands-on labs", "weeks": 4, "category": "certification"},
    "machine learning": {"resource": "Andrew Ng's Machine Learning Specialization", "weeks": 6, "category": "course"},
    "data analysis":   {"resource": "Google Data Analytics Certificate", "weeks": 4, "category": "certification"},
    "pandas":          {"resource": "Kaggle's Pandas micro-course + a dataset project", "weeks": 2, "category": "project"},
    "numpy":           {"resource": "NumPy quickstart + practice exercises", "weeks": 1, "category": "course"},
    "tensorflow":      {"resource": "TensorFlow Developer Certificate track", "weeks": 5, "category": "certification"},
    "excel":           {"resource": "Excel for data analysis (formulas, pivot tables)", "weeks": 1, "category": "course"},
    "power bi":        {"resource": "Microsoft Power BI free learning path + a dashboard project", "weeks": 2, "category": "project"},
    "tableau":         {"resource": "Tableau Public tutorials + build a portfolio dashboard", "weeks": 2, "category": "project"},
    "rest api":        {"resource": "Build and consume a REST API end-to-end", "weeks": 2, "category": "project"},
    "linux":           {"resource": "Linux command line basics (Linux Journey)", "weeks": 1, "category": "course"},
    "streamlit":       {"resource": "Streamlit docs + rebuild a small dashboard", "weeks": 1, "category": "project"},
    "langchain":       {"resource": "LangChain docs + build a small RAG demo", "weeks": 2, "category": "project"},
    "java":            {"resource": "Java fundamentals + OOP practice problems", "weeks": 3, "category": "course"},
    "ci/cd":           {"resource": "GitHub Actions basics, set up a CI pipeline for a repo", "weeks": 2, "category": "project"},
    "python":          {"resource": "Python Crash Course / official Python tutorial + small scripts", "weeks": 2, "category": "course"},
}

DEFAULT_RESOURCE = {"resource": "Search for a well-reviewed beginner course on this topic", "weeks": 2, "category": "course"}

# Best-effort mapping of a skill to the closest official roadmap.sh guide.
# roadmap.sh doesn't have a dedicated page for every keyword (e.g. "pandas"),
# so anything not listed here falls back to a Google search scoped to roadmap.sh.
SKILL_ROADMAP_SH_URLS = {
    "python":            "https://roadmap.sh/python",
    "java":              "https://roadmap.sh/java",
    "javascript":        "https://roadmap.sh/javascript",
    "html":              "https://roadmap.sh/frontend",
    "css":               "https://roadmap.sh/frontend",
    "react":             "https://roadmap.sh/react",
    "node.js":           "https://roadmap.sh/nodejs",
    "git":               "https://roadmap.sh/git-github",
    "docker":            "https://roadmap.sh/docker",
    "kubernetes":        "https://roadmap.sh/kubernetes",
    "aws":               "https://roadmap.sh/aws",
    "linux":             "https://roadmap.sh/linux",
    "mongodb":           "https://roadmap.sh/mongodb",
    "rest api":          "https://roadmap.sh/api-design",
    "machine learning":  "https://roadmap.sh/ai-data-scientist",
    "tensorflow":        "https://roadmap.sh/ai-data-scientist",
    "data analysis":     "https://roadmap.sh/data-analyst",
    "langchain":         "https://roadmap.sh/ai-engineer",
    "ci/cd":             "https://roadmap.sh/devops",
    "sql":               "https://roadmap.sh/postgresql-dba",
}


def get_all_roles():
    return list(ROLE_SKILL_MAP.keys())


def get_resource_for_skill(skill):
    return SKILL_RESOURCES.get(skill.lower(), DEFAULT_RESOURCE)


def get_roadmap_url(skill):
    """Return a roadmap.sh URL for this skill, or a scoped Google-search fallback."""
    skill_lower = skill.lower()
    if skill_lower in SKILL_ROADMAP_SH_URLS:
        return SKILL_ROADMAP_SH_URLS[skill_lower]
    query = skill_lower.replace(" ", "+")
    return f"https://www.google.com/search?q={query}+roadmap+site:roadmap.sh"


# Detailed topic breakdown per skill, shown in the detail panel when a
# tree node is clicked. Each skill maps to a list of {heading, points}
# sections. Anything not listed falls back to DEFAULT_TOPICS.
TOPICS = {
    "python": [
        {"heading": "Core fundamentals", "points": [
            "Syntax, indentation, and code style (PEP8)",
            "Variables, data types, type casting",
            "Control flow: if/else, for, while loops",
            "Functions, arguments, return values, lambdas",
        ]},
        {"heading": "Built-in data structures", "points": [
            "Lists, tuples, sets, dictionaries",
            "List/dict/set comprehensions",
            "String manipulation and formatting",
        ]},
    ],
    "java": [
        {"heading": "Core fundamentals", "points": [
            "Syntax, variables, data types",
            "OOP: classes, objects, inheritance, interfaces",
            "Collections framework (List, Map, Set)",
            "Exception handling",
        ]},
    ],
    "javascript": [
        {"heading": "Core fundamentals", "points": [
            "Variables (let/const), data types, operators",
            "Functions, arrow functions, closures",
            "Promises, async/await",
            "DOM manipulation and events",
        ]},
    ],
    "html": [
        {"heading": "Fundamentals", "points": [
            "Semantic tags and document structure",
            "Forms and input validation",
            "Accessibility basics (alt text, ARIA)",
        ]},
    ],
    "css": [
        {"heading": "Fundamentals", "points": [
            "Box model, selectors, specificity",
            "Flexbox and Grid layout",
            "Responsive design and media queries",
        ]},
    ],
    "react": [
        {"heading": "Core concepts", "points": [
            "Components, JSX, props, state",
            "Hooks: useState, useEffect, custom hooks",
            "Conditional rendering, lists and keys",
            "Routing with React Router",
        ]},
    ],
    "node.js": [
        {"heading": "Core concepts", "points": [
            "Event loop, modules, npm",
            "Building REST APIs with Express",
            "Middleware and error handling",
            "Connecting to a database",
        ]},
    ],
    "sql": [
        {"heading": "Core concepts", "points": [
            "SELECT, WHERE, ORDER BY, GROUP BY",
            "Joins (inner, left, right, full)",
            "Subqueries and aggregate functions",
            "Indexes and query performance basics",
        ]},
    ],
    "mongodb": [
        {"heading": "Core concepts", "points": [
            "Documents, collections, schema design",
            "CRUD operations",
            "Aggregation pipeline basics",
        ]},
    ],
    "django": [
        {"heading": "Core concepts", "points": [
            "Models, views, templates (MVT)",
            "Django ORM and migrations",
            "Django REST Framework for APIs",
        ]},
    ],
    "flask": [
        {"heading": "Core concepts", "points": [
            "Routing and request handling",
            "Templates with Jinja2",
            "Building a simple REST API",
        ]},
    ],
    "git": [
        {"heading": "Core workflow", "points": [
            "init, add, commit, status, log",
            "Branching and merging",
            "Pull requests and code review workflow",
            "Resolving merge conflicts",
        ]},
    ],
    "docker": [
        {"heading": "Core concepts", "points": [
            "Images vs containers",
            "Writing a Dockerfile",
            "docker-compose for multi-container apps",
        ]},
    ],
    "kubernetes": [
        {"heading": "Core concepts", "points": [
            "Pods, deployments, services",
            "ConfigMaps and secrets",
            "Scaling and rolling updates",
        ]},
    ],
    "aws": [
        {"heading": "Core services", "points": [
            "EC2, S3, IAM basics",
            "Deploying a simple app",
            "Monitoring with CloudWatch",
        ]},
    ],
    "machine learning": [
        {"heading": "Machine learning fundamentals", "points": [
            "What ML is vs traditional programming",
            "Why ML works: pattern discovery from data",
            "ML vs statistics vs rule-based systems",
            "When not to use ML",
        ]},
        {"heading": "Types of machine learning", "points": [
            "Supervised learning",
            "Unsupervised learning",
            "Reinforcement learning (high-level)",
        ]},
    ],
    "tensorflow": [
        {"heading": "Core concepts", "points": [
            "Tensors and basic operations",
            "Building a simple neural network",
            "Training, evaluating, saving a model",
        ]},
    ],
    "data analysis": [
        {"heading": "Core concepts", "points": [
            "Data cleaning and preprocessing",
            "Descriptive statistics",
            "Visualizing trends and distributions",
        ]},
    ],
    "pandas": [
        {"heading": "Core concepts", "points": [
            "DataFrames and Series basics",
            "Filtering, grouping, merging data",
            "Handling missing data",
        ]},
    ],
    "numpy": [
        {"heading": "Core concepts", "points": [
            "Arrays and vectorized operations",
            "Indexing, slicing, broadcasting",
        ]},
    ],
    "excel": [
        {"heading": "Core concepts", "points": [
            "Formulas and functions",
            "Pivot tables",
            "Charts and conditional formatting",
        ]},
    ],
    "power bi": [
        {"heading": "Core concepts", "points": [
            "Connecting and shaping data (Power Query)",
            "Building visuals and dashboards",
            "DAX basics",
        ]},
    ],
    "tableau": [
        {"heading": "Core concepts", "points": [
            "Connecting data sources",
            "Building charts and dashboards",
            "Filters, parameters, calculated fields",
        ]},
    ],
    "rest api": [
        {"heading": "Core concepts", "points": [
            "HTTP methods and status codes",
            "Designing resource-based endpoints",
            "Authentication basics (API keys, tokens)",
        ]},
    ],
    "linux": [
        {"heading": "Core concepts", "points": [
            "Navigating the filesystem, permissions",
            "Common commands (grep, find, chmod)",
            "Process management basics",
        ]},
    ],
    "ci/cd": [
        {"heading": "Core concepts", "points": [
            "What CI/CD solves and why it matters",
            "Setting up a pipeline (e.g. GitHub Actions)",
            "Automated testing and deployment steps",
        ]},
    ],
}

DEFAULT_TOPICS = [
    {"heading": "Key topics", "points": [
        "Look up an official guide or docs for this topic",
        "Build one small practice project using it",
        "Review common interview questions on this skill",
    ]}
]


def get_topics(skill):
    return TOPICS.get(skill.lower(), DEFAULT_TOPICS)