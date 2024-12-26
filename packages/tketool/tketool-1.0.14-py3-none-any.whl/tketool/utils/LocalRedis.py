# pass_generate
import sqlite3
from tketool.JConfig import *
import os, threading

db = None
connect_pool = {}


def _load():
    # version 1.2
    """
    这是一个名为"_load"的私有函数，用于从配置中获取一个数据库连接对象。
    
    此函数首先获取当前线程的ID，然后在连接池中查找是否存在与该ID相关的连接。如果存在，则返回这个连接；如果不存在，它将创建一个新的连接到指定的SQLite数据库，并在该数据库中创建一个名为state的表（如果该表还不存在的话）。
    
    在创建表时，该函数定义了两个字段：一个是主键字段key，它的类型是TEXT；另一个是名为value的BLOB字段。创建完表之后，将新建的连接添加到连接池中，并返回该连接。
    
    函数的返回值是一个SQLite数据库的连接对象。
    
    Args:
        无
    
    Returns:
        sqlite3.Connection: SQLite数据库的连接对象
    
    注意：此函数没有错误处理机制，如果在连接数据库或者执行SQL语句的过程中发生错误，将会抛出异常。
    """
    

    global db, connect_pool

    curr_thread_id = threading.get_ident()
    if curr_thread_id not in connect_pool:
        path = get_config_instance().get_config("state_file_path", "state.sqlite")
        connect_pool[curr_thread_id] = sqlite3.connect(path)
        connect_pool[curr_thread_id].execute("""
                    CREATE TABLE IF NOT EXISTS state (
                        key TEXT NOT NULL PRIMARY KEY,
                        value BLOB
                    )
                    """)
    return connect_pool[curr_thread_id]


def set_value(key, v):
    # version 1.1
    """
    这是一个设置值的函数，它将会把key和value(键值对)存储在名为'state'的数据库表中。如果已经存在相同的key，那么它会用新的value替换旧的value，否则就插入一条新的记录。
    
    参数:
        key: 需要设置的键。它是任意可以被哈希化的对象，例如字符串、数字或者元组。
        v: 与键对应的值。它也是一个任意的对象，可以是数字、字符串、列表、字典等等。
    
    返回值:
        这个函数没有返回值。
    
    使用方法:
        set_value('name', '张三')
        set_value(1, 100)
    
    注意事项：
        使用这个函数前，需要确保已经创建了名为'state'的数据库表，且该表有'key'和'value'两列。如果表不存在或者列不正确，那么这个函数将会抛出异常。
        此外，这个函数没有做任何的类型检查或者错误处理，所以调用者需要确保传入的参数是正确的，否则可能抛出异常。
    """
    

    obj = _load()
    with obj:
        obj.execute("""
            INSERT OR REPLACE INTO state (key, value)
            VALUES (?, ?)
            """,
                    (key, v)
                    )


def get_value(key):
    # version 1.1
    """
    这个函数用于从数据库中获取一个给定键对应的值。这个函数可能是一个配置读取工具的一部分，
    
    用于获取某个配置项的值。
    
    参数:
    
        key: 要获取的键。这是一个字符串。
    
    返回值:
    
        返回一个元组。如果键在对象中，则返回一个包含值的元组，如果键不在对象中，返回一个空元组。
    
    示例部分:
    
    ```python
    
        # 获取 'my_key' 对应的值
    
        value = get_value('my_key')
    
        if value:
    
            print('my_key 对应的值是 ', value)
    
        else:
    
            print('my_key 不在配置中')
    
    ```
    
    注意，这个函数依赖于一个名为 `_load` 的函数，但是这个函数在这段代码中没有定义。我们假设 `_load` 函数的目的是加载一个包含配置信息的对象，并返回这个对象。
    
    这个函数没有明显的错误或者bug。
    """
    

    obj = _load()
    cursor = obj.execute("""
        SELECT value FROM state WHERE key = ?
        """,
                         (key,)
                         )
    row = cursor.fetchone()
    return row[0] if row is not None else None


def has_value(key):
    # version 1.1
    """
    该函数用于判断给定的键是否在数据库的状态表中存在。
    
    参数:
        key: 需要检查的键，作为字符串传入。
    
    返回:
        如果查询的键在状态表中存在，则返回True，否则返回False。
    
    示例:
     has_value('my_key')
    True
     has_value('nonexistent_key')
    False
    """
    

    obj = _load()
    cursor = obj.execute("""
        SELECT 1 FROM state WHERE key = ?
        """,
                         (key,)
                         )
    return cursor.fetchone() is not None


def value_add(key, v):
    # version 1.1
    """
    这是一个value_add函数，主要用于数据库中为指定的键添加值。如果该键尚不存在，则会先插入一条新的记录。
    
    参数:
        key: 需要添加值的键，数据类型为字符串。
        v: 需要添加的值，数据类型为整型。
    
    返回:
        返回更新后键对应的值。
    
    使用示例:
        value_add('test', 1)
    
    注意：
        该函数依赖于_load()函数和get_value()函数，所以在调用value_add()函数前，请确保前述两个函数已被正确定义和实现。
        这个函数没有进行异常处理，如果在执行SQL语句时出现错误，程序可能会崩溃。在后续版本中会考虑加入异常处理机制。
    
    该函数在version 1.1版本中已更新。
    """
    

    obj = _load()
    with obj:
        obj.execute(
            "INSERT OR IGNORE INTO state (key, value) VALUES (?, 0)",
            (key,)
        )
        obj.execute(
            "UPDATE state SET value = value + ? WHERE key = ? ",
            (v, key)
        )
    return get_value(key)