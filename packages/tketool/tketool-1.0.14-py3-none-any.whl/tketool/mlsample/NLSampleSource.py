# pass_generate
import abc
from tketool.logs import log


class NLSampleSourceBase(metaclass=abc.ABCMeta):
    """
    这是一个基于abc.ABCMeta元类的NLSampleSourceBase抽象类。这个类定义了一个样本源的通用接口，包括创建新的样本集，检查样本集是否存在，添加行数据，获取元数据键，获取目录列表，迭代数据，迭代指针，删除样本集，加载指针数据，获取样本集的数量，添加附件，读取附件，读取一个行数据等方法。
    
    此抽象类的目的是为了定义一个统一的样本源接口，不同的数据源可以实现这个接口，提供统一的访问方式。这对于大型项目中处理各种各样的数据源非常有用，可以大大提高代码的可维护性和扩展性。
    
    以下是一个可能的使用例子：
    
    ```python
    class MySampleSource(NLSampleSourceBase):
        def create_new_set(self, name: str, description: str, tags: [str], keys: [str], base_set="") -> bool:
            # 在这里实现你的逻辑
    
        # 实现其他的抽象方法...
    ```
    
    注意，由于这是一个抽象类，你不能直接实例化它。你应该创建一个新的类，继承这个抽象类，并实现所有的抽象方法。
    
    此类没有已知的错误或bug。
    """

    @abc.abstractmethod
    def create_new_set(self, name: str, ss, tags: [str], keys: [str], base_set="") -> bool:
        """
        `create_new_set`是一个抽象方法，需要在子类中实现。这个方法的目的是创建一个新的数据集。
        
        参数:
            name (str): 新的数据集的名称。
            description (str): 新的数据集的描述。
            tags ([str]): 新的数据集的标签列表。
            keys ([str]): 新的数据集的关键字列表。
            base_set (str, optional): 基础数据集的名称，这个参数默认为空字符串。
        
        返回:
            bool: 如果新的数据集成功创建则返回True，否则返回False。
        
        用法示例:
            class MySampleSource(NLSampleSourceBase):
                def create_new_set(self, name, description, tags, keys, base_set=""):
                    # 实现创建新数据集的逻辑
                    pass
            source = MySampleSource()
            source.create_new_set("my_new_set", "This is a new set.", ["tag1", "tag2"], ["key1", "key2"])
        
        注意:
            这个方法是抽象方法，不能直接调用，需要在子类中实现。如果在子类中没有实现这个方法，将会在运行时抛出`NotImplementedError`异常。
        """

        pass

    @abc.abstractmethod
    def has_set(self, name: str) -> bool:
        """
        此方法用于检查是否存在指定名称的数据集。
        
        参数:
            name (str): 要检查的数据集的名称。
        
        返回:
            bool: 如果数据集存在则返回True，否则返回False。
        
        示例:
        
        ```python
            nl_sample_source = NLSampleSourceBase()
        
            if nl_sample_source.has_set("my_dataset"):
                print("Dataset exists.")
            else:
                print("Dataset does not exist.")
        ```
        """

        pass

    @abc.abstractmethod
    def add_row(self, name: str, data: []) -> bool:
        """
        此函数是抽象基类NLSampleSourceBase的一个抽象方法，需要在子类中实现。其主要目的是向给定名称的数据集中添加一行数据。
        
        参数:
        name: str，数据集的名称。
        data: list，要添加的数据列表。
        
        返回值:
        bool，如果数据添加成功，则返回True，否则返回False。
        
        示例:
        
        class SampleSource(NLSampleSourceBase):
            data_dict = {}
        
            def add_row(self, name: str, data: []) -> bool:
                if name in self.data_dict:
                    self.data_dict[name].append(data)
                    return True
                return False
        
        source = SampleSource()
        source.add_row('dataset1', ['data'])
        
        注意:
        子类必须实现此方法，否则在实例化子类并调用此方法时会抛出TypeError。
        """

        pass

    @abc.abstractmethod
    def get_metadata_keys(self, name: str) -> {}:
        """
        根据提供的名称，获取元数据键的抽象方法。
        
        参数:
            name (str): 数据集的名称。
        
        返回:
            dict: 返回一个字典，字典的键是元数据的键，值是具体的元数据内容。
        
        注释:
            这是一个抽象方法，需要在子类中实现。在使用此方法时，请确保提供的数据集名称存在，否则可能会抛出异常。
        
        示例:
            >>> source = NLSampleSourceBaseSubClass()  # 假设NLSampleSourceBaseSubClass是NLSampleSourceBase的子类
            >>> meta_keys = source.get_metadata_keys("example_set")
            >>> print(meta_keys)
            {'key1': 'value1', 'key2': 'value2'}
        """

        pass

    @abc.abstractmethod
    def get_dir_list(self) -> {}:
        """
            get_dir_list方法是一个抽象方法，需要在子类中实现。该方法的主要目的是获取所有数据集合的目录列表。
        
            返回值:
                返回一个字典。字典的键是数据集合的名称，值是这些数据集合的相关信息。相关信息可能包括但不限于数据集合的元数据和其他相关信息。
        """

        pass

    @abc.abstractmethod
    def iter_data(self, name: str):
        """
        这是一个抽象方法。子类需要实现这个方法以便提供对特定数据集的迭代访问。
        
        参数:
            name (str): 数据集的名称。
        
        返回:
            生成器: 返回一个可以用于迭代数据集每一行的生成器。
        
        示例:
        
            class MySampleSource(NLSampleSourceBase):
                ...
                def iter_data(self, name: str):
                    with open(name, "r") as file:
                        for line in file:
                            yield line.strip().split(",")
                ...
        
            my_source = MySampleSource()
            for row in my_source.iter_data("my_dataset"):
                print(row)
        
        注意: 这个方法只是一个接口，具体实现应该由子类提供。如果子类没有提供特定的实现，那么调用这个方法时会抛出 NotImplementedError 异常。
        """

        pass

    @abc.abstractmethod
    def iter_pointer(self, name: str):
        """
        该函数是一个抽象方法，需要在子类中实现。它的主要目的是迭代并返回一个特定集合的指针。
        
        参数:
            name (str): 需要迭代的集合的名称。
        
        返回:
            此方法的返回类型依赖于具体实现，但通常它会返回一个可迭代的对象，例如列表或生成器。
        
        注意:
            由于这是一个抽象方法，它自身并不执行任何操作。具体的行为将在子类中定义。请参照子类的文档以获取更具体的使用细节和例子。
        
        异常:
            如果集合不存在，或者name参数不是字符串，那么实现此函数的子类可能会抛出异常。具体的行为和异常类型依赖于具体的实现。
        """

        pass

    @abc.abstractmethod
    def delete_set(self, name: str):
        """
        删除指定的数据集
        
        此方法将删除具有给定名称的数据集。此操作是不可撤销的。
        
        参数:
            name (str): 要删除的数据集的名称。
        
        返回:
            此方法没有返回值。
        
        注意:
            此方法不会检查数据集是否存在，如果尝试删除不存在的数据集，它可能会引发错误。
        
        例子:
        
        ```python
        sample_source = NLSampleSourceBase()
        sample_source.delete_set('my_dataset')
        ```
        
        此代码将删除名为'my_dataset'的数据集。如果此数据集不存在，将会引发一个错误。
        
        可能的错误:
            如果尝试删除不存在的数据集，将会引发一个错误。
        
        注意:
            由于此操作无法撤销，因此在调用此方法之前, 应该要小心确认是否真的需要删除此数据集。
        """

        pass

    @abc.abstractmethod
    def load_pointer_data(self, name: str, pointer):
        """
        这是一个抽象方法,由子类实现。该方法的目的是从给定名称的数据集中加载指定的数据。
        
        Args:
            name: str 类型，表示数据集的名称。
            pointer: 指向数据集中特定数据的指针。
        
        Raises:
            由于这个函数是由子类实现的，因此可能会抛出任何类型的异常。具体的异常类型和处理方式依赖于子类的实现。
        
        Returns:
            此函数的返回类型取决于子类的具体实现。通常，它应该返回从数据集中加载的数据。
        
        注意:
            这是一个抽象方法，必须在子类中重写。如果在没有重写的情况下调用，将会引发 NotImplementedError。
        
        示例:
            以下示例假设我们有一个名为 `MySampleSource` 的子类，它实现了 `load_pointer_data` 方法。
        
            ```
            class MySampleSource(NLSampleSourceBase):
                def load_pointer_data(self, name: str, pointer):
                    return my_dataset[name][pointer]
        
            source = MySampleSource()
            data = source.load_pointer_data('my_dataset', 123)
            ```
        """

        pass

    @abc.abstractmethod
    def get_set_count(self, name: str):
        """
        该函数的主要目标是获取指定数据集的数量。
        
        参数:
            name: 字符串，指定的数据集的名称。
        
        返回:
            返回整数，表示指定数据集中的数据条目数。
        
        使用示例：
            示例代码：
                nls = NLSampleSourceBase()
                count = nls.get_set_count('dataset_name')
            在这个示例中，我们首先实例化了一个NLSampleSourceBase对象，然后使用get_set_count方法来获取名为'dataset_name'的数据集的条目数量。
        
        注意：
            由于这是一个抽象方法，因此具体的实现可能会根据不同的子类变化。
            在使用此方法时，需要确保数据集的名称是存在的，否则可能会抛出异常。
        """

        pass

    @abc.abstractmethod
    def add_attachment(self, set_name: str, key, data):
        """
        该函数是用于向指定的数据集添加附件。
        
        参数:
            set_name (str): 数据集的名称。
            key: 附件的键值。该键值应该是可哈希且可用作字典的键。
            data: 要添加的附件数据。
        
        返回类型:
            此方法没有返回值。
        
        注意:
            此方法可能会抛出由于无法找到指定的数据集或者无法添加附件数据导致的异常。
        
        使用示例:
            add_attachment("my_dataset", "my_key", my_data)
        这会将my_data作为附件添加到名为"my_dataset"的数据集中，可以使用"my_key"作为键来获取这个附件。
        
        此函数假定set_name和key不会为None，如果为None则可能会引发错误。
        """

        pass

    @abc.abstractmethod
    def read_attachment_keys(self, set_name: str):
        """
        这是一个抽象方法，需要在子类中实现。该方法的功能是读取指定数据集的附件。
        
        参数:
            set_name (str): 要读取附件的数据集名称。
        
        返回:
            该方法的返回类型取决于具体实现，一般情况下应返回附件的数据。
        
        注意:
            由于这是一个抽象方法，如果在子类中没有实现该方法，那么在调用该方法时将会抛出 `NotImplementedError` 异常。
        
        示例:
            ```python
            class MySampleSource(NLSampleSourceBase):
                def read_attachment(self, set_name: str):
                    # 实现具体的读取附件的逻辑，比如从硬盘中读取某个文件
                    return read_file(set_name)
            ```
        """

        pass

    @abc.abstractmethod
    def read_attachment(self, set_name: str, key: str):
        """
        这是一个抽象方法，需要在子类中实现。该方法的功能是读取指定数据集的附件。

        参数:
            set_name (str): 要读取附件的数据集名称。

        返回:
            该方法的返回类型取决于具体实现，一般情况下应返回附件的数据。

        注意:
            由于这是一个抽象方法，如果在子类中没有实现该方法，那么在调用该方法时将会抛出 `NotImplementedError` 异常。

        示例:
            ```python
            class MySampleSource(NLSampleSourceBase):
                def read_attachment(self, set_name: str):
                    # 实现具体的读取附件的逻辑，比如从硬盘中读取某个文件
                    return read_file(set_name)
            ```
        """

        pass

    @abc.abstractmethod
    def read_one_row(self, set_name: str):
        """
        该抽象方法用于读取指定数据集的一行数据。
        
        Args:
            set_name (str): 指定数据集的名称
        
        Returns:
            该方法应返回一个列表，列表元素为数据集中的一行数据。数据类型可能包括但不限于整型，浮点型，字符串型等。
        
        Raises:
            NotImplementedError: 如果该方法在子类中没有被实现，则会抛出此异常。
        
        注意:
            这是一个抽象方法，需要在子类中实现。具体的实现会根据数据存储和获取的方式有所差别，比如可能会从数据库中获取数据，也可能会从文件中读取数据等。因此，具体的实现需要根据实际的数据存储方式来决定。
        """

        pass

    def arrange_dir_list(self):
        """
        这是一个方法，用于整理目录列表。
        
        这个方法首先通过调用'get_dir_list()'方法获取目录列表。然后，它会创建一个新的字典，其中包含目录列表中每个键的元数据、子项、数量和基础集。
        
        接着，这个方法会遍历新字典中的每个项目，检查每个项目的基础集是否为空。如果基础集不为空，并且基础集在新的字典中，那么这个项目会被添加到其基础集的子项中。否则，这个项目将被置顶输出。
        
        最后，方法将返回新字典中基础集为空的所有项目。
        
        参数:
        无
        
        返回:
        一个字典，其中包含新字典中基础集为空的所有项目。
        
        注意:
        尽管这个方法包含一段被注释掉的代码，但是这段代码基本上是将新的字典打印出来。这可以用于调试或检查新的字典。
        
        错误和bug:
        无
        """

        dir_list = self.get_dir_list()

        new_dic = {key: {
            'meta': dir_list[key]['meta'],
            'children': {},
            'count': dir_list[key]['count'],
            'base_set': dir_list[key]['meta']['base_set']
        } for key in dir_list.keys()}

        for set_key in new_dic.keys():
            if new_dic[set_key]['base_set'] != "":
                if new_dic[set_key]['base_set'] not in new_dic:
                    log(f"没有找到{set_key}的父节点，置顶输出")
                    new_dic[set_key]['base_set'] = ""
                else:
                    base_set_name = new_dic[set_key]['base_set']
                    new_dic[base_set_name]['children'][set_key] = new_dic[set_key]

        # if print:
        #     def printsub(level: int, name, item):
        #         blank_str = ""
        #         for _ in range(level):
        #             blank_str += "\t"
        #         print(f"{blank_str} - {name}({item['count']}): {item['meta']['des']}")
        #         for sub_item in item['children'].keys():
        #             printsub(level + 1, sub_item, item['children'][sub_item])
        #
        #     for key in new_dic.keys():
        #         printsub(0, key, new_dic[key])

        return {key: new_dic[key] for key in new_dic if new_dic[key]['base_set'] == ""}

    def print_markdown_arrange_dir_list(self, path=None, max_length=1000):
        """
        此方法用于以markdown格式打印并整理目录列表。
        
        参数:
            path (str): 输出markdown文件的路径，默认为None，此时会创建一个名为"data_list.md"的文件。
            max_length (int): markdown文档中，每行最大的字符长度。
        
        返回:
            None
        
        此函数首先获取目录列表，然后根据目录列表生成一个新的字典，字典中的每个元素包括：
        - "meta": 元数据
        - "children": 子目录
        - "count": 数据集中的记录数
        - "row_sample": 示例行
        对于每个键，函数都会读取一行数据作为示例，并打印其在markdown文件中的相关信息。
        
        注意：此函数可能会覆盖已存在的文件，因此在使用时请确认文件路径的正确性。
        """

        dir_list = self.get_dir_list()

        local_path = path
        if local_path is None:
            local_path = "data_list.md"

        def doc_to_markdown(s):
            if not isinstance(s, str):
                return s
            alllines = s.split('\n')[:20]
            return "\n >".join(alllines)[:max_length]

        with open(local_path, "w") as file:
            lines = ["[toc]"]
            new_dic = {}
            files_order_list = sorted([k for k in dir_list.keys()], key=lambda item: len(item.split('_')))
            key_pointers = {}
            for set_key in files_order_list:
                row_key = dir_list[set_key]['meta']['label_keys']
                one_row = self.read_one_row(set_key)
                if dir_list[set_key]['meta']['base_set'] == "":
                    new_dic[set_key] = {
                        'meta': dir_list[set_key]['meta'],
                        'children': {},
                        'count': dir_list[set_key]['count'],
                        'row_sample': zip(row_key, one_row)
                    }
                    key_pointers[set_key] = new_dic[set_key]
                else:
                    base_set_name = dir_list[set_key]['meta']['base_set']
                    key_pointers[base_set_name]['children'][set_key] = {
                        'meta': dir_list[set_key]['meta'],
                        'children': {},
                        'count': dir_list[set_key]['count'],
                        'row_sample': zip(row_key, one_row)
                    }
                    key_pointers[set_key] = key_pointers[base_set_name]['children'][set_key]

            def printsub(level: int, name, item):
                blank_str = "#"
                for _ in range(level):
                    blank_str += "#"
                lines.append(f"{blank_str} {name}")
                lines.append(f"**{item['meta']['des']}**")
                lines.append(f"count: {item['count']}")
                for key, val in item['row_sample']:
                    new_val = doc_to_markdown(val)
                    lines.append(f"key: {key}")
                    lines.append(f"> {new_val}")
                    lines.append(" ")
                for sub_item in item['children'].keys():
                    printsub(level + 1, sub_item, item['children'][sub_item])

            for key in new_dic.keys():
                printsub(0, key, new_dic[key])

            file.writelines("\n".join(lines))

    def flush(self):
        """
        这个是一个抽象方法，具体的实现应由继承该基础类的子类进行定义。
        
        方法简介：flush()方法的主要目的是清空或同步缓冲数据。一般在进行文件读写操作或数据库操作时，有可能会先把数据写入到缓冲区，等缓冲区满了或手动调用flush()方法时，才真正的将数据写入到文件或数据库。对于一些需要立即看到写入效果的操作，可能需要在写入后立即调用此方法。
        
        参数列表：该方法不接受任何参数。
        
        返回类型：由于这是一个抽象方法，所以没有具体的返回值类型，具体的返回值类型由子类实现的flush()方法决定。
        
        使用示例：由于这是一个抽象方法，没有具体的使用例子。但是一般在子类中，可以按照如下方式进行实现和使用：
        
        class ChildClass(NLSampleSourceBase):
            def flush(self):
                # 实现flush操作
                print('flush')
        
        child_class = ChildClass()
        child_class.flush()  # 输出: flush
        
        注意: 这是一个抽象方法，如果子类没有实现这个方法，那么在实例化子类时，Python解释器会抛出TypeError的错误。
        """

        pass



