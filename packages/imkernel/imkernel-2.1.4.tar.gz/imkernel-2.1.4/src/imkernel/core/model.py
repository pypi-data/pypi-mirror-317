import pandas as pd
from imkernel.core.system import System
from imkernel.utils import id_generator
from loguru import logger


class ModelIdentifierLinking:
    def __init__(
        self,
        linking_type: str,
        linking_identifier_id: int = None,
        linking_identifier_name: str = None,
        remark: int = None,
    ):
        self.id = id_generator.idgen.next_id()
        self.linking_type = linking_type
        self.linking_identifier_id = linking_identifier_id
        self.linking_identifier_name = linking_identifier_name
        self.remark = remark


class ModelVariableMap:
    def __init__(
        self,
        model_element_id: int = None,
        model_element_name: str = None,
        model_method_id: int = None,
        model_method_name: str = None,
        model_procedure_id: int = None,
        model_procedure_name: str = None,
    ):
        self.id = id_generator.idgen.next_id()
        self.model_element_id = model_element_id
        self.model_element_name = model_element_name
        self.model_method_id = model_method_id
        self.model_method_name = model_method_name
        self.model_procedure_id = model_procedure_id
        self.model_procedure_name = model_procedure_name


class ModelData:
    def __init__(
        self,
        remark_num_value_dict: dict = None,
        remark_identifier_id_value_dict: dict = None,
        remark_identifier_name_value_dict: dict = None,
    ):
        self.id = id_generator.idgen.next_id()
        self.remark_num_value_dict = remark_num_value_dict
        self.remark_identifier_id_value_dict = remark_identifier_id_value_dict
        self.remark_identifier_name_value_dict = remark_identifier_name_value_dict


# region 和表的映射
class Model:
    def __init__(
        self,
        name: str,
        identifier_linking_list: list[ModelIdentifierLinking] = None,
        model_variable_map_list: list[ModelVariableMap] = None,
        model_data_list: list[ModelData] = None,
    ):
        self.id = id_generator.idgen.next_id()
        self.name = name
        self.identifier_linking_list = identifier_linking_list if identifier_linking_list else []
        self.model_variable_map_list = model_variable_map_list if model_variable_map_list else []
        self.model_data_list = model_data_list if model_data_list else []

    def add_identifier_linking(self, identifier_linking: ModelIdentifierLinking):
        self.identifier_linking_list.append(identifier_linking)

    def add_model_variable_map(self, model_variable_map: ModelVariableMap):
        self.model_variable_map_list.append(model_variable_map)

    def add_model_data(self, model_data: ModelData):
        self.model_data_list.append(model_data)

    def delete_identifier_linking(self, identifier_linking: ModelIdentifierLinking):
        self.identifier_linking_list.remove(identifier_linking)

    def delete_model_variable_map(self, model_variable_map: ModelVariableMap):
        self.model_variable_map_list.remove(model_variable_map)

    def delete_model_data(self, model_data: ModelData):
        self.model_data_list.remove(model_data)

    def update_identifier_linking(self, old_identifier_linking: ModelIdentifierLinking, new_identifier_linking: ModelIdentifierLinking):
        for i, item in enumerate(self.identifier_linking_list):
            if item == old_identifier_linking:  # 判断是否匹配旧对象
                self.identifier_linking_list[i] = new_identifier_linking

    def update_model_variable_map(self, old_model_variable_map: ModelIdentifierLinking, new_model_variable_map: ModelIdentifierLinking):
        for i, item in enumerate(self.model_variable_map_list):
            if item == old_model_variable_map:  # 判断是否匹配旧对象
                self.model_variable_map_list[i] = new_model_variable_map

    def update_model_data(self, old_model_data: ModelIdentifierLinking, new_model_data: ModelIdentifierLinking):
        for i, item in enumerate(self.model_data_list):
            if item == old_model_data:  # 判断是否匹配旧对象
                self.model_data_list[i] = new_model_data

    # def get_identifier_linking(self):
    #     return self.identifier_linking_list

    # def get_model_variable_map(self):
    #     return self.model_variable_map_list

    # def get_model_data(self):
    #     return self.model_data_list

    def show_model_detail_with_data(self, system: System):
        data = {"model_name": [], "type_name": [], "identifier": []}
        for identifier_linking in self.identifier_linking_list:
            data["model_name"].append(self.name)
            results = system.get(identifier=identifier_linking.linking_identifier_name)
            data["type_name"].append(results[0].type)
            data["identifier"].append(identifier_linking.linking_identifier_name)

        for index1, model_data in enumerate(self.model_data_list):
            data[f"value{index1+1}"] = []
            for identifier_linking in self.identifier_linking_list:
                data[f"value{index1+1}"].append(model_data.remark_identifier_name_value_dict.get(identifier_linking.linking_identifier_name, None))

        df = pd.DataFrame(data)
        return df

    def show_model_variable_map(self):
        data = {
            "model_name": [],
            "model_element_name": [],
            "model_method_name": [],
            "model_procedure_name": [],
        }

        for model_variable_map in self.model_variable_map_list:
            data["model_name"].append(self.name)
            data["model_element_name"].append(model_variable_map.model_element_name)
            data["model_method_name"].append(model_variable_map.model_method_name)
            data["model_procedure_name"].append(model_variable_map.model_procedure_name)

        df = pd.DataFrame(data)
        return df
