# pass_generate
import base64
import os, threading
import sqlite3
import pickle
from tketool.JConfig import get_config_instance
import tketool.buffer.bufferbase as bb
from tketool.logs import log

# Global variables should be in uppercase according to PEP8
BUFFER_FOLDER = get_config_instance().get_config("buffer_folder", "buffer")
BUFFER_FILE_PATH = os.path.join(os.getcwd(), BUFFER_FOLDER, "buffer.db")


def init_db():
    """
    这个函数`init_db`的主要作用是初始化数据库，并提供对数据库表`buffer`的增删查改的接口。
    
    函数首先检查存放数据库的文件夹是否存在，如果不存在则创建。
    然后建立连接池，这是一个字典，其键值为线程的ID，值为线程创建的SQLite数据库连接。
    
    函数内部定义了四个操作数据库的函数：
    
    - `_load_buffer_file(key)`: 从`buffer`表中加载具有特定键（`key`）的数据，返回的数据为pickle反序列化后的数据。如果键不存在，返回None。
    
    - `_save_buffer_file(lists)`: 将数据保存到`buffer`表中，数据是一个列表，列表的每个元素是一个键值对，键为字符串，值为任意pickle序列化后的对象。
    
    - `_delete_buffer_file(key)`: 从`buffer`表中删除具有特定键（`key`）的数据。
    
    - `_has_buffer_file(key)`: 判断`buffer`表中是否存在具有特定键（`key`）的数据。
    
    函数最后将这四个函数绑定到全局变量`bb`的相应方法上。
    
    :param 无
    :return tuple: 返回一个元组，元组的第一个元素为数据库连接，第二个元素为一个指向数据库的游标。
    
    示例：
    
    ```
    conn, cursor = init_db()
    ```
    
    注意：函数没有进行异常处理，如果数据库操作失败，可能会抛出异常。
    """

    if not os.path.exists(BUFFER_FOLDER):
        os.makedirs(BUFFER_FOLDER)

    connect_pool = {}

    def get_or_create_connect():
        """
        此函数用于获取或创建数据库连接。
        
        此函数根据当前线程的id检查连接池中是否存在对应的连接，如果存在则返回该连接，否则创建一个新的连接并添加到连接池中。
        
        函数不需要参数。
        
        返回值为sqlite3.Connection对象，即数据库连接。
        
        此函数没有已知的错误或bug。
        
        以下是一个使用示例：
        
            # 使用函数获取或创建连接
            conn = get_or_create_connect()
            # 使用获取的连接执行数据库操作
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM table_name")
        
        注意：在多线程环境中，每个线程必须使用独立的数据库连接，共享同一连接可能会导致数据冲突或其他问题。此函数通过为每个线程创建独立的连接来解决此问题。
        """

        curr_thread_id = threading.get_ident()
        if curr_thread_id not in connect_pool:
            connect_pool[curr_thread_id] = sqlite3.connect(BUFFER_FILE_PATH)
        return connect_pool[curr_thread_id]

    t_conn = get_or_create_connect()
    t_c = t_conn.cursor()

    # create table if not exists
    t_c.execute('''
        CREATE TABLE IF NOT EXISTS buffer (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
    ''')
    t_conn.commit()

    def _load_buffer_file(key):
        """
        _load_buffer_file(key)是一个内部函数, 它的主要目的是从数据库中读取特定键值对应的缓存文件。
        
        参数:
        key (str) : 表示需要获取的键值。
        
        返回:
        返回的值类型是不确定的，因为这取决于在创建缓存文件时存储的数据类型。如果数据库中存在对应的键值，则返回对应的值，否则返回None。
        
        示例用法：
        
        _load_buffer_file("my_key")
        
        这将返回数据库中以"my_key"为键的缓存文件的值。如果不存在对应的键值，将返回None。
        
        请注意，在调用此函数时，需要确保已经初始化了数据库连接。
        
        """

        conn = get_or_create_connect()
        c = conn.cursor()
        c.execute("SELECT value FROM buffer WHERE key = ?", (key,))
        row = c.fetchone()
        if row is not None:
            byte_str = base64.b64decode(row[0].encode('utf-8'))
            return pickle.loads(byte_str)
        else:
            return None

    def _save_buffer_file(lists):
        """
        _save_buffer_file是一个内部函数，它将传入的列表中的每个元素进行序列化，然后将序列化后的值存储到数据库中。
        
        参数:
            lists (list): 需要保存的数据列表，每个元素都是一个元组，元组的第一个元素是key，第二个元素是待保存的对象。
        
        返回类型:
            None
        
        使用方法：
            这个函数是作为init_db函数的内部函数，不应该直接调用，它将在init_db函数中被赋值给bb.save_buffer_file，之后应使用bb.save_buffer_file来保存数据。
        
        示例:
            假设有一个数据列表[('key1', obj1), ('key2', obj2)]
            _save_buffer_file([('key1', obj1), ('key2', obj2)])
        
        注意:
            这个函数没有进行错误处理，如果数据库操作失败，会直接抛出异常。
            另外，它使用了REPLACE INTO语句来插入或更新数据，如果数据库中已经存在同样的key，那么原来的数据会被新的数据替换。
        """

        conn = get_or_create_connect()
        c = conn.cursor()
        for k, v in lists:
            byte_str = pickle.dumps(v)
            str_obj = base64.b64encode(byte_str).decode('utf-8')
            c.execute("REPLACE INTO buffer (key, value) VALUES (?, ?)", (k, str_obj))
        conn.commit()

    def _delete_buffer_file(key):
        """
        _delete_buffer_file(key)函数用于从数据库中删除特定的key对应的记录。
        
        参数:
            key: 字符串类型，代表要从数据库中删除的记录的Key。
        
        返回:
            无返回值。
        
        使用方法:
            _delete_buffer_file('test_key')  # 删除key为'test_key'的记录。
        
        注意:
            此函数不返回任何值，仅用于执行删除数据库记录的操作。
            若数据库中不存在对应的key，此函数将不会产生任何效果。
        """

        conn = get_or_create_connect()
        c = conn.cursor()
        c.execute("DELETE FROM buffer WHERE key = ?", (key,))
        conn.commit()

    def _has_buffer_file(key):
        """
        这是一个函数，其主要功能是检查SQLite数据库的'buffer'表中是否存在给定的key。
        
        参数:
            key: 需要查询的键值。
        
        返回:
            返回一个布尔值，如果存在该键则返回True，否则返回False。
        
        例子:
            _has_buffer_file('test_key')
        """

        conn = get_or_create_connect()
        c = conn.cursor()
        c.execute("SELECT 1 FROM buffer WHERE key = ?", (key,))
        row = c.fetchone()
        return row is not None

    bb.has_buffer_file = _has_buffer_file
    bb.load_buffer_file = _load_buffer_file
    bb.delete_buffer_file = _delete_buffer_file
    bb.save_buffer_file = _save_buffer_file

    return t_conn, t_c


# Initialize the SQLite connection and cursor and store them in global variables
CONN_OBJ, CURSOR_OBJ = init_db()
log("use onesqlite")

def close_db():
    """
    这个函数是用于关闭数据库连接的。在全局变量CONN_OBJ存在的情况下，它会调用CONN_OBJ的close方法来关闭连接，并将CONN_OBJ设置为None。
    
    函数没有接收任何参数，也没有返回任何内容。主要的用途是在执行数据库操作后，释放数据库连接资源。
    
    该函数假设CONN_OBJ具有close方法，如果CONN_OBJ不具有此方法，将会抛出异常。同时，该函数没有处理可能的数据库关闭异常，如果在关闭数据库连接时发生错误，该错误会被抛出。
    
    示例代码：
    
        # 初始化数据库连接
        CONN_OBJ = create_db_connection()
    
        # 执行数据库操作
        ...
    
        # 在完成数据库操作后，关闭数据库连接
        close_db()
    """

    global CONN_OBJ
    if CONN_OBJ:
        CONN_OBJ.close()
        CONN_OBJ = None
