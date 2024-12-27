import os
import time

import itables.options as opt
import pandas as pd
from IPython.display import display
from itables import show
from treelib import Tree

from imkernel.core import get_algorithm_by_path
from imkernel.utils.pf_utils import model_data_value, tree_to_df


def show_csv(file_name):
    df = pd.read_csv(file_name)
    opt.lengthMenu = [[10, 25, 50, -1], ["10行", "25行", "50行", "全部"]]
    opt.dom = "lftp"
    show(df)


def show_excel(file_name):
    df = pd.read_excel(file_name)
    show(
        df,
        dom="lftpB",
        searching=True,
        paging=True,
        pageLength=10,
        classes="display",
        buttons=[
            {
                "extend": "excel",
                "text": "导出Excel",
                "title": None,
                "filename": "导出数据",
                "messageTop": None,
            }
        ],
        lengthMenu=[
            [10, 25, 50, 100, -1],
            ["10行", "25行", "50行", "100行", "显示全部"],
        ],
    )


def run_method_old(sysname, method_name, method_id):
    # 首先检查原始列数

    method_df_raw = sysname.reset_index()

    # 筛选第二列等于method_name的行
    filtered_df = method_df_raw[method_df_raw.iloc[:, 1] == method_name]
    # 检查筛选结果
    if filtered_df.empty:
        raise ValueError(f"没有找到方法: {method_name}")

    method_df_raw = filtered_df
    # 获取第三行的值
    target_row = method_df_raw.iloc[2]

    # 找到匹配项的列索引
    # 我们可能需要跳过由reset_index产生的列
    original_cols_start = len(method_df_raw.columns) - len(sysname.columns)
    target_row = target_row.iloc[original_cols_start:]

    matching_cols = target_row[target_row == method_id].index

    if len(matching_cols) > 0:
        matching_col = method_df_raw.columns.get_loc(matching_cols[0])
        fourth_col = 3

        target_df = method_df_raw.iloc[:, [fourth_col, matching_col]]

        # 创建临时字典存储标签和数值
        temp_dict = {}
        excel_name = ""
        # 遍历第一列
        for idx, value in enumerate(target_df.iloc[:, 0]):
            if isinstance(value, str):
                if value.startswith("标签"):
                    num = value.split()[-1]  # 获取标签后面的数字
                    if "标签" + num not in temp_dict:
                        temp_dict["标签" + num] = {}
                    temp_dict["标签" + num]["label"] = target_df.iloc[idx, 1]
                elif value.startswith("数值"):
                    num = value.split()[-1]  # 获取数值后面的数字
                    if "标签" + num not in temp_dict:
                        temp_dict["标签" + num] = {}
                    temp_dict["标签" + num]["value"] = target_df.iloc[idx, 1]
                elif value == "文件地址":
                    excel_name = target_df.iloc[idx, 1]

        # 创建最终的字典，将标签值作为key，数值值作为value
        final_dict = {}
        for item in temp_dict.values():
            if "label" in item and "value" in item:
                label = item["label"]
                value = item["value"]
                if label and value:  # 确保标签和值都不为空
                    final_dict[label] = value

        # 将最终字典转换为DataFrame
        result_df = pd.DataFrame(list(final_dict.items()), columns=["标签", "数值"])
        if not excel_name:
            excel_name = method_id
        # 保存为Excel
        if not excel_name.endswith("xlsx"):
            excel_name = excel_name + ".xlsx"
        # 转换为绝对路径
        excel_path = os.path.abspath(excel_name)
        # 生成CSV路径 (替换扩展名)
        csv_path = excel_path.rsplit(".", 1)[0] + ".csv"

        result_df.to_excel(excel_path, index=False)
        result_df.to_csv(csv_path, index=False)
        print(f"运行 {method_name} 成功，生成到{excel_path}")
        return excel_path, csv_path
    else:
        raise Exception(f"找不到{method_id}")


def process_dataframe(df):
    grouped_data = {}

    for index, row in df.iterrows():
        column_name = row.iloc[0]
        row_name = row.iloc[1]
        value = row.iloc[2]

        if column_name not in grouped_data:
            grouped_data[column_name] = {}

        # 判断value类型
        if isinstance(value, list):
            # 如果是list，直接添加
            grouped_data[column_name][row_name] = value
        else:
            # 如果不是list，判断是否为空
            if pd.notna(value):
                grouped_data[column_name][row_name] = value

    return grouped_data


def run_method(method_df, method_name, method_id):
    """
    执行指定方法，并处理其输入和输出参数。

    Args:
        method_df (pandas.DataFrame): 包含方法信息的DataFrame。
        method_name (str): 要执行的方法的名称。
        method_id (str): 要执行的方法的唯一标识符。

    Returns:
        list: 方法执行后的结果列表。

    Raises:
        ValueError: 如果未找到指定方法或编号不唯一时抛出。
        Exception: 如果程序或编号不唯一，或输出结果数量与预期输出数量不匹配时抛出。
    """
    method_df_raw = method_df.reset_index()
    # 筛选第二列等于method_name的行
    filtered_df = method_df_raw[method_df_raw.iloc[:, 1] == method_name]
    if filtered_df.empty:
        raise ValueError(f"没有找到方法: {method_name}")
    # method_df_raw = filtered_df

    id_column = filtered_df.iloc[:, 4]  # 编号列
    layer_3_column = filtered_df.iloc[:, 2]  # 关键词列
    # 方法3：使用列表索引方法index()
    try:
        id_index = id_column[id_column == "编号"].index.tolist()
        program_name_index = layer_3_column[layer_3_column == "程序"].index.tolist()
        input_index = layer_3_column[layer_3_column == "输入特性"].index.tolist()
        output_index = layer_3_column[layer_3_column == "输出特性"].index.tolist()

        if len(program_name_index) != 1 or len(id_index) != 1:
            raise Exception("程序或编号不唯一")
        program_name_index = program_name_index[0]
    except Exception as e:
        print(f"未找到指定关键词 {e}")

    # 获取目标id列
    id_temp_row = method_df_raw.iloc[id_index[0]]
    # 找到等于method_id的列索引
    id_col_indx = id_temp_row[id_temp_row == method_id].index.tolist()
    if len(id_col_indx) != 1:
        raise Exception(f"{method_id}未找到或不唯一")
    id_col_indx = id_col_indx[0]

    result = {"method_name": None, "method_body": None, "input": {}, "output": {}}
    # method_body_full = method_df_raw.loc[program_name_index, prog6ram_name_index + 1]
    # 使用iloc - 通过位置索引
    program_str = method_df_raw.iloc[id_index[0], 3]  # 直接使用整数索引，而不是列表
    result["method_name"] = program_str.rsplit("\\", 1)[-1]  # 获取方法体
    result["method_body"] = program_str.rsplit("\\", 1)[0]  # 获取路径部分
    input_df = method_df_raw.loc[
        input_index, ["prop type", "prop variable", id_col_indx]
    ]
    result["input"] = process_dataframe(input_df)
    output_df = method_df_raw.loc[
        output_index, ["prop type", "prop variable", id_col_indx]
    ]
    result["output"] = process_dataframe(output_df)
    method_body = result["method_body"]
    method_name = result["method_name"]
    input = result["input"]
    output = result["output"]
    print(f"方法体：{method_body}，方法：{method_name}")
    print(f"输入参数：{input}")
    print(f"输出参数：{output}")

    print(f"尝试导入方法体")
    # 获取算法
    function = get_algorithm_by_path(method_body, method_name)
    if not function:
        raise Exception(f"未能导入{method_name}")
    print(f"成功导入算法: {method_name}")
    # 开始计时
    start_time = time.time()
    func_result = function(**input)

    # 结束计时
    end_time = time.time()

    # 计算耗时
    execution_time = end_time - start_time

    print(f"算法运行完毕，耗时：{execution_time:.4f}秒")
    format_result = []
    # 转换format_result为list
    if isinstance(func_result, tuple):
        format_result = list(func_result)
    elif isinstance(func_result, list):
        format_result = [func_result]
    else:
        format_result = [func_result]
    # print(f"格式化结果: {format_result} origin_type:{type(func_result)}type: {type(format_result)}")
    # # 检查结果数量与输出index数量是否匹配
    if len(format_result) != len(output_index):
        raise ValueError(
            f"输出结果数量({len(format_result)})与预期输出数量({len(output_index)})不匹配"
        )

    # 将结果写回原始DataFrame
    for idx, result_value in zip(output_index, format_result):
        # 如果结果是嵌套列表，转换为字符串
        if isinstance(result_value, (list, tuple)):
            result_value = str(result_value)

        # 获取method_df中对应的索引位置
        row_idx = method_df.index[idx]
        method_df.loc[row_idx, id_col_indx] = result_value

    print(f"已将结果写回DataFrame")
    return format_result


#
# def run_method_oldold(sysname, method_name, method_id):
#     """
#     方法运行
#     Args:
#         sysname:
#         method_name:
#         method_id:
#
#     Returns:
#
#     """
#     method_df_raw = sysname.reset_index()
#     # 筛选第二列等于method_name的行
#     filtered_df = method_df_raw[method_df_raw.iloc[:, 1] == method_name]
#     if filtered_df.empty:
#         raise ValueError(f"没有找到方法: {method_name}")
#     method_df_raw = filtered_df
#
#     id_column = method_df_raw.iloc[:, 4]  # 关键词列
#     layer_3_column = method_df_raw.iloc[:, 2]  # 关键词列
#     # 方法3：使用列表索引方法index()
#     try:
#         id_index = id_column[id_column == "编号"].index.tolist()
#         program_name_index = layer_3_column[layer_3_column == "程序名"].index.tolist()
#         program_file_index = layer_3_column[layer_3_column == "程序地址"].index.tolist()
#         name_index = layer_3_column[layer_3_column == "名称"].index.tolist()
#         input_index = layer_3_column[layer_3_column == "输入特性"].index.tolist()
#
#         output_index = layer_3_column[layer_3_column == "输出特性"].index.tolist()
#
#         if len(program_name_index) != 1 or len(program_file_index) != 1:
#             raise Exception("程序名或程序地址不唯一")
#         program_name_index = program_name_index[0]
#         program_file_index = program_file_index[0]
#     except Exception as e:
#         print(f"未找到指定关键词 {e}")
#     # 判断id是否存在
#     if len(id_index) != 1:
#         raise Exception("编号所在行未找到或不唯一")
#     # 获取目标id列
#     id_temp_row = method_df_raw.iloc[id_index[0]]
#     # 找到等于method_id的列索引
#     id_col_indx = id_temp_row[id_temp_row == method_id].index.tolist()
#     if len(id_col_indx) != 1:
#         raise Exception(f"{method_id}未找到或不唯一")
#     id_col_indx = id_col_indx[0]
#
#     result = {
#         'method_name': None,
#         'method_body': None,
#         'input': {},
#         'output': {}
#     }
#     result['method_name'] = method_df_raw.loc[program_name_index, id_col_indx]
#     result['method_body'] = method_df_raw.loc[program_file_index, id_col_indx]
#     input_df = method_df_raw.loc[input_index, ['prop name', 'prop variable', id_col_indx]]
#     result['input'] = process_dataframe(input_df)
#     output_df = method_df_raw.loc[output_index, ['prop name', 'prop variable', id_col_indx]]
#     result['output'] = process_dataframe(output_df)
#     method_body = result['method_body']
#     method_name = result['method_name']
#     input = result['input']
#     output = result['output']
#     print(f"方法体：{method_body}，方法：{method_name}")
#     print(f"输入参数：{input}")
#     print(f"输出参数：{output}")
#
#     print(f"尝试导入方法体")
#     # 获取算法
#     function = get_algorithm_by_path(method_body, method_name)
#     if not function:
#         raise Exception(f"未能导入{method_name}")
#     print(f"成功导入算法: {method_name}")
#     # 开始计时
#     start_time = time.time()
#     format_result = function(**input, **output)
#
#     # 结束计时
#     end_time = time.time()
#
#     # 计算耗时
#     execution_time = end_time - start_time
#     print(f"算法运行完毕，耗时：{execution_time:.4f}秒")
#     return format_result
#
#
# def run_method_1_old(sysname, method_name, method_id):
#     """
#     适配1维表单生成
#     Args:
#         sysname:
#         method_name:
#         method_id:
#
#     Returns:
#
#     """
#     method_df_raw = sysname.reset_index()
#     # 筛选第二列等于method_name的行
#     filtered_df = method_df_raw[method_df_raw.iloc[:, 1] == method_name]
#     if filtered_df.empty:
#         raise ValueError(f"没有找到方法: {method_name}")
#     method_df_raw = filtered_df
#     target_row = method_df_raw.iloc[2]
#     original_cols_start = len(method_df_raw.columns) - len(sysname.columns)
#     target_row = target_row.iloc[original_cols_start:]
#     matching_cols = target_row[target_row == method_id].index
#
#     if len(matching_cols) > 0:
#         matching_col = method_df_raw.columns.get_loc(matching_cols[0])
#
#         target_df = method_df_raw.iloc[:, [2, 3, matching_col]]
#         # 初始化结果字典
#         result = {
#             'method_name': None,
#             'method_body': None,
#             'input': {},
#             'output': {}
#         }
#
#         # 遍历DataFrame的每一行
#         for index, row in target_df.iterrows():
#             category = row.iloc[0]  # 第一列的值
#             key = row.iloc[1]  # 第二列的值（键）
#             value = row.iloc[2]  # 第三列的值（值）
#
#             # 处理程序名和程序地址
#             if category == '程序名':
#                 result['method_name'] = value
#             elif category == '程序地址':
#                 result['method_body'] = value.strip('r"') if value else None
#
#             # 处理输入参数
#             elif category == '输入':
#                 if value not in [None, 'None']:
#                     result['input'][key] = value
#
#             # 处理输出参数
#             elif category == '输出':
#                 if value not in [None, 'None']:
#                     result['output'][key] = value
#         method_body = result['method_body']
#         method_name = result['method_name']
#         input = result['input']
#         output = result['output']
#
#         print(f"方法体：{method_body}，方法：{method_name}")
#         print(f"输入参数：{input}")
#         print(f"输出参数：{output}")
#
#         print(f"尝试导入方法体")
#         # 获取算法
#         function = get_algorithm_by_path(method_body, method_name)
#         if not function:
#             raise Exception(f"未能导入{method_name}")
#         print(f"成功导入算法: {method_name}")
#         # 开始计时
#         start_time = time.time()
#         format_result = function(**input, **output)
#
#         # 结束计时
#         end_time = time.time()
#
#         # 计算耗时
#         execution_time = end_time - start_time
#         print(f"算法运行完毕，耗时：{execution_time:.4f}秒")
#         return format_result
#     else:
#         raise Exception(f"找不到{method_id}")
