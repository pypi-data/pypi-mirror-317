import pandas as pd
from imkernel.core.system import System
from imkernel.utils import id_generator
from loguru import logger


class ModelLinking:
    def __init__(
        self,
        linking_type: str = None,
        identifier_id: int = None,
        identifier_name: str = None,
        remark: int = None,
    ):
        self.id = id_generator.idgen.next_id()
        self.linking_type = linking_type
        self.identifier_id = identifier_id
        self.identifier_name = identifier_name
        self.remark = remark


class ModelMap:
    def __init__(
        self,
        element_id: int = None,
        element_name: str = None,
        method_id: int = None,
        method_name: str = None,
        procedure_id: int = None,
        procedure_name: str = None,
    ):
        self.id = id_generator.idgen.next_id()
        self.element_id = element_id
        self.element_name = element_name
        self.method_id = method_id
        self.method_name = method_name
        self.procedure_id = procedure_id
        self.procedure_name = procedure_name


class ModelData:
    def __init__(
        self,
        remark_num_value: dict = None,
        identifier_id_value: dict = None,
        identifier_name_value: dict = None,
    ):
        self.id = id_generator.idgen.next_id()
        self.remark_num_value = remark_num_value
        self.identifier_id_value = identifier_id_value
        self.identifier_name_value = identifier_name_value


class ModelObject:
    def __init__(
        self,
        name: str,
        linking_list: list[ModelLinking] = None,
        map_list: list[ModelMap] = None,
        data_list: list[ModelData] = None,
    ):
        self.id = id_generator.idgen.next_id()
        self.name = name
        self.linking_list = linking_list if linking_list else []
        self.map_list = map_list if map_list else []
        self.data_list = data_list if data_list else []

    def add_linking(self, linking: ModelLinking):
        self.linking_list.append(linking)

    def add_map(self, map: ModelMap):
        self.map_list.append(map)

    def add_data(self, data: ModelData):
        self.data_list.append(data)

    def delete_linking(self, linking: ModelLinking):
        self.linking_list.remove(linking)

    def delete_map(self, map: ModelMap):
        self.map_list.remove(map)

    def delete_data(self, data: ModelData):
        self.data_list.remove(data)

    def update_linking(self, old_linking: ModelLinking, new_linking: ModelLinking):
        for i, item in enumerate(self.linking_list):
            if item == old_linking:  # 判断是否匹配旧对象
                self.linking_list[i] = new_linking

    def update_map(self, old_map: ModelLinking, new_map: ModelLinking):
        for i, item in enumerate(self.map_list):
            if item == old_map:  # 判断是否匹配旧对象
                self.map_list[i] = new_map

    def update_data(self, old_data: ModelLinking, new_data: ModelLinking):
        for i, item in enumerate(self.data_list):
            if item == old_data:  # 判断是否匹配旧对象
                self.data_list[i] = new_data


class Model:
    def __init__(self, name: str, object_list: list[ModelObject] = None):
        self.id = id_generator.idgen.next_id()
        self.name = name
        self.object_list = object_list if object_list else []

    def add_object(self, object: ModelObject):
        self.object_list.append(object)

    def delete_object(self, object: ModelObject):
        self.object_list.remove(object)

    def update_object(self, old_object: ModelObject, new_object: ModelObject):
        for i, item in enumerate(self.object_list):
            if item == old_object:  # 判断是否匹配旧对象
                self.object_list[i] = new_object

    def show(self, system: System):
        table_data = {"model_name": [], "object_name": [], "type_name": [], "identifier": []}
        for object in self.object_list:
            for linking in object.linking_list:
                table_data["model_name"].append(self.name)
                table_data["object_name"].append(object.name)
                results = system.get(identifier=linking.identifier_name)
                table_data["type_name"].append(results[0].type)
                table_data["identifier"].append(linking.identifier_name)

            for index1, data in enumerate(object.data_list):
                table_data[f"value{index1+1}"] = []
                for linking in object.linking_list:
                    table_data[f"value{index1+1}"].append(data.identifier_name_value.get(linking.identifier_name, None))

        df = pd.DataFrame(table_data)
        return df

    def show_map(self):
        data = {
            "model_name": [],
            "object_name": [],
            "element_name": [],
            "method_name": [],
            "procedure_name": [],
        }

        for object in self.object_list:
            for map in object.map_list:
                data["model_name"].append(self.name)
                data["object_name"].append(object.name)
                data["element_name"].append(map.element_name)
                data["method_name"].append(map.method_name)
                data["procedure_name"].append(map.procedure_name)

        df = pd.DataFrame(data)
        return df
