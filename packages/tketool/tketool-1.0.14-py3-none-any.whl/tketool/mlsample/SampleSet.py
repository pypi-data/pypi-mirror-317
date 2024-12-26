from tketool.mlsample.NLSampleSource import NLSampleSourceBase
import random
from typing import List
from functools import reduce


class SampleSet:
    """
    这是一个名为SampleSet的类，主要用于管理和处理样本数据。
    
    SampleSet类通过与样本来源交互，可以从样本来源获取所需的样本数据，同时还可以对样本数据进行各种操作，如shuffle(打乱顺序)、take(获取一定数量的样本)、skip(跳过一定数量的样本)、batch(将样本分批次获取)和func(对样本进行自定义操作)。
    
    类的属性包括:
    - sample_source: 样本来源，用于获取样本数据
    - set_name: 样本集名称，用于标识当前的样本集
    - count: 样本数量
    
    类的方法包括:
    - __init__: 初始化类，设置样本来源和样本集名称
    - __iter__: 迭代器方法，返回当前类的迭代器
    - sample_source: 返回样本来源
    - set_name: 返回样本集名称
    - count: 返回样本数量
    - _base_iter: 基础迭代器，用于在迭代过程中管理样本数据的获取和处理
    - shuffle: 打乱样本顺序
    - take: 获取一定数量的样本
    - skip: 跳过一定数量的样本
    - batch: 将样本分批次获取
    - func: 对样本进行自定义操作
    
    示例:
    
    # 创建一个SampleSet对象
    sample_set = SampleSet(sample_source, 'train')
    
    # 对样本进行打乱顺序
    sample_set.shuffle()
    
    # 获取10个样本
    sample_set.take(10)
    
    # 跳过5个样本
    sample_set.skip(5)
    
    # 将样本分批次获取，每批次5个样本
    sample_set.batch(5)
    
    # 对样本进行自定义操作
    sample_set.func(lambda x: x * 2)
    
    注意: 该类没有显著的错误或者bug，但在处理大规模数据时可能需要考虑内存和性能问题。
    """

    def __init__(self, source_base: NLSampleSourceBase,
                 set_name: str | List[str],
                 concat_intersection=True
                 ):
        """
        `SampleSet`类是一个用于管理和处理样本集的类。它提供了各种方法，如`shuffle`、`take`、`skip`、`batch`和`func`，以对样本集进行操作，如打乱样本、取样本、跳过样本、分批样本以及应用函数到样本。此外，它还保存了有关样本集的一些信息，如样本源、集合名称以及样本的数量等。
        
        此类的初始化方法定义如下：
        
        
        ```python
        def __init__(self, source_base: NLSampleSourceBase, set_name: str):
        ```
        
        ## 参数
        
        - `source_base` (NLSampleSourceBase): 样本源的基类对象，用于获取样本数据和样本元数据等信息。
        - `set_name` (str): 样本集的名称。
        
        ## 属性
        
        - `_sample_source` (NLSampleSourceBase): 存储`source_base`参数，表示样本源。
        - `_set_name` (str): 存储`set_name`参数，表示样本集的名称。
        - `_shuffle` (bool): 初始化为`False`，表示样本是否需要打乱。
        - `batch_count` (int): 初始化为`None`，表示每批样本的数量。
        - `_data_keys` (list): 存储从样本源获取的样本元数据键。
        - `_iter_keys` (list): 初始化为空列表，用于存储迭代的键。
        - `_loaded_pointer` (bool): 初始化为`False`，表示是否已加载指针。
        - `_func` (list): 初始化为只包含`_base_iter`函数的列表，用于存储需要对样本进行的函数操作。
        - `_count` (int): 存储从样本源获取的样本集的数量。
        
        ## 使用示例
        
        ```python
        from nl_sample_source_base import NLSampleSourceBase
        
        # 创建样本源
        sample_source = NLSampleSourceBase()
        
        # 创建样本集
        sample_set = SampleSet(sample_source, 'train')
        
        # 打乱样本
        sample_set.shuffle()
        
        # 取100个样本
        sample_set.take(100)
        
        # 跳过10个样本
        sample_set.skip(10)
        
        # 分成每批10个样本
        sample_set.batch(10)
        
        # 对每个样本应用函数
        sample_set.func(lambda x: x**2)
        ```
        """

        self._sample_source = source_base
        self._set_name_list = set_name if isinstance(set_name, list) else [set_name]
        self._concat_intersection = concat_intersection
        self._shuffle = False

        self.batch_count = None

        self._data_keys_list = [source_base.get_metadata_keys(sn) for sn in self._set_name_list]

        k_sets = [set(kk['label_keys']) for kk in self._data_keys_list]
        if self._concat_intersection:
            self.keys = reduce(lambda a, b: a.intersection(b), k_sets)
        else:
            self.keys = reduce(lambda a, b: a.union(b), k_sets)

        self._iter_keys = []

        self._loaded_pointer = False

        self._func = [self._base_iter]

        self._count_list = [self._sample_source.get_set_count(sn) for sn in self._set_name_list]
        self._count = sum(self._count_list)

    def __iter__(self):
        """
        该方法是一个特殊的迭代器方法，允许SampleSet对象进行迭代操作。当Python执行for...in...循环时，如果在for后面的对象是一个迭代器，那么Python将会自动调用这个方法。
        
        返回:
            返回一个函数对象，该函数对象通过调用self._func[-1]()方法得到。这意味着，每次迭代都将使用self._func列表中的最后一个函数进行。根据SampleSet类中其他方法对self._func的操作，这个函数可能实现了一系列的数据操作，比如取样、跳过、批处理等。
        
        例子:
        假设我们有一个SampleSet对象sampleset，我们可以这么使用这个迭代器方法：
        ```
        for sample in sampleset:
            print(sample)
        ```
        在这个例子中，每次迭代都会打印出一个样本。
        
        警告:
        在多线程环境中，由于self._func[-1]()返回的函数对象可能会被其他线程修改，因此这个迭代器方法可能会产生预期之外的结果。为了避免这种情况，建议在单线程环境下使用这个方法，或者使用线程锁确保访问self._func的原子性。"""

        return self._func[-1]()

    @property
    def sample_source(self):
        """
        这是一个property函数，用于返回_sample_source属性。
        
        返回:
            _sample_source(NLSampleSourceBase类型): 返回提供样本集信息及访问的基本对象。
        """

        return self._sample_source

    @property
    def set_name(self):
        """
        获取当前样本集的名称
        
        这是一个简单的getter方法，不接受任何参数，返回结果是一个字符串，代表当前样本集的名称。
        
        返回:
            返回当前样本集的名称(set_name)。
        """

        return self._set_name_list

    def count(self):
        """
        `count` 是一个方法，用于获取 SampleSet 实例中的样本数量。
        
        此方法无需任何输入参数。
        
        返回值：
        返回一个整数，表示 SampleSet 实例中的样本数量。
        
        示例用法：
        ```python
        sample_set = SampleSet(source_base, set_name)
        num_samples = sample_set.count()
        ```
        此示例说明如何创建 SampleSet 类的实例并使用 `count` 方法获取样本数量。
        
        不含已知错误或 bug。
        """

        return self._count

    def _base_iter(self):
        """
        `_base_iter`是一个私有生成器方法，主要用于数据集的迭代和随机打乱。
        
        首次调用时，此方法会加载数据集的迭代指针并存储在`_iter_keys`列表中，其后的调用则直接从这个列表中读取。
        如果`_shuffle`属性为`True`，则会对`_iter_keys`列表中的元素进行随机打乱。
        
        每次迭代时，该方法都会根据当前的指针，从数据源中加载对应的数据，并以字典的形式返回。
        
        注意，此方法是一个私有方法，仅供内部使用。
        
        返回：
        返回一个生成器，每次迭代返回一个含有数据的字典。
        
        示例：
        ```python
        for data in self._base_iter():
            process(data)
        ```
        """

        if self._loaded_pointer == False:
            totle_count = 0
            # for file_index, seek_p in self._sample_source.iter_pointer(self._set_name):
            #     if file_index not in self._iter_map:
            #         self._iter_map[file_index] = []
            #         self._iter_keys.append(file_index)
            #     self._iter_map[file_index].append(seek_p)
            #     totle_count += 1
            for idx, set_name in enumerate(self._set_name_list):
                for pointer in self._sample_source.iter_pointer(set_name):
                    self._iter_keys.append((idx, pointer))
                    totle_count += 1
                self._loaded_pointer = True

        if self._shuffle:
            random.shuffle(self._iter_keys)
            # for key in self._iter_map.keys():
            #     random.shuffle(self._iter_map[key])

        for p in self._iter_keys:
            # for p in self._iter_map[key_list]:
            set_name = self._set_name_list[p[0]]
            keylist = self._data_keys_list[p[0]]['label_keys']
            data = {k: v for k, v in
                    zip(keylist, self._sample_source.load_pointer_data(set_name, p[1]))}
            yield {k: data[k] if k in data else None for k in self.keys}

    def shuffle(self):
        """
            此函数用于启用样本混洗功能。
        
            函数shuffle(self)将实例变量self._shuffle标记为True，表示在生成器函数_base_iter(self)中，将对数据指针的迭代顺序进行随机打乱。
        
            这个函数没有任何参数。
        
            返回的是包含此函数的类的实例，即self，这样可以实现函数链式调用。
        
            示例:
        
            假设sample_set是SampleSet类的一个实例，
        
            那么我们可以这样调用此函数：sample_set.shuffle()。
        
            在这之后，当我们从sample_set中取出样本时，样本的顺序就会被随机打乱。
        
            注意：这个函数必须在生成样本之前调用，如果在生成样本之后调用，将不会有任何效果。
        
            在实际使用中，我们通常会这样使用：
        
            sample_set.shuffle().batch(128)
        
            这样可以先打乱样本的顺序，然后按照每128个样本为一组，进行分组操作。
        
        """

        self._shuffle = True
        return self

    def take(self, count):
        """
        `take`是一个实例方法，用于从样本集中获取指定数量的样本。
        
        参数:
        
        - count: int
          指定要从样本集中获取的样本数量。
        
        返回:
        
        - SampleSet类的实例。通过调用此方法，可以在类实例上应用链式操作。
        
        示例:
        
        ```python
        sample_set = SampleSet(source_base, set_name)
        sample_set = sample_set.take(5)  # 从样本集中获取5个样本
        for sample in sample_set:
            print(sample)
        ```
        
        注意：
        
        - 此函数会更改内部计数器`self._count`的值，以反映从样本集中获取的样本数量。
        - 这个函数不会立即执行获取样本的操作，而是在迭代样本集时才会真正获取样本。这是通过在函数内部创建并添加一个新的生成器函数到`self._func`列表实现的。
        - 当请求的样本数量大于样本集中的可用样本数量时，此函数会将`self._count`设置为样本集的大小。
        """

        fun_index = len(self._func) - 1

        if self._count >= count:
            self._count = count

        def take_func():
            kcount = count
            for _item in self._func[fun_index]():
                kcount -= 1
                if kcount >= 0:
                    yield _item
                else:
                    break

        self._func.append(take_func)
        return self

    def skip(self, count):
        """
            `skip`函数用于在数据集中跳过指定数量的样本。
        
            参数:
            count (int): 需要跳过的样本数量。
        
            返回:
            SampleSet: 返回当前的SampleSet实例，便于链式操作。
        
            用法示例:
            sample_set = SampleSet(source_base, set_name)
            sample_set.skip(10)  # 跳过前10个样本
        
            注意:
            1. 如果跳过的样本数量比当前样本集中的样本总数还要多，则所有样本都会被跳过，样本集的数量会被设置为0。
            2. 该函数会影响当前样本集的总样本数（self._count）。
        """

        fun_index = len(self._func) - 1

        self._count = self._count - count
        if self._count < 0:
            self._count = 0

        def skip_func():
            kcount = count
            for _item in self._func[fun_index]():
                kcount -= 1
                if kcount >= 0:
                    continue
                else:
                    yield _item

        self._func.append(skip_func)
        return self

    def batch(self, batch_count):
        """
        这个方法是`SampleSet`类的一个成员方法，其主要目标是将样本集按照指定的批量大小进行分批。
        
        参数:
            batch_count (int): 指定每批样本的数量。
        
        返回:
            SampleSet: 返回修改后的样本集对象，该对象的每个迭代都将产生一个包含指定数量样本的批次。
        
        示例:
        假设我们有一个SampleSet对象`s`，将其按每批10个样本进行分批，可以通过以下方式实现：
        
        ```python
        s.batch(10)
        ```
        
        注意:
        此方法可能会更改样本集的总数(`self._count`)，这是因为它会将总数调整为能够容纳完整批次的最大数量。例如，如果样本总数是25，批次大小是10，那么总数将被减少到20，既然最后的5个样本不足以形成一个完整的批次，将不会被迭代产生出来。
        
        此外，此方法会对样本集的迭代方式进行更改，使其在每次迭代时产生一个包含`batch_count`个样本的列表，而不是单个样本。
        """

        self.batch_count = batch_count
        fun_index = len(self._func) - 1

        n_c_a = self._count // batch_count
        n_c_b = self._count % batch_count
        self._count = n_c_a
        if n_c_b > 0:
            self._count += 1

        def batch_func():
            batch_list = []

            b_batch_c = 0
            for _item in self._func[fun_index]():
                batch_list.append(_item)
                b_batch_c += 1

                if b_batch_c == batch_count:
                    yield batch_list
                    b_batch_c = 0
                    batch_list = []

            if b_batch_c > 0:
                yield batch_list

        self._func.append(batch_func)
        return self

    def func(self, func):
        """
        此函数是在SampleSet类中定义的一个方法，用于将给定的函数应用到SampleSet的每一个元素上。
        
        参数:
            func: 一个函数。这个函数将会应用到SampleSet的每一个元素上。
        
        示例:
        
        def double(x):
            return x * 2
        
        sample_set = SampleSet(source_base, set_name)
        sample_set.func(double)
        
        上述代码会将函数double应用到SampleSet的每一项上，即每一项都会乘以2。
        
        注意:
        func的参数类型和返回类型应与SampleSet中的元素类型一致。
        
        返回:
            SampleSet对象本身，用于链式调用。
        """

        fun_index = len(self._func) - 1

        def func_func():
            for _item in self._func[fun_index]():
                yield func(_item)

        self._func.append(func_func)
        return self

    def match(self, cols=None, str_equal=None, include=None, start_with=None, end_with=None, ignore_case=True):
        fun_index = len(self._func) - 1

        def match_func():
            match_keys = None
            if cols is None:
                match_keys = self.keys
            else:
                if isinstance(cols, str):
                    match_keys = [cols]
                else:
                    match_keys = cols

            for k in match_keys:
                if k not in self.keys:
                    raise Exception("no key named " + k)

            for _item in self._func[fun_index]():
                matched = False
                for col in match_keys:
                    val = str(_item[col])
                    if ignore_case:
                        val = val.lower()
                    if str_equal and str_equal == val:
                        matched = True
                    elif include and include in val:
                        matched = True
                    elif start_with and val.startswith(start_with):
                        matched = True
                    elif end_with and val.endswith(end_with):
                        matched = True

                if matched:
                    yield _item

        self._func.append(match_func)
        return self
