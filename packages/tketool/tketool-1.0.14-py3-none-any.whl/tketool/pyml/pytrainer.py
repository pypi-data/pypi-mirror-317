# pass_generate
import os.path
from tketool.evaluate.scores import *
from prettytable import PrettyTable, ALL
import torch
from tketool.mlsample.SampleSet import SampleSet
from tketool.utils.progressbar import process_status_bar
from tketool.files import create_folder_if_not_exists
from tketool.logs import log_multi_row
from datetime import datetime
from tketool.pyml.trainbase import *
from tketool.pyml.utils import convert_to_list

optimizer_dict = {
    "adamw": torch.optim.AdamW,
    "adam": torch.optim.Adam,
    "sgd": torch.optim.SGD,
}


class pymodel_trainer(trainer_plugin_base):
    """
    `pymodel_trainer`类是一个基于PyTorch的模型训练器，继承自`trainer_plugin_base`。该类主要负责模型的训练、验证以及训练进程的插件调用。
    
    主要成员函数:
    - __init__: 初始化函数，构造模型训练器
    - train: 训练模型
    - evaluate: 对模型进行评价
    - invoke_model: 调用模型进行预测
    - calculate_loss: 计算损失
    - zero_grad: 重置梯度
    - step: 执行一步优化
    - backward: 执行反向传播
    
    初始化函数__init__的参数列表如下
    - model: 需要训练的PyTorch模型
    - loss_obj: 用于计算模型损失的损失函数
    - update_mode: 模型参数更新的模式，每一步更新或者每一轮更新
    - output_folder: 模型输出文件夹的路径
    - plugins: 训练插件列表
    - optimizer_type: 优化器的类型，默认为"adamw"
    - learn_rate: 学习率，默认为0.01
    
    train函数的参数列表如下
    - sample_set: 需要训练的样本集合
    - epoch: 训练的轮数
    - input_convert_func: 输入数据转换函数，默认不变
    - label_convert_func: 标签数据转换函数，默认不变
    
    evaluate函数的参数列表如下
    - sample_set: 需要评价的样本集合
    - input_convert_func: 输入数据转换函数，默认不变
    - label_convert_func: 标签数据转换函数，默认不变
    - logit_convert_func: logits转换函数，默认不变
    - scores: 评价指标列表，默认包括准确率、精确率、召回率和F1分数
    
    注：这个类没有明显的错误或bug。
    """

    def Invoke(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        """
        `Invoke`是`pymodel_trainer`类中的一个方法。该方法目前为空，没有执行任何操作。
        
        参数:
        - `global_state` : global_state_board对象，用于存储所有全局状态，包括模型、优化器等。
        - `epoch_state` : epoch_state_board对象，用于存储当前epoch的状态，包括损失等。
        - `step_state` : step_state_board对象，用于存储当前步骤的状态，包括输入、输出、损失等。
        
        返回类型：无
        
        示例：
        ```python
        trainer = pymodel_trainer(...)
        global_state = global_state_board(...)
        epoch_state = epoch_state_board(...)
        step_state = step_state_board(...)
        trainer.Invoke(global_state, epoch_state, step_state)
        ```
        注意：这个方法目前为空，没有执行任何操作。尚未发现错误或者bug。
        """

        pass

    def __init__(self,
                 model: torch.nn.Module,
                 loss_obj,
                 update_mode=update_mode_enum.Per_Step,
                 output_folder=None,
                 plugins=[],
                 optimizer_type="adamw",
                 learn_rate=0.01):
        """
        这是一个`pymodel_trainer`类的初始化函数，用于初始化训练模型的各个参数和属性。
        
        参数:
        
        - `model`: 一个`torch.nn.Module`对象，表示模型。
        - `loss_obj`: 损失函数对象，用于计算模型的损失。
        - `update_mode`: 更新模型的方式，有按步（Per_Step）和按批（Per_Epoch）两种，取值来自`update_mode_enum`，默认是按步更新。
        - `output_folder`: 模型输出的文件夹路径，如果为None，则按时间戳创建一个新的文件夹，否则使用给定的路径。
        - `plugins`: 插件列表，默认为空。插件可以用来扩展模型的功能。
        - `optimizer_type`: 优化器的类型，默认为"adamw"。优化器用于更新模型的参数。
        - `learn_rate`: 学习率，默认为0.01。学习率决定了模型参数更新的步长。
        
        在这个初始化函数中，将会对模型、损失函数和优化器等重要属性进行初始化设置，并创建用于存储模型的文件夹。同时，也会根据插件列表来进行插件的初始化。
        
        注意，该函数没有返回值。
        
        使用示例：
        
        ```python
        model = torch.nn.Linear(10, 1)
        loss_obj = torch.nn.MSELoss()
        trainer = pymodel_trainer(model=model, loss_obj=loss_obj, output_folder='model_path')
        ```
        
        在这个例子中，我们创建了一个线性模型和均方误差损失函数，并且使用`pymodel_trainer`类进行了初始化。在初始化过程中，我们传入了模型和损失函数，并指定了模型的输出文件夹路径。
        
        错误和警告：
        
        本函数中，`optimizer_type`的取值应为`optimizer_dict`中的键，否则会引发错误。
        """

        self.model = model
        self.loss = loss_obj
        self.optimizer = optimizer_dict[optimizer_type](
            [{
                'params': p,
                'name': name
            } for name, p in model.named_parameters() if p.requires_grad], lr=learn_rate)

        if output_folder is None:
            self.out_folder = os.path.join("model", f"{datetime.now().strftime('%m_%d_%H_%M')}")
        else:
            self.out_folder = output_folder
        self.update_mode = update_mode
        create_folder_if_not_exists(self.out_folder)
        create_folder_if_not_exists(self.out_folder, 'saved_model')

        self.plugin = {}
        for pl in [self] + plugins:
            for ty, funs in pl.get_plugin_map().items():
                if ty not in self.plugin:
                    self.plugin[ty] = []
                for sub_fun in funs:
                    self.plugin[ty].append(sub_fun)

    def _invoke_plugin(self, plugin_enum, base_wall, epoch_wall, batch_wall):
        """
        _invoke_plugin 是一个私有方法，用于在训练过程中的某些特定阶段调用插件函数。例如，在每一个训练批次开始时，或者在每一个训练批次结束后，可能需要执行一些特定的操作（例如，记录日志、更新学习率等）。这些操作可以通过编写插件函数，并在合适的时机调用这些插件函数来实现。
        
        参数:
        - plugin_enum: 一个枚举值，指定当前训练的阶段。例如，可以是 'Batch_begin'（在一个训练批次开始时），'Batch_end'（在一个训练批次结束后）等。
        - base_wall: 一个全局状态板对象，包含了全局的训练状态，例如，当前的模型、优化器、损失函数等。
        - epoch_wall: 一个周期状态板对象，包含了当前训练周期的状态，例如，当前周期的损失值、准确率等。
        - batch_wall: 一个步骤状态板对象，包含了当前训练批次的状态，例如，当前批次的输入数据、目标数据、模型输出等。
        
        返回:
        - 无返回值
        
        使用方法:
        - 这是一个私有方法，通常不会直接在类外部调用。而是在训练过程中的特定阶段，例如，一个训练批次开始时，调用 '_invoke_plugin(plugin_enum.Begin, base_wall, epoch_wall, batch_wall)'，在一个训练批次结束后，调用 '_invoke_plugin(plugin_enum.End, base_wall, epoch_wall, batch_wall)' 等。
        
        注意事项:
        - 如果 plugin_enum 对应的插件函数列表为空，或者不存在，那么 '_invoke_plugin' 方法会直接返回，不会执行任何操作。
        
        可能的错误:
        - 如果 plugin_enum 不是预定义的枚举值，'_invoke_plugin' 方法可能无法正确地找到并执行对应的插件函数。
        
        """

        if plugin_enum not in self.plugin:
            return

        for pl in self.plugin[plugin_enum]:
            pl(base_wall, epoch_wall, batch_wall)

    @invoke_at([plugin_invoke_Enum.Begin])
    def _statistics(self, global_state: global_state_board, epoch_state: epoch_state_board,
                    step_state: step_state_board):
        """
        这是一个名为_statistics的函数，它的主要功能是统计和记录训练过程中模型的参数信息。
        
        参数：
        - `global_state`(global_state_board类型)：全局状态板，主要用于存放全局级别的训练信息，如模型、优化器等。
        - `epoch_state`(epoch_state_board类型)：历元状态板，主要用于存放每个历元级别的训练信息，如当前历元的损失值等。
        - `step_state`(step_state_board类型)：步骤状态板，主要用于存放每个训练步骤级别的训练信息，如当前步骤的损失值等。
        
        返回值：
        - 无
        
        函数首先创建了一个PrettyTable对象，用于格式化参数信息的输出。然后遍历优化器的参数组，统计每个参数的数量，并将其添加到PrettyTable中。在统计过程中，参数的总数量也被累加并存储在全局状态板的update_parameter_count属性中。最后，将总的参数数量也添加到PrettyTable中，并以日志的形式输出。
        
        注意：此函数不会返回任何值，它的主要目的是统计和记录训练过程中的参数信息，以便于后期分析和调试。
        
        示例代码：
        
        ```python
        # 创建一个trainer对象
        trainer = pymodel_trainer(model=model, loss_obj=loss, optimizer_type="adamw", learn_rate=0.01)
        
        # 创建全局、历元、步骤状态板
        global_state = global_state_board(...)
        epoch_state = epoch_state_board(...)
        step_state = step_state_board(...)
        
        # 调用_statistics函数
        trainer._statistics(global_state, epoch_state, step_state)
        ```
        """

        xtable = PrettyTable()
        xtable.field_names = ["name", "shape", "size", ]
        global_state.update_parameter_count = 0

        for group in global_state.optimizer.param_groups:
            param_count = sum(p.numel() for p in group['params'])
            xtable.add_row([group['name'], "", param_count])
            for p in group['params']:
                xtable.add_row(["", p.shape, p.numel()])
            global_state.update_parameter_count += param_count
        xtable.add_row(["total", "", global_state.update_parameter_count])
        log_multi_row("parameters info: \n" + str(xtable))

    def zero_grad(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        """
            这个方法用来将优化器中的所有梯度清零。在训练神经网络时，我们需要在每个更新步骤之前清零梯度，因为PyTorch在`.backward()`方法中会累加梯度，而不是替换它们。
        
            参数:
            - `global_state` (`global_state_board`): 全局状态板，包含了模型、优化器和其他全局状态信息。
            - `epoch_state` (`epoch_state_board`): 当前epoch的状态板，包含了当前epoch的信息，如当前epoch的损失，准确度等。
            - `step_state` (`step_state_board`): 当前步（batch）的状态板，包含了当前步的信息，如输入数据，目标标签，模型输出等。
        
            返回类型:
            无返回值。此方法主要用于更新全局状态板上的优化器的状态。
        
            示例:
            ```
            model_trainer = pymodel_trainer(model, loss_obj, optimizer_type="adam", learn_rate=0.01)
            for epoch in range(num_epochs):
                epoch_state = epoch_state_board(epoch)
                for step in range(num_steps):
                    step_state = step_state_board(step)
                    model_trainer.zero_grad(global_state, epoch_state, step_state)
                    ...
            ```
        """

        global_state.optimizer.zero_grad()

    def invoke_model(self, global_state: global_state_board, epoch_state: epoch_state_board,
                     step_state: step_state_board):
        """
        `invoke_model`是`pymodel_trainer`类中的一个方法，用于执行模型的前向传播过程。
        
        参数:
        - `global_state`(`global_state_board`类型的实例): 保存全局状态信息的实例，包含当前正在训练的模型等信息。
        - `epoch_state`(`epoch_state_board`类型的实例): 保存某一训练轮次(epoch)的状态信息的实例。本方法中未使用。
        - `step_state`(`step_state_board`类型的实例): 保存某一训练步骤(step)的状态信息的实例，包含了本步骤的输入数据等信息。
        
        返回值:
        - `Tensor`: 前向传播过程的输出结果。
        
        示例:
        ```python
        # 假设global_state, epoch_state, step_state已经初始化
        output = trainer.invoke_model(global_state, epoch_state, step_state)
        ```
        
        注意事项:
        - 本方法会根据`step_state`中的输入数据(`converted_input`)执行模型的前向传播过程，但并未处理模型的输出结果。具体的后处理过程(如损失函数的计算等)需要在调用本方法后自行进行。
        - `epoch_state`参数在本方法中未被使用，可以传入`None`。
        """

        return global_state.model(step_state.converted_input)

    def calculate_loss(self, global_state: global_state_board, epoch_state: epoch_state_board,
                       step_state: step_state_board):
        """
        `calculate_loss` 是 `pymodel_trainer` 类的一个成员方法。其功能是计算神经网络模型在给定输入和标签下的损失。
        
        参数:
        - `global_state`: 一个 `global_state_board` 对象。包含了模型的全局信息，如模型对象，损失函数对象，优化器对象等。
        - `epoch_state`: 一个 `epoch_state_board` 对象。包含了当前epoch的信息，如当前epoch的损失，当前epoch的编号等。
        - `step_state`: 一个 `step_state_board` 对象。包含了当前step的信息，如当前step的输入，当前step的输出，当前step的标签等。
        
        返回:
        - `loss`: 一个 Pytorch 的 Tensor 对象，表示模型在当前step的输入和标签下的损失。
        
        示例使用：
        ```python
        trainer = pymodel_trainer(model=my_model, loss_obj=my_loss)  # 创建训练器对象
        global_state = global_state_board(...)
        epoch_state = epoch_state_board(...)
        step_state = step_state_board(...)
        loss = trainer.calculate_loss(global_state, epoch_state, step_state)  # 计算损失
        ```
        
        注意：
        - 必须确保 `global_state` 中的 `loss_obj` 是一个有效的 Pytorch 的损失函数对象。
        - 必须确保 `step_state` 中的 `logit` 和 `converted_label` 是同形状的 Tensor，否则可能无法计算损失。
        - 目前没有发现该函数存在错误或bug。
        """

        return global_state.loss_obj(step_state.logit, step_state.converted_label)

    def backward(self, global_state: global_state_board, epoch_state: epoch_state_board,
                 step_state: step_state_board):
        """
        `backward`函数是`pymodel_trainer`类的一个方法。这个方法用于在给定的步骤状态下，将损失反向传播回模型中。反向传播是神经网络学习的关键步骤，它通过计算损失函数关于网络权重的梯度，来更新模型的参数。这个函数并不返回任何值，但它修改了`step_state`的状态。
        
        参数:
        
        - `global_state` (`global_state_board`): 全局状态板，存储了训练过程的全局信息，如模型，优化器等。
        - `epoch_state` (`epoch_state_board`): 存储了当前训练周期的状态信息，如当前是第几个训练周期，当前训练周期的损失等。
        - `step_state` (`step_state_board`): 存储了当前步骤的状态信息，如当前是第几步，当前步骤的输入，输出，损失等。
        
        返回值:
        
        - 无
        
        示例:
        
        ```python
        trainer = pymodel_trainer(model, loss_obj)
        for epoch in range(num_epochs):
            for step in range(num_steps):
                # forward pass
                output = trainer.invoke_model(global_state, epoch_state, step_state)
                # calculate loss
                loss = trainer.calculate_loss(global_state, epoch_state, step_state)
                # backward pass
                trainer.backward(global_state, epoch_state, step_state)
        ```
        
        错误和异常:
        
        - 如果`step_state.loss_tensor`不存在或者为None，会导致`backward()`函数调用失败。
        """

        step_state.loss_tensor.backward()

    def step(self, global_state: global_state_board, epoch_state: epoch_state_board,
             step_state: step_state_board):
        """
        `step` 方法是 `pymodel_trainer` 类的一个成员函数，用于执行一次模型的参数更新步骤。
        
        参数列表:
        
        - `global_state`: 是一个 `global_state_board` 实例，储存全局状态，包括模型、优化器、损失函数等信息。
        
        - `epoch_state`: 是一个 `epoch_state_board` 实例，储存当前周期的状态，比如周期损失等。
        
        - `step_state`: 是一个 `step_state_board` 实例，储存当前批处理步骤的状态，如输入、输出、损失值等。在本函数中并未被使用。
        
        此函数无返回值。
        
        函数工作流程:
        
        - 调用 `optimizer` 的 `step` 方法，按优化器设定的更新策略更新模型的参数。
        
        注意事项:
        
        - 本函数并未进行错误处理，如果在参数更新过程中出现错误，会引发运行时错误。
        
        使用示例:
        ```python
        trainer = pymodel_trainer(
            model=your_model,
            loss_obj=your_loss,
            optimizer_type='adamw',
        )
        while training:
            ...
            trainer.step(global_state, epoch_state, step_state)
            ...
        ```
        """

        global_state.optimizer.step()

    def train(self,
              sample_set: SampleSet,
              epoch=100,
              input_convert_func=lambda x: x,
              label_convert_func=lambda x: x
              ):
        """
        `train` 是 `pymodel_trainer` 类的一个方法，它负责训练模型。
        
        参数:
        - `sample_set (SampleSet)`: 训练集数据
        - `epoch (int)`: 训练的轮次(epochs)，默认为100
        - `input_convert_func (function)`: 转换输入数据的函数，默认为恒等函数
        - `label_convert_func (function)`: 转换标签数据的函数，默认为恒等函数
        
        返回类型:
        此函数没有返回值。
        
        使用例子:
        ```python
        trainer = pymodel_trainer(model, loss_obj)
        trainer.train(sample_set, epoch=50)
        ```
        
        注意事项:
        如果loss值不是一个tensor，将会抛出一个异常。在训练过程中，根据`update_mode`参数的设置，可能在每个步骤（step）或每个轮次（epoch）结束时更新模型参数。在每个步骤或轮次结束时，都会释放与该步骤或轮次相关的资源。
        """

        pb = process_status_bar()
        self.model.train()

        global_state = global_state_board(self, epoch, sample_set, pb, input_convert_func, label_convert_func)

        self._invoke_plugin(plugin_invoke_Enum.Begin, global_state, None, None)

        for epoch in pb.iter_bar(range(epoch), key='epoch'):

            epoch_state = epoch_state_board(epoch)

            self._invoke_plugin(plugin_invoke_Enum.Epoch_begin, global_state, epoch_state, None)

            if global_state.update_mode == update_mode_enum.Per_Epoch:
                self.zero_grad(global_state, epoch_state, None)
                # self.zero_grad(plugin_invoke_Enum.Epoch_begin, global_state, epoch_state, None)
                # global_state.optimizer.zero_grad()

            batch_size = global_state.batch_count
            batch_dataset = global_state.sample_set
            for idx, item in pb.iter_bar(enumerate(batch_dataset), key='batch', max=batch_size):
                batch_state = step_state_board(idx, item, global_state)

                batch_state.converted_input = global_state.input_convert_func(item)
                batch_state.converted_label = global_state.label_convert_func(item)

                self._invoke_plugin(plugin_invoke_Enum.Batch_begin, global_state, epoch_state, batch_state)

                # optimizer = base_wall['optimizer']
                # model = base_wall['model']
                # loss = base_wall['loss']

                # batch_X = batch_state.converted_input  # batch_wall['Convert_x']
                # batch_Y = batch_state.converted_label  # batch_wall['Convert_y']

                if global_state.update_mode == update_mode_enum.Per_Step:
                    self.zero_grad(global_state, epoch_state, batch_state)
                    # global_state.optimizer.zero_grad()

                # logit= model(batch_x)
                batch_state.logit = self.invoke_model(global_state, epoch_state, batch_state)

                # loss_tensor=loss(logit, batch_Y)
                loss_value = self.calculate_loss(global_state, epoch_state, batch_state)

                # loss_value= loss_tensor.item()
                if torch.is_tensor(loss_value):
                    batch_state.loss_value = loss_value.item()
                    batch_state.loss_tensor = loss_value
                else:
                    raise Exception("Loss must be a tensor.")

                epoch_state.epoch_loss += batch_state.loss_value

                batch_state.end_time = time.time()

                self.backward(global_state, epoch_state, batch_state)
                # accelerator.backward(loss_tensor)
                # loss_tensor.backward()

                self._invoke_plugin(plugin_invoke_Enum.After_Backward, global_state, epoch_state, batch_state)

                if global_state.update_mode == update_mode_enum.Per_Step:
                    self.step(global_state, epoch_state, batch_state)
                    # global_state.optimizer.step()
                    self._invoke_plugin(plugin_invoke_Enum.Update, global_state, epoch_state, batch_state)
                    global_state.parameter_update_times += 1

                global_state.step += 1
                self._invoke_plugin(plugin_invoke_Enum.Batch_end, global_state, epoch_state, batch_state)

                del batch_state

            if global_state.update_mode == update_mode_enum.Per_Epoch:
                self.step(global_state, epoch_state, None)
                # global_state.optimizer.step()
                self._invoke_plugin(plugin_invoke_Enum.Update, global_state, epoch_state, None)
                global_state.parameter_update_times += 1

            epoch_state.end_time = time.time()

            self._invoke_plugin(plugin_invoke_Enum.Epoch_end, global_state, epoch_state, None)

            del epoch_state

        self._invoke_plugin(plugin_invoke_Enum.End, global_state, None, None)

    def evaluate(self,
                 sample_set: SampleSet,
                 input_convert_func=lambda x: x,
                 label_convert_func=lambda x: x,
                 logit_convert_func=lambda x: x,
                 scores=[],
                 ):
        """
        这个函数是用于评估模型性能的方法。在评估过程中，它将对数据样本集合进行遍历，然后将每个样本送入模型进行预测。预测结果将被转化为类别标签，并与真实的类别标签进行比较，以计算各类评估指标，如准确率、精确率、召回率和F1分数等。
        
        参数:
            sample_set: SampleSet对象，用于存储需要进行评估的数据样本集合。
            input_convert_func: 函数对象，将用于对输入数据进行预处理。默认为恒等函数。
            label_convert_func: 函数对象，将用于对标签进行预处理。默认为恒等函数。
            logit_convert_func: 函数对象，将用于对模型输出的logits进行处理，从而得到预测的类别标签。默认为恒等函数。
            scores: 评估指标计算对象的列表。默认会至少包含AccuracyScores()，PrecisionScores()，RecallScores()，F1Scores()这四种。
        
        返回:
            这个函数将返回一个三元组，分别包含各类评价指标的结果、总体评价指标的结果以及混淆矩阵。
        
        示例:
            假设我们有一个已经训练好的模型model，和一个用于评估的数据集sample_set。我们可以通过以下代码来进行评估：
            ```python
            per_type_result, all_result, c_matrix = model.evaluate(sample_set)
            ```
            这样我们就可以得到每类的评价指标，总体评价指标以及混淆矩阵。
        """

        scores = [AccuracyScores(), PrecisionScores(), RecallScores(), F1Scores()] + scores

        evaluator = Evaluator(scores)

        pb = process_status_bar()
        self.model.eval()

        batch_dataset = sample_set
        batch_size = sample_set.count()

        global_state = global_state_board(self, -1, sample_set, pb, input_convert_func, label_convert_func)

        result_true_label = []
        result_predict_label = []

        for idx, item in pb.iter_bar(enumerate(batch_dataset), key='evaluate', max=batch_size):
            batch_state = step_state_board(idx, item, global_state)

            batch_state.converted_input = global_state.input_convert_func(item)
            batch_state.converted_label = global_state.label_convert_func(item)

            batch_state.logit = self.invoke_model(global_state, None, batch_state)

            logit_label = convert_to_list(logit_convert_func(batch_state.logit))
            true_label = convert_to_list(batch_state.converted_label)

            for t_v, p_v in zip(true_label, logit_label):
                result_true_label.append(t_v)
                result_predict_label.append(p_v)

        per_type_result = evaluator.get_per_result(result_true_label, result_predict_label)
        all_result, c_matrix = evaluator.get_all_result(result_true_label, result_predict_label,
                                                        return_confusion_matrix=True)

        return per_type_result, all_result, c_matrix
