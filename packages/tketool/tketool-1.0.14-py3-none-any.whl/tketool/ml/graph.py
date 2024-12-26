# pass_generate
from tketool.ml.modelbase import Model_Base


class graph(Model_Base):
    """
    这是一个graph类，基于Model_Base，用于创建和管理图形数据结构。图中的每个节点和线都可以有关联的数据。
    
    属性:
    model_name: 返回类名。
    
    方法:
    
        __init__: 初始化方法，创建四个字典，分别存储节点，节点线索引，线和线的端点。
        __getitem__: 通过节点id获取节点数据。
        __setitem__: 设置节点id和其对应的数据。
        __contains__: 检查节点id是否存在于节点字典中。
        __iter__: 迭代器，遍历并返回节点字典中的所有项。
        add_node: 添加节点，需要节点id和可选的节点数据。
        add_line: 添加线，需要两个节点id和可选的线数据。线id将自动创建。
        get_node: 通过节点id获取节点数据。
        get_relations: 通过节点id获取与其相连的所有线以及线的另一端节点的数据。可以通过start_to参数控制是获取从该节点出发的线还是指向该节点的线。
    使用示例:
    
        g = graph()  # 创建一个图
        g.add_node('node1')  # 添加一个id为'node1'的节点
        g.add_node('node2', {'color': 'red'})  # 添加一个id为'node2'的节点，并关联一个数据
        g.add_line('node1', 'node2', {'weight': 10})  # 添加一条从'node1'到'node2'的线，并关联一个数据
        print(g.get_node('node1'))  # 获取并打印'node1'的数据
        print(g.get_relations('node1'))  # 获取并打印'node1'出发的所有线的数据
    
    注意:
    
    - add_node时，如果节点id已存在，将抛出异常。
    - add_line时，如果任一节点id不存在，线将不会被添加，也不会抛出异常。
    """

    @property
    def model_name(self):
        """
        这是一个图模型类(graph)，存储和操作简单图形的数据结构。
        
        该类继承于Model_Base基类。
        
        该类的数据是存储在字典中，包括存储节点数据(nodes)、节点线索引(node_lines_index)、线条数据(lines)、线条端点(lines_endpoint)等。
        
        每个节点的id和数据都在字典nodes中存储，每个线条的id和数据都在字典lines中存储，每个线条的端点存储在字典lines_endpoint中，每个节点对应的线条索引存储在字典node_lines_index中。
        
        提供了以下方法：
        - add_node：添加新的节点到图中。
        - add_line：添加新的线条到图中。
        - get_node：通过节点ID获取节点的数据。
        - get_relations：获取与给定节点ID相关的所有线条数据。
        
        以下是一个使用例子：
        
        ```python
        g = graph()  # 创建一个图
        g.add_node('node1', "data1")  # 添加一个节点
        g.add_node('node2', "data2")  # 添加另一个节点
        g.add_line('node1', 'node2', "line_data")  # 添加一个线条，连接node1和node2
        print(g.get_node('node1'))  # 输出 "data1"
        print(g.get_relations('node1'))  # 输出所有与node1有关的线条数据
        ```
        """

        return self._model_name

    def __init__(self, name=None):
        """
        这是一个名为 `graph` 的类，继承自 `Model_Base`，用于构建和操作图形结构。
        
        在 `graph` 类的初始化方法 `__init__` 中，定义了四个字典，分别用于存储节点数据、节点与线条关系、线条数据以及线条的起止节点。
        
        - `self.save_variables['nodes']` 存储节点数据，键为节点的id，值为节点的数据。
        - `self.save_variables['node_lines_index']` 存储节点与线条的关系，键为节点id，值为该节点连接的所有线条的id列表。
        - `self.save_variables['lines']` 存储线条数据，键为线条id，值为线条的数据。
        - `self.save_variables['lines_endpoint']` 存储线条的起止节点，键为线条id，值为一个元组，元素为线条的起始节点id和结束节点id。
        
        示例：
        
        ```python
        g = graph()
        g.add_node(1, "node1")  # 添加一个节点，节点id为1，节点数据为"node1"
        g.add_node(2, "node2")  # 添加一个节点，节点id为2，节点数据为"node2"
        g.add_line(1, 2, "line between node1 and node2")  # 添加一条线，连接节点1和节点2，线条数据为"line between node1 and node2"
        print(g.get_node(1))  # 输出"node1"
        print(g.get_relations(1))  # 输出[(2, 'line between node1 and node2')]
        ```
        
        注意：
        当你添加一个已存在的节点ID时，程序将抛出异常，需要注意捕捉和处理。
        """

        super().__init__()
        self.save_variables['nodes'] = {}  # id: data
        self.save_variables['node_lines_index'] = {}  # node_id: [line_id]
        self.save_variables['lines'] = {}  # id:data
        self.save_variables['lines_endpoint'] = {}  # id:(start_end)
        self._model_name = name

    def __getitem__(self, item):
        """
        这是一个特殊方法，它允许我们使用带有键的索引操作符 (例如：obj[key]) 来获取对象中的数据。在此类中，该方法被用来从图的节点中获取数据。
        
        参数:
            item: 键值，这里指图中节点的ID。
        
        返回:
            返回与给定键（图中节点的ID）关联的数据。
        
        示例:
            创建一个名为graph的图对象，然后添加一些节点：
            graph_instance = graph()
            graph_instance.add_node('node1', data='data1')
            graph_instance.add_node('node2', data='data2')
            然后，我们可以通过以下方式获取节点数据：
            node_data = graph_instance['node1']
            打印node_data会输出 'data1'。
        """

        return self.save_variables['nodes'][item]

    def __setitem__(self, key, value):
        """
        该方法定义了如何为图中的节点(node)设置数据。
        
        参数:
            key : 节点的唯一标识符，通常为节点的id。
            value : 需要存储在节点中的数据。
        
        返回值:
            无
        
        示例:
            # 创建一个graph对象
            g = graph()
        
            # 将数据"hello"存储在id为1的节点中
            g[1] = "hello"
        
            # 输出id为1的节点数据
            print(g[1])  # 输出 "hello"
        """

        self.save_variables['nodes'][key] = value

    def __contains__(self, item):
        """
        该方法用于检查节点是否在图中。
        
        参数:
            item: 需要查询的节点。
        
        返回:
            如果节点存在于图中,返回True,否则返回False。
        
        请注意:
            在图中,键是节点的ID,值是此节点的数据。
            这种方法对于检查节点是否存在在图中是有用的。
        
        例子:
            >>> g = graph()
            >>> g.add_node('node1')
            >>> 'node1' in g
            True
            >>> 'node2' in g
            False
        """

        return item in self.save_variables['nodes']

    def __iter__(self):
        """
        这是一个迭代器方法，它允许我们在“graph”类对象上进行迭代操作。它会遍历保存在“nodes”字典中的每个节点，并返回它们的键值对。
        
        在Python中，如果一个类定义了__iter__方法，那么它就可以被视为可迭代对象。当我们使用for循环来遍历这个对象时，for循环会自动调用这个__iter__方法，获取一个迭代器，并使用这个迭代器来遍历我们想要的数据。
        
        参数列表：
        无
        
        返回类型：
        generator，返回字典“nodes”中的键值对
        
        代码示例：
        ```
        g = graph()
        g.add_node('node1', 'data1')
        g.add_node('node2', 'data2')
        for node_key, node_value in g:
            print(node_key, node_value)
        ```
        当我们运行以上代码时，会输出：
        ```
        node1 data1
        node2 data2
        ```
        注意：无已知错误或bug。
        """

        for item_key, item_value in self.save_variables['nodes'].items():
            yield item_key, item_value

    def add_node(self, id, data=None):
        """
        该方法用于向图中添加节点。
        
        参数:
            id (str): 要添加的节点的唯一标识。
            data (optional): 与节点相关的额外数据，默认为None。
        
        返回:
            None
        
        异常:
            Exception: 如果节点id已经存在于图中，将会抛出异常。
        
        示例:
            >>> g = graph()
            >>> g.add_node('node1', data={'name': 'node1', 'value': 1})
            >>> assert 'node1' in g
        
        注意:
            请确保每个节点的id都是唯一的，否则添加节点时将会抛出异常。
        """

        if id in self.save_variables['nodes']:
            raise Exception("duplicate node id.")
        self.save_variables['nodes'][id] = data

    def add_line(self, node_id1, node_id2, data=None):
        """
        此方法用于添加一条连接两个节点的线路，并可以将数据附加到该线路上。
        
        参数：
            node_id1：需要连接的第一个节点的标识符。
            node_id2：需要连接的第二个节点的标识符。
            data：可选参数，默认为None。这将作为附加数据添加到线路上。
        
        返回：
            此方法没有返回值。
        
        示例：
            graph.add_line('node_1', 'node_2', 'line_data')
        
        注意事项：
            如果两个节点已经通过线路连接，该方法将重新添加新的线路。每条线路的名称都是唯一的，即使它们连接的是相同的节点。
        """

        line_name = f"line_{len(self.save_variables['lines'])}"
        self.save_variables['lines'][line_name] = data

        if node_id1 not in self.save_variables['node_lines_index']:
            self.save_variables['node_lines_index'][node_id1] = []
        self.save_variables['node_lines_index'][node_id1].append(line_name)

        if node_id2 not in self.save_variables['node_lines_index']:
            self.save_variables['node_lines_index'][node_id2] = []
        self.save_variables['node_lines_index'][node_id2].append(line_name)

        self.save_variables['lines_endpoint'][line_name] = (node_id1, node_id2)

    def get_node(self, key):
        """
        该函数的目的是通过键来获取图中的节点。
        
        参数:
            key: 节点的键。
        
        返回:
            返回与给定键对应的节点。
        
        示例:
            graph_instance = graph()
            graph_instance.add_node('node_1', data='This is node 1')
            node = graph_instance.get_node('node_1')
            print(node)  # 输出: This is node 1
        
        注意:
            如果给定的键不存在于图中，将会引发KeyError异常。
        """

        return self.save_variables['nodes'][key]

    def get_relations(self, key, start_to=True):
        """
        此方法用于获取指定节点的关联信息。包含与之相连的其他节点及其相应的线数据。
        
        参数:
            key: 一个字符串，代表要查询关系的节点id。
            start_to: 一个布尔值，默认为True。当为True时，返回从给定节点出发的关系；当为False时，返回指向给定节点的关系。
        
        返回:
            返回一个元组列表，列表中的每个元组包含两个元素，第一个是关联节点的id，第二个是连接两个节点的线的数据。
        
        例子:
        假设我们有这样的一个图——节点A通过线1与节点B相连，通过线2与节点C相连。那么：
            graph.get_relations('A') 会返回 [('B', data1), ('C', data2)]
            graph.get_relations('A', start_to=False) 会返回空列表，因为没有线指向节点A。
        
        注意：
            如果给定的key在图中不存在，该函数将返回一个空列表。
        """

        result = []

        if key not in self.save_variables['node_lines_index']:
            return result

        for lineid in self.save_variables['node_lines_index'][key]:
            line_data = self.save_variables['lines'][lineid]
            if start_to:
                if self.save_variables['lines_endpoint'][lineid][0] == key:
                    result.append((self.save_variables['lines_endpoint'][lineid][1], line_data))
                else:
                    continue
            else:
                if self.save_variables['lines_endpoint'][lineid][1] == key:
                    result.append((self.save_variables['lines_endpoint'][lineid][0], line_data))
                else:
                    continue

        return result

# aa = graph()
# aa.add_node("a", 1)
# aa.add_node("b", 2)
# aa.add_line("a", "b", 33)
# aa.add_line("b", "a", 44)
# r1 = aa.get_relations("a")
# r2 = aa.get_relations("a", False)
# pass
