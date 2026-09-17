# Intelligent Study Planner & Advisor Agent

An AI system that helps students plan study schedules, reason about topic
prerequisites, and get ML-driven insights into their exam readiness —
built for the **Fundamentals in AI and ML** course project.

## Overview

The project models study-scheduling as a **search problem** solved by a
planning agent, uses a **Prolog-style knowledge base** to reason about
topic prerequisites and skip-eligibility, and applies **machine learning**
(classification, clustering, sentiment analysis) to predict exam risk and
surface learning insights — covering agents & environments, search
strategies, knowledge representation, and core ML concepts in one system.

## Features

- **Planning Agent** — generates an optimal study order across subjects
  given deadlines, difficulty, and available hours per day (A* / greedy
  best-first search).
- **Knowledge Base (Prolog)** — encodes topic prerequisites and answers
  queries like *"Can I skip X if I already know Y?"* and *"What should I
  revise before Z?"*.
- **Risk Classifier** — predicts pass/fail risk per subject from
  attendance, study hours, and past marks (Logistic Regression / Decision
  Tree).
- **Learning-Pattern Clustering** — groups students/topics by study
  behaviour using K-Means (e.g. consistent vs. cramming vs. struggling).
- **Sentiment Analysis** — flags stress or difficulty from a student's
  self-reported notes ("I found this topic confusing").

## Technologies / Tools Used

- Python 3.10+
- scikit-learn (Logistic Regression, Decision Tree, K-Means)
- pandas, numpy (data handling)
- Custom lexicon-based sentiment analyzer (no external downloads needed)
- Prolog-style knowledge base (`rules.pl`) with a pure-Python interface
  (`kb_interface.py`) that mirrors it 1:1 — runs with no SWI-Prolog
  install required; `pyswip` support is included as an optional path
- pytest / unittest (testing)
- Git / GitHub (version control)

## Project Structure

```
study-planner-ai/
├── README.md
├── statement.md
├── requirements.txt
├── src/
│   ├── agent/              # Planning agent (search strategies)
│   │   └── search_agent.py
│   ├── knowledge_base/     # Prolog rules + Python interface
│   │   ├── rules.pl
│   │   └── kb_interface.py
│   ├── ml/                 # Classification, clustering, sentiment
│   │   ├── classifier.py
│   │   ├── clustering.py
│   │   └── sentiment.py
│   ├── data/
│   │   └── sample_students.csv
│   └── main.py              # CLI entry point
├── tests/
│   └── test_agent.py
└── docs/
    ├── diagrams/             # Architecture, UML, ER diagrams
    └── screenshots/
```

## Steps to Install & Run

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd study-planner-ai
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. (Optional, for real Prolog backend) Install SWI-Prolog and ensure
   `pyswip` can locate it. Otherwise the pure-Python fallback in
   `kb_interface.py` works out of the box.
4. Run the application:
   ```bash
   python src/main.py
   ```

## Instructions for Testing

Run the full test suite (13 tests covering the search agent, knowledge
base, and all three ML modules) with:

```bash
pytest tests/ -v
```

All 13 tests pass as of this submission.

## Screenshots

*(Add screenshots of the CLI/UI output, sample study plan, and
classifier results here once implemented.)*

## Author

Built as part of the VITyarthi "Build Your Own Project" submission for
Fundamentals in AI and ML.
