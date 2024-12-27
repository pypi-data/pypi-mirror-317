# api_utils/client.py
from .project import ProjectApi
from .system import SystemApi
from .node import NodeApi


class ApiClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            if not hasattr(cls._instance, 'initialized'):
                base_url = kwargs.get('base_url', "http://127.0.0.1:20001")
                cls._instance.project = ProjectApi(base_url=base_url)
                cls._instance.system = SystemApi(base_url=base_url)
                cls._instance.node = NodeApi(base_url=base_url)
                cls._instance.initialized = True
        return cls._instance
