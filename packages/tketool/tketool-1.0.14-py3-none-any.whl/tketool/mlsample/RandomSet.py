# pass_generate
from tketool.mlsample.MemorySampleSource import Memory_NLSampleSource
import numpy as np


def create_SampleSet(set_name, input_size, count):
    """
    这是一个在内存中生成样本集并保存的函数。该函数首先创建一个新的样本集，然后在每次循环中生成随机输入样本和对应的随机标签，最后将这些样本添加到样本集中。
    
    参数:
      set_name (str): 新建样本集的名称。
      input_size (int): 每个样本输入的大小。
      count (int): 需要生成的样本数量。
    
    返回值:
      Memory_NLSampleSource: 包含新生成样本集的Memory_NLSampleSource对象。
    
    示例:
      创建一个名为'test_set'，每个输入样本大小为10，样本数量为100的样本集:
      ```python
      sample_set = create_SampleSet('test_set', 10, 100)
      ```
    
    注意：
      该函数没有做参数类型和值的检查，如果传入的参数类型或值不正确，可能会抛出异常。
    """

    NSet = Memory_NLSampleSource()

    NSet.create_new_set(set_name, "", [], ["t_input", "a_lable"], "", "")
    for _ in range(count):
        c_list = np.random.rand(input_size).tolist()
        c_result = 1 if np.random.randint(0, 10, 1) > 5 else 0
        NSet.add_row(set_name, [c_list, c_result])

    return NSet
