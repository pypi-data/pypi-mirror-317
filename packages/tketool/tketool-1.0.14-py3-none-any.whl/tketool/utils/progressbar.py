# pass_generate
import math, sys, time
from collections.abc import Iterable
from tketool.logs import current_logger, log


class process_status_bar:
    """
    这是一个用于处理状态条显示的类，可以用于需要状态条展示进度的情况，显示进度条的长度、进度、剩余时间等信息。
    
    属性:
        _iter_stack: 用于储存状态的栈。
        _process_bar_len: 进度条显示长度。
        _print_str: 用于打印的字符串。
        hidden: 是否隐藏进度条。
    
    方法:
        _cast_second_strformat(self, sec): 将给定的秒数转换为时:分:秒的格式。
        _flush_(self): 根据状态栈更新并显示进度条。
        iter_bar(self, iter_item, value=0, key=None, max=None): 开始一个新的进度显示，显示对应的迭代对象的进度。
        start(self, key, max, value=0): 开始一个新的状态条显示。
        set_value(self, v): 设置进度条的当前值。
        one_done(self): 完成一个任务，进度值加1。
        stop_current(self): 停止当前的状态条显示。
        process_print(self, str): 打印自定义字符串。
        print_log(self, str): 打印日志信息。
    
    使用示例：
    
        psb = process_status_bar(30)
        for item in psb.iter_bar(range(100), key="Processing", max=100):
            job_do_something(item)
        psb.stop_current()
    
    注意事项：
    - 当迭代对象为无限长度或者非可迭代对象时，需要手动设置max值。
    - 在使用iter_bar开始一个新的进度显示时，需要在完成任务后手动调用stop_current停止当前的状态条显示。
    """

    def __init__(self, processbar_length=20, bar_max_str_leng=200):
        """
        初始化一个进程状态栏（process status bar）类。
        
        参数:
        processbar_length (int, 默认为20): 用于指定进程状态栏的长度。
        
        此类的主要目的是用于在控制台显示进程或任务的进度信息，例如，当你需要在循环中处理大量数据时，你可以使用此类来跟踪和显示进度。此类还可以显示每个任务的剩余时间和平均处理时间，这对于估计长时间运行的任务非常有用。
        
        示例:
        
        ```
        bar = process_status_bar(30)
        for i in bar.iter_bar(range(100), key="Processing"):
            time.sleep(0.1)  # 模拟数据处理
        ```
        
        在上述示例中，我们首先创建了一个长度为30的进程状态栏实例。然后我们使用iter_bar方法在循环中处理数据。在此方法中，我们需要传递一个可迭代对象以及一个关键字参数key来描述正在进行的任务。在每次循环迭代中，我们都会使用time.sleep来模拟数据处理的过程，处理完一个数据，状态栏会自动更新进度。
        
        此类没有明显的错误或BUG，但是在处理无法预计长度的迭代对象（如生成器）时，可能无法正确显示进度。对于这种情况，你需要手动设置进度条的最大值。
        
        """

        self._iter_stack = []
        self._process_bar_len = processbar_length
        self._print_str = ""
        self.hidden = False
        self.max_str_length = bar_max_str_leng
        # self._print_logs = []

    def _cast_second_strformat(self, sec):
        """
        此函数的主要目的是将秒数转为字符串格式的时间展示。
        
        参数:
            sec: int
                输入的秒数
        
        返回:
            str
                返回一个HH:MM:SS格式的字符串，其中HH、MM、SS分别表示小时、分钟和秒。
        
        例如，输入3661秒，返回'01:01:01'。
        
        注意:
            此函数假设输入的秒数sec为非负整数。如果输入的sec为负数或者非整数，可能会产生无法预期的结果或错误。
        """

        m, s = divmod(sec, 60)
        h, m = divmod(m, 60)
        return "%02d:%02d:%02d" % (h, m, s)

    def _split_max_output_length(self, ostr) -> str:
        if len(ostr) <= self.max_str_length:
            return ostr
        else:
            #cut_str = int(self.max_str_length * 0.4)
            return f"...{ostr[-self.max_str_length:]}"
            #return f"{ostr[0:cut_str]}.....{ostr[-cut_str:]}"

    def _flush_(self):
        """
        `_flush_`方法是`process_status_bar`类内部使用的方法，主要用于刷新和输出进度条的状态。这个方法首先检查是否需要隐藏进度条，如果需要则直接返回。然后，它会构建含有所有迭代器状态的字符串，包括进度百分比、剩余时间等信息。然后，它会更新当前迭代器的平均执行时间和剩余执行时间。最后，它会通过日志输出当前的进度条状态。这个方法没有参数和返回值。
        
        这个方法可能会有一些小问题。比如，当迭代器的最大值为0时，进度条的长度可能会取整到0，导致进度条显示不正确。此外，当迭代器的值为0时，平均执行时间和剩余执行时间都会被设置为0，这可能不是我们期望的结果。在实际使用中需要注意这些问题。
        """

        if self.hidden:
            return

        if len(self._iter_stack) == 0:
            # sys.stdout.write('\r')
            # sys.stdout.write("                                                      ")
            # sys.stdout.flush()
            return

        stack_str = ""
        for iter_i in range(len(self._iter_stack) - 1):
            p_value = self._iter_stack[iter_i]['value'] / float(self._iter_stack[iter_i]['max'])
            p_value = "%.2f" % (p_value * 100)
            p_count = f"{self._iter_stack[iter_i]['value']}/{self._iter_stack[iter_i]['max']}"

            if self._iter_stack[iter_i]['value'] != 0:
                avg_cost = self._iter_stack[iter_i]['avg_cost']
                b_dic = self._iter_stack[iter_i]
                sur_plus = avg_cost * b_dic['max'] - time.time() + b_dic['start']
                time_show = f"({self._cast_second_strformat(avg_cost)},{self._cast_second_strformat(sur_plus)})"
            else:
                time_show = ""

            stack_str += f"[{self._iter_stack[iter_i]['key']}  {p_count}  {p_value}%{time_show}] >>"
            pass

        current_item = self._iter_stack[-1]
        p_value = 0 if float(current_item["max"]) == 0 else current_item["value"] / float(current_item["max"])
        p_value_str = "%.2f" % (p_value * 100)

        bar_size = math.floor(p_value * self._process_bar_len)

        bar_str = ""
        for i in range(self._process_bar_len):
            if i + 1 <= bar_size:
                bar_str += "*"
            else:
                bar_str += " "

        if current_item['value'] != 0:
            avg_cost = current_item['avg_cost']
            sur_plus = current_item['plus_cost']
            time_show = f"{self._cast_second_strformat(avg_cost)},{self._cast_second_strformat(sur_plus)}"
        else:
            time_show = "-:-:-,-:-:-"

        bar_str = f'{stack_str} {current_item["key"]} {current_item["value"]}/{current_item["max"]}  [{bar_str}]{p_value_str}% [{time_show}] - {self._print_str} '

        current_logger.log(60, self._split_max_output_length(bar_str))

        # if len(self._print_logs) == 0:
        #     current_logger.log(60, bar_str)
        #     # sys.stdout.write('\r' + bar_str)
        # else:
        #     # sys.stdout.write('\r')
        #     for s in self._print_logs:
        #         current_logger.log(s)
        #         # sys.stdout.write(s + "\n")
        #     self._print_logs.clear()
        #     current_logger.log(60, bar_str)
        #     # sys.stdout.write(bar_str)
        # sys.stdout.flush()

    def iter_bar(self, iter_item, value=0, key=None, max=None):
        """
        `iter_bar`是一个成员函数，这个函数主要是为了在迭代过程中创建进度条。
        
        参数:
            iter_item (Iterable): 需要迭代的对象。
            value (int, 可选): 迭代开始时的值，默认为0。
            key (str, 可选): 进度条的名字，默认为None，在此情况下，会自动生成名字为"Iter i"(i为当前进度条所在的堆栈位置)。
            max (int, 可选): 迭代对象的最大长度，默认为None，在此情况下，会尝试获取iter_item的长度作为最大长度。
        
        返回:
            generator: 对输入的迭代对象进行封装，每次迭代完成后，都会更新进度条。
        
        例子:
            bar = process_status_bar()
            for i in bar.iter_bar(range(100)):
                print(i)
        
        这将打印出从0到99的数字，同时在控制台显示进度条。
        注意在循环结束后，进度条会自动调用`stop_current`来结束。如果在循环过程中出现异常需要提前结束，你需要手动调用`stop_current`来清理进度条。
        
        异常:
            如果iter_item不是一个有限长度的可迭代对象，这个函数将抛出一个异常。
        """

        def get_length(iter_item):
            if isinstance(iter_item, Iterable):
                try:
                    return len(iter_item)
                except TypeError:
                    # 'iter_item' is an iterable but doesn't have a __len__ method.
                    # It could be something like an infinite generator.
                    raise Exception("该对象为无限长度的可迭代对象")
            else:
                raise Exception("需要指定max值")

        if max is None:
            max = get_length(iter_item)

        self.start(key, max, value)
        for _iter in iter_item:
            yield _iter
            self.one_done()

        self.stop_current()

    def start(self, key, max, value=0):
        """
                开始一个新的进度追踪过程。每个进度追踪过程用一个字典进行存储，其中包括进度追踪的键（标记）、最大值、当前值、开始时间、平均耗时和剩余时间。这些信息会在进度条中显示。
        
                Args:
                    key (str): 进度追踪的标记，如果未指定，则默认为"Iter {len(self._iter_stack)}"格式的字符串。
                    max (int): 进度追踪的最大值。
                    value (int, optional): 进度追踪的当前值，默认为0。
        
                Returns:
                    None
        
                注意事项：
                    1. 如果同一个进度条对象中，连续调用了多次start() 方法，但未对应调用stop()，那么会形成一个进度追踪的栈结构。
                    2. 在进度条显示时，会依次展示栈中所有进度追踪的信息，并以 ">>" 分隔。
                    3. 调用stop()方法时，会出栈最顶层的进度追踪过程。
                """

        if key is None:
            key = f"Iter {len(self._iter_stack)}"
        self._iter_stack.append({
            'key': key,
            'value': value,
            'max': max,
            'start': time.time(),
            'avg_cost': 0,
            'plus_cost': 0
        })
        self._flush_()

    def set_value(self, v):
        """
        这是一个更新进度条中当前任务进度的方法。
        
        参数:
            v: 这是一个整数，代表当前任务完成的进度。
        
        返回:
            这个函数没有返回值。
        
        用法:
        
        ```python
        # 创建一个进度条对象
        p = process_status_bar()
        
        # 开始一个名为'task1'，总进度为100的任务
        p.start('task1', 100)
        
        # 设置任务'task1'完成了30的进度
        p.set_value(30)
        ```
        
        注意:
            1. 如果v超过了任务的总进度，可能会导致进度条显示错误。
            2. `set_value`方法只会更新最近一次`start`开始的任务的进度，不会影响其他任务。
        """

        self._iter_stack[-1]['value'] = v

        if self._iter_stack[-1]['value'] != 0:
            avg_cost = (time.time() - self._iter_stack[-1]['start']) / self._iter_stack[-1]['value']
            sur_plus = avg_cost * (self._iter_stack[-1]['max'] - self._iter_stack[-1]['value'])
            self._iter_stack[-1]['avg_cost'] = avg_cost
            self._iter_stack[-1]['plus_cost'] = sur_plus
        else:
            self._iter_stack[-1]['avg_cost'] = 0
            self._iter_stack[-1]['plus_cost'] = 0

        self._flush_()

    def one_done(self):
        """
        `one_done(self):` 这个函数的主要职责是更新进度条的进度。
        
        函数名称：one_done
        
        函数目的：该函数会将进程栈中的最后一个元素的值增加1，然后更新进度条。每当一个任务完成时，此函数被调用一次。
        
        参数列表：该函数不接受任何参数。
        
        返回类型：无返回值。
        
        使用示例：
        
        ```
        bar = process_status_bar()
        for i in range(10):
            # 进行一些操作
            bar.one_done()
        ```
        
        注意：该函数不会检查进度是否超过了最大值，因此使用时需要确保任务的总数不会超过预先设定的最大值。
        
        """

        self.set_value(self._iter_stack[-1]['value'] + 1)

    def stop_current(self):
        """
            `stop_current`方法用于终止当前进度条，并将其从进度条栈中移除。如果所有的进度条都已经被移除，那么在日志中留下一个标记。
        
            该方法没有参数。
        
            返回类型: 无。
        
            使用示例：
            ```python
            processbar = process_status_bar()
            processbar.start('Task1', 10)
            for i in range(10):
                # 执行相关任务
                processbar.one_done()  # 每完成一个子任务，调用一次one_done()
            processbar.stop_current()  # 完成所有子任务后，调用stop_current()结束当前进度条
            ```
            注意：stop_current应当在完成所有子任务后调用，否则可能引发错误。
        """

        self._iter_stack.pop(-1)
        self._flush_()

        # clear a mark of log
        if len(self._iter_stack) == 0:
            current_logger.log(62, "")

    # def update_process_value(self, v):
    #     """
    #     强制更新进度条的进度数值
    #     :param v: 要更新的数值
    #     :return: 无返回
    #     """
    #     self._iter_stack[-1]['value'] = v

    def process_print(self, str):
        """
        `process_print` 是一个成员方法，其主要功能是为进度条附加一个字符串，用于描述当前进度条的状态，例如："正在执行某操作..."。这个方法会将传入的字符串作为状态信息显示在进度条的末尾。同时，此方法会调用 `_flush_` 方法对进度条进行刷新，使得新的状态信息能够立即显示出来。
        
        参数:
            str: 字符串类型，用于描述当前进度条的状态信息。
        
        返回值:
            无返回值。
        
        使用示例：
        ```python
        p = process_status_bar(processbar_length=20)
        p.start(key='Step1', max=100)
        for i in range(100):
            time.sleep(0.1)  # 模拟耗时操作
            p.one_done()
            if i == 50:
                p.process_print('已完成一半工作')
        p.stop_current()
        ```
        
        注意事项：
            本方法不对输入字符串`str`进行任何安全性或合法性检查，请确保输入的`str`为合法的字符串，且不含有可能破坏进度条显示效果的特殊字符。
        """

        self._print_str = str
        self._flush_()

    def print_log(self, str):
        """
        `print_log(self, str)`方法是`process_status_bar`类的一个成员方法，用于打印日志信息。
        
        参数:
            str: 需要打印的日志信息，类型为字符串。
        
        返回:
            无返回值。
        
        使用示例:
        ```python
        bar = process_status_bar()
        bar.print_log("开始处理...")
        ...
        bar.print_log("处理完成...")
        ```
        以上代码演示了如何使用`print_log`方法打印日志信息。
        
        注意: 该方法内部调用了log函数打印日志，但是这里没有提供log函数的定义，并且该方法的注释部分也被注释掉了，所以在使用这个方法前，需要保证log函数已经被定义，否则会引发`NameError`异常。
        """

        log(str)
        # self._print_logs.append(str + "\n")
        # self._flush_()

# pba = process_status_bar()
# for i in pba.iter_bar([xx for xx in range(20)], key='ddd'):
#     log("dd")
# pass
