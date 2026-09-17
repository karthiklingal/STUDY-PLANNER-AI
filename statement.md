# Problem Statement

Students juggling multiple subjects before exams often struggle to decide
**what to study, in what order, and how much time to allocate**, especially
when subjects have prerequisite dependencies and varying difficulty. Manual
planning is time-consuming and rarely accounts for a student's actual
learning pattern or risk of failing a subject.

This project builds an **Intelligent Study Planner & Advisor Agent** that
combines classical AI planning (search), symbolic reasoning (knowledge
representation / Prolog), and machine learning to generate a personalized,
prerequisite-aware study schedule and flag subjects at risk.

## Scope of the Project

- Covers a fixed set of subjects/topics (configurable) with associated
  prerequisites, difficulty levels, and deadlines.
- Generates a day-by-day study plan using search-based planning.
- Answers prerequisite/skip-eligibility queries via a knowledge base.
- Predicts pass/fail risk per subject using a trained classifier on
  attendance, study hours, and past marks.
- Clusters students/topics by learning pattern.
- Performs basic sentiment analysis on free-text study notes to flag
  difficulty/stress.
- Out of scope: real-time integration with college LMS/attendance
  systems, multi-user authentication, and mobile app delivery (CLI/simple
  UI only for this submission).

## Target Users

- Students preparing for multi-subject exams (e.g. CAT-style exam
  cycles) who want a structured, prerequisite-aware study plan.
- Can be adapted for tutors/mentors to spot at-risk students early.

## High-Level Features

1. **Study Plan Generation** — search-based agent produces an ordered,
   deadline-aware study schedule.
2. **Prerequisite Reasoning** — Prolog-based knowledge base answers
   "what must I know before X" and "can I skip X" queries.
3. **Risk Prediction** — ML classifier flags subjects where the student
   is at risk of failing, based on historical patterns.
4. **Learning-Pattern Insights** — clustering groups students/topics into
   behavioural categories to guide personalized recommendations.
5. **Sentiment-Based Flagging** — detects stress/difficulty signals from
   the student's own notes to prioritize support.
