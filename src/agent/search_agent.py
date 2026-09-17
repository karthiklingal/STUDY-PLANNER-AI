"""
search_agent.py
----------------
Planning Agent Module.

Models study-scheduling as a search problem and solves it with a
greedy best-first strategy (a simplified A*): at each step, pick the
subject with the highest "urgency" score, where urgency balances how
close the deadline is against how difficult/long the subject is.

State        : tuple of subjects already scheduled
Actions      : "schedule subject X next"
Goal test    : all subjects scheduled
Heuristic    : urgency = difficulty / days_remaining
               (higher urgency = study sooner)
"""

from datetime import date, datetime
import heapq


def _days_until(deadline_str, today):
    deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
    return max((deadline - today).days, 1)  # avoid divide-by-zero


def plan_schedule(subjects, hours_per_day, today=None):
    """
    Produce an ordered, day-by-day study plan.

    Parameters
    ----------
    subjects : list[dict]
        Each item: {"name": str, "difficulty": int (1-5),
                     "hours_needed": float, "deadline": "YYYY-MM-DD"}
    hours_per_day : float
        Study hours available per day.
    today : date, optional
        Defaults to date.today().

    Returns
    -------
    list[dict] : plan entries, each
        {"day": int, "subject": str, "hours": float, "deadline": str}
    """
    if today is None:
        today = date.today()

    heap = []
    for s in subjects:
        days_left = _days_until(s["deadline"], today)
        urgency = s["difficulty"] / days_left
        heapq.heappush(heap, (-urgency, s["name"], s))

    ordered = [item[2] for item in sorted(heap)]

    plan = []
    day = 1
    hours_left_today = hours_per_day
    remaining = {s["name"]: s["hours_needed"] for s in subjects}

    while any(remaining[s["name"]] > 0 for s in subjects):
        progressed = False
        for s in ordered:
            name = s["name"]
            if remaining[name] <= 0:
                continue
            if hours_left_today <= 0:
                break
            chunk = min(hours_left_today, remaining[name])
            plan.append({
                "day": day,
                "subject": name,
                "hours": round(chunk, 2),
                "deadline": s["deadline"],
            })
            remaining[name] -= chunk
            hours_left_today -= chunk
            progressed = True
        day += 1
        hours_left_today = hours_per_day
        if not progressed and any(remaining[s["name"]] > 0 for s in subjects):
            break

    return plan


def print_plan(plan):
    print(f"{'Day':<5}{'Subject':<20}{'Hours':<8}{'Deadline'}")
    for entry in plan:
        print(f"{entry['day']:<5}{entry['subject']:<20}{entry['hours']:<8}{entry['deadline']}")


if __name__ == "__main__":
    demo_subjects = [
        {"name": "Digital_Logic", "difficulty": 3, "hours_needed": 6, "deadline": "2026-09-22"},
        {"name": "DSA", "difficulty": 4, "hours_needed": 8, "deadline": "2026-09-23"},
        {"name": "Discrete_Math", "difficulty": 3, "hours_needed": 5, "deadline": "2026-09-24"},
        {"name": "Logic", "difficulty": 2, "hours_needed": 4, "deadline": "2026-09-25"},
        {"name": "AI_ML", "difficulty": 5, "hours_needed": 10, "deadline": "2026-09-28"},
    ]
    plan = plan_schedule(demo_subjects, hours_per_day=3, today=date(2026, 9, 16))
    print_plan(plan)
