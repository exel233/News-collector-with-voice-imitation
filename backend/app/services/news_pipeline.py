import hashlib
import math
from collections import defaultdict
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.models import NewsEvent, SourceArticle, Topic, User
from app.services.providers.news.factory import get_news_provider


def _normalize_hash(title: str) -> str:
    cleaned = " ".join(title.lower().split())
    return hashlib.sha256(cleaned.encode("utf-8")).hexdigest()


def _build_why_it_matters(topic_slug: str) -> str:
    topic_map = {
        "computer-science": "This matters because it could shift product roadmaps, developer tooling, or AI deployment costs.",
        "politics": "This matters because policy changes can quickly affect regulation, procurement, and public trust.",
        "business": "This matters because market shifts can ripple into hiring, investment, and consumer demand.",
        "science": "This matters because early research wins often shape longer-term technology and public outcomes.",
        "world": "This matters because global instability can affect public safety, supply chains, and policy responses.",
    }
    return topic_map.get(topic_slug, "This matters because it could influence broader public and business decisions.")


def _calculate_recency(published_at: datetime) -> float:
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    hours_old = max((now - published_at).total_seconds() / 3600, 0.1)
    return max(0.1, min(1.0, 1 / math.log(hours_old + 2)))


def ingest_articles(db: Session) -> list[SourceArticle]:
    created: list[SourceArticle] = []
    provider = get_news_provider()
    try:
        fetched_articles = provider.fetch()
    except Exception:
        fetched_articles = []

    if not fetched_articles and settings.mock_news_mode:
        from app.services.providers.news.mock_provider import MockNewsProvider

        fetched_articles = MockNewsProvider().fetch()

    for article in fetched_articles:
        existing = db.query(SourceArticle).filter(SourceArticle.url == article["url"]).first()
        if existing:
            created.append(existing)
            continue
        record = SourceArticle(
            **article,
            normalized_hash=_normalize_hash(article["title"]),
            metadata_json={},
        )
        db.add(record)
        created.append(record)
    db.commit()
    return created


def cluster_articles(db: Session) -> list[NewsEvent]:
    has_live_articles = db.query(SourceArticle).filter(~SourceArticle.url.like("https://example.com/%")).count() > 0
    article_query = db.query(SourceArticle)
    if has_live_articles:
        article_query = article_query.filter(~SourceArticle.url.like("https://example.com/%"))
    articles = article_query.order_by(SourceArticle.published_at.desc()).all()
    db.query(NewsEvent).delete()
    db.flush()
    clusters: dict[str, list[SourceArticle]] = defaultdict(list)
    for article in articles:
        clusters[article.normalized_hash[:24]].append(article)

    events: list[NewsEvent] = []
    for cluster_key, grouped in clusters.items():
        newest = sorted(grouped, key=lambda item: item.published_at, reverse=True)[0]
        event = NewsEvent(cluster_key=cluster_key)
        db.add(event)
        event.title = newest.title
        event.topic_slug = newest.topic_slug
        event.summary = newest.summary
        event.why_it_matters = _build_why_it_matters(newest.topic_slug)
        event.source_count = len({item.source_name for item in grouped})
        event.global_importance = sum(item.importance_score for item in grouped) / len(grouped)
        event.recency_score = _calculate_recency(newest.published_at)
        event.novelty_score = 1 / (1 + len(grouped) / 3)
        event.metadata_json = {
            "article_urls": [item.url for item in grouped],
            "sources": sorted({item.source_name for item in grouped}),
        }
        events.append(event)
    db.commit()
    return events


def get_topic_relevance(user: User, topic_slug: str) -> float:
    weights = {pref.topic.slug: pref.priority_weight for pref in user.topic_preferences}
    return weights.get(topic_slug, 0.15)


def rank_events_for_user(db: Session, user: User) -> list[dict]:
    cluster_articles(db)
    selected_topics = {pref.topic.slug for pref in user.topic_preferences}
    ranked = []
    for event in db.query(NewsEvent).order_by(NewsEvent.created_at.desc()).all():
        relevance = get_topic_relevance(user, event.topic_slug)
        diversity = min(event.source_count / 3, 1.0)
        score = (
            settings.ranking_topic_weight * relevance
            + settings.ranking_importance_weight * event.global_importance
            + settings.ranking_recency_weight * event.recency_score
            + settings.ranking_source_diversity_weight * diversity
            + settings.ranking_novelty_weight * event.novelty_score
        )
        if event.global_importance >= 0.93:
            score += 0.15
        ranked.append(
            {
                "event": event,
                "score": round(score, 4),
                "is_focus": event.topic_slug in selected_topics,
                "relevance": relevance,
            }
        )
    ranked.sort(key=lambda item: item["score"], reverse=True)
    return ranked


def get_available_topics(db: Session) -> list[Topic]:
    return db.query(Topic).order_by(Topic.label.asc()).all()
