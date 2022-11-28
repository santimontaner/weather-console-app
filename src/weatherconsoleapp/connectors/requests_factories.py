from abc import ABC, abstractmethod
from typing import Optional
import logging
import requests

logger = logging.getLogger(__name__)

class WeatherConnectorTimeout(BaseException):
    """Exception thrown when connector times out.
    """

class BaseRequestsFactory(ABC):

    @abstractmethod
    def get(self, url: str, params: dict) -> dict:
        """GET requests against the resource specified in the `url` parameter.
        """

class RequestsFactory(ABC):

    def get(self, url: str, params: Optional[dict] = None) -> dict:
        if params is None:
            params = {}

        try:
            response = requests.get(url, params=params)
        except requests.exceptions.Timeout:
            logger.error("Server timeout", exc_info=True)
            raise WeatherConnectorTimeout("AccuweatherApiConnector timed out.")
        logger.info("Response status code: %s %s", response.status_code, response.reason)
        return response.json()

