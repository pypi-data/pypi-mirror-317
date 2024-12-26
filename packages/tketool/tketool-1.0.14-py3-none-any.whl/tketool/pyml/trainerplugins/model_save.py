# pass_generate
import sys
from tketool.files import delete_files_in_directory
from tketool.logs import convert_print_color, log_color_enum
from tketool.pyml.pytrainer import *
from enum import Enum
from tketool.files import create_folder_if_not_exists
import os, pickle, torch, re
from tketool.logs import log
from tketool.files import *


# class model_preload_Enum(Enum):
#     NoLoad = 1
#     Load_latest = 2


class model_save(trainer_plugin_base):
    """
    这个类是一个模型的保存插件，在训练的过程中，不同的步骤下进行模型的保存。它继承了trainer_plugin_base基类。
    
    主要功能：
    
    - 在训练过程的每个步骤结束时，每隔一定步数（save_per_step）进行模型保存
    - 在每一个训练周期结束的时候，如果该周期的损失值小于之前保存过的模型的损失值，那么就保存该模型
    - 具备模型保存路径不存在时，创建路径的能力
    
    主要方法：
    
    - `__init__(self, save_per_step=1, mini_loss_save=True, save_folder='checkpoint')`：初始化方法，设置保存步长、是否保存最小损失模型以及模型保存路径
    - `BeginInvoke(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board)`：在训练开始时，创建模型保存的文件夹
    - `save_model(self, global_state: global_state_board, path)`：保存模型的方法，会根据训练器的类型，选择不同的保存方法
    - `Batch_end(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board)`：在每个批次训练结束时，每隔一定步数进行模型的保存
    - `epoch_end(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board)`：在每个训练周期结束时，如果该周期的损失值小于之前保存过的模型的损失值，那么保存该模型
    - `Invoke(self, base_wall, epoch_wall, batch_wall)`：在插件调用时被执行，但在该类中并未被实现
    
    例子：
    
    ```python
    trainer = Trainer(...)
    plugin = model_save(save_per_step=100, save_folder='./checkpoint')
    trainer.add_plugin(plugin)
    trainer.train(...)
    ```
    
    注意事项：
    - 由于`Invoke`方法在该类中并未被实现，所以如果有需要在插件调用时执行的操作，请在子类中重写此方法。
    """

    def __init__(self, save_per_step=1, mini_loss_save=True, save_folder='checkpoint', save_opt_params=True):
        """
        初始化model_save类的实例对象。
        
        此类是训练模型时的一个插件，用于保存训练过程中的模型。其中，每一步训练后都会保存一次模型，并且在每个周期结束后，如果损失降低，也会保存模型。
        
        参数:
        save_per_step(int, 默认值为1): 每训练多少步，保存一次模型。
        mini_loss_save(bool, 默认值为True): 是否在每个训练周期结束后，如果损失有所降低，保存模型。
        save_folder(str, 默认值为'checkpoint'): 保存模型的文件夹名称。
        
        返回:
        无
        
        使用示例:
        ```python
        save_plugin = model_save(save_per_step=50, mini_loss_save=True, save_folder='model_checkpoints')
        ```
        在这个示例中，model_save的实例在每50步训练后保存一次模型，如果训练周期结束后，损失有所降低，也会保存模型，所有的模型都保存在'model_checkpoints'文件夹下。
        
        注意：
        此类没有返回值。
        """

        self.save_per_step = save_per_step
        # self.save_per_batch = save_per_batch
        self.save_folder = save_folder
        self.mini_loss = sys.float_info.max
        # self.saved_models = []
        self.save_opt_parameters = save_opt_params

    @invoke_at([plugin_invoke_Enum.Begin])
    def BeginInvoke(self, global_state: global_state_board, epoch_state: epoch_state_board,
                    step_state: step_state_board):
        """
        这是一个`model_save`类中的`BeginInvoke`函数，其作用是在训练开始时创建模型保存的文件夹。
        
        参数:
            global_state (global_state_board): 存储全局状态相关信息的实例，包括当前模型、优化器等信息。
            epoch_state (epoch_state_board): 存储当前周期(epoch)相关状态的实例，如当前周期的损失等。
            step_state (step_state_board): 存储当前步骤相关状态的实例，如当前步骤的损失、正确率等。
        
        返回:
            无返回值
        
        使用示例：
            在训练开始时，首先创建一个`model_save`类的实例，然后调用这个函数来创建模型保存的文件夹。
            ```
            save_plugin = model_save(save_per_step=100, save_folder='checkpoint')
            save_plugin.BeginInvoke(global_state, epoch_state, step_state)
            ```
        注意事项：
            该函数无返回值，主要作用是创建保存模型的文件夹，如果文件夹已经存在则不会重复创建。
            该函数没有错误处理，如果在创建文件夹时出现错误（如权限问题、磁盘空间不足等），可能会抛出异常。
        """

        create_folder_if_not_exists(global_state.model_folder, self.save_folder)

    def save_model(self, global_state: global_state_board, path):
        """
            本函数用于模型的保存。根据训练器的类型，将模型的需要优化的参数保存在指定的路径下。
        
            参数:
            - global_state: global_state_board类型，包含全局状态信息，如训练器类型、模型等。
            - path: 字符串类型，用于指定模型保存的路径。
        
            返回:
            - 无返回值
        
            注意：本函数不会检查路径是否合法、是否有权限等，这些需要在调用前确认。
        """

        if global_state.trainer_type_name == "pytrainer_deepspeed":
            model_engine = global_state.trainer.model_engine
            state_dict = {name: param for name, param in model_engine.module.named_parameters() if param.requires_grad}

            model_engine.save_checkpoint(save_dir=path,  # client_state={'model': state_dict},
                                         exclude_frozen_parameters=True)
        else:
            parameters_to_save = {name: param for name, param in global_state.model.named_parameters() if
                                  param.requires_grad}
            torch.save(parameters_to_save, path)

        if self.save_opt_parameters:
            opt = global_state.optimizer
            save_path = os.path.join(global_state.model_folder, f"opt_state.pth")
            torch.save(opt.state_dict(), save_path)

    @invoke_at([plugin_invoke_Enum.Batch_end])
    def Batch_end(self, global_state: global_state_board, epoch_state: epoch_state_board,
                  step_state: step_state_board):
        """
            `Batch_end`是一个函数，其属于`model_save`类的方法。此函数在每个batch训练结束后被调用，用于定期保存当前全局状态下的模型参数。如果全局状态下的步数可以被预设的保存步数整除，则会保存模型。
        
            参数:
            - `global_state` (`global_state_board`): 表示全局状态的对象，包含了模型、优化器等相关信息。
            - `epoch_state` (`epoch_state_board`): 表示当前epoch（训练周期）状态的对象，包含了当前epoch的损失、准确率等信息。
            - `step_state` (`step_state_board`): 表示当前步骤状态的对象，包含了当前步骤的损失、准确率等信息。
        
            该函数没有返回值。
        
            例如，如果设定`save_per_step`=100，那么每进行100步训练，函数就会执行以下操作：
            1. 构建保存路径，路径包括模型文件夹、保存文件夹和步数信息。
            2. 调用`save_model`方法保存模型
            3. 将保存信息添加到日志堆栈
        
            注意：此函数不保证每次都能够成功保存模型，只有当全局状态下的步数能够被预设的保存步数整除时，才会进行保存。
        
        """

        if global_state.step % self.save_per_step == 0:
            save_path = os.path.join(global_state.model_folder, self.save_folder, f"step-{global_state.step}.pth")
            self.save_model(global_state, save_path)
            # torch.save(global_state.model.state_dict(), save_path)
            global_state.log_stack.append(f" Model save: {save_path}")

    @invoke_at([plugin_invoke_Enum.Epoch_end])
    def epoch_end(self, global_state: global_state_board, epoch_state: epoch_state_board,
                  step_state: step_state_board):
        """
        此方法是`model_save`类的一个方法，旨在在每个训练周期结束时执行特定的操作。主要功能是在训练周期结束时，如果周期损失低于当前最小损失，则保存模型。
        
        参数:
        - `global_state` (`global_state_board`类型): 全局状态对象，包含训练过程中全局的状态信息，如模型、优化器等。
        - `epoch_state` (`epoch_state_board`类型): 周期状态对象，包含训练过程中每个周期的状态信息，如周期损失等。
        - `step_state` (`step_state_board`类型): 步骤状态对象，包含训练过程中每个步骤的状态信息。
        
        此方法没有返回值。
        
        注意：
        - 使用此方法需要确保`global_state`、`epoch_state`和`step_state`对象已经被正确初始化，并在运行过程中被正确更新。
        - 此方法会改变`self.mini_loss`的值，用于记录当前训练过程中的最小损失值。
        - 如果保存的模型文件夹已经存在，则会删除文件夹中的所有文件，然后保存新的模型。
        - 此方法不会处理任何异常，如果在运行过程中出现异常，如文件读写错误等，需要在调用此方法的地方进行捕获和处理。
        """

        if epoch_state.epoch_loss < self.mini_loss:
            save_folder = os.path.join(global_state.model_folder, self.save_folder, "mini_loss")

            if os.path.exists(save_folder):
                delete_files_in_directory(save_folder)
            else:
                create_folder_if_not_exists(save_folder)

            save_path = os.path.join(save_folder, f"mini-loss-{global_state.step}.pth")
            self.save_model(global_state, save_path)
            # torch.save(global_state.model.state_dict(), save_path)
            global_state.log_stack.append(f" Model save: {save_path}")

            self.mini_loss = epoch_state.epoch_loss

    def Invoke(self, base_wall, epoch_wall, batch_wall):
        """
        Invoke方法是model_save类的一个空方法，它在这个类中没有具体的实现，并且在类的其他地方也没有被调用。这个方法可能是一个占位符，留待未来实现某些功能时使用。
        
        参数:
        - base_wall: 未在类中使用，可能是未来实现某些功能时使用。
        - epoch_wall: 未在类中使用，可能是未来实现某些功能时使用。
        - batch_wall: 未在类中使用，可能是未来实现某些功能时使用。
        
        返回:
        - 无返回类型
        
        注意:
        - 此函数当前未实现任何功能，也未在类的其他地方被调用，可能存在一些占位的目的。
        """

        pass


def load_saved_parameters(model, path):
    """
    该函数用于加载保存的模型参数。
    
    参数:
        model: PyTorch模型，该模型是需要加载参数的模型。
        path: str，保存模型参数的路径。
    
    该函数从给定的路径加载模型参数，并将它们加载到给定的模型中。函数首先确定模型参数的设备位置，
    然后根据这个设备位置加载模型参数。如果加载的参数中包含'module'关键字，我们将直接使用该关键字对应的参数。
    
    在加载过程中，该函数会检查每一个参数的形状是否与保存的参数形状相匹配。如果不匹配，将会打印一条警告日志信息。
    
    最后，函数会打印加载了多少个参数。
    
    注意:
        1. 此函数没有返回值，它直接修改传入的模型参数。
        2. 如果参数加载过程中出现任何错误，函数会抛出异常。
    
    用法示例：
        model = SomePyTorchModel()
        path = "/path/to/saved/parameters"
        load_saved_parameters(model, path)
    """

    model_device = next(model.parameters()).device

    parameters_to_load = torch.load(path, map_location=model_device)
    total_params = 0

    if 'module' in parameters_to_load:
        parameters_to_load = parameters_to_load['module']

    for name, param in model.named_parameters():
        if name in parameters_to_load:
            if param.data.shape != parameters_to_load[name].data.shape:
                log(f"load p shape warning: {name} ({str(param.data.shape)}) not match the saved shape {parameters_to_load[name].data.shape}")
            param.data = parameters_to_load[name].data
            total_params += param.numel()
    log(f"load p count: {total_params}")


def load_saved_opt_parameters(opt, path):
    device = next(opt.parameters()).device
    opt_state = torch.load(path, map_location=device)

    opt.load_state_dict(opt_state)


class model_loader:
    def __init__(self, saved_path):
        self.step_model_dict = {}
        self.mini_loss_path = ""
        self.opt_path = ""

        pattern = re.compile(r'step-(\d+)\.pth$')

        for file in enum_files(saved_path, recursive=False):
            match = pattern.match(file[1])
            if match:
                step_num = int(match.group(1))
                self.step_model_dict[step_num] = file[0]

        save_folder = os.path.join(saved_path, "mini_loss")
        self.mini_loss_path = [file[0] for file in enum_files(save_folder, recursive=False)]
        if len(self.mini_loss_path) > 0:
            self.mini_loss_path = self.mini_loss_path[0]

        self.opt_path = os.path.join(save_folder, f"opt_state.pth")
        if not os.path.exists(self.opt_path):
            self.opt_path = None

    def load_mini_loss(self, model, opt=None):
        load_saved_parameters(model, self.mini_loss_path)
        if opt and self.opt_path:
            load_saved_opt_parameters(opt, self.opt_path)

    def load_last(self, model, opt=None):
        sorted_list = list(sorted(self.step_model_dict.items(), key=lambda item: item[0]))
        load_saved_parameters(model, sorted_list[0][1])
        if opt and self.opt_path:
            load_saved_opt_parameters(opt, self.opt_path)

    def load_step(self, model, step_num, opt=None):
        path = self.step_model_dict[step_num]
        load_saved_parameters(model, path)
        if opt and self.opt_path:
            load_saved_opt_parameters(opt, self.opt_path)

#
