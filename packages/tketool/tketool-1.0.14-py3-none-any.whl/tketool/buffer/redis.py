# pass_generate
import json
import redis
from tketool.JConfig import get_config_instance
import tketool.buffer.bufferbase as bb
from tketool.logs import log

# Global Redis connection pool
REDIS_CONNECTION_POOL = None
# Redis hash key for buffering
REDIS_BUFFER_KEY = "redis_buffer"


def _get_pool():
    """
    这个函数的目的是获取redis连接池对象。如果全局变量REDIS_CONNECTION_POOL为空，即当前没有redis连接池，那么这个函数会根据配置文件中的redis_host和redis_port创建一个新的redis连接池，并将其赋值给REDIS_CONNECTION_POOL。如果REDIS_CONNECTION_POOL已经有值，即已经存在redis连接池，那么直接返回这个redis连接池对象。
    
    这个函数没有参数。
    
    返回值是redis连接池对象。
    
    示例：
    调用这个函数：pool = _get_pool()
    然后你就可以用这个pool来创建redis连接对象：
    redis_conn = redis.Redis(connection_pool=pool)
    
    注意：
    1. 这个函数依赖于redis库，如果你没有安装这个库，那么会出错。你可以使用pip install redis来安装这个库。
    2. 这个函数也依赖于配置文件中的redis_host和redis_port，如果配置文件中没有这两个值，那么也会出错。
    """

    global REDIS_CONNECTION_POOL
    if REDIS_CONNECTION_POOL is None:
        config_obj = get_config_instance()
        REDIS_CONNECTION_POOL = redis.ConnectionPool(
            host=config_obj.get_config("redis_host"),
            port=int(config_obj.get_config("redis_port")),
            decode_responses=True
        )
    return REDIS_CONNECTION_POOL


def _load_buffer_file(key):
    """
    此函数用于从redis缓存中加载特定键的缓存文件。
    
    Args:
        key: 需要检索的缓存键。
    
    Returns:
        返回一个字典，该字典包含key对应的缓存数据。
    
    Raises:
        Exception: 如果给定的键在redis中不存在，则引发异常。
    
    该函数首先创建一个redis连接，并通过该连接查询给定键的存在性。
    如果键存在，则从redis中获取该键的值，并通过json.loads将其从字符串转换为字典格式。
    如果键不存在，则抛出一个异常，提示没有找到给定键的缓存项。
    
    例如：
    _load_buffer_file('example_key')
    这将加载与'example_key'对应的缓存数据，如果存在的话。
    
    注意：该函数依赖于redis的连接池和REDIS_BUFFER_KEY全局变量。确保在使用此函数之前初始化了这些值。
    
    此函数没有已知的bug。
    """

    rrdis = redis.Redis(connection_pool=_get_pool())

    if rrdis.hexists(REDIS_BUFFER_KEY, key):
        return json.loads(rrdis.hget(REDIS_BUFFER_KEY, key))

    raise Exception("Buffer item not found for the given key.")


def _save_buffer_file(lists):
    """
    将给定的键值对列表存储到Redis缓存中。
    
    这个函数会遍历输入的列表，其中每个元素应该是一个键值对。对于列表中的每个键值对，它将键作为字段名，将序列化后的值作为字段值，存储到预先定义好的Redis缓存中。
    
    参数：
    lists (list[tuple]): 需要存储的键值对列表。每个元素是一个包含两个元素的元组，第一个元素作为字段名，第二个元素作为字段值。
    
    返回类型：
    无
    
    使用示例：
    _save_buffer_file([('key1', 'value1'), ('key2', 'value2')])
    
    注意：
    - 在调用该函数前，确保Redis服务已经启动，并且全局变量REDIS_BUFFER_KEY已经被初始化。
    - 该函数并未处理可能出现的Redis连接错误，或者数据序列化错误。在实际使用中，可能需要在调用该函数的地方添加异常处理代码。
    """

    rrdis = redis.Redis(connection_pool=_get_pool())
    for key, value in lists:
        rrdis.hset(REDIS_BUFFER_KEY, key, json.dumps(value))


def _delete_buffer_file(key):
    """
    删除指定的缓冲文件。
    
    这个函数的目的是根据提供的键值删除在Redis中的缓冲文件。函数首先检查是否存在指定键值的缓冲文件，
    如果存在，则通过建立Redis连接，从Redis缓冲键中删除该键值的信息。
    
    Args:
        key: 需要被删除的缓冲文件的键值。
    
    Returns:
        无返回值。
    
    Raises:
        如果Redis连接错误或删除操作出错，可能会抛出异常。
    
    注意:
        在使用该函数前，请确保已经成功建立Redis连接，并且Redis中存在指定键值的缓冲文件。
    """

    if _has_buffer_file(key):
        rrdis = redis.Redis(connection_pool=_get_pool())
        rrdis.hdel(REDIS_BUFFER_KEY, key)


def _has_buffer_file(key):
    """
    此函数是检查Redis缓存中是否存在特定的buffer文件。
    
    参数:
        key: str类型，代表需要检查的buffer文件的key。
    
    返回:
        bool类型，如果Redis中存在该key对应的buffer文件，返回True，否则返回False。
    
    注意:
        此函数依赖于`_get_pool()`函数（未在此示例中提供），它应该返回一个Redis连接池。
        确保已经设置了全局变量REDIS_BUFFER_KEY，它应该是一个Redis的hash类型的key，其值是一个映射，其中包含了buffer文件的key和它们对应的值。
    
    示例:
    
        >>> _has_buffer_file('some_key')
        True
        >>> _has_buffer_file('non_existent_key')
        False
    """

    rrdis = redis.Redis(connection_pool=_get_pool())
    return rrdis.hexists(REDIS_BUFFER_KEY, key)


# Update bufferbase with the implemented functions
bb.has_buffer_file = _has_buffer_file
bb.load_buffer_file = _load_buffer_file
bb.delete_buffer_file = _delete_buffer_file
bb.save_buffer_file = _save_buffer_file
log("use redis")
