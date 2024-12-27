from enum import Enum

import treelib


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


class Prop:
    def __int__(self, name: str, id: str):
        self.name = name
        self.id = id


class Element:
    def __init__(self, name: str, type: str, id: str, property: str, prop_variable: str):
        self.name = name
        self.type = type  # person
        self.id = id
        self.property = property
        self.prop_variable = prop_variable

    def Add(self, element, new_element):
        raise NotImplementedError

    def Delete(self):
        raise NotImplementedError

    def Create(self):
        raise NotImplementedError


from treelib import Tree
from treelib import Node

t = Tree()
n = Node(tag='xxx')
if __name__ == '__main__':
    Element(name='DITS-511')
    Element.Add(type='person', id='机构', property='', prop_variable='')
