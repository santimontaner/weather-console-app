from abc import ABC, abstractmethod
from typing import Optional
import requests

class BaseRequestsFactory(ABC):

    @abstractmethod
    def get(self, url: str, params: dict) -> dict:
        """GET requests against the resource specified in the `url` parameter.
        """

class RequestsFactory(ABC):

    def get(self, url: str, params: Optional[dict] = None) -> dict:
        if params is None:
            params = {}
        return requests.get(url, params=params)
