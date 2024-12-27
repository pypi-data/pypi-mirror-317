import json

import pandas
import treelib
from treelib import Tree
import numpy as np
import pandas as pd


def find_node_by_tag(tree, tag):
    """通过节点的tag在树中查找"""
    for node in tree.all_nodes():
        if node.tag == tag:
            return node
    else:
        return None


def sys_add_branch_nodes(tree, node_name, names1, names2, names3):
    """为tree_sys添加分支节点"""
    node = find_node_by_tag(tree, node_name)
    node_child_num = len(tree.children(node.identifier))
    node_id = 'system ' if node.identifier == 'rootsystem' else node.identifier + '.'
    for i, name1 in enumerate(names1):
        id_1 = node_id + str(i + 1 + node_child_num)
        tree.create_node(name1, id_1, node.identifier)
        if names2:
            for j, name2 in enumerate(names2[i]):
                id_2 = node_id + str(i + 1 + node_child_num) + '.' + str(j + 1)
                tree.create_node(name2, id_2, id_1)
                if names3:
                    for k, name3 in enumerate(names3[i][j]):
                        id_3 = node_id + str(i + 1 + node_child_num) + '.' + str(j + 1) + '.' + str(k + 1)
                        tree.create_node(name3, id_3, id_2)


def tree_ele(dimension: str, root_ele: str, ele: str, eleid: str, eleprop: str, elevar: list, tree=None):
    """
    单元树，创建tree或向tree中添加分支
    :param dimension: person(人员), machine(机器), product(产品),
    :param root_ele: 根节点名称
    :param ele: 单元名（一级节点）
    :param eleid: 单元的名称（二级节点）
    :param eleprop: 单元的特性（二级节点）
    :param elevar: 单元的特性变量（三级节点）
    :param tree: 传入表示向tree中添加分支，不传入表示新建tree（可选）
    :return: 单元树tree
    """
    if dimension not in ['person', 'machine', 'product']:
        print('维度输入错误')
        return None
    root_name = root_ele + '_' + dimension
    if tree is None:
        tree = treelib.Tree()
        tree.create_node(root_name, root_name)  # 创建根节点

    node_child_num = len(tree.children(tree.all_nodes()[0].identifier))

    ele_idf = dimension + ' ' + str(node_child_num + 1)
    tree.create_node(ele, ele_idf, root_name)  # 创建单元名（一级节点）
    tree.create_node(eleid, dimension + 'id ' + str(node_child_num + 1), ele_idf)  # 创建单元的名称（二级节点）
    tree.create_node(eleprop, dimension + 'prop ' + str(node_child_num + 1), ele_idf)  # 创建单元的特性（二级节点）
    for i, var in enumerate(elevar):
        tree.create_node(var, dimension + 'var ' + str(node_child_num + 1) + '.' + str(i + 1),
                         dimension + 'prop ' + str(node_child_num + 1))  # 创建单元的特性变量（三级节点）
    return tree


def combine_sys_ele(system_tree, root_ele, person_tree=None, machine_tree=None, product_tree=None):
    """
    将单元树合并到系统树下的root_ele对应节点
    :param system_tree: 需要合并的系统树
    :param root_ele: 系统树下的指定节点tag
    :param person_tree: 人员单元树
    :param machine_tree: 机器单元树
    :param product_tree: 产品单元树
    :return: None
    """
    node = find_node_by_tag(system_tree, root_ele)
    if person_tree:
        system_tree.paste(node.identifier, person_tree, deep=False)
    if machine_tree:
        system_tree.paste(node.identifier, machine_tree, deep=False)
    if product_tree:
        system_tree.paste(node.identifier, product_tree, deep=False)


def create_tree(supname, name, subname=None, origin=None):
    """
    构建或合并树结构。
    该方法用于创建或合并一棵树，提供一个根节点（supname）、二级节点（name 列表），
    以及每个二级节点的子节点（subname 列表）。如果提供了 origin 树，则在该树的基础上进行合并；
    如果 supname 已经在 origin 树中，则合并新的节点；否则，创建一棵新的树。

    参数:
    supname (str): 根节点的名称。作为树的一级节点。
    name (list of list of str): 每个子列表代表 supname 的直接子节点的名称列表。
    subname (list of list of str, optional): 每个子列表表示对应 name 节点的子节点，默认为 None。
    origin (Tree, optional): 现有树对象。如果提供，将在此基础上进行节点合并。默认为 None。

    返回:
    Tree: 构建或合并后的树结构。如果 `supname` 不存在于 `origin` 中，则返回一棵新的树。
    如果 `origin` 不为空且包含 `supname`，则对原树进行修改并返回。

    逻辑:
    - 如果 origin 为空，或者 origin 中不包含 supname，创建一个新树，supname 作为根节点。
    - 遍历 name 列表：
        - 为每个子列表中的 name 创建子节点，如果节点不存在则添加到树中。
        - 如果提供了 subname 且对应的子列表存在，则为 name 的每个子节点添加子节点。
    """
    # 如果 origin 为空，或者 origin 中不包含 supname，创建新树
    if origin is None or not origin.contains(supname):
        tree = Tree()
        tree.create_node(supname, supname)  # 创建根节点
    else:
        # 如果 origin 存在并且包含 supname，则直接使用 origin 进行扩展
        tree = origin

    # 添加 name 节点和对应的 subname 节点
    for idx, node_list in enumerate(name):
        for node_name in node_list:
            # 检查 name 节点是否已存在于树中
            if not tree.contains(node_name):
                tree.create_node(node_name, node_name, parent=supname)  # 如果不存在则创建 name 节点

            # 如果 subname 不为 None，则添加子节点
            if subname is not None and idx < len(subname):
                for sub_node_name in subname[idx]:
                    # 检查子节点是否已存在于树中
                    if not tree.contains(sub_node_name):
                        tree.create_node(sub_node_name, sub_node_name, parent=node_name)  # 如果不存在则创建子节点

    return tree


def tree_to_json(tree: treelib.Tree) -> str:
    """将treelib的Tree对象转换为通用json对象
    Args:
        tree (treelib.Tree): 要转换的树对象
    Returns:
        str: 树结构的JSON字符串表示
    """

    def node_to_dict(node):
        """将树节点转换为字典格式。
        Args:
            node: 要转换的树节点
        Returns:
            dict: 包含节点信息的字典
        """
        children = tree.children(node.identifier)
        return {
            'id': node.identifier,
            'name': node.tag,
            'data': node.data,
            'children': [node_to_dict(child) for child in children]
        }

    root = tree.get_node(tree.root)
    return json.dumps(node_to_dict(root), ensure_ascii=False)


def element_data_value(df, dimension: str, root_ele: str, ele: str, eleid: str, elevar: list):
    """
    向传入的df中进行维度单元的输入操作
    :param df: 需要输入的df对象
    :param dimension: 维度 person(人员), machine(机器), product(产品),
    :param root_ele: 树的根节点名称，系统树中的项目名称
    :param ele: 单元树中的一级节点，df中的一级索引
    :param eleid: 二级节点'名称'的值
    :param elevar: 二级节点'特征'对应三级节点对应的值
    :return: None
    """
    # 列满需要添加新列之后进行插入，标记哪一列没有值
    tmp = len(df.columns) + 1  # 默认新一列
    # 查找是否有没有值的列
    for i, col in enumerate(df.columns):
        if df.loc[:, col].all():
            tmp = i  # i列没有值，可以进行插入
            break
    # 插值
    df.loc[(root_ele + '_' + dimension, ele, '名称'), [dimension + ' ' + str(tmp)]] = eleid
    for idx, var in zip(df.index.get_level_values(-1)[1:], elevar):
        df.loc[(root_ele + '_' + dimension, ele, '特性', idx), [dimension + ' ' + str(tmp)]] = var
