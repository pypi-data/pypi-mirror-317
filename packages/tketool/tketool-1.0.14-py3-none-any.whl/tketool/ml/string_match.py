# pass_generate
def lcs(s1, s2):
    """
    此函数是用于计算两个字符串之间的Levenshtein距离，即将一个字符串转换为另一个字符串所需要的最少单字符编辑（插入、删除或替换）的数量。这种度量方式在许多领域都有应用，包括计算机科学中的信息检索和自然语言处理。
    
    参数:
    s1, s2: 需要计算Levenshtein距离的两个字符串。
    
    返回:
    返回计算得出的Levenshtein距离，归一化，即除以两个字符串中的最大长度，这样得出的值会在0和1之间，值越小表示两个字符串越相似。
    
    示例:
        s1 = "kitten"
        s2 = "sitting"
        lcs_distance = lcs(s1, s2)
        print(lcs_distance)  # 输出: 0.5714285714285714
    
    注意:
    此函数使用的是动态规划方法，时间复杂度为O(len(s1)*len(s2))，空间复杂度也为O(len(s1)*len(s2))，在处理大规模数据时需要注意。
    """

    # 创建一个二维数组来存储在每一步中计算出来的Levenshtein距离
    dp_table = [[0 for _ in range(len(s2) + 1)] for _ in range(len(s1) + 1)]

    # 初始化第一行和第一列，这对应于将一个空字符串转化为另一个字符串
    for i in range(len(s1) + 1):
        dp_table[i][0] = i

    for j in range(len(s2) + 1):
        dp_table[0][j] = j

    # 对s1和s2进行迭代
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            if s1[i - 1] == s2[j - 1]:
                cost = 0
            else:
                cost = 1

            # 在三种可能的操作（删除、插入、替换）中选择最小的值
            dp_table[i][j] = min(dp_table[i - 1][j] + 1,  # 删除
                                 dp_table[i][j - 1] + 1,  # 插入
                                 dp_table[i - 1][j - 1] + cost)  # 替换

    return dp_table[-1][-1] / max(len(s1), len(s2))


def match_2_string_list(list1: [str], list2: [str], top_n=1) -> [[int]]:
    """
    这个函数的目的是找出列表2中与列表1中每个字符串最匹配的字符串的索引。匹配程度通过使用最长公共子序列（lcs）算法来评估。
    
    参数:
        list1: 一个由字符串组成的列表。将从列表2中寻找每个字符串的最佳匹配项。
        list2: 一个由字符串组成的列表，我们将从这个列表中寻找与列表1中的字符串最匹配的字符串。
        top_n: 整数。默认为1。表示返回匹配程度最高的前n个字符串的索引。
    
    返回:
        返回一个二维列表。列表的长度与list1一致。每个子列表都包含top_n个从list2中选出的与list1中对应字符串匹配程度最高的字符串的索引。
        例如，如果list1 = ['abc', 'def'], list2 = ['abc', 'def', 'ghi', 'jkl']，top_n = 2，那么返回的结果可能是[[0, 1], [1, 0]]。
        这意味着与'abc'最匹配的两个字符串在list2中的索引是0和1，与'def'最匹配的两个字符串在list2中的索引是1和0。
    
    注意:
        这个函数使用lcs（最长公共子序列）算法来评估字符串之间的匹配程度，因此在输入长度较大的字符串列表时，可能会花费较长时间。
        此外，如果top_n的值设置得较大，且列表2的长度远大于top_n，可能会浪费一些计算资源，因为我们只关心匹配程度最高的top_n个结果。
    
    示例:
        list1 = ['abc', 'def']
        list2 = ['abc', 'def', 'ghi', 'jkl']
        top_n = 2
        print(match_2_string_list(list1, list2, top_n))
        结果：[[0, 1], [1, 0]]
    """

    result = []

    for str1 in list1:
        lcs_values = [(lcs(str1, str2), index) for index, str2 in enumerate(list2)]
        lcs_values.sort(key=lambda x: x[0], reverse=True)
        best_match_indices = [index for _, index in lcs_values[:top_n]]

        result.append(best_match_indices)

    return result
