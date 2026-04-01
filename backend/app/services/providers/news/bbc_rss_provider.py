from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree as ET

import httpx

from app.services.providers.news.base import NewsProvider


class BbcRssNewsProvider(NewsProvider):
    FEEDS = {
        "computer-science": ("BBC Technology", "https://feeds.bbci.co.uk/news/technology/rss.xml"),
        "business": ("BBC Business", "https://feeds.bbci.co.uk/news/business/rss.xml"),
        "politics": ("BBC Politics", "https://feeds.bbci.co.uk/news/politics/rss.xml"),
        "world": ("BBC World", "https://feeds.bbci.co.uk/news/world/rss.xml"),
        "science": ("BBC Health", "https://feeds.bbci.co.uk/news/health/rss.xml"),
    }

    def fetch(self) -> list[dict]:
        articles: list[dict] = []
        seen_urls: set[str] = set()
        with httpx.Client(timeout=15, follow_redirects=True) as client:
            for topic_slug, (source_name, url) in self.FEEDS.items():
                response = client.get(url)
                response.raise_for_status()
                root = ET.fromstring(response.text)
                for item in root.findall(".//item")[:8]:
                    link = (item.findtext("link") or "").strip()
                    title = (item.findtext("title") or "").strip()
                    description = (item.findtext("description") or "").strip()
                    if not link or not title or link in seen_urls:
                        continue
                    seen_urls.add(link)
                    articles.append(
                        {
                            "source_name": source_name,
                            "title": title,
                            "summary": self._clean_summary(description) or title,
                            "url": link,
                            "topic_slug": topic_slug,
                            "published_at": self._parse_date(item.findtext("pubDate")),
                            "credibility_score": 0.9,
                            "importance_score": self._estimate_importance(topic_slug, title, description),
                        }
                    )
        return articles

    def _clean_summary(self, raw: str) -> str:
        return " ".join(raw.replace("<![CDATA[", "").replace("]]>", "").split())

    def _parse_date(self, value: str | None) -> datetime:
        if not value:
            return datetime.now(timezone.utc).replace(tzinfo=None)
        parsed = parsedate_to_datetime(value)
        if parsed.tzinfo is not None:
            parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
        return parsed

    def _estimate_importance(self, topic_slug: str, title: str, summary: str) -> float:
        text = f"{title} {summary}".lower()
        score = 0.68
        if any(keyword in text for keyword in ["war", "crisis", "emergency", "attack", "earthquake", "election", "inflation", "summit"]):
            score += 0.18
        if topic_slug in {"world", "politics", "business"}:
            score += 0.05
        return min(score, 0.96)
