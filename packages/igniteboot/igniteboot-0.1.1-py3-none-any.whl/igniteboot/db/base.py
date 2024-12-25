from abc import ABC, abstractmethod
from typing import Any, Tuple, Optional

class BaseDatabase(ABC):

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def execute(self, query: str, params: Tuple[Any, ...] = ()) -> Any:
        pass

    @abstractmethod
    def fetchall(self, query: str, params: Tuple[Any, ...] = ()) -> list:
        pass
