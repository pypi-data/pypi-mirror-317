import copy
import warnings

import pandas as pd
import treelib

from imkernel.utils import id_generator


# import id_generator
def get_data_structure(id=None, node_type=None, data=None):
    # def get_data_structure(id='None', node_type='None', data='None'):
    data = {'id': id,
            'node_type': node_type,
            'data': data}
    return data


def _level_list(names, lvl):
    """
    规范输入列表层数
    :param names: 需要规范的输入
    :param lvl: 最终列表的嵌套层数: 1, 2, 3
    :return: names 规范好的输入列表
    """
    if names and (lvl == 1 or lvl == 2 or lvl == 3) and not isinstance(names, list):
        names = [names]
    if names and (lvl == 2 or lvl == 3) and not isinstance(names[0], list):
        names = [names]
    if names and (lvl == 3) and not isinstance(names[0][0], list):
        names = [names]
    return names


def _tree_sub_node(n_tree, n_id, n_tag, data):
    """
    在树tree中n_id节点的子节点查找是否存在名为n_tag的节点
    :param n_tree: 原树
    :param n_id: 节点的id
    :param n_tag: 需要查找的子节点的tag
    :param data: 节点存储的数据
    """
    c_nodes = n_tree.children(n_id)  # 子节点b
    # 若已存在直接返回节点
    for c_node in c_nodes:
        if c_node.tag == n_tag:
            return c_node
    # 不存在则新建节点并返回
    else:
        return n_tree.create_node(tag=n_tag, identifier=id_generator.idgen.next_id(), parent=n_id, data=data)


def find_node_by_tag(tree, tag: str):
    """
    通过节点的tag在树中查找
    :param tree: 寻找的tree
    :param tag: 需要寻找的节点tag名称
    """
    for node in tree.all_nodes():
        if node.tag == tag:
            return node
    else:
        print(f'未找到 {tag} 节点。')
        return None


def tree_sys(layer_1, model_name=None) -> treelib.Tree or None:  # , sys=None, subsys=None
    """
    创建系统树
    :param layer_1: tree 传入tree表示向其中添加分支，传入str表示新建tree（根节点）
    :param model_name: supsys 总系统列表（一级节点）
    # :param sys: 系统列表（二级节点）
    # :param subsys: 子系统列表（三级节点）
    :return: tree(系统树)
    """
    tree = layer_1
    supsys = model_name
    # 没有树则新建
    if isinstance(tree, str):
        tree_name = tree
        tree = treelib.Tree()
        tree.create_node(tree_name, id_generator.idgen.next_id(), data=get_data_structure(node_type='layer_1'))  # 创建根节点
    if isinstance(tree, treelib.Tree):
        # 遍历三个名称列表进行节点添加
        if supsys:
            names1 = _level_list(supsys, 1)  # 规范列表层数
            for i, name1 in enumerate(names1):
                node1 = _tree_sub_node(tree, tree.root, name1, data=get_data_structure(node_type='model_name'))
                # if sys:
                #     names2 = _level_list(sys, 2)  # 规范列表层数
                #     if i >= len(names2):  # 如果子名称长度小于上一级名称则跳过
                #         continue
                #     for j, name2 in enumerate(names2[i]):
                #         node2 = _tree_sub_node(tree, node1.identifier, name2, "model")
                #         if subsys:
                #             names3 = _level_list(subsys, 3)  # 规范列表层数
                #             if j >= len(names3):  # 如果子名称长度小于上一级名称则跳过
                #                 continue
                #             for k, name3 in enumerate(names3[i][j]):
                #                 _tree_sub_node(tree, node2.identifier, name3, "subsystem")
    else:
        print(f'tree的类型错误，创建失败：{type(tree)}')
        return None
    return tree


# def tree_ele(tree, dimension: str, ele: str, eleid: str, eleprop: str,
#              elevar=None) -> treelib.Tree:
#     """
#     创建单元树
#     :param tree: 传入tree表示向其中添加分支，传入str表示新建tree（根节点）
#     :param dimension: person(人员), machine(机器), product(产品)
#     :param ele: 单元名（一级节点）
#     :param eleid: 单元的名称（二级节点）
#     :param eleprop: 单元的特性（二级节点）
#     :param elevar: 单元的特性变量（三级节点）
#     :return: tree（单元树）
#     """
#     # 没有树则新建
#     if isinstance(tree, str):
#         tree_name = f'{tree}_{dimension}'
#         tree = treelib.Tree()
#         tree.create_node(tree_name, id_generator.idgen.next_id(), data=dimension)  # 创建根节点
#     if isinstance(tree, treelib.Tree):
#         # 创建节点，已有则不新建，没有则新建
#         ele_node = _tree_sub_node(tree, tree.root, ele, f'{dimension}_name')  # ele（一级节点）
#         id_node = _tree_sub_node(tree, ele_node.identifier, eleid, f'{dimension}_id')  # 创建单元的名称（二级节点）
#         pr_node = _tree_sub_node(tree, ele_node.identifier, eleprop, f'{dimension}_prop')  # 创建单元的特性（二级节点）
#         elevar = _level_list(elevar, 1)  # 规范列表层数
#         for var in elevar:
#             var_node = _tree_sub_node(tree, pr_node.identifier, var, f'{dimension}_var')  # 特性的值名称（三级节点）
#     else:
#         print(f'tree的类型错误，创建失败：{type(tree)}')
#         return None
#     return tree


# def tree_method(tree, method_name: str,
#                 in_param=None, out_param=None,
#                 in_sub_param=None, out_sub_param=None) -> treelib.Tree:
#     """
#     创建方法树
#     :param tree: 传入tree表示向其中添加分支，传入str表示新建tree（根节点）
#     :param method_name: 方法名称（一级节点）
#     :param in_param: 方法输入参数（二级节点）
#     :param in_sub_param: 方法输入子参数（三级节点）
#     :param out_param: 方法输出参数（二级节点）
#     :param out_sub_param: 方法输出子参数（三级节点）
#     :return: tree（方法树）
#     """
#     # 没有树则新建
#     if isinstance(tree, str):
#         tree_name = f'{tree}_method'
#         tree = treelib.Tree()
#         tree.create_node(tree_name, id_generator.idgen.next_id(), data='method')  # 创建根节点
#     if isinstance(tree, treelib.Tree):
#         # 创建节点，已有则不新建，没有则新建
#         m_node = _tree_sub_node(tree, tree.root, method_name, 'method_name')  # 方法节点（一级节点）
#         # s_node = tree.create_node('状态操作', f'method_state_operate {m_num}', m_node.identifier)
#         # tree.create_node('状态', f'method_state {m_num}', s_node.identifier)
#         # tree.create_node('操作', f'method_operate {m_num}', s_node.identifier)
#         # 输入
#         i_node = _tree_sub_node(tree, m_node.identifier, "输入", 'method_in_param')  # 输入节点（二级节点）
#         in_param = _level_list(in_param, 1)  # 规范列表层数
#         for i, p1 in enumerate(in_param):
#             p1_node = _tree_sub_node(tree, i_node.identifier, p1, data='method_in_sub_param')  # 输入分类节点（三级节点）
#             if in_sub_param:
#                 in_params = _level_list(in_sub_param, 2)  # 规范列表层数
#                 if i >= len(in_params):
#                     continue
#                 for j, p2 in enumerate(in_params[i]):
#                     _tree_sub_node(tree, p1_node.identifier, p2, data='method_in_param_var')  # 输入值节点（四级节点）
#         # 输出
#         o_node = _tree_sub_node(tree, m_node.identifier, "输出", 'method_out_param')  # 输出节点（二级节点）
#         out_param = _level_list(out_param, 1)  # 规范列表层数
#         for i, p1 in enumerate(out_param):
#             p1_node = _tree_sub_node(tree, o_node.identifier, p1, data='method_out_sub_param')  # 输出分类节点（三级节点）
#             if out_sub_param:
#                 out_params = _level_list(out_sub_param, 2)  # 规范列表层数
#                 if i >= len(out_params):
#                     continue
#                 for j, p2 in enumerate(out_params[i]):
#                     _tree_sub_node(tree, p1_node.identifier, p2, data='method_out_param_var')  # 输出值节点（四级节点）
#     else:
#         print(f'tree的类型错误，创建失败：{type(tree)}')
#         return None
#     return tree


# def tree_procedure(tree, name: str, subname:str,
#                    prop=None, variable=None) -> treelib.Tree:
#     """
#     创建流程树
#     :param tree: 传入tree表示向其中添加分支，传入str表示新建tree（根节点）
#     :param name: 流程名称（一级节点）
#     :param subname: 子名称（二级节点）
#     :param prop: 特征名称 list（三级节点）
#     :param variable: 特征值 list（四级节点）
#     :return: tree（流程树）
#     """
#     if isinstance(tree, str):
#         tree_name = f'{tree}_procedure'
#         tree = treelib.Tree()
#         tree.create_node(tree_name, id_generator.idgen.next_id(), data='procedure')  # 创建根节点
#     if isinstance(tree, treelib.Tree):
#         # 创建节点，已有则不新建，没有则新建
#         p_node = _tree_sub_node(tree, tree.root, name, "procedure_name")  # 流程名称（一级节点）
#         s_node = _tree_sub_node(tree, p_node.identifier, subname, "procedure_sub")  # 流程子名称（二级节点）
#         props = _level_list(prop, 1)  # 规范列表层数
#         for i, prop in enumerate(props):
#             prop_node = _tree_sub_node(tree, s_node.identifier, prop, data='procedure_sub_param')  # 特性节点（三级节点）
#             if variable:
#                 variables = _level_list(variable, 2)  # 规范列表层数
#                 if i >= len(variables):
#                     continue
#                 for j, var in enumerate(variables[i]):
#                     _tree_sub_node(tree, prop_node.identifier, var, data='procedure_sub_var')  # 变量节点（四级节点）
#     else:
#         print(f'tree的类型错误，创建失败：{type(tree)}')
#         return None
#     return tree


def tree_dimension(layer_2: str, object_type: str, layer_3=None, prop_type=None, prop_variable=None,
                   tree=None) -> treelib.Tree or None:
    """
    创建维度子树
    :param layer_2: dimension 维度：person(人员), machine(机器), product(产品), method(方法), procedure(流程)
    :param object_type: name 名称（一级节点）
    :param layer_3: item 子名称 list（二级节点）
    :param prop_type: prop 特性名称 list（三级节点）
    :param prop_variable: variable 特性变量名称 list（四级节点）
    :param tree: 传入tree表示向其中添加分支，传入str表示新建tree（根节点）
    :return: tree（维度子树）
    """
    dimension = layer_2
    name = object_type
    item = layer_3
    prop = prop_type
    variable = prop_variable
    # if isinstance(tree, str):
    if tree is None:
        # tree_name = f"{tree}_{dimension}"
        tree = treelib.Tree()
        tree.create_node(dimension, id_generator.idgen.next_id(), data=get_data_structure(node_type='layer_2'))  # 创建根节点
    if isinstance(tree, treelib.Tree):
        # 创建固定需求节点
        name_node = _tree_sub_node(tree, tree.root, name, data=get_data_structure(node_type='object_name'))  # 名称（一级节点）
        # id_node = _tree_sub_node(tree, name_node.identifier, "编号", data=f"{dimension}_item")  # item 编号，即id
        # if dimension == "method":
        #     mt_node = _tree_sub_node(tree, name_node.identifier, "程序名", data=f"{dimension}_item")  # item 方法：程序名
        #     mt_node = _tree_sub_node(tree, name_node.identifier, "程序地址", data=f"{dimension}_item")  # item 方法：程序地址
        # if dimension == "procedure":
        #     st_node = _tree_sub_node(tree, name_node.identifier, "状态", data=f"{dimension}_item")  # item 流程：状态
        #     _tree_sub_node(tree, st_node.identifier, "状态", data=f"{dimension}_item")  # prop 状态：状态
        #     _tree_sub_node(tree, st_node.identifier, "起止时间", data=f"{dimension}_item")  # prop 状态：起止时间
        # 遍历三个名称列表进行节点添加
        if item:
            items = _level_list(item, 1)  # 规范列表层数
            for i, it in enumerate(items):
                item_node = _tree_sub_node(tree, name_node.identifier, it, data=get_data_structure(node_type='layer_3'))  # 子名称（二级节点）
                if prop:
                    props = _level_list(prop, 2)  # 规范列表层数
                    if i >= len(props):  # 如果子名称长度小于上一级名称则跳过
                        continue
                    for j, pr in enumerate(props[i]):
                        prop_node = _tree_sub_node(tree, item_node.identifier, pr,
                                                   data=get_data_structure(node_type='prop_name'))  # 特性节点（三级节点）
                        if variable:
                            variables = _level_list(variable, 3)  # 规范列表层数
                            if j >= len(variables):  # 如果子名称长度小于上一级名称则跳过
                                continue
                            for k, var in enumerate(variables[j][i]):
                                _tree_sub_node(tree, prop_node.identifier, var,
                                               data=get_data_structure(node_type='prop_variable'))  # 特性变量节点（四级节点）
    else:
        print(f'tree的类型错误，创建失败：{type(tree)}')
        return None
    return tree


def combine_sys_dimension(system_tree, root_ele: str, sub_trees) -> None:
    """
    将子树合并到系统树下的root_ele对应节点
    :param system_tree: 需要合并的系统树
    :param root_ele: 系统树下的指定节点tag
    :param sub_trees: 子树列表
    :return: None
    """

    def find_node(tree, tag):
        """通过节点的tag在树中查找"""
        for tag_n in tree.all_nodes():
            if tag_n.tag == tag:
                return tag_n
        else:
            return None

    if not isinstance(sub_trees, list):
        sub_trees = [sub_trees]
    # 查找子树需要合并到系统树的指定节点
    node = find_node(system_tree, root_ele)
    if node:
        from treelib.exceptions import NodeIDAbsentError
        for sub_tree in sub_trees:
            if sub_tree:
                try:
                    system_tree.remove_node(sub_tree.all_nodes()[0].identifier)
                except NodeIDAbsentError:
                    pass
                system_tree.paste(node.identifier, sub_tree, deep=False)
    else:
        print('合并失败，请查看树中是否存在' + root_ele + '这个节点。')


def tree_model(sys_tree, model_name, name, node_list, tree=None) -> treelib.Tree or None:
    """
    创建模型树
    :param sys_tree: 系统树
    :param model_name: 系统树中的模型节点名称 
    :param name: 模型树节点名称
    :param node_list: 节点名称列表
    :param tree: 模型子树
    :return: tree (模型子树)
    """
    model_dim_dict = {}  # 存放模型维度及其下的选中节点的字典，{维度: [选中节点]}
    model_node = find_node_by_tag(sys_tree, model_name)  # model name 的模型节点
    for dim_node in sys_tree.children(model_node.identifier):  # layer 2 即 维度节点
        # print(dim_node.tag)
        model_dim_dict[dim_node.tag] = []
        for obj_node in sys_tree.children(dim_node.identifier):  # object type 节点
            # print(obj_node.tag)
            if obj_node.tag in node_list:
                model_dim_dict[dim_node.tag].append(obj_node.tag)
    # print(model_dim_dict)

    if tree is None:
        tree = treelib.Tree()
        tree.create_node("model", id_generator.idgen.next_id(), data={'node_type': "model", 'model_name': model_name})  # 根节点
    if isinstance(tree, treelib.Tree):
        # 创建固定需求节点
        name_node = _tree_sub_node(tree, tree.root, name, data={'node_type': "model_group", 'model_name': model_name})  # 名称
        for key, n_list in model_dim_dict.items():
            dim_node = _tree_sub_node(tree, name_node.identifier, key, data={'node_type': "model_dimension", 'model_name': model_name})  # 维度
            for node in n_list:
                obj_node = tree.create_node(node, id_generator.idgen.next_id(),
                                            parent=dim_node.identifier, data={'node_type': "model_object", 'model_name': model_name})  # 节点
                tree.create_node("编号", id_generator.idgen.next_id(),
                                 parent=obj_node.identifier, data={'node_type': "model_object_id", 'model_name': model_name})  # 编号
            # 没有list中的节点则删除
            if not tree.children(dim_node.identifier):
                tree.remove_node(dim_node.identifier)

    all_nodes = []
    for nodes in model_dim_dict.values():
        if nodes:
            all_nodes += nodes
    for node in node_list:
        if node not in all_nodes:
            print(f"'{node}'节点不存在于系统树中，无法创建。")
    return tree


def tree_to_df(tree, columns_name: str, columns_num=5, index_levels=None) -> pd.DataFrame:
    """
    将树转换为dataframe，所有节点作为多级索引
    :param tree: 需要转换的树
    :param columns_name: 列名
    :param columns_num: 列数
    :param index_levels: 索引的名称
    :return: 返回转换的dataframe
    """
    idx_len = tree.depth()  # 树的深度
    idx_tuples = []  # 索引根据元组生成
    idx_names = index_levels if index_levels else [f'{i + 1}级' for i in range(idx_len + 1)]  # 索引的名称
    # 生成多级索引的元组
    for path in tree.paths_to_leaves():
        tags = []
        for nid in path:
            tags.append(tree.get_node(nid).tag)
        tags += ['None'] * (idx_len - len(path[:-1]))  # 补充缺少的索引名
        idx_tuples.append(tuple(tags))
    # 创建多级行索引
    index = pd.MultiIndex.from_tuples(
        tuples=idx_tuples,
        names=idx_names
    )
    df = pd.DataFrame(index=index)
    for n in range(columns_num):
        df[f'{columns_name}{n + 1}'] = None
    df.astype('object')
    return df


# def dimension_data_value(df, name: str, item: str, prop: str, variable: list) -> None:
#     """
#     df数据输入
#     :param df: 需要进行数据输入的df
#     :param name: 名称（一级节点）
#     :param item: 子名称 list（二级节点）
#     :param prop: 特性名称 list（三级节点）
#     :param variable: 特性变量名称 list（四级节点）
#     :return: None
#     """
#     # 忽略多级索引可能导致的性能警告
#     warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)
#     # 系统名称
#     sysname = df.index[0][0]
#     # 列满需要添加新列之后进行插入，标记哪一列没有值
#     tmp = len(df.columns) + 1  # 默认新一列
#     indexes = [df.index.get_level_values(0)[0], name, item, prop]  # [sysname, name, item, prop]
#     # 查找是否有没有值的列
#     for i, col in enumerate(df.columns):
#         if df.loc[tuple(indexes), col].isnull().all():
#             tmp = i + 1  # i+1列没有值或需要进行覆盖操作
#             break
#     # 插值
#     col_name = f'value {tmp}'
#     for idx, var in zip(df.loc[tuple(indexes)].index, variable):
#         df.loc[tuple(indexes + [idx]), col_name] = var


def model_data_value(df, index_levels: list, values, col_num=-1) -> None:
    """
    df的数据传入
    :param df: 传值的df
    :param index_levels: 索引列表
    :param values: 数值列表
    :param col_num: 传入的列
    :return: None
    """
    # 获取列的前缀
    columns_name = ''
    for char in df.columns[0]:
        if not char.isdigit():
            columns_name += char
    # 规范输入列表层数
    reg_values = _level_list(values, 2)
    tmp_values = copy.deepcopy(reg_values)  # 深拷贝，防止变量覆盖问题

    # 单列插入值
    def col_data_value(vars, col_x):
        # 忽略多级索引可能导致的性能警告
        warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)
        warnings.simplefilter(action='ignore', category=FutureWarning)
        if col_x == -1:  # 未指定列
            tmp = len(df.columns) + 1  # 默认新列
            # 查找是否有没有值的列
            for i, col in enumerate(df.columns):
                if df.loc[tuple(index_levels), col].isnull().all():
                    tmp = i + 1  # i+1列没有值或需要进行覆盖操作
                    break
        else:  # 指定列则进行修改
            if col_x > len(df.columns):
                print(f"目前共有{len(df.columns)}列，{col_x}超出能修改列的范围，不进行修改。")
                return
            tmp = col_x
        # 插值
        for i, var in enumerate(vars):
            if isinstance(var, str) and var[0] == '[' and var[-1] == ']':
                vars[i] = [x.replace(' ', '') for x in var[1: -1].split(',')]
        col_name = f'{columns_name}{tmp}'
        for i in range(len(df.loc[tuple(index_levels), col_name])):
            df.loc[tuple(index_levels), col_name].iloc[i] = vars[i]

    # 遍历二维列表进行列插入
    for i in range(len(tmp_values)):
        if col_num != -1: col_num = col_num + i
        col_data_value(tmp_values[i], col_num)


def search_model_data(df, index_levels: list, cols=None):
    """
    在df中根据索引和列名进行搜索
    :param df: dataframe
    :param index_levels: 多级索引列表
    :param cols: 列的数字列表
    :return: 搜索到的部分df
    """
    # 获取列的前缀
    columns_name = ''
    for char in df.columns[0]:
        if not char.isdigit():
            columns_name += char
    # 查看所有列
    if not cols:
        return df.loc[tuple(index_levels)]
    # 查看单列
    if isinstance(cols, int):
        cols = [cols]
    # 查看多列
    if isinstance(cols, list):
        cols = [f'{columns_name}{col}' for col in cols]
    # 去除不存在的列
    remove_list = []
    for col in cols:
        if col not in list(df.columns):
            print(f'{col} 不在数据中，无法查找到。')
            remove_list.append(col)
    for rem in remove_list:
        cols.remove(rem)
    return df.loc[tuple(index_levels), cols]


def rename_df_index(df, index_names: dict):
    """
    对df的索引进行重命名
    :param df: dataframe
    :param index_names: 索引的字典，将key与value进行替换
    """
    idx_set = set()  # 索引名称集合
    for col in df.index.values:
        for x in col:
            idx_set.add(x)
    for k in index_names.keys():
        if k not in idx_set:
            print(f"没有'{k}'索引。")
    new_index_names = {key: value for key, value in index_names.items() if key in idx_set}
    df.rename(index=new_index_names, inplace=True)  # 如果索引集合中含有该key则变为value
    return None


if __name__ == '__main__':
    pass
    # # 系统树
    # system_tree = tree_sys(layer_1='system', model_name=['insofaiam', 'insofrobot', 'DTIS_511'])
    # print(system_tree)
    #
    # # 人员机器产品树
    # person_tree = tree_dimension('DTIS_511-person', '个人', '特性', '属性',
    #                              ['地址', '头像', '年龄', '性别', '手机'])
    # print(person_tree)
    # person_tree = tree_dimension('person', '机构', '特性',
    #                              '属性', ['排序', '地址', '类型'], tree=person_tree)
    # print(person_tree)
    # person_tree = tree_dimension('person', '职位', '特性', tree=person_tree)
    # person_tree = tree_dimension('person', '角色', '特性', tree=person_tree)
    # person_tree = tree_dimension('person', '账号', '特性', tree=person_tree)
    # print(person_tree)

    # # 方法树
    # method_tree = tree_dimension(layer_2='DTIS_511-method', object_name='一维表单生成', layer_3=['输入', '输出'],
    #                              prop_name=[['标签1', '标签2', '标签3', '标签4', '标签5', '标签6',
    #                                          '数值1', '数值2', '数值3', '数值4', '数值5', '数值6', '题目'],
    #                                         ['文件名', '文件地址']])
    # print(method_tree)
    # method_tree = tree_dimension(tree=method_tree, layer_2='method', object_name='工艺设计', layer_3=['输入', '输出'])
    # print(method_tree)

    # # 流程树
    # procedure_tree = tree_dimension(layer_2='procedure', object_name='试验人员组织', layer_3='特性',
    #                                 prop_name=['一岗', '二岗'],
    #                                 prop_variable=[[['力测量', '功放系统', '台体系统', '应变系统', '控制系统']], [['力测量', '混响室本体']]])
    # print(procedure_tree)
    # procedure_tree = tree_dimension(tree=procedure_tree, layer_2='procedure', object_name='试验人员组织', layer_3='特性',
    #                                 prop_name=['一岗', '二岗'],
    #                                 prop_variable=[[[]], [['力测量', '功放系统']]])
    # print(procedure_tree)

    # # 合并树
    # combine_sys_dimension(system_tree, 'DTIS_511', [person_tree])
    # print(system_tree)
    #
    # mod_tree = tree_model(sys_tree=system_tree, model_name="DTIS_511", name="试验任务定义",
    #                       node_list=['个人', '机构', '私人', '工艺设计'])
    # print(mod_tree)
    # mod_tree = tree_model(sys_tree=system_tree, model_name="DTIS_511", name="试验任务成员",
    #                       node_list=['个人', '机构', '角色'], tree=mod_tree)
    # print(mod_tree)

    # # 树转df
    # system_df = tree_to_df(system_tree, 'value ', 2,
    #                        ['layer 1', 'model name', 'layer 2', 'object name',
    #                        'layer 3', 'prop name', 'prop variable'])
    # print(system_df)

    # rename_df_index(system_df, {'标签1': 'level_1', '标签2': 'level_2', '标签3': 'level_3'})
    # print(system_df)

    # method_df = tree_to_df(method_tree, 'method ', 3,
    #                        ['layer 2', 'object name', 'layer 3', 'prop name'])
    # print(method_df)
    # transposed_data = ['[50.0, 50.0, 50.0, 50.0, 50.0]',
    #                    '[0.4149, 0.4149, 0.4149, 0.4149, 0.4149]',
    #                    '[0.2098, 0.2098, 0.2098, 0.2098, 0.2098]',
    #                    '[0.0582, 0.0582, 0.0582, 0.0582, 0.0582]',
    #                    '[0.4492, 0.4492, 0.4492, 0.4492, 0.4492]',]
    # model_data_value(system_df, ['model', 'DTIS_511', 'DTIS_511-person', '个人'], transposed_data)
    # print(system_df)
    # print(transposed_data)

    # for x in method_df.iloc[0, 0]:
    #     print(x)
    # # df数据添加
    # model_data_value(system_df, ['model', 'insofaiam'], 'aiam')
    # print(system_df)
    # # df数据添加
    # model_data_value(system_df, ['model', 'DTIS_511', 'person', '个人', '特性'], [[5, 4, 3, 2, 1], [1, 2, 3, 4, 5]])
    # print(system_df)
    # model_data_value(system_df, ['model', 'DTIS_511', 'person', '个人', '特性'], [[9, 9, 9, 9, 9], [0, 0, 0, 0, 0]])
    # print(system_df)

    # system_df.loc[('model', 'DTIS_511', 'person', '个人', '特性'), ['value 1']] = [9, 9, 9, 9, 9]
    # print(system_df.loc[('model', 'DTIS_511', 'person', '个人')])
    # person_df = search_model_data(system_df, ['model', 'DTIS_511', 'person'], cols=4)
    # print(person_df)

    # # 索引 object name
    # print(system_df[system_df.index.get_level_values('layer 3') == '编号'])

    # tree = treelib.Tree()
    # tree.create_node('test', '001')
    # tree.subtree()
