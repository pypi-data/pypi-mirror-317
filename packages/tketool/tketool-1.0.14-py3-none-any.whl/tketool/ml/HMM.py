# pass_generate
from typing import Callable, List
import numpy as np
from tketool.ml.modelbase import Model_Base
from hmmlearn.hmm import CategoricalHMM
import abc
import inspect
import functools


def _normalized(list_a):
    """
    这是一个归一化函数，用于将输入列表的所有元素归一化，使得所有元素的和为1。

    参数:
        list_a (list): 输入的列表，元素需要是可被转化为numpy数组的数字。

    返回:
        numpy.ndarray or int: 归一化后的numpy数组，如果输入列表的元素之和为0，则返回0。

    使用示例:
        >>> _normalized([1, 2, 3])
        array([0.16666667, 0.33333333, 0.5])

    注意:
        - 如果输入的列表为空，或者所有元素都是0，函数将返回0。
        - 该函数没有错误处理机制，如果输入的列表中包含无法转化为数字的元素，将会引发错误。
    """

    arr = np.array(list_a)
    sum_arr = np.sum(arr)
    if sum_arr == 0:
        return 0
    else:
        return arr / sum_arr


# class HMM_Base(Model_Base):
#     """
#     这是一个基类，用于实现隐马尔可夫模型(Hidden Markov Model, HMM)。这个类定义了HMM模型所需要的基本参数和抽象方法。
#
#     属性:
#         init_prob: 初始概率分布。存储在一个字典中，键为隐藏状态，值为每个隐藏状态的初始概率。
#
#         trans_prob: 转移概率分布。存储在一个字典中，键为隐藏状态对，值为从一个隐藏状态转移到另一个隐藏状态的概率。
#
#         emission_prob: 发射概率分布。存储在一个字典中，键为隐藏状态，值为每个隐藏状态发出每个可能的观测的概率。
#
#         state_count: 隐藏状态的数量。
#
#     方法:
#         seq_match(self, X): 抽象方法，需要子类实现。根据给定的观测序列，计算最有可能的隐藏状态序列。
#
#         seq_decode(self, X): 抽象方法，需要子类实现。根据给定的观测序列，解码出最有可能的隐藏状态序列。
#
#         train(self, X, *args): 抽象方法，需要子类实现。根据给定的观测序列，训练HMM模型的参数。
#
#         init_model(self, hidden_state_count: int, *args): 抽象方法，需要子类实现。初始化HMM模型的参数。
#
#         load_init_model(self, path_or_stream): 抽象方法，需要子类实现。从给定的路径或流中加载先前初始化的HMM模型。
#
#     使用示例:
#         ```
#         class HMM(HMM_Base):
#             def seq_match(self, X):
#                 # 实现seq_match方法
#                 pass
#             def seq_decode(self, X):
#                 # 实现seq_decode方法
#                 pass
#             def train(self, X, *args):
#                 # 实现train方法
#                 pass
#             def init_model(self, hidden_state_count: int, *args):
#                 # 实现init_model方法
#                 pass
#             def load_init_model(self, path_or_stream):
#                 # 实现load_init_model方法
#                 pass
#         hmm = HMM()
#         ```
#     """
#
#     def __init__(self):
#         """
#         这是一个基础的隐马尔可夫模型类(HMM_Base)，继承自Model_Base类。
#         该类定义了HMM模型的基本属性，如初始概率、转移概率、发射概率和状态数量等。
#         同时，也定义了一些抽象方法，如序列匹配、序列解码、训练模型、初始化模型和加载模型等，具体的实现需要在子类中完成。
#
#         类属性：
#             init_prob：初始概率
#             trans_prob：转移概率
#             emission_prob：发射概率
#             state_count：状态数量
#
#         抽象方法：
#             seq_match(self, X)：序列匹配
#             seq_decode(self, X)：序列解码
#             train(self, X, *args)：训练模型
#             init_model(self, hidden_state_count: int, *args)：初始化模型
#             load_init_model(self, path_or_stream)：加载模型
#
#         使用示例：
#         假设我们有一个子类HMM，并已经实现了上述的抽象方法。我们可以这样使用：
#
#         ```python
#         hmm = HMM()
#         hmm.init_model(hidden_state_count=3)
#         hmm.train(X)
#         decoded_sequence = hmm.seq_decode(X)
#         ```
#
#         注意：
#         - 该类自身无法直接使用，需要在子类中实现所有的抽象方法后才可以使用。
#         - 在使用前，必须先进行模型的初始化，否则会出现错误。
#         """
#
#         super().__init__()
#
#     @property
#     def init_prob(self):
#         """
#         HMM_Base类中的init_prob()函数是一个计算属性，用于获取初始化概率。
#
#         参数:
#         无
#
#         返回:
#         返回HMM模型的初始化概率。这是一个字典，以状态名称作为键，对应的初始化概率作为值。
#
#         注意:
#         此函数没有设置参数，因此无法直接设置初始化概率。要设置初始化概率，应使用相应的setter方法。
#
#         例子:
#         假设我们有一个HMM模型实例名为hmm，我们可以通过调用此函数来获取初始化概率。
#         ```
#         init_prob = hmm.init_prob
#         ```
#         """
#
#         return self.save_variables['init_prob']
#
#     @init_prob.setter
#     def init_prob(self, v):
#         """
#         HMM_Base类是一个抽象类，主要定义了隐马尔科夫模型(Hidden Markov Model, HMM)中的一些基本操作。这些基本操作包括初始化模型、加载模型、训练模型、序列匹配、序列解码等。
#
#         在这个类中，我们使用了许多python的装饰器，例如@property和@abc.abstractmethod。其中，@property用于将一个方法转换为只读的属性，@abc.abstractmethod用于声明抽象方法，子类必须实现这些抽象方法。
#
#         这个类的初始化函数是__init__，它调用了父类Model_Base的初始化函数。
#
#         这个类中的init_prob是一个属性，它的getter方法返回模型的初始概率，setter方法用于设置模型的初始概率。
#
#         下面是一个这个类的使用例子：
#         ```python
#         class MyHMM(HMM_Base):
#             def seq_match(self, X):
#                 pass
#             def seq_decode(self, X):
#                 pass
#             def train(self, X, *args):
#                 pass
#             def init_model(self, hidden_state_count: int, *args):
#                 pass
#             def load_init_model(self, path_or_stream):
#                 pass
#
#         my_hmm = MyHMM()
#         my_hmm.init_prob = [0.2, 0.4, 0.4]
#         print(my_hmm.init_prob)  # 输出：[0.2, 0.4, 0.4]
#         ```
#
#         注释函数：
#         ```python
#             @init_prob.setter
#             def init_prob(self, v):
#                 self.save_variables['init_prob'] = v
#         ```
#         该函数是`init_prob`属性的setter方法，用于设置模型的初始概率。
#
#         参数：
#             v : list或numpy数组
#                 初始概率的值。它是一个一维数组，元素的总和为1。
#
#         返回：
#             无
#
#         错误或Bug：
#             如果v的总和不为1，那么可能会导致模型的结果不准确。
#
#         """
#
#         self.save_variables['init_prob'] = v
#
#     @property
#     def trans_prob(self):
#         """
#         该类是隐马尔可夫模型（HMM）的基础类，其中trans_prob是一个属性，表示转移概率。
#
#         更具体地说，转移概率是指在给定当前状态的条件下，系统在下一步转移到其他状态的概率。它是HMM模型的三个主要参数之一，其余两个是初始概率和发射概率。
#
#         以下是Python中使用该类的一些示例:
#
#         ```python
#         hmm = HMM_Base()    # 创建HMM_Base的实例
#         hmm.trans_prob = np.array([[0.7, 0.3], [0.4, 0.6]])    # 设置转移概率
#         print(hmm.trans_prob)   # 打印当前的转移概率
#         ```
#
#         注意: 任何修改trans_prob的操作都会触发其setter方法, 它会将新赋值的值保存在`self.save_variables['trans_prob']`中。然后，这个值可以通过调用getter方法来访问。
#
#         Args:
#             v (numpy.ndarray): 一个二维数组，表示状态之间的转移概率。它的形状应该是(n, n)，其中n是隐藏状态的数量。
#
#         返回:
#             此函数无返回值。
#
#         Raises:
#             ValueError: 如果输入的转移概率矩阵不是二维的，或者其行和列的数量不相等，或者任何一行的元素总和不等于1，那么就会引发ValueError。
#
#         """
#
#         return self.save_variables['trans_prob']
#
#     @trans_prob.setter
#     def trans_prob(self, v):
#         """
#             设置转移概率（trans_prob）属性。
#
#             参数:
#             v : 二维列表或者二维数组
#                 代表转移概率，第i行第j列的元素代表从状态i转移到状态j的概率。
#
#             返回:
#             无返回值
#
#             例子:
#             model.trans_prob = [[0.1, 0.9], [0.8, 0.2]]
#             print(model.trans_prob)
#             [[0.1, 0.9], [0.8, 0.2]]
#         """
#
#         self.save_variables['trans_prob'] = v
#
#     @property
#     def emission_prob(self):
#         """
#         `emission_prob`是一个属性，代表模型的发射概率。发射概率是指在隐藏模型中，每一种隐藏状态生成观察状态的概率。
#
#         Getter:
#         将返回保存在`save_variables`字典中的`emission_prob`键对应的值，即模型的发射概率。
#
#         Setter:
#         参数：
#             v: 需要设置的新的发射概率。
#
#         将`save_variables`字典中的`emission_prob`键的值设置为新的发射概率v。
#
#         注意：如果v的值不是概率（即不在0~1之间）或者v的维度和隐藏状态的数量不匹配，可能会导致模型不准确或者运行错误。
#         """
#
#         return self.save_variables['emission_prob']
#
#     @emission_prob.setter
#     def emission_prob(self, v):
#         """
#             emission_prob 是一个装饰器方法，用于获取和设置隐藏马尔科夫模型中的概率。
#
#             通过此方法，用户可以获取当前模型的发射概率。
#
#             如果提供了一个值作为参数，那么它将被用于设置新的发射概率。
#
#             参数:
#                 v: 一个一维或二维的 numpy 数组，用于设置发射概率。如果没有提供参数，那么函数将返回当前的发射概率。
#
#             返回:
#                 如果没有提供参数，那么函数将返回当前的发射概率。
#                 如果提供了参数，那么函数将不返回任何值，而是更新当前的发射概率。
#
#             示例:
#                 ```python
#                 hmm = HMM_Base()
#                 hmm.emission_prob = np.array([0.1, 0.2, 0.3, 0.4])
#                 print(hmm.emission_prob)  # 输出: array([0.1, 0.2, 0.3, 0.4])
#                 ```
#         """
#
#         self.save_variables['emission_prob'] = v
#
#     @property
#     def state_count(self):
#         """
#         这是一个属性方法，用于获取HMM_Base类的实例的状态数量。
#
#         属性:
#             无
#
#         返回:
#             返回保存在实例的'save_variables'字典中的'state_count'的值，表示该HMM模型的状态数量。
#         """
#
#         return self.save_variables['state_count']
#
#     @abc.abstractmethod
#     def seq_match(self, X):
#         """
#         `seq_match`是一个抽象方法, 需要在`HMM_Base`的子类中实现.
#
#         这个方法的目的是在给定输入序列`X`的情况下, 计算该序列的匹配概率.
#
#         参数:
#             X : list 或者 array-like
#                 输入序列，通常是观测值序列.
#
#         返回:
#             float
#             返回输入序列X的匹配概率.
#
#         例子:
#             假设我们有一个`HMM_Base`的子类实例`hmm`, 我们可以如下调用这个方法:
#             ```python
#             prob = hmm.seq_match(X)
#             ```
#             上述代码会返回输入序列X的匹配概率.
#         """
#
#         pass
#
#     @abc.abstractmethod
#     def seq_decode(self, X):
#         """
#         这是一个抽象方法，由继承`HMM_Base`类的子类实现。这个方法的作用是对输入的观测序列`X`进行解码，获取最有可能的隐藏状态序列。
#
#         参数:
#             X: 一个可迭代的对象，表示观测序列，例如一个包含观测状态的列表。
#
#         返回:
#             一个可迭代的对象，表示最有可能的隐藏状态序列。
#
#         示例:
#             ```python
#             class MyHMM(HMM_Base):
#                 def seq_decode(self, X):
#                     # 这里应该设置解码的逻辑，示例中省略此部分。
#                     pass
#             hmm = MyHMM()
#             X = ["观测状态1", "观测状态2", "观测状态3"]
#             hidden_states = hmm.seq_decode(X)
#             ```
#
#         注意:
#             - 这个方法没有默认的实现，如果子类不实现这个方法，将会在运行时抛出`TypeError`。
#             - 输入的观测序列`X`应符合特定的数据类型或结构，这取决于具体如何实现这个方法。
#         """
#
#         pass


class str_base_hmm:
    def __init__(self, init_prob: {str: float},
                 trans_prob_func: Callable[[str, str], float], emission_prob_func: Callable[[str, str], float]):
        super().__init__()
        # Normalization and caching of initial probabilities
        total_init_prob = sum(init_prob.values())
        self.init_prob = {k: np.log(v / total_init_prob) for k, v in init_prob.items()}  # Convert to log probabilities

        self.states = list(init_prob.keys())

        # Caching for transition and emission probabilities
        self.trans_cache = {}
        self.emit_cache = {}

        # Normalized and cached transition probabilities function
        def normalized_trans(s1, s2):
            if (s1, s2) not in self.trans_cache:
                prob = trans_prob_func(s1, s2)
                norm_prob = prob / sum(trans_prob_func(s1, s) for s in self.states)
                self.trans_cache[(s1, s2)] = np.log(norm_prob)
            return self.trans_cache[(s1, s2)]

        self.trans_prob_func = normalized_trans

        # Normalized and cached emission probabilities function
        def normalized_emit(x, s):
            if (x, s) not in self.emit_cache:
                prob = emission_prob_func(x, s)
                norm_prob = prob / sum(emission_prob_func(x, s) for s in self.states)
                self.emit_cache[(x, s)] = np.log(norm_prob)  # norm_prob  #
            return self.emit_cache[(x, s)]

        self.emission_prob_func = normalized_emit

    def seq_match(self, X: List[str]) -> float:
        """
        Forward Algorithm Implementation with Log Probabilities
        """
        N = len(self.init_prob)
        T = len(X)

        states = list(self.init_prob.keys())

        forward_prob = np.ones((N, T)) * -np.inf  # Initialize with negative infinity (log(0))
        for s in range(N):
            forward_prob[s, 0] = self.init_prob[states[s]] + self.emission_prob_func(X[0], states[s])

        for t in range(1, T):
            for s in range(N):
                forward_prob[s, t] = np.logaddexp.reduce(
                    [forward_prob[s_prime, t - 1] + self.trans_prob_func(states[s_prime], states[s])
                     for s_prime in range(N)]) + self.emission_prob_func(X[t], states[s])
        return np.logaddexp.reduce(forward_prob[:, -1])  # Sum of log probabilities

    def seq_decode(self, X: List[str]) -> List[str]:
        """
        Viterbi Algorithm Implementation with Log Probabilities
        """
        N = len(self.init_prob)
        T = len(X)

        states = list(self.init_prob.keys())

        viterbi_prob = np.ones((N, T)) * -np.inf  # Initialize with negative infinity (log(0))
        back_pointer = np.zeros((N, T), dtype=int)

        # Initialization
        for s in range(N):
            viterbi_prob[s, 0] = self.init_prob[states[s]] + self.emission_prob_func(X[0], states[s])

        # Recursion
        for t in range(1, T):
            for s in range(N):
                max_prob, max_state = max(
                    ((viterbi_prob[s_prime, t - 1] + self.trans_prob_func(states[s_prime], states[s]), s_prime)
                     for s_prime in range(N)), key=lambda x: x[0])
                viterbi_prob[s, t] = max_prob + self.emission_prob_func(X[t], states[s])
                back_pointer[s, t] = max_state

        # Termination
        max_prob = -np.inf
        max_state = 0
        for s in range(N):
            if viterbi_prob[s, -1] > max_prob:
                max_prob = viterbi_prob[s, -1]
                max_state = s

        # Sequence backtracking
        optimal_path = []
        for t in reversed(range(T)):
            optimal_path.insert(0, states[max_state])
            if t != 0:  # Avoid accessing back_pointer out of bounds
                max_state = back_pointer[max_state, t - 1]

        return optimal_path


def state(prob):
    def decorator_state(func):
        @functools.wraps(func)
        def wrapper_state(*args, **kwargs):
            return func(*args, **kwargs)

        # Mark this method as a state method
        wrapper_state._is_state = True
        wrapper_state._prob = prob
        return wrapper_state

    return decorator_state


def state_trans(func):
    @functools.wraps(func)
    def wrapper_state_trans(*args, **kwargs):
        return func(*args, **kwargs)

    # Mark this method as a transition method
    wrapper_state_trans._is_trans = True
    return wrapper_state_trans


class str_base_hmm_by_type_define(str_base_hmm):
    def __init__(self, define_type):
        init_prob = {}
        self.ss_emission_prob_funcs = {}

        # Fetch all methods from the defined type
        for attr_name in dir(define_type):
            method = getattr(define_type, attr_name)

            # Process state methods
            if hasattr(method, "_is_state"):
                init_prob[attr_name] = method._prob
                self.ss_emission_prob_funcs[attr_name] = method

            # Process transition method
            if hasattr(method, "_is_trans"):
                self.ss_trans_prob_func = method

        super().__init__(
            init_prob=init_prob,
            trans_prob_func=lambda s1, s2: self.ss_trans_prob_func(s1, s2),
            emission_prob_func=lambda x, s: self.ss_emission_prob_funcs[s](x)
        )

# class categorical_hmm(HMM_Base):
#     """
#     这是一个名为`categorical_hmm`的类，它继承自`HMM_Base`基类。
#     该类的主要目标是实现一个分类的隐藏马尔可夫模型（HMM）。
#
#     方法包括：
#     - `__init__`：初始化方法，创建一个空的模型实例。
#     - `model_name`：返回模型的名字，这里是"categorical_hmm"。
#     - `seq_match`：使用模型进行序列匹配，返回贝叶斯信息准则（BIC）的值。
#     - `seq_decode`：使用模型对给定的序列进行解码。
#     - `train`：训练模型，可以接受自定义的初始概率和转移概率。
#     - `init_model`：初始化模型，设置隐藏状态的数量。
#     - `load_init_model`：加载已经初始化的模型。
#
#     示例：
#     ```python
#     hmm = categorical_hmm()
#     hmm.init_model(3)
#     hmm.train(X)
#     hmm.seq_decode(X)
#     ```
#
#     注意：
#     - 这个类不包含任何错误处理或异常处理代码，因此在使用时需要注意数据的准确性和完整性。
#     - 另外，由于这个类是一个隐藏马尔可夫模型，因此在使用前需要先初始化模型和训练模型。
#     - 尽管`train`方法中有`custom_start_prob`和`custom_trans_prob`参数，但是这个类并没有实现自定义的初始概率和转移概率的功能。
#     """
#
#     def __init__(self):
#         """
#         初始化categorical_hmm类。该类是一个基于分类的隐藏马尔可夫模型(HMM)，它继承了HMM_Base类。在这个分类HMM模型中，我们可以进行序列匹配，序列解码，模型训练和模型初始化等操作。这个类使用CategoricalHMM模型进行训练和预测。
#
#         属性:
#             model (CategoricalHMM): 使用的CategoricalHMM模型。
#         """
#
#         super().__init__()
#         self.model = None
#
#     @property
#     def model_name(self):
#         """
#         这是一个返回模型名称的属性方法。
#
#         此方法将返回模型的名称，以便在其他地方进行标识。这个方法没有输入参数，并且返回类型是字符串。
#
#         返回：
#             str：模型的名称，即"categorical_hmm"。
#         """
#
#         return "categorical_hmm"
#
#     def seq_match(self, X):
#         """
#         这是一个序列匹配方法，用于计算观察序列的贝叶斯信息准则（BIC）。
#
#         参数:
#             X: ndarray，观察到的序列，用于计算BIC。
#
#         返回:
#             float, 返回观察序列的BIC值。
#
#         注意:
#             此方法依赖于已经训练好的模型，如果模型尚未训练，调用此方法会引发异常。
#         """
#
#         return self.model.bic(X)
#
#     def seq_decode(self, X):
#         """
#         该函数用于解码观察序列，以找到最可能的隐藏状态序列。
#
#         参数:
#             X: 观察序列，是一个列表或者数组类型。
#
#         返回:
#             该函数返回一个元组，其包含两个元素。第一个元素是解码得到的最可能的隐藏状态序列，第二个元素是这个隐藏状态序列的对数概率。
#
#         用法示例:
#             categorical_hmm = categorical_hmm()
#             categorical_hmm.init_model(hidden_state_count=3)
#             categorical_hmm.train(X)
#             state_sequence, log_prob = categorical_hmm.seq_decode(X)
#         """
#
#         return self.model.decode(X)
#
#     def train(self, X, custom_start_prob=None, custom_trans_prob=None, *args):
#         """
#         这个类是基于隐马尔科夫模型的分类器的实现。其中，`train`方法是用于训练模型的。
#
#         ```python
#         def train(self, X, custom_start_prob=None, custom_trans_prob=None, *args):
#         ```
#
#         参数:
#         - `X` : 二维列表，表示输入序列，每个子列表代表一个观察序列。
#         - `custom_start_prob` : 列表或者None。如果列表，则表示自定义的初始状态概率分布，否则使用模型默认值。
#         - `custom_trans_prob` : 二维列表或者None。如果提供，则表示自定义的状态转移概率矩阵，否则使用模型默认值。
#         - `*args` : 可选参数，预留用于后续扩展。
#
#         返回:
#         无返回值。
#
#         此方法使用序列`X`来训练HMM模型。如果提供了自定义的初始状态概率分布或者状态转移概率矩阵，那么在训练过程中会使用这些自定义的参数。在训练结束后，会更新模型的各个概率分布。
#
#         注意:
#         - 参数`X`应为二维列表，其中每个元素应为可被模型处理的数据类型。
#         - 如果`custom_start_prob`和/或`custom_trans_prob`为列表，则其长度应为模型的隐藏状态数量。
#         - 输入数据或自定义参数的错误可能导致训练失败。
#         """
#
#         if custom_trans_prob is not None:
#             self.model.transmat_ = np.array([_normalized(l) for l in custom_trans_prob])
#
#         if custom_start_prob is not None:
#             self.model.startprob_ = _normalized(custom_start_prob)
#
#         train_x = []
#         length = []
#         for sub in X:
#             length.append(len(sub))
#             for inp in sub:
#                 train_x.append(inp)
#         self.model.fit(train_x, lengths=length)
#
#         self.init_prob = self.model.startprob_.tolist()
#         self.trans_prob = self.model.transmat_.tolist()
#         self.emission_prob = self.model.emissionprob_.tolist()
#
#     def init_model(self, hidden_state_count: int, *args):
#         """
#         初始化模型方法
#
#         这个方法用于初始化隐藏马尔可夫模型，模型的隐藏状态数量由参数hidden_state_count指定。模型是使用CategoricalHMM类创建的。
#
#         参数:
#             hidden_state_count (int): 隐藏状态的数量，这决定了隐藏马尔可夫模型的复杂程度。
#             *args: 可变长参数，用于接收任何额外的参数，但在这个方法中并未使用。
#
#         返回类型:
#             无返回值
#
#         例子:
#             # 创建一个有5个隐藏状态的分类隐马尔可夫模型
#             chmm = categorical_hmm()
#             chmm.init_model(5)
#         """
#
#         self.save_variables['state_count'] = hidden_state_count
#         self.model = CategoricalHMM(n_components=hidden_state_count)
#         time.time()
#
#     def load_init_model(self, load_init_model):
#         """
#         加载并初始化模型。
#
#         这个方法主要是根据提供的模型初始化参数来加载和初始化模型。它首先从提供的路径中加载模型参数，然后创建一个对应的`CategoricalHMM`模型实例，并用加载的参数初始化模型的初始概率`startprob_`、转移概率矩阵`transmat_`和发射概率`emissionprob_`。
#
#         参数:
#             load_init_model: 需要加载的模型初始化参数的路径。
#
#         返回值:
#             无返回值。
#
#         使用示例:
#             ```python
#             chmm = categorical_hmm()
#             chmm.load_init_model('path_to_model_init_parameters')
#             ```
#
#         注意事项:
#             1. 参数`load_init_model`必须是有效的模型初始化参数文件路径，否则会引发异常。
#             2. 该方法可以用于加载训练后的模型参数，以便于后续的模型预测或继续训练。
#             3. 加载的模型参数必须与模型的hidden_state_count属性相吻合，否则会引发异常。
#         """
#
#         self.load(load_init_model)
#         self.model = CategoricalHMM(n_components=self.save_variables['state_count'])
#         self.model.startprob_ = np.array(self.init_prob)
#         self.model.transmat_ = np.array(self.trans_prob)
#         self.model.emissionprob_ = np.array(self.emission_prob)


# class aa:
#     @state(0.3)
#     def aa(self, x):
#         return 0.2
#
#     @state(0.4)
#     def bb(self, x):
#         return 0.6
#
#     @state(0.5)
#     def cc(self, x):
#         return 0.4
#
#     @state_trans
#     def trans(self, s1, s2):
#         return 0.4
#
#
# hmm = str_base_hmm_by_type_define(aa())
# rar = hmm.seq_decode(["3", "1", "2", "3", "1", "2", "3", "1", "2"])
# pass
