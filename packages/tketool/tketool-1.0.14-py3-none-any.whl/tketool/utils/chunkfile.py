# pass_generate
import os, pickle, io
import time


class chunk_file():
    """
    这是一个chunk_file类，其主要目的是实现在一个大文件上的键值存储。它将所有的key和相应的value存储起来，每个value存储在文件的某个位置，这个位置由key指示。这个类的设计使我们可以在不必将整个文件加载到内存的情况下高效地获取键值。这在处理大数据集时非常有用，尤其是当数据集大到无法完全装入内存时。
    
    示例使用方法如下：
    
    创建一个实例：
    ```python
    cf = chunk_file('example')
    ```
    
    添加键值对：
    ```python
    cf.add('key1', 'value1')
    cf.add('key2', 'value2')
    ```
    
    获取键值对：
    ```python
    value1 = cf.get('key1')  # 返回'value1'
    value2 = cf.get('key2')  # 返回'value2'
    ```
    
    该类的主要方法和属性如下：
    
    - `__init__(file_path)`：初始化方法，`file_path`是将要存储数据的文件路径。
    
    - `__contains__(item)`：判断`item`是否在当前的键值对中。
    
    - `__iter__()`：返回一个迭代器，可以遍历所有的键值对。
    
    - `__getitem__(key)`：获取给定`key`对应的值。
    
    - `verify_data()`：验证所有的数据是否完整，因为该方法只是简单地遍历所有数据，所以总是返回True。
    
    - `add(key, value)`：向文件中添加一对键值对，返回存储的值的长度。
    
    - `get(key)`：获取给定`key`对应的值。
    
    - `flush()`：将当前的键值对写入硬盘。
    
    注意，这个类没有提供删除或修改数据的方法。另外，在使用这个类时，需要确保操作系统支持大文件的处理。
    """

    def __init__(self, file_path):
        """
        这是一个名为`chunk_file`的类，其目的是为了处理二进制文件，并将其分块存储以便更有效地进行搜索和访问。
        
        这个类可以以键值对的形式存储和读取二进制数据，其中键用于标识特定的数据块，而值则是要存储的实际数据。
        数据将被pickle化并存储在二进制文件中，同时还会创建一个索引字典，其中包含每个键对应的文件位置和长度信息。
        此索引字典也会作为一个.key文件存储在磁盘上，以便在后续的会话中快速加载和访问。
        
        类的初始化方法：`__init__(self, file_path)`
        此方法是为了初始化一个`chunk_file`对象。
        
        参数：
            file_path：存储数据块的二进制文件的路径。
        
        它会首先根据提供的file_path生成.key和.value文件的路径。
        然后，它会尝试从.key文件加载索引字典，如果文件不存在，则会创建一个空的索引字典。
        最后，它会打开.value文件以便后续的读写操作。
        """

        self.key_file_path = file_path + ".key"
        self.value_file_path = file_path + ".value"

        self.index_dict = {}
        self.write_next_loc = 0

        if os.path.exists(self.key_file_path):
            with open(self.key_file_path, "rb") as ff:
                self.index_dict = pickle.load(ff)

        open(self.value_file_path, "ab").close()
        self.file_obj = open(self.value_file_path, "rb+")

    def __contains__(self, item):
        """
        这是一个魔法方法，用于支持 `in` 操作符。它检查一个给定的键（item）是否在 `index_dict` 字典中。这个字典存储了文件的索引信息，其中键是数据的标识符，值是数据在文件中的位置和长度。
        
        参数：
            item：需要查询的键。
        
        返回：
            bool：如果键在 `index_dict` 中，返回 True，否则返回 False。
        """

        return item in self.index_dict

    def __iter__(self):
        """
        这是一个迭代器方法，用于将类的实例对象作为迭代器使用。
        
        在每一次迭代时，它会返回一个元组，元组的第一个元素为键，第二个元素是通过get方法得到对应的值。
        
        这个方法允许我们遍历整个索引字典，同时获取字典中每一个键对应的值。
        
        例如：
        ```python
        chunk = chunk_file("your_file_path")
        for key, value in chunk:
            print(f"Key: {key}, Value: {value}")
        ```
        
        注意：
        如果getitem方法无法获取到key对应的值，get方法会返回None，这时迭代出的value也就是None。
        
        参数列表：
        无
        
        返回类型介绍：
        返回一个元组，元组的第一个元素为键，第二个元素是通过get方法得到对应的值。
        
        错误或者bug：
        暂无
        """

        for item_key in self.index_dict.keys():
            yield item_key, self.get(item_key)

    def __getitem__(self, key):
        """
        该方法实现了类的特殊方法__getitem__，使得类对象可以通过key值索引查询到对应的value。
        
        参数:
            self: 类的实例。
            key: 需要查询的键值。
        
        返回:
            通过pickle模块反序列化后的数据。
        
        例子:
            chunk = ChunkFile('some_file')
            value = chunk['some_key']  # 使用__getitem__方法查询对应的value值。
        
        注意:
            如果查询的key值不存在于index_dict字典中，那么方法会返回None。
        """

        return self.get(key)

    def verify_data(self):
        """
        此函数用于验证存储的数据是否可以正常读取，主要是验证存储数据的完整性。它会遍历类内部的所有键值对，尝试读取每个键的值，但并不实际返回任何值。如果在读取过程中没有发生任何错误，说明存储的数据是完整的，此时返回True。如果在读取过程中发生了错误，此函数会抛出异常。
        
        参数:
        无
        
        返回:
            Boolean : 如果所有数据都被成功读取，返回True。
        
        使用示例:
        >>> cf = chunk_file('test_file')
        >>> cf.add('key1', 'value1')
        >>> cf.verify_data()
        True
        
        注意：
        此函数没有捕获可能抛出的异常，因此在使用时需要配合try...except...结构使用，以捕获可能出现的读取错误。
        
        错误与异常：
        如果在读取数据时出现错误，此函数会抛出异常，具体的异常类型取决于错误的性质。
        """

        for item, val in self:
            pass
        return True

    def add(self, key, value):
        """
        该函数主要用于向文件中添加数据，并且将数据存储位置及长度的信息存储到索引字典中。
        
        参数:
        
        - key: 待添加数据的关键字，用于数据的检索。
        - value: 实际需要存储的数据。
        
        返回值:
        
        - act_len: 实际存储数据的长度。
        
        使用方法:
        
        首先，函数创建一个BytesIO缓存对象，并使用pickle将待存储的数据序列化后存储到缓存对象中。接着，函数计算出序列化数据的实际长度，并将缓存对象的指针重新设置到初始位置。
        然后，函数调整文件对象的指针到下一次写入位置，并将序列化后的数据写入到文件中。函数将数据的存储位置和长度作为值，关键字作为键，添加到索引字典中。最后，函数将文件对象的指针位置设置为文件的当前位置，并返回实际存储数据的长度。
        """

        with io.BytesIO() as temf:
            pickle.dump(value, temf)
            act_len = temf.tell()
            temf.seek(0)
            self.file_obj.seek(self.write_next_loc)
            self.file_obj.write(temf.read(act_len))
            self.index_dict[key] = (self.write_next_loc, act_len)
            self.write_next_loc = self.file_obj.tell()

        return act_len

    def get(self, key):
        """
        这是一个用于从文件中获取值的函数。
        
        对于给定的键，该函数首先检查键是否存在于索引字典中。如果键不存在，函数将返回None。如果键存在，它将找到与该键关联的值在文件中的位置和长度，然后在该位置读取长度为len的数据，并将数据加载回Python对象，然后返回。
        
        函数参数:
          key : 需要获取的数据的键。
        
        返回类型:
          函数返回与键关联的数据值。如果键不存在，则返回None。
        
        注意：如果键不存在于索引中，函数将返回None。此外，函数假设存在键的值可以成功的被pickle模块加载回Python对象，如果不能加载，函数可能会抛出异常。
        """

        if key not in self.index_dict:
            return None
        loc, len = self.index_dict[key]
        with io.BytesIO() as bf:
            self.file_obj.seek(loc)
            bf.write(self.file_obj.read(len))
            bf.seek(0)
            return pickle.load(bf)

    def flush(self):
        """
        这个函数是`chunk_file` 类的一个成员方法。该方法的主要作用是将当前对象的状态持久化到磁盘中。具体实现是，先刷新已打开文件对象的IO缓冲区，然后将索引字典`index_dict`保存到`.key`文件中。
        
        函数没有输入参数，也没有返回值。
        
        示例：
        ```python
        cf = chunk_file("/path/to/chunkfile")
        cf.add("key", "value")
        cf.flush()  # 此时，磁盘上的`/path/to/chunkfile.key`文件中保存了索引字典
        ```
        
        注意，调用该函数后，如果不再对`chunk_file`对象进行修改，那么就可以安全的关闭Python进程，不会丢失已添加到`chunk_file`对象中的数据。
        """

        self.file_obj.flush()
        with open(self.key_file_path, 'wb') as ff:
            pickle.dump(self.index_dict, ff)
