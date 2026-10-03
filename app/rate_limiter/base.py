from abc import ABC, abstractmethod


class RateLimiter(ABC):

    @abstractmethod
    def is_allowed(self, client_id: str) -> bool:
        pass