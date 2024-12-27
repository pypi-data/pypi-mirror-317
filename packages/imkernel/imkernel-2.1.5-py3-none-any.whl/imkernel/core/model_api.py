import treelib

from imkernel.utils import request_utils, id_generator


def trees(tree_id, include_self=True):
    endpoint = f"/api/pythonimkernelxh/trees/{tree_id}/{include_self}"
    response_data = request_utils.api_get(endpoint)
    if not response_data:
        raise Exception(f"未找到根节点为{tree_id}的树")
    return response_data


def delete_tree(tree_id):
    endpoint = f"/api/pythonimkernelxh/deletetree/{tree_id}"
    request_utils.api_post(endpoint, None)


def delete_node_data_ids(node_ids):
    endpoint = f"/api/treedata/deletenodeids"
    response_json = request_utils.api_post(endpoint, node_ids)
    return response_json


def add_node(id, tree_id, tag, node_type, parent_id):
    endpoint = "/api/pythonimkernelxh/addnode"
    node_json = {
        "id": id,
        "treeId": tree_id,
        "name": tag,
        "nodeType": node_type,
        "parentId": parent_id
    }
    response_json = request_utils.api_post(endpoint, node_json)
    if not response_json:
        return False
    return True


#
# def delete_node(id, tree_id, tag, node_type, parent_id):
#     endpoint = "/api/pythonimkernelxh/addnode"
#     node_json = {
#         "id": id,
#         "treeId": tree_id,
#         "name": tag,
#         "nodeType": node_type,
#         "parentId": parent_id
#     }
#     response_json = request_utils.api_post(endpoint, node_json)
#     if not response_json:
#         return False
#     return True


if __name__ == '__main__':
    # trees('609955664159494')
    a = add_node(20, 2, 2, 2, -1)
    print(a)
