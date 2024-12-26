# pass_generate
from tketool.pyml.pytrainer import *
from tketool.evaluate.scores import *
from tketool.pyml.utils import convert_to_list


class classification_evalution_trainset(trainer_plugin_base):
    """
    这是一个用于训练集分类评估的类classification_evalution_trainset，继承自trainer_plugin_base类。
    
    这个类主要是用来计算和记录训练过程中的各类评估指标，包括准确率、精度、召回率和F1分数，并将各类评估指标的结果绘制成图表。它有三个主要的方法：begin、batch_end和epoch_end，分别在训练开始、每个批次结束和每个周期结束时被调用。
    
    - __init__方法是类的初始化方法，设置了一些基本的属性，包括logit_convert_func函数、epoch_result_true_label列表、epoch_result_predict_label列表、scores列表和evaluator评估器。
    
    - begin方法在训练开始时被调用，它会为每种评估指标创建一个空列表，用于存储指标的计算结果。
    
    - batch_end方法在每个批次结束时被调用，它会将当前批次的预测结果和真实结果添加到对应的列表中。
    
    - epoch_end方法在每个周期结束时被调用，它会计算当前周期的所有评估指标，然后将计算结果添加到图表数据中，并清空存储预测结果和真实结果的列表，为下一个周期的计算做准备。
    
    使用示例：
    ```python
    classification_evaluator = classification_evalution_trainset()
    classification_evaluator.begin(global_state, epoch_state, step_state)
    for batch in batches:
        classification_evaluator.batch_end(global_state, epoch_state, step_state)
    classification_evaluator.epoch_end(global_state, epoch_state, step_state)
    ```
    
    注意：这个类需要配合trainer_plugin_base类和Evaluator类使用，而且在使用前需要确保全局状态、周期状态和步骤状态的设置是正确的。
    """

    def __init__(self, logit_convert_func=lambda x: x):
        """
        这是一个构造函数，用于初始化classification_evalution_trainset类的实例。
        
        分类评估训练集类用于对分类模型的训练结果进行评估，包括准确度、精确度、召回率和F1分数等指标的计算。
        
        该类的实例会在训练过程中进行调用，以记录每个批次和每个周期的训练结果，并在全局状态板上展示这些结果。
        
        参数:
            logit_convert_func (function, 默认值是lambda x: x): 一个函数，用于将预测结果（logit）转换为预测标签。默认的转换函数是lambda x: x，即不做任何转换。
        
        属性:
            logit_convert_func (function): logit转换函数。
            epoch_result_true_label (list): 真实标签的列表，用于记录每个周期的真实标签。
            epoch_result_predict_label (list): 预测标签的列表，用于记录每个周期的预测标签。
            scores (list): 评估指标列表，包括准确度、精确度、召回率和F1分数。
            evaluator (Evaluator): 评估器，用于计算每个周期的评估指标。
        
        使用示例：
        ```python
        # 创建一个分类评估训练集实例，使用自定义的logit转换函数
        evaluator = classification_evalution_trainset(logit_convert_func=my_convert_func)
        ```
        
        注意：
        无已知错误或bug。
        """

        self.logit_convert_func = logit_convert_func
        self.epoch_result_true_label = []
        self.epoch_result_predict_label = []

        self.scores = [AccuracyScores(), PrecisionScores(), RecallScores(), F1Scores()]
        self.evaluator = Evaluator(self.scores)

    @invoke_at([plugin_invoke_Enum.Begin])
    def begin(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        """
        这是一个类方法，用于在训练过程的开始阶段进行一些初始化工作。具体来说，该方法是在训练的每个epoch开始时被调用的，它会为每一个评估指标创建一个空的列表，用于存储每个epoch的评估结果。这些评估结果随后会被用于生成训练过程的图表数据。
        
        参数:
        - global_state (global_state_board): 全局状态板实例，用于存储全局的训练状态，如学习率、训练集和验证集的损失等。
        - epoch_state (epoch_state_board): epoch状态板实例，用于存储当前epoch的训练状态，如当前epoch的损失、准确率等。
        - step_state (step_state_board): 步骤状态板实例，用于存储当前步骤的训练状态，如当前步的输入、输出、损失等。
        
        返回:
        - 返回类型是None。
        
        例子:
        - 如果你的评估指标有accuracy、precision、recall和f1 score，那么在开始阶段，global_state.chart_datas将会被初始化为{'accuracy': [], 'precision': [], 'recall': [], 'f1 score': []}。
        """

        for sc in self.scores:
            name = sc.Name
            global_state.chart_datas[name] = []

    @invoke_at([plugin_invoke_Enum.Batch_end])
    def batch_end(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        """
        `batch_end` 是一个方法,用在每次批量处理数据后. 它从`step_state`中获取预测的输出（logit）和实际标签（true label），并以列表形式存储它们，以便在后续的评估阶段使用。
        
        参数：
        - `global_state` (global_state_board)：全局状态板，它存储了全局的数据，如整个训练过程的图表数据。
        - `epoch_state` (epoch_state_board)：时代状态板，它存储了当前时代的数据。在这个方法中并未使用。
        - `step_state` (step_state_board)：步骤状态板，它存储了当前步骤（或称之为批次）的数据，如logit（即模型的输出）和converted_label（即实际标签）。
        
        返回：
        - 无
        
        在这个方法中，它首先将logit和实际标签转换为列表形式，然后将其添加到`self.epoch_result_true_label`和`self.epoch_result_predict_label`中，这两个列表存储了一个epoch的所有步骤（或批次）的结果，用于在epoch结束时进行模型评估。
        
        注意：这个方法不返回任何值，它只是处理和存储数据。
        
        示例：
        
        以下是如何使用此方法的一个示例：
        
        ```python
        # 假设我们有一个classification_evaluation_trainset的实例
        trainer = classification_evaluation_trainset()
        
        # 假设我们有一些全局，时代和步骤状态
        global_state = ...
        epoch_state = ...
        step_state = ...
        
        # 我们可以在每个批次结束后调用这个方法
        trainer.batch_end(global_state, epoch_state, step_state)
        ```
        """

        logit_label = convert_to_list(self.logit_convert_func(step_state.logit))
        true_label = convert_to_list(step_state.converted_label)

        for t_v, p_v in zip(true_label, logit_label):
            self.epoch_result_true_label.append(t_v)
            self.epoch_result_predict_label.append(p_v)

    @invoke_at([plugin_invoke_Enum.Epoch_end])
    def epoch_end(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        """
        这个函数定义了在每个训练周期结束时的操作。
        
        函数参数:
            global_state (global_state_board): 全局状态，用于存储整个训练过程中的信息，例如图表数据等。
            epoch_state (epoch_state_board): 当前训练周期的状态，包含了当前周期的训练信息。
            step_state (step_state_board): 当前训练步骤的状态，包含了当前训练步骤的信息。
        
        该函数首先会根据当前训练周期的真实标签和预测标签，通过Evaluator计算出所有评价指标的结果，并存储在result中。然后，遍历result, 将每个评价指标的结果添加到全局状态的图表数据中。最后，清空当前训练周期的真实标签和预测标签，为下一周期的训练做准备。
        
        无返回值。
        
        使用示例：
            在训练过程中，每当一个训练周期结束时，都会调用该函数来处理周期结束时的操作。
        
        注意：
            该函数假设step_state中的logit已经被转换成了标签格式，如果没有转换，可能会影响结果的正确性。
        """

        result = self.evaluator.get_all_result(self.epoch_result_true_label, self.epoch_result_predict_label)

        for key, sc_val in result.items():
            global_state.chart_datas[key].append(sc_val)

        self.epoch_result_true_label = []
        self.epoch_result_predict_label = []
