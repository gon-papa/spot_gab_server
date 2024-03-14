from abc import ABC, abstractmethod


class BaseTempleteInterface(ABC):
    @abstractmethod
    def get_html_en(self, **kwargs: str) -> str:
        pass

    @abstractmethod
    def get_html_ja(self, **kwargs: str) -> str:
        pass
