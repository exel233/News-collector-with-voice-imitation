from datetime import datetime, timedelta


def mock_articles() -> list[dict]:
    now = datetime.utcnow()
    return [
        {
            "source_name": "Tech Ledger",
            "title": "Open-source AI tooling sees major enterprise adoption",
            "summary": "Enterprises are expanding deployments of open-source AI tooling for internal copilots and data workflows.",
            "url": "https://example.com/tech-1",
            "topic_slug": "computer-science",
            "published_at": now - timedelta(hours=2),
            "credibility_score": 0.82,
            "importance_score": 0.74,
        },
        {
            "source_name": "Chip Daily",
            "title": "New accelerator chips promise lower-cost inference at scale",
            "summary": "Vendors unveiled inference-focused accelerator chips aimed at reducing energy and cloud costs.",
            "url": "https://example.com/tech-2",
            "topic_slug": "computer-science",
            "published_at": now - timedelta(hours=4),
            "credibility_score": 0.80,
            "importance_score": 0.77,
        },
        {
            "source_name": "World Wire",
            "title": "Emergency summit called after regional conflict escalates",
            "summary": "Leaders are convening after a sudden escalation raised concerns about trade routes and civilian safety.",
            "url": "https://example.com/world-1",
            "topic_slug": "world",
            "published_at": now - timedelta(hours=1),
            "credibility_score": 0.89,
            "importance_score": 0.95,
        },
        {
            "source_name": "Policy Desk",
            "title": "Governments propose new AI procurement and safety reporting rules",
            "summary": "A new policy package would require additional disclosures for public-sector AI deployments.",
            "url": "https://example.com/politics-1",
            "topic_slug": "politics",
            "published_at": now - timedelta(hours=3),
            "credibility_score": 0.85,
            "importance_score": 0.81,
        },
        {
            "source_name": "Science Current",
            "title": "Researchers publish stronger battery recycling method",
            "summary": "A materials science team reports a process that could improve battery reuse economics.",
            "url": "https://example.com/science-1",
            "topic_slug": "science",
            "published_at": now - timedelta(hours=5),
            "credibility_score": 0.78,
            "importance_score": 0.68,
        },
        {
            "source_name": "Market Note",
            "title": "Global stocks swing after surprise inflation data",
            "summary": "Markets turned volatile as investors reassessed interest-rate expectations after fresh inflation figures.",
            "url": "https://example.com/business-1",
            "topic_slug": "business",
            "published_at": now - timedelta(hours=2, minutes=30),
            "credibility_score": 0.84,
            "importance_score": 0.88,
        },
    ]
