def normalize_scores(results):
    """
    Convert FAISS L2 distance → confidence score (0–1)
    """
    if not results:
        return results

    max_dist = max(r["score"] for r in results)
    min_dist = min(r["score"] for r in results)

    for r in results:
        if max_dist == min_dist:
            r["confidence"] = 1.0
        else:
            r["confidence"] = round(
                1 - ((r["score"] - min_dist) / (max_dist - min_dist)),
                3
            )

    return results

