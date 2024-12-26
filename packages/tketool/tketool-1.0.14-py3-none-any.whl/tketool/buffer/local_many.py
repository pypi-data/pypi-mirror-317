# pass_generate
import pickle
import os
from tketool.JConfig import get_config_instance
import tketool.buffer.bufferbase as bb
from tketool.logs import log
from tketool.buffer.bufferbase import buffer


def get_path_for_key(key: str) -> str:
    """
    此函数用于获取给定键的路径。
    
    参数:
        key (str): 用于构建最终路径的键。
    
    返回:
        str: 返回由缓冲文件夹路径和给定键组成的路径。如果缓冲文件夹路径在配置中没有找到，默认将使用"buffer"作为缓冲文件夹路径。
    
    例子:
        >>> get_path_for_key('sample_key')
        '/path/to/buffer_folder/sample_key'
    
    注:
        此函数依赖于get_config_instance()方法来获取配置实例，并从中读取"buffer_folder"配置。如果该配置不存在，它会默认使用"buffer"。因此，确保在调用此函数之前，已经正确配置了get_config_instance()方法。
    """

    buffer_folder = get_config_instance().get_config("buffer_folder", "buffer")
    return os.path.join(buffer_folder, key)


def _load_buffer_file(key):
    """
    这是一个用于加载缓存文件的函数。
    
    参数:
        key: 键名，用于通过get_path_for_key函数获取文件路径。
    
    返回:
        返回经过pickle模块反序列化后的对象。
    
    注意:
        1. 函数使用二进制读取模式打开文件，所以这个函数只能用于读取二进制文件。
        2. 函数使用pickle模块进行反序列化，因此只能处理pickle模块可以反序列化的对象。
        3. 函数没有进行异常处理，如果文件不存在或者文件内容无法被pickle模块反序列化，函数会抛出异常。
    
    示例：
        # 假设有个以二进制方式存储的pickle文件'test.pkl'，其内容为{'hello': 'world'}
        # 首先，我们需要实现get_path_for_key函数，使其可以根据键名返回对应的文件路径
        def get_path_for_key(key):
            return key + '.pkl'
        # 然后，我们可以使用_load_buffer_file函数来读取这个文件
        print(_load_buffer_file('test'))  # 输出 {'hello': 'world'}
    """

    path = get_path_for_key(key)
    with open(path, 'rb') as f:
        return pickle.load(f)


def _save_buffer_file(lists):
    """
    这个函数的主要目的是将传入的列表数据进行持久化，将每一个键值对保存为一个独立的文件。
    
    这个函数没有返回值。
    
    参数:
        lists: 一个包含键值对的列表，列表中的每一项都是一个元组，元组的第一项是键，第二项是要保存的数据。
    
    特别注意，这个函数会将键值对中的键作为文件名，值作为文件内容，将数据保存在磁盘上。保存的路径由get_path_for_key函数确定，保存的方式是pickle序列化。
    
    如果文件的保存路径不存在，这个函数会先创建对应的文件夹，然后再进行数据的保存。
    
    这个函数使用pickle模块进行对象的序列化和反序列化。确保你传入的对象是可以被pickle模块处理的。
    
    使用案例：
    ```python
    buffer_lists = [('key1', data1), ('key2', data2), ...]
    _save_buffer_file(buffer_lists)
    ```
    在使用时，只需要将需要保存的数据以列表的形式传入即可。
    
    可能的错误：
    如果传入的键值对的键不能作为文件名，或者数据不能被pickle模块处理，那么这个函数可能会抛出异常。
    """

    folder = os.path.dirname(get_path_for_key(""))
    if not os.path.exists(folder):
        os.makedirs(folder)  # Ensure all necessary directories are created

    for key, item in lists:
        path = get_path_for_key(key)
        with open(path, 'wb') as f:
            pickle.dump(item, f)


def _delete_buffer_file(key):
    """
    该函数的目的是删除一个给定键对应的文件。函数首先通过键获取文件的路径，然后检查该路径是否存在。如果存在，函数将删除该路径的文件。
    
    参数:
        key: 一个字符串，用于获取要删除的文件的路径。
    
    返回值:
        该函数没有返回值。
    
    示例:
        假设有一个名为"sample"的文件，我们可以通过以下方式删除它：
        _delete_buffer_file("sample")
    
    注意:
        该函数不会检查键是否有效，也不会处理删除过程中可能出现的异常。因此，在调用此函数时，请确保输入的键是有效的，并且相关文件的读写权限已经被正确设置。
    """

    path = get_path_for_key(key)
    if os.path.exists(path):
        os.remove(path)


def _has_buffer_file(key):
    """
    这是一个检查缓存文件是否存在的函数。
    
    Args:
        key (str): 文件的关键字。
    
    Returns:
        bool: 如果文件存在返回True, 否则返回False。
    
    Example:
        >>> _has_buffer_file("example")
        True
    """

    return os.path.exists(get_path_for_key(key))


# Update bufferbase with the implemented functions
bb.has_buffer_file = _has_buffer_file
bb.load_buffer_file = _load_buffer_file
bb.delete_buffer_file = _delete_buffer_file
bb.save_buffer_file = _save_buffer_file
log("use local_many")