# pass_generate
from tketool.ml.modelbase import Model_Base


class mapping(Model_Base):
    """
    `mapping`类是一个从`Model_Base`继承的子类，主要用于实现左右两个实体之间的映射。这个类主要含有三个方法：`add`，`left`和`right`。
    
    'add'方法用于添加一个新的左实体到右实体的映射关系。这个映射关系被存储在'content'列表中，并且每个映射的索引会被添加到对应的左或者右实体的字典中。
    
    'left'方法接受一个左实体作为参数，返回所有与这个左实体关联的右实体。
    
    'right'方法接受一个右实体作为参数，返回所有与这个右实体关联的左实体。
    
    一个例子如下：
    
    ```python
    # 实例化mapping类
    m = mapping()
    # 添加映射关系
    m.add('a', '1')
    m.add('b', '2')
    m.add('a', '3')
    # 查询关联的实体
    print(m.left('a'))  # 输出：['1', '3']
    print(m.right('2'))  # 输出：['b']
    ```
    
    无已知错误或者bug。注意：这个类不支持删除已经添加的映射关系，如果需要这个功能，请在子类中实现。
    """

    @property
    def model_name(self):
        """
        mapping类是Model_Base的子类，主要用于建立左右两个对象之间的映射关系。每个对象都包含一个字典属性和一个内容列表。
        
        - model_name方法是一个属性方法，返回类名"mapping"。
        
        类的使用示例：
        
        ```python
        map_obj = mapping()
        map_obj.add('a', '1')  # 建立'a'和'1'的映射关系
        map_obj.add('a', '2')  # 建立'a'和'2'的映射关系
        map_obj.add('b', '1')  # 建立'b'和'1'的映射关系
        print(map_obj.left('a'))  # 输出['1', '2']
        print(map_obj.right('1'))  # 输出['a', 'b']
        ```
        """

        return "mapping"

    def __init__(self):
        """
        这是一个名为“mapping”的类的初始化函数，该类继承了Model_Base基类。该类主要用于建立和查询左右两个元素之间的映射关系。
        
        在初始化过程中，首先调用基类的初始化函数，然后创建了三个用于保存映射关系的字典：'left_dic'，'right_dic'和'content'。
        
        - 'left_dic'用于保存左侧元素到右侧元素的映射关系，其形式为{左侧元素：[对应的右侧元素的索引]}
        - 'right_dic'用于保存右侧元素到左侧元素的映射关系，其形式为{右侧元素：[对应的左侧元素的索引]}
        - 'content'用于保存映射关系的内容，其形式为[[左侧元素，右侧元素]]
        
        此外，这个函数没有明显的错误或者bug。
        
        这是一个示例代码来说明如何使用这个类：
        
        ```
        map = mapping()
        map.add('a', '1')
        map.add('b', '1')
        map.add('a', '2')
        print(map.left('a'))  # 输出：['1', '2']
        print(map.right('1'))  # 输出：['a', 'b']
        ```
        """

        super().__init__()
        self.save_variables['left_dic'] = {}
        self.save_variables['right_dic'] = {}
        self.save_variables['content'] = []
        # self.left_dic = {}
        # self.right_dic = {}
        # self.content = []

    def add(self, left, right):
        """
        该 `add` 方法用于在映射模型类中添加新的映射关系。
        
        参数:
            left (任意类型): 左侧的映射元素。用作映射的键。
            right (任意类型): 右侧的映射元素。用作映射的值。
        
        返回值:
            无返回值。
        
        使用方法:
            `add` 方法用于向映射模型中添加新的映射关系。例如：
            ```python
            mapping_obj = mapping()
            mapping_obj.add('apple', '苹果')
            ```
            在这个例子中，`left` 参数是 'apple'，`right` 参数是 '苹果'。执行 `add` 方法后，在映射模型中添加了一个新的从 'apple' 到 '苹果' 的映射关系。
        
        注意事项:
            当 `left` 或 `right` 参数在映射模型中不存在时，会在映射模型的 'left_dic' 或 'right_dic' 属性中添加一个新的键，并将键对应的值设置为一个空列表。然后，为该列表添加包含映射关系的索引。
            当 `left` 或 `right` 参数在映射模型中已存在时，只会在其对应的列表中添加新的映射关系索引。
        """

        index = len(self.save_variables['content'])
        self.save_variables['content'].append([left, right])
        if left not in self.save_variables['left_dic']:
            self.save_variables['left_dic'][left] = []
        self.save_variables['left_dic'][left].append(index)
        if right not in self.save_variables['right_dic']:
            self.save_variables['right_dic'][right] = []
        self.save_variables['right_dic'][right].append(index)

    def left(self, left):
        """
        这个函数用于获取与指定“left”对象相关联的所有“right”对象。
        
        这个函数接受一个参数：
        - left: 我们想要查询的左边的对象。
        
        返回值：
        - 如果left存在在left_dic字典中，函数会返回一个列表，其中包含与left关联的所有right对象。
        - 如果left不存在在left_dic字典中，函数会返回None。
        
        举个例子，
        假设我们有以下的映射关系：{'a': ['x', 'y'], 'b': ['y', 'z']}，那么left('a')将返回['x', 'y']。
        """

        if left in self.save_variables['left_dic']:
            return [self.save_variables['content'][idx][1] for idx in self.save_variables['left_dic'][left]]
        return None

    def right(self, right):
        """
        此方法用于获取映射关系中对应于给定右侧元素的左侧元素。
        
        参数:
            right: 需要查询映射关系的右侧元素。
        
        返回:
            如果右侧元素存在于映射关系中，则返回一个列表，其中包含对应于给定右侧元素的所有左侧元素；
            如果右侧元素不存在于映射关系中，则返回None。
        
        例如:
            假设我们已经添加了如下映射关系: (1, 'a'), (2, 'a'), (3, 'b')
            如果我们调用right('a')，那么将返回[1, 2]
            如果我们调用right('b')，那么将返回[3]
            如果我们调用right('c')，那么将返回None
        
        错误或者bug:
            没有发现错误或者bug。
        """

        if right in self.save_variables['right_dic']:
            return [self.save_variables['content'][idx][0] for idx in self.save_variables['right_dic'][right]]
        return None
