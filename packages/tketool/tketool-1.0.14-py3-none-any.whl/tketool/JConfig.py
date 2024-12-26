# pass_generate
import os
from tketool.logs import log


class ConfigManager:
    """
    这是一个ConfigManager类，其目的是用来处理配置文件的读取和写入。它将读取指定的配置文件，并将其内容存储为字典格式以供查询。如果尝试获取不存在的配置项，它会使用默认值，并在配置文件中添加这个键值对。
    
    以下是一个使用示例:
    
    ```python
    cm = ConfigManager("/path/to/config")
    value = cm.get_config("key", "default")
    ```
    
    类方法介绍:
    - `__init__`: 初始化方法，接收一个配置文件路径参数。在创建类实例时，会立即加载配置文件。
    
    - `_load_configs`: 私有方法，负责加载配置文件。如果文件存在，就读取所有行并将其转换为字典格式。如果文件不存在，就创建一个新的空文件。
    
    - `_sanitize_string`: 静态方法，接收一个字符串，去掉其开头和结尾的双引号或单引号，然后返回。
    
    - `get_config`: 公有方法，接收一个键和一个默认值参数。如果键存在于配置文件中，则返回对应的值；如果不存在，则返回默认值，并将这个键值对添加到配置文件中。
    
    注意：如果配置文件的写入权限被禁止，这个类可能会抛出异常。
    
    """

    def __init__(self, config_file_path):
        """
            ConfigManager是一个用于配置管理的类。
        
            创建对象时，用户需要提供配置文件的路径作为参数。在创建对象后，该类会自动加载指定路径下的配置文件，以便后续通过键值对的方式获取配置信息。
        
            如果在获取配置信息时，指定的键不存在，该类会自动在配置文件末尾添加该键，并设置其值为默认值。
        
            示例：
            ```python
            config_manager = ConfigManager("/path/to/config/file")
            db_host = config_manager.get_config("db_host", "localhost")
            ```
        
            参数:
            config_file_path: 配置文件的路径。可以是相对路径或绝对路径。如果指定的路径不存在，会自动创建一个新的空白配置文件。
        
            注意：
            1. 配置文件中的键和值都是字符串形式，键值对之间通过等号("=")分隔，例如：`db_host=localhost`
            2. 此类没有提供修改配置信息的方法，如果需要修改配置信息，需要直接修改配置文件，然后重新创建ConfigManager对象以加载新的配置信息。
        """

        self._config_map = {}

        self._config_file_path = config_file_path

        self._load_configs()

    def _load_configs(self):
        """
        `_load_configs`是一个私有方法，用于加载配置文件中的配置。如果配置文件存在，它会读取文件中的每一行，并通过等号('=')将每一行分割为key和value，并将它们加入到`_config_map`字典中。同时，为了确保配置项的值是干净的，我们使用`_sanitize_string`方法去除两边可能存在的引号。
        
        如果配置文件不存在，此方法会创建一个新的空的配置文件。
        
        注意，此方法没有返回值。
        
        执行这个方法不需要任何参数。
        
        这个方法在初始化`ConfigManager`类的时候会被自动调用，用于加载配置文件的内容，无需手动调用。
        """

        if os.path.exists(self._config_file_path):
            with open(self._config_file_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    key, sep, value = line.strip().partition('=')
                    if sep:  # ensure that '=' is present
                        self._config_map[self._sanitize_string(key)] = self._sanitize_string(value)
        else:
            with open(self._config_file_path, 'w') as f:
                f.writelines("")

    @staticmethod
    def _sanitize_string(s):
        """
            _sanitize_string是一个静态方法，用于处理输入的字符串，去除字符串两边的双引号和单引号。
        
            参数:
            s (str): 待处理的字符串。
        
            返回:
            str: 返回处理后的字符串。
        
            例如：
            输入字符串为' "example" ',调用此方法后，返回的字符串为'example'。
        
            注意：
            该方法仅处理字符串前后的引号，不处理字符串中间的引号。
        """

        return s.strip('"').strip("'")

    def get_config(self, key, default_value=""):
        """
        此函数是用于获取指定键的配置值。如果键存在于配置映射中，则直接返回其对应的值；否则，会给出警告并在配置文件中添加键和默认值，并返回默认值。
        
        参数:
            key (str): 需要获取的配置的键。
            default_value (str, 可选): 如果键不存在于配置映射中，将使用此默认值。默认值为""。
        
        返回:
            str: 返回的配置值，如果键不存在于配置映射中，返回的是默认值。
        
        注意:
            如果键不存在，此函数将自动在配置文件中创建该键，并设置其值为默认值，然后返回默认值。
        """

        if key in self._config_map:
            return self._config_map[key]

        log(f"No config key: {key}")
        with open(self._config_file_path, 'a') as f:
            f.writelines(f'{key}="{default_value}"\n')

        return default_value


_config_instance = {}


def get_config_instance(filename=None):
    """
    这个函数的目标是得到一个配置管理器实例。
    
    如果文件名参数为空，函数将获取当前工作目录下名为'config.jconfig'的文件。
    
    如果该文件名还未在_config_instance全局变量中，函数将创建一个新的配置管理器实例，
    并将其在_config_instance中与该文件名关联起来。
    
    这个函数使用了全局变量_config_instance来存储所有已创建的配置管理器实例，
    并以文件名作为每个实例的键。这种设计模式被称为单例模式，通过它，可以确保对于同一个配置文件，
    总是返回同一个配置管理器实例。
    
    参数:
        filename: str, optional, default=None
            配置文件的名字。如果没有指定，将使用当前工作目录中名为'config.jconfig'的文件。
    
    返回:
        ConfigManager实例。根据提供的文件名，返回对应的配置管理器实例。如果该文件名还未在
        _config_instance中，则创建一个新的实例并返回。
    
    错误:
        如果指定的文件不存在，ConfigManager的构造函数将抛出异常。
    
    示例:
        # 获取默认配置文件的配置管理器实例
        config_instance = get_config_instance()
    
        # 获取指定配置文件的配置管理器实例
        config_instance = get_config_instance('my_config.jconfig')
    
    注意:
        此函数依赖于_config_instance全局变量和ConfigManager类，需要确保在使用此函数之前，
        这些全局变量和类已经被正确地定义和初始化。
    """

    global _config_instance

    if not filename:
        filename = os.path.join(os.getcwd(), 'config.jconfig')

    if filename not in _config_instance:
        # if _config_instance is None:
        _config_instance[filename] = ConfigManager(filename)
        log(f"use config_file in {filename}")
    return _config_instance[filename]
