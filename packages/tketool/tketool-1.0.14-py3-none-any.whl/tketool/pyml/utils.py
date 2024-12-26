# pass_generate
import torch


def convert_to_list(var):
    """
    将输入的变量转换为列表类型。
    
    这个函数接收一个输入——可以是整数、浮点数、列表或者Tensor，并将其转换为列表。如果输入是整数或浮点数，它将被放入一个新的列表中并返回。如果输入已经是一个列表，那么函数会直接返回它。如果输入是一个Tensor，函数会将其转换为列表，如果Tensor是2D的，它将被flatten(降维)为1D列表。
    
    注意：
    假设传入的tensor都是1D或者2D的。
    
    参数:
    var: 输入变量，可以是int、float、list、Tensor类型。
    
    返回:
    列表，其中包含了原始输入的元素。如果输入是2D Tensor，返回的列表将是flatten后的1D列表。
    
    可能抛出的错误:
    ValueError：如果输入的不是int、float、list或Tensor类型，将抛出一个值错误。
    """

    # 如果var是int或者float类型
    if isinstance(var, int) or isinstance(var, float):
        return [var]
    # 如果var是list类型
    elif isinstance(var, list):
        return var
    # 如果var是Tensor类型
    elif torch.is_tensor(var):
        # 这里假设你的tensor都是1D或者2D的
        if len(var.shape) == 1:
            return var.tolist()
        elif len(var.shape) == 2:
            # 处理2维tensor，转换为1D list
            return var.flatten().tolist()
    else:
        raise ValueError(f"Unsupported type: {type(var)}")
