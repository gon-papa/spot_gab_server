from abc import ABC, abstractmethod

class BaseTempleteInterface(ABC):
    @abstractmethod
    def get_html(self, **kwargs: str) -> str:
        pass