# api_utils/base.py
import urllib.parse
from typing import Any, Dict, Optional
import requests


class BaseApiClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            if not hasattr(cls._instance, 'base_url'):
                cls._instance._init_client(kwargs.get('base_url', "http://127.0.0.1:20001"))
        return cls._instance

    def _init_client(self, base_url: str):
        self.base_url = base_url.rstrip("/") + "/api/"

    def _make_url(self, endpoint: str) -> str:
        endpoint = endpoint.lstrip("/")
        return urllib.parse.urljoin(self.base_url, endpoint)

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        response.raise_for_status()
        data = response.json()
        success = data.get("code") == 200
        return {
            "success": success,
            "data": data.get("data", {}),
            "message": data.get("message", ""),
            "code": data.get("code"),
        }

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = self._make_url(endpoint)
        response = requests.get(url, params=params)
        return self._handle_response(response)

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = self._make_url(endpoint)
        response = requests.post(url, data=data)
        return self._handle_response(response)

    def post_json(self, endpoint: str, json=None) -> Dict[str, Any]:
        url = self._make_url(endpoint)
        response = requests.post(url, json=json)
        return self._handle_response(response)
