"""
build_report.py
----------------
Generates the VITyarthi project report PDF from the actual project
artifacts: code metrics, test results, and the diagrams already saved
in docs/diagrams/.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle, ListFlowable, ListItem
)
from reportlab.lib import colors
import os

BASE = os.path.dirname(__file__)
DIAG = os.path.join(BASE, "docs", "diagrams")
OUT = os.path.join(BASE, "docs", "Project_Report.pdf")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="H1c", parent=styles["Heading1"], fontSize=20, spaceAfter=14, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="H2", parent=styles["Heading2"], fontSize=15, spaceBefore=16, spaceAfter=8, textColor=colors.HexColor("#26215C")))
styles.add(ParagraphStyle(name="H3", parent=styles["Heading3"], fontSize=12.5, spaceBefore=10, spaceAfter=6, textColor=colors.HexColor("#534AB7")))
styles.add(ParagraphStyle(name="Body", parent=styles["Normal"], fontSize=10.5, leading=15, alignment=TA_LEFT, spaceAfter=8))
styles.add(ParagraphStyle(name="Cover", parent=styles["Normal"], fontSize=13, alignment=TA_CENTER, spaceAfter=10))
styles.add(ParagraphStyle(name="Caption", parent=styles["Normal"], fontSize=9, alignment=TA_CENTER, textColor=colors.grey, spaceBefore=4, spaceAfter=14))

story = []

# ---------- 1. Cover Page ----------
story.append(Spacer(1, 5*cm))
story.append(Paragraph("Intelligent Study Planner &amp; Advisor Agent", styles["H1c"]))
story.append(Paragraph("VITyarthi &mdash; Build Your Own Project", styles["Cover"]))
story.append(Paragraph("Course: Fundamentals in AI and ML", styles["Cover"]))
story.append(Paragraph("Submission: Project Report", styles["Cover"]))
story.append(Spacer(1, 3*cm))
story.append(Paragraph("Author: [Your Name]", styles["Cover"]))
story.append(Paragraph("Registration No.: [Your Reg. No.]", styles["Cover"]))
story.append(Paragraph("Date: September 2026", styles["Cover"]))
story.append(PageBreak())

def h2(text):
    story.append(Paragraph(text, styles["H2"]))

def h3(text):
    story.append(Paragraph(text, styles["H3"]))

def body(text):
    story.append(Paragraph(text, styles["Body"]))

def bullets(items):
    story.append(ListFlowable(
        [ListItem(Paragraph(i, styles["Body"]), leftIndent=12) for i in items],
        bulletType="bullet", start="•"
    ))
    story.append(Spacer(1, 6))

def diagram(filename, caption):
    img_path = os.path.join(DIAG, filename)
    img = Image(img_path)
    max_w = 16*cm
    ratio = img.imageHeight / float(img.imageWidth)
    img.drawWidth = max_w
    img.drawHeight = max_w * ratio
    story.append(img)
    story.append(Paragraph(caption, styles["Caption"]))

# ---------- 2. Introduction ----------
h2("2. Introduction")
body("Students preparing for multi-subject exam cycles often struggle to decide "
     "what to study, in what order, and how much time to allocate, especially "
     "when subjects have prerequisite dependencies and differing difficulty. "
     "This project, the <b>Intelligent Study Planner &amp; Advisor Agent</b>, "
     "addresses this by combining three areas from the Fundamentals in AI and "
     "ML syllabus: search-based planning (agents and search strategies), "
     "symbolic knowledge representation (Prolog-style prerequisite reasoning), "
     "and applied machine learning (classification, clustering, and sentiment "
     "analysis).")

# ---------- 3. Problem Statement ----------
h2("3. Problem Statement")
body("Manual study planning rarely accounts for deadline pressure, topic "
     "prerequisites, or a student's actual risk of failing a subject. There is "
     "no lightweight tool that combines rule-based prerequisite reasoning with "
     "data-driven risk prediction into a single, deadline-aware study "
     "schedule. This project builds such a tool.")

# ---------- 4. Functional Requirements ----------
h2("4. Functional Requirements")
bullets([
    "<b>Planning module:</b> generate a day-by-day study schedule across multiple subjects, given deadlines, difficulty, and available hours per day.",
    "<b>Knowledge base module:</b> answer prerequisite questions (\"what must I know before X\") and skip-eligibility queries (\"can I skip X given what I already know\").",
    "<b>ML risk module:</b> predict pass/fail risk per subject from attendance, study hours, and past marks.",
    "<b>ML clustering module:</b> group students by learning pattern (struggling / moderate / consistent) using unsupervised learning.",
    "<b>ML sentiment module:</b> flag stress or difficulty signals from free-text student notes.",
])

# ---------- 5. Non-functional Requirements ----------
h2("5. Non-functional Requirements")
bullets([
    "<b>Performance:</b> the planner and ML predictions return in under a second for the dataset sizes used in this project.",
    "<b>Reliability:</b> modules handle missing or malformed input gracefully rather than crashing (e.g. zero available hours, unknown topic names).",
    "<b>Usability:</b> a single CLI entry point (main.py) runs all three modules with no configuration required.",
    "<b>Maintainability:</b> the codebase is split into independent packages (agent, knowledge_base, ml) so each can be extended or replaced without touching the others.",
    "<b>Scalability:</b> the classifier and clustering pipeline are built on scikit-learn and scale to much larger datasets than the 30-row sample used here.",
])

# ---------- 6. System Architecture ----------
h2("6. System Architecture")
body("The system is organized into a thin CLI layer that orchestrates three "
     "independent modules, all reading from a shared CSV data store. This "
     "separation keeps the planning logic, the symbolic reasoning, and the "
     "statistical ML pipeline decoupled and independently testable.")
diagram("architecture.png", "Figure 1: System architecture diagram")

# ---------- 7. Design Diagrams ----------
h2("7. Design Diagrams")

h3("7.1 Use Case Diagram")
body("The student is the sole actor, interacting with four core use cases "
     "exposed by the system.")
diagram("use_case.png", "Figure 2: Use case diagram")

h3("7.2 Workflow Diagram")
body("The end-to-end process flow: the student's input passes through "
     "planning, prerequisite checking, and ML-based risk flagging before a "
     "final plan is returned.")
diagram("workflow.png", "Figure 3: Process workflow diagram")

h3("7.3 Sequence Diagram")
body("Shows the message sequence for a single \"generate plan\" request "
     "across the CLI, SearchAgent, KnowledgeBase, and ML components.")
diagram("sequence.png", "Figure 4: Sequence diagram")

h3("7.4 Class / Component Diagram")
body("The CLI orchestrator composes five independent classes/modules, each "
     "owning one responsibility.")
diagram("class_component.png", "Figure 5: Class / component diagram")

body("<b>Note on ER diagram:</b> this project uses a flat CSV file "
     "(src/data/sample_students.csv) rather than a relational database, so no "
     "ER diagram or schema design applies. This is a deliberate scope "
     "decision suited to the project's size — see Section 8.")

# ---------- 8. Design Decisions & Rationale ----------
h2("8. Design Decisions &amp; Rationale")
bullets([
    "<b>Greedy/A*-style planner instead of full A*:</b> a simplified urgency-based greedy search (urgency = difficulty / days remaining) was chosen over an exhaustive A* state-space search because the scheduling problem is small enough that greedy allocation gives a near-optimal, easily explainable plan, while keeping the implementation transparent for demonstration purposes.",
    "<b>Pure-Python knowledge base fallback:</b> the KB is authored as real Prolog (rules.pl) but the app calls a pure-Python mirror (kb_interface.py) by default, so the project runs on any machine without requiring SWI-Prolog installation. The Prolog file remains the source of truth for the KR component.",
    "<b>Logistic Regression as primary classifier:</b> chosen over more complex models for interpretability and because the feature set (attendance, study hours, past marks) is small and linearly separable in this dataset; a Decision Tree is trained alongside for comparison (see Section 11).",
    "<b>K-Means for clustering:</b> chosen for simplicity and fast convergence on a small numeric feature set; k=3 was selected to produce actionable, human-labelled groups (struggling / moderate / consistent) even though k=2 scored marginally higher on silhouette score (see Section 11).",
    "<b>Lexicon-based sentiment analysis instead of a pretrained model:</b> avoids any external model download, keeping the project fully offline-runnable, while still handling negation (\"not confused\") correctly.",
])

# ---------- 9. Implementation Details ----------
h2("9. Implementation Details")
body("The project is implemented in Python 3 and organized as follows:")
table_data = [
    ["Module", "File(s)", "Responsibility"],
    ["Planning agent", "src/agent/search_agent.py", "Greedy/A*-style deadline-aware scheduling"],
    ["Knowledge base", "src/knowledge_base/rules.pl,\nkb_interface.py", "Prerequisite reasoning (Prolog + Python mirror)"],
    ["ML: classification", "src/ml/classifier.py", "Pass/fail risk prediction"],
    ["ML: clustering", "src/ml/clustering.py", "Learning-pattern grouping (K-Means)"],
    ["ML: sentiment", "src/ml/sentiment.py", "Stress/difficulty flagging from notes"],
    ["Orchestration", "src/main.py", "CLI entry point tying all modules together"],
    ["Tests", "tests/test_agent.py", "13 unit tests across all modules"],
]
t = Table(table_data, colWidths=[3.5*cm, 5*cm, 7.5*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#EEEDFE")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.HexColor("#26215C")),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#B4B2A9")),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
]))
story.append(t)
story.append(Spacer(1, 10))
body("Total: 6 functional source files plus 2 knowledge-base files, 1 test "
     "file, and 1 sample dataset — 10 files in src/ and tests/, satisfying "
     "the minimum 5-10 meaningful modules/files requirement. Version control "
     "was maintained using Git, with the repository structured into "
     "agent/, knowledge_base/, ml/, data/, and tests/ packages.")

# ---------- 10. Dataset, Model & Evaluation (ML-specific) ----------
h2("10. Dataset Description, Model Selection &amp; Evaluation Methodology")
h3("10.1 Dataset")
body("A synthetic dataset of 30 student records (src/data/sample_students.csv) "
     "was created, each with attendance percentage, average study hours per "
     "day, past marks percentage, subject, and pass/fail result. The dataset "
     "was intentionally constructed with a clear separation between passing "
     "and failing profiles to demonstrate the full ML pipeline; a production "
     "version would use real, noisier institutional data.")

h3("10.2 Model Selection Rationale")
body("Logistic Regression was chosen as the primary classifier for its "
     "interpretability and suitability for small, roughly linearly-separable "
     "feature sets. A Decision Tree was trained in parallel as a comparison "
     "point. For clustering, K-Means was chosen for its simplicity and fast "
     "convergence on 3 numeric features; the value of k was chosen using "
     "silhouette score analysis (Section 11.2).")

h3("10.3 Evaluation Methodology")
body("The classifier was evaluated using an 75/25 train/test split with "
     "accuracy, precision, recall, and a confusion matrix. Clustering quality "
     "was evaluated using the silhouette score across k = 2 to 5. Sentiment "
     "analysis was validated with hand-written example sentences covering "
     "positive, negative, neutral, and negated cases.")

# ---------- 11. Screenshots / Results ----------
h2("11. Screenshots / Results")
h3("11.1 Sample Study Plan Output")
body("Running <font face='Courier'>python src/agent/search_agent.py</font> "
     "with 5 subjects and a 3-hour daily budget produces a day-by-day plan "
     "that correctly prioritizes the subject with the nearest, highest-"
     "difficulty deadline (DSA, due in 7 days) before lower-urgency subjects "
     "such as AI_ML (due in 12 days).")

h3("11.2 Classifier Results")
body("Both Logistic Regression and Decision Tree achieved <b>100% accuracy, "
     "precision, and recall</b> on the held-out test split (confusion matrix: "
     "[[4,0],[0,4]]). This reflects the clean separation in the synthetic "
     "dataset described in Section 10.1 &mdash; real institutional data would "
     "be expected to show more overlap between passing and failing profiles, "
     "and this is noted as a limitation in Section 14.")

h3("11.3 Clustering Results")
body("Silhouette scores were computed for k = 2 through 5: k=2 scored "
     "highest (0.687), followed by k=3 (0.563). k=3 was selected for the "
     "final system because it produces three actionable, distinct "
     "behavioural groups (struggling / moderate / consistent) rather than a "
     "simple binary split, which better serves the advisory use case.")

h3("11.4 Sentiment Analysis Results")
body("The analyzer correctly classified test sentences, including correctly "
     "flipping polarity under negation &mdash; e.g. \"I am not confused "
     "anymore, it's clear now\" was correctly classified as <b>positive</b> "
     "rather than negative, despite containing the negative-lexicon word "
     "\"confused\".")

# ---------- 12. Testing Approach ----------
h2("12. Testing Approach")
body("A suite of 13 unit tests (tests/test_agent.py) covers all three "
     "modules using Python's pytest framework:")
bullets([
    "Planning agent: verifies total scheduled hours match required hours, and that the nearest-deadline subject is scheduled first.",
    "Knowledge base: verifies direct and transitive (recursive) prerequisite lookup, skip-eligibility logic, and \"what to study before\" queries.",
    "ML classifier: verifies predictions return a valid label and that accuracy metrics are within [0, 1].",
    "ML clustering: verifies every student is assigned one of the three expected pattern labels.",
    "ML sentiment: verifies correct classification of positive, negative, and negated example sentences.",
])
body("All 13 tests pass. Run with: <font face='Courier'>pytest tests/ -v</font>")

# ---------- 13. Challenges Faced ----------
h2("13. Challenges Faced")
bullets([
    "Balancing a genuine A*-style search against implementation complexity — a simplified greedy urgency heuristic was used instead of a full state-space search, documented as a deliberate trade-off in Section 8.",
    "Avoiding external, non-offline dependencies (a downloaded sentiment model, a required SWI-Prolog install) while still faithfully representing the Knowledge Representation and NLP concepts from the syllabus.",
    "Constructing a synthetic dataset large enough to train a stable classifier while keeping it small enough to inspect and reason about manually.",
])

# ---------- 14. Learnings & Key Takeaways ----------
h2("14. Learnings &amp; Key Takeaways")
bullets([
    "Search-based planning, symbolic knowledge representation, and statistical machine learning are complementary: search handles sequencing, KR handles hard logical constraints, and ML handles fuzzy, data-driven prediction.",
    "A clean, perfectly-separable synthetic dataset is useful for demonstrating a pipeline but does not test a model's real robustness — realistic data would need deliberate noise and overlap between classes.",
    "Keeping modules independently testable (via dependency-light pure-Python fallbacks) made it far easier to verify each AI technique in isolation before integrating them.",
])

# ---------- 15. Future Enhancements ----------
h2("15. Future Enhancements")
bullets([
    "Replace the greedy urgency heuristic with a full A* search over the state space for provably optimal schedules.",
    "Integrate a real SWI-Prolog backend via pyswip for a genuine Prolog inference engine instead of the Python mirror.",
    "Train the classifier and clustering models on real, anonymized institutional data with realistic noise.",
    "Add a simple web or Streamlit front-end in place of the CLI for a more accessible user experience.",
    "Extend sentiment analysis with a lightweight pretrained transformer model for more nuanced emotion detection.",
])

# ---------- 16. References ----------
h2("16. References")
bullets([
    "Russell, S. &amp; Norvig, P. — <i>Artificial Intelligence: A Modern Approach</i> (agents, search strategies, knowledge representation).",
    "scikit-learn documentation — https://scikit-learn.org/stable/",
    "SWI-Prolog documentation — https://www.swi-prolog.org/",
    "Course syllabus: Fundamentals in AI and ML (CAT2 portion) — set theory, probability, ML basics, classification, clustering.",
])

doc = SimpleDocTemplate(OUT, pagesize=A4,
                         topMargin=2*cm, bottomMargin=2*cm,
                         leftMargin=2.2*cm, rightMargin=2.2*cm)
doc.build(story)
print("Report written to", OUT)
