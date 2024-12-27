import datetime

import pandas as pd
import requests
import treelib
from loguru import logger
from treelib import Tree

from imkernel.core import model_api
from imkernel.utils import id_generator, pf_utils, request_utils, xh_utils
from imkernel.utils.id_generator import idgen
from imkernel.utils.pf_utils import model_data_value, tree_to_df

LAYER_1 = "layer_1"
MODEL_NAME = "model_name"
LAYER_2 = "layer_2"
OBJECT_NAME = "object_name"
LAYER_3 = "layer_3"
PROP_NAME = "prop_name"
PROP_VARIABLE = "prop_variable"


def get_data_structure(id=None, node_type=None, data=None):
    data = {"id": id, "node_type": node_type, "data": data}
    return data


def tree_to_list(tree):
    """
    将treelib树转换为符合IM规则的list，同时生成雪花ID避免冲突
    Args:
        tree:

    Returns:

    """
    # 深度与类型的映射字典
    depth_type_map = {
        1: "layer_1",
        2: "model_name",
        3: "layer_2",
        4: "object_name",
        5: "layer_3",
        6: "prop_name",
        7: "prop_variable",
    }

    result = []
    # 用于存储原始id到新id的映射
    id_mapping = {}

    def traverse(node_id, tree_id):
        node = tree.get_node(node_id)
        depth = tree.depth(node)

        # 为当前节点生成新id
        new_id = idgen.next_id()
        id_mapping[node.identifier] = new_id

        # 获取父节点的新id
        parent_node = tree.parent(node.identifier)
        new_parent_id = id_mapping.get(parent_node.identifier, 0) if parent_node else 0

        # 创建节点字典
        node_dict = {
            "id": new_id,
            "parentId": new_parent_id,
            "name": node.tag,
            "treeId": node.identifier,  # 使用原始treelib node的id
            "nodeType": depth_type_map.get(depth + 1, "None"),
        }
        result.append(node_dict)

        # 递归遍历子节点
        for child in tree.children(node_id):
            traverse(child.identifier, tree_id)

    # 从根节点开始遍历
    traverse(tree.root, 1)

    return result


def list_to_tree(json_list):
    """
    将符合IM规则的list转换回treelib树，并在节点data中添加snow_id和nodeType
    Args:
        json_list: list of dict, 包含id, parentId, name, treeId, nodeType的字典列表

    Returns:
        Tree: treelib树对象
    """
    tree = Tree()

    # 首先找到根节点（parentId为0的节点）
    root_node = next((node for node in json_list if node["parentId"] == 0), None)
    if not root_node:
        raise ValueError("No root node found in the list")

    # 创建一个映射表，用于快速查找父节点
    nodes_by_id = {node["id"]: node for node in json_list}

    # 用于记录已处理的节点
    processed_nodes = set()

    def add_node_and_children(node):
        if node["id"] in processed_nodes:
            return

        # 获取节点信息
        node_id = node["treeId"]  # 使用原始的treeId作为节点标识符
        parent_id = node["parentId"]
        node_name = node["name"]
        snow_id = node["id"]  # 获取snow_id
        node_type = node["nodeType"]  # 获取nodeType

        # 如果是根节点
        if parent_id == 0:
            tree.create_node(
                tag=node_name,
                identifier=node_id,
                data={"snow_id": snow_id, "node_type": node_type},
            )
        else:
            # 获取父节点的treeId
            parent_node = nodes_by_id[parent_id]
            parent_tree_id = parent_node["treeId"]
            # 创建当前节点，包含snow_id和nodeType
            tree.create_node(
                tag=node_name,
                identifier=node_id,
                parent=parent_tree_id,
                data={"snow_id": snow_id, "node_type": node_type},
            )

        processed_nodes.add(node["id"])

        # 查找并添加所有子节点
        children = [n for n in json_list if n["parentId"] == node["id"]]
        for child in children:
            add_node_and_children(child)

    # 从根节点开始构建树
    add_node_and_children(root_node)

    return tree


def model_tree_to_list(tree, df):
    # 深度与类型的映射字典
    depth_type_map = {
        1: "model",
        2: "model_group",
        3: "model_dimension",
        4: "model_object",
        5: "model_object_id",
    }

    result = []
    id_mapping = {}

    def get_layer2_type(tag):
        if "method" in tag:
            return "model_method"
        elif "procedure" in tag:
            return "model_procedure"
        elif "product" in tag:
            return "model_product"
        else:
            return "未找到类型"

    def get_model_name(node):
        if node.data:
            return node.data.get("model_name", "")
        else:
            return ""

    def find_df_row(node):
        # 构建节点完整路径
        path = []
        current = node
        while current is not None:
            path.insert(0, current.tag)
            current = tree.parent(current.identifier)

        # 在DataFrame中查找匹配的行
        for idx, row in df.iterrows():
            idx_values = list(idx)

            # 检查路径是否匹配
            # 从后向前匹配，确保层级关系正确
            path_matches = True
            path_len = len(path)
            idx_len = len(idx_values)

            # 从最后一个元素开始比较
            for i in range(1, min(path_len, idx_len) + 1):
                if path[-i] != idx_values[-i]:
                    path_matches = False
                    break

            if path_matches:
                # 获取所有数值列的值（跳过索引）
                numeric_cols = [col for col in df.columns if col.startswith("id ")]
                values = [row[col] for col in numeric_cols if pd.notna(row[col])]
                return values
        return []

    def traverse(node_id, tree_id):
        node = tree.get_node(node_id)
        depth = tree.depth(node)

        # 为当前节点生成新id
        new_id = idgen.next_id()
        id_mapping[node.identifier] = new_id

        # 获取父节点的新id
        parent_node = tree.parent(node.identifier)
        new_parent_id = id_mapping.get(parent_node.identifier, 0) if parent_node else 0

        # 获取节点数据
        node_data = find_df_row(node)

        # 创建节点字典
        node_dict = {
            "id": new_id,
            "parentId": new_parent_id,
            "name": node.tag,
            "treeId": node.identifier,
            "nodeType": (
                get_layer2_type(node.tag)
                if depth == 2
                else depth_type_map.get(depth + 1, "None")
            ),
            "modelName": get_model_name(node),
            "data": node_data,
        }
        result.append(node_dict)

        # 递归遍历子节点
        for child in tree.children(node_id):
            traverse(child.identifier, tree_id)

    # 从根节点开始遍历
    traverse(tree.root, 1)

    return result


def delete_tree(tree):
    if not isinstance(tree, treelib.Tree):
        raise Exception("参数类型不正确")
    tree_id = tree[0].data["snow_id"]

    response_json = model_api.delete_tree(tree_id)
    if response_json:
        print(f"删除成功,共删除{response_json}个节点")


def get_tree_list():
    root_id_list = []
    endpoint = "/api/pythonimkernelxh/getallnamebytype/layer_1"
    response_json = request_utils.api_get(endpoint)

    for item in response_json:
        print(f"TreeID: {item['id']}, TreeName: {item['name']}")


def get_tree(version_name=""):
    root_id_list = []
    name = "model-" + str(version_name)
    endpoint = "/api/pythonimkernelxh/getallnamebytype/layer_1"
    response_json = request_utils.api_get(endpoint)
    for item in response_json:
        if item["name"] == name:
            model_id = item["id"]
            root_id_list.append(model_id)

    if len(root_id_list) == 0:
        print("暂无数据")
        return
    tree_list = []

    for index, root_id in enumerate(root_id_list):
        endpoint = f"/api/pythonimkernelxh/getallchildnodes/{root_id}/true"
        tree_node_list = request_utils.api_get(endpoint)
        treelib_tree = list_to_tree(tree_node_list)
        tree_list.append(treelib_tree)
        return treelib_tree


def search_nodes(tree, node_type, tag, start_node=None):
    """
    在树中搜索特定类型和标签的节点

    参数:
        tree: treelib的Tree对象
        node_type: 要搜索的节点类型
        tag: 要搜索的标签名称
        start_node: 搜索的起始节点，如果为None则搜索整棵树

    返回:
        找到的节点，如果没找到返回None
    """
    nodes = []

    # 如果提供了起始节点，只搜索其子树
    if start_node:
        # 获取子树的所有节点
        children = tree.subtree(start_node.identifier).all_nodes()
        # 排除起始节点本身
        children = [
            node for node in children if node.identifier != start_node.identifier
        ]

        for node in children:
            if node.tag == tag:
                if node.data["node_type"] == node_type:
                    nodes.append(node)
    # 如果没有提供起始节点，搜索整棵树
    else:
        for node in tree.all_nodes():
            if node.tag == tag:
                if node.data["node_type"] == node_type:
                    nodes.append(node)

    if len(nodes) > 1:
        raise Exception(f"tag名称{tag}有多个结果{len(nodes)}")
    if len(nodes) == 0:
        return None
    return nodes[0]


def add_node(
    tree,
    model_name,
    layer_2: str,
    object_name: str = None,
    layer_3=None,
    prop_name=None,
    prop_variable=None,
    show_info=False,
):
    def show_create_node(node):
        if not show_info:
            return
        logger.info(f"新建node:{node.identifier} {node.tag} {node.data['node_type']}")

    def show_exist_node(node):
        if not show_info:
            return
        if not node:
            return
        logger.info(f"现存node:{node.identifier} {node.tag} {node.data['node_type']}")

    def create_node(tag, node_type, parent_node):
        identifier = id_generator.idgen.next_id()
        node = treelib.Node(
            tag=tag,
            identifier=identifier,
            data={"node_type": node_type, "snow_id": identifier},
        )
        response = model_api.add_node(
            node.identifier,
            node.identifier,
            tag,
            node.data["node_type"],
            parent_node.data["snow_id"],
        )
        if response:
            # 创建节点后立即添加到树中
            tree.add_node(node, parent=parent_node.identifier)
            return node
        else:
            raise Exception("API请求失败")

    dimension = layer_2
    name = object_name
    item = layer_3
    prop = prop_name
    variable = prop_variable
    if tree is None:
        raise Exception("请传入树")

    if model_name is None:
        raise Exception("请指定模型名称")
    model_name_node = search_nodes(tree, "model_name", model_name)
    if not model_name_node:
        raise Exception(f"没有找到模型{model_name}")

    if not layer_2:
        raise Exception("请指定layer_2层级的节点")

    # 查找layer_2节点是否存在
    layer_2_node = search_nodes(tree, "layer_2", layer_2, start_node=model_name_node)
    show_exist_node(layer_2_node)
    # 如果不存在，那么需要创建新的
    if not layer_2_node:
        layer_2_node = create_node(
            tag=dimension, node_type="layer_2", parent_node=model_name_node
        )
        show_create_node(layer_2_node)
    if not object_name:
        return
    # 查找object_name节点是否存在
    object_name_node = search_nodes(
        tree, "object_name", object_name, start_node=layer_2_node
    )
    show_exist_node(object_name_node)
    # 如果不存在，那么需要创建新的object_name
    if not object_name_node:
        object_name_node = create_node(
            tag=object_name, node_type="object_name", parent_node=layer_2_node
        )
        show_create_node(object_name_node)
    if not layer_3:
        return
    # 查找layer_3节点是否存在
    layer_3_node = search_nodes(tree, "layer_3", layer_3, start_node=object_name_node)
    show_exist_node(layer_3_node)
    # 如果不存在，那么需要创建新的layer_3
    if not layer_3_node:
        layer_3_node = create_node(
            tag=layer_3, node_type="layer_3", parent_node=object_name_node
        )
    if not prop_name:
        return
    # 查找prop_name节点是否存在
    prop_name_node = search_nodes(tree, "prop_name", prop_name, start_node=layer_3_node)
    show_exist_node(prop_name_node)
    # 如果不存在，那么需要创建新的prop_name
    if not prop_name_node:
        prop_name_node = create_node(
            tag=prop_name, node_type="prop_name", parent_node=layer_3_node
        )
        show_create_node(prop_name_node)

    if not prop_variable:
        return
    # 查找prop_variable节点是否存在
    prop_variable_node = search_nodes(
        tree, "prop_variable", prop_variable, start_node=prop_name_node
    )
    show_exist_node(prop_variable_node)
    # 如果不存在，那么需要创建新的prop_variable
    if not prop_variable_node:
        prop_variable_node = create_node(
            tag=prop_variable, node_type="prop_variable", parent_node=prop_name_node
        )
        show_create_node(prop_variable_node)
    return tree


def delete_node(
    tree,
    model_name,
    layer_2: str,
    object_name: str = None,
    layer_3=None,
    prop_name=None,
    prop_variable=None,
    show_info=False,
):
    def show_delete_node(node):
        if not show_info:
            return
        if not node:
            return
        logger.info(f"已删除节点:{node.identifier} tag:{node.tag} ")

    def show_not_found_node(node_type, node_tag, parent_path=None):
        if not show_info:
            return
        path_str = ""
        if parent_path:
            path_str = " -> ".join(
                [f"{node['type']}({node['tag']})" for node in parent_path]
            )
            path_str = f"路径: {path_str} -> "
        logger.info(f"未找到要删除的节点: {path_str}{node_tag}({node_type})")

    def delete_node_with_api(node):
        if not node:
            return False
        # 调用API删除节点及其子树
        response = model_api.delete_tree(node.identifier)
        if response:
            # API调用成功后从树中删除节点
            tree.remove_node(node.identifier)
            show_delete_node(node)
            return True
        else:
            raise Exception("API删除节点请求失败")

    if tree is None:
        raise Exception("请传入树")

    if model_name is None:
        raise Exception("请指定模型名称")
    # 初始化父节点路径
    parent_path = []

    # 查找model_name节点
    model_name_node = search_nodes(tree, "model_name", model_name)
    if not model_name_node:
        show_not_found_node("model_name", model_name)
        return
    parent_path.append({"type": "model_name", "tag": model_name})
    # if not layer_2:
    #     # 如果只指定到model_name层级，删除整个model_name节点及其子节点
    #     return delete_node_with_api(model_name_node)

    # 查找layer_2节点
    layer_2_node = search_nodes(tree, "layer_2", layer_2, start_node=model_name_node)
    if not layer_2_node:
        show_not_found_node("layer_2", layer_2, parent_path)
        return
    parent_path.append({"type": "layer_2", "tag": layer_2})

    if not object_name:
        return delete_node_with_api(layer_2_node)

    # 查找object_name节点
    object_name_node = search_nodes(
        tree, "object_name", object_name, start_node=layer_2_node
    )
    if not object_name_node:
        show_not_found_node("object_name", object_name, parent_path)
        return
    parent_path.append({"type": "object_name", "tag": object_name})

    if not layer_3:
        return delete_node_with_api(object_name_node)

    # 查找layer_3节点
    layer_3_node = search_nodes(tree, "layer_3", layer_3, start_node=object_name_node)
    if not layer_3_node:
        show_not_found_node("layer_3", layer_3, parent_path)
        return
    parent_path.append({"type": "layer_3", "tag": layer_3})

    if not prop_name:
        return delete_node_with_api(layer_3_node)

    # 查找prop_name节点a
    prop_name_node = search_nodes(tree, "prop_name", prop_name, start_node=layer_3_node)
    if not prop_name_node:
        show_not_found_node("prop_name", prop_name, parent_path)
        return
    parent_path.append({"type": "prop_name", "tag": prop_name})

    if not prop_variable:
        return delete_node_with_api(prop_name_node)

    # 查找prop_variable节点
    prop_variable_node = search_nodes(
        tree, "prop_variable", prop_variable, start_node=prop_name_node
    )
    if not prop_variable_node:
        show_not_found_node("prop_variable", prop_variable, parent_path)
        return

    # 删除prop_variable节点
    return delete_node_with_api(prop_variable_node)


def find_node_recursively(tree, current_node_id, target_tag):
    """
    递归地在树中查找指定的节点。

    :param tree: treelib.Tree 对象，表示树结构
    :param current_node_id: 当前节点的 ID
    :param target_tag: 目标节点的 tag 值
    :return: 找到的节点 ID 或 None
    """
    # 先检查当前节点是否匹配
    current_node = tree.get_node(current_node_id)
    if current_node.tag == target_tag:
        return current_node_id

    # 获取当前节点的所有子节点
    children = tree.children(current_node_id)

    for child in children:
        # 如果找到目标节点
        if child.tag == target_tag:
            return child.identifier

        # 如果当前节点的子树中可能存在目标节点，递归查找
        result = find_node_recursively(tree, child.identifier, target_tag)
        if result is not None:
            return result

    # 如果当前节点及其子树中未找到目标节点，返回 None
    return None


def save_system_old(tree: Tree, df: pd.DataFrame):
    """
    从 df 中获取符合要求的行，将每行数据组成一个 list，并赋值给 tree 中对应节点的 data 字段。

    :param tree: treelib.Tree 对象，表示树结构
    :param df: pandas.DataFrame 对象，包含多重索引的表格数据
    :param system_name: 系统名称，留空则按照时间戳
    """
    add_nodelist_endpoint = "/api/pythonimkernelxh/addnodelist"
    add_nodedata_endpoint = "/api/treedata/addlist"
    node_list = []
    tree_id = None

    # 遍历 df 的每一行
    for i in range(len(df)):
        # 判断当前行是否所有列都为空，如果是则跳过
        if all(pd.isnull(df.iloc[i])):
            continue

        # 将 NaN 替换为空字符串，然后将行转为列表
        row_data = df.iloc[i].fillna("").tolist()

        # 获取当前行的多重索引，并逐层递归查找对应的节点
        current_index = list(df.index[i])
        current_node_id = tree.root  # 从根节点开始

        for idx in current_index:
            # 先检查当前节点是否匹配
            current_node = tree.get_node(current_node_id)
            if current_node.tag == idx:
                continue

            # 不匹配则在子节点中查找
            current_node_id = find_node_recursively(tree, current_node_id, idx)
            if current_node_id is None:
                # 如果找不到目标节点，跳过该行
                break

        if current_node_id is not None:
            # 找到对应节点，更新其 data 字段
            node = tree.get_node(current_node_id)

            if node is not None:
                new_data = {"id": current_node_id, "data": row_data}
                node.data.update(new_data)  # 只增加或更新指定的键值对
            # 将数据添加到 node_list 中
            node_list.append(node.data)

    newtree = regenerate_model_tree(tree)

    # 构建结构数据列表
    nodelist = []
    for node in newtree.all_nodes():
        node_info = {
            "id": node.identifier,  # 节点ID
            "treeId": node.identifier,  # 树ID
            "name": node.tag,  # 节点名称
            "nodeType": node.data.get("node_type", "None"),  # 节点类型
            "parentId": (
                newtree.parent(node.identifier).identifier
                if newtree.parent(node.identifier)
                else 0
            ),  # 父节点ID
        }
        nodelist.append(node_info)
    response_json = request_utils.api_post(add_nodelist_endpoint, nodelist)
    print(f"保存系统模型结构成功！共添加 {response_json} 个节点")
    # 构建节点数据列表
    nodedatalist = []
    for node in newtree.all_nodes():
        data = node.data["data"]
        if data is not None:
            # 遍历data，把他转为string
            for k, v in enumerate(data):
                try:
                    data[k] = str(v)
                except Exception as e:
                    logger.error(f"转换失败： {e}")
        if data is None:
            data = ["", "", "", "", "", ""]
        node_data = {
            "nodeId": node.identifier,  # 节点ID
            "name": node.tag,  # 节点名称
            "key": {},  # key字段留空
            "value": {"data": data},  # value中放入节点的data数据
        }
        nodedatalist.append(node_data)
    add_data_list_response = request_utils.api_post(add_nodedata_endpoint, nodedatalist)
    if add_data_list_response:
        print(f"保存系统数据成功！共添加 {len(nodedatalist)} 条数据")


def save_system(
    tree: Tree, datadf: pd.DataFrame, system_name: str = None, show_info: bool = False
):
    """
    从 df 中获取符合要求的行，将每行数据组成一个 list，并赋值给 tree 中对应节点的 data 字段。
    :param tree: treelib.Tree 对象，表示树结构
    :param datadf: pandas.DataFrame 对象，包含多重索引的表格数据
    :param system_name: 系统名称，留空则按照时间戳
    :param show_info: 是否显示处理信息，默认False
    """

    def log_info(message):
        if show_info:
            print(message)

    if system_name is None:
        system_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    getallnamebytype_endpoint = "/api/pythonimkernelxh/getallnamebytype/"
    add_nodelist_endpoint = "/api/pythonimkernelxh/addnodelist"
    add_nodedata_endpoint = "/api/treedata/addlist"
    node_list = []
    tree_id = None
    db_system_name = "model-" + system_name
    db_tree_list = request_utils.api_get(getallnamebytype_endpoint + "layer_1")
    for db_tree in db_tree_list:
        if db_tree["name"] == db_system_name:
            tree_id = db_tree["id"]
            break

    # 遍历 df 的每一行
    uncatch = 0
    catch = 0
    db = 0
    for i in range(len(datadf)):
        current_index = list(datadf.index[i])
        log_info(f"正在处理第 {i} 行数据... {current_index}")
        # 判断当前行是否所有列都为空，如果是则跳过
        if all(pd.isnull(datadf.iloc[i])):
            log_info(f"第 {i} 行数据为空，跳过！")
            uncatch += 1
            continue

        catch += 1
        # 将 NaN 替换为空字符串，然后将行转为列表
        row_data = datadf.iloc[i].fillna("").tolist()

        # 获取当前行的多重索引，并逐层递归查找对应的节点
        current_node_id = tree.root  # 从根节点开始
        match_path = []  # 记录匹配路径
        match_failed = False

        for level, idx in enumerate(current_index):
            # 先检查当前节点是否匹配
            current_node = tree.get_node(current_node_id)
            match_path.append(f"Level {level}: 当前节点 '{current_node.tag}'")

            if current_node.tag == idx:
                continue

            # 不匹配则在子节点中查找
            match_path.append(f"  - 尝试匹配: '{idx}'")
            current_node_id = find_node_recursively(tree, current_node_id, idx)

            if current_node_id is None:
                match_failed = True
                match_path.append(f"  - 未找到匹配节点")
                break
            else:
                found_node = tree.get_node(current_node_id)
                match_path.append(f"  - 找到匹配节点: '{found_node.tag}'")

        # 只在匹配失败时输出匹配过程
        if match_failed:
            log_info(f"\n第 {i} 行匹配失败，索引: {current_index}")
            log_info("匹配过程:")
            log_info("\n".join(match_path))
            continue

        # 找到对应节点，更新其 data 字段
        node = tree.get_node(current_node_id)
        if node is not None:
            new_data = {"id": current_node_id, "data": row_data}
            node.data.update(new_data)  # 只增加或更新指定的键值对
            db += 1
            # 将数据添加到 node_list 中
            node_list.append(node.data)

    root_node = tree.get_node(tree.root)
    root_node.tag = db_system_name
    newtree = regenerate_model_tree(tree)
    log_info(f"catch{catch},uncatch{uncatch} db:{db}")
    if tree_id:
        log_info(f"系统模型已存在，进行增量更新！")
        db_tree = get_tree(system_name)
        map_tree(db_tree, newtree)
        try:
            delete_db_tree_node_data(db_tree)
            model_api.delete_tree(tree_id)
        except Exception as e:
            logger.error(f"删除tree失败：{e}，中断操作！")
            return

    nodelist = []
    for node in newtree.all_nodes():
        node_info = {
            "id": node.identifier,  # 节点ID
            "treeId": node.identifier,  # 树ID
            "name": node.tag,  # 节点名称
            "nodeType": node.data.get("node_type", "None"),  # 节点类型
            "parentId": (
                newtree.parent(node.identifier).identifier
                if newtree.parent(node.identifier)
                else 0
            ),  # 父节点ID
        }
        nodelist.append(node_info)
    response_json = request_utils.api_post(add_nodelist_endpoint, nodelist)
    print(f"保存系统模型结构成功！共添加 {response_json} 个节点")
    # 构建节点数据列表
    nodedatalist = []
    for node in newtree.all_nodes():
        data = node.data["data"]
        if data is not None:
            # 遍历data，把他转为string
            for k, v in enumerate(data):
                try:
                    data[k] = str(v)
                except Exception as e:
                    logger.error(f"转换失败： {e}")
        if data is None:
            data = ["", "", "", "", "", ""]
        node_data = {
            "nodeId": node.identifier,  # 节点ID
            "name": node.tag,  # 节点名称
            "key": {},  # key字段留空
            "value": {"data": data},  # value中放入节点的data数据
        }
        nodedatalist.append(node_data)
    add_data_list_response = request_utils.api_post(add_nodedata_endpoint, nodedatalist)
    if add_data_list_response:
        print(f"保存系统数据成功！共添加 {uncatch} 条数据")


def delete_db_tree_node_data(db_tree: treelib.Tree):
    id_list = [x.identifier for x in db_tree.all_nodes()]
    r = model_api.delete_node_data_ids(id_list)
    # if not r:
    #     raise Exception("删除data失败")


def map_tree(db_tree: treelib.Tree, new_tree: treelib.Tree):
    # 存储新旧ID的映射关系
    id_mapping = {}

    # 第一步：找到matching nodes并正确更新ID
    for db_node in db_tree.all_nodes():
        data = db_node.data
        node_type = data["node_type"]
        if node_type == "layer_1" or node_type == "model_name":
            for new_node in new_tree.all_nodes():
                if (
                    new_node.tag == db_node.tag
                    and new_node.data["node_type"] == node_type
                ):
                    old_id = new_node.identifier
                    new_tree.update_node(old_id, identifier=db_node.identifier)
                    id_mapping[old_id] = db_node.identifier
                    break

    # 第二步：更新所有节点的parent指向
    for node in new_tree.all_nodes():
        parent_id = node.predecessor(new_tree.identifier)
        if parent_id and parent_id in id_mapping:
            try:
                new_tree.move_node(node.identifier, id_mapping[parent_id])
            except Exception as e:
                print(
                    f"Failed to move node {node.identifier} to parent {id_mapping[parent_id]}: {str(e)}"
                )
                continue

    return True


def regenerate_model_tree(tree):
    # 创建新树
    new_tree = Tree()

    # 获取所有节点, 按层级排序
    nodes = tree.all_nodes()

    # 创建旧ID到新ID的映射
    id_mapping = {}

    # 第一遍遍历: 生成新ID并建立映射关系
    for node in nodes:
        old_id = node.identifier
        new_id = str(idgen.next_id())  # 转换为字符串，因为treelib的ID通常是字符串
        id_mapping[old_id] = new_id

    # 第二遍遍历: 重建树结构
    for node in nodes:
        old_id = node.identifier
        new_id = id_mapping[old_id]

        # 获取父节点ID
        parent = tree.parent(old_id)
        new_parent_id = id_mapping[parent.identifier] if parent else None

        # 如果是根节点，为tag添加时间戳
        if parent is None:
            new_tag = node.tag
            # timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            # new_tag = f"{node.tag}-{timestamp}"
        else:
            new_tag = node.tag

        # 复制节点数据并创建新节点
        new_tree.create_node(
            tag=new_tag, identifier=new_id, parent=new_parent_id, data=node.data
        )

    return new_tree


def save_model(tree, df, save_name):
    """
    保存模型到数据库
    Args:
        tree:
    """
    get_all_tree = "/api/pythonmodelnode/trees/0/true"
    all_tree = response_json = request_utils.api_get(get_all_tree)
    tree_id = [x["id"] for x in all_tree]

    for id in tree_id:
        delete_endpoint = f"/api/pythonmodelnode/deletetree/{id}"
        a = request_utils.api_post(delete_endpoint, None)

    endpoint = "/api/pythonmodelnode/addnodelist"

    node_list = model_tree_to_list(tree, df)
    node_list[0]["name"] = node_list[0]["name"] + save_name
    response_json = request_utils.api_post(endpoint, node_list)
    print(f"保存model成功！共添加{response_json}个节点")
    return response_json
