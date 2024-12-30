from abc import ABC, abstractmethod


class ILogHelper(ABC):
    @abstractmethod
    def debug(self, tekst: str):
        pass

    @abstractmethod
    def info(self, tekst: str):
        pass

    @abstractmethod
    def warning(self, tekst: str):
        pass

    @abstractmethod
    def error(self, tekst: str, ex: Exception):
        pass

    @abstractmethod
    def critical(self, tekst: str, ex: Exception):
        pass
