# pass_generate
from tketool.pyml.pytrainer import *
from tketool.pyml.trainbase import *
import os, pickle
from tketool.logs import log


class log_plugin(trainer_plugin_base):
    """
    `log_plugin` 是一个继承自`trainer_plugin_base`的类。这个类的主要目的是在训练过程中进行日志记录，包括在每一个批次和每一个训练周期开始和结束的时候。
    
    这个类的主要功能如下：
    - 在训练开始时，创建日志文件并设置文件路径。
    - 在每一个训练周期和批次开始时，记录堆栈中的日志信息。
    - 在每一个训练周期和批次结束时，记录训练的损失并清空堆栈中的日志信息。
    - 在训练结束时，将堆栈中的日志信息写入到日志文件中。
    
    使用这个类的例子如下：
    ```python
    logger = log_plugin(show_in_batch=True, show_in_epoch=True)
    logger.start(global_state, epoch_state, step_state)
    # 在训练过程中，可以使用下面的方法记录日志信息
    logger._log("Training started.")
    # 在训练结束时，使用下面的方法将日志信息写入到文件中
    logger.end(global_state, epoch_state, step_state)
    ```
    
    类方法：
    - `__init__(self, show_in_batch=False, show_in_epoch=True)`: 构造函数，初始化类的实例。
    - `start(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board)`: 在训练开始时调用，设置日志文件的路径。
    - `end(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board)`: 在训练结束时调用，将堆栈中的日志信息写入到日志文件中。
    - `epoch_begin(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board)`: 在每一个训练周期开始时调用，记录堆栈中的日志信息。
    - `epoch_end(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board)`: 在每一个训练周期结束时调用，记录训练的损失并清空堆栈中的日志信息。
    - `batch_begin(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board)`: 在每一个批次开始时调用，记录堆栈中的日志信息。
    - `batch_end(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board)`: 在每一个批次结束时调用，记录训练的损失并清空堆栈中的日志信息。
    
    注意：
    - 需要保证`global_state_board`, `epoch_state_board`和`step_state_board`已经被正确初始化。
    """

    def Invoke(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        """
        log_plugin类是一个用于记录训练过程的插件类。 它可以在训练开始，结束，每个epoch开始和结束，每个batch开始和结束时记录和输出训练信息。该类继承自trainer_plugin_base。用户可以通过设置show_in_batch和show_in_epoch来决定是否在每个batch或者epoch中输出训练信息。
        
        使用例子如下:
        
        log = log_plugin(show_in_batch=True, show_in_epoch=True)
        log.start(global_state, epoch_state, step_state)
        log.batch_begin(global_state, epoch_state, step_state)
        log.batch_end(global_state, epoch_state, step_state)
        log.epoch_begin(global_state, epoch_state, step_state)
        log.epoch_end(global_state, epoch_state, step_state)
        log.end(global_state, epoch_state, step_state)
        
        def Invoke(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        
            此函数是log_plugin类中的一个函数，它并没有具体的实现。这是一个抽象方法，需要在子类中重写。这个方法的目的是为了实现在训练过程中的某些特定时刻进行一些操作，比如在每个epoch开始时记录当前的loss值等。
        
            参数:
            global_state: global_state_board类型，表示全局状态，包含整个训练过程的信息，如模型保存的位置，训练的进度条等。
            epoch_state: epoch_state_board类型，表示在当前epoch的状态，包含当前epoch的索引，当前epoch的loss值等。
            step_state: step_state_board类型，表示在当前step的状态，包含当前step的索引，当前step的loss值等。
        
            返回值: 无
        
            注意: 由于这个函数在父类中没有具体的实现，所以如果在子类中没有重写这个函数，而又调用了这个函数的话，程序会报错。
        
        """

        pass

    def _log(self, content):
        """
        _log是一个私有方法，用于记录内容到日志文件中。
        
        方法将接收的参数content追加到指定的日志文件中。如果日志文件不存在，会创建一个新的。
        
        参数：
            content (str)：需要记录到日志文件中的内容。
        
        返回：
            无
        
        例子：
            下方是一个使用示例。创建一个log_plugin对象，然后调用_log方法记录内容到日志文件。
            ```
            log_plugin_obj = log_plugin()
            log_plugin_obj._log("This is a log message")
            ```
        注意：
            - 这个方法不应该直接调用，它是一个内部方法，用于log_plugin类内部
            - 这个方法没有返回值，它的作用是副作用，即写入文件。
        """

        log(content)
        # 打开文件，如果文件不存在，则创建
        with open(self.save_file, "a") as log_file:  # 'a' 表示 append mode，即增量方式
            log_file.write(content + "\n")

    def _log_stackcontent(self, global_state: global_state_board):
        """
            这个方法的主要目的是将全局状态(global_state)中的日志堆栈内的所有消息进行日志记录，然后清空日志堆栈。
        
            参数:
            global_state (global_state_board): 训练过程的全局状态，包含训练的各种信息和状态，如日志堆栈。
        
            返回:
            无
        
            注意这个方法没有返回值，但是会改变全局状态(global_state)中的日志堆栈，完成日志记录后会清空日志堆栈。
        
            示例：
        
            # 创建log_plugin对象
            log_plugin_obj = log_plugin()
        
            # 假设我们已经有了一个global_state对象
            global_state = global_state_board()
        
            # 在某一步骤添加日志信息到global_state的日志堆栈中
            global_state.log_stack.append("Step 1 completed.")
        
            # 调用_log_stackcontent方法进行日志记录
            log_plugin_obj._log_stackcontent(global_state)
        
            # 此时，"Step 1 completed."已经被记录到日志文件中，global_state中的日志堆栈已经被清空。
        """

        for message in global_state.log_stack:
            self._log(message)
        global_state.log_stack.clear()

    @invoke_at([plugin_invoke_Enum.Begin])
    def start(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        """
            在训练开始时调用的方法。
        
            该方法在训练开始时被调用。主要作用是设定日志文件的保存路径。日志文件将保存在模型文件夹下，文件名为"log.txt"。
        
            参数:
                global_state (global_state_board): 全局状态板，记录全局的训练状态，如模型文件夹路径等。
                epoch_state (epoch_state_board): 该训练周期的状态板，记录了该训练周期的相关信息。
                step_state (step_state_board): 当前训练步骤的状态板，记录了当前训练步骤的相关信息。
        
            返回:
                无返回值。
        
            注意:
                该方法不应该被直接调用，而应该作为训练插件在训练过程中的一个生命周期进行调用。
        """

        self.save_file = os.path.join(global_state.model_folder, "log.txt")

    @invoke_at([plugin_invoke_Enum.End])
    def end(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        """
        这是一个`end`方法，它是`log_plugin`类的一部分，该类是trainer_plugin_base的子类。该方法在训练的最后阶段被调用，用于输出并清空global_state的日志堆栈。
        
        参数：
        - `global_state` (`global_state_board`): 全局状态板，包含全局的状态信息，如模型、优化器等。
        - `epoch_state` (`epoch_state_board`): 当前训练周期状态板，包含当前周期的状态信息，如当前周期的损失值、准确率等。
        - `step_state` (`step_state_board`): 当前步骤状态板，包含当前步骤的状态信息，如当前步骤的损失值、准确率等。
        
        返回值：
        该函数没有返回值。
        
        示例：
        
        ```python
            def end(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
                self._log_stackcontent(global_state)
        ```
        
        注意：
        - `_log_stackcontent`是`log_plugin`类的一个私有方法，它会输出并清空global_state的日志堆栈。
        """

        self._log_stackcontent(global_state)

    @invoke_at([plugin_invoke_Enum.Epoch_begin])
    def epoch_begin(self, global_state: global_state_board, epoch_state: epoch_state_board,
                    step_state: step_state_board):
        """
        `epoch_begin`是`log_plugin`类的一个方法，该方法在每个训练周期开始时被调用。它执行的主要操作是记录全局状态中的日志信息。log_plugin类主要用于在训练过程中实现日志记录功能，通过记录每一个epoch和batch的开始和结束状态，以及在这些状态下模型的损失值，帮助用户了解模型训练过程中的情况。
        
        参数:
        - `global_state` (`global_state_board`类型): 训练过程中的全局状态，包含所有插件需要访问的全局信息。
        - `epoch_state` (`epoch_state_board`类型): 当前训练周期的状态信息，包括当前的训练周期数、训练周期损失等。
        - `step_state` (`step_state_board`类型): 当前步骤的状态信息，包括当前步骤数、步骤损失等。
        
        无返回值。
        
        示例:
        
        假设我们正在训练一个模型，该模型的训练过程由一个log_plugin实例来监控和记录，那么在每个训练周期开始时，就会调用这个`epoch_begin`方法：
        
        ```python
        log = log_plugin()
        log.epoch_begin(global_state, epoch_state, step_state)
        ```
        
        在这个方法中，首先会清空`global_state`的日志堆栈，并将堆栈中的每一条消息记录到日志文件中。这样就可以在每个训练周期开始时，清空上一个训练周期的日志信息，并记录新的训练周期的日志信息。
        """

        self._log_stackcontent(global_state)

    @invoke_at([plugin_invoke_Enum.Epoch_end])
    def epoch_end(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        """
        `epoch_end` 是 `log_plugin` 类的一个方法，用于处理每个训练周期结束后的逻辑。
        
        此方法主要用于记录和保存训练周期结束时的状态信息，如损失值，并将这些信息写入日志文件中。此外，此方法还会清空全局状态的日志栈，以准备下一次的训练周期。
        
        参数：
        - `global_state` (`global_state_board` 类型): 全局状态板，用于存储全局的状态信息。
        - `epoch_state` (`epoch_state_board` 类型): 训练周期状态板，用于存储当前训练周期的状态信息。
        - `step_state` (`step_state_board` 类型): 训练步骤状态板，用于存储当前训练步骤的状态信息。
        
        返回值：
        - 此方法没有返回值。
        
        注意：
        - 此方法被 `invoke_at` 装饰器修饰，会在每个训练周期结束时被调用。
        
        示例：
        ```python
        # 创建 log_plugin 对象
        log_plugin = log_plugin()
        
        # 创建全局状态板、训练周期状态板和训练步骤状态板
        global_state = global_state_board()
        epoch_state = epoch_state_board()
        step_state = step_state_board()
        
        # 训练周期结束，调用 epoch_end 方法
        log_plugin.epoch_end(global_state, epoch_state, step_state)
        ```
        """

        if self.show_in_epoch:
            pb = global_state.progress_bar  # base_wall["pb"]
            epoch = epoch_state.epoch_idx  # epoch_wall['current_epoch_idx']
            loss = epoch_state.epoch_loss  # epoch_wall['epoch_loss']
            self._log(f"Epoch [{epoch + 1}], Total Loss: {loss:.4f}")
        self._log_stackcontent(global_state)

    @invoke_at([plugin_invoke_Enum.Batch_begin])
    def batch_begin(self, global_state: global_state_board, epoch_state: epoch_state_board,
                    step_state: step_state_board):
        """
        这是一个在批处理开始前执行的函数,功能是记录全局状态的日志。
        它的参数包括全局状态、当前的epoch状态和step状态。
        
        参数:
            global_state(global_state_board): 存储全局状态信息的对象
            epoch_state(epoch_state_board): 存储当前epoch状态信息的对象
            step_state(step_state_board): 存储步骤状态信息的对象
        
        返回:
            无返回值
        """

        self._log_stackcontent(global_state)

    @invoke_at([plugin_invoke_Enum.Batch_end])
    def batch_end(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        """
            在一次训练批次结束时会调用这个方法。用于记录该批次的训练情况，并将记录写入日志文件。
        
            参数:
            global_state: global_state_board类型，代表全局状态，包含了全局信息如模型、数据等。
            epoch_state: epoch_state_board类型，代表当前的训练周期状态，包含了当前训练周期的信息。
            step_state: step_state_board类型，代表当前训练步骤的状态，包含了当前步骤的信息。
        
            返回值:
            无
        
            使用示例:
            ```python
            log_plugin.batch_end(global_state, epoch_state, step_state)
            ```
        
            注意事项:
            本方法没有返回值，主要功能是记录日志。
        
        """

        if self.show_in_batch:
            pb = global_state.progress_bar  # base_wall["pb"]
            batch = step_state.batch_idx
            loss = step_state.loss_value  # epoch_wall['epoch_loss']
            self._log(f"Batch [{batch + 1}], Total Loss: {loss:.4f}")
        self._log_stackcontent(global_state)

    def __init__(self, show_in_batch=False, show_in_epoch=True):
        """
        初始化log_plugin类。 这是一个用于训练过程中记录日志的插件，可以设定是否在每个batch和epoch开始和结束时记录日志。
        
        参数:
            show_in_batch(可选): 布尔值，如果为True，则在每个batch开始和结束时记录日志。 默认为False。
            show_in_epoch(可选): 布尔值，如果为True，则在每个epoch开始和结束时记录日志。 默认为True。
        
        属性:
            save_file: 用于保存日志的文件的路径，具体路径在start函数中由global_state.model_folder指定。
            show_in_batch: 是否在每个batch开始和结束时记录日志。
            show_in_epoch: 是否在每个epoch开始和结束时记录日志。
        
        例子:
            log_plugin = log_plugin(show_in_batch=True, show_in_epoch=False)
            在开始和结束每个batch时将日志记录在文件中，但是不在epoch开始和结束时记录。
        
        """

        self.save_file = None
        self.show_in_batch = show_in_batch
        self.show_in_epoch = show_in_epoch
