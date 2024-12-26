# pass_generate
from tketool.pyml.pytrainer import *
from tketool.logs import log, print_table
import numpy as np
import os, pickle


class grad_log(trainer_plugin_base):
    """
    这个类是`grad_log`，它是`trainer_plugin_base`的子类，这个类用于在训练过程中检查模型参数的梯度，以便于调试和监控模型的训练过程。
    
    主要的功能和用法如下：
    
    1. 在训练开始（`Invoke2`）和每个batch结束后（`Invoke`），检查模型的参数，如果参数的绝对值超过设定的阈值，就用`_format_table`函数将参数的信息格式化后记录下来。
    
    2. `_format_table`函数会将参数的信息（包括形状、最小值、最大值等）格式化为字符串，方便后续查看。
    
    使用示例：
    
    ```python
    logger = grad_log(batch_check_freq=10)
    trainer.add_plugin(logger)
    trainer.train()
    ```
    
    初始化的参数：
    
    - `init_model_check`：是否在训练开始时检查模型参数，默认为True。
    - `batch_check_freq`：每几个batch检查一次模型参数，默认为3。
    - `check_fp16`：是否检查16位浮点数，默认为True。
    - `warning_level`：设置梯度的警告级别，默认为1。
    
    函数：
    
    - `__init__`：初始化函数，设置一些参数和阈值。
    - `_in_range`：检查值是否在设定的范围内。
    - `_format_table`：格式化参数的信息。
    - `Invoke2`：在训练开始时调用，检查模型参数。
    - `Invoke`：在batch结束后调用，检查模型参数。
    
    注意：
    
    这个类没有返回值，主要用于在训练过程中打印和记录参数信息。
    """

    def __init__(self, init_model_check=True, batch_check_freq=3, check_fp16=True, warning_level=1):
        """
        初始化 grad_log 类实例。
        
        grad_log 是一个用于检查 model 的参数和梯度值是否在安全范围内的 trainer 插件。如果参数或梯度值超出范围，将以指定的警告级别打印警告。该类可帮助我们了解模型训练过程中参数和梯度的变化情况，以便调整学习率等超参数，优化模型训练过程。
        
        参数:
            init_model_check (bool): 是否在训练开始时检查模型的初始参数值，默认为 True。
            batch_check_freq (int): 每隔几个 batch 检查一次参数和梯度值，默认为 3。
            check_fp16 (bool): 是否检查半精度浮点数 (float16) 的参数和梯度值，默认为 True。如果为 False，将检查单精度浮点数 (float32)。
            warning_level (int): 警告级别，默认为 1。级别越高，安全范围越小，警告越频繁。
        
        使用示例:
        ```python
        from trainer_plugin_base import trainer_plugin_base
        
        class my_trainer(trainer_plugin_base):
            def __init__(self):
                super().__init__()
                self.plugin = grad_log(init_model_check=True, batch_check_freq=1, check_fp16=False, warning_level=2)
        ```
        在这个示例中，我们初始化了一个 my_trainer 类，它继承了 trainer_plugin_base 并使用 grad_log 插件。在每个 batch 训练结束后，都将检查模型的参数和梯度值，并以较高的警告级别打印警告。我们不检查 float16 参数，只检查 float32 参数。
        """

        self.freq = 0
        self.per_batch = batch_check_freq
        if check_fp16:
            self.check_max = np.finfo(np.float16).max / (10 ** warning_level)
            self.check_min = np.finfo(np.float16).tiny * (10 ** warning_level)
        else:
            self.check_max = np.finfo(np.float32).max / (10 ** warning_level)
            self.check_min = np.finfo(np.float32).tiny * (10 ** warning_level)

        self.check_model = init_model_check

    def _in_range(self, *values):
        """
        这是一个工具函数，它接受一个或多个值作为输入，并检查这些值是否在预先定义的范围内。
        这个函数的主要目的是在梯度下降训练过程中，对模型参数和梯度进行检查，以确保它们没有超出浮点数可以表示的范围，防止因溢出等问题导致的训练失败。
        
        参数:
            *values (float): 一个或多个需要检查的浮点数值。
        
        返回:
            bool: 如果所有输入值都在预定义的范围内，返回True；否则返回False。
        
        使用示例:
            ```python
            check_result = self._in_range(max_value, min_value)
            if not check_result:
                # 如果检查失败，打印警告信息或进行其他处理
                print("Warning: some values are out of range.")
            ```
        注意：这个函数不会对输入值进行任何修改或处理，只进行范围检查。
        """

        for value in values:
            if abs(value) > self.check_max:
                return False
            elif value != 0 and abs(value) < self.check_min:
                return False
        return True

    def _format_table(self, row_data):
        """
        这是一个私有方法，用于格式化表格中的每一行数据。方法首先遍历每个单元格数据，判断该数据的类型，如果数据是浮点型，它会首先检查该数据是否在预设范围内，如果在范围内，精确到小数点后八位，否则，将其标记为异常值（以 "**" 包围）。如果数据是列表类型，则将每个元素转换为字符串，并用逗号连接。如果数据类型既不是浮点型也不是列表类型，则直接将该数据转换为字符串。
        
        参数:
            row_data: 数据列表，包含要格式化的行数据。
        
        返回:
            formatted_row: 格式化后的行数据列表。
        
        例子:
            假设_row_data = [123.456789, [1,2,3], "测试"]
            经过_format_table方法处理后，得到formatted_row = ['123.45678900', '1,2,3', '测试']
        
        注意:
            这个方法主要被类方法Invoke和Invoke2使用，而不应该直接被调用。
        """

        formatted_row = []
        for cell in row_data:
            if isinstance(cell, float):
                # If it's a float, format it to have 4 decimal places.
                if self._in_range(cell):
                    formatted_row.append("{:.8f}".format(cell))
                else:
                    formatted_row.append("**{:.8f}**".format(cell))
            elif isinstance(cell, list):
                # If it's a list of integers, convert each integer to string and join them with commas.
                formatted_row.append(','.join(str(x) for x in cell))
            else:
                # Otherwise, just convert the value to string.
                formatted_row.append(str(cell))

        return formatted_row

    @invoke_at([plugin_invoke_Enum.Begin])
    def Invoke2(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        """
        `Invoke2` 是 `grad_log` 类的一个方法，它在训练过程中的某个指定时点被调用。其主要目的是检查模型中各个参数的值是否在合理范围内，并将那些超出范围的参数进行记录和显示。
        
        该方法接收三个参数，分别为 `global_state`，`epoch_state`，和 `step_state`。
        
        参数：
        - `global_state` (类型：global_state_board)：一个存储全局状态的对象，包括了整个训练过程的相关信息，例如模型参数、优化器状态等。
        - `epoch_state` (类型：epoch_state_board)：一个存储当前训练轮次(epoch)状态的对象，包括了当前轮次的相关信息，例如当前轮次的训练损失、准确率等。
        - `step_state` (类型：step_state_board)：一个存储当前训练步骤(step)状态的对象，包括了当前步骤的相关信息，例如当前步骤的训练损失、梯度值等。
        
        返回值：
        - 此方法无返回值。
        
        在执行过程中，该方法首先检查每个需要进行梯度更新的模型参数，计算其均值、方差、最大值和最小值。然后判断这些值是否在设定的阈值范围内。如果参数值超出范围，则将该参数的名称、形状、最小值、最大值、均值、方差等信息添加到`rows`列表中。最后，如果`rows`列表不为空，即存在参数值超出范围的情况，则调用`print_table`函数，将这些信息以表格的形式打印出来。
        
        注意：这个方法并不会改变模型参数的值，只是进行检查并输出超出范围的参数信息。如果希望在参数值超出范围时进行某种处理，需要在这个方法中添加相应的代码。
        """

        if self.check_model is False:
            return

        rows = []

        for name, param_model in global_state.model.named_parameters():
            if param_model.requires_grad is False:
                continue

            mean_value = param_model.data.mean().item()
            variance_value = param_model.data.var().item()
            max_value = param_model.data.max().item()
            mini_value = param_model.data.min().item()
            shape = list(param_model.data.size())

            if not self._in_range(max_value, mini_value):
                rows.append(self._format_table([name, shape, mini_value, max_value, mean_value, variance_value]))

        if len(rows) > 0:
            print_table(['name', 'shape', 'min_value', 'max_value', 'mean', 'var'], rows)

        # log_str = (f"name: {name} ({param_model.data.shape}): "
        #            f"value: [{param_model.data.min().item()}, {param_model.data.max().item()}] "
        #            f"grad: [{param_model.grad.min().item() if param_model.grad is not None else 0}, "
        #            f"{param_model.grad.max().item() if param_model.grad is not None else 0}]"
        #            f"mean: {mean_value} "
        #            f"variance: {variance_value}")
        # log(log_str)

    @invoke_at([plugin_invoke_Enum.Batch_end])
    def Invoke(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        """
        这是一个触发方法，用于在每个训练批次结束时进行调用。该方法主要用于检查模型参数的梯度，包括梯度的最大值、最小值等。如果检测到的梯度值超出预定义的范围，该方法将对梯度值进行格式化并打印出来。
        
        参数:
        - global_state(global_state_board): 全局状态板，包含模型的全局状态信息，如模型的参数、优化器等。
        - epoch_state(epoch_state_board): epoch状态板，包含当前epoch的状态信息，如当前epoch的损失值、准确率等。
        - step_state(step_state_board): step状态板，包含当前step的状态信息，如当前step的损失值、准确率等。
        
        无返回值。
        
        其中一段代码示例如下：
        ```python
        for group in global_state.optimizer.param_groups:
            for param_tensor in group['params']:
                max_value = param_tensor.data.max().item()
                mini_value = param_tensor.data.min().item()
                shape = list(param_tensor.data.size())
                grad_mini = param_tensor.grad.min().item() if param_tensor.grad is not None else 0
                grad_max = param_tensor.grad.max().item() if param_tensor.grad is not None else 0
                if not self._in_range(max_value, mini_value, grad_mini, grad_max):
                    rows.append(self._format_table([shape, mini_value, max_value, grad_mini, grad_max]))
        ```
        以上代码遍历优化器的参数组，对每一个参数张量，计算其数据的最大值、最小值以及梯度的最大值、最小值，然后判断这些值是否在允许的范围内，如果不在，则将这些值进行格式化并添加到rows列表中。
        
        此方法没有已知的错误或bug。
        """

        self.freq += 1
        if self.freq < self.per_batch:
            return
        else:
            self.freq = 0

        rows = []
        for group in global_state.optimizer.param_groups:
            for param_tensor in group['params']:
                max_value = param_tensor.data.max().item()
                mini_value = param_tensor.data.min().item()
                shape = list(param_tensor.data.size())
                grad_mini = param_tensor.grad.min().item() if param_tensor.grad is not None else 0
                grad_max = param_tensor.grad.max().item() if param_tensor.grad is not None else 0

                if not self._in_range(max_value, mini_value, grad_mini, grad_max):
                    rows.append(self._format_table([shape, mini_value, max_value, grad_mini, grad_max]))

        if len(rows) > 0:
            print_table(['shape', 'min_value', 'max_value', 'grad_mini', 'grad_max'], rows)
