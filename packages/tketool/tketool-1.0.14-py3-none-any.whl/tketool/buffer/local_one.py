# pass_generate
import shelve
import os
from tketool.JConfig import get_config_instance
import tketool.buffer.bufferbase as bb
from tketool.logs import log

# Global variables should be in uppercase according to PEP8
BUFFER_FOLDER = get_config_instance().get_config("buffer_folder", "buffer")
BUFFER_FILE_PATH = os.path.join(os.getcwd(), BUFFER_FOLDER, "buffer.bin")


def init_shelve():
    """
    这是一个初始化Shelve数据库的函数，Shelve数据库是一种简单的键值对存储。
    
    函数首先检查存储Shelve文件的目录是否存在，如果不存在，则创建该目录。
    然后，打开Shelve文件，并返回一个对象。
    
    函数定义了四个内部函数：_load_buffer_file，_save_buffer_file，_delete_buffer_file和_has_buffer_file。
    这些函数分别用于加载、保存、删除Shelve数据库中的键值对，以及检查一个键是否在数据库中。
    
    此外，这四个内部函数也被赋值给了bb对象的四个属性，分别为：has_buffer_file，load_buffer_file，delete_buffer_file，save_buffer_file。
    这样做的目的是为了在函数外部也能调用这四个内部函数。
    
    函数最后返回了打开的Shelve对象。
    
    函数没有参数。
    
    返回值是一个Shelve对象。
    
    注意：
    1. 如果删除的键不存在，_delete_buffer_file函数将会抛出KeyError异常。
    2. 如果保存的键已经存在，_save_buffer_file函数将会覆盖原有的值。
    """

    if not os.path.exists(BUFFER_FOLDER):
        os.makedirs(BUFFER_FOLDER)

    shelve_obj = shelve.open(BUFFER_FILE_PATH)

    def _load_buffer_file(key):
        """
        这个函数是一个用于从shelve对象加载数据的函数。
        
        参数:
            key: 一个string类型的参数，代表文件的键值。
        
        返回:
            函数将返回与键值对应的数据。
        
        示例:
            _load_buffer_file('example_key')
        
        这个函数没有已知的错误或bug。
        """

        return shelve_obj.get(key)

    def _save_buffer_file(lists):
        """
        保存缓存文件
        
        本函数的主要目的是将提供的列表保存到缓存文件中。每个列表元素应为一个键值对，函数会将每一对键值对存入缓存文件中。
        
        参数:
            lists: list[tuple]，待保存的键值对列表，列表中的每个元素为一个元组，元组的第一项为键，第二项为值。
        
        返回:
            无返回值。
        
        示例:
        
        ```python
        _save_buffer_file([('key1', 'value1'), ('key2', 'value2')])
        ```
        
        注意：
        在函数结束后，会调用shelve_obj.sync()来确保所有的修改都被写入硬盘。
        
        错误或异常：
        若lists中的元素不是元组或元组长度不为2，则会抛出相应的错误。
        
        """

        for k, v in lists:
            shelve_obj[k] = v
        shelve_obj.sync()

    def _delete_buffer_file(key):
        """
        删除指定的键值对。
        
        这个函数主要是在shelve对象上进行操作，输入一个键，然后删除shelve对象中对应的键值对。并同步更新到磁盘。
        
        Args:
            key: 需要删除的键。
        
        Returns:
            无返回值。
        
        Raises:
            KeyError: 如果给定的键在shelve对象中不存在。
        
        例子:
        
            _delete_buffer_file('test_key')  # 删除键为'test_key'的键值对。
        """

        del shelve_obj[key]
        shelve_obj.sync()

    def _has_buffer_file(key):
        """
        这是一个检查给定的key是否存在于shelve对象中的函数。
        
        参数:
            key: 需要在shelve对象中查找的键。
        
        返回:
            返回一个布尔值，如果给定的键在shelve对象中存在，则返回True，否则返回False。
        
        示例:
        
            # 初始化shelve对象
            shelve_obj = init_shelve()
        
            # 检查指定的键是否在shelve对象中
            if shelve_obj._has_buffer_file('my_key'):
                print("键存在")
            else:
                print("键不存在")
        
        注意:
            本函数在查找键时，会遍历shelve对象的所有键，可能会有一定的性能消耗，因此在键的数量较多时慎用。
        """

        lllm = [kk for kk in shelve_obj.keys()]
        return key in shelve_obj

    bb.has_buffer_file = _has_buffer_file
    bb.load_buffer_file = _load_buffer_file
    bb.delete_buffer_file = _delete_buffer_file
    bb.save_buffer_file = _save_buffer_file

    return shelve_obj


# Initialize the shelve object and store it in a global variable
SHELVE_OBJ = init_shelve()
log("use local_one")


def close_shelve():
    """
    关闭shelve对象的函数。
    
    这个函数会检查全局的SHELVE_OBJ对象是否存在，如果存在，就会关闭这个对象，并将其设置为None。这个函数主要用于确保shelve对象在不需要的时候被正确关闭，避免占用资源或者导致数据不一致的问题。
    
    函数没有参数，也没有返回值。
    
    示例：
    ```python
    close_shelve()
    ```
    注意：这个函数依赖于全局变量SHELVE_OBJ，所以在使用之前需要确保SHELVE_OBJ已经被正确初始化。另外，如果已经关闭了SHELVE_OBJ，再次调用这个函数会导致错误。
    
    待解决的问题：目前这个函数没有处理可能的异常，比如在关闭SHELVE_OBJ的时候可能会出现的IO错误。
    """

    global SHELVE_OBJ
    if SHELVE_OBJ:
        SHELVE_OBJ.close()
        SHELVE_OBJ = None
