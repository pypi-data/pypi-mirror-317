# pass_generate
from tketool.pyml.pytrainer import *
import argparse, deepspeed
from deepspeed.utils import logger as ds_logger
from tketool.logs import set_logger

set_logger(ds_logger)


class pytrainer_deepspeed(pymodel_trainer):
    """
    `pytrainer_deepspeed` 是一个继承自 `pymodel_trainer` 的类，用于使用DeepSpeed深度学习优化库训练PyTorch模型。
    
    这个类的目的是在PyTorch模型训练过程中使用DeepSpeed进行优化，包括自动混合精度训练、模型并行、激活checkpointing等特性。通过构造函数，可以选择使用的精度类型。
    
    它使用了DeepSpeed的initialize方法，配置参数包含了对DeepSpeed的各种参数设置，如fp16训练、Zero优化、激活checkpointing等。
    
    类中的`_drive_batch_data`方法用于在训练开始前，将批次数据移动到指定的设备上。`init_deepspeed`方法在训练开始时，初始化DeepSpeed的模型、优化器等参数。`invoke_model`方法用于前向传播，`backward`方法用于反向传播，`step`方法用于更新模型参数。
    
    示例：
    ```
    model = SomeTorchModel()
    loss_obj = SomeLossObject()
    trainer = pytrainer_deepspeed(model, loss_obj, precision_type=dtype_enum.BF16)
    global_state = GlobalStateBoard(...)
    epoch_state = EpochStateBoard(...)
    step_state = StepStateBoard(...)
    trainer.init_deepspeed(global_state, epoch_state, step_state)
    for epoch in range(num_epochs):
        for batch in dataloader:
            step_state.update(batch)
            trainer._drive_batch_data(global_state, epoch_state, step_state)
            output = trainer.invoke_model(global_state, epoch_state, step_state)
            loss = loss_obj(output, step_state.converted_label)
            trainer.backward(global_state, epoch_state, step_state)
            trainer.step(global_state, epoch_state, step_state)
    ```
    
    注意: 这个类没有明确的错误处理机制，如果传入的参数不符合要求，可能导致错误。
    """

    def __init__(self, model: torch.nn.Module, loss_obj, precision_type=dtype_enum.Auto,
                 **kwargs):
        """
        初始化pytrainer_deepspeed类。
        
        pytrainer_deepspeed是一个继承自pymodel_trainer的类，主要用于训练深度学习模型。该类通过抽象化处理，使得用户可以在不了解深度学习训练细节的情况下，便捷地进行模型训练。
        
        参数:
            model (torch.nn.Module): 需要训练的PyTorch模型。
            loss_obj: 损失函数对象，用于在训练过程中计算预测值与真实值之间的误差。
            precision_type (dtype_enum, 可选): 模型训练的精度类型。默认为dtype_enum.Auto，表示自动选择精度类型。dtype_enum中还包含Float32和BF16两种类型，分别表示使用32位浮点数和16位浮点数进行训练。
            **kwargs: 其他参数。
        
        该类的主要方法包括:
            init_deepspeed: 初始化DeepSpeed引擎。
            invoke_model: 调用模型进行前向传播。
            backward: 调用模型进行反向传播。
            step: 更新模型参数。
        
        使用示例:
        
            ```python
            model = torch.nn.Linear(10, 1) # 假设我们的模型是一个线性模型
            loss_obj = torch.nn.MSELoss()  # 我们使用均方误差作为损失函数
            trainer = pytrainer_deepspeed(model, loss_obj, precision_type=dtype_enum.Float32)
            ```
        """

        super().__init__(model, loss_obj, **kwargs)
        self.model_engine = None

        if precision_type == dtype_enum.Float32 or precision_type == dtype_enum.Auto:
            self.fp16 = False
            self.bf16 = False
        elif precision_type == dtype_enum.BF16:
            self.fp16 = False
            self.bf16 = True
        else:
            self.fp16 = True
            self.bf16 = False

    @invoke_at([plugin_invoke_Enum.Batch_begin])
    def _drive_batch_data(self, global_state: global_state_board, epoch_state: epoch_state_board,
                          step_state: step_state_board):
        """
        这是一个类的方法，负责驱动批次数据。
        
        这个方法的主要功能是将输入数据从CPU转移到GPU上，用于模型的训练计算。
        
        在分布式训练中，由于数据需要在不同的设备上进行计算，因此需要将数据转移到相应的设备上。
        
        参数:
            global_state: global_state_board对象，表示全局状态的信息，如模型、优化器等。
        
            epoch_state: epoch_state_board对象，表示当前epoch的状态信息。
        
            step_state: step_state_board对象，表示当前步骤的状态信息，其中包含了当前步骤的输入和标签数据。
        
        返回值:
            无返回值。
        
        注意:
            这个方法没有返回值，但它会修改step_state对象的converted_input和converted_label属性，
            使其指向GPU上的内存地址。
        
        示例:
            假设我们有一个名为trainer的pytrainer_deepspeed对象，以及global_state, epoch_state和step_state这三个状态对象，我们可以像下面这样使用这个方法：
        
            ```python
            trainer._drive_batch_data(global_state, epoch_state, step_state)
            ```
        
            在调用这个方法之后，step_state.converted_input和step_state.converted_label将被转移到GPU上，可以被用于模型的训练计算。
        """

        def move_to_drive(tensor_or_dict):
            if isinstance(tensor_or_dict, dict):
                return {k: v.to(self.model_engine.local_rank) for k, v in tensor_or_dict.items()}

            else:
                return tensor_or_dict.to(self.model_engine.local_rank)

        step_state.converted_input = move_to_drive(step_state.converted_input)
        step_state.converted_label = move_to_drive(step_state.converted_label)

    @invoke_at([plugin_invoke_Enum.Begin])
    def init_deepspeed(self, global_state: global_state_board, epoch_state: epoch_state_board,
                       step_state: step_state_board):
        """
        这个函数是`pytrainer_deepspeed`类的一部分，用来初始化DeepSpeed模型训练库。
        
        DeepSpeed是微软开源的一个高性能分布式训练库，可以大幅度提升训练速度，同时减少所需的计算资源。这个函数会根据全局状态、时期状态以及步骤状态来设置DeepSpeed的配置参数。
        
        参数:
        - global_state (`global_state_board`): 全局状态板，包含了训练过程中的全局信息，如模型、优化器等。
        - epoch_state (`epoch_state_board`): 时期状态板，包含了训练过程中某一轮时期的信息。
        - step_state (`step_state_board`): 每步训练的状态板，包含了训练过程中某一步的信息。
        
        该函数不返回任何值，但会更改`self.model_engine`和`global_state.optimizer`的值。
        
        使用示例：
        
        ```python
        trainer = pytrainer_deepspeed(model, loss)
        trainer.init_deepspeed(global_state, epoch_state, step_state)
        ```
        
        注意：此函数无法单独使用，它依赖于`pymodel_trainer`类和`pytrainer_deepspeed`类的其他方法。
        
        注意：在使用此函数前，确保你的环境中已安装了DeepSpeed库。
        
        注意：此函数没有明显的错误或bug，但在使用时要确保传入的状态板（state_board）的类型和值是正确的，否则可能会引发错误。
        """

        deepspeed_config = {
            "steps_per_print": 3000000,
            "fp16": {
                "enabled": self.fp16
            },
            "bf16": {
                "enabled": self.bf16
            },
            "train_batch_size": 3,
            "zero_optimization": {
                "stage": 2,
                "allgather_partitions": True,
                "reduce_scatter": True
            },
            "activation_checkpointing": {
                "partition_activations": True,
                "cpu_checkpointing": True
            },
        }

        self.model_engine, global_state.optimizer, _, _ = deepspeed.initialize(model=global_state.model,
                                                                               optimizer=global_state.optimizer,
                                                                               config_params=deepspeed_config, )

    def invoke_model(self, global_state: global_state_board, epoch_state: epoch_state_board,
                     step_state: step_state_board):
        """
        这是pytrainer_deepspeed类中的一个成员函数,它的主要功能是调用深度学习模型进行前向传播。
        
        参数:
        - global_state：global_state_board类型，包含全局状态信息，如模型、优化器等。
        - epoch_state：epoch_state_board类型，包含单个epoch的状态信息。
        - step_state：step_state_board类型，包含单个训练步骤的状态信息。
        
        返回:
        - 返回模型在输入数据上的前向传播结果。
        
        注意：
        这个函数的作用主要是调用模型进行前向传播，并没有与模型相关的其他操作，如更新参数等。
        
        例子:
        
            trainer = pytrainer_deepspeed(model, loss_obj)
            trainer.init_deepspeed(global_state, epoch_state, step_state)
            output = trainer.invoke_model(global_state, epoch_state, step_state)
        """

        return self.model_engine(step_state.converted_input)

    def backward(self, global_state: global_state_board, epoch_state: epoch_state_board,
                 step_state: step_state_board):
        """
        这是一个负责执行模型的反向传播的函数。这个函数会使用deepSpeed引擎进行反向传播，从而优化模型的参数。
        
        参数:
        - global_state: global_state_board对象，表示全局状态，包含了全局的设置和参数。
        - epoch_state: epoch_state_board对象，表示当前epoch的状态，包含了当前epoch的设置和参数。
        - step_state: step_state_board对象，表示当前步骤的状态，包含了当前步骤的设置和参数。
        
        返回:
        - 这个函数没有返回值。
        
        例子:
        ```python
        # 假设已经有了global_state，epoch_state和step_state对象
        trainer = pytrainer_deepspeed(model, loss_obj)
        trainer.backward(global_state, epoch_state, step_state)
        ```
        
        注意:
        这个函数不会检查输入参数的合法性，如果输入的参数类型或者值不正确，可能会抛出异常。使用时需要保证输入参数的正确性。
        """

        self.model_engine.backward(step_state.loss_tensor)

    def step(self, global_state: global_state_board, epoch_state: epoch_state_board,
             step_state: step_state_board):
        """
        这个方法是pytrainer_deepspeed类的一部分，该类是用于训练pytorch模型的。这个类扩展了pymodel_trainer类，添加了对deepspeed库的支持，这是一个用于加速深度学习训练过程的库。
        
        `step`方法是每一步训练过程中的一个步骤，在每一轮训练的每个批次数据过后调用。
        
        参数:
        - global_state: global_state_board对象，包含全局状态信息，如模型，优化器等。
        - epoch_state: epoch_state_board对象，包含当前epoch的状态信息。
        - step_state: step_state_board对象，包含当前步骤的状态信息。
        
        无返回值。
        
        这个方法的主要任务是执行模型的优化器的step操作，这会更新模型的权重。
        
        注意：这个方法没有明确的错误处理或者异常抛出，如果在执行过程中有任何错误，都会直接导致程序终止运行。
        
        代码示例：
        ```python
        trainer = pytrainer_deepspeed(model, loss_obj)
        for epoch in range(num_epochs):
            for batch_data in data_loader:
                # ... 此处省略了一些代码，包括数据预处理，模型前向计算，计算损失等步骤
                trainer.step(global_state, epoch_state, step_state)
        ```
        """

        self.model_engine.step()
