def get_node_by_tag_and_data(tree, tag, data):
    """
    通过tag和data一起查找节点

    Args:
        tag: 节点的tag
        data: 节点的data

    Returns:
        Node: 找到的节点,如果没找到返回None
    """
    # 获取所有节点
    nodes = tree.all_nodes()

    # 遍历所有节点查找匹配的节点
    for node in nodes:
        if node.tag == tag and node.data == data:
            return node
    return None


def remove_node_by_tag_and_data(self, tag, data):
    """
    通过tag和data删除节点

    Args:
        tag: 节点的tag
        data: 节点的data

    Returns:
        bool: 是否成功删除节点
    """
    node = self.get_node_by_tag_and_data(tag, data)
    if node:
        self.remove_node(node.identifier)
        return True
    return False


from treelib import Tree
import json


def json_to_tree(json_data):
    tree = Tree()

    def add_node(node_data, parent=None):
        # 添加当前节点
        tree.create_node(
            tag=node_data['name'],
            identifier=node_data['id'],
            parent=node_data['parentId'],
            data={
                'nodeType': node_data['nodeType'],
                'nodeTypeAddition': node_data['nodeTypeAddition']
            }
        )

        # 递归添加子节点
        if 'children' in node_data and node_data['children']:
            for child in node_data['children']:
                add_node(child)

    # 从根节点开始构建树
    add_node(json_data)
    return tree


if __name__ == '__main__':
    # 使用示例
    json_str = '''
    {
    "id": 602543219574214,
    "name": "root",
    "nodeType": "root",
    "parentId": null,
    "nodeTypeAddition": null,
    "children": [
        {
            "id": 602543219627462,
            "name": "insofaiam",
            "nodeType": "supermodel",
            "parentId": 602543219574214,
            "nodeTypeAddition": null,
            "children": [
                {
                    "id": 602543691511238,
                    "name": "insofmining",
                    "nodeType": "model",
                    "parentId": 602543219627462,
                    "nodeTypeAddition": null,
                    "children": [
                        {
                            "id": 602543691515334,
                            "name": "人员",
                            "nodeType": "person",
                            "parentId": 602543691511238,
                            "nodeTypeAddition": null,
                            "children": null
                        },
                        {
                            "id": 602543691515335,
                            "name": "机器",
                            "nodeType": "machine",
                            "parentId": 602543691511238,
                            "nodeTypeAddition": null,
                            "children": [
                                {
                                    "id": 604931788694982,
                                    "name": "制造检测系统",
                                    "nodeType": "parameter_group",
                                    "parentId": 602543691515335,
                                    "nodeTypeAddition": "machine",
                                    "children": [
                                        {
                                            "id": 604931903784390,
                                            "name": "铣床",
                                            "nodeType": "parameter_group",
                                            "parentId": 604931788694982,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 604938635314630,
                                                    "name": "NC_code",
                                                    "nodeType": "parameter",
                                                    "parentId": 604931903784390,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 604967375340998,
                                                            "name": "txt_file",
                                                            "nodeType": "prop",
                                                            "parentId": 604938635314630,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 604938613867974,
                                                    "name": "technological_parameter",
                                                    "nodeType": "parameter",
                                                    "parentId": 604931903784390,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 604967132349894,
                                                            "name": "Cutter_length",
                                                            "nodeType": "prop",
                                                            "parentId": 604938613867974,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 604967153718726,
                                                            "name": "Cutter_angle",
                                                            "nodeType": "prop",
                                                            "parentId": 604938613867974,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 604967174497734,
                                                            "name": "Feed_speed",
                                                            "nodeType": "prop",
                                                            "parentId": 604938613867974,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 604967196153286,
                                                            "name": "Spindle_speed",
                                                            "nodeType": "prop",
                                                            "parentId": 604938613867974,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "id": 604931925804486,
                                            "name": "检测设备",
                                            "nodeType": "parameter_group",
                                            "parentId": 604931788694982,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 604932000208326,
                                                    "name": "视觉检测装置",
                                                    "nodeType": "parameter_group",
                                                    "parentId": 604931925804486,
                                                    "nodeTypeAddition": "",
                                                    "children": null
                                                }
                                            ]
                                        },
                                        {
                                            "id": 604931866310086,
                                            "name": "叶片实物",
                                            "nodeType": "parameter_group",
                                            "parentId": 604931788694982,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 604938498266566,
                                                    "name": "milling_tool_path",
                                                    "nodeType": "parameter",
                                                    "parentId": 604931866310086,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 604966354810310,
                                                            "name": "X",
                                                            "nodeType": "prop",
                                                            "parentId": 604938498266566,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 604966394172870,
                                                            "name": "Y",
                                                            "nodeType": "prop",
                                                            "parentId": 604938498266566,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 604966414710214,
                                                            "name": "Z",
                                                            "nodeType": "prop",
                                                            "parentId": 604938498266566,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 604966443288006,
                                                            "name": "I",
                                                            "nodeType": "prop",
                                                            "parentId": 604938498266566,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 604966456309190,
                                                            "name": "J",
                                                            "nodeType": "prop",
                                                            "parentId": 604938498266566,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 604966470645190,
                                                            "name": "K",
                                                            "nodeType": "prop",
                                                            "parentId": 604938498266566,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 604938520864198,
                                                    "name": "path_parameter",
                                                    "nodeType": "parameter",
                                                    "parentId": 604931866310086,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 604966829999558,
                                                            "name": "Cutter_diameter",
                                                            "nodeType": "prop",
                                                            "parentId": 604938520864198,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 604966871442886,
                                                            "name": "Cutting_depth",
                                                            "nodeType": "prop",
                                                            "parentId": 604938520864198,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 604966894753222,
                                                            "name": "Residual_height",
                                                            "nodeType": "prop",
                                                            "parentId": 604938520864198,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 604938541360582,
                                                    "name": "point_cloud",
                                                    "nodeType": "parameter",
                                                    "parentId": 604931866310086,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 604966983984582,
                                                            "name": "txt_file",
                                                            "nodeType": "prop",
                                                            "parentId": 604938541360582,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 604938558019014,
                                                    "name": "profile_error",
                                                    "nodeType": "parameter",
                                                    "parentId": 604931866310086,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 604967036818886,
                                                            "name": "profile_error",
                                                            "nodeType": "prop",
                                                            "parentId": 604938558019014,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "id": 602543691515336,
                            "name": "物料",
                            "nodeType": "product",
                            "parentId": 602543691511238,
                            "nodeTypeAddition": null,
                            "children": [
                                {
                                    "id": 604927531595206,
                                    "name": "设计系统",
                                    "nodeType": "parameter_group",
                                    "parentId": 602543691515336,
                                    "nodeTypeAddition": "",
                                    "children": [
                                        {
                                            "id": 604927830001094,
                                            "name": "叶片",
                                            "nodeType": "parameter_group",
                                            "parentId": 604927531595206,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 604931478173126,
                                                    "name": "曲面",
                                                    "nodeType": "parameter_group",
                                                    "parentId": 604927830001094,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 604931537429958,
                                                            "name": "型线",
                                                            "nodeType": "parameter_group",
                                                            "parentId": 604931478173126,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604938291557830,
                                                                    "name": "eleven_parameter",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604931537429958,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 604939973854662,
                                                                            "name": "Chord_Length",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604938291557830,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 604939996849606,
                                                                            "name": "Upper_Max_Width",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604938291557830,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 604940017669574,
                                                                            "name": "Upper_Max_Width_Loc",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604938291557830,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 604940043249094,
                                                                            "name": "Upper_Angle",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604938291557830,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 604940064032198,
                                                                            "name": "Upper_tip_coeff",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604938291557830,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 604940084196806,
                                                                            "name": "Upper_aft_part_shape",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604938291557830,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 604940111439302,
                                                                            "name": "Lower_max_width",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604938291557830,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 604940128757190,
                                                                            "name": "Lower_max_width_loc",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604938291557830,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 604940149786054,
                                                                            "name": "Lower_Angle",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604938291557830,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 604940223509958,
                                                                            "name": "Lower_tip_coeff",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604938291557830,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 604940244358598,
                                                                            "name": "Lower_aft_part_shape",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604938291557830,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 604940275172806,
                                                                            "name": "Tangent_Leading_Edge",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604938291557830,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 604940297328070,
                                                                            "name": "spanwise_length",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604938291557830,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                },
                                                                {
                                                                    "id": 604938316821958,
                                                                    "name": "molded_line_point_sampling_point",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604931537429958,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 604940359448006,
                                                                            "name": "X",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604938316821958,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 604940378424774,
                                                                            "name": "Y",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604938316821958,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 604940391216582,
                                                                            "name": "Z",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604938316821958,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                },
                                                                {
                                                                    "id": 604938337330630,
                                                                    "name": "molded_line_control_point",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604931537429958,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 604940473685446,
                                                                            "name": "X",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604938337330630,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 604940491462086,
                                                                            "name": "Y",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604938337330630,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 604940503098822,
                                                                            "name": "Z",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604938337330630,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                },
                                                                {
                                                                    "id": 604938355791302,
                                                                    "name": "point",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604931537429958,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 604940564731334,
                                                                            "name": "X",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604938355791302,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 604940576093638,
                                                                            "name": "Y",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604938355791302,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 604940587787718,
                                                                            "name": "Z",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604938355791302,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 604938146338246,
                                                            "name": "CAD_file",
                                                            "nodeType": "parameter",
                                                            "parentId": 604931478173126,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604939700295110,
                                                                    "name": "obj_file",
                                                                    "nodeType": "prop",
                                                                    "parentId": 604938146338246,
                                                                    "nodeTypeAddition": "",
                                                                    "children": null
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 604938167473606,
                                                            "name": "control_point",
                                                            "nodeType": "parameter",
                                                            "parentId": 604931478173126,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604939762247110,
                                                                    "name": "X",
                                                                    "nodeType": "prop",
                                                                    "parentId": 604938167473606,
                                                                    "nodeTypeAddition": "",
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 604939775198662,
                                                                    "name": "Y",
                                                                    "nodeType": "prop",
                                                                    "parentId": 604938167473606,
                                                                    "nodeTypeAddition": "",
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 604939788469702,
                                                                    "name": "Z",
                                                                    "nodeType": "prop",
                                                                    "parentId": 604938167473606,
                                                                    "nodeTypeAddition": "",
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 604938063320518,
                                                    "name": "CAD_file",
                                                    "nodeType": "parameter",
                                                    "parentId": 604927830001094,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 604939611973062,
                                                            "name": "obj_file",
                                                            "nodeType": "prop",
                                                            "parentId": 604938063320518,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "id": 602543691515337,
                            "name": "过程",
                            "nodeType": "procedure",
                            "parentId": 602543691511238,
                            "nodeTypeAddition": null,
                            "children": [
                                {
                                    "id": 604935613179334,
                                    "name": "叶片设计",
                                    "nodeType": "parameter_group",
                                    "parentId": 602543691515337,
                                    "nodeTypeAddition": "procedure",
                                    "children": [
                                        {
                                            "id": 604935886144966,
                                            "name": "型线生成",
                                            "nodeType": "parameter_group",
                                            "parentId": 604935613179334,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 605031560857030,
                                                    "name": "算法名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 604935886144966,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 605032686060998,
                                                            "name": "method_eleven_parameter",
                                                            "nodeType": "prop",
                                                            "parentId": 605031560857030,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 605030788732358,
                                                    "name": "单元名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 604935886144966,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 605032636024262,
                                                            "name": "molded_line",
                                                            "nodeType": "prop",
                                                            "parentId": 605030788732358,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "id": 604935906989510,
                                            "name": "曲面生成",
                                            "nodeType": "parameter_group",
                                            "parentId": 604935613179334,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 605030807893446,
                                                    "name": "单元名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 604935906989510,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 605032728241606,
                                                            "name": "curved_surface",
                                                            "nodeType": "prop",
                                                            "parentId": 605030807893446,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 605032746608070,
                                                            "name": "molded_line",
                                                            "nodeType": "prop",
                                                            "parentId": 605030807893446,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 605031544088006,
                                                    "name": "算法名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 604935906989510,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 605032786752966,
                                                            "name": "method_curved_surface_generate",
                                                            "nodeType": "prop",
                                                            "parentId": 605031544088006,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "id": 604935933007302,
                                            "name": "叶片生成",
                                            "nodeType": "parameter_group",
                                            "parentId": 604935613179334,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 605030826513862,
                                                    "name": "单元名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 604935933007302,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 605032838665670,
                                                            "name": "blade",
                                                            "nodeType": "prop",
                                                            "parentId": 605030826513862,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 605031526954438,
                                                    "name": "算法名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 604935933007302,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 605032873833926,
                                                            "name": "method_blade_generate",
                                                            "nodeType": "prop",
                                                            "parentId": 605031526954438,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "id": 604935638795718,
                                    "name": "叶片制造",
                                    "nodeType": "parameter_group",
                                    "parentId": 602543691515337,
                                    "nodeTypeAddition": "procedure",
                                    "children": [
                                        {
                                            "id": 604936007636422,
                                            "name": "路径规划",
                                            "nodeType": "parameter_group",
                                            "parentId": 604935638795718,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 605030850311622,
                                                    "name": "单元名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 604936007636422,
                                                    "nodeTypeAddition": "",
                                                    "children": null
                                                },
                                                {
                                                    "id": 605031506138566,
                                                    "name": "算法名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 604936007636422,
                                                    "nodeTypeAddition": "",
                                                    "children": null
                                                }
                                            ]
                                        },
                                        {
                                            "id": 604936043951558,
                                            "name": "工艺设计",
                                            "nodeType": "parameter_group",
                                            "parentId": 604935638795718,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 605030872499654,
                                                    "name": "单元名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 604936043951558,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 605032971425222,
                                                            "name": "milling_machine",
                                                            "nodeType": "prop",
                                                            "parentId": 605030872499654,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 605031488091590,
                                                    "name": "算法名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 604936043951558,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 605033012999622,
                                                            "name": "method_technological_design",
                                                            "nodeType": "prop",
                                                            "parentId": 605031488091590,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "id": 604936064456134,
                                            "name": "加工铣削",
                                            "nodeType": "parameter_group",
                                            "parentId": 604935638795718,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 605030889612742,
                                                    "name": "单元名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 604936064456134,
                                                    "nodeTypeAddition": "",
                                                    "children": null
                                                },
                                                {
                                                    "id": 605031467189702,
                                                    "name": "算法名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 604936064456134,
                                                    "nodeTypeAddition": "",
                                                    "children": null
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "id": 604935663048134,
                                    "name": "叶片检测",
                                    "nodeType": "parameter_group",
                                    "parentId": 602543691515337,
                                    "nodeTypeAddition": "procedure",
                                    "children": [
                                        {
                                            "id": 604936226960838,
                                            "name": "常规检测",
                                            "nodeType": "parameter_group",
                                            "parentId": 604935663048134,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 605030911706566,
                                                    "name": "单元名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 604936226960838,
                                                    "nodeTypeAddition": "",
                                                    "children": null
                                                },
                                                {
                                                    "id": 605031448581574,
                                                    "name": "算法名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 604936226960838,
                                                    "nodeTypeAddition": "",
                                                    "children": null
                                                }
                                            ]
                                        },
                                        {
                                            "id": 604936250979782,
                                            "name": "视觉检测",
                                            "nodeType": "parameter_group",
                                            "parentId": 604935663048134,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 605030929364422,
                                                    "name": "单元名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 604936250979782,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 605033163032006,
                                                            "name": "visual_inspect_device",
                                                            "nodeType": "prop",
                                                            "parentId": 605030929364422,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 605031429789126,
                                                    "name": "算法名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 604936250979782,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 605033198421446,
                                                            "name": "method_blade_viaual_inspect",
                                                            "nodeType": "prop",
                                                            "parentId": 605031429789126,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "id": 604935688926662,
                                    "name": "叶片数据工程",
                                    "nodeType": "parameter_group",
                                    "parentId": 602543691515337,
                                    "nodeTypeAddition": "procedure",
                                    "children": [
                                        {
                                            "id": 604936360117702,
                                            "name": "叶片数据采集",
                                            "nodeType": "parameter_group",
                                            "parentId": 604935688926662,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 604937366484422,
                                                    "name": "试验数据采集",
                                                    "nodeType": "parameter_group",
                                                    "parentId": 604936360117702,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 605031088768454,
                                                            "name": "单元名称",
                                                            "nodeType": "parameter",
                                                            "parentId": 604937366484422,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 605031388014022,
                                                            "name": "算法名称",
                                                            "nodeType": "parameter",
                                                            "parentId": 604937366484422,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 604937399272902,
                                                    "name": "工厂数据采集",
                                                    "nodeType": "parameter_group",
                                                    "parentId": 604936360117702,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 605031124465094,
                                                            "name": "单元名称",
                                                            "nodeType": "parameter",
                                                            "parentId": 604937399272902,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 605031367943622,
                                                            "name": "算法名称",
                                                            "nodeType": "parameter",
                                                            "parentId": 604937399272902,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "id": 604936383518150,
                                            "name": "叶片数据筛选",
                                            "nodeType": "parameter_group",
                                            "parentId": 604935688926662,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 604937447699910,
                                                    "name": "筛选模型训练",
                                                    "nodeType": "parameter_group",
                                                    "parentId": 604936383518150,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 605031148496326,
                                                            "name": "单元名称",
                                                            "nodeType": "parameter",
                                                            "parentId": 604937447699910,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 605033540224454,
                                                                    "name": "blade_optimize_system",
                                                                    "nodeType": "prop",
                                                                    "parentId": 605031148496326,
                                                                    "nodeTypeAddition": "",
                                                                    "children": null
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 605031347197382,
                                                            "name": "算法名称",
                                                            "nodeType": "parameter",
                                                            "parentId": 604937447699910,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 605033573615046,
                                                                    "name": "method_AI_filter_model_train",
                                                                    "nodeType": "prop",
                                                                    "parentId": 605031347197382,
                                                                    "nodeTypeAddition": "",
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 604937487410630,
                                                    "name": "AI数据筛选",
                                                    "nodeType": "parameter_group",
                                                    "parentId": 604936383518150,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 605031168124358,
                                                            "name": "单元名称",
                                                            "nodeType": "parameter",
                                                            "parentId": 604937487410630,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 605033676727750,
                                                                    "name": "blade_optimize_system",
                                                                    "nodeType": "prop",
                                                                    "parentId": 605031168124358,
                                                                    "nodeTypeAddition": "",
                                                                    "children": null
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 605031328818630,
                                                            "name": "算法名称",
                                                            "nodeType": "parameter",
                                                            "parentId": 604937487410630,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 605033715131846,
                                                                    "name": "method_AI_data_filter",
                                                                    "nodeType": "prop",
                                                                    "parentId": 605031328818630,
                                                                    "nodeTypeAddition": "",
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "id": 604936337089990,
                                            "name": "叶片试验设计",
                                            "nodeType": "parameter_group",
                                            "parentId": 604935688926662,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 605031034250694,
                                                    "name": "单元名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 604936337089990,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 605033287685574,
                                                            "name": "blade_optimize_system",
                                                            "nodeType": "prop",
                                                            "parentId": 605031034250694,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 605031407449542,
                                                    "name": "算法名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 604936337089990,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 605033323795910,
                                                            "name": "method_experiment_design",
                                                            "nodeType": "prop",
                                                            "parentId": 605031407449542,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "id": 604935711524294,
                                    "name": "叶片AI优化",
                                    "nodeType": "parameter_group",
                                    "parentId": 602543691515337,
                                    "nodeTypeAddition": "procedure",
                                    "children": [
                                        {
                                            "id": 604936434890182,
                                            "name": "AI优化模型训练",
                                            "nodeType": "parameter_group",
                                            "parentId": 604935711524294,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 605031234594246,
                                                    "name": "单元名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 604936434890182,
                                                    "nodeTypeAddition": "",
                                                    "children": null
                                                },
                                                {
                                                    "id": 605031308965318,
                                                    "name": "算法名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 604936434890182,
                                                    "nodeTypeAddition": "",
                                                    "children": null
                                                }
                                            ]
                                        },
                                        {
                                            "id": 604936456660422,
                                            "name": "AI优化参数推荐",
                                            "nodeType": "parameter_group",
                                            "parentId": 604935711524294,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 605031274165702,
                                                    "name": "单元名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 604936456660422,
                                                    "nodeTypeAddition": "",
                                                    "children": null
                                                },
                                                {
                                                    "id": 605031289144774,
                                                    "name": "算法名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 604936456660422,
                                                    "nodeTypeAddition": "",
                                                    "children": null
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "id": 602543691515338,
                            "name": "方法",
                            "nodeType": "method",
                            "parentId": 602543691511238,
                            "nodeTypeAddition": null,
                            "children": [
                                {
                                    "id": 604932284769734,
                                    "name": "叶片设计",
                                    "nodeType": "parameter_group",
                                    "parentId": 602543691515338,
                                    "nodeTypeAddition": "method",
                                    "children": [
                                        {
                                            "id": 604932587652550,
                                            "name": "曲面生成",
                                            "nodeType": "parameter_group",
                                            "parentId": 604932284769734,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 604933053486534,
                                                    "name": "曲面生成方法",
                                                    "nodeType": "parameter_group",
                                                    "parentId": 604932587652550,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 604971341522374,
                                                            "name": "入参参数组",
                                                            "nodeType": "parameter",
                                                            "parentId": 604933053486534,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604992970032582,
                                                                    "name": "molded_line_control_point",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604971341522374,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 605001153078726,
                                                                            "name": "cpt_text",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604992970032582,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 604971356706246,
                                                            "name": "出参参数组",
                                                            "nodeType": "parameter",
                                                            "parentId": 604933053486534,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604993014789574,
                                                                    "name": "CAD_file",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604971356706246,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 605001206367686,
                                                                            "name": "obj_file",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604993014789574,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                },
                                                                {
                                                                    "id": 604993034331590,
                                                                    "name": "control_point",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604971356706246,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 605001255167430,
                                                                            "name": "X",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604993034331590,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605001276347846,
                                                                            "name": "Y",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604993034331590,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605001288332742,
                                                                            "name": "Z",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604993034331590,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 604971383276998,
                                                            "name": "程序文件",
                                                            "nodeType": "parameter",
                                                            "parentId": 604933053486534,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604973614040518,
                                                                    "name": "程序主文件",
                                                                    "nodeType": "prop",
                                                                    "parentId": 604971383276998,
                                                                    "nodeTypeAddition": "",
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "id": 604932606924230,
                                            "name": "叶片生成",
                                            "nodeType": "parameter_group",
                                            "parentId": 604932284769734,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 604933103543750,
                                                    "name": "叶片生成方法",
                                                    "nodeType": "parameter_group",
                                                    "parentId": 604932606924230,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 604971443922374,
                                                            "name": "入参参数组",
                                                            "nodeType": "parameter",
                                                            "parentId": 604933103543750,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604985822250438,
                                                                    "name": "curved_surface_CAD",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604971443922374,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 605003106915782,
                                                                            "name": "obj_file",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604985822250438,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 604971460105670,
                                                            "name": "出参参数组",
                                                            "nodeType": "parameter",
                                                            "parentId": 604933103543750,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604993128207814,
                                                                    "name": "blade_CAD",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604971460105670,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 605003144906182,
                                                                            "name": "obj_file",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604993128207814,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 604971486758342,
                                                            "name": "程序文件",
                                                            "nodeType": "parameter",
                                                            "parentId": 604933103543750,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604973658469830,
                                                                    "name": "程序主文件",
                                                                    "nodeType": "prop",
                                                                    "parentId": 604971486758342,
                                                                    "nodeTypeAddition": "",
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "id": 604932565259718,
                                            "name": "型线生成",
                                            "nodeType": "parameter_group",
                                            "parentId": 604932284769734,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 604932958447046,
                                                    "name": "曲面生成十一参数法",
                                                    "nodeType": "parameter_group",
                                                    "parentId": 604932565259718,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 604967884039622,
                                                            "name": "入参参数组",
                                                            "nodeType": "parameter",
                                                            "parentId": 604932958447046,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604985209537990,
                                                                    "name": "eleven_parameter",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604967884039622,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 605000338916806,
                                                                            "name": "Chord_Length",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604985209537990,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605000361539014,
                                                                            "name": "Upper_Max_Width",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604985209537990,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605000386102726,
                                                                            "name": "Upper_Max_Width_Loc",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604985209537990,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605000405509574,
                                                                            "name": "Upper_Angle",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604985209537990,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605000424695238,
                                                                            "name": "Upper_tip_coeff",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604985209537990,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605000445765062,
                                                                            "name": "Upper_aft_part_shape",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604985209537990,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605000465466822,
                                                                            "name": "Lower_max_width",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604985209537990,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605000485582278,
                                                                            "name": "Lower_max_width_loc",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604985209537990,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605000505075142,
                                                                            "name": "Lower_Angle",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604985209537990,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605000524400070,
                                                                            "name": "Lower_tip_coeff",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604985209537990,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605000544060870,
                                                                            "name": "Lower_aft_part_shape",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604985209537990,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605000562300358,
                                                                            "name": "Tangent_Leading_Edge",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604985209537990,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605000582063558,
                                                                            "name": "spanwise_length",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604985209537990,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 604967908758982,
                                                            "name": "出参参数组",
                                                            "nodeType": "parameter",
                                                            "parentId": 604932958447046,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604992358208966,
                                                                    "name": "molded_line_point_sampling_point",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604967908758982,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 605000681051590,
                                                                            "name": "X",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604992358208966,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605000694187462,
                                                                            "name": "Y",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604992358208966,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605000706360774,
                                                                            "name": "Z",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604992358208966,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                },
                                                                {
                                                                    "id": 604992381081030,
                                                                    "name": "molded_line_control_point",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604967908758982,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 605000736552390,
                                                                            "name": "X",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604992381081030,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605000748959174,
                                                                            "name": "Y",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604992381081030,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605000761218502,
                                                                            "name": "Z",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604992381081030,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 604968304678342,
                                                            "name": "程序文件",
                                                            "nodeType": "parameter",
                                                            "parentId": 604932958447046,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604973535876550,
                                                                    "name": "程序主文件",
                                                                    "nodeType": "prop",
                                                                    "parentId": 604968304678342,
                                                                    "nodeTypeAddition": "",
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 604932984333766,
                                                    "name": "曲面生成采样点法",
                                                    "nodeType": "parameter_group",
                                                    "parentId": 604932565259718,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 604971173164486,
                                                            "name": "入参参数组",
                                                            "nodeType": "parameter",
                                                            "parentId": 604932984333766,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604985610008006,
                                                                    "name": "molded_line_sampling_point",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604971173164486,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 605000858265030,
                                                                            "name": "X",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604985610008006,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605000872244678,
                                                                            "name": "Y",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604985610008006,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605000884512198,
                                                                            "name": "Z",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604985610008006,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 604971198830022,
                                                            "name": "出参参数组",
                                                            "nodeType": "parameter",
                                                            "parentId": 604932984333766,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604992827270598,
                                                                    "name": "molded_line_point_sampling_point",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604971198830022,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 605000925492678,
                                                                            "name": "X",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604992827270598,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605000937059782,
                                                                            "name": "Y",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604992827270598,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605000947566022,
                                                                            "name": "Z",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604992827270598,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                },
                                                                {
                                                                    "id": 604992846542278,
                                                                    "name": "molded_line_control_point",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604971198830022,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 605000978187718,
                                                                            "name": "X",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604992846542278,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605000990373318,
                                                                            "name": "Y",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604992846542278,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605001002526150,
                                                                            "name": "Z",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604992846542278,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 604971237696966,
                                                            "name": "程序文件",
                                                            "nodeType": "parameter",
                                                            "parentId": 604932984333766,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604973575345606,
                                                                    "name": "程序主文件",
                                                                    "nodeType": "prop",
                                                                    "parentId": 604971237696966,
                                                                    "nodeTypeAddition": "",
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "id": 604932315211206,
                                    "name": "叶片加工检测",
                                    "nodeType": "parameter_group",
                                    "parentId": 602543691515338,
                                    "nodeTypeAddition": "method",
                                    "children": [
                                        {
                                            "id": 604932673131974,
                                            "name": "叶片铣削加工",
                                            "nodeType": "parameter_group",
                                            "parentId": 604932315211206,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 604933158954438,
                                                    "name": "加工路径规划方法",
                                                    "nodeType": "parameter_group",
                                                    "parentId": 604932673131974,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 604971619222982,
                                                            "name": "入参参数组",
                                                            "nodeType": "parameter",
                                                            "parentId": 604933158954438,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604989531145670,
                                                                    "name": "curved_surface_control_point",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604971619222982,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 605004130657734,
                                                                            "name": "cpt_file",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604989531145670,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 604971632846278,
                                                            "name": "出参参数组",
                                                            "nodeType": "parameter",
                                                            "parentId": 604933158954438,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604993682183622,
                                                                    "name": "milling_tool_path",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604971632846278,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 605004211070406,
                                                                            "name": "X",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604993682183622,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605004223890886,
                                                                            "name": "Y",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604993682183622,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605004233213382,
                                                                            "name": "Z",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604993682183622,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605004245251526,
                                                                            "name": "I",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604993682183622,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605004254254534,
                                                                            "name": "J",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604993682183622,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605004265264582,
                                                                            "name": "K",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604993682183622,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                },
                                                                {
                                                                    "id": 604993713976774,
                                                                    "name": "milling_tool_path_txt",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604971632846278,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 605004330309062,
                                                                            "name": "xyzijk_file",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604993713976774,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 604971657991622,
                                                            "name": "程序文件",
                                                            "nodeType": "parameter",
                                                            "parentId": 604933158954438,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604973705258438,
                                                                    "name": "程序主文件",
                                                                    "nodeType": "prop",
                                                                    "parentId": 604971657991622,
                                                                    "nodeTypeAddition": "",
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 604933254206918,
                                                    "name": "加工铣削方法",
                                                    "nodeType": "parameter_group",
                                                    "parentId": 604932673131974,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 604971783665094,
                                                            "name": "入参参数组",
                                                            "nodeType": "parameter",
                                                            "parentId": 604933254206918,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604989695780294,
                                                                    "name": "NC_code",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604971783665094,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 605006337340870,
                                                                            "name": "txt_file",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604989695780294,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                },
                                                                {
                                                                    "id": 604989718955462,
                                                                    "name": "blade_blank_set",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604971783665094,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 605006386787782,
                                                                            "name": "Bar_code",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604989718955462,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 604971797116358,
                                                            "name": "出参参数组",
                                                            "nodeType": "parameter",
                                                            "parentId": 604933254206918,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604994016064966,
                                                                    "name": "blade_product_set",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604971797116358,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 605006476158406,
                                                                            "name": "Bar_code",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604994016064966,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                },
                                                                {
                                                                    "id": 604994040702406,
                                                                    "name": "machine_parameter",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604971797116358,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 605006535546310,
                                                                            "name": "Brand",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604994040702406,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605006556227014,
                                                                            "name": "Type",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604994040702406,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 604971815798214,
                                                            "name": "程序文件",
                                                            "nodeType": "parameter",
                                                            "parentId": 604933254206918,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604973758842310,
                                                                    "name": "程序主文件",
                                                                    "nodeType": "prop",
                                                                    "parentId": 604971815798214,
                                                                    "nodeTypeAddition": "",
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 604933232506310,
                                                    "name": "加工工艺设计方法",
                                                    "nodeType": "parameter_group",
                                                    "parentId": 604932673131974,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 604971710571974,
                                                            "name": "入参参数组",
                                                            "nodeType": "parameter",
                                                            "parentId": 604933232506310,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604989612713414,
                                                                    "name": "milling_tool_path_txt",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604971710571974,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 605005536044486,
                                                                            "name": "X",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604989612713414,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605005547099590,
                                                                            "name": "Y",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604989612713414,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605005557822918,
                                                                            "name": "Z",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604989612713414,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605005582833094,
                                                                            "name": "I",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604989612713414,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605005594359238,
                                                                            "name": "J",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604989612713414,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605005607208390,
                                                                            "name": "K",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604989612713414,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 604971724420550,
                                                            "name": "出参参数组",
                                                            "nodeType": "parameter",
                                                            "parentId": 604933232506310,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604993820251590,
                                                                    "name": "NC_code",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604971724420550,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 605005652784582,
                                                                            "name": "txt_file",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604993820251590,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 604971745379782,
                                                            "name": "程序文件",
                                                            "nodeType": "parameter",
                                                            "parentId": 604933232506310,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604973733746118,
                                                                    "name": "程序主文件",
                                                                    "nodeType": "prop",
                                                                    "parentId": 604971745379782,
                                                                    "nodeTypeAddition": "",
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "id": 604932702934470,
                                            "name": "叶片产品检测",
                                            "nodeType": "parameter_group",
                                            "parentId": 604932315211206,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 604933305103814,
                                                    "name": "常规检测方法",
                                                    "nodeType": "parameter_group",
                                                    "parentId": 604932702934470,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 604971887216070,
                                                            "name": "入参参数组",
                                                            "nodeType": "parameter",
                                                            "parentId": 604933305103814,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604989827302854,
                                                                    "name": "blade_product_set",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604971887216070,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 605027165754822,
                                                                            "name": "Bar_code",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604989827302854,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                },
                                                                {
                                                                    "id": 604989847504326,
                                                                    "name": "blade_test_taget",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604971887216070,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 605027211896262,
                                                                            "name": "Profile",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604989847504326,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605027231507910,
                                                                            "name": "Average_roughness",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604989847504326,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605027250537926,
                                                                            "name": "Qualified_or_not",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604989847504326,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605027277530566,
                                                                            "name": "Processing_time",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604989847504326,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 604971900880326,
                                                            "name": "出参参数组",
                                                            "nodeType": "parameter",
                                                            "parentId": 604933305103814,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604994249360838,
                                                                    "name": "blade_test_actual",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604971900880326,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 605027341723078,
                                                                            "name": "Profile",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604994249360838,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605027376108998,
                                                                            "name": "Average_roughness",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604994249360838,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605027397117382,
                                                                            "name": "Qualified_or_not",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604994249360838,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605027417650630,
                                                                            "name": "Processing_time",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604994249360838,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                },
                                                                {
                                                                    "id": 604994269369798,
                                                                    "name": "test_error",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604971900880326,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 605027486172614,
                                                                            "name": "Profile_error",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604994269369798,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605027506251206,
                                                                            "name": "Average_roughness_error",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604994269369798,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605027526673862,
                                                                            "name": "Qualified_or_not",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604994269369798,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605027548059078,
                                                                            "name": "Processing_time_error",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604994269369798,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 604971924809158,
                                                            "name": "程序文件",
                                                            "nodeType": "parameter",
                                                            "parentId": 604933305103814,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604973797103046,
                                                                    "name": "程序主文件",
                                                                    "nodeType": "prop",
                                                                    "parentId": 604971924809158,
                                                                    "nodeTypeAddition": "",
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 604933333202374,
                                                    "name": "视觉检测方法",
                                                    "nodeType": "parameter_group",
                                                    "parentId": 604932702934470,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 604972162528710,
                                                            "name": "入参参数组",
                                                            "nodeType": "parameter",
                                                            "parentId": 604933333202374,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604989919049158,
                                                                    "name": "CAD_file",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604972162528710,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 605027731535302,
                                                                            "name": "Bar_code",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604989919049158,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        },
                                                                        {
                                                                            "id": 605027750467014,
                                                                            "name": "obj_file",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604989919049158,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 604972176651718,
                                                            "name": "出参参数组",
                                                            "nodeType": "parameter",
                                                            "parentId": 604933333202374,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604994354484678,
                                                                    "name": "pcd_file",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604972176651718,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 605027853645254,
                                                                            "name": "Profile_error",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604994354484678,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 604972193207750,
                                                            "name": "程序文件",
                                                            "nodeType": "parameter",
                                                            "parentId": 604933333202374,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604973823940038,
                                                                    "name": "程序主文件",
                                                                    "nodeType": "prop",
                                                                    "parentId": 604972193207750,
                                                                    "nodeTypeAddition": "",
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "id": 604932338132422,
                                    "name": "叶片数据工程",
                                    "nodeType": "parameter_group",
                                    "parentId": 602543691515338,
                                    "nodeTypeAddition": "method",
                                    "children": [
                                        {
                                            "id": 604932770473414,
                                            "name": "叶片数据采集",
                                            "nodeType": "parameter_group",
                                            "parentId": 604932338132422,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 604933463360966,
                                                    "name": "实际数据采集",
                                                    "nodeType": "parameter_group",
                                                    "parentId": 604932770473414,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 604934042224070,
                                                            "name": "实际数据采集方法",
                                                            "nodeType": "parameter_group",
                                                            "parentId": 604933463360966,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604972949706182,
                                                                    "name": "入参参数组",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604934042224070,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 604990612051398,
                                                                            "name": "blade_product_set",
                                                                            "nodeType": "parameter",
                                                                            "parentId": 604972949706182,
                                                                            "nodeTypeAddition": "",
                                                                            "children": [
                                                                                {
                                                                                    "id": 605028903060934,
                                                                                    "name": "Bar_code",
                                                                                    "nodeType": "prop",
                                                                                    "parentId": 604990612051398,
                                                                                    "nodeTypeAddition": "",
                                                                                    "children": null
                                                                                }
                                                                            ]
                                                                        },
                                                                        {
                                                                            "id": 604990630651334,
                                                                            "name": "feature_dataset",
                                                                            "nodeType": "parameter",
                                                                            "parentId": 604972949706182,
                                                                            "nodeTypeAddition": "",
                                                                            "children": [
                                                                                {
                                                                                    "id": 605028946679238,
                                                                                    "name": "feature1",
                                                                                    "nodeType": "prop",
                                                                                    "parentId": 604990630651334,
                                                                                    "nodeTypeAddition": "",
                                                                                    "children": null
                                                                                },
                                                                                {
                                                                                    "id": 605028964869574,
                                                                                    "name": "feature2",
                                                                                    "nodeType": "prop",
                                                                                    "parentId": 604990630651334,
                                                                                    "nodeTypeAddition": "",
                                                                                    "children": null
                                                                                }
                                                                            ]
                                                                        }
                                                                    ]
                                                                },
                                                                {
                                                                    "id": 604972962416070,
                                                                    "name": "出参参数组",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604934042224070,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 604994990958022,
                                                                            "name": "feature_label_dataset",
                                                                            "nodeType": "parameter",
                                                                            "parentId": 604972962416070,
                                                                            "nodeTypeAddition": "",
                                                                            "children": [
                                                                                {
                                                                                    "id": 605029039650246,
                                                                                    "name": "feature1",
                                                                                    "nodeType": "prop",
                                                                                    "parentId": 604994990958022,
                                                                                    "nodeTypeAddition": "",
                                                                                    "children": null
                                                                                },
                                                                                {
                                                                                    "id": 605029052446150,
                                                                                    "name": "feature2",
                                                                                    "nodeType": "prop",
                                                                                    "parentId": 604994990958022,
                                                                                    "nodeTypeAddition": "",
                                                                                    "children": null
                                                                                },
                                                                                {
                                                                                    "id": 605029071058374,
                                                                                    "name": "label1",
                                                                                    "nodeType": "prop",
                                                                                    "parentId": 604994990958022,
                                                                                    "nodeTypeAddition": "",
                                                                                    "children": null
                                                                                },
                                                                                {
                                                                                    "id": 605029084370374,
                                                                                    "name": "label2",
                                                                                    "nodeType": "prop",
                                                                                    "parentId": 604994990958022,
                                                                                    "nodeTypeAddition": "",
                                                                                    "children": null
                                                                                }
                                                                            ]
                                                                        }
                                                                    ]
                                                                },
                                                                {
                                                                    "id": 604972978509254,
                                                                    "name": "程序文件",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604934042224070,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 604973936481734,
                                                                            "name": "程序主文件",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604972978509254,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 604933423347142,
                                                    "name": "试验数据采集",
                                                    "nodeType": "parameter_group",
                                                    "parentId": 604932770473414,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 604933970556358,
                                                            "name": "试验设计",
                                                            "nodeType": "parameter_group",
                                                            "parentId": 604933423347142,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604972710073798,
                                                                    "name": "入参参数组",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604933970556358,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 604990206342598,
                                                                            "name": "DOE_parameter",
                                                                            "nodeType": "parameter",
                                                                            "parentId": 604972710073798,
                                                                            "nodeTypeAddition": "",
                                                                            "children": [
                                                                                {
                                                                                    "id": 605028116805062,
                                                                                    "name": "doe1",
                                                                                    "nodeType": "prop",
                                                                                    "parentId": 604990206342598,
                                                                                    "nodeTypeAddition": "",
                                                                                    "children": null
                                                                                },
                                                                                {
                                                                                    "id": 605028138120646,
                                                                                    "name": "doe2",
                                                                                    "nodeType": "prop",
                                                                                    "parentId": 604990206342598,
                                                                                    "nodeTypeAddition": "",
                                                                                    "children": null
                                                                                }
                                                                            ]
                                                                        },
                                                                        {
                                                                            "id": 604990187533766,
                                                                            "name": "feature_dataset_ranged",
                                                                            "nodeType": "parameter",
                                                                            "parentId": 604972710073798,
                                                                            "nodeTypeAddition": "",
                                                                            "children": [
                                                                                {
                                                                                    "id": 605028050912710,
                                                                                    "name": "feature1",
                                                                                    "nodeType": "prop",
                                                                                    "parentId": 604990187533766,
                                                                                    "nodeTypeAddition": "",
                                                                                    "children": null
                                                                                },
                                                                                {
                                                                                    "id": 605028071015878,
                                                                                    "name": "feature2",
                                                                                    "nodeType": "prop",
                                                                                    "parentId": 604990187533766,
                                                                                    "nodeTypeAddition": "",
                                                                                    "children": null
                                                                                }
                                                                            ]
                                                                        }
                                                                    ]
                                                                },
                                                                {
                                                                    "id": 604972723234246,
                                                                    "name": "出参参数组",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604933970556358,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 604994525996486,
                                                                            "name": "feature_dataset",
                                                                            "nodeType": "parameter",
                                                                            "parentId": 604972723234246,
                                                                            "nodeTypeAddition": "",
                                                                            "children": [
                                                                                {
                                                                                    "id": 605028192114118,
                                                                                    "name": "feature1",
                                                                                    "nodeType": "prop",
                                                                                    "parentId": 604994525996486,
                                                                                    "nodeTypeAddition": "",
                                                                                    "children": null
                                                                                },
                                                                                {
                                                                                    "id": 605028213310918,
                                                                                    "name": "feature2",
                                                                                    "nodeType": "prop",
                                                                                    "parentId": 604994525996486,
                                                                                    "nodeTypeAddition": "",
                                                                                    "children": null
                                                                                }
                                                                            ]
                                                                        }
                                                                    ]
                                                                },
                                                                {
                                                                    "id": 604972753708486,
                                                                    "name": "程序文件",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604933970556358,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 604973866452422,
                                                                            "name": "程序主文件",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604972753708486,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 604933994534342,
                                                            "name": "试验数据采集",
                                                            "nodeType": "parameter_group",
                                                            "parentId": 604933423347142,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604972803937734,
                                                                    "name": "入参参数组",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604933994534342,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 604990328387014,
                                                                            "name": "blade_product_set",
                                                                            "nodeType": "parameter",
                                                                            "parentId": 604972803937734,
                                                                            "nodeTypeAddition": "",
                                                                            "children": [
                                                                                {
                                                                                    "id": 605028319172038,
                                                                                    "name": "Bar_code",
                                                                                    "nodeType": "prop",
                                                                                    "parentId": 604990328387014,
                                                                                    "nodeTypeAddition": "",
                                                                                    "children": null
                                                                                }
                                                                            ]
                                                                        },
                                                                        {
                                                                            "id": 604990349669830,
                                                                            "name": "feature_dataset",
                                                                            "nodeType": "parameter",
                                                                            "parentId": 604972803937734,
                                                                            "nodeTypeAddition": "",
                                                                            "children": [
                                                                                {
                                                                                    "id": 605028362757574,
                                                                                    "name": "feature1",
                                                                                    "nodeType": "prop",
                                                                                    "parentId": 604990349669830,
                                                                                    "nodeTypeAddition": "",
                                                                                    "children": null
                                                                                },
                                                                                {
                                                                                    "id": 605028381328838,
                                                                                    "name": "feature2",
                                                                                    "nodeType": "prop",
                                                                                    "parentId": 604990349669830,
                                                                                    "nodeTypeAddition": "",
                                                                                    "children": null
                                                                                }
                                                                            ]
                                                                        }
                                                                    ]
                                                                },
                                                                {
                                                                    "id": 604972861953478,
                                                                    "name": "出参参数组",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604933994534342,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 604994624529862,
                                                                            "name": "feature_label_dataset",
                                                                            "nodeType": "parameter",
                                                                            "parentId": 604972861953478,
                                                                            "nodeTypeAddition": "",
                                                                            "children": [
                                                                                {
                                                                                    "id": 605028645279174,
                                                                                    "name": "feature1",
                                                                                    "nodeType": "prop",
                                                                                    "parentId": 604994624529862,
                                                                                    "nodeTypeAddition": "",
                                                                                    "children": null
                                                                                },
                                                                                {
                                                                                    "id": 605028658070982,
                                                                                    "name": "feature2",
                                                                                    "nodeType": "prop",
                                                                                    "parentId": 604994624529862,
                                                                                    "nodeTypeAddition": "",
                                                                                    "children": null
                                                                                },
                                                                                {
                                                                                    "id": 605028679685574,
                                                                                    "name": "label1",
                                                                                    "nodeType": "prop",
                                                                                    "parentId": 604994624529862,
                                                                                    "nodeTypeAddition": "",
                                                                                    "children": null
                                                                                },
                                                                                {
                                                                                    "id": 605028692858310,
                                                                                    "name": "label2",
                                                                                    "nodeType": "prop",
                                                                                    "parentId": 604994624529862,
                                                                                    "nodeTypeAddition": "",
                                                                                    "children": null
                                                                                }
                                                                            ]
                                                                        }
                                                                    ]
                                                                },
                                                                {
                                                                    "id": 604972878808518,
                                                                    "name": "程序文件",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604933994534342,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 604973893100998,
                                                                            "name": "程序主文件",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604972878808518,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "id": 604932797416902,
                                            "name": "叶片数据治理",
                                            "nodeType": "parameter_group",
                                            "parentId": 604932338132422,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 604933531018694,
                                                    "name": "叶片数据筛选",
                                                    "nodeType": "parameter_group",
                                                    "parentId": 604932797416902,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 604933826471366,
                                                            "name": "筛选模型训练方法",
                                                            "nodeType": "parameter_group",
                                                            "parentId": 604933531018694,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604973057631686,
                                                                    "name": "入参参数组",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604933826471366,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 604990730630598,
                                                                            "name": "feature_label_dataset",
                                                                            "nodeType": "parameter",
                                                                            "parentId": 604973057631686,
                                                                            "nodeTypeAddition": "",
                                                                            "children": [
                                                                                {
                                                                                    "id": 605029269112262,
                                                                                    "name": "dataset",
                                                                                    "nodeType": "prop",
                                                                                    "parentId": 604990730630598,
                                                                                    "nodeTypeAddition": "",
                                                                                    "children": null
                                                                                }
                                                                            ]
                                                                        }
                                                                    ]
                                                                },
                                                                {
                                                                    "id": 604973070243270,
                                                                    "name": "出参参数组",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604933826471366,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 604995534845382,
                                                                            "name": "model_weight",
                                                                            "nodeType": "parameter",
                                                                            "parentId": 604973070243270,
                                                                            "nodeTypeAddition": "",
                                                                            "children": [
                                                                                {
                                                                                    "id": 605029307700678,
                                                                                    "name": "wgt_file",
                                                                                    "nodeType": "prop",
                                                                                    "parentId": 604995534845382,
                                                                                    "nodeTypeAddition": "",
                                                                                    "children": null
                                                                                }
                                                                            ]
                                                                        }
                                                                    ]
                                                                },
                                                                {
                                                                    "id": 604973091669446,
                                                                    "name": "程序文件",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604933826471366,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 604973987214790,
                                                                            "name": "程序主文件",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604973091669446,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 604933852771782,
                                                            "name": "AI数据筛选方法",
                                                            "nodeType": "parameter_group",
                                                            "parentId": 604933531018694,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 604973140891078,
                                                                    "name": "入参参数组",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604933852771782,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 604991679509958,
                                                                            "name": "feature_label_dataset",
                                                                            "nodeType": "parameter",
                                                                            "parentId": 604973140891078,
                                                                            "nodeTypeAddition": "",
                                                                            "children": [
                                                                                {
                                                                                    "id": 605029420406214,
                                                                                    "name": "dataset",
                                                                                    "nodeType": "prop",
                                                                                    "parentId": 604991679509958,
                                                                                    "nodeTypeAddition": "",
                                                                                    "children": null
                                                                                },
                                                                                {
                                                                                    "id": 605029437162950,
                                                                                    "name": "wgt_file",
                                                                                    "nodeType": "prop",
                                                                                    "parentId": 604991679509958,
                                                                                    "nodeTypeAddition": "",
                                                                                    "children": null
                                                                                }
                                                                            ]
                                                                        },
                                                                        {
                                                                            "id": 604991706301894,
                                                                            "name": "model_weight",
                                                                            "nodeType": "parameter",
                                                                            "parentId": 604973140891078,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                },
                                                                {
                                                                    "id": 604973154710982,
                                                                    "name": "出参参数组",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604933852771782,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 604995609740742,
                                                                            "name": "filtered_feature_label_dataset",
                                                                            "nodeType": "parameter",
                                                                            "parentId": 604973154710982,
                                                                            "nodeTypeAddition": "",
                                                                            "children": [
                                                                                {
                                                                                    "id": 605029476890054,
                                                                                    "name": "filtered_feature",
                                                                                    "nodeType": "prop",
                                                                                    "parentId": 604995609740742,
                                                                                    "nodeTypeAddition": "",
                                                                                    "children": null
                                                                                }
                                                                            ]
                                                                        }
                                                                    ]
                                                                },
                                                                {
                                                                    "id": 604973169608134,
                                                                    "name": "程序文件",
                                                                    "nodeType": "parameter",
                                                                    "parentId": 604933852771782,
                                                                    "nodeTypeAddition": "",
                                                                    "children": [
                                                                        {
                                                                            "id": 604974014404038,
                                                                            "name": "程序主文件",
                                                                            "nodeType": "prop",
                                                                            "parentId": 604973169608134,
                                                                            "nodeTypeAddition": "",
                                                                            "children": null
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "id": 604932358731206,
                                    "name": "叶片AI优化",
                                    "nodeType": "parameter_group",
                                    "parentId": 602543691515338,
                                    "nodeTypeAddition": "method",
                                    "children": [
                                        {
                                            "id": 604932420109766,
                                            "name": "AI推荐训练方法",
                                            "nodeType": "parameter_group",
                                            "parentId": 604932358731206,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 604973230654918,
                                                    "name": "入参参数组",
                                                    "nodeType": "parameter",
                                                    "parentId": 604932420109766,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 604991774344646,
                                                            "name": "filtered_feature_label_dataset",
                                                            "nodeType": "parameter",
                                                            "parentId": 604973230654918,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 605029559301574,
                                                                    "name": "dataset",
                                                                    "nodeType": "prop",
                                                                    "parentId": 604991774344646,
                                                                    "nodeTypeAddition": "",
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 604973243925958,
                                                    "name": "出参参数组",
                                                    "nodeType": "parameter",
                                                    "parentId": 604932420109766,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 604995725247942,
                                                            "name": "model_weight",
                                                            "nodeType": "parameter",
                                                            "parentId": 604973243925958,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 605029599270342,
                                                                    "name": "wgt_file",
                                                                    "nodeType": "prop",
                                                                    "parentId": 604995725247942,
                                                                    "nodeTypeAddition": "",
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 604973263603142,
                                                    "name": "程序文件",
                                                    "nodeType": "parameter",
                                                    "parentId": 604932420109766,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 604974066476486,
                                                            "name": "程序主文件",
                                                            "nodeType": "parameter",
                                                            "parentId": 604973263603142,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "id": 604932449994182,
                                            "name": "AI参数推荐方法",
                                            "nodeType": "parameter_group",
                                            "parentId": 604932358731206,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 604973299922374,
                                                    "name": "入参参数组",
                                                    "nodeType": "parameter",
                                                    "parentId": 604932449994182,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 604991827011014,
                                                            "name": "designate_parameter",
                                                            "nodeType": "parameter",
                                                            "parentId": 604973299922374,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 605029661324742,
                                                                    "name": "dataset",
                                                                    "nodeType": "prop",
                                                                    "parentId": 604991827011014,
                                                                    "nodeTypeAddition": "",
                                                                    "children": null
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 604991845627334,
                                                            "name": "model_weight",
                                                            "nodeType": "parameter",
                                                            "parentId": 604973299922374,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 605029695190470,
                                                                    "name": "wgt_file",
                                                                    "nodeType": "prop",
                                                                    "parentId": 604991845627334,
                                                                    "nodeTypeAddition": "",
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 604973313209798,
                                                    "name": "出参参数组",
                                                    "nodeType": "parameter",
                                                    "parentId": 604932449994182,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 604995790140870,
                                                            "name": "recommand_parameter",
                                                            "nodeType": "parameter",
                                                            "parentId": 604973313209798,
                                                            "nodeTypeAddition": "",
                                                            "children": [
                                                                {
                                                                    "id": 605029743646150,
                                                                    "name": "optimized_data",
                                                                    "nodeType": "prop",
                                                                    "parentId": 604995790140870,
                                                                    "nodeTypeAddition": "",
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 604973327136198,
                                                    "name": "程序文件",
                                                    "nodeType": "parameter",
                                                    "parentId": 604932449994182,
                                                    "nodeTypeAddition": "",
                                                    "children": [
                                                        {
                                                            "id": 604974085629382,
                                                            "name": "程序主文件",
                                                            "nodeType": "parameter",
                                                            "parentId": 604973327136198,
                                                            "nodeTypeAddition": "",
                                                            "children": null
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "id": 604937932891590,
                            "name": "feature",
                            "nodeType": "parameter",
                            "parentId": 602543691511238,
                            "nodeTypeAddition": "",
                            "children": [
                                {
                                    "id": 604939377518022,
                                    "name": "feature 0",
                                    "nodeType": "prop",
                                    "parentId": 604937932891590,
                                    "nodeTypeAddition": "",
                                    "children": null
                                },
                                {
                                    "id": 604939396416966,
                                    "name": "feature 1",
                                    "nodeType": "prop",
                                    "parentId": 604937932891590,
                                    "nodeTypeAddition": "",
                                    "children": null
                                },
                                {
                                    "id": 604939409556934,
                                    "name": "feature 2",
                                    "nodeType": "prop",
                                    "parentId": 604937932891590,
                                    "nodeTypeAddition": "",
                                    "children": null
                                }
                            ]
                        },
                        {
                            "id": 604937966396870,
                            "name": "label",
                            "nodeType": "parameter",
                            "parentId": 602543691511238,
                            "nodeTypeAddition": "",
                            "children": [
                                {
                                    "id": 604939471156678,
                                    "name": "label 0",
                                    "nodeType": "prop",
                                    "parentId": 604937966396870,
                                    "nodeTypeAddition": "",
                                    "children": null
                                },
                                {
                                    "id": 604939484771782,
                                    "name": "label 1",
                                    "nodeType": "prop",
                                    "parentId": 604937966396870,
                                    "nodeTypeAddition": "",
                                    "children": null
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "id": 602543219627463,
            "name": "insofrobot",
            "nodeType": "supermodel",
            "parentId": 602543219574214,
            "nodeTypeAddition": null,
            "children": [
                {
                    "id": 602543727117766,
                    "name": "insoftube",
                    "nodeType": "model",
                    "parentId": 602543219627463,
                    "nodeTypeAddition": null,
                    "children": [
                        {
                            "id": 602543727117767,
                            "name": "人员",
                            "nodeType": "person",
                            "parentId": 602543727117766,
                            "nodeTypeAddition": null,
                            "children": null
                        },
                        {
                            "id": 602543727117768,
                            "name": "机器",
                            "nodeType": "machine",
                            "parentId": 602543727117766,
                            "nodeTypeAddition": null,
                            "children": [
                                {
                                    "id": 603520836933062,
                                    "name": "设备",
                                    "nodeType": "parameter_group",
                                    "parentId": 602543727117768,
                                    "nodeTypeAddition": null,
                                    "children": [
                                        {
                                            "id": 603520894277062,
                                            "name": "弯管机",
                                            "nodeType": "parameter_group",
                                            "parentId": 603520836933062,
                                            "nodeTypeAddition": null,
                                            "children": [
                                                {
                                                    "id": 603521322644934,
                                                    "name": "旋转装置",
                                                    "nodeType": "parameter_group",
                                                    "parentId": 603520894277062,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603551099930054,
                                                            "name": "旋转装置参数",
                                                            "nodeType": "parameter",
                                                            "parentId": 603521322644934,
                                                            "nodeTypeAddition": null,
                                                            "children": [
                                                                {
                                                                    "id": 603556477830598,
                                                                    "name": "模型文件",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551099930054,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603556504757702,
                                                                    "name": "活动类型",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551099930054,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603556524967366,
                                                                    "name": "最小范围",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551099930054,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603556544484806,
                                                                    "name": "最大范围",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551099930054,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603556563629510,
                                                                    "name": "最大速度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551099930054,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603556583929286,
                                                                    "name": "轴点",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551099930054,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603556604204486,
                                                                    "name": "轴方向",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551099930054,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603521407522246,
                                                    "name": "摆臂装置",
                                                    "nodeType": "parameter_group",
                                                    "parentId": 603520894277062,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603551224313286,
                                                            "name": "摆臂装置参数",
                                                            "nodeType": "parameter",
                                                            "parentId": 603521407522246,
                                                            "nodeTypeAddition": null,
                                                            "children": [
                                                                {
                                                                    "id": 603556695852486,
                                                                    "name": "模型文件",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551224313286,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603556719498694,
                                                                    "name": "活动类型",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551224313286,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603556740048326,
                                                                    "name": "最小范围",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551224313286,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603556759578054,
                                                                    "name": "最大范围",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551224313286,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603556776285638,
                                                                    "name": "最大速度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551224313286,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603556796868038,
                                                                    "name": "轴点",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551224313286,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603556816590278,
                                                                    "name": "轴方向",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551224313286,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603521432585670,
                                                    "name": "主夹装置",
                                                    "nodeType": "parameter_group",
                                                    "parentId": 603520894277062,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603551445124550,
                                                            "name": "主夹装置参数",
                                                            "nodeType": "parameter",
                                                            "parentId": 603521432585670,
                                                            "nodeTypeAddition": null,
                                                            "children": [
                                                                {
                                                                    "id": 603557021328838,
                                                                    "name": "名称",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551445124550,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557043062214,
                                                                    "name": "模型文件",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551445124550,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557062976966,
                                                                    "name": "层数",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551445124550,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557085242822,
                                                                    "name": "类型",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551445124550,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557104874950,
                                                                    "name": "弯曲半径",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551445124550,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557125395910,
                                                                    "name": "匹配管径",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551445124550,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557147583942,
                                                                    "name": "模具高度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551445124550,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557166253510,
                                                                    "name": "中心高",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551445124550,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557186340294,
                                                                    "name": "脱模长度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551445124550,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557206545862,
                                                                    "name": "主夹宽度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551445124550,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557226182086,
                                                                    "name": "导夹长度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551445124550,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557258831302,
                                                                    "name": "导夹宽度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551445124550,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603521467295174,
                                                    "name": "导夹装置",
                                                    "nodeType": "parameter_group",
                                                    "parentId": 603520894277062,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603551545046470,
                                                            "name": "导夹装置参数",
                                                            "nodeType": "parameter",
                                                            "parentId": 603521467295174,
                                                            "nodeTypeAddition": null,
                                                            "children": [
                                                                {
                                                                    "id": 603557355738566,
                                                                    "name": "名称",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551545046470,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557382366662,
                                                                    "name": "模型文件",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551545046470,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557401146822,
                                                                    "name": "层数",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551545046470,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557419136454,
                                                                    "name": "类型",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551545046470,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557441263046,
                                                                    "name": "弯曲半径",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551545046470,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557461579206,
                                                                    "name": "匹配管径",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551545046470,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557479986630,
                                                                    "name": "模具高度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551545046470,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557496419782,
                                                                    "name": "中心高",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551545046470,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557517985222,
                                                                    "name": "脱模长度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551545046470,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557537703366,
                                                                    "name": "主夹宽度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551545046470,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557555566022,
                                                                    "name": "导夹长度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551545046470,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557575579078,
                                                                    "name": "导夹宽度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551545046470,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603521489565126,
                                                    "name": "弯管机支座",
                                                    "nodeType": "parameter_group",
                                                    "parentId": 603520894277062,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603551328216518,
                                                            "name": "弯管机支座参数",
                                                            "nodeType": "parameter",
                                                            "parentId": 603521489565126,
                                                            "nodeTypeAddition": null,
                                                            "children": [
                                                                {
                                                                    "id": 603556915955142,
                                                                    "name": "模型文件",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551328216518,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603521519195590,
                                                    "name": "模具",
                                                    "nodeType": "parameter_group",
                                                    "parentId": 603520894277062,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603551642281414,
                                                            "name": "模具参数",
                                                            "nodeType": "parameter",
                                                            "parentId": 603521519195590,
                                                            "nodeTypeAddition": null,
                                                            "children": [
                                                                {
                                                                    "id": 603557673215430,
                                                                    "name": "名称",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551642281414,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557692593606,
                                                                    "name": "模型文件",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551642281414,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557714585030,
                                                                    "name": "层数",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551642281414,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557736056262,
                                                                    "name": "类型",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551642281414,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557753984454,
                                                                    "name": "弯曲半径",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551642281414,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557775173062,
                                                                    "name": "匹配管径",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551642281414,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557794633158,
                                                                    "name": "模具高度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551642281414,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557815444934,
                                                                    "name": "中心高",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551642281414,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557836801478,
                                                                    "name": "脱模长度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551642281414,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557857899974,
                                                                    "name": "主夹宽度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551642281414,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557877687750,
                                                                    "name": "导夹长度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551642281414,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603557897532870,
                                                                    "name": "导夹宽度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551642281414,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603550957233606,
                                                    "name": "弯管机参数",
                                                    "nodeType": "parameter",
                                                    "parentId": 603520894277062,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603554981443014,
                                                            "name": "编号",
                                                            "nodeType": "prop",
                                                            "parentId": 603550957233606,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603556216956358,
                                                            "name": "模型文件",
                                                            "nodeType": "prop",
                                                            "parentId": 603550957233606,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603556237141446,
                                                            "name": "主夹安装面至轮模中心距离",
                                                            "nodeType": "prop",
                                                            "parentId": 603550957233606,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603556258440646,
                                                            "name": "导夹安装面至轮模中心距离",
                                                            "nodeType": "prop",
                                                            "parentId": 603550957233606,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603556281869766,
                                                            "name": "左右弯轮模安装高度差",
                                                            "nodeType": "prop",
                                                            "parentId": 603550957233606,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603556305024454,
                                                            "name": "安装坐标系",
                                                            "nodeType": "prop",
                                                            "parentId": 603550957233606,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603556326016454,
                                                            "name": "世界坐标系",
                                                            "nodeType": "prop",
                                                            "parentId": 603550957233606,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603556355032518,
                                                            "name": "machine_toml_config_path",
                                                            "nodeType": "prop",
                                                            "parentId": 603550957233606,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603556379608518,
                                                            "name": "Processing_info",
                                                            "nodeType": "prop",
                                                            "parentId": 603550957233606,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "id": 603520967517638,
                                            "name": "机器人",
                                            "nodeType": "parameter_group",
                                            "parentId": 603520836933062,
                                            "nodeTypeAddition": null,
                                            "children": [
                                                {
                                                    "id": 603521740170694,
                                                    "name": "机械臂",
                                                    "nodeType": "parameter_group",
                                                    "parentId": 603520967517638,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603551842596294,
                                                            "name": "机械臂参数",
                                                            "nodeType": "parameter",
                                                            "parentId": 603521740170694,
                                                            "nodeTypeAddition": null,
                                                            "children": [
                                                                {
                                                                    "id": 603558168778182,
                                                                    "name": "模型文件",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551842596294,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603558188959174,
                                                                    "name": "活动类型",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551842596294,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603558208464326,
                                                                    "name": "最小范围",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551842596294,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603558227670470,
                                                                    "name": "最大范围",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551842596294,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603558247577030,
                                                                    "name": "最大速度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551842596294,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603558267073990,
                                                                    "name": "轴点",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551842596294,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603558288373190,
                                                                    "name": "轴方向",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603551842596294,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603551745811910,
                                                    "name": "机器人参数",
                                                    "nodeType": "parameter",
                                                    "parentId": 603520967517638,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603558015178182,
                                                            "name": "机器人编号",
                                                            "nodeType": "prop",
                                                            "parentId": 603551745811910,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603558036018630,
                                                            "name": "模型文件",
                                                            "nodeType": "prop",
                                                            "parentId": 603551745811910,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603558062593478,
                                                            "name": "DH",
                                                            "nodeType": "prop",
                                                            "parentId": 603551745811910,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603558087833030,
                                                            "name": "机器人坐标系",
                                                            "nodeType": "prop",
                                                            "parentId": 603551745811910,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603558107530694,
                                                            "name": "工具坐标系",
                                                            "nodeType": "prop",
                                                            "parentId": 603551745811910,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "id": 603520993416646,
                                            "name": "手抓",
                                            "nodeType": "parameter_group",
                                            "parentId": 603520836933062,
                                            "nodeTypeAddition": null,
                                            "children": [
                                                {
                                                    "id": 603551931049414,
                                                    "name": "手抓参数",
                                                    "nodeType": "parameter",
                                                    "parentId": 603520993416646,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603558369859014,
                                                            "name": "模型文件",
                                                            "nodeType": "prop",
                                                            "parentId": 603551931049414,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603558388557254,
                                                            "name": "手抓长度",
                                                            "nodeType": "prop",
                                                            "parentId": 603551931049414,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603558408103366,
                                                            "name": "手抓中心点",
                                                            "nodeType": "prop",
                                                            "parentId": 603551931049414,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603558426486214,
                                                            "name": "手抓坐标",
                                                            "nodeType": "prop",
                                                            "parentId": 603551931049414,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603558445000134,
                                                            "name": "手抓速度",
                                                            "nodeType": "prop",
                                                            "parentId": 603551931049414,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "id": 603521011574214,
                                            "name": "底座",
                                            "nodeType": "parameter_group",
                                            "parentId": 603520836933062,
                                            "nodeTypeAddition": null,
                                            "children": [
                                                {
                                                    "id": 603552000746950,
                                                    "name": "底座参数",
                                                    "nodeType": "parameter",
                                                    "parentId": 603521011574214,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603558517179846,
                                                            "name": "模型文件",
                                                            "nodeType": "prop",
                                                            "parentId": 603552000746950,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603558536275398,
                                                            "name": "底座宽度",
                                                            "nodeType": "prop",
                                                            "parentId": 603552000746950,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603558556210630,
                                                            "name": "底座高度",
                                                            "nodeType": "prop",
                                                            "parentId": 603552000746950,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "id": 602543727117769,
                            "name": "物料",
                            "nodeType": "product",
                            "parentId": 602543727117766,
                            "nodeTypeAddition": null,
                            "children": [
                                {
                                    "id": 603519850382790,
                                    "name": "产品",
                                    "nodeType": "parameter_group",
                                    "parentId": 602543727117769,
                                    "nodeTypeAddition": null,
                                    "children": [
                                        {
                                            "id": 603520605418950,
                                            "name": "管件",
                                            "nodeType": "parameter_group",
                                            "parentId": 603519850382790,
                                            "nodeTypeAddition": null,
                                            "children": [
                                                {
                                                    "id": 603524923348422,
                                                    "name": "工件基本参数",
                                                    "nodeType": "parameter",
                                                    "parentId": 603520605418950,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603553750369734,
                                                            "name": "名称",
                                                            "nodeType": "prop",
                                                            "parentId": 603524923348422,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603554034288070,
                                                            "name": "模型文件",
                                                            "nodeType": "prop",
                                                            "parentId": 603524923348422,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603554062071238,
                                                            "name": "方式",
                                                            "nodeType": "prop",
                                                            "parentId": 603524923348422,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603554085832134,
                                                            "name": "管长",
                                                            "nodeType": "prop",
                                                            "parentId": 603524923348422,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603554107454918,
                                                            "name": "内径",
                                                            "nodeType": "prop",
                                                            "parentId": 603524923348422,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603554128377286,
                                                            "name": "外径",
                                                            "nodeType": "prop",
                                                            "parentId": 603524923348422,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603554148324806,
                                                            "name": "厚度",
                                                            "nodeType": "prop",
                                                            "parentId": 603524923348422,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603554166179270,
                                                            "name": "first_seg_length",
                                                            "nodeType": "prop",
                                                            "parentId": 603524923348422,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603554184222150,
                                                            "name": "min_mid_seg_length",
                                                            "nodeType": "prop",
                                                            "parentId": 603524923348422,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603554205836742,
                                                            "name": "last_seg_length",
                                                            "nodeType": "prop",
                                                            "parentId": 603524923348422,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603554225096134,
                                                            "name": "夹持段编号",
                                                            "nodeType": "prop",
                                                            "parentId": 603524923348422,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603554245367238,
                                                            "name": "夹持线长比例",
                                                            "nodeType": "prop",
                                                            "parentId": 603524923348422,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603554274055622,
                                                            "name": "XYZ",
                                                            "nodeType": "prop",
                                                            "parentId": 603524923348422,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603554297529798,
                                                            "name": "YBC",
                                                            "nodeType": "prop",
                                                            "parentId": 603524923348422,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603554319025606,
                                                            "name": "material",
                                                            "nodeType": "prop",
                                                            "parentId": 603524923348422,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603554343699910,
                                                            "name": "needReverse",
                                                            "nodeType": "prop",
                                                            "parentId": 603524923348422,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "id": 602543727121862,
                            "name": "过程",
                            "nodeType": "procedure",
                            "parentId": 602543727117766,
                            "nodeTypeAddition": null,
                            "children": [
                                {
                                    "id": 603592521110982,
                                    "name": "工作单元选择",
                                    "nodeType": "parameter_group",
                                    "parentId": 602543727121862,
                                    "nodeTypeAddition": null,
                                    "children": [
                                        {
                                            "id": 603592576169414,
                                            "name": "管件解析",
                                            "nodeType": "parameter_group",
                                            "parentId": 603592521110982,
                                            "nodeTypeAddition": null,
                                            "children": [
                                                {
                                                    "id": 603594588595654,
                                                    "name": "单元名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 603592576169414,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603596869879238,
                                                            "name": "管件",
                                                            "nodeType": "prop",
                                                            "parentId": 603594588595654,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603595111757254,
                                                    "name": "算法名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 603592576169414,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603597066257862,
                                                            "name": "管件解析",
                                                            "nodeType": "prop",
                                                            "parentId": 603595111757254,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "id": 603592661509574,
                                    "name": "加工工艺生成",
                                    "nodeType": "parameter_group",
                                    "parentId": 602543727121862,
                                    "nodeTypeAddition": null,
                                    "children": [
                                        {
                                            "id": 603592795489734,
                                            "name": "模具匹配",
                                            "nodeType": "parameter_group",
                                            "parentId": 603592661509574,
                                            "nodeTypeAddition": null,
                                            "children": [
                                                {
                                                    "id": 603594648098246,
                                                    "name": "单元名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 603592795489734,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603597183284678,
                                                            "name": "管件",
                                                            "nodeType": "prop",
                                                            "parentId": 603594648098246,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603597223323078,
                                                            "name": "模具",
                                                            "nodeType": "prop",
                                                            "parentId": 603594648098246,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603597266724294,
                                                            "name": "弯管机",
                                                            "nodeType": "prop",
                                                            "parentId": 603594648098246,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603595074954694,
                                                    "name": "算法名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 603592795489734,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603599537038790,
                                                            "name": "模具匹配方法",
                                                            "nodeType": "prop",
                                                            "parentId": 603595074954694,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "id": 603592824313286,
                                            "name": "加工工艺生成",
                                            "nodeType": "parameter_group",
                                            "parentId": 603592661509574,
                                            "nodeTypeAddition": null,
                                            "children": [
                                                {
                                                    "id": 603594692826566,
                                                    "name": "单元名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 603592824313286,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603597411521990,
                                                            "name": "管件",
                                                            "nodeType": "prop",
                                                            "parentId": 603594692826566,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603597436327366,
                                                            "name": "模具",
                                                            "nodeType": "prop",
                                                            "parentId": 603594692826566,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603597459699142,
                                                            "name": "弯管机",
                                                            "nodeType": "prop",
                                                            "parentId": 603594692826566,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603595040544198,
                                                    "name": "算法名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 603592824313286,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603599631058374,
                                                            "name": "加工工艺生成方法",
                                                            "nodeType": "prop",
                                                            "parentId": 603595040544198,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "id": 603592842986950,
                                            "name": "补偿设置",
                                            "nodeType": "parameter_group",
                                            "parentId": 603592661509574,
                                            "nodeTypeAddition": null,
                                            "children": [
                                                {
                                                    "id": 603594732725702,
                                                    "name": "单元名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 603592842986950,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603597602760134,
                                                            "name": "弯管机",
                                                            "nodeType": "prop",
                                                            "parentId": 603594732725702,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603597629605318,
                                                            "name": "管件",
                                                            "nodeType": "prop",
                                                            "parentId": 603594732725702,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603597675095494,
                                                            "name": "模具",
                                                            "nodeType": "prop",
                                                            "parentId": 603594732725702,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603595005408710,
                                                    "name": "算法名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 603592842986950,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603599705126342,
                                                            "name": "补偿设置方法",
                                                            "nodeType": "prop",
                                                            "parentId": 603595005408710,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "id": 603592861242822,
                                            "name": "仿真分析",
                                            "nodeType": "parameter_group",
                                            "parentId": 603592661509574,
                                            "nodeTypeAddition": null,
                                            "children": [
                                                {
                                                    "id": 603594772268486,
                                                    "name": "单元名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 603592861242822,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603597742949830,
                                                            "name": "管件",
                                                            "nodeType": "prop",
                                                            "parentId": 603594772268486,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603597772010950,
                                                            "name": "模具",
                                                            "nodeType": "prop",
                                                            "parentId": 603594772268486,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603597805262278,
                                                            "name": "弯管机",
                                                            "nodeType": "prop",
                                                            "parentId": 603594772268486,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603594972673478,
                                                    "name": "算法名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 603592861242822,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603599781316038,
                                                            "name": "仿真分析方法",
                                                            "nodeType": "prop",
                                                            "parentId": 603594972673478,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "id": 603592879056326,
                                            "name": "干涉分析",
                                            "nodeType": "parameter_group",
                                            "parentId": 603592661509574,
                                            "nodeTypeAddition": null,
                                            "children": [
                                                {
                                                    "id": 603594821457350,
                                                    "name": "单元名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 603592879056326,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603597873931718,
                                                            "name": "管件",
                                                            "nodeType": "prop",
                                                            "parentId": 603594821457350,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603597898319302,
                                                            "name": "模具",
                                                            "nodeType": "prop",
                                                            "parentId": 603594821457350,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603597920695750,
                                                            "name": "弯管机",
                                                            "nodeType": "prop",
                                                            "parentId": 603594821457350,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603594941949382,
                                                    "name": "算法名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 603592879056326,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603599856031174,
                                                            "name": "干涉分析方法",
                                                            "nodeType": "prop",
                                                            "parentId": 603594941949382,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "id": 603592899069382,
                                            "name": "加工程序生成",
                                            "nodeType": "parameter_group",
                                            "parentId": 603592661509574,
                                            "nodeTypeAddition": null,
                                            "children": [
                                                {
                                                    "id": 603594855503302,
                                                    "name": "单元名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 603592899069382,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603597986887110,
                                                            "name": "管件",
                                                            "nodeType": "prop",
                                                            "parentId": 603594855503302,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603598008419782,
                                                            "name": "模具",
                                                            "nodeType": "prop",
                                                            "parentId": 603594855503302,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        },
                                                        {
                                                            "id": 603598029809094,
                                                            "name": "弯管机",
                                                            "nodeType": "prop",
                                                            "parentId": 603594855503302,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603594899072454,
                                                    "name": "算法名称",
                                                    "nodeType": "parameter",
                                                    "parentId": 603592899069382,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603599919125958,
                                                            "name": "加工程序生成方法",
                                                            "nodeType": "prop",
                                                            "parentId": 603594899072454,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "id": 602543727121863,
                            "name": "方法",
                            "nodeType": "method",
                            "parentId": 602543727117766,
                            "nodeTypeAddition": null,
                            "children": [
                                {
                                    "id": 603562084623814,
                                    "name": "模型解析",
                                    "nodeType": "parameter_group",
                                    "parentId": 602543727121863,
                                    "nodeTypeAddition": null,
                                    "children": [
                                        {
                                            "id": 603562190308806,
                                            "name": "管件解析",
                                            "nodeType": "parameter_group",
                                            "parentId": 603562084623814,
                                            "nodeTypeAddition": null,
                                            "children": [
                                                {
                                                    "id": 603564378662342,
                                                    "name": "程序文件",
                                                    "nodeType": "parameter",
                                                    "parentId": 603562190308806,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603567439345094,
                                                            "name": "程序主文件",
                                                            "nodeType": "prop",
                                                            "parentId": 603564378662342,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603575063152070,
                                                    "name": "入参参数组",
                                                    "nodeType": "parameter",
                                                    "parentId": 603562190308806,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603564537427398,
                                                            "name": "工件基本参数",
                                                            "nodeType": "parameter",
                                                            "parentId": 603575063152070,
                                                            "nodeTypeAddition": null,
                                                            "children": [
                                                                {
                                                                    "id": 603569267979718,
                                                                    "name": "名称",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564537427398,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569289184710,
                                                                    "name": "模型文件",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564537427398,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569309947334,
                                                                    "name": "方式",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564537427398,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569327990214,
                                                                    "name": "管长",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564537427398,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569350948294,
                                                                    "name": "内径",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564537427398,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569368548806,
                                                                    "name": "外径",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564537427398,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569387025862,
                                                                    "name": "厚度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564537427398,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569409406406,
                                                                    "name": "first_seg_length",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564537427398,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569428051398,
                                                                    "name": "min_mid_seg_length",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564537427398,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569448326598,
                                                                    "name": "last_seg_length",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564537427398,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569468765638,
                                                                    "name": "夹持段编号",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564537427398,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569486878150,
                                                                    "name": "夹持线长比例",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564537427398,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569509807558,
                                                                    "name": "XYZ",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564537427398,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569527731654,
                                                                    "name": "YBC",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564537427398,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569547851206,
                                                                    "name": "material",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564537427398,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569567778246,
                                                                    "name": "needReverse",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564537427398,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603575083804102,
                                                    "name": "出参参数组",
                                                    "nodeType": "parameter",
                                                    "parentId": 603562190308806,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603580461049286,
                                                            "name": "工件基本参数",
                                                            "nodeType": "parameter",
                                                            "parentId": 603575083804102,
                                                            "nodeTypeAddition": null,
                                                            "children": [
                                                                {
                                                                    "id": 603580579182022,
                                                                    "name": "名称",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603580461049286,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603580603213254,
                                                                    "name": "模型文件",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603580461049286,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603580630762950,
                                                                    "name": "方式",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603580461049286,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603580666672582,
                                                                    "name": "管长",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603580461049286,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603580687766982,
                                                                    "name": "内径",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603580461049286,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603580713141702,
                                                                    "name": "外径",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603580461049286,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603580738663878,
                                                                    "name": "厚度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603580461049286,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603580805719494,
                                                                    "name": "first_seg_length",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603580461049286,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603580852835782,
                                                                    "name": "min_mid_seg_length",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603580461049286,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603580901524934,
                                                                    "name": "last_seg_length",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603580461049286,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603580954031558,
                                                                    "name": "夹持段编号",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603580461049286,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603580997952966,
                                                                    "name": "夹持线长比例",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603580461049286,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603581017294278,
                                                                    "name": "XYZ",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603580461049286,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603581036041670,
                                                                    "name": "YBC",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603580461049286,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603581061875142,
                                                                    "name": "material",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603580461049286,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603581093115334,
                                                                    "name": "needReverse",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603580461049286,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "id": 603562270946758,
                                    "name": "加工工艺生成",
                                    "nodeType": "parameter_group",
                                    "parentId": 602543727121863,
                                    "nodeTypeAddition": null,
                                    "children": [
                                        {
                                            "id": 603562314237382,
                                            "name": "模具匹配方法",
                                            "nodeType": "parameter_group",
                                            "parentId": 603562270946758,
                                            "nodeTypeAddition": null,
                                            "children": [
                                                {
                                                    "id": 603564802102726,
                                                    "name": "程序文件",
                                                    "nodeType": "parameter",
                                                    "parentId": 603562314237382,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603567500539334,
                                                            "name": "程序主文件",
                                                            "nodeType": "prop",
                                                            "parentId": 603564802102726,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603575697085894,
                                                    "name": "出参参数组",
                                                    "nodeType": "parameter",
                                                    "parentId": 603562314237382,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603581564396998,
                                                            "name": "模具参数",
                                                            "nodeType": "parameter",
                                                            "parentId": 603575697085894,
                                                            "nodeTypeAddition": null,
                                                            "children": [
                                                                {
                                                                    "id": 603581668824518,
                                                                    "name": "名称",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603581564396998,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603581708604870,
                                                                    "name": "模型文件",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603581564396998,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603581732509126,
                                                                    "name": "层数",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603581564396998,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603581750924742,
                                                                    "name": "类型",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603581564396998,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603581770782150,
                                                                    "name": "弯曲半径",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603581564396998,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603581791688134,
                                                                    "name": "匹配管径",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603581564396998,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603581813859782,
                                                                    "name": "模具高度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603581564396998,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603581851477446,
                                                                    "name": "中心高",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603581564396998,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603581872690630,
                                                                    "name": "脱模长度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603581564396998,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603581892613574,
                                                                    "name": "主夹宽度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603581564396998,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603581915153862,
                                                                    "name": "导夹长度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603581564396998,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603581942461894,
                                                                    "name": "导夹宽度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603581564396998,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603576118068678,
                                                    "name": "入参参数组",
                                                    "nodeType": "parameter",
                                                    "parentId": 603562314237382,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603564881364422,
                                                            "name": "工件基本参数",
                                                            "nodeType": "parameter",
                                                            "parentId": 603576118068678,
                                                            "nodeTypeAddition": null,
                                                            "children": [
                                                                {
                                                                    "id": 603569717257670,
                                                                    "name": "名称",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564881364422,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569738438086,
                                                                    "name": "模型文件",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564881364422,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569760114118,
                                                                    "name": "方式",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564881364422,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569782089158,
                                                                    "name": "管长",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564881364422,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569802479046,
                                                                    "name": "内径",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564881364422,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569822221766,
                                                                    "name": "外径",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564881364422,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569843860934,
                                                                    "name": "厚度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564881364422,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569863341510,
                                                                    "name": "first_seg_length",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564881364422,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569883280838,
                                                                    "name": "min_mid_seg_length",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564881364422,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569903801798,
                                                                    "name": "last_seg_length",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564881364422,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569922233798,
                                                                    "name": "夹持段编号",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564881364422,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569939084742,
                                                                    "name": "夹持线长比例",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564881364422,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569959052742,
                                                                    "name": "XYZ",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564881364422,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603569980786118,
                                                                    "name": "YBC",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564881364422,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603570001081798,
                                                                    "name": "material",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564881364422,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603570022127046,
                                                                    "name": "needReverse",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564881364422,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 603564964156870,
                                                            "name": "弯管机参数",
                                                            "nodeType": "parameter",
                                                            "parentId": 603576118068678,
                                                            "nodeTypeAddition": null,
                                                            "children": [
                                                                {
                                                                    "id": 603570134078918,
                                                                    "name": "编号",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564964156870,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603570155296198,
                                                                    "name": "模型文件",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564964156870,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603570173978054,
                                                                    "name": "主夹安装面至轮模中心距离",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564964156870,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603570196477382,
                                                                    "name": "导夹安装面至轮模中心距离",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564964156870,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603570222499270,
                                                                    "name": "左右弯轮模安装高度差",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564964156870,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603570246096326,
                                                                    "name": "安装坐标系",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564964156870,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603570270430662,
                                                                    "name": "世界坐标系",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564964156870,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603570290619846,
                                                                    "name": "machine_toml_config_path",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564964156870,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603570320020934,
                                                                    "name": "Processing_info",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603564964156870,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "id": 603562339259846,
                                            "name": "加工工艺生成方法",
                                            "nodeType": "parameter_group",
                                            "parentId": 603562270946758,
                                            "nodeTypeAddition": null,
                                            "children": [
                                                {
                                                    "id": 603565114987974,
                                                    "name": "程序文件",
                                                    "nodeType": "parameter",
                                                    "parentId": 603562339259846,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603567559914950,
                                                            "name": "程序主文件",
                                                            "nodeType": "prop",
                                                            "parentId": 603565114987974,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603575737427398,
                                                    "name": "出参参数组",
                                                    "nodeType": "parameter",
                                                    "parentId": 603562339259846,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603582339466694,
                                                            "name": "弯管机参数",
                                                            "nodeType": "parameter",
                                                            "parentId": 603575737427398,
                                                            "nodeTypeAddition": null,
                                                            "children": [
                                                                {
                                                                    "id": 603583016060358,
                                                                    "name": "编号",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603582339466694,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603583160456646,
                                                                    "name": "主夹安装面至轮模中心距离",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603582339466694,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603583249360326,
                                                                    "name": "左右弯轮模安装高度差",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603582339466694,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603583330907590,
                                                                    "name": "世界坐标系",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603582339466694,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603583416968646,
                                                                    "name": "Processing_info",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603582339466694,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603583048439238,
                                                                    "name": "模型文件",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603582339466694,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603583186150854,
                                                                    "name": "导夹安装面至轮模中心距离",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603582339466694,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603583300363718,
                                                                    "name": "安装坐标系",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603582339466694,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603583379658182,
                                                                    "name": "machine_toml_config_path",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603582339466694,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603576077837766,
                                                    "name": "入参参数组",
                                                    "nodeType": "parameter",
                                                    "parentId": 603562339259846,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603565199111622,
                                                            "name": "弯管机参数",
                                                            "nodeType": "parameter",
                                                            "parentId": 603576077837766,
                                                            "nodeTypeAddition": null,
                                                            "children": [
                                                                {
                                                                    "id": 603571626624454,
                                                                    "name": "编号",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565199111622,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603571647382982,
                                                                    "name": "模型文件",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565199111622,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603571667252678,
                                                                    "name": "主夹安装面至轮模中心距离",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565199111622,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603571686708678,
                                                                    "name": "导夹安装面至轮模中心距离",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565199111622,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603571704952262,
                                                                    "name": "左右弯轮模安装高度差",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565199111622,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603571725329862,
                                                                    "name": "安装坐标系",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565199111622,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603571744712134,
                                                                    "name": "世界坐标系",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565199111622,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603571767629254,
                                                                    "name": "machine_toml_config_path",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565199111622,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603571787015622,
                                                                    "name": "Processing_info",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565199111622,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 603565158917574,
                                                            "name": "工件基本参数",
                                                            "nodeType": "parameter",
                                                            "parentId": 603576077837766,
                                                            "nodeTypeAddition": null,
                                                            "children": [
                                                                {
                                                                    "id": 603571233805766,
                                                                    "name": "名称",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565158917574,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603571256313286,
                                                                    "name": "模型文件",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565158917574,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603571275847110,
                                                                    "name": "方式",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565158917574,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603571297007046,
                                                                    "name": "管长",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565158917574,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603571316250054,
                                                                    "name": "内径",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565158917574,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603571335157190,
                                                                    "name": "外径",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565158917574,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603571354076614,
                                                                    "name": "厚度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565158917574,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603571372889542,
                                                                    "name": "first_seg_length",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565158917574,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603571392763334,
                                                                    "name": "min_mid_seg_length",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565158917574,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603571429262790,
                                                                    "name": "last_seg_length",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565158917574,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603571453707718,
                                                                    "name": "夹持段编号",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565158917574,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603571473290694,
                                                                    "name": "夹持线长比例",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565158917574,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603571490981318,
                                                                    "name": "XYZ",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565158917574,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603571510138310,
                                                                    "name": "YBC",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565158917574,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603571528672710,
                                                                    "name": "material",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565158917574,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603571546572230,
                                                                    "name": "needReverse",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565158917574,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "id": 603562362115526,
                                            "name": "补偿设置方法",
                                            "nodeType": "parameter_group",
                                            "parentId": 603562270946758,
                                            "nodeTypeAddition": null,
                                            "children": [
                                                {
                                                    "id": 603565350520262,
                                                    "name": "程序文件",
                                                    "nodeType": "parameter",
                                                    "parentId": 603562362115526,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603567613126086,
                                                            "name": "程序主文件",
                                                            "nodeType": "prop",
                                                            "parentId": 603565350520262,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603575782983110,
                                                    "name": "出参参数组",
                                                    "nodeType": "parameter",
                                                    "parentId": 603562362115526,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603583825352134,
                                                            "name": "补偿参数",
                                                            "nodeType": "parameter",
                                                            "parentId": 603575782983110,
                                                            "nodeTypeAddition": null,
                                                            "children": [
                                                                {
                                                                    "id": 603583906731462,
                                                                    "name": "compensation_parameter",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603583825352134,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603576033928646,
                                                    "name": "入参参数组",
                                                    "nodeType": "parameter",
                                                    "parentId": 603562362115526,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603565763237318,
                                                            "name": "补偿参数",
                                                            "nodeType": "parameter",
                                                            "parentId": 603576033928646,
                                                            "nodeTypeAddition": null,
                                                            "children": [
                                                                {
                                                                    "id": 603572561638854,
                                                                    "name": "compensation_parameter",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565763237318,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 603565670389190,
                                                            "name": "加工参数",
                                                            "nodeType": "parameter",
                                                            "parentId": 603576033928646,
                                                            "nodeTypeAddition": null,
                                                            "children": [
                                                                {
                                                                    "id": 603572480808390,
                                                                    "name": "Processing_parameter",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565670389190,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "id": 603562390115782,
                                            "name": "仿真分析方法",
                                            "nodeType": "parameter_group",
                                            "parentId": 603562270946758,
                                            "nodeTypeAddition": null,
                                            "children": [
                                                {
                                                    "id": 603565833782726,
                                                    "name": "程序文件",
                                                    "nodeType": "parameter",
                                                    "parentId": 603562390115782,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603567665251782,
                                                            "name": "程序主文件",
                                                            "nodeType": "prop",
                                                            "parentId": 603565833782726,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603575817905606,
                                                    "name": "出参参数组",
                                                    "nodeType": "parameter",
                                                    "parentId": 603562390115782,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603584503797190,
                                                            "name": "仿真参数",
                                                            "nodeType": "parameter",
                                                            "parentId": 603575817905606,
                                                            "nodeTypeAddition": null,
                                                            "children": [
                                                                {
                                                                    "id": 603584576816582,
                                                                    "name": "simulation_parameter",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603584503797190,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603576000996806,
                                                    "name": "入参参数组",
                                                    "nodeType": "parameter",
                                                    "parentId": 603562390115782,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603565881226694,
                                                            "name": "加工参数",
                                                            "nodeType": "parameter",
                                                            "parentId": 603576000996806,
                                                            "nodeTypeAddition": null,
                                                            "children": [
                                                                {
                                                                    "id": 603572669478342,
                                                                    "name": "Processing_parameter",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603565881226694,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "id": 603562411120070,
                                            "name": "干涉分析方法",
                                            "nodeType": "parameter_group",
                                            "parentId": 603562270946758,
                                            "nodeTypeAddition": null,
                                            "children": [
                                                {
                                                    "id": 603566439921094,
                                                    "name": "程序文件",
                                                    "nodeType": "parameter",
                                                    "parentId": 603562411120070,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603567784842694,
                                                            "name": "程序主文件",
                                                            "nodeType": "prop",
                                                            "parentId": 603566439921094,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603575860377030,
                                                    "name": "出参参数组",
                                                    "nodeType": "parameter",
                                                    "parentId": 603562411120070,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603584831333830,
                                                            "name": "干涉参数",
                                                            "nodeType": "parameter",
                                                            "parentId": 603575860377030,
                                                            "nodeTypeAddition": null,
                                                            "children": [
                                                                {
                                                                    "id": 603584945530310,
                                                                    "name": "interference_parameter",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603584831333830,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603575962944966,
                                                    "name": "入参参数组",
                                                    "nodeType": "parameter",
                                                    "parentId": 603562411120070,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603566132762054,
                                                            "name": "工件基本参数",
                                                            "nodeType": "parameter",
                                                            "parentId": 603575962944966,
                                                            "nodeTypeAddition": null,
                                                            "children": [
                                                                {
                                                                    "id": 603573024081350,
                                                                    "name": "名称",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603566132762054,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603573491897798,
                                                                    "name": "模型文件",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603566132762054,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603573511697862,
                                                                    "name": "方式",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603566132762054,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603573531104710,
                                                                    "name": "管长",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603566132762054,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603573549254086,
                                                                    "name": "内径",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603566132762054,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603573570016710,
                                                                    "name": "外径",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603566132762054,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603573590488518,
                                                                    "name": "厚度",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603566132762054,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603573610419654,
                                                                    "name": "first_seg_length",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603566132762054,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603573629404614,
                                                                    "name": "min_mid_seg_length",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603566132762054,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603573647959494,
                                                                    "name": "last_seg_length",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603566132762054,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603573667521990,
                                                                    "name": "夹持段编号",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603566132762054,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603573686695366,
                                                                    "name": "夹持线长比例",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603566132762054,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603573708559814,
                                                                    "name": "XYZ",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603566132762054,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603573727557062,
                                                                    "name": "YBC",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603566132762054,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603573746857414,
                                                                    "name": "material",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603566132762054,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603573764711878,
                                                                    "name": "needReverse",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603566132762054,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "id": 603566157858246,
                                                            "name": "弯管机参数",
                                                            "nodeType": "parameter",
                                                            "parentId": 603575962944966,
                                                            "nodeTypeAddition": null,
                                                            "children": [
                                                                {
                                                                    "id": 603573836137926,
                                                                    "name": "编号",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603566157858246,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603573855368646,
                                                                    "name": "模型文件",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603566157858246,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603573876131270,
                                                                    "name": "主夹安装面至轮模中心距离",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603566157858246,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603573900510662,
                                                                    "name": "导夹安装面至轮模中心距离",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603566157858246,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603573918873030,
                                                                    "name": "左右弯轮模安装高度差",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603566157858246,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603573940336070,
                                                                    "name": "安装坐标系",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603566157858246,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603573959603654,
                                                                    "name": "世界坐标系",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603566157858246,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603573976532422,
                                                                    "name": "machine_toml_config_path",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603566157858246,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                },
                                                                {
                                                                    "id": 603573994522054,
                                                                    "name": "Processing_info",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603566157858246,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "id": 603562437535174,
                                            "name": "加工程序生成方法",
                                            "nodeType": "parameter_group",
                                            "parentId": 603562270946758,
                                            "nodeTypeAddition": null,
                                            "children": [
                                                {
                                                    "id": 603566485108166,
                                                    "name": "程序文件",
                                                    "nodeType": "parameter",
                                                    "parentId": 603562437535174,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603567830525382,
                                                            "name": "程序主文件",
                                                            "nodeType": "prop",
                                                            "parentId": 603566485108166,
                                                            "nodeTypeAddition": null,
                                                            "children": null
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603575897073094,
                                                    "name": "出参参数组",
                                                    "nodeType": "parameter",
                                                    "parentId": 603562437535174,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603585078375878,
                                                            "name": "加工参数",
                                                            "nodeType": "parameter",
                                                            "parentId": 603575897073094,
                                                            "nodeTypeAddition": null,
                                                            "children": [
                                                                {
                                                                    "id": 603585134593478,
                                                                    "name": "Process_parameter",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603585078375878,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "id": 603575920514502,
                                                    "name": "入参参数组",
                                                    "nodeType": "parameter",
                                                    "parentId": 603562437535174,
                                                    "nodeTypeAddition": null,
                                                    "children": [
                                                        {
                                                            "id": 603566305961414,
                                                            "name": "加工参数",
                                                            "nodeType": "parameter",
                                                            "parentId": 603575920514502,
                                                            "nodeTypeAddition": null,
                                                            "children": [
                                                                {
                                                                    "id": 603574128952774,
                                                                    "name": "Process_parameter",
                                                                    "nodeType": "prop",
                                                                    "parentId": 603566305961414,
                                                                    "nodeTypeAddition": null,
                                                                    "children": null
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "id": 603550806914502,
                            "name": "feature",
                            "nodeType": "parameter",
                            "parentId": 602543727117766,
                            "nodeTypeAddition": null,
                            "children": [
                                {
                                    "id": 603553396852166,
                                    "name": "feature 0",
                                    "nodeType": "prop",
                                    "parentId": 603550806914502,
                                    "nodeTypeAddition": null,
                                    "children": null
                                },
                                {
                                    "id": 603553417995718,
                                    "name": "feature 1",
                                    "nodeType": "prop",
                                    "parentId": 603550806914502,
                                    "nodeTypeAddition": null,
                                    "children": null
                                },
                                {
                                    "id": 603553431934406,
                                    "name": "feature 2",
                                    "nodeType": "prop",
                                    "parentId": 603550806914502,
                                    "nodeTypeAddition": null,
                                    "children": null
                                }
                            ]
                        },
                        {
                            "id": 603550833145286,
                            "name": "label",
                            "nodeType": "parameter",
                            "parentId": 602543727117766,
                            "nodeTypeAddition": null,
                            "children": [
                                {
                                    "id": 603553558173126,
                                    "name": "label 0",
                                    "nodeType": "prop",
                                    "parentId": 603550833145286,
                                    "nodeTypeAddition": null,
                                    "children": null
                                },
                                {
                                    "id": 603553620088262,
                                    "name": "label 1",
                                    "nodeType": "prop",
                                    "parentId": 603550833145286,
                                    "nodeTypeAddition": null,
                                    "children": null
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 602543738463686,
                    "name": "insofbend",
                    "nodeType": "model",
                    "parentId": 602543219627463,
                    "nodeTypeAddition": null,
                    "children": [
                        {
                            "id": 602543738463687,
                            "name": "人员",
                            "nodeType": "person",
                            "parentId": 602543738463686,
                            "nodeTypeAddition": null,
                            "children": null
                        },
                        {
                            "id": 602543738463688,
                            "name": "机器",
                            "nodeType": "machine",
                            "parentId": 602543738463686,
                            "nodeTypeAddition": null,
                            "children": null
                        },
                        {
                            "id": 602543738463689,
                            "name": "物料",
                            "nodeType": "product",
                            "parentId": 602543738463686,
                            "nodeTypeAddition": null,
                            "children": null
                        },
                        {
                            "id": 602543738463690,
                            "name": "过程",
                            "nodeType": "procedure",
                            "parentId": 602543738463686,
                            "nodeTypeAddition": null,
                            "children": null
                        },
                        {
                            "id": 602543738463691,
                            "name": "方法",
                            "nodeType": "method",
                            "parentId": 602543738463686,
                            "nodeTypeAddition": null,
                            "children": null
                        }
                    ]
                },
                {
                    "id": 602543749240262,
                    "name": "insoflaser",
                    "nodeType": "model",
                    "parentId": 602543219627463,
                    "nodeTypeAddition": null,
                    "children": [
                        {
                            "id": 602543749240263,
                            "name": "人员",
                            "nodeType": "person",
                            "parentId": 602543749240262,
                            "nodeTypeAddition": null,
                            "children": null
                        },
                        {
                            "id": 602543749240264,
                            "name": "机器",
                            "nodeType": "machine",
                            "parentId": 602543749240262,
                            "nodeTypeAddition": null,
                            "children": null
                        },
                        {
                            "id": 602543749240265,
                            "name": "物料",
                            "nodeType": "product",
                            "parentId": 602543749240262,
                            "nodeTypeAddition": null,
                            "children": null
                        },
                        {
                            "id": 602543749240266,
                            "name": "过程",
                            "nodeType": "procedure",
                            "parentId": 602543749240262,
                            "nodeTypeAddition": null,
                            "children": null
                        },
                        {
                            "id": 602543749240267,
                            "name": "方法",
                            "nodeType": "method",
                            "parentId": 602543749240262,
                            "nodeTypeAddition": null,
                            "children": null
                        }
                    ]
                }
            ]
        },
        {
            "id": 602543219627464,
            "name": "insoftest",
            "nodeType": "supermodel",
            "parentId": 602543219574214,
            "nodeTypeAddition": null,
            "children": [
                {
                    "id": 602543270180294,
                    "name": "DTIS-511",
                    "nodeType": "model",
                    "parentId": 602543219627464,
                    "nodeTypeAddition": null,
                    "children": [
                        {
                            "id": 602543270180295,
                            "name": "人员",
                            "nodeType": "person",
                            "parentId": 602543270180294,
                            "nodeTypeAddition": null,
                            "children": [
                                {
                                    "id": 603489646511558,
                                    "name": "部门",
                                    "nodeType": "parameter_group",
                                    "parentId": 602543270180295,
                                    "nodeTypeAddition": null,
                                    "children": [
                                        {
                                            "id": 603490804975046,
                                            "name": "群组特性",
                                            "nodeType": "parameter",
                                            "parentId": 603489646511558,
                                            "nodeTypeAddition": null,
                                            "children": [
                                                {
                                                    "id": 603490847532486,
                                                    "name": "类型",
                                                    "nodeType": "prop",
                                                    "parentId": 603490804975046,
                                                    "nodeTypeAddition": null,
                                                    "children": null
                                                },
                                                {
                                                    "id": 603490862908870,
                                                    "name": "级别",
                                                    "nodeType": "prop",
                                                    "parentId": 603490804975046,
                                                    "nodeTypeAddition": null,
                                                    "children": null
                                                },
                                                {
                                                    "id": 603490878154182,
                                                    "name": "编码",
                                                    "nodeType": "prop",
                                                    "parentId": 603490804975046,
                                                    "nodeTypeAddition": null,
                                                    "children": null
                                                },
                                                {
                                                    "id": 603490890327494,
                                                    "name": "排序",
                                                    "nodeType": "prop",
                                                    "parentId": 603490804975046,
                                                    "nodeTypeAddition": null,
                                                    "children": null
                                                },
                                                {
                                                    "id": 603490903291334,
                                                    "name": "状态",
                                                    "nodeType": "prop",
                                                    "parentId": 603490804975046,
                                                    "nodeTypeAddition": null,
                                                    "children": null
                                                }
                                            ]
                                        },
                                        {
                                            "id": 603491179496902,
                                            "name": "个人特性",
                                            "nodeType": "parameter",
                                            "parentId": 603489646511558,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 603491241039302,
                                                    "name": "状态",
                                                    "nodeType": "prop",
                                                    "parentId": 603491179496902,
                                                    "nodeTypeAddition": "",
                                                    "children": null
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "id": 603489745180102,
                                    "name": "部门",
                                    "nodeType": "parameter_group",
                                    "parentId": 602543270180295,
                                    "nodeTypeAddition": null,
                                    "children": null
                                }
                            ]
                        },
                        {
                            "id": 602543270180296,
                            "name": "机器",
                            "nodeType": "machine",
                            "parentId": 602543270180294,
                            "nodeTypeAddition": null,
                            "children": [
                                {
                                    "id": 606266425663557,
                                    "name": "111",
                                    "nodeType": "parameter_group",
                                    "parentId": 602543270180296,
                                    "nodeTypeAddition": "machine",
                                    "children": [
                                        {
                                            "id": 606295291486277,
                                            "name": "222",
                                            "nodeType": "parameter",
                                            "parentId": 606266425663557,
                                            "nodeTypeAddition": "",
                                            "children": [
                                                {
                                                    "id": 606295318798405,
                                                    "name": "21212",
                                                    "nodeType": "prop",
                                                    "parentId": 606295291486277,
                                                    "nodeTypeAddition": "",
                                                    "children": null
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "id": 602543270180297,
                            "name": "物料",
                            "nodeType": "product",
                            "parentId": 602543270180294,
                            "nodeTypeAddition": null,
                            "children": null
                        },
                        {
                            "id": 602543270180298,
                            "name": "过程",
                            "nodeType": "procedure",
                            "parentId": 602543270180294,
                            "nodeTypeAddition": null,
                            "children": null
                        },
                        {
                            "id": 602543270184390,
                            "name": "方法",
                            "nodeType": "method",
                            "parentId": 602543270180294,
                            "nodeTypeAddition": null,
                            "children": null
                        }
                    ]
                },
                {
                    "id": 602543784478150,
                    "name": "NDT-SNPTC",
                    "nodeType": "model",
                    "parentId": 602543219627464,
                    "nodeTypeAddition": null,
                    "children": [
                        {
                            "id": 602543784478151,
                            "name": "人员",
                            "nodeType": "person",
                            "parentId": 602543784478150,
                            "nodeTypeAddition": null,
                            "children": null
                        },
                        {
                            "id": 602543784478152,
                            "name": "机器",
                            "nodeType": "machine",
                            "parentId": 602543784478150,
                            "nodeTypeAddition": null,
                            "children": null
                        },
                        {
                            "id": 602543784478153,
                            "name": "物料",
                            "nodeType": "product",
                            "parentId": 602543784478150,
                            "nodeTypeAddition": null,
                            "children": null
                        },
                        {
                            "id": 602543784478154,
                            "name": "过程",
                            "nodeType": "procedure",
                            "parentId": 602543784478150,
                            "nodeTypeAddition": null,
                            "children": null
                        },
                        {
                            "id": 602543784478155,
                            "name": "方法",
                            "nodeType": "method",
                            "parentId": 602543784478150,
                            "nodeTypeAddition": null,
                            "children": null
                        }
                    ]
                }
            ]
        }
    ]
}
    '''

    # 解析JSON字符串
    json_data = json.loads(json_str)

    # 转换为树
    tree = json_to_tree(json_data)

    # 显示树结构
    print(tree)
