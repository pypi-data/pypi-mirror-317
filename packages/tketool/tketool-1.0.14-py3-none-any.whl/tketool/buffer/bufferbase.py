# pass_generate
from functools import wraps
from tketool.hash_util import hash_str, hash_obj_strbase
import threading

BUFFER_ITEMS = {}
BUFFER_OPER_QUEUE = []

has_buffer_file = None
load_buffer_file = None
delete_buffer_file = None
save_buffer_file = None

flush_freq = 10

buffer_lock = threading.Lock()


def flush():
    """
    该`flush`函数是用于把缓冲区的内容存储到文件中，然后清空缓冲区。
    
    这个函数没有参数和返回值，但在执行过程中，如果没有导入任何模块，会抛出异常。
    
    函数执行的步骤如下：
    1. 检查是否导入了任何模块，如果没有，抛出异常。
    2. 获取`buffer_lock`锁，保证同一时间只有一个线程可以执行这段代码。
    3. 从BUFFER_OPER_QUEUE队列中获取要保存的项目，队列中存储的是要保存的项目的key。
    4. 将要保存的项目以列表的形式传给`save_buffer_file`函数，该函数负责将项目存储到文件中。
    5. 最后清空BUFFER_OPER_QUEUE队列。
    
    注意：
    - `has_buffer_file`、`buffer_lock`、`BUFFER_OPER_QUEUE`和`BUFFER_ITEMS`都应该是事先定义好的全局变量。
    - `save_buffer_file`应该是一个可以将项目存储到文件中的函数。
    """

    if has_buffer_file is None:
        raise Exception("No module imported")

    with buffer_lock:
        queue_set = set(BUFFER_OPER_QUEUE)
        save_item_list = [(key, BUFFER_ITEMS[key]) for key in queue_set]
        save_buffer_file(save_item_list)

        # Clear the queue after flushing
        BUFFER_OPER_QUEUE.clear()


def set_flush_freq(count):
    """
    这是一个设置全局变量flush_freq的函数。它接收一个参数count，并将flush_freq设为count。
    
    参数:
        count: 任何可以赋值给flush_freq的值。
    
    返回:
        无返回值。
    
    注意: 这个函数会改变全局变量flush_freq的值。确保在调用此函数时了解这一点，以避免可能的问题。
    """

    global flush_freq
    flush_freq = count


def get_hash_key(func_name, *args, **kwargs):
    """
    这个函数用于生成一个基于函数名，参数(位置参数和关键词参数)的哈希键。
    
    参数:
    func_name (str): 函数名
    *args (tuple): 可变位置参数，可以接受任意数量的位置参数
    **kwargs (dict): 可变关键词参数，可以接受任意数量的关键词参数
    
    返回:
    hash_key (str): 返回一个字符串，该字符串以函数名作为前缀，并加上基于参数的哈希值。
    
    例如：
    
    假设我们有一个函数：def my_func(a, b, c=2, d=3):
    
    我们可以这样使用 get_hash_key 函数：
    
    hash_key = get_hash_key('my_func', 1, 2, c=3, d=4)
    
    这将返回一个字符串，比如 "my_func_7fe02"
    
    注意：这个函数依赖另外两个函数 hash_str 和 hash_obj_strbase 来生成哈希值，
    如果这两个函数不存在或者报错，那么这个函数也会报错。
    
    错误/异常:
    如果输入的 func_name 不是字符串，或者 *args 或 **kwargs 中的元素不能被 hash_obj_strbase 正确处理，那么这个函数可能会抛出异常。
    """

    key_buffer = [hash_str(func_name)]
    if args:
        key_buffer.append([hash_obj_strbase(arg) for arg in args])
    if kwargs:
        key_buffer.append([hash_obj_strbase(kwarg) for kwarg in kwargs.values()])
    return str(func_name) + "_" + hash_obj_strbase(key_buffer)


def buffer_item(key: str, value):
    """
    这个函数的作用是将一个键值对存放到缓冲区中。
    
    参数:
        key: str - 需要存放的键。
        value: 需要存放的值，可以为任何类型。
    
    这个函数没有返回值。
    
    在函数内部，首先会对给定的键执行一个哈希操作来得到一个新的键（nkey）。然后将给定的值存放到以nkey为键的缓冲区中。并且，将nkey添加到操作队列中。
    
    当操作队列的长度达到设定的刷新频率时，将调用flush()函数，将缓冲区的内容写入到磁盘中。
    
    注意：该函数是线程安全的，使用了锁来确保在修改缓冲区和操作队列时不会出现数据竞争。
    
    在调用这个函数时，需要确保给定的键是字符串类型，否则哈希操作可能会失败。
    
    示例：
        buffer_item('my_key', 'my_value')
    
    上述代码将把键为'my_key'，值为'my_value'的键值对存入缓冲区中。
    """

    with buffer_lock:
        nkey = get_hash_key(key)
        BUFFER_ITEMS[nkey] = value
        BUFFER_OPER_QUEUE.append(nkey)

        if len(BUFFER_OPER_QUEUE) >= flush_freq:
            flush()


def get_buffer_item(key: str):
    """
    此函数的作用是通过给定的键值，从缓存中获取对应的项目。如果在内存缓存中没有找到对应项目，它将尝试从缓存文件中加载。如果在文件中也没有找到，将抛出一个值错误。
    
    参数:
        key: str类型，输入的键值，用来在缓存中查找对应的项目。
    
    返回:
        返回对应键值的缓存项目。
    
    异常:
        如果没有导入任何模块，会抛出一个异常。
        如果没有找到对应键值的缓存项目，会抛出一个值错误。
    
    注意：
        此函数是线程安全的，可以在多线程环境下同时访问。
    
    示例：
        item = get_buffer_item('my_key')
        print(item)
    
    """

    if has_buffer_file is None:
        raise Exception("No module imported")

    nkey = get_hash_key(key)
    with buffer_lock:
        if nkey in BUFFER_ITEMS:
            return BUFFER_ITEMS[nkey]

        if has_buffer_file(nkey):
            BUFFER_ITEMS[nkey] = load_buffer_file(nkey)
            return BUFFER_ITEMS[nkey]

    raise ValueError(f"No buffer item found for key: {key}")


def has_item_key(key: str):
    """
    这是一个检查是否存在指定键(通过hash处理)的函数. 它首先确认是否导入了模块，然后获取参数key的hash值。 最后，它会检查这个hash值是否在BUFFER_ITEMS中，或者是否在buffer file中.
    
    参数:
        key (str): 要检查的键.
    
    返回:
        Boolean: 如果键存在于BUFFER_ITEMS或buffer file中，则返回True，否则返回False.
    
    异常:
        如果没有导入模块，将引发异常.
    """

    if has_buffer_file is None:
        raise Exception("No module imported")

    nkey = get_hash_key(key)

    return nkey in BUFFER_ITEMS or has_buffer_file(nkey)


def remove_item(key: str):
    """
    移除指定的缓存项。
    
    此函数用于从BUFFER_ITEMS中移除指定的缓存项。如果缓存项在缓冲文件中也存在，也将一并删除。
    
    Args:
        key (str): 要移除的缓存项的键。
    
    Raises:
        Exception: 如果没有导入模块，将抛出异常。
    
    注意:
        此函数需要配合其他函数使用，如get_hash_key, has_buffer_file, delete_buffer_file等。
    
    例如:
        remove_item('test_key')
    
    注意，如果没有提前导入必要的模块或准备好必要的配置，此函数可能会引发错误。
    """

    if has_buffer_file is None:
        raise Exception("No module imported")

    nkey = get_hash_key(key)

    with buffer_lock:
        if nkey in BUFFER_ITEMS:
            del BUFFER_ITEMS[nkey]
        if has_buffer_file(nkey):
            delete_buffer_file(nkey)


def buffer(version=1.0):
    """
    这是一个装饰器函数，用于缓存函数的运行结果。当函数的输入参数相同时，不会重复运行函数，而是直接返回缓存的结果，提高了程序的运行效率。
    
    参数:
        version (float): 缓存版本，默认为1.0。当函数逻辑发生改变，需要清除旧的缓存时，可以通过修改这个版本号来实现。
    
    返回:
        decorator (function): 返回一个装饰器，用于装饰其他函数。
    
    使用示例:
    ```python
        @buffer(version=2.0)
        def add(x, y):
            return x + y
    ```
    在此示例中，`add`函数被`buffer`装饰器装饰，当多次调用`add(1, 2)`时，实际上函数只运行了一次，其它次数直接返回了缓存的结果。
    
    注意:
    1. 该装饰器使用了全局的`BUFFER_ITEMS`字典进行缓存，如果使用的地方较多，可能会占用较多的内存。
    2. 缓存的键是通过函数名和参数生成的哈希值，如果函数名或参数的字符串表示发生改变，可能会产生冲突。
    """

    '''
    Decorator to cache the result of a function.

    :param version: Cache version.
    '''

    def decorator(func):
        """
            内部装饰器函数，用于应用缓存功能。
        
            这个函数定义了一个装饰器，它被用于缓存某个函数的结果。当相同的参数传递给该函数时，装饰器会检查缓存中是否有这个函数之前的运行结果。
            如果存在，并且版本号也匹配，那么装饰器会返回缓存中的结果，而不是再次运行函数。如果不存在或者版本号不匹配，那么函数将被
            执行，并且结果会被缓存起来。
        
            这个装饰器函数可以用于任何需要大量计算，并且希望避免重复计算的函数上，以提高程序的运行效率。
        
            :param func: 需要应用装饰器的函数。
            :return: 装饰后的函数。
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            global BUFFER_ITEMS
            nkey = get_hash_key(func.__name__, args, kwargs)
            if has_item_key(nkey):
                buffer_value = get_buffer_item(nkey)
                if buffer_value['version'] == version:
                    return buffer_value['value']

            func_result = func(*args, **kwargs)
            buffer_item(nkey, {'version': version, 'value': func_result})

            return func_result

        return wrapper

    return decorator
