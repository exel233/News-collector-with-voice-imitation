from app.data.mock_articles import mock_articles
from app.services.providers.news.base import NewsProvider


class MockNewsProvider(NewsProvider):
    def fetch(self) -> list[dict]:
        return mock_articles()
