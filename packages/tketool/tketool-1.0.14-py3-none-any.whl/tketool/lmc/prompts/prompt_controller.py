# pass_generate
import time
import re
from tketool.files import *
import importlib.resources, os
import xml.etree.ElementTree as ET


def get_prompt_by_path(path):
    doc = read_prompt_file(path, None)
    return doc


def get_prompt(key: str, lang="english", folder=None):
    """
    `get_prompt`函数是用于获取提示文件的内容的函数。
    
    参数:
        key (str): 提示文件的键值。
        lang (str, 可选): 提示文件的语言版本，默认为 "english"。
        return_details (bool, 可选): 是否返回提示文件的详细内容，如果为 False，只返回文件中的模板字符串，默认为 False。
        folder (str, 可选): 提示文件所在的文件夹路径，默认为 None，表示提示文件在安装包中。
    
    返回:
        str 或 dict: 如果`return_details`为 True，返回提示文件的详细内容，类型为字典；否则只返回文件中的模板字符串，类型为字符串。
    
    raise:
        IOError: 如果无法找到指定的文件，或者读取文件出错。
    
    注意:
        此函数将尝试从指定的文件夹或安装的包中获取提示文件。所以如果你安装了此包，请确保提示文件存在于正确的位置，否则可能会引发 IOError。
    
    示例:
    
        get_prompt('welcome', return_details=True)
        # 返回 {'templatestr': 'Welcome to our system!', 'details': 'This is the welcome message showed to the user when they log in.'}
    """

    def get_file_path(lang, key):
        """
        这个函数是用来获取文件路径的。给定语言和键，它会构造出对应的文件路径。
        
        参数:
            lang: str类型。文件的语言，例如"english"、"chinese"等。
            key: str类型。文件的名称，不包含文件扩展名。例如，如果文件的全名为"example.txt"，那么键应该是"example"。
        
        返回:
            返回一个由importlib.resources.files('tketool').joinpath生成的文件路径。
        
        注意:
            这个函数假设所有的文件都存放在"lmc/prompts/templates"目录下，并且文件的扩展名都是".txt"。
            在非DEBUG模式下，这个函数会从tketool包中寻找文件。因此，这个函数只能在安装了tketool包的环境中运行。
        
        示例:
            get_file_path("chinese", "example")返回的是"lmc/prompts/templates/chinese/example.txt"
        """

        path = os.path.join("lmc", "prompts", "templates", lang, f"{key}.txt")
        # 非DEBUG模式，我们试图从安装的包中获取文件
        return importlib.resources.files('tketool').joinpath(path)

    if folder is None:
        path = get_file_path(lang, key)
        static_path = None
    else:
        path = os.path.join(folder, lang, f"{key}.txt")
        static_path = os.path.join(folder, lang, "static.txt")

    doc = read_prompt_file(path, static_path)
    return doc


class prompt_field:
    def __init__(self):
        self.field_name = ""
        self.field_type = ""
        self.field_sub_type = ""
        self.field_des = ""


class prompt_model:
    def __init__(self):
        self.model_name = ""
        self.fields_list = []


class prompt_enum:
    def __init__(self):
        self.enum_name = ""
        self.enums_list = {}


class prompt_define:
    def __init__(self):
        self.prompt_name = ""
        self.prompt_output = "str"
        self.prompt_goto = []
        self.prompt_condition_field = ""
        self.prompt_condition_value = ""
        self.prompt_condition_default = False
        self.prompt_content = ""


class prompt_define_file:
    def __init__(self):
        self.prompts = {}
        self.models = {}
        self.enums = {}
        self.static_str_dict = {}


def read_static_file(path) -> (dict, dict, dict):
    if path is None or not os.path.exists(path):
        return {}, {}, {}

    static_tree = ET.parse(path)
    root = static_tree.getroot()

    static_dict = {}
    static_model_dict = {}
    static_enum_dict = {}

    for child in root:
        if child.tag == "static":
            key = child.attrib['name']

            content_lines = []
            for content_line in child.itertext():
                content_lines.append(content_line)
            value = '\n'.join(content_lines)
            static_dict[key] = value

        if child.tag == 'model':
            model = prompt_model()
            model.model_name = child.attrib['name']
            for field_elem in child.findall('field'):
                field = prompt_field()
                field.field_name = field_elem.attrib['name']
                field.field_type = field_elem.attrib['type']
                field.field_des = field_elem.attrib.get('des', '')  # 默认值为空字符串
                # field.field_sub_type = field_elem.attrib.get('sub_type', '')
                model.fields_list.append(field)
            static_model_dict[model.model_name] = model

        if child.tag == 'enum':
            enum = prompt_enum()
            enum.enum_name = child.attrib['name']
            for item_elem in child.findall('item'):  # 查找所有名为 'item' 的子元素
                key = item_elem.attrib['key']  # 获取 'key' 属性
                value = item_elem.attrib['value']  # 获取 'value' 属性
                enum.enums_list[key] = value  # 将键值对添加到枚举字典中
            static_enum_dict[enum.enum_name] = enum

    return static_dict, static_model_dict, static_enum_dict


def read_prompt_file(path, static_file_path) -> prompt_define_file:
    tree = ET.parse(path)
    root = tree.getroot()

    pd_file = prompt_define_file()
    pd_file.static_str_dict, pd_file.models, pd_file.enums = read_static_file(static_file_path)

    # 遍历所有一级子节点
    for child in root:
        if child.tag == 'model':
            model = prompt_model()
            model.model_name = child.attrib['name']
            for field_elem in child.findall('field'):
                field = prompt_field()
                field.field_name = field_elem.attrib['name']
                field.field_type = field_elem.attrib['type']
                field.field_des = field_elem.attrib.get('des', '')  # 默认值为空字符串
                # field.field_sub_type = field_elem.attrib.get('sub_type', '')
                model.fields_list.append(field)
            pd_file.models[model.model_name] = model

        elif child.tag == 'enum':
            enum = prompt_enum()
            enum.enum_name = child.attrib['name']
            for item_elem in child.findall('item'):  # 查找所有名为 'item' 的子元素
                key = item_elem.attrib['key']  # 获取 'key' 属性
                value = item_elem.attrib['value']  # 获取 'value' 属性
                enum.enums_list[key] = value  # 将键值对添加到枚举字典中
            pd_file.enums[enum.enum_name] = enum

        elif child.tag == 'prompt':
            prompt = prompt_define()
            prompt.prompt_name = child.attrib['name']
            prompt.prompt_output = child.attrib.get('output', 'str')  # 设置默认output类型为str
            prompt.prompt_goto = [x.strip() for x in child.attrib.get('goto', '').split(',') if x.strip()]
            prompt.prompt_condition_field = child.attrib.get('condition_field', '')
            prompt.prompt_condition_value = child.attrib.get('condition_value', '')
            prompt.prompt_condition_default = child.attrib.get('condition_default', '').lower() == 'true'
            # prompt.vote_count = child.attrib.get('vote_count', '1')
            # prompt.vote_max = child.attrib.get('vote_max', '1')
            # prompt.vote_field = child.attrib.get('vote_field', '')

            content_lines = []
            for content_line in child.itertext():
                content_lines.append(content_line.strip())
            prompt.prompt_content = '\n'.join(content_lines).strip()

            pd_file.prompts[prompt.prompt_name] = prompt

    return pd_file


def write_prompt_file(path, file_define: prompt_define_file):
    root = ET.Element('prompts')

    # 写入models
    for model_name, model in file_define.models.items():
        model_elem = ET.SubElement(root, 'model', name=model_name)
        for field in model.fields_list:
            ET.SubElement(model_elem, 'field', name=field.field_name, type=field.field_type, des=field.field_des)

    # 写入enums
    for enum_name, enum in file_define.enums.items():
        enum_elem = ET.SubElement(root, 'enum', name=enum_name)
        for key, value in enum.enums_list.items():
            ET.SubElement(enum_elem, 'key', key=key, value=value)

    # 写入prompts
    for prompt_name, prompt in file_define.prompts.items():
        prompt_elem = ET.SubElement(root, 'prompt',
                                    name=prompt.prompt_name,
                                    output=prompt.prompt_output,
                                    goto=",".join(prompt.prompt_goto),
                                    condition_field=prompt.prompt_condition_field,
                                    condition_value=prompt.prompt_condition_value,
                                    condition_default=str(prompt.prompt_condition_default).lower())
        prompt_elem.text = prompt.prompt_content

    tree = ET.ElementTree(root)
    tree.write(path, encoding='utf-8', xml_declaration=True)
