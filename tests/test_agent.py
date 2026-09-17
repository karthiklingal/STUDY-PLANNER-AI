"""
test_agent.py
-------------
Unit tests for the search agent, knowledge base, and ML modules.
Run with: pytest tests/
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from datetime import date
from agent.search_agent import plan_schedule
from knowledge_base.kb_interface import (
    query_prerequisites, all_prerequisites, can_skip, what_to_study_before
)
from ml.classifier import train_model, predict_risk
from ml.clustering import cluster_students
from ml.sentiment import analyze

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "src", "data", "sample_students.csv")


# --- Planning agent ---
def test_plan_schedule_covers_all_hours():
    subjects = [{"name": "A", "difficulty": 3, "hours_needed": 5, "deadline": "2026-12-31"}]
    plan = plan_schedule(subjects, hours_per_day=2, today=date(2026, 1, 1))
    total_hours = sum(p["hours"] for p in plan)
    assert total_hours == 5


def test_plan_schedule_prioritizes_nearest_deadline():
    subjects = [
        {"name": "Urgent", "difficulty": 3, "hours_needed": 2, "deadline": "2026-01-05"},
        {"name": "Later", "difficulty": 3, "hours_needed": 2, "deadline": "2026-06-01"},
    ]
    plan = plan_schedule(subjects, hours_per_day=2, today=date(2026, 1, 1))
    assert plan[0]["subject"] == "Urgent"


# --- Knowledge base ---
def test_prerequisites_lookup():
    assert "probability_theory" in query_prerequisites("machine_learning")


def test_all_prerequisites_transitive():
    prereqs = all_prerequisites("sentiment_analysis")
    assert "machine_learning" in prereqs
    assert "probability_theory" in prereqs


def test_can_skip_true():
    assert can_skip("machine_learning", ["probability_theory", "linear_algebra"])


def test_can_skip_false():
    assert not can_skip("machine_learning", ["probability_theory"])


def test_what_to_study_before():
    missing = what_to_study_before("classification", ["probability_theory"])
    assert "machine_learning" in missing


# --- ML: classifier ---
def test_classifier_predicts_valid_label():
    trained = train_model(DATA_PATH, model_type="logistic")
    sample = {"attendance_pct": 90, "avg_study_hours_per_day": 3.0, "past_marks_pct": 85}
    result = predict_risk(sample, trained)
    assert result["prediction"] in ("Pass", "Fail")
    assert result["risk"] in ("low", "high")


def test_classifier_metrics_present():
    trained = train_model(DATA_PATH, model_type="decision_tree")
    assert 0.0 <= trained["metrics"]["accuracy"] <= 1.0


# --- ML: clustering ---
def test_clustering_assigns_pattern_labels():
    result = cluster_students(DATA_PATH, k=3)
    assert set(result["data"]["pattern"].unique()).issubset(
        {"struggling", "moderate", "consistent"}
    )


# --- ML: sentiment ---
def test_sentiment_negative():
    result = analyze("This topic is confusing and I am stressed.")
    assert result["sentiment"] == "negative"


def test_sentiment_positive():
    result = analyze("I feel confident and prepared for this.")
    assert result["sentiment"] == "positive"


def test_sentiment_negation_flips_polarity():
    result = analyze("I am not confused anymore, it's clear now.")
    assert result["sentiment"] == "positive"
