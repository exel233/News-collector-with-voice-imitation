from abc import ABC, abstractmethod


class NewsProvider(ABC):
    @abstractmethod
    def fetch(self) -> list[dict]:
        raise NotImplementedError
