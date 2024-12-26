# pass_generate
import abc
from typing import List


class ScoreAbstractClass(metaclass=abc.ABCMeta):
    """
    这是一个抽象类ScoreAbstractClass，它定义了一个评分系统的基本接口。它使用了抽象类元类abc.ABCMeta，强制要求所有子类必须实现定义的抽象方法。这个类主要用于规范和定义评分系统的基本结构，为实际的评分系统提供统一的调用方式。
    
    它定义了两个抽象方法:
    
    1. Name: 这是一个property装饰的方法，要求所有子类必须提供一个名为Name的属性。这个属性返回一个str类型，用于描述这个评分系统的名称。
    
    2. get_score: 这是一个需要子类实现的方法，它接收一个名为confusion_matrix的参数，并返回一个列表类型的评分结果。
    
    示例:
    
        class MyScore(ScoreAbstractClass):
            @property
            def Name(self) -> str:
                return "MyScoreName"
    
            def get_score(self, confusion_matrix) -> []:
                return [1, 2, 3] # 自定义的评分逻辑
    
        my_score = MyScore()
        print(my_score.Name)  # 输出: MyScoreName
        print(my_score.get_score(None))  # 输出: [1, 2, 3]
    """

    @property
    @abc.abstractmethod
    def Name(self) -> str:
        """
        这是一个抽象方法，需要在子类中实现。
        
        返回：
            str：返回评分标准的名称。
        
        注意事项：
            这是一个抽象属性，不能直接使用，需要在子类中实现。
        
        错误或异常：
            如果在子类中没有实现这个方法，那么在实例化子类的时候，会抛出TypeError异常。
        
        示例：
        ```python
        class AccuracyScore(ScoreAbstractClass):
        
            @property
            def Name(self) -> str:
                return 'accuracy'
        ```
        在上面的示例中，我们创建了一个名为AccuracyScore的子类，并在子类中实现了Name方法，返回了'accuracy'字符串。
        """

        pass

    @abc.abstractmethod
    def get_score(self, confusion_matrix) -> []:
        """
        这是一个抽象方法，需要在子类中实现。目的是根据输入的混淆矩阵，计算并返回分数。
        
        参数:
            confusion_matrix (list): 混淆矩阵，是一个二维列表。
        
        返回:
            list: 根据混淆矩阵计算得到的分数，返回值类型为列表。
        
        示例:
            class ScoreConcreteClass(ScoreAbstractClass):
                @property
                def Name(self):
                    return 'ScoreConcreteClass'
        
                def get_score(self, confusion_matrix):
                    # 计算并返回分数
                    pass
            score_concrete_class = ScoreConcreteClass()
            score = score_concrete_class.get_score([[1, 0], [0, 1]])
        """

        pass


class Evaluator:
    """
    这是一个评估器类(Evaluator)，用于处理分类问题的评估。
    
    这个类的主要目的是计算出分类问题的混淆矩阵，并基于这个混淆矩阵，计算出一系列分类评价指标的结果。
    这个类需要在初始化时传入一个评价指标方法列表，这个列表中的每个元素都应该是一个继承自ScoreAbstractClass的实例对象，每个对象都应实现了get_score方法。
    
    这个类主要有三个方法，分别是：get_confusion_matrix，get_per_result和get_all_result。
    
    - get_confusion_matrix方法：计算出分类问题的混淆矩阵。
      参数有两个，分别是真实标签列表和预测标签列表。
      返回两个值，一个是标签到索引的映射字典，另一个是混淆矩阵。
    
    - get_per_result方法：计算出每个类别的评价指标结果。
      参数有三个，分别是真实标签列表，预测标签列表，以及一个可选的return_confusion_matrix参数，默认为False，表示是否返回混淆矩阵。
      返回一个包含每个评价指标结果的字典，如果return_confusion_matrix为True，还会返回混淆矩阵。
    
    - get_all_result方法：计算出所有类别的平均评价指标结果。
      参数有三个，分别是真实标签列表，预测标签列表，以及一个可选的return_confusion_matrix参数，默认为False，表示是否返回混淆矩阵。
      返回一个包含所有类别平均评价指标结果的字典，如果return_confusion_matrix为True，还会返回混淆矩阵。
    
    示例：
    ```python
    class MyScore(ScoreAbstractClass):
        def get_score(self, confusion_matrix):
            # 实现自己的评价指标计算方法
            pass
    
    my_score = MyScore()
    evaluator = Evaluator([my_score])
    true_labels = [0, 1, 0, 1, 0, 1]
    predict_labels = [0, 1, 1, 0, 0, 1]
    print(evaluator.get_all_result(true_labels, predict_labels))
    ```
    """

    def __init__(self, score_methods: [ScoreAbstractClass]):
        """
        初始化Evaluator类。
        
        Evaluator类是一个评价器，其目的在于计算分类模型的性能。它可以计算多个评分方法并返回结果。对于每个评分方法，Evaluator类将计算混淆矩阵，并根据这个混淆矩阵得到每个类别的评分结果。
        
        参数:
            score_methods (list[ScoreAbstractClass]): 评分方法类的列表，每个类都应该从ScoreAbstractClass继承，并实现get_score方法。
        
        例子:
            >>> from sklearn.metrics import accuracy_score, precision_score
            >>> evaluator = Evaluator([accuracy_score, precision_score])
            >>> true_labels = [0, 1, 1, 1, 0]
            >>> predict_labels = [0, 1, 0, 1, 1]
            >>> result = evaluator.get_all_result(true_labels, predict_labels)
            >>> print(result)
            {'accuracy_score': 0.6, 'precision_score': 0.6666666666666666}
        """

        self.all_scores = score_methods

    def get_confusion_matrix(self, true_labels: list, predict_labels: list) -> (dict, list):
        """
        该方法用于生成混淆矩阵。混淆矩阵是一种常用的模型评估工具，特别是在处理多类别分类问题时。混淆矩阵显示了模型预测的类别和实际类别的对应情况。
        
        参数:
            true_labels (list): 真实的标签列表。
            predict_labels (list): 模型预测的标签列表。
        
        返回:
            (dict, list): 返回一个元组，第一个元素是一个字典，包含所有唯一标签及其在混淆矩阵中的索引；第二个元素是一个二维列表，表示混淆矩阵，其行和列的顺序与第一个元素中标签的顺序一致。
        
        例子:
        
            >>> evaluator = Evaluator([ScoreClass()])
            >>> true_labels = ['dog', 'cat', 'dog', 'fish']
            >>> predict_labels = ['dog', 'fish', 'dog', 'cat']
            >>> evaluator.get_confusion_matrix(true_labels, predict_labels)
            ({'fish': 0, 'dog': 1, 'cat': 2}, [[0, 0, 1], [0, 2, 0], [1, 0, 0]])
        
        在这个示例中，'fish', 'dog', 'cat'分别在混淆矩阵中的索引为0,1,2。混淆矩阵表示'fish'被预测为'cat'一次，'dog'被正确预测两次，'cat'被预测为'fish'一次。
        
        注意：
            如果输入的真实标签和预测标签的数量不一致，将可能出现错误。
        
        """

        # 找出所有的唯一标签
        unique_labels = list(set(true_labels + predict_labels))

        # 创建一个空的混淆矩阵
        confusion_matrix = [[0 for _ in range(len(unique_labels))] for _ in range(len(unique_labels))]

        # 创建一个字典来存储每个类别的索引
        label_to_index = {label: index for index, label in enumerate(unique_labels)}

        # 填充混淆矩阵
        for t, p in zip(true_labels, predict_labels):
            i = label_to_index[t]
            j = label_to_index[p]
            confusion_matrix[i][j] += 1

        return label_to_index, confusion_matrix

    def get_per_result(self, true_labels: list, predict_labels: list, return_confusion_matrix=False):
        """
        该函数主要用于获取每个类别的评分结果。首先，它会生成一个混淆矩阵，然后根据所有预定义的评分方法计算每个类别的评分，并将结果存储在字典中。
        
        参数:
            true_labels (list): 真实标签列表。
            predict_labels (list): 预测标签列表。
            return_confusion_matrix (bool): 是否返回混淆矩阵，默认为False。
        
        返回:
            如果return_confusion_matrix为True，那么返回一个元组，包括一个字典和一个混淆矩阵。字典的键是评分名称，值是另一个字典，里面包含每个类别的评分。混淆矩阵是一个二维列表，表示混淆矩阵的每个元素。
            如果return_confusion_matrix为False，那么只返回一个字典，其结构与上述相同。
        
        示例:
            evaluator = Evaluator([ScoreMethod1(), ScoreMethod2()])
            result_dict, confusion_matrix = evaluator.get_per_result(true_labels, predict_labels, return_confusion_matrix=True)
            print(result_dict)
            print(confusion_matrix)
        """

        mapping, confusion_matrix = self.get_confusion_matrix(true_labels, predict_labels)

        result_dict = {}
        for score in self.all_scores:
            score_name = score.Name
            score_result = score.get_score(confusion_matrix)
            result_dict[score_name] = {k: score_result[v] for k, v in mapping.items()}

        if return_confusion_matrix:
            return result_dict, confusion_matrix
        return result_dict

    def get_all_result(self, true_labels: list, predict_labels: list, return_confusion_matrix=False):
        """
        此函数是`Evaluator`类的一个方法，用于获取模型在所有类别上的预测结果。
        
        参数:
            true_labels (list): 真实标签的列表。
            predict_labels (list): 模型预测的标签列表。
            return_confusion_matrix (bool, 可选): 是否返回混淆矩阵。默认为False。
        
        返回:
            返回一个包含每一个评分方法名称及其对应结果的字典；当`return_confusion_matrix`设为True时，同时返回混淆矩阵。
        
        此函数首先调用`get_per_result`方法获取每个类别的评分结果，然后计算所有类别的平均分，并存储为一个新的字典。字典的键是评分方法的名称，值是该评分方法在所有类别上的平均分。如果某类别的评分不存在，将其值设为None。
        
        示例:
        ```
        e = Evaluator([score_method1, score_method2])
        result = e.get_all_result(true_labels, predict_labels)
        ```
        """

        per_result, confusion_matrix = self.get_per_result(true_labels, predict_labels, return_confusion_matrix=True)
        new_dict = {}
        for key, v in per_result.items():
            totle = 0
            ty_count = len(v.keys())
            for ty, tyv in v.items():
                if tyv:
                    totle += tyv
            if ty_count != 0:
                new_dict[key] = totle / ty_count
            else:
                new_dict[key] = None
        if return_confusion_matrix:
            return new_dict, confusion_matrix

        return new_dict
