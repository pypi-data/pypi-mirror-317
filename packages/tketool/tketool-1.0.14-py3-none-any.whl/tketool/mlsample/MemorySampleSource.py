# pass_generate
from tketool.mlsample.NLSampleSource import NLSampleSourceBase


class Memory_NLSampleSource(NLSampleSourceBase):
    """
    Memory_NLSampleSource是一个继承自NLSampleSourceBase基类的类，用于处理和存储数据样本。
    
    类的主要方法包括创建新的数据集、检查数据集是否存在、添加数据行、获取元数据键、获取目录列表、遍历数据和指针、删除数据集、加载指针数据、获取数据集数量以及处理附件。
    
    此类主要在内存中维护一个数据字典，对数据集的各种操作都是对这个字典的操作。使用前需要先实例化对象，再调用相应的方法。
    
    主要方法说明：
    - `__init__`: 初始化方法，创建空的数据字典。
    - `create_new_set`: 创建新的数据集，如果数据集已存在则抛出异常。返回操作是否成功的布尔值。
    - `has_set`: 检查指定名称的数据集是否存在。返回布尔值。
    - `add_row`: 向指定数据集添加一行数据。返回操作是否成功的布尔值。
    - `get_metadata_keys`: 获取指定数据集的元数据键。返回一个包含元数据的字典。
    - `get_dir_list`: 获取所有数据集的目录列表。返回一个包含所有数据集的元数据和数量的字典。
    - `iter_data`和`iter_pointer`: 遍历指定数据集的数据和指针。返回一个迭代器。
    - `delete_set`: 删除指定的数据集。
    - `load_pointer_data`: 加载指定数据集的指针数据。返回加载的数据。
    - `get_set_count`: 获取指定数据集的数据数量。返回数据数量。
    - `add_attachment`和`read_attachment`: 操作附件。但当前版本不支持，调用时会抛出异常。
    - `read_one_row`: 读取指定数据集的第一行数据。返回数据。
    
    注意：此类在操作附件时会抛出异常，因为当前版本还不支持。
    
    使用示例：
    ```python
    mem_source = Memory_NLSampleSource()
    mem_source.create_new_set('set1', 'description', ['tag1', 'tag2'], ['key1', 'key2'])
    mem_source.add_row('set1', ['data1', 'data2'])
    print(mem_source.get_dir_list())
    ```
    """



    def __init__(self):
        """
        这是一个基于内存的样本源类，实现了`NLSampleSourceBase`中定义的接口。
        
        该类提供一种快速加载和处理内存中数据的方式，可以创建新的数据集，检查数据集是否存在，向数据集中添加行，获取数据集的元数据等操作。
        
        属性:
        
        - datas(dict): 存储数据的字典，键是数据集的名字，值是一个字典，包含了数据集的各种元数据信息以及数据本身。
        
        使用示例:
        
        ```
        # 创建一个内存样本源对象
        mem_source = Memory_NLSampleSource()
        
        # 创建一个新的数据集
        mem_source.create_new_set('dataset1', 'this is a test dataset', ['tag1', 'tag2'], ['key1', 'key2'])
        
        # 检查一个数据集是否存在
        print(mem_source.has_set('dataset1'))  # 输出: True
        
        # 向一个数据集中添加行
        mem_source.add_row('dataset1', ['data1', 'data2'])
        
        # 获取一个数据集的元数据
        print(mem_source.get_metadata_keys('dataset1'))  # 输出: {'des': 'this is a test dataset', 'tags': ['tag1', 'tag2'], 'label_keys': ['key1', 'key2'], 'base_set': '', 'base_set_process': ''}
        
        # 获取所有数据集的列表
        print(mem_source.get_dir_list())  # 输出: {'dataset1': {'meta': {'des': 'this is a test dataset', 'tags': ['tag1', 'tag2'], 'label_keys': ['key1', 'key2'], 'base_set': '', 'base_set_process': ''}, 'count': 1}}
        ```
        """

        self.datas = {}

    def create_new_set(self, name: str, description: str, tags: [str], keys: [str], base_set="",
                       base_set_process="") -> bool:
        """
        这个类的目的是模拟一个名为Memory_NLSampleSource的内存数据源。它提供一些基本的操作，如创建新的数据集、检查数据集是否存在、添加行、获取元数据键等。这个类最主要的用途是进行数据集的管理和数据操作。
        
        函数 create_new_set 是用来创建新的数据集的。它需要以下输入参数:
        
        - name: str 类型，用于指定新数据集的名称。
        - description: str 类型，用于描述新的数据集。
        - tags: str 类型的列表，用于给新的数据集添加标签。
        - keys: str 类型的列表，用于指定新的数据集的键。
        - base_set: str 类型，是一个可选参数，默认为空字符串，用于指定新的数据集的基础集。
        - base_set_process: str 类型，是一个可选参数，默认为空字符串，用于指定新的数据集的基础集处理方式。
        
        返回值为 bool 类型，如果新增数据集成功，返回True。
        
        值得注意的是，如果在添加新的数据集时，存在名称相同的数据集，程序会抛出一个异常，提示"已存在相同的set"。
        
        此外，这个类不支持添加附件和读取附件，如果尝试调用这两个方法，程序会抛出一个异常，提示"not support"。
        """

        if name in self.datas:
            raise Exception("已存在相同的set")

        self.datas[name] = {
            'name': name,
            'des': description,
            'tags': tags,
            'label_keys': keys,
            'base_set': base_set,
            'base_set_process': base_set_process,
            'data': [],
        }

        return True

    def has_set(self, name: str) -> bool:
        """
        该函数的主要作用是检查给定的名字是否存在于当前数据源中。
        
        参数:
            name (str): 需要查询的数据集名称。
        
        返回:
            bool: 如果数据集存在, 返回True, 否则返回False.
        
        使用示例:
        
        ```python
        memory_sample_source = Memory_NLSampleSource()
        memory_sample_source.create_new_set("test_set", "a description", ["tag1", "tag2"], ["key1", "key2"])
        print(memory_sample_source.has_set("test_set"))  # 输出: True
        print(memory_sample_source.has_set("nonexistent_set"))  # 输出: False
        ```
        注意: 如果查询的数据集名称不存在, 该函数不会引发异常, 而只是返回False.
        """

        return name in self.datas

    def add_row(self, name: str, data: []) -> bool:
        """
        这是一个函数，名为 `add_row`，它的作用是在指定的数据集中添加一条新的数据。
        
        参数：
        - `name` (str)：数据集的名称。
        - `data` (list)：要添加的数据，它是一个列表。
        
        返回类型：
        - `bool`：如果数据成功添加到数据集中，则返回 `True`。
        
        示例：
        ```python
        # 创建一个 Memory_NLSampleSource 实例
        source = Memory_NLSampleSource()
        # 创建一个新的数据集
        source.create_new_set(name='new_set', description='This is a new set', tags=['tag1', 'tag2'], keys=['key1', 'key2'])
        # 在新的数据集中添加数据
        source.add_row(name='new_set', data=['data1', 'data2'])
        ```
        
        注意：
        - 如果数据集名不存在，函数将会引发 KeyError。
        - 此函数不支持并发调用，如果多个线程同时调用此函数可能会导致数据错误。
        """

        self.datas[name]['data'].append(data)
        return True

    def get_metadata_keys(self, name: str) -> {}:
        """
            此函数用于获取指定数据集的元数据键及其对应的值。
        
            参数:
            name: str - 数据集的名称。
        
            返回值:
            dict - 返回一个字典，字典中的每个元素对应数据集的一种元数据，包括'描述'、'标签'、'标签键'、'基础集合'和'基础集合处理'。
        
            示例:
            get_metadata_keys("dataset_name") 返回值可能如下:
            {
                'des': '这是一个用于图像分类的数据集',
                'tags': ['图像', '分类'],
                'label_keys': ['猫', '狗', '鸟'],
                'base_set': '原始数据集',
                'base_set_process': '数据预处理步骤详细描述',
            }
        
            注意:
            如果提供的数据集名称不存在于当前数据源中，此函数将抛出KeyError异常。
        """

        return {
            'des': self.datas[name]['des'],
            'tags': self.datas[name]['tags'],
            'label_keys': self.datas[name]['label_keys'],
            'base_set': self.datas[name]['base_set'],
            'base_set_process': self.datas[name]['base_set_process'],
        }

    def get_dir_list(self) -> {}:
        """
            get_dir_list函数是用来获取所有数据集的元数据以及每个数据集的数据数量。
        
            遍历数据集（datas）的所有键值，对于每一个键值（x_key），
            获取其元数据（通过调用get_metadata_keys方法）和数据数量（通过调用get_set_count方法）。
        
            返回值是一个字典，键值是数据集的名称，值是一个字典，其中包含了元数据（存储在'meta'键值下）以及数据数量（存储在'count'键值下）。
        
            函数不接受任何参数。
        
            返回类型是一个字典，它的键是字符串类型（数据集的名称），值是一个字典，这个字典的键是字符串类型（'meta'和'count'），值的类型分别是字典和整数。
        
            例如：
            假设当前的数据集是{'set1': {'name': 'set1', 'des': 'description1', 'tags': ['tag1', 'tag2'], 'label_keys': ['key1', 'key2'], 'base_set': '', 'base_set_process': '', 'data': [1, 2, 3]}}
        
            那么这个函数的返回值将会是：
            {'set1': {'meta': {'des': 'description1', 'tags': ['tag1', 'tag2'], 'label_keys': ['key1', 'key2'], 'base_set': '', 'base_set_process': ''}, 'count': 3}}
        """

        # 'meta': node,
        # 'count': count,
        # 'filecount': filecount
        return {x_key: {
            'meta': self.get_metadata_keys(x_key),
            'count': self.get_set_count(x_key),
        }
            for x_key in self.datas.keys()}

    def iter_data(self, name: str):
        """
        这是一个用于迭代数据集中数据的函数。
        
        参数:
            name (str): 需要迭代的数据集的名称。
        
        返回:
            iterator: 返回一个迭代器，用于按顺序访问数据集中的所有数据。
        
        示例:
            >>> mem_source = Memory_NLSampleSource()
            >>> mem_source.create_new_set('test', 'This is a test set', [], ['key1', 'key2'])
            >>> mem_source.add_row('test', ['value1', 'value2'])
            >>> for data in mem_source.iter_data('test'):
            ...     print(data)
            ['value1', 'value2']
        
        注意:
            - 如果给定的数据集名称不在内存中，这个函数将会抛出一个KeyError。
            - 这个函数不会改变数据集或数据的状态，可以安全的多次调用。
        """

        for item in self.datas[name]['data']:
            yield item

    def iter_pointer(self, name: str):
        """
        该方法作用于Memory_NLSampleSource类，主要用于生成数据集名称对应的数据索引迭代器。
        
        参数:
        name : str
            数据集名称，用于指定需要生成索引迭代器的数据集。
        
        返回：
            一个生成器，会产生指定数据集中的数据索引，从0开始到数据集的长度。
        
        使用示例：
        
        memory_source = Memory_NLSampleSource()
        memory_source.create_new_set("example_set","An example set",[],[],"")
        memory_source.add_row("example_set", ["data1","data2","data3"])
        pointer_iter = memory_source.iter_pointer("example_set")
        
        for pointer in pointer_iter:
            print(pointer)
        
        上述代码中，首先创建了Memory_NLSampleSource的实例memory_source，然后创建了一个新的数据集"example_set"并添加了一些数据，然后使用iter_pointer方法生成了索引迭代器pointer_iter，最后用for循环遍历并打印出所有的索引。
        
        注意：
        该方法不会对输入的数据集名称进行检查，如果输入的数据集名称不存在于数据源中，会直接导致KeyError异常。使用时需要确保数据集名称的正确性。
        """

        for idx in range(len(self.datas[name]['data'])):
            yield idx

    def delete_set(self, name: str):
        """
        这是一个用于删除已存在的数据集的方法。
        
        参数:
            name: str类型,表示需要删除的数据集的名称。
        
        返回:
            无返回值。
        
        例子:
            delete_set('example_set')将会删除名为'example_set'的数据集。
        
        注意:
            如果传入的名称在数据集中不存在，将会引发KeyError错误。
        """

        del self.datas[name]

    def load_pointer_data(self, name: str, pointer):
        """
        此函数用于加载指定索引位置的数据。
        
        参数:
            name: str类型，数据集的名称
            pointer: 数据索引位置
        
        返回:
            返回给定数据集中指定索引位置（pointer）的数据。
        
        示例:
        >>> data_source = Memory_NLSampleSource()
        >>> data_source.create_new_set("test", "", [], [], "")
        >>> data_source.add_row("test", ["Hello, world!"])
        >>> data_source.load_pointer_data("test", 0)
        ['Hello, world!']
        
        注意:
        这个函数不会检查索引（pointer）是否在数据边界之内，如果提供的索引超过数据边界，会抛出IndexError。
        """

        return self.datas[name]['data'][pointer]

    def get_set_count(self, name: str):
        """
            这个函数用于获取指定数据集的数量。
        
            参数:
            name: str, 指定的数据集的名称。
        
            返回:
            int, 返回指定数据集的数量。
        
            示例:
            ```python
            instance = Memory_NLSampleSource()
            instance.create_new_set('name1', 'description1', ['tag1', 'tag2'], ['key1', 'key2'])
            instance.add_row('name1', ['data1', 'data2'])
            print(instance.get_set_count('name1'))  # 输出1
            ```
        """

        return len(self.datas[name]['data'])

    def add_attachment(self, set_name: str, key, data):
        """
        这个方法是在类Memory_NLSampleSource中定义的，该类主要用于管理和存储数据集样本的相关信息，不过这个方法并未实现任何功能，尝试调用这个方法将会触发一个异常。
        
        方法名称：add_attachment
        参数：
            set_name (str): 数据集的名字。
            key: 该参数在当前方法中没有用到。
            data: 该参数在当前方法中没有用到。
        返回：
            无返回值。
        异常：
            如果调用该方法，将会触发一个异常，提示"not support"。
        
        注意：在当前版本中，这个方法并未实现，如果你尝试调用它，将会触发一个异常。
        """

        raise Exception("not support")

    def read_attachment(self, set_name: str):
        """
        这个函数是在Memory_NLSampleSource类中定义的，用于读取指定数据集(set_name)的附加信息，但实际上并未实现这个功能，因此当调用此函数时，会抛出一个"Not support"的异常。
        
        参数:
            set_name (str): 需要读取附加信息的数据集名称。
        
        返回:
            抛出异常。
        
        示例:
            ```python
            mem = Memory_NLSampleSource()
            mem.read_attachment('dataset_name')
            ```
        
        注意：
            这个函数并未实现，调用时会抛出异常。
        """

        raise Exception("not support")

    def read_attachment_keys(self, set_name: str):
        raise Exception("not support")

    def read_one_row(self, set_name: str):
        """
        这个函数的目的是从给定的集合(set)中读取一行数据。
        
        Args:
            set_name: str类型，表示需要读取的数据集的名称。
        
        Returns:
            返回类型是list，返回从数据集中读取的第一行数据。
        
        Usage:
            例如，我们有一个名为'example_set'的数据集，我们可以通过以下方式读取第一行数据：
            ```python
            data_source = Memory_NLSampleSource()
            first_row = data_source.read_one_row('example_set')
            ```
        
        注意:
            - 如果给定的集合名称不存在，将会抛出一个KeyError异常。
            - 如果数据集为空（即没有数据行），此函数将返回一个空列表。
        """

        return self.datas[set_name]['data'][0]
