"""
clustering.py
-------------
Groups students by learning pattern using K-Means, based on
attendance, study hours, and past marks. Useful to spot behavioural
groups like "consistent high performers" vs "at-risk/cramming".
"""

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

FEATURES = ["attendance_pct", "avg_study_hours_per_day", "past_marks_pct"]


def cluster_students(data_path, k=3, random_state=42):
    df = pd.read_csv(data_path)
    X = df[FEATURES]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = KMeans(n_clusters=k, random_state=random_state, n_init=10)
    labels = model.fit_predict(X_scaled)
    df["cluster"] = labels

    score = silhouette_score(X_scaled, labels) if k > 1 else None

    # Label clusters by their average past marks (low -> high)
    cluster_means = df.groupby("cluster")["past_marks_pct"].mean().sort_values()
    ordered_labels = ["struggling", "moderate", "consistent"][:k]
    rank_to_name = {rank: name for rank, name in zip(cluster_means.index, ordered_labels)}
    df["pattern"] = df["cluster"].map(rank_to_name)

    return {"data": df, "model": model, "scaler": scaler, "silhouette_score": score}


def find_best_k(data_path, k_range=range(2, 6)):
    """Helper to justify k via silhouette score (for the report)."""
    results = {}
    for k in k_range:
        r = cluster_students(data_path, k=k)
        results[k] = r["silhouette_score"]
    return results


if __name__ == "__main__":
    import os
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_students.csv")

    print("Silhouette scores by k (higher is better):")
    for k, score in find_best_k(data_path).items():
        print(f"  k={k}: {round(score, 3)}")

    result = cluster_students(data_path, k=3)
    print(f"\nChosen k=3, silhouette score = {round(result['silhouette_score'], 3)}")
    print(result["data"][["student_id", "subject", "past_marks_pct", "pattern"]])
