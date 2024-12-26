# pass_generate
from tketool.evaluate.EvalutionBase import *


class AccuracyScores(ScoreAbstractClass):
    """
    这是一个名为AccuracyScores的类，该类继承自ScoreAbstractClass抽象类。AccuracyScores类的主要目的是通过传入的混淆矩阵来计算和返回每个类别的精度。
    
    每个类别的精度是通过混淆矩阵的对角线上的元素（正确分类的数量）除以该类别总的预测数量来得到的。
    
    如果某类别没有预测（即混淆矩阵的某行和为0），则其精度被设置为None。
    
    类方法介绍：
    
    - `Name`：这是一个属性方法，返回评分类的名称，即"Accuracy"。
    
    - `get_score`：这个方法接受一个混淆矩阵作为输入，返回一个列表，列表中的每个元素代表每个类别的精度。如果某类别没有预测（即混淆矩阵的某行和为0），则其精度被设置为None。
    
    使用示例：
    
    假设我们有一个二分类问题的混淆矩阵[[5, 2], [3, 7]]，我们可以通过以下方式使用 AccuracyScores 类来计算每个类别的精度：
    
    ```python
    confusion_matrix = [[5, 2], [3, 7]]
    accuracy_scores = AccuracyScores()
    accuracies = accuracy_scores.get_score(confusion_matrix)
    print(accuracies)
    ```
    
    输出结果为：[0.7142857142857143, 0.7]，表示类别1的精度为0.71，类别2的精度为0.7。
    """

    @property
    def Name(self) -> str:
        """
        这是一个类方法，用于获取当前类的名称。
        
        返回:
            str: 返回字符串 "Accuracy"，作为当前类的名称。
        """

        return "Accuracy"

    def get_score(self, confusion_matrix) -> []:
        """
        此函数是 `AccuracyScores` 类的一个方法，用于根据混淆矩阵计算并返回每个类别的精确度。
        
        参数:
            confusion_matrix (list): 是一个二维列表，表示混淆矩阵。混淆矩阵的行对应真实类别，列对应预测类别。每一行的总和即为该类别的总预测次数。
        
        返回:
            list: 一个列表，其中包含每个类别的精确度。列表的索引i对应的是第i类的精确度。如果某个类别的总预测次数为0，则返回None。
        
        示例:
        ```python
        confusion_matrix = [[10, 2, 3], [0, 8, 1], [0, 1, 9]]
        accuracy_scores = AccuracyScores()
        print(accuracy_scores.get_score(confusion_matrix))  # 输出：[0.6666666666666666, 0.8888888888888888, 0.9]
        ```
        
        注意:
            如果混淆矩阵的某一行（即某一类）的总预测次数为0，表示没有对该类进行预测，此时该类的精确度无法计算，我们将其设置为None。如果你希望在这种情况下返回其他值，可以修改以下代码：
            ```python
            accuracies.append(None)  # 或设为你希望在这种情况下返回的其他值
            ```
        """

        # 计算并返回每个类别的精度
        accuracies = []
        for i, row in enumerate(confusion_matrix):
            total_predictions = sum(row)
            if total_predictions == 0:
                accuracies.append(None)  # 或设为你希望在这种情况下返回的其他值
            else:
                accuracies.append(confusion_matrix[i][i] / total_predictions)
        return accuracies


class PrecisionScores(ScoreAbstractClass):
    """
    这是一个名为PrecisionScores的类，它继承了ScoreAbstractClass抽象类。这个类的目的是用来计算和返回混淆矩阵中的准确度得分。
    
    Properties:
        Name : str
            返回字符串"Precision"，表示这个类的名称。
    
    Functions:
        get_score(self, confusion_matrix) -> list:
            这个函数接收一个混淆矩阵作为输入，计算并返回一个列表，其中包含了每个类的精确度得分。
    
    参数：
        confusion_matrix : list
            这是一个二维列表，代表混淆矩阵。它的行表示实际的类别，列表示预测的类别。
    
    返回：
        precisions : list
            这是一个列表，其中包含了每个类的精确度得分。精确度得分是由真正例数除以预测正例数得到的。如果预测的正例数为0，则该类别的精确度得分为None。
    
    例如：
        如果我们有一个二分类问题的混淆矩阵[[1, 2], [0, 2]]，那么对于第一个类别，真正例数为1，预测正例数为1，所以精确度得分为1/1=1。对于第二个类别，真正例数为2，预测正例数为4，所以精确度得分为2/4=0.5。所以，这个函数会返回列表[1, 0.5]。
    
    注意：这个类需要ScoreAbstractClass抽象类作为父类，所以确保在使用前已经导入了这个抽象类。
    """

    @property
    def Name(self) -> str:
        """
                此函数是PrecisionScores类的一个方法，用于返回字符串"Precision"。
        
                方法的返回类型为字符串。
        
                Args:
                    self: 代表类的实例。
        
                Returns:
                    返回字符串 "Precision"。
        
                Example:
                    precision_scores = PrecisionScores()
                    name = precision_scores.Name
                    print(name) # 输出 "Precision"
        """

        return "Precision"

    def get_score(self, confusion_matrix) -> list:
        """
        该函数用于计算精确度分数。精确度分数是评估预测模型分类结果质量的一个重要指标，其定义为：在预测为正类的样本中，真实为正类的比例。
        
        参数:
        confusion_matrix (list): 混淆矩阵，二维数组，每一行对应真实类，每一列对应预测类。对角线元素表示预测结果与真实情况相符的数量。
        
        返回:
        list: 返回一个列表，列表的每一个元素对应一个类别的精确度。如果某个类别没有正例预测，则返回None。
        
        举例：
        假设我们有一个混淆矩阵[[5, 2, 0], [3, 7, 1], [2, 4, 9]]，代表有3个类别，分别为类别0，类别1，类别2。那么，这个函数会返回一个列表，里面的三个值分别对应这三个类别的精确度。
        """

        precisions = []
        for i in range(len(confusion_matrix)):
            pred_positive = sum(confusion_matrix[j][i] for j in range(len(confusion_matrix)))
            true_positive = confusion_matrix[i][i]
            if pred_positive == 0:
                precisions.append(None)
            else:
                precisions.append(true_positive / pred_positive)
        return precisions


class RecallScores(ScoreAbstractClass):
    """
    这是一个名为 `RecallScores` 的类，继承自 `ScoreAbstractClass`。这个类的主要目的是为了计算并返回“召回率”（Recall）。
    
    “召回率”是在所有正样本中，预测为正样本的比率。它是衡量模型对正样本的预测能力，也是评估模型性能的重要指标之一。
    
    这个类有两个主要的方法，一个是 `Name`，一个是 `get_score`:
    
    - `Name` 方法是一个属性方法，返回的是字符串 "Recall"。
    
    - `get_score` 方法是用来根据输入的 `confusion_matrix`（混淆矩阵）计算召回率的。它返回的是一个召回率的列表，列表中的每一个元素对应混淆矩阵中每一行的召回率。
    
    使用方法：
    假设我们有一个混淆矩阵 `cm`，我们可以这样来获取召回率：
    
    ```python
    recall_scores = RecallScores()
    recalls = recall_scores.get_score(cm)
    print(recalls)
    ```
    
    注意：
    如果在计算召回率时，某一行的实际正样本总数（即混淆矩阵一行的和）为0，那么这一行的召回率会被设置为None。
    
    参数列表：
    - `confusion_matrix`：2维列表，表示混淆矩阵，真实值和预测值的组合情况。
    
    返回类型：
    - `get_score` 返回一个列表，列表中的每一个元素对应混淆矩阵中每一行的召回率，如果某行的实际正样本总数为0，则对应的召回率为None。
    """

    @property
    def Name(self) -> str:
        """
        这是一个属性方法，用于获取当前类的名称。
        
        返回:
            str: 返回字符串 "Recall"，表示这个类的名称。
        """

        return "Recall"

    def get_score(self, confusion_matrix) -> list:
        """
            `get_score` 是 `RecallScores` 类中的一个方法，用于从混淆矩阵中计算每一类的召回率。
        
            召回率是一个重要的评价指标，用于衡量我们的模型预测正例的能力。召回率的公式为TP/(TP+FN)，其中TP代表真正例（实际为正例且被正确预测为正例的数量），FN代表假负例（实际为正例但被错误预测为负例的数量）。因此，get_score方法通过遍历混淆矩阵的每一行（每一类），并计算每一行的真正例数除以行内元素总和（真正例数 + 假负例数）来得到每一类的召回率。
        
            如果某一类的真实样本总数（行内元素总和）为0，我们将该类的召回率记为None。
        
            参数：
                confusion_matrix (list of list of int): 混淆矩阵，每一行代表一个类别，每一行内的元素总和代表该类别的真实样本总数，行内对角线元素代表该类别的真正例数。
        
            返回:
                list: 返回一个列表，包含每一类的召回率。
        
            示例:
                confusion_matrix = [[2, 1], [1, 2]]
                执行 get_score(confusion_matrix)
                返回结果为 [2/3, 2/3]
        
            注意:
                如果混淆矩阵的输入不正确（例如，不是一个二维矩阵），或者混淆矩阵中包含负数，代码可能会出错。
            """

        recalls = []
        for i, row in enumerate(confusion_matrix):
            actual_positive = sum(row)
            true_positive = row[i]
            if actual_positive == 0:
                recalls.append(None)
            else:
                recalls.append(true_positive / actual_positive)
        return recalls


class F1Scores(ScoreAbstractClass):
    """
    这是一个计算F1分数的类，继承自ScoreAbstractClass。F1分数是精确度和召回率的调和平均数，是评价模型性能的一种常用指标。
    
    类方法：
    - `Name`：返回评分方法的名字，即"F1"。
    - `get_score`：根据混淆矩阵计算F1分数。
    
    属性：
    - `Name`：评分方法的名字。
    
    方法：
    - `get_score(self, confusion_matrix)`：计算F1分数。
      - 参数：
        - `confusion_matrix`：混淆矩阵。
      - 返回：
        - `f1_scores`：F1分数列表。
    
    使用示例：
    ```python
    f1_score_calculator = F1Scores()
    f1_scores = f1_score_calculator.get_score(confusion_matrix)
    ```
    注意：在计算F1分数时，如果精确度和召回率中任何一个为None，或者两者之和为0，则F1分数为None。
    
    """

    @property
    def Name(self) -> str:
        """
        此方法是F1Scores类的一个属性方法。这个方法没有参数，它返回一个字符串，代表这个评分类的名称，即"F1"。这个名称可能被用于报告或者和其他评分方法进行比较。
        
        返回:
            str: 返回"F1"，代表F1分数。
        
        示例:
            f1_calculator = F1Scores()
            print(f1_calculator.Name)  # 输出 "F1"
        
        注意:
            这个方法不接受任何参数，也不会改变对象的状态，只是提供一个固定的字符串。同时，作为一个属性方法，你不需要在调用时加括号。
        """

        return "F1"

    def get_score(self, confusion_matrix) -> list:
        """
        这个`get_score`方法是在`F1Scores`类中定义的，该类继承自`ScoreAbstractClass`。该方法的主要目的是计算给定混淆矩阵的F1得分。
        
        参数:
            confusion_matrix (list): 需要计算得分的混淆矩阵。混淆矩阵是一个二维数组，每个元素表示预测类别和真实类别的匹配情况。
        
        返回:
            list: F1得分的列表。每个元素对应混淆矩阵中某个类别的F1得分。如果计算不出精确度或召回率，或者它们的和为零，对应的F1得分为None。
        
        此方法首先使用`PrecisionScores`和`RecallScores`类计算混淆矩阵的精确度和召回率。然后，对于每个类别，使用以下公式计算F1得分：
            F1 = 2 * ((precision * recall) / (precision + recall))
        
        示例:
            confusion_matrix = [[1, 2], [3, 4]]
            f1_scores_calculator = F1Scores()
            f1_scores = f1_scores_calculator.get_score(confusion_matrix)
            print(f1_scores) # 输出: [0.6666666666666666, 0.5714285714285715]
        
        请注意，此方法假设`PrecisionScores`和`RecallScores`的`get_score`方法返回的列表长度与混淆矩阵中的类别数量相同。如果这个假设不成立，那么此方法可能会引发错误。
        
        此方法还可能返回包含None的列表，这时因为无法计算某个类别的F1得分。在处理返回的F1得分列表时，应当特别注意这一点。
        """

        f1_scores = []
        precisions_calculator = PrecisionScores()
        recalls_calculator = RecallScores()

        precisions = precisions_calculator.get_score(confusion_matrix)
        recalls = recalls_calculator.get_score(confusion_matrix)

        for precision, recall in zip(precisions, recalls):
            if precision is None or recall is None or (precision + recall) == 0:
                f1_scores.append(None)
            else:
                f1_scores.append(2 * ((precision * recall) / (precision + recall)))
        return f1_scores
