"""
sentiment.py
------------
Lightweight lexicon-based sentiment analyzer for student notes/feedback,
e.g. "I found this topic really confusing and I'm stressed about it."

A lexicon approach is used (rather than a downloaded pretrained model)
so the project runs fully offline with no external downloads -- a
deliberate design choice worth noting in the report's "design
decisions & rationale" section.
"""

import re

NEGATIVE_WORDS = {
    "confusing", "confused", "difficult", "hard", "stressed", "stress",
    "worried", "anxious", "struggle", "struggling", "fail", "failing",
    "overwhelmed", "behind", "panic", "afraid", "scared", "tough",
    "lost", "frustrated", "frustrating", "hate", "boring", "tired",
}

POSITIVE_WORDS = {
    "clear", "confident", "easy", "understood", "understand", "good",
    "great", "comfortable", "ready", "prepared", "strong", "enjoy",
    "enjoyed", "love", "interesting", "fun", "improved", "improving",
}

INTENSIFIERS = {"very", "really", "extremely", "so", "totally"}
NEGATORS = {"not", "no", "never", "n't"}


def _tokenize(text):
    return re.findall(r"[a-z']+", text.lower())


def analyze(text):
    """
    Returns {"sentiment": "positive"/"negative"/"neutral",
              "score": float, "flags": list[str]}
    Score ranges roughly from -1 (very negative) to +1 (very positive).
    """
    tokens = _tokenize(text)
    score = 0.0
    flags = []

    for i, tok in enumerate(tokens):
        weight = 1.0
        # simple negation: flip polarity if a negator appears just before
        negated = i > 0 and tokens[i - 1] in NEGATORS
        # simple intensifier boost
        if i > 0 and tokens[i - 1] in INTENSIFIERS:
            weight = 1.5

        if tok in NEGATIVE_WORDS:
            score += (-weight if not negated else weight)
            flags.append(tok)
        elif tok in POSITIVE_WORDS:
            score += (weight if not negated else -weight)

    if tokens:
        score = score / max(len(tokens), 1) * 5  # scale into a readable range
        score = max(-1.0, min(1.0, score))

    if score < -0.1:
        sentiment = "negative"
    elif score > 0.1:
        sentiment = "positive"
    else:
        sentiment = "neutral"

    return {"sentiment": sentiment, "score": round(score, 3), "flags": sorted(set(flags))}


if __name__ == "__main__":
    samples = [
        "I found this topic really confusing and I'm quite stressed about the exam.",
        "I feel confident and prepared, the concepts are clear now.",
        "It's fine, nothing special either way.",
        "I am not confused anymore, it's actually pretty clear now.",
    ]
    for s in samples:
        print(f"{s!r}\n  -> {analyze(s)}\n")
