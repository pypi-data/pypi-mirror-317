# pass_generate
from tketool.pyml.pytrainer import *
from accelerate import Accelerator
from accelerate import init_empty_weights, infer_auto_device_map, load_checkpoint_in_model, dispatch_model


class pytrainer_accelerate(pymodel_trainer):
    """
    这是一个名为pytrainer_accelerate的类，继承自pymodel_trainer。该类的目标是提供一种在使用PyTorch框架和Accelerator库在GPU或CPU上训练模型的方式。用户可以通过指定参数，灵活地控制训练过程，如是否使用CPU进行训练，指定使用哪些GPU，以及每个GPU的最大使用率等。
    
    该类在初始化时，将传入的模型和损失函数，以及其他参数绑定到自身。同时根据指定的设备类型创建Accelerator实例，并将模型分配到相应的设备上。
    
    类中定义的_drive_batch_data方法，在每个训练批次开始时被调用，用于将输入和标签数据转移到用于训练的设备上。
    
    backward方法则在计算反向传播时被调用，用于计算损失函数的梯度。
    
    使用示例：
    ```python
    model = torch.nn.Sequential(...)
    loss_obj = torch.nn.CrossEntropyLoss()
    trainer = pytrainer_accelerate(model, loss_obj, use_cpu=False, use_gpu_ids=[0, 1])
    for epoch in range(num_epochs):
        for batch in dataloader:
            trainer._drive_batch_data(...)
            trainer.backward(...)
    ```
    
    参数：
    - model (torch.nn.Module)：待训练的模型。
    - loss_obj：用于模型训练的损失函数。
    - use_cpu (bool)：是否使用CPU进行训练。默认为False。
    - use_gpu_ids (list)：要用于训练的GPU的ID列表。如果是None，则使用所有可用的GPU。默认为None。
    - no_split_module_classes (list)：不进行模型分割的模块类别列表。默认为空列表。
    - max_use_per_gpu (float)：每个GPU的最大使用率，值在0.0到1.0之间，默认为1.0。
    - kwargs：其他参数。
    
    注意点：
    - 当use_cpu为True时，无论use_gpu_ids的值为何，都只会使用CPU进行训练。
    - 当use_gpu_ids为None时，将使用所有可用的GPU进行训练，但是GPU的使用率仍然受max_use_per_gpu参数的限制。
    - 当指定no_split_module_classes时，对应的模块在分配到设备时，将保持整体，不会被分割。
    """

    def __init__(self, model: torch.nn.Module, loss_obj,
                 use_cpu=False,
                 use_gpu_ids=None,
                 no_split_module_classes=[],
                 max_use_per_gpu=1.0,
                 **kwargs):
        """
        `pytrainer_accelerate`是一个pytorch模型训练加速器类，继承自`pymodel_trainer`。它利用了Accelerator库来配合GPU或CPU进行分布式训练，并在模型训练的过程中对数据进行优化处理，提高模型训练速度和效率。
        
        参数:
        - `model`: 需要被训练的torch.nn.Module模型对象。
        - `loss_obj`: 损失函数对象。
        - `use_cpu`: 布尔值，是否使用CPU进行训练。默认值为False。
        - `use_gpu_ids`: 列表，需要使用的GPU的ID。如果为None,则自动选择GPU。默认值为None。
        - `no_split_module_classes`: 列表，不希望分割的模块类。默认值为空列表。
        - `max_use_per_gpu`: 每个GPU最大使用的内存百分比，范围是0-1。默认值为1.0。
        - `kwargs`: 其他参数。
        
        方法:
        - `_drive_batch_data`: 在每个批次训练开始时调用，将数据移动到加速器设备（CPU或GPU）上。
        - `backward`: 对损失函数进行反向传播。
        
        示例:
        
        ```python
        model = torch.nn.Linear(10, 1)
        loss_obj = torch.nn.MSELoss()
        trainer = pytrainer_accelerate(model, loss_obj, use_cpu=False, use_gpu_ids=[0, 1])
        ```
        
        在上述示例中，我们创建了一个线性模型和一个均方差损失函数，然后使用`pytrainer_accelerate`类来加速模型训练，我们选择了使用ID为0和1的两个GPU进行训练。
        """

        super().__init__(model, loss_obj, **kwargs)

        self.accelerator = Accelerator(cpu=use_cpu)

        if self.accelerator.device.type == "cuda":
            if use_gpu_ids is not None:
                max_memory = {}  # {int(cuda): '8GiB' for cuda in ['0', '1', '2', '3']}
                for cuda_id in use_gpu_ids:
                    device = torch.device(f"cuda:{int(cuda_id)}")
                    prop = torch.cuda.get_device_properties(device)
                    gpu_memory = round(prop.total_memory / (1024 ** 3) * max_use_per_gpu, 1)
                    max_memory[int(cuda_id)] = f"{gpu_memory}GiB"
            else:
                max_memory = None

            self.device_map = infer_auto_device_map(self.model, max_memory=max_memory,
                                                    no_split_module_classes=no_split_module_classes)
            self.model = dispatch_model(self.model, device_map=self.device_map)

    @invoke_at([plugin_invoke_Enum.Batch_begin])
    def _drive_batch_data(self, global_state: global_state_board, epoch_state: epoch_state_board,
                          step_state: step_state_board):
        """
        这个类为 `pytrainer_accelerate`，它继承了 `pymodel_trainer` 类，主要针对模型的训练过程进行加速处理。主要通过使用 `Accelerator` 对象和 `device_map` 实现模型处理设备的自动调度，并在每个批次数据处理前，将数据转移到合适的处理设备。
        
        函数 `_drive_batch_data` 是 `pytrainer_accelerate` 的一个成员函数，它在每个批次数据处理前被调用。这个函数的主要作用是将数据（输入和标签）转移到合适的处理设备（CPU或CUDA设备）。数据的转移过程都在 `move_to_drive` 这个内部函数中完成，支持数据为 `dict` 类型或者其他类型。转移后的数据会保存在 `step_state` 对象的 `converted_input` 和 `converted_label` 属性中。
        
        `_drive_batch_data` 函数的参数列表如下：
        
        - `global_state: global_state_board`：全局状态板，用于存放全局状态信息。
        - `epoch_state: epoch_state_board`：当前周期状态板，用于存放当前周期的状态信息。
        - `step_state: step_state_board`：当前步骤状态板，用于存放当前步骤的状态信息。
        
        这个函数没有返回值。
        """

        def move_to_drive(tensor_or_dict):
            if isinstance(tensor_or_dict, dict):
                return {k: v.to(self.accelerator.device) for k, v in tensor_or_dict.items()}

            else:
                return tensor_or_dict.to(self.accelerator.device)

        step_state.converted_input = move_to_drive(step_state.converted_input)
        step_state.converted_label = move_to_drive(step_state.converted_label)

    def backward(self, global_state: global_state_board, epoch_state: epoch_state_board,
                 step_state: step_state_board):
        """
        `backward`是`pytrainer_accelerate`类的一个方法。`pytrainer_accelerate`类是一个模型训练器，它继承自`pymodel_trainer`类，并添加了accelerate库的支持，可以在CPU和GPU上进行高效训练。
        
        它通过`model`参数接受一个pytorch模型，并通过`loss_obj`参数接受一个损失对象。此外，还可以通过参数`use_cpu`、`use_gpu_ids`、`no_split_module_classes`、`max_use_per_gpu`等来指定训练的硬件环境和模型的部署方式。
        
        该类的实例化方法通过`Accelerator`类创建一个加速器，并根据给定的硬件环境和模型部署方式将模型部署到对应的设备上。
        
        `backward`方法是用于执行反向传播的。它接受三个参数，分别是`global_state`、`epoch_state`和`step_state`，这些状态对象包含了训练过程中的全局状态、当前epoch的状态和当前步骤的状态。它通过`accelerator`的`backward`方法来执行反向传播，并更新状态对象中的损失张量。
        
        参数:
        - `global_state` (`global_state_board`): 全局状态板，包含了训练过程中的全局状态。
        - `epoch_state` (`epoch_state_board`): epoch状态板，包含了当前epoch的状态。
        - `step_state` (`step_state_board`): 步骤状态板，包含了当前步骤的状态。
        
        返回:
        - 无
        
        示例:
        ```python
        # 创建一个模型和损失对象
        model = torch.nn.Linear(10, 1)
        loss_obj = torch.nn.MSELoss()
        
        # 创建一个训练器
        trainer = pytrainer_accelerate(model, loss_obj, use_cpu=True)
        
        # 创建状态板
        global_state = global_state_board(...)
        epoch_state = epoch_state_board(...)
        step_state = step_state_board(...)
        
        # 执行反向传播
        trainer.backward(global_state, epoch_state, step_state)
        ```
        """

        self.accelerator.backward(step_state.loss_tensor)
        # step_state.loss_tensor.backward()
