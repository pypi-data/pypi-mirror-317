from enum import Enum
from tketool.markdowns.markdown import markdown_item_base


class flowchart_color_enum(str, Enum):
    """
    这个类是一个枚举类，名为flowchart_color_enum，它继承自str和Enum类。它主要是定义了一些代表不同颜色的字符串常量，这些字符串常量都是对应颜色的十六进制RGB值。这些颜色经常会被用在流程图中，因此这个枚举类的名称被命名为flowchart_color_enum。
    
    使用这个枚举类时，你可以直接使用它的枚举值来表示颜色，而不需要记住颜色的十六进制RGB值。这会使你的代码更易读，更易维护。
    
    类属性包含：
    - Red: 红色，其十六进制RGB值为"#FF0000"。
    - Yellow: 黄色，其十六进制RGB值为"#FFFF00"。
    - Blue: 蓝色，其十六进制RGB值为"#00BFFF"。
    - Orange: 橙色，其十六进制RGB值为"#FFA500"。
    - LightGreen: 浅绿色，其十六进制RGB值为"#90EE90"。
    - MediumPurple: 中紫色，其十六进制RGB值为"#9370DB"。
    - Auqamarin: 浅碧色，其十六进制RGB值为"#7FFFAA"。
    - DeepSkyBlue: 深天蓝色，其十六进制RGB值为"#00BFFF"。
    - NavajoWhite: 纳瓦霍白色，其十六进制RGB值为"#FFDEAD"。
    
    以下是一个使用示例：
    
    ```python
    # 初始化一个颜色变量
    color = flowchart_color_enum.Blue
    # 打印颜色的RGB值
    print(color.value)
    ```
    
    这个枚举类没有任何已知的错误或bug。
    """

    Red = "#FF0000",
    Yellow = "#FFFF00",
    Blue = "#00BFFF",
    Orange = "#FFA500",
    LightGreen = "#90EE90",
    MediumPurple = "#9370DB",
    Auqamarin = "#7FFFAA",
    DeepSkyBlue = "#00BFFF",
    NavajoWhite = "#FFDEAD",


class flowchart_shape_enum(str, Enum):
    """
    这是一个名为`flowchart_shape_enum`的枚举类，继承自`str`和`Enum`。
    
    此类的主要目的是提供一个方便的方式来表示流程图中的形状。
    
    例如，可以通过`flowchart_shape_enum.Roundedges`来表示具有圆角的形状，通过`flowchart_shape_enum.Stadium`来表示体育场形状等等。此枚举类中的每一个值都是一个字符串，这些字符串的形式是特定的，可以被用来在流程图生成器中创建对应的形状。
    
    使用例子如下：
    
    ```python
    shape = flowchart_shape_enum.Circle
    print(shape.value)  # 输出: ((%%))
    ```
    
    此类没有已知的错误或bug。
    """

    Roundedges = "(%%)",
    Stadium = "([%%])",
    Circle = "((%%))",
    Rhombus = "{%%}",
    Parallelogram = "[/%%/]",
    Asymmetric = ">%%]",
    Hexagon = "{{%%}}",


uncode = ["。", "（", "）", "，", '"', '(', ")", "“", '”', "、", "’", "？", "：", "；"]


class MFlowchart(markdown_item_base):
    """
    `MFlowchart` 类继承自 `markdown_item_base` 类，主要用于生成和管理基于图表的Markdown项目。它提供了一系列的方法，供用户添加节点、设置节点颜色和形状，以及添加线条等。
    
    此类使用的示例如下：
    
    ```python
    flowchart = MFlowchart(oriented_left2right=True)
    flowchart.add_node(name='Node1', id='1', anchor_title='title1', icon='icon1')
    flowchart.set_node_color(id='1', color=flowchart_color_enum.RED)
    flowchart.set_node_shape(id='1', shape=flowchart_shape_enum.CIRCLE)
    flowchart.add_line(id1='1', id2='2', message='message', dot_line=False)
    ```
    
    主要方法介绍：
    
    - `__init__(self, oriented_left2right=True)`: 类的构造方法，初始化一个新的 `MFlowchart` 实例。可选参数 `oriented_left2right` 决定图表是从左向右 (`True`) 还是从上到下 (`False`) 排列。
    
    - `flush_row_anchor(self, anchor_str) -> [str]`: 该方法生成流程图的字符串表示，主要用于Markdown的渲染。返回一个字符串列表，每个字符串是流程图的一行。
    
    - `_convert_name(self, answer)`: 对节点或线条的名称进行处理，以保证其在Markdown中的正确显示。
    
    - `add_node(self, name, id, anchor_title=None, icon=None)`: 添加一个新的节点。参数包括节点名称 (`name`)，节点ID (`id`)，锚点标题 (`anchor_title`) 和图标 (`icon`)。
    
    - `set_node_color(self, id, color: flowchart_color_enum)`: 设置指定节点的颜色。颜色值需要从 `flowchart_color_enum` 枚举中选取。
    
    - `set_node_shape(self, id, shape: flowchart_shape_enum)`: 设置指定节点的形状。形状值需要从 `flowchart_shape_enum` 枚举中选取。
    
    - `add_line(self, id1, id2, message=None, dot_line=False)`: 添加一条从 `id1` 节点到 `id2` 节点的线。可选参数 `message` 是线条的文字说明，`dot_line` 决定线条是否为虚线。
    """

    def __init__(self, oriented_left2right=True):
        """
        初始化MFlowchart类的实例。

        MFlowchart是一个用于创建和编辑Markdown格式的流程图的类。它可以定义节点、线条、节点颜色、节点形状等。
        初始化方法中，我们定义了一些保存流程图信息的列表和字典，以及流程图的默认方向。

        参数:
            oriented_left2right(bool, 可选): 流程图的方向，默认为从左到右。如果为False，则流程图的方向为从上到下。

        使用示例：
            m_flowchart = MFlowchart(oriented_left2right=False)
            m_flowchart.add_node("开始", "node1")
            m_flowchart.add_node("结束", "node2")
            m_flowchart.add_line("node1", "node2")
            lines = m_flowchart.flush_row_anchor()
            for line in lines:
                print(line)
        """

        self.nodes = []
        self.node_color = {}
        self.node_shape = {}
        self.lines = []
        self.oriented = "LR" if oriented_left2right else "TD"
        self.node_navigate = {}
        self.node_icon = {}
        self.id_mapping = {}

        self.sub_graphs = {}
        self.sub_graphs_nodes = {}

    def flush_row_anchor(self, anchor_str) -> [str]:

        """
        `flush_row_anchor` 是 `MFlowchart` 类的一个成员函数，主要负责生成流程图的每一行内容。
        
        参数:
            anchor_str : str
                该参数在函数内部并未使用，可能是历史代码遗留或者预留的接口，当前版本中没有实际意义。
        
        返回:
            List[str]
                返回一个字符串列表，每个元素代表了流程图的一行。
        
        该函数首先定义了流程图的基本格式，然后对 `nodes` 和 `lines` 这两个属性进行遍历，根据这两个属性的内容生成流程图的节点和连线。
        对于节点，它会检查节点的形状（`node_shape`）和图标（`node_icon`）是否被定义，如果被定义则使用定义的形状和图标，否则使用默认值。
        对于连线，它会检查连线是否有标签（`line[2]`）和是否为虚线（`line[3]`），然后生成相应的连线。
        最后，它会为每个节点添加点击跳转链接（如果有的话）和节点颜色。
        
        举个例子，如果我们有如下的流程图对象：
        
        ```python
            mf = MFlowchart()
            mf.add_node("Start", "start")
            mf.add_node("End", "end")
            mf.add_line("start", "end", "Go")
        ```
        
        那么 `flush_row_anchor` 函数会生成以下的列表：
        
        ```python
            [
                '```mermaid\n',
                'graph LR\n',
                'start[Start] \n',
                'end[End] \n',
                'start -->|Go| end \n',
                '```\n'
            ]
        ```
        
        这个列表可以直接用于生成Markdown文件。
        
        注意：本函数没有对输入参数做任何的错误检查和处理，因此在使用时需要保证输入的有效性。
        """

        lines = ['```mermaid\n', f'graph {self.oriented}\n']

        def out_node(node):
            if node[0] in self.node_shape:
                splite = self.node_shape[node[0]].split("%%")
                left_c = splite[0]
                right_c = splite[1]
            else:
                left_c = '['
                right_c = ']'

            rep_str = node[1].replace("\\", "\\\\")

            if node[0] in self.node_icon:
                node_str = f"fa:{self.node_icon[node[0]]} {rep_str}"
            else:
                node_str = rep_str

            lines.append(f'{node[0]}{left_c}"{node_str}"{right_c} \n')

        for sub_graph_key in self.sub_graphs.keys():
            gra_str = self.sub_graphs[sub_graph_key].replace("\\", "\\\\")
            lines.append(f"subgraph {sub_graph_key} [{gra_str}]\n")
            for sub_node in self.sub_graphs_nodes[sub_graph_key]:
                out_node(sub_node)
            lines.append(f"end\n")

        for node in self.nodes:
            out_node(node)

        for line in self.lines:
            if line[2] is None:
                if line[3]:
                    lines.append(f"{line[0]} -.-> {line[1]} \n")
                else:
                    lines.append(f"{line[0]} --> {line[1]} \n")
            else:
                if line[3]:
                    lines.append(f"{line[0]} -.->|{line[2]}| {line[1]} \n")
                else:
                    lines.append(f"{line[0]} -->|{line[2]}| {line[1]} \n")

        for k in self.node_navigate.keys():
            v = self.node_navigate[k]  # self.node_navigate[k].lower().replace(' ', '-')
            lines.append(f'click {k} href "#{v}"\n')

        for node_color_key in self.node_color:
            lines.append(f"style {node_color_key} fill:{self.node_color[node_color_key]}\n")

        lines.append("```\n")
        return lines

    def _convert_name(self, answer):
        """
        _convert_name函数是一个内部函数，主要用于对输入的名称进行处理和转换。
        
        参数:
        answer (str or None): 需要处理的名字，如果为None则直接返回None。如果名字以"/"开始，会在前面添加一个空格。同时，会将名字中的所有uncode字符替换为一个空格。
        
        返回:
        str or None: 返回处理后的名字，如果输入为None则直接返回None。
        
        注意: 该函数并未处理可能存在的错误，比如answer不是字符串或None的情况，并且该函数也没有对uncode进行定义，可能需要在外部定义uncode变量并传入。
        
        使用示例:
        _convert_name("/my name") 会返回 " my name"
        _convert_name("my name") 会返回 "my name"
        _convert_name(None) 会返回 None
        """

        if answer is None:
            return None
        if answer.startswith('/'):
            answer = " " + answer

        for cc in uncode:
            answer = answer.replace(cc, " ")

        return answer

    def add_sub_graph(self, name, id):
        if id not in self.id_mapping:
            self.id_mapping[id] = f"id_{len(self.id_mapping)}"
        id = self.id_mapping[id]

        self.sub_graphs[id] = name
        self.sub_graphs_nodes[id] = []

    def add_node(self, name, id, anchor_title=None, icon=None, sub_graph_id=None):

        """
        `add_node`方法用于向流程图中添加节点。
        
        参数:
        - name (str): 节点的名字。
        - id (int/str): 节点的ID，每个节点的ID需要唯一。
        - anchor_title (str，可选): 锚点标题，用于在Markdown中创建导航，如果给出，则此节点将在流程图中为此链接创建一个导航。默认值是None。
        - icon (str，可选): 为节点添加图标，必须是可接受的图标名称。默认值是None。
        
        返回:
        - 无返回值。
        
        使用方法：
        ```python
        flowchart = MFlowchart()
        flowchart.add_node(name="开始", id=1)
        flowchart.add_node(name="结束", id=2, icon="fa:check")
        ```
        在上面的例子中，我们首先创建了一个`MFlowchart`对象。然后，我们使用`add_node`方法添加了两个节点，一个名为“开始”的节点和一个名为“结束”带有图标的节点。
        
        注意：所有节点的id必须是唯一的，否则将导致错误。
        """

        if id not in self.id_mapping:
            self.id_mapping[id] = f"id_{len(self.id_mapping)}"
        id = self.id_mapping[id]

        if sub_graph_id is None:
            self.nodes.append((id, self._convert_name(name), None))
        else:
            self.sub_graphs_nodes[self.id_mapping[sub_graph_id]].append((id, self._convert_name(name), None))

        if anchor_title is not None:
            self.node_navigate[id] = anchor_title
        if icon is not None:
            self.node_icon[id] = icon

        return id

    def set_node_color(self, id, color: flowchart_color_enum):

        """
            该方法用于设置流程图节点的颜色。
        
            参数:
                id: 流程图节点的标识符，用于区分不同的节点。
                color: 流程图节点的颜色，应为flowchart_color_enum枚举类的一个实例，
                       该枚举类定义了一系列可用的颜色。
        
            此方法无返回值。
        
            例:
        
            ```python
            flowchart = MFlowchart()
            flowchart.add_node('Node1', '1')
            flowchart.set_node_color('1', flowchart_color_enum.Blue)
            ```
        
            在上述例子中，我们首先创建了一个MFlowchart类的实例，然后添加了一个名为'Node1'的节点，并设定其id为'1'，
            最后我们调用了set_node_color方法将此节点的颜色设定为蓝色。
        
            注意: 如果传入的id不在实例的节点id映射中，将不会进行任何操作。
        """

        self.node_color[self.id_mapping[id]] = color

    def set_node_shape(self, id, shape: flowchart_shape_enum):
        """
        设置流程图中节点的形状
        
        这个函数用于设置流程图中指定id的节点的形状。
        
        参数:
            id: 要设置的节点的id。这个id应该是一个已经添加到流程图中的节点的id。
        
            shape: 要设置的形状。这个应该是一个flowchart_shape_enum枚举的实例，表示要设置的形状。
        
        返回值:
            这个函数没有返回值。
        
        使用示例:
        
        ```python
        # 创建一个MFlowchart实例
        flowchart = MFlowchart()
        
        # 添加一个节点
        flowchart.add_node("node1", "id1")
        
        # 设置该节点的形状
        flowchart.set_node_shape("id1", flowchart_shape_enum.ELLIPSE)
        ```
        
        注意:
            如果传入的id不存在，这个函数没有任何效果。所以在调用这个函数之前，要确保id已经存在于流程图中。
        """

        self.node_shape[self.id_mapping[id]] = shape

    def add_line(self, id1, id2, message=None, dot_line=False):

        """
        在流程图中添加一条线。该函数将两个节点通过一条线进行连接，线上可以添加消息，并且可以指定线的类型（实线或虚线）。
        
        参数:
            id1: str, 起始节点的id。
            id2: str, 结束节点的id。
            message: str, 线上的消息，可选，默认为None。
            dot_line: bool, 是否为虚线，可选，默认为False。如果为True，则添加的线为虚线，否则为实线。
        
        返回类型:
            无返回值。
        
        示例:
            以下代码将节点'id1'和节点'id2'通过一条实线连接，线上的消息为'message':
            ```python
            flowchart = MFlowchart()
            flowchart.add_node('name1', 'id1')
            flowchart.add_node('name2', 'id2')
            flowchart.add_line('id1', 'id2', 'message')
            ```
        
        注意：
            在调用此函数前，确保参数中的起始节点id和结束节点id已经被添加到流程图中。如果这两个id对应的节点不存在，将抛出异常。
        """

        id1 = self.id_mapping[id1]
        id2 = self.id_mapping[id2]

        self.lines.append((id1, id2, self._convert_name(message), dot_line))


class FGantt(markdown_item_base):
    """
    `FGantt`类是一个继承自`markdown_item_base`的类，主要用于在Markdown文件中创建和处理甘特图。甘特图是一种用于描述项目计划执行时间的条形图。在这个类中，用户可以设定甘特图的标题，日期格式，并为甘特图添加项目和相关的时间信息。
    
    以下是使用`FGantt`类的一个简单示例：
    
    ```python
    # 创建一个甘特图实例，标题为"My Project"，日期格式为"YYYY-MM-DD"
    gantt_chart = FGantt("My Project", "YYYY-MM-DD")
    
    # 添加一个名为"Task1"的项目
    gantt_chart.add_item("Task1")
    
    # 为"Task1"项目添加一个名为"start"的时间，日期为"2022-01-01"
    gantt_chart.add_item_data("Task1", "start", "2022-01-01")
    
    # 输出甘特图的Markdown格式
    print(''.join(gantt_chart.flush_row_anchor()))
    ```
    
    属性:
    - `self.Items`：存储甘特图中所有项目的字典。
    - `self.Title`：甘特图的标题。
    - `self.date_format`：甘特图中使用的日期格式。
    
    方法:
    - `__init__(self, gantt_title, date_format='YYYY-MM-DD')`：初始化方法，设置甘特图的标题和日期格式。
    - `flush_row_anchor(self, anchor_str) -> [str]`：返回一个包含整个甘特图Markdown格式的字符串列表。
    - `add_item(self, name)`：在甘特图中添加一个新的项目。
    - `add_item_data(self, key, date_name, date)`：为指定的项目添加时间信息。
    
    错误和Bug:
    暂时没有发现错误和Bug。
    """

    def __init__(self, gantt_title, date_format='YYYY-MM-DD', axisFormat='YYYY-MM-DD'):

        """
        `FGantt`类的初始化方法。
        
        该方法用于创建`FGantt`类的新实例，创建一个甘特图制作工具。甘特图是一种常用的项目管理工具，用于描述项目的各个阶段如何随时间推移进行。该类帮助用户创建和管理甘特图的数据，并提供将其输出到Markdown文件的方法。
        
        参数:
        gantt_title: str, 甘特图的标题。
        date_format: str, 可选参数，默认为'YYYY-MM-DD'，表示日期格式。用于解析和格式化甘特图中的日期数据。
        
        返回:
        无返回值。
        
        示例:
        ```python
        gantt = FGantt('My Project')
        gantt.add_item('Task 1')
        gantt.add_item_data('Task 1', 'Start', '2020-01-01')
        gantt.add_item_data('Task 1', 'End', '2020-02-01')
        out_str = gantt.flush_row_anchor()
        print('\n'.join(out_str))
        ```
        以上代码将创建一个名为"My Project"的甘特图项目，添加一个名为"Task 1"的任务，并为该任务设定开始和结束日期。然后，该代码将生成一个Markdown格式的甘特图，并打印出来。
        
        注意:
        目前还没有发现错误或bug。
        """

        self.Items = {}
        self.Title = gantt_title
        self.date_format = date_format
        self.axis_format = axisFormat

    def flush_row_anchor(self, anchor_str) -> [str]:

        """
        此函数用于生成带有甘特图信息的markdown文本。
        
        参数：
            anchor_str (str): 锚点字符串，但在函数内部并未使用此参数。
        
        返回：
            list: 返回一个包含markdown格式的甘特图信息的字符串列表。
        
        此函数会生成一个markdown格式的甘特图。首先添加mermaid和gantt的声明，然后添加日期格式和标题。接着，遍历Items字典中所有的项目，为每一个项目创建一个section，然后在section中添加所有的时间段。最后添加结束的声明。
        """

        out_str = ['```mermaid\n', 'gantt\n', f'\tdateFormat {self.date_format}\n',
                   f'axisFormat {self.axis_format}\n', f'\ttitle {self.Title}\n']

        for item_key, times in self.Items.items():
            out_str.append(f"\tsection {item_key}\n")
            for t_key, t_time_tulp in times['dates'].items():
                out_str.append(f"\t{t_key}\t:{t_time_tulp[0]}, {t_time_tulp[1]}\n")

        out_str.append('```\n')
        return out_str

    def add_item(self, name):

        """
        这是一个添加项目的方法，用于在Gantt图中插入一个新的项目。
        
        参数:
            name (str): 一个字符串，用于表示项目的名称。该名称将被用作项目在Gantt图中的标识。
        
        返回:
            None
        
        示例:
        
            # 创建一个新的Gantt图对象
            g = FGantt('项目进度')
        
            # 增加一个名为 '任务1' 的项目
            g.add_item('任务1')
        
        此方法不包含任何异常处理，如果传入的name参数不是字符串类型，程序可能会崩溃。
        """

        self.Items[name] = {
            'dates': {}
        }

    def add_item_data(self, key, date_name, date):

        """
        这是FGantt类的一个方法，用于向指定的项目添加具体的日期数据。
        
        参数:
            key (str): 在Items字典中的键，也是项目的名称。
            date_name (str): 日期的名称，比如可以是项目的开始日期或结束日期等。
            date (tuple): 一个包含具体日期信息的元组，第一个元素是日期的开始时间，第二个元素是日期的结束时间。
        
        返回:
            无
        
        使用例子:
            gantt = FGantt('Project Schedule')
            gantt.add_item('Task1')
            gantt.add_item_data('Task1', 'start_date', ('2021-01-01', '2021-01-31'))
        
        注意:
            1. 请保证key和date_name的唯一性，否则可能会覆盖已有的数据。
            2. date的格式应符合提供给FGantt类的date_format参数。
        """

        self.Items[key]['dates'][date_name] = date

# mf = MFlowchart()
# mf.add_sub_graph("sub_a", "sub_a")
# mf.add_node("node1","n1",sub_graph_id="sub_a")
# mf.add_node("node3","n3",sub_graph_id="sub_a")
# mf.add_node("node2","n2")
# mf.add_line("sub_a","n2")
#
# sss="".join(mf.flush_row_anchor(None))
# pass

# class SubFlowChart(MFlowchart):
#     def __init__(self, oriented='TB'):
#         super().__init__()
#         self.sub_lines = {}
#         self.oriented = oriented
#
#     def add_sub_lines(self, id1, id2, sub_name, message=None, dot_line=False):
#         id1 = self.id_mapping[id1]
#         id2 = self.id_mapping[id2]
#
#         if sub_name not in self.id_mapping:
#             self.id_mapping[sub_name] = f"id_{len(self.id_mapping)}"
#
#         if sub_name not in self.sub_lines:
#             self.sub_lines[sub_name] = []
#         self.sub_lines[sub_name].append((id1, id2, self._convert_name(message), dot_line))
#
#     def add_sub_chart(self):
#         self.lines.append(self.sub_lines)
#         self.sub_lines.clear()
#
#     def _format_line(self, line, lines):
#         if line[2] is None:
#             if line[3]:
#                 lines.append(f"{line[0]} -.-> {line[1]} \n")
#             else:
#                 lines.append(f"{line[0]} --> {line[1]} \n")
#         else:
#             if line[3]:
#                 lines.append(f"{line[0]} -.->|{line[2]}| {line[1]} \n")
#             else:
#                 lines.append(f"{line[0]} -->|{line[2]}| {line[1]} \n")
#
#         return lines
#
#     def flush_row_anchor(self, anchor_str) -> [str]:
#         lines = ['```mermaid\n', f'flowchart {self.oriented}\n']
#         for node in self.nodes:
#             if node[0] in self.node_shape:
#                 splite = self.node_shape[node[0]].split("%%")
#                 left_c = splite[0]
#                 right_c = splite[1]
#             else:
#                 left_c = '['
#                 right_c = ']'
#
#             if node[0] in self.node_icon:
#                 node_str = f"fa:{self.node_icon[node[0]]} {node[1]}"
#             else:
#                 node_str = node[1]
#
#             lines.append(f"{node[0]}{left_c}{node_str}{right_c} \n")
#
#         for line in self.lines:
#             if isinstance(line, dict):  # 流程子图
#                 for sub_name, sub_lines in line.items():
#                     # 子图之间的连接必须使用id编号
#                     lines.append(f'subgraph {self.id_mapping[sub_name]} [{sub_name}]\n')
#                     for _line in sub_lines:
#                         lines = self._format_line(_line, lines)
#                     lines.append('end \n')
#             else:
#                 lines = self._format_line(line, lines)
#
#         for k in self.node_navigate.keys():
#             v = self.node_navigate[k]  # self.node_navigate[k].lower().replace(' ', '-')
#             lines.append(f'click {k} href "#{v}"\n')
#
#         for node_color_key in self.node_color:
#             lines.append(f"style {node_color_key} fill:{self.node_color[node_color_key]}\n")
#
#         lines.append("```\n")
#         return lines
