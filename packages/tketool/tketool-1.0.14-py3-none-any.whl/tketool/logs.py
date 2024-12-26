# pass_generate
import logging, sys
from enum import Enum
from prettytable import PrettyTable, ALL
from collections import deque


class Custom_Handler(logging.Handler):
    """
    这个类是一个自定义的日志处理器，它继承自`logging.Handler`。
    
    这个处理器的主要功能是：将日志信息输出到标准输出，并且提供了一些特殊的处理，比如处理进度条显示和历史记录。
    
    这个处理器的工作原理如下：
    
    - 当日志等级为62时，表示这是一个进度条结束的信号，它会将进度条的标志位设置为`False`，并输出‘process finish.’信息。
    
    - 当日志等级为60时，表示这是一个进度条开始的信号，它会将进度条的标志位设置为`True`，并在标准输出上显示进度条。
    
    - 当日志等级为61时，表示这是一个普通的日志信息，但是需要在进度条下方打印，所以它会先输出一个回车符`\r`，然后输出日志信息，最后再输出进度条。
    
    - 对于其他日志等级，也会根据进度条的标志位来决定是在进度条下方打印，还是直接打印。
    
    这个处理器还维护了一个最近输出的20条日志的历史记录队列。
    
    这个类的使用方法如下：
    
    ```python
    import logging
    
    handler = Custom_Handler()
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    
    # 输出普通日志
    logger.log(61, "This is a normal log.")
    
    # 开始进度条
    logger.log(60, "Start progress bar...")
    
    # 结束进度条
    logger.log(62, "End progress bar.")
    ```
    """

    def __init__(self):
        """
            Custom_Handler类的初始化函数。
        
            该类是用于特殊的日志处理，包括处理进度条显示以及历史记录的保存等功能。在初始化的时候，会设定一些默认的参数。
        
            Attributes:
                in_processbar (bool): 一个标志位，用于判断当前是否在处理进度条显示。
                history (deque): 一个双端队列，用于保存最近的20条历史记录。
                processbar_str_temp (str): 一个临时字符串，用于保存当前的进度条显示。
        
            示例:
                handler = Custom_Handler()
                logger = logging.getLogger('your_logger')
                logger.addHandler(handler)
        
            注意:
                此类特定于处理带有进度条的日志。对于普通的日志，可能不适用。
        """

        super().__init__()
        self.in_processbar = False
        self.history = deque(maxlen=20)
        self.processbar_str_temp = ""

    def emit(self, record):
        """
        这是 Custom_Handler 类中的一个方法，用于将记录的日志信息输出至标准输出。此方法根据记录的日志级别进行不同的处理。
        
        参数:
            record: logging.LogRecord 对象，包含了所有要输出的日志信息。
        
        返回类型: 无返回值。
        
        函数流程：
            1. 如果日志级别为62，表明进度条已完成，它将向标准输出写入'\r'和'process finish.'，然后返回。
            2. 如果日志级别为60，表明进度条正在进行中，它将替换消息中的换行符，然后将消息写入到标准输出，如果此时不在进度条中，它还会在消息前增加一个换行符。
            3. 如果日志级别为其他值，它会根据是否在进度条中进行不同处理。如果在进度条中，它将在消息前后各增加一个换行符并将消息和进度条一起写入到标准输出。如果不在进度条中，它将在消息前增加一个换行符，然后将消息写入到标准输出。
        
        特殊处理：
            如果日志级别为61，它将不会替换消息中的换行符。
        
        注意：
            无论何时，都会刷新标准输出，并将消息添加到历史队列中。
        
        错误或者bug: 无特殊说明。
        """

        if record.levelno == 62:
            self.in_processbar = False
            sys.stdout.write('\r')
            sys.stdout.write('process finish.')
            return

        if record.levelno == 60:
            rp_msg = record.msg.replace("\n", "")
            self.processbar_str_temp = rp_msg
            self.in_processbar = True

            if self.in_processbar:
                sys.stdout.write('\r')
                sys.stdout.write(rp_msg)
                sys.stdout.flush()
            else:
                sys.stdout.write('\n')
                sys.stdout.write(rp_msg)
                sys.stdout.flush()
        else:
            if record.levelno == 61:
                rp_msg = record.msg
            else:
                rp_msg = record.msg.replace("\n", "")

            if self.in_processbar:
                sys.stdout.write('\r')
                sys.stdout.write(rp_msg)
                sys.stdout.write('\n')
                sys.stdout.write(self.processbar_str_temp)
                sys.stdout.flush()
            else:
                sys.stdout.write('\n')
                sys.stdout.write(rp_msg)
                sys.stdout.flush()
            self.history.append(rp_msg)


pass

logging.addLevelName(60, "process_bar")
logging.addLevelName(61, "multirow")
logging.addLevelName(62, "process_bar_end")
current_handle = Custom_Handler()
current_logger = logging.getLogger("tke_main")
current_logger.setLevel(logging.DEBUG)


def set_logger(target_logger):
    """
    这个函数用于设置日志记录器的处理程序。
    
    参数列表:
        target_logger (logging.Logger): 需要设置处理程序的目标日志记录器
    
    返回类型:
        无
    
    此函数将遍历目标日志记录器中的所有处理程序，并将它们从记录器中移除。
    然后，它将当前的处理程序添加到目标日志记录器中。
    注意，此函数假定在调用此函数之前，已经创建并配置了名为current_handle的处理程序。
    
    示例:
    
        import logging
        logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        set_logger(logger, handler)
    
    这段代码创建了一个名为__name__的日志记录器，并将默认流处理程序设置为处理程序。
    然后，它使用set_logger函数将处理程序设置为当前处理程序。
    
    注意: 此函数存在一个潜在的问题，那就是它会移除目标日志记录器中的所有处理程序，而不仅仅是要替换的那一个。
    如果记录器在其他地方也在使用，这可能会导致问题。在使用此函数之前，最好确认目标记录器的处理程序是否真的需要被完全替换。
    """

    for handler in target_logger.handlers[:]:
        target_logger.removeHandler(handler)
    target_logger.addHandler(current_handle)


set_logger(current_logger)


def log(str):
    """
    这是一个简单的日志记录函数。此函数首先通过全局变量current_logger获取当前的日志处理器，然后调用其info方法记录日志。此函数没有返回值。
    
    参数:
    str: 需要被记录的日志信息，类型为字符串。
    
    示例:
    log("This is a test log.")  # 输出: This is a test log.
    
    注意:
    尽管在函数体中存在一个被注释掉的print语句，但请不要取消注释并使用，因为它可能会在不支持ANSI escape code的环境中造成问题。该语句设计为在控制台输出彩色日志，\033[0m为ANSI escape code，用于重置颜色。
    
    错误和bug:
    暂时没有发现错误和bug。
    """

    global current_logger
    current_logger.info(str)
    # print(f"{str}\n")  # Using \033[0m to reset the color after printing


def log_multi_row(str):
    """
    这是一个记录多行日志的函数。
    
    函数的工作原理是使用全局变量 `current_logger`，并调用其 `log` 方法，实现多行日志的记录。
    
    参数:
        str (str): 需要记录的多行日志的字符串。
    
    返回类型:
        无。
    
    使用示例:
         log_multi_row("这是一个\n多行日志")
    
    注意事项:
        1. 本函数没有返回值，其功能仅仅是记录日志。
        2. 在使用本函数前，需要确保全局变量 `current_logger` 已经被正确初始化并可以使用。
        3. 由于 `log` 方法的第一个参数是 `61`，因此本函数可能仅适用于某些特定配置的日志系统。
    """

    global current_logger
    current_logger.log(61, str)


def get_log_history():
    """
    这是一个函数，获取当前句柄的日志历史记录。
    
    函数没有参数。
    
    返回类型是列表，其中包含当前句柄的历史记录。
    
    示例：
    ```python
    log_history = get_log_history()
    ```
    
    注意：此函数使用了全局变量current_handle，确保在调用此函数前已正确初始化此全局变量。
    
    没有已知错误或bug。
    """

    global current_handle
    return [s for s in current_handle.history]


class log_color_enum(Enum):
    """
    这是一个枚举类log_color_enum，其目的是定义一系列关于日志颜色的常量。这些常量与ANSI颜色代码相对应。
    
    枚举值包括:
    - DEFAULT: 默认颜色，无特殊颜色代码。
    - RED: 红色代码。
    - YELLOW: 黄色代码。
    - GREEN: 绿色代码。
    - BLUE: 蓝色代码。
    - MAGENTA: 洋红色代码。
    - CYAN: 青色代码。
    
    每个枚举值都是由ANSI颜色代码字符串表示。例如，对于红色，其ANSI颜色代码是"\033[91m"。
    
    使用示例:
    
    ```python
    print(f"{log_color_enum.RED.value}This is red text{log_color_enum.DEFAULT.value}")
    ```
    
    在上述示例中，我们使用log_color_enum.RED.value获取红色的ANSI代码，然后将其添加到需要显示为红色的文本前面。然后，我们添加DEFAULT的ANSI代码，以重置颜色到默认状态。这样，任何在这之后打印的文本都将以默认颜色显示，而不是红色。
    
    注意，在某些环境（如Windows的某些版本）中，ANSI颜色代码可能无法正常工作。可能需要使用第三方库（如colorama）来启用ANSI颜色支持。
    
    没有已知的错误或bug。
    """

    DEFAULT = ""
    RED = "\033[91m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"


def convert_print_color(*args):
    """
    此函数接收多个参数（可能是字符串或者元组），并根据参数类型进行处理。如果参数是元组，且元组长度为2，元组的第二个元素是颜色枚举类型，那么该元组被认为是包含字符串和颜色枚举的元组，函数会将其转化为带有颜色的字符串；如果参数不符合前述条件，那么直接认为该参数是字符串，进行处理。
    
    Args:
        *args: 可变参数。每个参数可能是一个字符串，或者一个包含字符串和颜色枚举的元组。
    
    Returns:
        str: 返回由输入参数转化而来的字符串，如果参数是包含字符串和颜色枚举的元组，转化后的字符串将带有颜色。
    
    Example:
    
        convert_print_color('hello', ('world', log_color_enum.RED))
        # 输出：'hello\033[31mworld\033[0m'
    
    Note:
        需要注意，对于元组参数，其第二个元素必须是颜色枚举类型，否则函数会抛出异常。
    """

    result = []

    for arg in args:
        if isinstance(arg, tuple) and len(arg) == 2 and isinstance(arg[1], log_color_enum):
            # 元组包含字符串和颜色枚举
            result.append(f"{arg[1].value}{arg[0]}\033[0m")
        else:
            # 只有字符串
            result.append(arg)

    return ''.join(result)


def _truncate_content(content, max_length):
    """
    这个函数的主要目的是截断一个给定的字符串内容，使其不超过指定的最大长度。
    
    参数:
        content: str
            需要被截断的字符串内容
        max_length: int
            字符串的最大允许长度
    
    返回类型:
        str:
            如果输入的字符串长度超过max_length，则返回被截断后并添加'..'的字符串；
            如果输入的字符串长度不超过max_length，则返回原字符串。
    
    示例：
        _truncate_content('Hello World', 5)
        返回值： 'Hello..'
    
    注意：
        如果max_length小于0，该函数并未做任何处理，可能会产生不符合预期的结果。
    """

    return (content[:max_length] + '..') if len(content) > max_length else content


def print_table(table_col: [str], rows: [[str]], truncate_string=30):
    """
    这个函数的主要作用是打印一个格式良好的表格，表格的列名由参数 `table_col` 提供，表格的数据由参数 `rows` 提供。
    
    参数:
        table_col (list[str]): 表格列的名字，这是一个字符串列表。
        rows (list[list[str]]): 表格的数据，这是一个二维字符串列表，每个子列表代表一行数据。
        truncate_string (int, optional): 如果某个单元格的字符串长度超过这个值，则会被截断。默认值为30。
    
    返回值:
        无。这个函数没有返回值，它的主要目标是提供一个优雅的表格输出。
    
    例子:
    
    ```python
    cols = ["姓名", "年龄", "职业"]
    data = [
        ["张三", "27", "工程师"],
        ["李四", "31", "医生"],
        ["王五", "25", "教师"]
    ]
    print_table(cols, data)
    ```
    
    注意事项：
    1. 当表格数据的行数和 `table_col` 的长度不一致时，将会引发 `Exception`。
    2. `truncate_string` 参数不能为负值，否则会引发 `Exception`。
    """

    xtable = PrettyTable()
    xtable.field_names = table_col
    for _r in rows:
        if truncate_string is not None:
            xtable.add_row([_truncate_content(rr, truncate_string) for rr in _r])
        else:
            xtable.add_row(_r)
    log_multi_row(str(xtable))
