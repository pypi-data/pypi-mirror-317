# api_utils/node.py
from typing import Dict, Any, Optional, List
from .base import BaseApiClient


class NodeApi(BaseApiClient):
    def get_node_detail(
            self,
            project_id: str,
            id: Optional[str] = None,
            name: Optional[str] = None,
            type: Optional[str] = None
    ) -> Dict[str, Any]:
        """获取系统节点详情"""
        params = {
            "project_id": project_id,
            "id": id,
            "name": name,
            "type": type
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.get("node/detail", params)

    def add_node(self, system_add: Dict[str, Any]) -> Dict[str, Any]:
        """新增记录"""
        return self.post_json("node/add", system_add)

    def update_node(self, system_update: Dict[str, Any]) -> Dict[str, Any]:
        """修改记录"""
        return self.post_json("node/update", system_update)

    def delete_node(self, project_id: int, id: int) -> Dict[str, Any]:
        """删除记录"""
        return self.post_json("node/delete", {
            "project_id": project_id,
            "id": id
        })

    def batch_add_nodes(self, systems: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量新增记录"""
        return self.post_json("node/batch_add", json=systems)
