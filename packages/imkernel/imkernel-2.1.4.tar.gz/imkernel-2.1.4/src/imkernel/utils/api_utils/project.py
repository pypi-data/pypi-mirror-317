# api_utils/project.py
from typing import Dict, Any, Optional
from .base import BaseApiClient


class ProjectApi(BaseApiClient):
    def get_project_list(self) -> Dict[str, Any]:
        """获取项目列表"""
        return self.get("project/list")

    def create_project(self, name: str, project_id: int) -> Dict[str, Any]:
        """创建项目"""
        return self.post("project/create", {
            "name": name,
            "id": project_id
        })

    def delete_project(self, project_id: str) -> Dict[str, Any]:
        """删除项目"""
        return self.post("project/delete", {
            "project_id": project_id
        })

    def get_project_detail(self, project_id: Optional[int] = None, project_name: Optional[str] = None) -> Dict[str, Any]:
        """获取项目详情"""
        params = {}
        if project_id is not None:
            params['project_id'] = project_id
        if project_name is not None:
            params['project_name'] = project_name
        return self.get("project/detail", params)
