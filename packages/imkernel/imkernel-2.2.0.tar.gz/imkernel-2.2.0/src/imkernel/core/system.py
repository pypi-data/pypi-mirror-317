from enum import Enum
from typing import Dict, Optional
from loguru import logger

import pandas as pd

from imkernel.utils import id_generator
from imkernel.utils.api_utils import ApiClient


class ModelType(Enum):
    """模型类型枚举"""
    # 人
    Person = "Person"
    # 机
    Machine = "Machine"
    # 产品
    Product = "Product"
    # 方法模型
    Method = "Method"
    # 过程模型
    Procedure = "Procedure"


class System:
    def __init__(self, name, items=None):
        self.id = id_generator.idgen.next_id()
        if name is None:
            self.name = self.id
        else:
            self.name = name
        # items可以为空
        if items is None:
            self.items = []
        else:
            self.items = items

    def _add_item(self, item) -> bool:
        """
        检查元素是否重复并添加到系统中
        """
        # 检查是否存在重复元素
        for existing_element in self.items:
            if (existing_element.type == item.type and
                    existing_element.identifier == item.identifier and
                    existing_element.prop == item.prop and
                    existing_element.variable == item.variable):
                return False

        # 如果没有重复，添加元素
        self.items.append(item)
        return True

    def add(self, type, identifier: str = None, prop=None, variable=None):
        def _add(item):
            # 直接添加Item
            obj = None
            if isinstance(item, Element):
                obj = item
            elif isinstance(item, Method):
                obj = item
            elif isinstance(item, Procedure):
                obj = item
            else:
                raise Exception("类型只能是Element/Method/Procedure")
            if not self._add_item(obj):
                logger.warning(f"添加单元时重复: type={obj.type}, identifier={obj.identifier}, "
                               f"prop={obj.prop}, variable={obj.variable}")
            else:
                logger.info(f"成功添加单元: type={obj.type}, identifier={obj.identifier}, "
                            f"prop={obj.prop}, variable={obj.variable}")

        # 如果后面都是None
        if identifier is None and prop is None and variable is None:
            if isinstance(type, list):
                # 接收列表类型
                for x in type:
                    _add(x)
            else:
                _add(type)

            # end if
        else:
            # 直接添加元素
            if isinstance(variable, list):
                added_list = []
                duplicate_list = []
                for item in variable:
                    element = Element(type, identifier, prop, item)
                    if self._add_item(element):
                        added_list.append(element)
                    else:
                        duplicate_list.append(element)

                if duplicate_list:
                    logger.warning(f"添加单元时重复: type={type}, identifier={identifier}, prop={prop}, "
                                   f"variables={[e.variable for e in duplicate_list]}")
                if added_list:
                    logger.info(f"成功添加单元: type={type}, identifier={identifier}, prop={prop}, "
                                f"variables={[e.variable for e in added_list]}")
                # return added_list
            else:
                element = Element(type, identifier, prop, variable)
                if not self._add_item(element):
                    logger.warning(f"添加单元时重复: type={type}, identifier={identifier}, "
                                   f"prop={prop}, variable={variable}")
                else:
                    logger.info(f"成功添加单元: type={type}, identifier={identifier}, "
                                f"prop={prop}, variable={variable}")
                # return element

    def add_element(self, element):
        if isinstance(element, Element):
            if not self._add_item(element):
                logger.warning(f"添加单元时重复: type={element.type}, identifier={element.identifier}, "
                               f"prop={element.prop}, variable={element.variable}")
            else:
                logger.info(f"成功添加单元: type={element.type}, identifier={element.identifier}, "
                            f"prop={element.prop}, variable={element.variable}")
        else:
            raise Exception("类型不正确")

    def delete(self, type=None, identifier=None, prop=None, variable=None):
        """
        根据条件查找并删除元素

        Args:
            type: 类型
            identifier: 标识
            prop: 属性
            variable: 变量值或变量列表

        Returns:
            删除的元素列表
        """
        # 如果variable是列表，进行批量删除
        if isinstance(variable, list):
            deleted_list = []
            not_found_list = []
            for item in variable:
                to_delete = []
                for element in self.items:
                    if (element.type == type and
                            element.identifier == identifier and
                            element.prop == prop and
                            element.variable == item):
                        to_delete.append(element)

                if to_delete:
                    for element in to_delete:
                        self.items.remove(element)
                        deleted_list.append(element)
                else:
                    not_found_list.append(item)

            if not_found_list:
                logger.warning(f"未找到要删除的单元: type={type}, identifier={identifier}, "
                               f"prop={prop}, variables={not_found_list}")
            if deleted_list:
                logger.info(f"成功删除单元: type={type}, identifier={identifier}, "
                            f"prop={prop}, variables={[e.variable for e in deleted_list]}")
            # return deleted_list

        # 如果variable是单个值
        else:
            to_delete = []
            for element in self.items:
                if (element.type == type and
                        element.identifier == identifier and
                        element.prop == prop and
                        element.variable == variable):
                    to_delete.append(element)

            if not to_delete:
                logger.warning(f"未找到要删除的单元: type={type}, identifier={identifier}, "
                               f"prop={prop}, variable={variable}")
            else:
                for element in to_delete:
                    self.items.remove(element)
                logger.info(f"成功删除单元: type={type}, identifier={identifier}, "
                            f"prop={prop}, variable={variable}")

            # return to_delete

    def get(self, type=None, identifier=None, prop=None, variable=None, exact_match=True):
        """
        查询元素，支持精确匹配和模糊匹配

        Args:
            type: 类型
            identifier: 标识
            prop: 属性
            variable: 变量值或变量列表
            exact_match: 是否精确匹配，默认True

        Returns:
            list: 匹配的元素列表
        """
        results = []

        # 记录查询条件
        query_conditions = {}
        if type is not None:
            query_conditions['type'] = type
        if identifier is not None:
            query_conditions['identifier'] = identifier
        if prop is not None:
            query_conditions['prop'] = prop
        if variable is not None:
            query_conditions['variable'] = variable

        # 如果没有提供任何条件，返回所有元素
        if not query_conditions:
            logger.info(f"查询所有单元: 共找到 {len(self.items)} 个元素")
            return self.items

        for element in self.items:
            match = True
            for attr, value in query_conditions.items():
                element_value = getattr(element, attr)

                if exact_match:
                    # 精确匹配
                    if isinstance(value, list):
                        if element_value not in value:
                            match = False
                            break
                    elif element_value != value:
                        match = False
                        break
                else:
                    # 模糊匹配
                    if isinstance(value, list):
                        if not any(str(v).lower() in str(element_value).lower() for v in value):
                            match = False
                            break
                    elif str(value).lower() not in str(element_value).lower():
                        match = False
                        break

            if match:
                results.append(element)

        # 记录查询结果
        match_type = "精确匹配" if exact_match else "模糊匹配"
        if results:
            logger.info(
                f"查询到{len(results)}个单元: 查询条件={query_conditions}, "
            )
        else:
            logger.warning(
                f"未找到匹配的单元: 查询条件={query_conditions}, "
            )

        return results

    def update(self, search_condition=None, new_values=None):
        """
        更新符合查询条件的元素

        Args:
            search_condition: dict, 查询条件，例如 {'type': 'person', 'identifier': '工作人员'}
            new_values: dict, 要更新的新值，例如 {'prop': '新属性', 'variable': '新变量'}

        Returns:
            int: 更新的元素数量
        """
        if not search_condition or not new_values:
            raise ValueError("必须同时提供查询条件和更新值")
        # 传递了Id，先校验是否存在id
        # 验证字段名称
        valid_fields = {'type', 'identifier', 'prop', 'variable'}
        invalid_fields = set(search_condition.keys()) - valid_fields
        if invalid_fields:
            raise ValueError(f"无效的字段名称: {invalid_fields}")

        update_count = 0
        # 保存更新前后的值用于日志记录
        updated_elements = []

        for element in self.items:
            # 检查是否匹配所有搜索条件
            match = True
            for field, value in search_condition.items():
                if getattr(element, field) != value:
                    match = False
                    break

            # 如果匹配，更新元素
            if match:
                # 保存更新前的值
                old_values = {
                    'type': element.type,
                    'identifier': element.identifier,
                    'prop': element.prop,
                    'variable': element.variable
                }

                # 进行更新
                for field, new_value in new_values.items():
                    setattr(element, field, new_value)
                update_count += 1

                # 记录更新信息
                updated_elements.append({
                    'old': old_values,
                    'new': {field: value for field, value in new_values.items()}
                })

        # 根据更新结果记录日志
        if update_count == 0:
            logger.warning(f"未找到匹配的元素进行更新: search_criteria={search_condition}")
        else:
            for update_info in updated_elements:
                old = update_info['old']
                new = update_info['new']
                logger.info(
                    f"成功更新单元: 查询条件={search_condition}, "
                    f"原值=(type={old.get('type')}, identifier={old.get('identifier')}, "
                    f"prop={old.get('prop')}, variable={old.get('variable')}), "
                    f"更新值={new}"
                )

        # return update_count

    def load(self):
        """从数据库加载模型"""
        api = ApiClient()
        # 获取项目
        response = api.project.get_project_detail(project_name=self.name)
        if response['code'] != 200:
            raise Exception(response['message'])
        project_id = response['data']['id']
        self.id = project_id
        system_response = api.system.get_system_detail(project_id=project_id)
        item_list = system_response['data']
        for item in item_list:
            item = Item(
                id=item['id'],
                type=item['type'],
                type_id=['type_id'],
                identifier=item['identifier'],
                identifier_id=item['identifier_id'],
                prop=item['prop'],
                prop_id=item['prop_id'],
                variable=item['variable'],
                variable_id=item['variable_id']
            )

            self.items.append(item)
        if response['code'] != 200:
            raise Exception(response['message'])
        logger.info(f"系统：{self.name} 加载成功")

    def save(self):
        """保存系统模型到数据库"""
        api = ApiClient()

        # 创建项目
        response = api.project.create_project(self.name, self.id)
        if not response['success']:
            # 项目已存在，报错
            # todo：查询项目ID，进行合并
            raise Exception(f"模型创建失败，{response['message']}")
        # 增加system信息

        item_list = []
        for element in self.items:
            item_dict = {
                'id': element.id,
                'type': element.type,
                'identifier': element.identifier,
                'prop': element.prop,
                'variable': element.variable,
                'order_index': 0,
                'project_id': self.id
            }
            item_list.append(item_dict)

        r = api.node.batch_add_nodes(item_list)
        logger.info(f"保存系统 {self.name} 成功 {len(r['data']['success'])}")
        # return r

    def show(self, type: str = None):
        """
        用DataFrame展示系统模型
        Args:
            type: 可选值为 person, machine, product, method, procedure
        """
        VALID_TYPES = {'person', 'machine', 'product', 'method', 'procedure'}
        TYPE_ORDER = {'person': 0, 'machine': 1, 'product': 2, 'method': 3, 'procedure': 4}

        if type is not None and type not in VALID_TYPES:
            raise ValueError(f"类型只能是 {','.join(VALID_TYPES)} 中的一种")

        if not self.items:
            return pd.DataFrame({'system': [self.name]})

        # 为每个元素创建一个字典列表
        data = []
        for element in self.items:
            row = {
                'system': self.name,
                'type': element.type,
                'identifier': element.identifier,
                'prop': element.prop,
                'variable': element.variable
            }
            data.append(row)

        # 转换为DataFrame
        df = pd.DataFrame(data)

        # 如果指定了type,进行过滤
        if type is not None:
            df = df[df['type'] == type]

        # 如果过滤后为空,返回只有system的DataFrame
        if df.empty:
            return pd.DataFrame({'system': [self.name]})

        # 重新排序列，将system列放在最前面
        columns = ['system'] + [col for col in df.columns if col != 'system']
        df = df[columns]

        # 添加type的排序值
        df['type_order'] = df['type'].map(TYPE_ORDER)

        # 多级排序并重置索引
        df = df.sort_values(by=['type_order', 'identifier', 'prop'], ascending=[True, True, True]).reset_index(drop=True)

        # 删除辅助排序列
        df = df.drop('type_order', axis=1)

        df_indexed = df.set_index(['system', 'type', 'identifier', 'prop', 'variable'])
        return df_indexed


class Item:
    def __init__(self, type: str, identifier: str, prop: str, variable: str, id=None, type_id=None, identifier_id=None, prop_id=None, variable_id=None):
        if id is not None:
            self.id = id
        else:
            self.id = id_generator.idgen.next_id()
        self.type = type
        self.type_id = type_id
        self.identifier = identifier
        self.identifier_id = identifier_id
        self.prop = prop
        self.prop_id = prop_id
        self.variable = variable
        self.variable_id = variable_id
        self.data = []


class Element(Item):
    def __init__(self, type: str, identifier: str, prop: str, variable: str, id: int = None):
        super().__init__(type, identifier, prop, variable, id)


class Method(Item):
    def __init__(self, identifier: str, prop: str, variable: str, id: int = None):
        super().__init__("method", identifier, prop, variable, id)


class Procedure(Item):
    def __init__(self, identifier: str, prop: str, variable: str, id: int = None):
        super().__init__("procedure", identifier, prop, variable, id)
