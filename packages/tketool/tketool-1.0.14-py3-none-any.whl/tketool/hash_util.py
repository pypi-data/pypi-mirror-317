# pass_generate
from collections.abc import Iterable
import hashlib


def hash_str(target_str: str) -> str:
    """
    这是一个将字符串哈希化的函数。
    
    Args:
        target_str (str): 对这个字符串进行哈希化操作。
    
    Returns:
        str: 返回一个经过MD5哈希运算后的字符串。
    
    注意:如果传入的不是字符串类型,会先将其转化为字符串类型然后进行哈希运算。
    
    示例:
    ```python
    print(hash_str('hello world')) # 输出: 5eb63bbbe01eeed093cb22bb8f5acdc3
    ```
    
    函数并不会检查传入参数的有效性, 如果传入对象不能被转化为字符串, 则会抛出一个ValueError异常。
    
    """

    if not isinstance(target_str, str):
        target_str = str(target_str)

    return hashlib.md5(target_str.encode("utf8")).hexdigest()


def hash_obj_strbase(obj) -> str:
    """
    该函数的主要功能是对输入的对象进行哈希处理，转换成字符串的形式。它能够对不同类型的对象进行处理，包括字符串、整数、浮点数、字典以及可迭代的对象。
    
    参数:
        obj: 待处理的对象，可以是任何类型
    
    返回:
        对输入对象进行哈希处理后的字符串
    
    处理过程:
        1. 如果输入的对象是字符串、整数、浮点数，则直接转换为字符串并进行哈希处理
        2. 如果输入的对象是字典，则将字典的键和值分别转换为列表，然后进行哈希处理，最后将处理后的键和值的哈希结果进行连接并进行哈希处理
        3. 如果输入的对象是可迭代的对象，则将每个元素转换为字符串并进行哈希处理，然后将所有元素的哈希结果连接成一个字符串并进行哈希处理
        4. 如果输入的对象是其他类型，则将对象的类名转换为字符串并进行哈希处理
    
    注意事项:
        这个函数没有处理递归引用的情况，例如，列表或字典等数据结构中包含自身的引用，这会导致无限递归。如果输入的对象中存在这种情况，函数可能会出现堆栈溢出的错误。
    
    示例:
        print(hash_obj_strbase("hello"))  # 输出一个字符串的哈希值
        print(hash_obj_strbase({"name": "Tom", "age": 20}))  # 输出一个字典的哈希值
        print(hash_obj_strbase([1, 2, 3]))  # 输出一个列表的哈希值
        print(hash_obj_strbase((1, 2, 3)))  # 输出一个元组的哈希值
    """

    if isinstance(obj, (str, int, float)):
        return hash_str(str(obj))

    if isinstance(obj, dict):
        keys_hashed = hash_obj_strbase(list(obj.keys()))
        values_hashed = hash_obj_strbase(list(obj.values()))
        return hash_str(keys_hashed + values_hashed)

    if isinstance(obj, Iterable):
        items_hashed_list = [hash_obj_strbase(x) for x in obj]
        return hash_str("".join(items_hashed_list))

    return hash_str(str(obj.__class__))
