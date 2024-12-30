# api_utils/system.py
from typing import Dict, Any, Optional
from .base import BaseApiClient


class SystemApi(BaseApiClient):
    def get_system_detail(
            self,
            project_id: int,
            type_id: Optional[str] = None,
            identifier_id: Optional[str] = None,
            prop_id: Optional[str] = None,
            variable_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取系统模型详情"""
        params = {
            "project_id": project_id,
            "type_id": type_id,
            "identifier_id": identifier_id,
            "prop_id": prop_id,
            "variable_id": variable_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.get("system/detail", params)
