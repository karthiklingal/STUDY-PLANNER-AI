"""
kb_interface.py
----------------
Python interface to the knowledge base described in rules.pl.

Two backends are supported:
  1. Real Prolog via `pyswip` (if SWI-Prolog is installed) -- use
     query_prolog() for that.
  2. A pure-Python fallback that mirrors rules.pl exactly, so the
     project runs even without SWI-Prolog installed. This is the
     default used by the rest of the app.
"""

# --- Facts mirrored from rules.pl -----------------------------------
PREREQUISITES = {
    "machine_learning": ["probability_theory", "linear_algebra"],
    "classification": ["machine_learning"],
    "clustering": ["machine_learning"],
    "sentiment_analysis": ["classification"],
    "search_strategies": ["agents_and_environments"],
    "knowledge_representation": ["propositional_logic"],
}

DIFFICULTY = {
    "probability_theory": "medium",
    "linear_algebra": "medium",
    "agents_and_environments": "easy",
    "search_strategies": "medium",
    "propositional_logic": "medium",
    "knowledge_representation": "hard",
    "machine_learning": "hard",
    "classification": "hard",
    "clustering": "hard",
    "sentiment_analysis": "hard",
}


def query_prerequisites(topic):
    """Direct prerequisites of a topic (one level)."""
    return PREREQUISITES.get(topic, [])


def all_prerequisites(topic, _seen=None):
    """Recursively resolve every prerequisite (transitive closure)."""
    if _seen is None:
        _seen = set()
    for p in PREREQUISITES.get(topic, []):
        if p not in _seen:
            _seen.add(p)
            all_prerequisites(p, _seen)
    return sorted(_seen)


def can_skip(topic, known_topics):
    """True if every prerequisite of `topic` is already in known_topics."""
    required = set(all_prerequisites(topic))
    return required.issubset(set(known_topics))


def what_to_study_before(topic, known_topics):
    """Prerequisites still missing, in a sensible study order."""
    required = all_prerequisites(topic)
    return [t for t in required if t not in set(known_topics)]


def difficulty_of(topic):
    return DIFFICULTY.get(topic, "unknown")


# --- Optional real-Prolog backend ------------------------------------
def query_prolog(query_str, rules_path="src/knowledge_base/rules.pl"):
    """
    Run a raw query against the actual Prolog file using pyswip.
    Requires SWI-Prolog installed and `pip install pyswip`.
    Example: query_prolog("prerequisite(machine_learning, X)")
    """
    from pyswip import Prolog  # imported lazily; optional dependency
    prolog = Prolog()
    prolog.consult(rules_path)
    return list(prolog.query(query_str))


if __name__ == "__main__":
    print("Prerequisites of 'classification':", query_prerequisites("classification"))
    print("All (recursive) prerequisites of 'sentiment_analysis':",
          all_prerequisites("sentiment_analysis"))
    print("Can skip 'machine_learning' knowing [probability_theory, linear_algebra]?",
          can_skip("machine_learning", ["probability_theory", "linear_algebra"]))
    print("Still need before 'sentiment_analysis' knowing ['machine_learning']:",
          what_to_study_before("sentiment_analysis", ["machine_learning"]))
