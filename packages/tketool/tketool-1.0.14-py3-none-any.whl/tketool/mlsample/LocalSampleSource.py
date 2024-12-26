import time

from tketool.mlsample.NLSampleSource import NLSampleSourceBase
from tketool.files import create_folder_if_not_exists
import os, io, pickle, shutil
import datetime


class LocalDisk_NLSampleSource(NLSampleSourceBase):
    """
    这个类是用来从本地磁盘加载和存储样本的一个工具类，它实现了NLSampleSourceBase接口。主要功能包括从本地磁盘获取样本数据、向本地磁盘写入样本数据、获取样本的元数据等。
    
    类的主要成员变量如下：
    - base_folder: 存储样本的基础文件夹路径
    - int_size和shortint_size: 整数和短整数的字节大小
    - pointer_size: 指针的字节大小
    - header_node_size和file_size: 头节点和文件的大小
    - file_pool: 存储打开的文件对象的字典，key为文件名，value为文件对象
    - base_seek_dic和linked_seek_dic: 存储基础头部和链接头部的字典
    
    主要方法如下：
    - __init__: 初始化一个LocalDisk_NLSampleSource实例
    - get_dir_list: 获取本地磁盘上存储样本的所有目录列表
    - get_file_date: 获取指定文件的日期
    - _try_get_file_obj: 尝试获得指定文件对象，如果不存在则会创建
    - __del__: 在删除对象时，关闭所有打开的文件
    - flush: 刷新文件缓冲区，保证所有的写操作都被写入磁盘
    - load_pointer_data: 加载指定的指针数据
    - create_new_set: 创建新的样本集
    - has_set: 判断是否存在指定的样本集
    - add_row: 向指定的样本集中添加一行数据
    - iter_data: 从指定的样本集中迭代读取数据
    - read_one_row: 从指定的样本集中读取一行数据
    - iter_pointer: 从指定的样本集中迭代读取指针数据
    - get_set_count: 获取指定样本集的样本数
    - get_metadata_keys: 获取指定样本集的元数据键值
    - print_set_info: 打印指定样本集的信息
    - delete_set: 删除指定的样本集
    - add_attachment: 向指定的样本集中添加附件
    - read_attachment: 读取指定样本集的附件信息
    
    示例：
    ```python
    ld_nls = LocalDisk_NLSampleSource("samples")
    ld_nls.create_new_set("set1", "description of set1", ["tag1", "tag2"], ["key1", "key2"])
    ld_nls.add_row("set1", ["data1", "data2"])
    for data in ld_nls.iter_data("set1"):
        print(data)
    ```
    """

    def get_dir_list(self) -> {}:
        """
        这个函数的主要目的是获取指定目录下的所有子目录信息。
        
        参数:
            self: 指代类实例的自身引用。
        
        返回:
            sets_infos: 返回一个字典，字典的key是子目录名，value是包含该子目录的相关信息的字典，包括'meta'、'count'、'filecount' 和 'create_date'等字段。
        
        异常:
            如果在执行过程中遇到错误，函数会抛出相应的异常。
        
        使用示例:
            假设我们有一个LocalDisk_NLSampleSource类的实例`ldnss`，我们可以这样使用这个函数：
            ```python
            dir_info = ldnss.get_dir_list()
            ```
            这样就可以得到`ldnss`实例的基础目录下的所有子目录信息。
        """

        sets = [file for file in os.listdir(self.base_folder) if not file.startswith('.')]
        sets_infos = {}
        for p_set in sets:
            base_f = self._try_get_file_obj(p_set)
            file_index, append_seek, data_start_seek, count, filecount, current_count, create_date, modify_data = self._read_base_header(
                base_f, True)
            node = self._read_node(base_f)
            sets_infos[p_set] = {
                'meta': node,
                'count': count,
                'filecount': filecount,
                'create_date': create_date,
                'modify_data': modify_data

            }
        return sets_infos

    def __init__(self, folder_path):
        """
        这是`LocalDisk_NLSampleSource`类的初始化函数，负责初始化该类的一些基本参数。
        
        参数:
            folder_path: 一个字符串，表示基础文件夹的路径。
        
        该类主要负责操作本地文件夹中的数据，包括获取文件夹列表，获取文件的创建日期，读取和写入数据等操作。在初始化过程中，会对基本参数进行赋值，并确保基础文件夹存在。
        
        示例:
        
            数据源 = LocalDisk_NLSampleSource("/path/to/folder")
            # 之后我们可以进行一些数据操作，例如获取文件夹列表：
            dir_list = 数据源.get_dir_list()
        
        注意事项:
            如果提供的基础文件夹路径不存在，则会抛出异常。请确保提供一个存在的文件夹路径。
        
        返回值: 无
        
        错误/异常:
            如果基础文件夹不存在，则会抛出异常。
        """

        self.base_folder = folder_path
        self.int_size = 8
        self.shortint_size = 4
        self.pointer_size = self.int_size + self.shortint_size
        self.header_node_size = 5 * 1024
        self.file_size = 1024 * 1024 * 100
        self.start_seek = self.int_size * 30 + self.pointer_size * 10 + self.header_node_size
        self.file_pool = {}

        self.base_seek_dic = {
            'version': 0,  # short
            'file_index': self.shortint_size,  # int
            'append_seek': self.int_size + self.shortint_size,  # pointer
            'data_start_seek': self.int_size + self.pointer_size + self.shortint_size,  # int ,
            'data_count': self.int_size * 2 + self.pointer_size + self.shortint_size,
            'file_count': self.int_size * 3 + self.pointer_size + self.shortint_size,
            'current_file_count': self.int_size * 4 + self.pointer_size + self.shortint_size,
            'create_time': self.int_size * 5 + self.pointer_size + self.shortint_size,
            'modify_time': self.int_size * 6 + self.pointer_size + self.shortint_size,
            'node': self.int_size * 7 + self.pointer_size + self.shortint_size
        }

        self.linked_seek_dic = {
            'file_index': 0,
            'current_file_count': self.int_size,
            'data_start_seek': self.int_size * 2,
        }

        create_folder_if_not_exists(self.base_folder)

    def get_file_date(self, name: str):
        """
        该函数用于获取本地磁盘上的指定文件的最后修改日期。
        
        参数：
            name (str)：文件名（不含扩展名）。函数将在类创建时设定的基础文件夹路径下寻找该文件。
        
        返回：
            datetime：返回一个datetime对象，表示该文件的最后修改日期。如果文件不存在，将抛出异常。
        
        使用方法：
            get_file_date("example_filename")
        会返回名为"example_filename.dlib"文件的最后修改日期。
        
        注意：
            1. 文件名应不包含扩展名，扩展名会在函数内部自动添加。
            2. 在文件系统支持的情况下，函数会返回文件的最后修改日期，而非创建日期。
        """

        path = os.path.join(self.base_folder, name, f"{name}.dlib")
        timestamp = os.path.getmtime(path)
        return datetime.datetime.fromtimestamp(timestamp)

    def _try_get_file_obj(self, name: str, file_index=0):
        """
        这个函数是尝试获取文件对象的方法，主要用于在文件池中查找指定的文件并返回其文件对象。如果文件池中不存在该文件，那么会打开这个文件并将它添加到文件池中。
        
        参数:
            name (str): 指定的文件名。
            file_index (int): 文件索引，默认值为0。
        
        返回:
            返回指定文件的文件对象。
        
        示例:
            这个函数的使用示例如下，主要在类的其他方法中被调用。
            ```
            def some_function(self, name: str):
                file_obj = self._try_get_file_obj(name)
                # 这里可以进行后续的操作，比如读取文件内容等。
            ```
        
        注意:
            1. 这个函数无法处理文件打开失败的情况，如果文件不存在或者无法访问，会抛出异常。
            2. 这个函数不负责关闭文件，需要在调用者中显式地关闭文件。
        """

        set_name = name
        if file_index != 0:
            name = f"{name}__{file_index}"
        if name not in self.file_pool:
            self.file_pool[name] = open(os.path.join(self.base_folder, set_name, f"{name}.dlib"), 'rb+')

        return self.file_pool[name]

    def __del__(self):
        """
        这是一个析构函数，用于当该对象不再被使用或调用时，清理并释放资源。在这个函数中，我们遍历文件池中的所有文件名，并关闭对应的文件。
        
        该函数没有参数和返回值。
        
        注意：在Python中，析构函数的执行不是确定的，也就是说我们无法准确预知何时析构函数会被调用。因此，尽量避免在析构函数中执行关键任务，而应在程序的控制流中明确地执行这些任务。
        
        示例：
        
        ```python
        class LocalDisk_NLSampleSource(NLSampleSourceBase):
            ...
            def __del__(self):
                for name in self.file_pool.keys():
                    self.file_pool[name].close()
            ...
        ```
        
        在上面的例子中，我们在 `__del__` 函数中关闭所有打开的文件。当对象不再被使用时，Python的垃圾回收器将会调用该函数，释放所占用的资源。
        """

        for name in self.file_pool.keys():
            self.file_pool[name].close()

    def flush(self):
        """
            刷新缓冲区。
        
            这个函数遍历文件池中的所有文件，对每个文件执行刷新操作，将缓冲区中的内容写入到文件中。这对于确保数据的一致性和完整性非常重要，特别是在长时间运行、大量输入/输出操作的程序中。
        
            注意：此函数不带任何参数，也没有返回值。
        
            如果在刷新操作中遇到任何错误或异常，它将由 Python 的内置 IOError 异常来处理。
        
            使用示例：
        
            disk = LocalDisk_NLSampleSource('/path/to/directory')
            # ... 执行一些文件操作
            disk.flush()  # 确保所有更改都已写入到文件中
        """

        for name in self.file_pool.keys():
            self.file_pool[name].flush()

    def _read_int(self, f) -> int:
        """
        这个函数是从一个文件中读取一个整数。
        
        参数:
            f: 一个文件对象。这个文件对象应该已经打开，并且设置为二进制模式。
        
        返回:
            返回一个整数。这个整数是从文件中读取的，转换成大端字节序，然后转换成无符号整数。
        
        例子:
            file_obj = open('path_to_file', 'rb')
            num = _read_int(file_obj)
            print(num)  # 打印出文件中读取的整数
        
        注意:
            这个函数没有做任何的错误处理。如果文件中没有足够的字节来读取一个整数，或者文件没有打开，或者文件不在正确的位置，这个函数可能会抛出异常。
        """

        return int.from_bytes(f.read(self.int_size), "big", signed=False)

    def _write_int(self, f, int_value: int):
        """
        该方法用于将整数值写入文件。
        
        参数:
            f (file): 需要写入的文件对象
            int_value (int): 需要写入的整数值
        
        返回类型: 无
        
        示例:
            _write_int(file_obj, 100)
        
        注意:
            在使用此函数时,确保文件对象已正确打开并且处于正确的位置,否则可能会覆盖原有的数据.
        """

        f.write(int_value.to_bytes(self.int_size, "big", signed=False))

    def _add_int_plusone(self, f, seekp):
        """
        这个函数是用于在指定位置将整数值加一。
        
        参数:
            f: 文件对象, 需要进行读写操作的文件对象。
            seekp: int, 指定的文件位置。
        
        返回:
            这个函数没有返回值。
        
        使用例子:
            假设我们有一个文件对象f，我们希望在文件的第10个字节的位置加1，我们可以这样使用这个函数：
            _add_int_plusone(f, 10)
        """

        f.seek(seekp)
        v = self._read_int(f)
        v += 1
        f.seek(seekp)
        self._write_int(f, v)

    def _read_shortint(self, f) -> int:
        """
        此函数是用于从给定的文件对象中读取一个大小为shortint_size的整数，并返回该整数。
        
        参数:
            f: 文件对象，已经打开并可以读取。
        
        返回:
            返回从文件对象读取的整数。
        
        示例:
            f = open('test_file', 'rb')
            value = _read_shortint(f)
            print(value)
        """

        return int.from_bytes(f.read(self.shortint_size), "big", signed=False)

    def _write_shortint(self, f, int_value: int):
        """
        这是一个Python函数，用于将整数值写入到文件中。
        
        参数:
            f: 文件句柄，文件必须以二进制写入模式打开
            int_value: 需要写入的整数值
        
        返回:
            无返回值
        
        使用示例:
        
            with open("testfile", 'wb') as f:
                _write_shortint(f, 10)
        
        注意：
        - 这个函数不会关闭文件，因此需要在调用它后手动关闭文件。
        - 该函数使用big-endian字节顺序以无符号整数格式写入数据，这点需要注意与读取时的字节顺序保持一致。
        """

        f.write(int_value.to_bytes(self.shortint_size, "big", signed=False))

    def _read_pointer(self, f) -> (int, int):
        """
            此函数用于从文件中读取一个“指针”。在这个上下文中，一个“指针”是一个由两部分组成的元组，其中包括一个页码和一个起始位置。这个函数首先读取一个短整数，然后读取一个普通的整数。
        
            参数:
            f -- 一个打开的文件或者类文件对象。
        
            返回:
            一个元组，第一个元素是页码，第二个元素是起始位置。
        """

        p = self._read_shortint(f)
        s = self._read_int(f)
        return (p, s)

    def _write_pointer(self, f, page: int, seek: int):
        """
            此函数是向指定的文件对象中写入指针信息，包括页码和偏移量。
        
            Args:
                f: 需要写入的文件对象，必须是已打开且可以读写的文件对象。
                page (int): 需要写入的页码信息，用于标识数据在文件中的位置。
                seek (int): 需要写入的偏移量信息，用于标识数据在文件中的位置。
        
            Returns:
                无返回值。
        
            Raises:
                无特定异常，但如果文件对象无法写入或者参数类型不正确，会抛出异常。
        
            Example:
                # 打开一个文件，然后向其中写入页码和偏移量
                with open('test.dlib', 'wb') as f:
                    _write_pointer(f, 5, 1024)
        
            注意：
                此函数不会自动关掉文件对象，需要在外部手动关闭。
        """

        self._write_shortint(f, page)
        self._write_int(f, seek)

    def _read_node(self, f):
        """
        此函数用于从文件流中读取并返回一个序列化的对象。
        
        参数:
            f: 文件流对象。
        
        返回:
            返回从文件流中读取的已反序列化的对象。
        
        使用示例:
        ```python
        with open('filename', 'rb') as f:
            obj = _read_node(f)
        ```
        
        注意:
            - 文件流对象f必须已经打开并可读。
            - 在文件流中的当前位置应该是序列化对象的开始位置。函数会从当前位置开始读取，而不是从文件的开头或结尾。
            - 此函数使用pickle模块进行反序列化，因此文件流中的数据必须是使用pickle序列化的。
        """

        f_len = self._read_int(f)
        act_len = self._read_int(f)
        with io.BytesIO() as bf:
            bf.write(f.read(act_len))
            bf.seek(0)
            return pickle.load(bf)

    def _seek_to_node(self, f):
        """
        这个函数的目的是读取一个文件的节点位置。函数首先保存当前的文件指针位置，然后读取该位置的两个整数值，分别是节点的长度和数据的实际长度。最后，函数将文件指针移动到实际数据的末尾，并返回原始的文件指针位置。
        
        参数列表:
            f: 文件对象。用于读取和定位节点。
        
        返回类型:
            int，返回的是文件对象的指针位置。
        
        使用方法:
            假设我们有一个文件对象f，我们可以这样调用此函数：
            ```
            location = _seek_to_node(f)
            ```
            这将返回指针位置，然后我们可以在其他函数中使用这个位置来读取或写入数据到文件对象f。
        
        注意：
            此函数假定文件对象f已经被打开了，并且可以读取。如果文件不可读或者没有打开，则使用此函数将会出错。此外，此函数会改变文件指针的位置，因此在使用后应当小心保存和恢复原始的文件指针位置。
        """

        o_loc = f.tell()
        f_len = self._read_int(f)
        act_len = self._read_int(f)
        c_loc = f.tell()
        f.seek(c_loc + act_len)
        return o_loc

    def _write_node(self, f, node, size=None):
        """
            该函数的主要目的是将给定的节点数据(node)写入到指定的文件对象中(f)。数据的最大尺寸可以通过可选的size参数进行设置。
        
            参数:
            - f: 要写入的文件对象，通常是一个已经打开的文件或者类文件的对象。
            - node: 要写入的节点数据，数据类型并未特定，可以是任意Python对象，这个对象会被pickle序列化存储。
            - size: 可选参数，用于设置要写入的数据的最大尺寸，单位为字节。如果Node的序列化后的长度超过此值，将会抛出异常。如果不设置此参数则不会对数据大小进行限制。
        
            返回值:
            - 无。此函数没有返回值，但是会直接改变传入的文件对象，写入的数据将保存在文件的当前位置。
        
            例子:
            ```
            f = open('test.dat', 'wb')
            node = {'name': 'test', 'value': 123}
            _write_node(f, node, size=1024)
            f.close()
            ```
            这个例子中，创建了一个新的文件对象f，指向文件'test.dat'，然后创建了一个字典作为节点数据，最后调用_write_node函数将节点数据写入到文件中，设置了最大的数据大小为1024字节。
        
            注意事项:
            - 请确保在使用完文件后正确地关闭了它，以防止数据丢失或者文件被意外地修改。
            - 此函数没有做任何关于文件权限或者文件存在性的检查，所有这些都需要在调用此函数前完成。
            - 传入的node数据需要能够被pickle模块正确地序列化和反序列化，否则在读取数据时可能会出现问题。
        """

        with io.BytesIO() as bf:
            pickle.dump(node, bf)
            act_len = bf.tell()
            if size and act_len > size:
                raise Exception("超过Node限制")
            f_len = act_len if size is None else size
            bf.seek(0)
            self._write_int(f, f_len)
            self._write_int(f, act_len)
            f.write(bf.read(act_len))

    def _read_base_header(self, f, return_time=False):
        """
        _read_base_header方法用于读取文件的基本头.
        
        参数:
            f: 文件对象, 已打开的文件对象，该文件对象需要有可读权限并且已经打开.
        
        返回:
            该函数返回一个包含六个元素的元组，元素分别为file_index, append_seek, data_start_seek, count, filecount, current_count.
        
            其中，
        
            file_index: 文件索引，为int类型，
            append_seek: 从文件开始处到当前位置的偏移量，为元组类型，包括页码和偏移量，
            data_start_seek: 从文件开始处到数据开始的偏移量，为int类型，
            count: 数据数量，为int类型，
            filecount: 文件数量，为int类型，
            current_file_count: 当前文件数量，为int类型。
        
        使用方法:
        
            file_obj = open('sample_file', 'r')
            base_header = _read_base_header(file_obj)
            print('Base Header:', base_header)
            file_obj.close()
        
        注意:
            对于无法打开或者读取的文件，该函数可能会抛出异常.
        """

        f.seek(0)

        version = self._read_shortint(f)
        file_index = self._read_int(f)
        append_seek = self._read_pointer(f)
        data_start_seek = self._read_int(f)
        count = self._read_int(f)
        file_count = self._read_int(f)
        current_file_count = self._read_int(f)

        create_time = self._read_int(f)
        modify_time = self._read_int(f)

        # node = self._read_node(f)
        if return_time:
            return file_index, append_seek, data_start_seek, count, file_count, current_file_count, create_time, modify_time
        else:
            return file_index, append_seek, data_start_seek, count, file_count, current_file_count

    def _read_linked_header(self, f):
        """
                此函数用于读取并返回链接头数据。
        
                参数:
                    f (file): 一个已打开的文件对象，该对象用于读取文件操作。
        
                返回:
                    返回一个元组，其中包含三个整型数据，分别为文件索引、当前计数和数据开始检索位置。
        
                示例:
                    file_index, current_count, data_start_seek = self._read_linked_header(file)
        
                注意:
                    传入的文件对象应处于读取状态，并且文件的内容应符合链接头数据的预期格式，否则可能会引发异常或错误。
        """

        f.seek(0)
        file_index = self._read_int(f)
        current_count = self._read_int(f)
        data_start_seek = self._read_int(f)

        return file_index, current_count, data_start_seek

    def load_pointer_data(self, name: str, pointer):
        """
                根据提供的数据集名称和指针，从基本文件读取并返回所需的数据。
        
                参数:
                name: str, 数据集的名称，该数据集应该存在于本地磁盘中。
                pointer: tuple, 包含文件索引和开始搜索的位置的元组。
        
                返回:
                返回从指定位置读取的数据。
        
                举例:
                假设我们有一个名为'test'的数据集，并且我们想要从该数据集的第一行中读取数据，则可以这样做:
                data = load_pointer_data('test', (0,0))
                这将返回'test'数据集的第一行数据。
        
                注意:
                如果数据集不存在或者指针指向的位置没有数据，那么这个函数会引发异常。
                """

        file_index, start_seek_location = pointer
        c_f = self._try_get_file_obj(name, file_index)
        c_f.seek(start_seek_location)
        return self._read_node(c_f)

    def _get_current_timestamp(self):
        return int(round(time.time() * 1000))

    def create_new_set(self, name: str, description: str, tags: [str], keys: [str],
                       base_set="", creator="") -> bool:
        """
        创建一个新的数据集
        
        这个方法用于创建一个新的数据集，包含数据集名称、描述、标签和关键字等信息，并在本地磁盘上创建相关文件以存储数据。
        
        参数:
            name : str
                新数据集的名称，同时也会作为数据集所在文件夹的名称.
            description : str
                数据集的描述信息，可以包含数据集的用途、来源等信息.
            tags : list of str
                数据集的标签，可以用来分类和搜索数据集.
            keys : list of str
                数据集中每条数据的关键字，对应数据的多个字段, 表示每条数据的结构.
        
        返回:
            bool
            如果数据集创建成功，返回True. 如果数据集已经存在，会抛出异常，不会返回False.
        
        例子:
            source = LocalDisk_NLSampleSource('/path/to/dataset')
            source.create_new_set('my_dataset', 'This is a dataset for testing.', ['test', 'sample'], ['field1', 'field2'])
            # 这将在/path/to/dataset/my_dataset下创建相关的文件，以存储数据集信息和数据.
        
        注意:
            - 数据集名称中不能包含下划线('_')，否则会抛出异常.
            - 如果数据集已经存在，再次调用这个方法会抛出异常.
        """

        # if '_' in name:
        #     log_error("set名中不能包含符号 '_' ")

        # if base_set != "":
        #     name = f"{base_set}_{name}"

        os.mkdir(os.path.join(self.base_folder, name))
        with open(os.path.join(self.base_folder, name, f"{name}.dlib"), 'wb') as f:
            header = {
                'name': name,
                'des': description,
                'tags': tags,
                'label_keys': keys,
                'base_set': base_set,
                'base_set_process': "",
                'creator': creator
            }

            self._write_shortint(f, 1)  # version

            self._write_int(f, 0)  # file_index
            self._write_pointer(f, 0, self.start_seek)  # append_seek
            self._write_int(f, self.start_seek)  # data_start_seek
            self._write_int(f, 0)  # data_count
            self._write_int(f, 1)  # file_count
            self._write_int(f, 0)  # current_file_count

            self._write_int(f, self._get_current_timestamp())  # create_time
            self._write_int(f, self._get_current_timestamp())  # modify time

            self._write_node(f, header, self.header_node_size)

        return True

    def has_set(self, name: str) -> bool:
        """
        此函数是用来检查是否存在某个set的。set是数据的集合，每个set中包含许多行数据，每行数据可以是一组标签和数据。
        
        Args:
            name: str, 待检查的set的名称。
        
        Returns:
            bool类型。如果存在该set，返回True; 否则，返回False。
        
        Examples:
            检查一个名为'sample_set'的set是否存在：
        
            ```python
            disk = LocalDisk_NLSampleSource(folder_path)
            if disk.has_set('sample_set'):
                print("The set 'sample_set' exists.")
            else:
                print("The set 'sample_set' does not exist.")
            ```
        
        注意：此函数不会对不存在的路径或无效的set名称做错误处理。如果提供了不存在的路径或无效的set名称，可能会抛出异常。在使用此函数时，应确保提供的set名称是合法且存在的。
        
        """

        if os.path.exists(os.path.join(self.base_folder, name, f"{name}.dlib")):
            return True
        return False

    def add_row(self, name: str, data: []) -> bool:
        """
        该函数为一个指定的set添加一行数据，这个set的名字由参数'name'指定。
        
        参数:
            name: str - 要添加数据的set的名字
            data: list - 要添加到set中的数据，应该是一个列表，列表的长度应该与set的元数据键的数量相同
        
        返回:
            bool - 如果数据添加成功，则返回True，否则返回False
        
        注意:
            - 如果data参数不是一个列表，函数会抛出一个异常
            - 如果data的长度与set的元数据键的数量不相同，函数会抛出一个异常
        """

        if not isinstance(data, list):
            raise Exception("数据格式错误")

        base_f = self._try_get_file_obj(name)
        file_index, append_seek, data_start_seek, count, filecount, current_count = self._read_base_header(base_f)

        meta_data_keys = self._read_node(base_f)['label_keys']
        assert len(data) == len(meta_data_keys)

        f = self._try_get_file_obj(name, append_seek[0])

        f.seek(append_seek[1])
        self._write_node(f, data)
        new_append_seek = f.tell()
        new_append_page = append_seek[0]

        if new_append_seek > self.file_size:
            new_append_page += 1
            with open(os.path.join(self.base_folder, name, f"{name}__{new_append_page}.dlib"), 'wb') as f_new:
                self._write_int(f_new, new_append_page)
                self._write_int(f_new, 0)
                self._write_int(f_new, 3 * self.int_size)
                new_append_seek = f_new.tell()
            self._add_int_plusone(base_f, self.base_seek_dic['file_count'])  # file_count

        base_f.seek(self.base_seek_dic['append_seek'])
        self._write_pointer(base_f, new_append_page, new_append_seek)  # append_seek
        self._add_int_plusone(base_f, self.base_seek_dic['data_count'])  # data_count
        base_f.seek(self.base_seek_dic['modify_time'])
        self._write_int(base_f, self._get_current_timestamp())

        # updata current file count
        if append_seek[0] == 0:
            self._add_int_plusone(f, self.base_seek_dic['current_file_count'])
        else:
            self._add_int_plusone(f, self.linked_seek_dic['current_file_count'])

        return True

    def iter_data(self, name: str):
        """
            此函数遍历并返回指定名称的数据集中的所有数据。
        
            参数:
                name (str): 数据集的名称。
        
            返回:
                生成器: 返回一个生成器,该生成器按顺序产生数据集中的每一行数据。
        
            使用示例:
                ```python
                ld = LocalDisk_NLSampleSource("my_folder_path")
                for data in ld.iter_data("my_dataset_name"):
                    print(data)
                ```
            注意:
                如果数据集不存在,此函数会引发异常。数据集的名称是大小写敏感的。
        
        """

        base_f = self._try_get_file_obj(name)
        file_index, append_seek, data_start_seek, count, filecount, current_count = self._read_base_header(base_f)

        for file_index in range(filecount):
            c_f = self._try_get_file_obj(name, file_index)
            if file_index == 0:
                c_f.seek(self.base_seek_dic['current_file_count'])
            else:
                c_f.seek(self.linked_seek_dic['current_file_count'])
            count = self._read_int(c_f)

            if file_index == 0:
                c_f.seek(self.base_seek_dic['data_start_seek'])
            else:
                c_f.seek(self.linked_seek_dic['data_start_seek'])
            start_seek_location = self._read_int(c_f)
            c_f.seek(start_seek_location)
            for f_count in range(count):
                yield self._read_node(c_f)

    def read_one_row(self, name: str):
        """
            def read_one_row(self, name: str):
                这是一个读取本地磁盘上特定文件（在此文件中，数据被存储为行）中的一行数据的方法。读取的行数据是以序列化形式存储的。
        
                参数:
                    name (str): 需要读取的文件的名字。
        
                返回:
                    返回一个被反序列化的数据对象，这个对象包含了在指定文件中的一行数据。
        
                使用示例:
                    ```python
                    disk_source = LocalDisk_NLSampleSource('path/to/folder')
                    row_data = disk_source.read_one_row('filename')
                    ```
        
                注意:
                    - 使用这个函数需要确保文件已经存在并且包含至少一行数据。
                    - 在使用这个函数读取数据前，数据应该已经被正确地序列化和保存到了文件中。
                    - 文件的存放位置应该在类初始化时设定的文件夹内。
        """

        base_f = self._try_get_file_obj(name)
        file_index, append_seek, data_start_seek, count, filecount, current_count = self._read_base_header(base_f)

        c_f = self._try_get_file_obj(name, 0)
        c_f.seek(self.base_seek_dic['current_file_count'])
        count = self._read_int(c_f)

        c_f.seek(self.base_seek_dic['data_start_seek'])

        start_seek_location = self._read_int(c_f)
        c_f.seek(start_seek_location)
        return self._read_node(c_f)

    def iter_pointer(self, name: str):
        """
        这个函数是在`LocalDisk_NLSampleSource`类中定义的，其主要作用是迭代返回给定名称的数据集的指针。指针包含文件索引和每个节点在文件中的位置。
        
        参数:
            name: str 类型，需要迭代的数据集的名称。
        
        返回:
            生成器，每次迭代返回一个包含文件索引和节点在文件中的位置的元组。
        
        举例:
        
        ```python
            source = LocalDisk_NLSampleSource(folder_path)
            for pointer in source.iter_pointer('dataset_name'):
                file_index, position = pointer
                print(f"文件索引: {file_index}, 位置: {position}")
        ```
        以上代码创建了一个`LocalDisk_NLSampleSource`对象，并使用`iter_pointer`函数迭代打印出'dataset_name' 数据集的每个节点指针的信息。
        
        注意: 这个函数不会检查给定的数据集名称是否存在，如果不存在，则会抛出异常。
        """

        base_f = self._try_get_file_obj(name)
        file_index, append_seek, data_start_seek, count, filecount, current_count = self._read_base_header(base_f)

        for file_index in range(filecount):
            c_f = self._try_get_file_obj(name, file_index)
            if file_index == 0:
                c_f.seek(self.base_seek_dic['current_file_count'])
            else:
                c_f.seek(self.linked_seek_dic['current_file_count'])
            count = self._read_int(c_f)

            if file_index == 0:
                c_f.seek(self.base_seek_dic['data_start_seek'])
            else:
                c_f.seek(self.linked_seek_dic['data_start_seek'])
            start_seek_location = self._read_int(c_f)
            c_f.seek(start_seek_location)
            for f_count in range(count):
                yield (file_index, self._seek_to_node(c_f))

    def get_set_count(self, name: str):
        """
            此函数用于获取指定名称的数据集的数据行数。
        
            参数:
            name: str，数据集的名称。
        
            返回:
            int，数据集的数据行数。
        
            示例:
            count = get_set_count('dataset_name')
        
            注意:
            如果提供的名称不存在于数据库中，该函数将引发异常。
        """

        base_f = self._try_get_file_obj(name)
        file_index, append_seek, data_start_seek, count, filecount, current_count = self._read_base_header(base_f)
        return count

    def get_metadata_keys(self, name: str) -> {}:
        """
        获取指定数据集的元数据键。
        
        参数:
            name (str): 要获取元数据键的数据集的名称。
        
        返回:
            dict: 返回元数据键的字典。
        
        示例:
        
        ```python
        disk = LocalDisk_NLSampleSource(folder_path)
        keys = disk.get_metadata_keys("my_dataset")
        print(keys)
        ```
        
        在这个示例中，我们首先创建一个LocalDisk_NLSampleSource对象，并指定一个文件夹路径。然后，我们调用get_metadata_keys方法，传入我们想要获取元数据键的数据集的名称。这将返回一个包含元数据键的字典。
        
        注意: 如果数据集名称不存在，这个函数将抛出一个异常。因此，需要确保数据集名称的有效性。
        """

        base_f = self._try_get_file_obj(name)
        file_index, append_seek, data_start_seek, count, filecount, current_count = self._read_base_header(base_f)
        return self._read_node(base_f)

    def print_set_info(self, name: str):
        """
        该函数用于打印指定名称的数据集信息。
        
        参数:
            name: str, 需要打印信息的数据集的名称。
        
        返回值:
            无
        
        使用方法:
            首先, 我们需要一个LocalDisk_NLSampleSource类的对象, 然后调用此对象的print_set_info方法来打印数据集的信息.
        
        例如:
            data_source = LocalDisk_NLSampleSource("/path/to/your/dataset")
            data_source.print_set_info('your_dataset_name')
        
        这个函数主要用于调试和检查数据集状态, 它会打印数据集的以下信息:
            - 文件索引
            - 追加的起始位置
            - 数据开始的位置
            - 数据的计数
            - 文件的计数
            - 文件的当前计数
        
        注意: 这个函数没有返回值, 它只是打印信息到控制台.
        
        这个函数没有已知的错误或者bug.
        """

        base_f = self._try_get_file_obj(name)
        v_count = 0
        file_index, append_seek, data_start_seek, count, filecount, current_count = self._read_base_header(base_f)
        print("*************************************************************** ")
        print(f"file_index(int):{file_index} \t append_seek:{append_seek[0]},{append_seek[1]} ")
        print(f"data_start_seek(int):{data_start_seek} \t count(int):{count} ")
        print(f"filecount(int):{filecount} \t current_count(int):{current_count} ")
        v_count += current_count
        # for index in range(1, filecount):
        #     cn_f = self._try_get_file_obj(name, index)
        #     file_index, current_count, start_append_seek = self._read_linked_header(cn_f)
        #     v_count += current_count
        #     print("———————————————————————————————————————————————————————————————— ")
        #     print(
        #         f"file_index(int):{file_index} \t current_count:{current_count},start_append_seek : {start_append_seek} ")
        if v_count != count:
            print(f'Count_ERROR:{count}->{v_count}')
        print("*************************************************************** ")

    def delete_set(self, name: str):
        """
        `delete_set` 方法是 `LocalDisk_NLSampleSource` 类的一个方法，用于删除具有指定名称的数据集。它首先关闭所有打开的文件对象，然后清空文件池，最后删除该数据集的文件夹。
        
        参数:
        
            name (str): 要删除的数据集的名称。
        
        返回值:
        
            此方法无返回值。
        
        示例:
        
            >>> source = LocalDisk_NLSampleSource(folder_path)
            >>> source.delete_set('my_dataset')
        
        注意:
        
            此方法不会检查数据集是否存在，如果尝试删除不存在的数据集，将会引发异常。在调用此方法前，应先使用 `has_set` 方法检查数据集是否存在。
        """

        for kname in self.file_pool.keys():
            self.file_pool[kname].close()
        self.file_pool = {}
        shutil.rmtree(os.path.join(self.base_folder, name))

    def modify_metadata(self, name, description=None, tags=None, base_set=None, base_set_process=None, creator=None):
        base_f = self._try_get_file_obj(name)

        base_f.seek(self.base_seek_dic['node'])
        meta_datas = self._read_node(base_f)

        if description:
            meta_datas['des'] = description
        if tags:
            meta_datas['tags'] = tags
        if base_set:
            meta_datas['base_set'] = base_set
        if base_set_process:
            meta_datas['base_set_process'] = base_set_process
        if creator:
            meta_datas['creator'] = creator

        base_f.seek(self.base_seek_dic['node'])

        self._write_node(base_f, meta_datas, self.header_node_size)

    def add_attachment(self, set_name: str, key, data):
        """
        该方法是向指定的数据集中添加附件。
        
        参数:
            set_name (str): 指定的数据集名称。
            key: 附件的关键字，用于检索数据。
            data: 要添加的数据。
        
        返回:
            无返回值。
        
        例子:
            ```python
            local_disk = LocalDisk_NLSampleSource('path_to_folder')
            local_disk.add_attachment('some_set', 'key1', 'some_data')
            ```
        
        注意:
            在使用此方法之前，需要确保数据集已经存在，否则会抛出异常。
        
        错误和bug:
            暂无已知错误或bug。
        """

        if not self.has_set(set_name):
            raise Exception("没有此set")

        attch_dict = {}

        attachment_file_path = os.path.join(self.base_folder, set_name, f"{set_name}.attch")
        attachment_key_file_path = os.path.join(self.base_folder, set_name, f"{set_name}_{key}.attch")

        with open(attachment_key_file_path, 'wb') as f:
            f.seek(0)
            self._write_node(f, {'key': key, 'data': data})

        if not os.path.exists(attachment_file_path):
            with open(attachment_file_path, 'wb') as f:
                attch_dict[key] = f"{set_name}_{key}.attch"
                self._write_node(f, attch_dict)
                # self._write_int(f, 0)
                # self._write_int(f, self.int_size * 2)
        else:
            with open(attachment_file_path, 'rb+') as f:
                attch_dict = self._read_node(f)
                attch_dict[key] = f"{set_name}_{key}.attch"
                f.seek(0)
                self._write_node(f, attch_dict)

    def read_attachment_keys(self, set_name: str):
        """
        这个函数是用于读取集合(或称为 set)的附件信息的。
        
        参数:
            set_name: str类型, 它是你想要读取附件的集合的名字。
        
        返回:
            返回一个列表，列表中包含集合的所有附件信息。
        
        用法:
            read_attachment('text_set')
        
        注意:
            如果集合不存在或者集合没有附件，会引发异常。
        """

        attachment_file_path = os.path.join(self.base_folder, set_name, f"{set_name}.attch")
        if not os.path.exists(attachment_file_path):
            return []
        else:
            with open(attachment_file_path, 'rb+') as f:
                attch_dict = self._read_node(f)

            return list(attch_dict.keys())

    def read_attachment(self, set_name: str, key: str):

        attch_dict = {}

        attachment_file_path = os.path.join(self.base_folder, set_name, f"{set_name}.attch")
        if not os.path.exists(attachment_file_path):
            return None
        else:
            with open(attachment_file_path, 'rb+') as f:
                attch_dict = self._read_node(f)

        if key not in attch_dict:
            return None

        else:
            attachment_key_file_path = os.path.join(self.base_folder, set_name, attch_dict[key])
            with open(attachment_key_file_path, 'rb') as f:
                data_dict_buffer=self._read_node(f)
                return data_dict_buffer['data']
    # attach_dic = []
    # with open(attachment_file_path, 'rb+') as f:
    #     count = self._read_int(f)
    #     start_loc = self._read_int(f)
    #     for _ in range(count):
    #         attach_dic.append(self._read_node(f))
    #
    # return attach_dic



