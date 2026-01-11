from collections import Counter, defaultdict

def analyze_trends(papers):
    yearly_topics = defaultdict(list)

    for p in papers:
        yearly_topics[p.year].extend(p.keywords)

    trends = {
        year: Counter(kws).most_common(5)
        for year, kws in yearly_topics.items()
    }
    return trends

