# pass_generate
from enum import Enum
import time, abc
import functools


class plugin_invoke_Enum(Enum):
    """
    `plugin_invoke_Enum` 是一个Python枚举类，用于表示插件调用的不同状态。
    
    这个枚举类定义了8个成员：
    
    - `Never`: 表示插件从未被调用。
    - `Epoch_begin`: 表示在数据训练的每个epoch开始时调用插件。
    - `Epoch_end`: 表示在数据训练的每个epoch结束时调用插件。
    - `Batch_begin`: 表示在数据训练的每个batch开始时调用插件。
    - `Batch_end`: 表示在数据训练的每个batch结束时调用插件。
    - `Begin`: 表示在插件的执行开始时。
    - `End`: 表示在插件的执行结束时。
    - `After_Backward`: 表示在反向传播之后调用插件。
    - `Update`: 表示在更新训练模型参数时调用插件。
    
    每个枚举成员都与一个整数值关联，这些值默认从0开始。
    
    例如：
    ```python
    print(plugin_invoke_Enum.Epoch_begin)  # 输出: Epoch_begin
    print(plugin_invoke_Enum.Epoch_begin.value)  # 输出: 1
    ```
    注意：Python的枚举类是不可变的，因此不能给枚举成员赋值。
    
    目前未发现此类存在错误或BUG。
    """

    Never = 0
    Epoch_begin = 1
    Epoch_end = 2
    Batch_begin = 3
    Batch_end = 4
    Begin = 5
    End = 6
    After_Backward = 7
    Update = 8


class device_use_enum(Enum):
    """
    这是一个名为device_use_enum的类，此类继承自Enum枚举类。该类的主要目的是定义设备使用方式的枚举类型。设备使用方式可以是自动（Auto）或者是CPU（CPU）。
    
    在使用这个枚举类时，可以直接通过类名调用枚举值，例如：
    
    ```python
    device = device_use_enum.Auto
    if device == device_use_enum.Auto:
        print("Device is set to Auto")
    ```
    
    请注意，这个类没有明显的错误或bug，但是当需要定义更多设备使用方式时，需要在类内部添加。
    """

    Auto = 1
    CPU = 2


class dtype_enum(Enum):
    """
    这是一个枚举类`dtype_enum`，它提供了一种枚举数据类型的方法，为不同的数据类型提供了枚举值。枚举值对应的是不同的数据类型，如自动类型、BF16类型、FP16类型、Float32类型等。
    
    它主要用于标记和识别不同的数据类型，并可以在代码中方便的引用和比较。
    
    示例：
    ```python
    def process_data(data, dtype):
        if dtype == dtype_enum.Auto:
            # do something
        elif dtype == dtype_enum.BF16:
            # do something
        elif dtype == dtype_enum.FP16:
            # do something
        elif dtype == dtype_enum.Float32:
            # do something
    ```
    
    该类没有发现明显的错误或者bug。
    """

    Auto = 1
    BF16 = 2
    FP16 = 3
    Float32 = 4


class update_mode_enum(Enum):
    """
    这是一个枚举类update_mode_enum，它是枚举（Enum）类的子类。该类定义了两种更新模式：“Per_Step”和“Per_Epoch”，分别对应数值1和2。这种设计通常用于表示不同的更新策略或模式，使得代码更具可读性和维护性。在调用或使用这个枚举类时，可以使用update_mode_enum.Per_Step或update_mode_enum.Per_Epoch来表示不同的更新模式。
    
    例如：
    在某神经网络的训练过程中，我们可以根据需要选择不同的更新模式：
    
    ```
    if update_mode == update_mode_enum.Per_Step:
        # 每一步都更新模型参数
        model.update()
    elif update_mode == update_mode_enum.Per_Epoch:
        # 每一个epoch结束后更新模型参数
        model.update()
    ```
    
    这样一来，通过使用本枚举类，我们的代码变得更易于理解和维护。
    """

    Per_Step = 1,
    Per_Epoch = 2,


class global_state_board():
    """
    这是一个名为`global_state_board`的类，该类的主要作用是在训练过程中进行全局状态的记录和管理。
    
    类的初始化函数需要接收的参数包括：
    - train_obj：训练对象，包含训练所需要的模型、损失函数、优化器等信息。
    - epoch_count：训练迭代的次数。
    - sample_set：训练集样本。
    - pb：进度条对象，用于展示训练进度。
    - input_convert_func：输入转换函数，用于处理输入数据。
    - label_convert_func：标签转换函数，用于处理标签数据。
    
    此外，该类还提供了`log`方法，用于将日志信息添加到`log_stack`列表中。
    
    示例：
    ```python
    # 创建训练对象
    trainer = SomeTrainer(model, loss, optimizer, out_folder)
    # 创建全局状态记录板对象
    gsb = global_state_board(trainer, epoch_count, sample_set, progress_bar, input_convert_func, label_convert_func)
    # 添加日志
    gsb.log('Start training...')
    ```
    
    注意：类的使用应在训练流程的控制和管理上下文中，确保提供的训练对象和数据集等信息正确无误。
    """

    def __init__(self, train_obj, epoch_count, sample_set, pb, input_convert_func, label_convert_func):
        """
        `global_state_board`是一个类，它用于记录和管理训练过程的全局状态信息。
        
        类初始化方法如下:
        
        __init__(self, train_obj, epoch_count, sample_set, pb, input_convert_func, label_convert_func):
        
        参数:
        
        train_obj: 训练对象，通常包含了模型、损失函数等信息。
        
        epoch_count: 训练的轮数。
        
        sample_set: 训练样本集。
        
        pb: 进度条对象，用于在训练过程中显示训练进度。
        
        input_convert_func: 输入转换函数，用于将原始输入数据转换为适合模型训练的格式。
        
        label_convert_func: 标签转换函数，用于将原始标签数据转换为适合模型训练的格式。
        
        该类的主要目标是在训练过程中收集和保存训练状态，包括训练对象的类型、模型、损失函数、优化器、训练的轮数、训练样本集、更新模式、进度条、输入和标签的转换函数等。同时，该类也负责记录训练日志、参数更新次数、插件数据、图表数据以及训练开始的时间。
        
        示例:
        
        ```
        # 创建一个训练对象
        train_obj = Trainer(model, loss, optimizer, out_folder)
        
        # 设置训练轮数
        epoch_count = 100
        
        # 创建训练样本集
        sample_set = SampleSet(data, labels)
        
        # 创建进度条对象
        pb = ProgressBar()
        
        # 定义输入转换函数
        def input_convert_func(input_data):
            return input_data.reshape(-1, 1)
        
        # 定义标签转换函数
        def label_convert_func(label_data):
            return label_data.reshape(-1, 1)
        
        # 创建global_state_board对象
        gsb = global_state_board(train_obj, epoch_count, sample_set, pb, input_convert_func, label_convert_func)
        ```
        """

        self.trainer_type_name = type(train_obj).__name__
        self.trainer = train_obj
        self.model = train_obj.model
        self.loss_obj = train_obj.loss
        self.optimizer = train_obj.optimizer
        self.model_folder = train_obj.out_folder
        self.epoch_count = epoch_count
        self.sample_set = sample_set
        self.update_mode = train_obj.update_mode
        self.progress_bar = pb
        self.input_convert_func = input_convert_func
        self.label_convert_func = label_convert_func

        self.batch_count = sample_set.count()

        self.update_parameter_count = -1

        self.log_stack = []
        self.parameter_update_times = 0

        self.plugin_datas = {}
        self.chart_datas = {}
        self.step = 0

        self.start_time = time.time()

    def log(self, lg_s):
        """
            `log`是`global_state_board`类的一个方法.
        
            使用这个方法可以将日志信息添加到`log_stack`属性中. `log_stack`是一个列表,用于存储所有的日志信息. 当调用`log`方法时,传入的日志信息将被添加到列表的尾部.
        
            参数:
        
            - `self`: 是指向类实例的引用. 在Python中,它是所有实例方法的第一个参数.
        
            - `lg_s`: 一个字符串类型的参数,它代表了要添加到`log_stack`的日志信息.
        
            返回值:
        
            - 这个方法没有返回值.
        
            用法:
        
            下面是一个使用`log`方法的例子.
        
            ```python
            board = global_state_board(...)
            board.log("Training started")
            ```
        
            在这个例子中,我们创建了一个`global_state_board`的实例,然后使用`log`方法添加了一条日志信息"Training started".
        
            注意:
        
            - 这个方法没有做任何的错误检查,所以当传入的`lg_s`不是字符串时,程序可能会崩溃.
        """

        self.log_stack.append(lg_s)


class epoch_state_board():
    """
    这是一个名为`epoch_state_board`的类，用于在训练神经网络时追踪和记录每个训练周期(epoch)的状态。
    
    每个`epoch_state_board`对象代表一个训练周期，它包含以下属性:
    
    - `epoch_idx`: 训练周期的索引值。
    
    - `epoch_loss`: 该训练周期的损失值。
    
    - `start_time`: 该训练周期的开始时间，表示为Unix时间戳。
    
    - `end_time`: 该训练周期的结束时间，表示为Unix时间戳。
    
    - `plugin_datas`: 一个字典，用于存储插件数据，键是插件名称，值是插件返回的任何数据。
    
    在每个训练周期开始时，会创建一个新的`epoch_state_board`对象，然后在训练过程中更新其属性。
    
    该类的主要目的是提供一种方便的方式来记录和访问训练信息，这样可以在训练过程中方便地进行调试和分析。
    
    示例用法如下：
    
    ```python
    # 假设我现在是在第5个训练周期
    epoch_board = epoch_state_board(5)
    
    # 在训练过程中，我可以不断更新损失值
    epoch_board.epoch_loss += loss_value
    
    # 当训练周期结束时，我可以记录结束时间
    epoch_board.end_time = time.time()
    
    # 我也可以通过`plugin_datas`属性记录其他信息，如准确率
    epoch_board.plugin_datas['accuracy'] = calculate_accuracy()
    
    # 在后续的代码中，我可以通过`epoch_board`对象来获取训练信息
    print(f"Epoch {epoch_board.epoch_idx} loss: {epoch_board.epoch_loss}")
    ```
    """

    def __init__(self, epoch_idx):
        """
        `epoch_state_board`类用于管理和跟踪每个训练周期(称为"epoch")的状态。它记录了训练周期的索引、该周期的损失函数值、训练开始和结束的时间以及相关的插件数据。
        
        类参数:
        
        - `epoch_idx`：该训练周期的索引（也就是编号）。
        
        类属性:
        
        - `epoch_idx`：存储传入的`epoch_idx`参数，表示当前训练周期的索引。
        - `epoch_loss`：在每个训练周期开始时，初始化为0，用于累积计算训练周期的总损失。
        - `start_time`：训练周期开始的时间，使用`time.time()`获取当前时间。
        - `end_time`：训练周期结束的时间，初始化为0。
        - `plugin_datas`：一个用于存储插件数据的字典，初始化为空。
        
        使用示例：
        
        ```python
        # 创建一个`epoch_state_board`对象，传入训练周期的索引作为参数
        epoch_status = epoch_state_board(epoch_idx=1)
        
        # 在训练周期中，可以通过`epoch_status.epoch_loss`来累积损失值
        for data in train_data:
            loss = train_step(data)
            epoch_status.epoch_loss += loss
        
        # 在训练周期结束后，可以通过`epoch_status.end_time`来设置结束时间
        epoch_status.end_time = time.time()
        ```
        
        注意：目前没有发现代码中存在的错误或bug。
        """

        self.epoch_idx = epoch_idx
        self.epoch_loss = 0
        self.start_time = time.time()
        self.end_time = 0

        self.plugin_datas = {}


class step_state_board():
    """
    `step_state_board`类是一个用于记录并跟踪训练过程中每一步的状态的类。这个类可以用来为每个训练步骤保存相关的信息，例如开始和结束时间、损失值等。这些信息有助于进一步的分析和调试。
    
    该类的属性包括：
    - batch_idx：当前批次的索引
    - ori_item：原始的批次数据
    - start_time：当前步骤开始的时间
    - end_time：当前步骤结束的时间
    - converted_input：转换后的输入数据，由`global_state.input_convert_func(batch_item)`得到
    - converted_label：转换后的标签数据，由`global_state.label_convert_func(batch_item)`得到
    - logit：预测的输出
    - loss_value：当前步骤的损失值
    - loss_tensor：当前步骤的损失张量
    - plugin_datas：插件数据，用于保存额外的信息
    
    使用方式如下：
    
    ```python
    global_state = some_global_state_board()  # 初始化一个全局状态
    for i, data in enumerate(dataloader):
        step_state = step_state_board(i, data, global_state)  # 创建步骤状态板
        ...
        # 在训练过程中更新步骤状态板的信息
        step_state.end_time = time.time()
        step_state.loss_value = some_loss
        ...
    ```
    
    注意，`converted_input`和`converted_label`的值应由`global_state.input_convert_func(batch_item)`和`global_state.label_convert_func(batch_item)`得到，但在`__init__`方法中并未被赋值，需要在后续的训练过程中手动赋值。
    """

    def __init__(self, batch_idx, batch_item, global_state: global_state_board):
        """
        类 `step_state_board` 是一个用于描述批处理状态的类。它用于跟踪批处理中的各种信息，如批处理索引、原始项目、开始和结束时间、转换后的输入和标签、日志、损失值、损失张量和插件数据等。
        
        类的使用示例：
        
        ```python
        # 初始化一个全局状态
        global_state = global_state_board()
        # 初始化一个批处理状态
        batch_state = step_state_board(batch_idx=0, batch_item=data, global_state=global_state)
        ```
        
        构造函数 `__init__` 的参数：
        
        - `batch_idx` : int 类型，批处理的索引。
        - `batch_item` : 数据类型不限，是批处理的原始数据项。
        - `global_state` : global_state_board 类型，描述全局的状态。
        
        构造函数 __init__ 不返回任何值，它的目的是初始化 `step_state_board` 类的实例。
        
        注意：目前函数里的 `global_state.input_convert_func(batch_item)` 和 `global_state.label_convert_func(batch_item)` 两行代码被注释掉了，可能会影响 `self.converted_input` 和 `self.converted_label` 的赋值，需要根据实际情况决定是否启用这两行代码。
        """

        self.batch_idx = batch_idx
        self.ori_item = batch_item
        self.start_time = time.time()
        self.end_time = 0
        self.converted_input = None  # global_state.input_convert_func(batch_item)
        self.converted_label = None  # global_state.label_convert_func(batch_item)
        self.logit = []
        self.loss_value = 0.0
        self.loss_tensor = None
        self.plugin_datas = {}


def invoke_at(types: [plugin_invoke_Enum]):
    """
    此函数是一个装饰器生成器，用于为函数添加一个特殊属性 _invoke_at，以便后续在特定的插件调用时识别和处理。
    
    参数:
    types (list): 包含plugin_invoke_Enum枚举类的列表，用于指示函数在哪些类型的插件调用时被触发。
    
    返回:
    返回一个装饰器，这个装饰器可以被用于装饰其他函数，给他们附加_invoke_at属性。
    
    使用示例:
    
    @invoke_at([plugin_invoke_Enum.Type1, plugin_invoke_Enum.Type2])
    def some_function():
        pass
    上述代码会给 some_function 函数附加一个属性_invoke_at，其值为[plugin_invoke_Enum.Type1, plugin_invoke_Enum.Type2]。
    
    注意事项:
    - 请确保 types 列表中的元素都是 plugin_invoke_Enum 枚举类的实例。
    - 被此函数装饰的函数在执行时，其实际行为不会被改变，即它仍然会按照原代码执行。
    """

    def decorator(func):
        """
        这是一个装饰器函数，该函数以另一个函数作为输入，并返回一个经过包装的函数。
        
        参数：
        func：一个函数，即将被装饰的函数。
        
        返回：
        返回一个经过包装的函数。包装后的函数在执行时会首先执行一些特定的操作（在这个具体例子中，没做任何操作）。包装后的函数具有一个额外的属性_invoke_at，它的值为传入的types列表。
        
        注意：
        这是一个高阶函数，本身返回了一个装饰器函数。在使用时，需先调用invoke_at函数，传入types参数，得到装饰器函数，再用该装饰器函数装饰需要的函数。
        例如：
        @invoke_at([plugin_invoke_Enum.type1, plugin_invoke_Enum.type2])
        def my_function():
          pass
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper._invoke_at = types
        return wrapper

    return decorator


class trainer_plugin_base(metaclass=abc.ABCMeta):
    """
    这是一个抽象基类，提供训练插件的基础结构和工具。这个类主要有两个方法：`get_plugin_map`和`Invoke`。
    
    # 类介绍
    此类作为所有训练插件的基类，定义了训练插件的基础结构和行为。提供了一个接口，供子类实现特定的训练行为。
    
    # 使用例子
    class MyTrainerPlugin(trainer_plugin_base):
        def Invoke(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
            # 实现特定的训练行为
    
    # 方法介绍
    - `get_plugin_map`：返回一个字典，字典的键是枚举类型，值是方法列表，这些方法在该枚举类型下被调用。此方法用于整理和提供训练插件的调用行为。
    
    - `Invoke`：这是一个抽象方法，需要在子类中实现。此方法在训练过程中被调用，根据当前的全局状态、纪元状态和步骤状态进行特定的训练行为。
    
    # 参数列表
    - `global_state`：全局状态板，提供了全局的状态信息，如训练总的纪元数、当前纪元数等。
    
    - `epoch_state`：纪元状态板，提供了当前纪元的状态信息，如纪元的开始时间、结束时间等。
    
    - `step_state`：步骤状态板，提供了当前步骤的状态信息，如步骤的开始时间、结束时间等。
    
    # 返回类型介绍
    - `get_plugin_map`：返回一个字典，键是枚举类型，值是方法列表。
    
    - `Invoke`：没有返回值。
    
    # 注意事项
    - 该类是一个抽象基类，不能直接实例化，只能作为基类被继承。
    
    - `Invoke`方法必须在子类中实现。
    """

    def get_plugin_map(self) -> {}:
        """
        这个方法用于获取插件映射表。插件映射表是一个字典，其键是枚举值，对应的值是一个包含所有具有此枚举值的方法的列表。
        
        插件映射表的获取过程如下：首先，我们遍历这个类的所有属性，然后检查每个属性是否具有'_invoke_at'属性。如果具有'_invoke_at'属性，我们就把这个属性看作是一个方法，并且将其'_invoke_at'属性的每个元素都看作是一个枚举值。然后，我们将这些枚举值和对应的方法添加到插件映射表中。
        
        参数:
        无
        
        返回类型:
        一个字典，其键是枚举值，对应的值是一个包含所有具有此枚举值的方法的列表。
        
        注意:
        如果同一个枚举值对应多个方法，那么这些方法将被添加到同一个列表中，并将此列表作为这个枚举值在插件映射表中的值。
        
        示例:
        如果我们有一个类，其内部定义了两个方法method1和method2，它们的'_invoke_at'属性都包含了同一个枚举值enum1，那么在调用get_plugin_map方法后，将返回一个插件映射表，其内容将是{enum1: [method1, method2]}。
        """

        run_dict = {}
        for name in dir(self):
            method = getattr(self, name)
            if hasattr(method, '_invoke_at'):
                for enum in method._invoke_at:
                    # 将每个enum和对应的方法添加到run_dict中
                    if enum not in run_dict:
                        run_dict[enum] = []
                    run_dict[enum].append(method)

        return run_dict

    def Invoke(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        """
        这是一个在基类`trainer_plugin_base`中的方法，名为`Invoke`。这个方法是一个抽象方法，用于在子类中被重写。
        
        参数:
        - global_state (global_state_board): 全局状态对象，用于存储和传递全局的状态信息
        - epoch_state (epoch_state_board): epoch状态对象，用于存储和传递当前epoch的状态信息
        - step_state (step_state_board): step状态对象，用于存储和传递当前step的状态信息
        
        返回:
        这个方法没有返回值。
        
        注意，这个方法过于抽象，具体的行为需要在子类中实现，因此可能会有不同的行为和返回值。如果你在使用这个方法的过程中遇到问题，可能是由于在子类中没有正确地重写这个方法。
        
        例子:
        ```python
        class MyTrainerPlugin(trainer_plugin_base):
            def Invoke(self, global_state, epoch_state, step_state):
                # 在这里实现你的逻辑
                print(global_state, epoch_state, step_state)
        ```
        在这个例子中，我们创建了一个新的训练插件`MyTrainerPlugin`，并重写了`Invoke`方法。在我们的实现中，我们只是简单地打印出了传入的状态信息。
        """

        pass
