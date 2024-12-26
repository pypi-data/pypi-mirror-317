# pass_generate
import abc, pickle


class Model_Base(metaclass=abc.ABCMeta):
    """
    这个 `Model_Base` 类是其它模型的基类，采用抽象基类 (abc.ABCMeta) 作为元类。模型需要实现 `model_name` 属性。此外，它还提供了保存和加载模型的方法。
    
    # 类的介绍和目的
    这个类用于定义模型的基本结构和功能，它包含两个主要的功能：保存模型和加载模型。
    
    `__init__` 方法初始化一个空的字典 `save_variables` 用于存储模型的参数。
    
    `model_name` 是一个抽象属性，子类需要根据自己的情况来实现这个属性。
    
    `save` 方法是用来保存模型的参数到文件或者流中，如果传入的是字符串，它会被认为是文件路径；如果传入的是一个流对象，它会直接将模型参数保存到这个流中。
    
    `load` 方法是用来从文件或者流中加载模型的参数，如果传入的是字符串，它会被认为是文件路径；如果传入的是一个流对象，它会直接从这个流中加载模型参数。
    
    # 示例
    ```
    class MyModel(Model_Base):
        @property
        def model_name(self):
            return 'MyModel'
    
    model = MyModel()
    model.save('mymodel.pkl')
    model.load('mymodel.pkl')
    ```
    在这个例子中，我们定义了一个 `MyModel` 类，并实现了 `model_name` 属性。然后我们创建了一个 `MyModel` 的实例，并调用 `save` 和 `load` 方法来保存和加载模型。
    
    注意: 这个类没有处理文件或者流读写错误的情况，当文件路径无效，或者文件权限不足，或者流对象无效时，可能会抛出异常。
    """

    def __init__(self):
        """
        这是`Model_Base`类的初始化函数。
        
        在创建一个`Model_Base`类的实例时，会调用这个函数。这里并没有特别的参数需要传入。
        
        `Model_Base`是一个基础模型的抽象类，它有两个基础功能：保存模型和加载模型。其中“模型”的保存和加载是通过pickle库实现的，保存和加载的对象是一个字典`save_variables`。
        
        在这个初始化函数中，我们创建了一个空字典`save_variables`，它用于以后保存模型的变量。
        
        示例：
        ```python
        model = Model_Base()
        ```
        注意：
        `Model_Base`是一个抽象类，不能直接实例化。在实际使用中，通常会创建它的子类，并实现`model_name`这个抽象属性。
        """

        self.save_variables = {}

    @property
    @abc.abstractmethod
    def model_name(self):
        """
        这是一个抽象方法，需要在子类中实现。这个方法定义了一个只读的属性`model_name`。由于用了`@property`装饰器，可以直接用`object.model_name`来访问，无需调用`object.model_name()`。由于该方法是抽象的，因此子类必须提供具体的实现。这个方法没有任何参数和返回值，但会返回在子类中实现的具体模型名。
        
        例如：
        ```python
        class MyModel(Model_Base):
            @property
            def model_name(self):
                return "my_model"
        ```
        在这个例子中，如果有一个`MyModel`的对象`m`，`m.model_name`会返回`"my_model"`。
        
        注意：在子类中重写这个方法时，要使用`@property`装饰器。
        """

        pass

    def save(self, path_or_stream):
        """
        这个方法是用于保存模型的状态的。
        
        参数:
            path_or_stream: 一个str类型或者一个file-like object. 如果是str类型, 则它应该是一个要保存的文件的路径名. 如果是file-like object, 则将直接在这个流上进行写入操作.
        
        返回:
            None
        
        这个方法不会返回任何值, 但是它会在指定的路径或流上保存模型的状态. 这个状态可以使用相同类的load方法进行加载.
        
        示例:
            ```python
            model = Model_Base()
            model.save('model.pkl')
            ```
        在此例中, 我们创建了一个Model_Base实例, 并使用save方法保存了它的状态到一个叫做'model.pkl'的文件.
        
        注意:
            1. 如果path_or_stream是一个文件路径, 则必须有足够的权限来写入该文件.
            2. 如果path_or_stream是一个file-like object, 则必须已经被打开, 并且可以进行写入操作.
        """

        if isinstance(path_or_stream, str):
            with open(path_or_stream, "wb") as f:
                pickle.dump(self.save_variables, f)
        else:
            pickle.dump(self.save_variables, path_or_stream)

    def load(self, path_or_stream):
        """
        此函数用于加载先前保存的模型变量。模型变量是以pickle格式存储的，可以从文件路径或者IO流中读取。
        
        参数:
            path_or_stream (str or file-like object): 如果是字符串，则它代表了要加载模型变量的文件路径。如果是file-like对象，则直接从该对象中读取模型变量。
        
        返回:
            无返回值。该方法将直接修改类实例的save_variables属性。
        
        使用示例:
            model = Model_Base()
            model.load('/path/to/saved/model.pkl')  # 从文件路径加载模型变量
            with open('/path/to/saved/model.pkl', 'rb') as f:
                model.load(f)  # 从文件流加载模型变量
        
        注意:
            在使用该方法前，请确保你已经正确实现了model_name属性（抽象方法）。否则将会抛出NotImplementedError异常。
        """

        if isinstance(path_or_stream, str):
            with open(path_or_stream, "rb") as f:
                self.save_variables = pickle.load(f)
        else:
            self.save_variables = pickle.load(path_or_stream)
