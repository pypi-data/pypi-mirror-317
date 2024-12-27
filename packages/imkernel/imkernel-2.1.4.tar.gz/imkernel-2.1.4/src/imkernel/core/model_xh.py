import os
import time
from venv import logger

import numpy as np
import pandas as pd
from treelib import Tree

from imkernel.core import get_algorithm_by_path
from imkernel.core.utils import remove_empty_members


def build_tree(supname, name, subname=None, sub_subname=None):
    """
    根据给定的树状数据结构，构建一棵树。

    参数:
    - supname: 根节点的名称
    - name: 二级节点的列表（每个子列表是一级节点的直接子节点）
    - subname: 三级节点的列表（可选）
    - sub_subname: 四级节点的列表（可选）

    返回:
    - tree: 构建完成的树
    """
    # 创建树并添加根节点，id和tag相同
    tree = Tree()
    tree.create_node(tag=supname, identifier=supname)

    # 遍历 name 列表并添加节点
    for idx, second_level_list in enumerate(name):
        # 创建二级节点，id为"根节点tag+二级节点tag"
        second_level_tag = second_level_list[0]
        second_level_id = f"{supname}@{second_level_tag}"
        tree.create_node(tag=second_level_tag, identifier=second_level_id, parent=supname)

        # 如果 subname 存在，则创建三级节点
        if subname:
            for third_level in subname[idx]:
                # 三级节点，id为"二级节点tag+三级节点tag"
                third_level_id = f"{second_level_tag}@{third_level}"
                tree.create_node(tag=third_level, identifier=third_level_id, parent=second_level_id)

                # 如果 sub_subname 存在，则创建四级节点
                if sub_subname:
                    for fourth_level in sub_subname[idx][subname[idx].index(third_level)]:
                        # 四级节点，id为"三级节点tag+四级节点tag"
                        fourth_level_id = f"{third_level}@{fourth_level}"
                        tree.create_node(tag=fourth_level, identifier=fourth_level_id, parent=third_level_id)

    return tree


# 方法：根据索引名称和列名添加值
def add_value(df, index_name, column_name, value):
    """
    根据索引名称和列名，为多级索引的 DataFrame 添加值。

    参数:
    df: pandas DataFrame，具有多级索引
    index_name: 要匹配的索引名称（针对 level_4）
    column_name: 要修改的列名
    value: 要添加的值
    """
    # 找到符合 index_name 的行，并在指定列中添加值
    df.loc[pd.IndexSlice[:, :, :, index_name], column_name] = value


# 将 MultiIndex DataFrame 转换为树的方法
def df_to_tree(df):
    # 创建根节点
    supname = "root"
    tree = Tree()
    tree.create_node(tag=supname, identifier=supname)

    # 遍历 DataFrame 的 MultiIndex
    for index, row in df.iterrows():
        current_parent = supname  # 从根节点开始
        for level, level_name in enumerate(index):
            # 跳过 None 或 NaN 的值
            if level_name is None or (isinstance(level_name, float) and np.isnan(level_name)):
                continue

            # 定义节点的 id 和 tag
            current_id = f"{current_parent}@{level_name}"
            if not tree.contains(current_id):
                tree.create_node(tag=level_name, identifier=current_id, parent=current_parent)
            current_parent = current_id  # 将当前节点设为下一级的父节点

        # 将行的所有值作为叶子节点添加
        for col, value in row.items():
            leaf_id = f"{current_parent}@{col}"
            if not tree.contains(leaf_id):
                tree.create_node(tag=f"{col}: {value}", identifier=leaf_id, parent=current_parent)

    return tree


def assign_results(element_df, element_idx, format_result):
    if not isinstance(format_result, (list, tuple)):
        format_result = [format_result]

    existing_output_cols = [col for col in element_df.columns if col.startswith('output')]
    existing_output_cols.sort()

    if not existing_output_cols:
        logger.error("DataFrame中没有output列")
        return element_df

    # 调整结果长度
    if len(format_result) > len(existing_output_cols):
        logger.warning(f"结果数量({len(format_result)})超过DataFrame的output列数({len(existing_output_cols)})，将截断多余的结果")
        format_result = format_result[:len(existing_output_cols)]
    elif len(format_result) < len(existing_output_cols):
        logger.warning(f"结果数量({len(format_result)})少于DataFrame的output列数({len(existing_output_cols)})，将用None补充")
        format_result = format_result + [None] * (len(existing_output_cols) - len(format_result))

    try:
        # 获取实际的索引位置
        index_position = element_df[element_idx].index[0]

        # 为每个列单独赋值
        for col, value in zip(existing_output_cols, format_result):
            element_df.at[index_position, col] = value

    except Exception as e:
        logger.error(f"赋值失败: {str(e)}")
        logger.error(f"DataFrame形状: {element_df.shape}")
        logger.error(f"选中的行数: {element_idx.sum()}")
        logger.error(f"现有output列: {existing_output_cols}")

    return element_df


def update_df_values(data_df, target_df, data_object, target_object, data_id, target_id):
    """
    更新DataFrame中的特定值

    Parameters:
    -----------
    data_df : DataFrame
        源数据框
    target_df : DataFrame
        目标数据框
    data_object : str
        源数据框中要匹配的object（如'型线'）
    target_object : str
        目标数据框中要匹配的object（如'型线生成_十一参数'）
    data_id : str
        源数据的编号（如'l00'）
    traget_id : str
        目标数据的编号（如'p00'）

    Returns:
    --------
    DataFrame
        更新后的目标数据框
    """

    # 切片函数
    def slice_multiindex_df(df, pattern):
        idx = df.index.get_level_values('object type').str.contains(pattern, na=False)
        return df[idx]

    # 对两个df分别切片
    df1_slice = slice_multiindex_df(data_df, pattern=data_object)
    df2_slice = slice_multiindex_df(target_df, pattern=target_object)

    # 找到要更新的列
    df = df1_slice
    column_location = df.loc[df.index.get_level_values('prop variable') == '编号'].isin([data_id]).idxmax(axis=1)[0]

    # 重设索引以进行更新
    df1_slice = df1_slice.reset_index()
    df2_slice = df2_slice.reset_index()
    df1_slice.set_index(['prop type', 'prop variable'], inplace=True)
    df2_slice.set_index(['prop type', 'prop variable'], inplace=True)

    # 检查索引是否唯一
    if not df1_slice.index.is_unique:
        raise ValueError("df1_slice索引在重置后仍然不是唯一的。请检查您的DataFrame中是否存在重复值。")
    if not df2_slice.index.is_unique:
        raise ValueError("df2_slice索引在重置后仍然不是唯一的。请检查您的DataFrame中是否存在重复值。")
    # 更新值
    df2_slice[column_location].update(df1_slice[column_location])
    # df2_slice[column_location]=df1_slice[column_location]

    # 恢复原始索引结构
    df1_slice.reset_index(inplace=True)
    df2_slice.reset_index(inplace=True)
    df2_slice.set_index(['layer 2', 'object type', 'layer 3', 'prop type', 'prop variable'], inplace=True)

    return df2_slice


def mapping_df_values(data_df, data_object, data_id, target_df, target_object, target_id, mapping_dict):
    """
    通过映射字典在两个DataFrame之间传递数据，支持多重索引

    参数:
    data_df: 源DataFrame
    target_df: 目标DataFrame
    mapping_dict: 字典，键为元组(level0, level1)，值为对应的数据源索引
    data_id: 源DataFrame中要传递的列名
    target_id: 目标DataFrame中要接收数据的列名

    返回:
    更新后的target_df副本
    """

    # 切片函数
    def slice_multiindex_df(df, pattern):
        idx = df.index.get_level_values('object type').str.contains(pattern, na=False)
        return df[idx]

    # 对两个df分别切片
    data_df = slice_multiindex_df(data_df, pattern=data_object)
    target_df = slice_multiindex_df(target_df, pattern=target_object)
    data_id = data_df.loc[data_df.index.get_level_values('prop variable') == '编号'].isin([data_id]).idxmax(axis=1)[0]
    target_id = target_df.loc[target_df.index.get_level_values('prop variable') == '编号'].isin([target_id]).idxmax(axis=1)[0]
    data_df = data_df.reset_index()
    target_df = target_df.reset_index()
    data_df.set_index(['prop type', 'prop variable'], inplace=True)
    target_df.set_index(['prop type', 'prop variable'], inplace=True)

    target_df_copy = target_df.copy()

    # 通过映射字典传递值
    for target_idx, data_idx in mapping_dict.items():
        # 确保target_idx是元组类型
        if not isinstance(target_idx, tuple):
            target_idx = (target_idx,)

        try:
            if data_idx in data_df.index:
                target_df_copy.loc[target_idx, target_id] = data_df.loc[data_idx, data_id]
        except KeyError:
            continue
    target_df_copy = target_df_copy.reset_index()
    target_df_copy.set_index(['layer 2', 'object type', 'layer 3', 'prop type', 'prop variable'], inplace=True)
    return target_df_copy
