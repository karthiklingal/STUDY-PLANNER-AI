"""
main.py
-------
CLI entry point tying together the three modules:
  1. agent.search_agent      -> generates a study plan (search)
  2. knowledge_base           -> prerequisite reasoning (KR / Prolog-style)
  3. ml (classifier/clustering/sentiment) -> risk prediction & insights
"""

import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))

from agent.search_agent import plan_schedule, print_plan
from knowledge_base.kb_interface import (
    query_prerequisites, all_prerequisites, can_skip, what_to_study_before
)
from ml.classifier import train_model, predict_risk
from ml.clustering import cluster_students
from ml.sentiment import analyze

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "sample_students.csv")


def demo_planning_agent():
    print("\n=== 1. Planning Agent: Study Schedule (Search) ===")
    subjects = [
        {"name": "Digital_Logic", "difficulty": 3, "hours_needed": 6, "deadline": "2026-09-22"},
        {"name": "DSA", "difficulty": 4, "hours_needed": 8, "deadline": "2026-09-23"},
        {"name": "Discrete_Math", "difficulty": 3, "hours_needed": 5, "deadline": "2026-09-24"},
        {"name": "Logic", "difficulty": 2, "hours_needed": 4, "deadline": "2026-09-25"},
        {"name": "AI_ML", "difficulty": 5, "hours_needed": 10, "deadline": "2026-09-28"},
    ]
    plan = plan_schedule(subjects, hours_per_day=3, today=date(2026, 9, 16))
    print_plan(plan)


def demo_knowledge_base():
    print("\n=== 2. Knowledge Base: Prerequisite Reasoning ===")
    topic = "sentiment_analysis"
    print(f"Direct prerequisites of '{topic}':", query_prerequisites(topic))
    print(f"All (recursive) prerequisites of '{topic}':", all_prerequisites(topic))
    known = ["machine_learning", "probability_theory", "linear_algebra"]
    print(f"Known topics: {known}")
    print(f"Can skip '{topic}'?", can_skip(topic, known))
    print(f"Still need before '{topic}':", what_to_study_before(topic, known))


def demo_ml_modules():
    print("\n=== 3. ML Module: Risk Classification ===")
    trained = train_model(DATA_PATH, model_type="logistic")
    print("Model accuracy on test split:", round(trained["metrics"]["accuracy"], 3))
    at_risk_student = {"attendance_pct": 50, "avg_study_hours_per_day": 0.8, "past_marks_pct": 40}
    print("Sample student:", at_risk_student)
    print("Prediction:", predict_risk(at_risk_student, trained))

    print("\n=== 3b. ML Module: Learning-Pattern Clustering ===")
    clustered = cluster_students(DATA_PATH, k=3)
    print("Silhouette score:", round(clustered["silhouette_score"], 3))
    print(clustered["data"][["student_id", "subject", "pattern"]].head(6).to_string(index=False))

    print("\n=== 3c. ML Module: Sentiment Analysis on Student Notes ===")
    note = "I found this topic really confusing and I'm stressed about the exam."
    print(f"Note: {note!r}")
    print("Analysis:", analyze(note))


def main():
    print("=" * 60)
    print("  Intelligent Study Planner & Advisor Agent")
    print("=" * 60)
    demo_planning_agent()
    demo_knowledge_base()
    demo_ml_modules()
    print("\nDone. Each module above can be called independently --")
    print("see src/agent, src/knowledge_base, and src/ml for details.")


if __name__ == "__main__":
    main()
