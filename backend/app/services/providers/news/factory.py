from app.core.config import settings
from app.services.providers.news.bbc_rss_provider import BbcRssNewsProvider
from app.services.providers.news.mock_provider import MockNewsProvider


def get_news_provider():
    if settings.live_rss_enabled:
        return BbcRssNewsProvider()
    return MockNewsProvider()
