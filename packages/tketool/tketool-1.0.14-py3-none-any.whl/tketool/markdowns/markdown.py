import time, abc
from tketool.files import write_file_line, write_file


def _convert_char(ss: str):
    """
    该函数的主要目的是将输入的字符串中的部分特殊字符转义。具体来说, 它会将输入字符串中的反斜杠(`\`)、两个下划线(`__`)和井号(`#`)分别转换为两个反斜杠(`\\`)、四个下划线(`\_\_`)和两个井号(`\#`)。
    
    参数:
        ss (str): 需要进行转义的字符串。
    
    返回类型:
        str: 完成转义后的字符串。
    
    示例:
        输入: _convert_char("test\\__#")
        输出: "test\\\\\_\_\\\#"
    
    注意:
        该函数没有错误检测机制，所以如果输入的不是字符串，虽然函数内部有将输入转化为字符串的步骤，但可能会得到意料之外的结果。
    """

    ss = str(ss)
    ss = ss.replace('\\', "\\\\")
    ss = ss.replace("__", "\_\_")
    ss = ss.replace("#", "\#")
    return ss


class markdown_item_base:
    """
    此类为 `markdown_item_base`，这是一个基础类，主要用于处理markdown文档的各种元素。
    
    类的方法：
    - `anchor_pointer_outer` : 返回一个空字符串，可能作为锚点调用的外部接口，返回类型为字符串。
    - `flush_begin` : 无返回值的方法，具体功能未知，可能在子类中做具体实现，或者作为某种复位或初始化方法。
    - `flush_row_anchor` : 接收一个字符串作为参数，返回一个空列表，可能在子类中做具体实现，用于处理markdown文档的行锚点。
    
    注意：这个类的全部方法都没有具体实现，可能作为接口或者抽象类供其他markdown相关的子类继承并实现具体方法。
    
    示例：
    
    ```python
    class markdown_item_subclass(markdown_item_base):
        def anchor_pointer_outer(self) -> str:
            return "#anchor"
    
        def flush_begin(self):
            print("begin flush")
    
        def flush_row_anchor(self, anchor_str) -> [str]:
            return [anchor_str]
    
    markdown_item = markdown_item_subclass()
    markdown_item.flush_begin()  # 输出 "begin flush"
    print(markdown_item.flush_row_anchor("my_anchor"))  # 输出 ["my_anchor"]
    ```
    
    此类尚未发现错误或者bug。
    """

    def anchor_pointer_outer(self) -> str:
        """
        此方法是markdown_item_base类的一部分。
        
        `anchor_pointer_outer`方法用于生成一个空的字符串，此方法没有参数。在具体实现中可能会被子类重写，用于生成特定的字符串。
        
        参数：
        无
        
        返回：
        str：返回一个空字符串
        
        注意：本方法在当前类中未实现具体功能，返回的都是空字符串。
        
        示例：
        ```python
        markdown_item = markdown_item_base()
        print(markdown_item.anchor_pointer_outer())  # 输出： ""
        ```
        """

        return ""

    def flush_begin(self):
        """
            `flush_begin`是一个在`markdown_item_base`类中定义的方法，此方法没有具体的实现内容，可能是一个需要子类进行重写的抽象方法。
        
            本方法没有输入参数，也没有返回值。
        
            例如，如果我们在子类中重写此方法，可能如下所示：
        
            ```python
            class markdown_item_sub(markdown_item_base):
        
                def flush_begin(self):
                    print("开始执行操作")
            ```
        
            在此示例中，`flush_begin`方法被重写，当调用此方法时，会打印出"开始执行操作"。
        """

        pass

    def flush_row_anchor(self, anchor_str) -> [str]:
        """
        此函数是markdown_item_base类的一个方法, 它的主要作用是处理传入的锚字符串,并以字符串数组形式返回。
        
        参数:
            anchor_str(str): 传入的锚字符串。
        
        返回:
            list[str]: 返回处理后的字符串数组，如果没有需要处理的内容，则返回空数组。
        """

        return []


class MTitle(markdown_item_base):
    """
    这是一个名为MTitle的类，它继承自markdown_item_base类。该类主要用于创建、存储和操作markdown格式的标题。
    
    标题在markdown中是非常重要的元素，它们帮助组织和突出内容的结构。这个类主要是用来生成不同等级的markdown标题的。
    
    类的初始化函数接收两个参数：
    
    - `title_str`: 这是标题的文本内容，是一个字符串。
    - `title_level`: 这是标题的等级，是一个整数。Markdown允许1-6级的标题。标题级别越高，标题文本越小。
    
    类中定义了一个名为`flush_row_anchor`的方法，这个方法接收一个名为`anchor_str`的参数，返回一个字符串列表。
    
    这个方法的主要作用是用于生成标题的markdown格式的字符串。它使用级别数量的井号`#`来表示标题的级别，然后添加标题文本。
    
    例如创建一个一级标题：
    ```python
    title_item = MTitle("Hello, world!", 1)
    print(title_item.flush_row_anchor("anchor"))
    ```
    输出：['# Hello, world!  \n']
    
    请注意，由于这是一个基于类的设计，所以在使用这个类时，需要先实例化后再调用其方法。
    """

    def __init__(self, title_str, title_level):
        """
        初始化 MTitle 类的实例。
        
        这是一个表示 Markdown 标题的类，通过设置标题内容和标题等级来创建标题。标题等级决定了标题的重要程度。
        
        参数:
            title_str (str): 标题的文本内容。
            title_level (int): 标题的等级。等级越高，标题在页面中的显示越大。
        
        示例：
            MTitle("这是一个标题", 1)
            这将会创建一个等级为 1 的标题，显示为 "这是一个标题"。
        """

        self.title_str = title_str
        self.title_level = title_level

    def flush_row_anchor(self, anchor_str) -> [str]:
        """
        该函数主要用于刷新标题行锚点的功能。
        
        参数:
            anchor_str: 锚点字符串，虽然在函数体中未使用，但可能在其他地方有调用。
        
        返回类型:
            返回一个列表，其中包含一个字符串，该字符串是Markdown格式的标题。标题的层级由`self.title_level`决定，标题内容由`self.title_str`决定。
        
        使用示例:
            mtitle = MTitle('测试标题', 1)
            mtitle.flush_row_anchor('anchor')
            输出: ['# 测试标题  \\n']
        
        注意:
            `_convert_char`函数将`self.title_str`中的特殊字符转换为Markdown可以识别的格式。此函数体中并未定义，因此应在同一作用域下被定义和引用。
        
        """

        return [f'{"#" * self.title_level} {_convert_char(self.title_str)}  \n']


class MTOC(markdown_item_base):
    """
    这个类名为MTOC，继承自markdown_item_base类。主要功能是处理markdown文本中的行锚点。
    
    具体方法如下：
    
    flush_row_anchor:
    
    该方法用于清理Markdown中的行锚点，将其替换为特定的字符串。
    
    参数:
        anchor_str (str): 需要被清理的行锚点字符串。
    
    返回:
        list[str]: 返回一个包含处理后的字符串的列表，返回的字符串是"[toc] \n"。
    
    用法示例：
    
    ```python
    mtoc = MTOC()
    result = mtoc.flush_row_anchor('#example')
    print(result)  # 输出：['[toc] \n']
    ```
    
    注意：目前未发现此类的错误或bug。
    
    """

    def flush_row_anchor(self, anchor_str) -> [str]:
        """
        这是一个类方法，其主要功能是生成markdown的目录链接。
        
        参数:
            self: 对象本身的引用
            anchor_str: 一个字符串，用于指示markdown文档中的锚点。
        
        返回:
            返回一个列表，其中只包含一个字符串。这个字符串是markdown目录的链接，格式为"[toc] \n"。
        
        使用示例:
            mtoc = MTOC()
            anchor_str = 'example'
            print(mtoc.flush_row_anchor(anchor_str))  # 输出：['[toc] \n']
        
        注意:
            无论传入什么样的anchor_str，此函数总是返回['[toc] \n']。也就是说，anchor_str参数在当前实现中并未使用。
            这可能是一个设计错误或者是尚未完成的功能。如果你希望根据不同的anchor_str生成不同的目录链接，请完善此函数的实现。
        
        """

        return [f'[toc] \n']


class MSplit_line(markdown_item_base):
    """
    这是一个名为 MSplit_line 的类，它继承自 markdown_item_base。该类的主要用途在于处理并控制Markdown语法中的分割线。
    
    这个类仅包含一个名为 flush_row_anchor 的方法。
    
    方法 flush_row_anchor 的作用是返回一个包含Markdown分割线语法的列表。
    
    例如：
    
        msplit_line = MSplit_line()
        print(msplit_line.flush_row_anchor("anchor"))  # 输出['*** \n']
    
    方法参数：
        anchor_str: 一个字符串类型的参数，但在这个方法中并未被实际使用。
    
    返回类型：
        返回一个包含字符串的列表，字符串为 "*** \n"，代表Markdown中的分割线。
    
    注意与bug：
        本方法的参数并未实际参与到业务逻辑中，考虑到方法的实现，可能需要重新审查和优化这个函数的设计。
    """

    def flush_row_anchor(self, anchor_str) -> [str]:
        """
        `flush_row_anchor`是`MSplit_line`类的一个方法，该类继承自`markdown_item_base`。
        
        该方法的目标是生成一个markdown的分隔线。
        
        参数:
            anchor_str (str): 该参数在当前的方法中并未被使用，但可能在其他继承自同一基类的类中有所使用。
        
        返回:
            [str]: 返回一个包含markdown分隔线的列表。分隔线是由一行的三个星号`***`组成。
        
        示例:
            ```
            ms = MSplit_line()
            print(ms.flush_row_anchor(""))
            # 输出：['*** \n']
            ```
        
        注意:
            当前方法未使用到输入参数`anchor_str`，可能存在参数冗余的问题。
        """

        return ["*** \n"]


class MFooter(markdown_item_base):
    """
    这是一个名为`MFooter`的类，它继承自`markdown_item_base`基类。这个类主要用于处理Markdown文档中的页脚信息。
    
    这个类有一个名为`flush_row_anchor`的方法，它会接受一个锚字符串（anchor string）作为输入，并返回一个包含特定格式的字符串列表。这个字符串列表中的第一项是"*** \n"，第二项是当前的时间戳，格式为'%Y-%m-%d %H:%M:%S'。
    
    `flush_row_anchor`方法的参数和返回类型如下：
    - 参数：
      - `anchor_str`：一个字符串，表示输入的锚字符串。
    - 返回类型：
      - 这个方法返回一个字符串列表，列表中的第一项是"*** \n"，第二项是当前的时间戳。
    
    使用这个类的示例：
    
    ```python
    m_footer = MFooter()
    m_footer.flush_row_anchor('example')
    ```
    
    在上述示例中，我们首先创建了一个`MFooter`类的实例，并调用`flush_row_anchor`方法处理指定的锚字符串。
    
    注意：这个类和方法都没有明显的错误或bug，但是在使用过程中，要确保传入`flush_row_anchor`的`anchor_str`参数是字符串类型，否则可能会引发类型错误。
    """

    def flush_row_anchor(self, anchor_str) -> [str]:
        """
        `flush_row_anchor`是`MFooter`类的一个方法，其主要目的是生成markdown的footer部分，该部分包含一个链接和当前的时间。
        
        参数:
        anchor_str (str): 需要生成的markdown链接的字符串。
        
        返回:
        list[str]: 返回一个包含两个字符串元素的列表。第一个元素是markdown的分隔线("*** \n")，第二个元素是当前的时间字符串(采用'%Y-%m-%d %H:%M:%S'格式)，每个元素后都跟着一个换行符("\n")。
        
        使用示例:
        ```python
        footer = MFooter()
        footer.flush_row_anchor("https://www.example.com")
        ```
        
        注意:
        当前版本中，该方法并未使用到参数`anchor_str`，这可能是一个待修复的bug。
        """

        return ["*** \n", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " \n"]


class MUnconvert_str(markdown_item_base):
    """
    `MUnconvert_str` 是一个从 `markdown_item_base` 类继承而来的类，主要用于处理和管理未转换的字符串内容。
    
    这个类主要有两个方法：
    
    - `__init__(self, content)`：初始化方法，接收一个 `content` 参数，表示未转换的字符串内容。
    
    - `flush_row_anchor(self, anchor_str) -> [str]`：该方法接收一个 `anchor_str` 参数，并且返回一个由 `content` 组成的列表。
    
    示例：
    
    ```python
    unconvert_str = MUnconvert_str("Hello World")
    result = unconvert_str.flush_row_anchor("some anchor")
    print(result)  # 输出 ["Hello World"]
    ```
    
    注意：本类不负责对字符串内容进行任何转换处理，只是单纯的返回原始字符串列表。
    """

    def __init__(self, content):
        """
        初始化 MUnconvert_str 类的实例。
        
        MUnconvert_str 类是一个处理 Markdown 项目的基类，它主要是用来处理未转换的字符串。
        
        参数:
            content (str): 未被转换的字符串内容。
        
        属性:
            content (str): 存储传入的字符串内容。
        
        示例:
        
            munconvert_str = MUnconvert_str("原始字符串")
            print(munconvert_str.content)  # 输出: 原始字符串
        """

        self.content = content

    def flush_row_anchor(self, anchor_str) -> [str]:
        """
        这个类`MUnconvert_str`是`markdown_item_base`的一个子类，主要用于处理不需要转换的字符串。
        
        类中的`flush_row_anchor`函数，用于将内容返回为字符串列表。
        
        函数参数:
            anchor_str (str): 作为参数传入，但在当前函数中并未使用。
        
        返回类型:
            返回一个包含单个元素的列表，元素为类初始化时传入的`content`内容。
        
        示例：
            unconvert_str = MUnconvert_str('test')
            print(unconvert_str.flush_row_anchor('any_str'))
            >> ['test']
        
        注意：虽然函数定义中包含`anchor_str`参数，但在函数实现中并未使用，可能是由于历史版本遗留或者未来版本预留的参数。
        """

        return [self.content]


class MCode(markdown_item_base):
    """
    MCode类继承自markdown_item_base基类，用于处理markdown中的代码块部分。
    
    该类的主要目标是将给定的代码内容和代码语言转化为markdown格式的代码块。
    
    类的初始化方法需要两个参数，code_content和code_language，其中code_content参数用于指定代码内容，
    code_language参数用于指定代码语言，默认为"python"。
    
    flush_row_anchor方法用于将code_content和code_language转化为markdown格式的代码块，返回一个字符串列表。
    
    例如：
    ```python
    mc = MCode("print('Hello, world!')", "python")
    mc.flush_row_anchor("anchor")
    输出：
    ['\n', '```python \n', "print('Hello, world!')", '\n', '```\n']
    ```
    
    注意，使用该类时，确保传入的code_content已经被正确转义，否则可能会导致markdown格式错误。
    
    参数:
        code_content (str): 代码内容
        code_language (str, optional): 代码语言，默认为"python"
    
    返回:
        flush_row_anchor方法返回一个包含markdown格式代码块的字符串列表。
    
    异常:
        无法正确处理非字符串类型的code_content或code_language参数时，可能会引发类型错误。
    """

    def __init__(self, code_content, code_language="python"):
        """
        初始化 MCode 类的实例。
        
        MCode 类是用于处理 markdown 中的代码块，提供将代码内容和代码语言封装成一个代码块的功能。
        
        Args:
            code_content (str): 需要封装的代码块的内容。
            code_language (str, optional): 代码块的编程语言，默认为 "python"。
        
        示例:
            mcode = MCode("print('Hello World!')", "python")
            这将创建一个包含 "print('Hello World!')" 的 Python 代码块。
        
        注意:
            目前不支持对代码块内容的语法检查，如果传入的代码内容有语法错误，可能会影响生成的 markdown 文件的正常显示。
        """

        self.content = code_content
        self.lang = code_language

    def flush_row_anchor(self, anchor_str) -> [str]:
        """
        这个类MCode继承自markdown_item_base，用于处理markdown中的代码部分。用户可以通过提供代码内容和代码语言来创建一个MCode对象。默认的代码语言为Python。
        
        例如：
        ```python
        mcode = MCode("print('Hello, World!')", "python")
        ```
        
        此外，此类还提供了一种方法flush_row_anchor，用于生成代码块的markdown表示形式。
        
        ## 方法：flush_row_anchor
        这个方法是用来生成代码块的markdown表示形式。
        
        ### 参数：
        
        - anchor_str: 字符串，指定代码行的锚点。 但是在此函数中并未使用此参数，可能是留待未来版本使用，或者是一个错误。
        
        ### 返回值：
        
        - 返回一个字符串列表，包括markdown代码块的开始标记、代码内容、结束标记。
        
        ### 例子：
        
        假设我们有一个MCode对象，代码内容为“print('Hello, World!')”，代码语言为Python：
        ```python
        mcode = MCode("print('Hello, World!')", "python")
        ```
        调用flush_row_anchor方法：
        ```python
        mcode.flush_row_anchor("any_string")
        ```
        将返回：
        ```python
        ['\n', '```python \n', "print('Hello, World!')", '\n', '```\n']
        ```
        这是一个markdown代码块的表示形式，可以直接插入到markdown文件中。
        
        ### 注意：
        
        当前版本中，anchor_str参数在方法中并未实际使用，这可能是一个错误或者是留给未来版本的特性。
        """

        return ["\n", f"```{self.lang} \n", _convert_char(self.content), "\n", "```\n"]


class MTable(markdown_item_base):
    """
    `MTable` 是一个 markdown 表格生成类，继承自 `markdown_item_base`。这个类的目的是为了方便地创建和管理 markdown 格式的表格。它有三个主要的方法：初始化 (`__init__`)，添加行 (`add_row`) 和刷新行锚 (`flush_row_anchor`)。
    
    初始化方法 (__init__) 接受一个列名列表 (`cols`) 作为输入，创建一个新的 `MTable` 实例。在这个实例中，列名被存储在 `self.cols` 中，而表格的数据被保存在 `self.datas` 中。
    
    添加行方法 (`add_row`) 接受一行数据 (`row`) 作为输入，并将其添加到 `self.datas` 中。
    
    刷新行锚方法 (`flush_row_anchor`) 接受一个锚字符串 (`anchor_str`) 作为输入，并返回一个包含更新后的 markdown 表格的字符串列表。这个方法首先生成标题行和分隔符行，然后遍历 `self.datas` 中的每一行，将每一行的数据转化为字符串并用 `<br>` 替换所有的换行符，最后添加到返回的字符串列表中。
    
    例如：
    
    ```python
    table = MTable(['姓名', '年龄'])
    table.add_row(['小明', '18'])
    table.add_row(['小红', '19'])
    lines = table.flush_row_anchor('demo')
    print(''.join(lines))
    ```
    
    将生成以下的 markdown 表格：
    
    ```
    | 姓名 | 年龄 |
    | ---- | ---- |
    | 小明 | 18 |
    | 小红 | 19 |
    ```
    """

    def __init__(self, cols: [str]):
        """
        初始化MTable类。
        
        MTable类是一个用于处理和存储markdown表格数据的类。它使用一组列名初始化，并存储添加的行数据。最后，可以通过flush_row_anchor方法将表格数据转换为markdown格式。
        
        参数:
        cols: List[str]，一组字符串，用来初始化表格的列名。
        
        属性:
        cols: 用于存放表格的列名。
        datas: 用于存储添加的行数据。
        
        使用示例:
        
        示例 1:
        
           mtable = MTable(['Name', 'Age'])
        
           mtable.add_row(['Tom', '30'])
        
           mtable.add_row(['Jerry', '35'])
        
           print(''.join(mtable.flush_row_anchor('')))
        
        输出:
        
           | Name | Age |
        
           | ---- | ---- |
        
           | Tom  | 30   |
        
           | Jerry| 35   |
        """

        self.cols = cols
        self.datas = []

    def add_row(self, row):
        """
        在当前Markdown表格实例中添加一行数据。
        
        参数:
            row: 一个具有与表格列数相同的元素数量的列表。列表元素将被转换为字符串并添加到Markdown表格中。
        
        返回:
            无
        
        示例:
            >> table = MTable(['Name', 'Age'])
            >> table.add_row(['John', 25])
            >> table.add_row(['Sara', 30])
            此时, Markdown表格中将添加两行数据。
        """

        self.datas.append(row)

    def flush_row_anchor(self, anchor_str) -> [str]:
        """
        这是一个类方法，用于将已添加的行数据转换为Markdown表格的格式。
        
        参数:
            anchor_str: 锚点字符串，该参数实际上在函数内部并未使用。
        
        返回:
            [str]: 返回一个字符串列表，列表中的每一个元素都代表Markdown表格的一行。列表中的字符串可以直接用于生成Markdown表格。
        
        使用方式：
            mtable = MTable(['col1','col2'])
            mtable.add_row(['row1_col1','row1_col2'])
            mtable.add_row(['row2_col1','row2_col2'])
            lines = mtable.flush_row_anchor('anchor')
            for line in lines:
                print(line)
        """

        lines = []
        title = [_convert_char(x) for x in self.cols]
        lines.append(f"| {' | '.join(title)} | \n")
        lines.append(f"| {' | '.join(['----' for _ in title])}  |  \n")
        for row in self.datas:
            row = [str(_x).strip() for _x in row]
            row_new = [str(x).replace('\n', '<br>') for x in row]
            lines.append(f"| {' | '.join(row_new)} | \n")
        lines.append("\n\n")
        return lines


class MImage(markdown_item_base):
    """
    MImage类是一个用于处理Markdown中的图片的类，继承自markdown_item_base。
    
    构造函数接收一个路径作为初始化参数，用来指示图片的位置。
    
    类中实现了flush_row_anchor方法，该方法用于生成一个包含图片的Markdown格式的字符串。
    
    注：这个类暂时没有检测到任何错误或者BUG。
    
    示例：
    ```
    m_image = MImage('path_to_your_image')
    markdown_str = m_image.flush_row_anchor('anchor_str')
    print(markdown_str)
    ```
    
    函数介绍：
    - flush_row_anchor(self, anchor_str) -> [str]
        - anchor_str: 锚点字符串。
        - 返回值: 返回一个列表，列表包含一个Markdown格式的字符串，字符串中包含了图片的HTML标签。
    """

    def __init__(self, path):
        """
        初始化 MImage 类。
        
        MImage 是一个用于处理 Markdown 中图片的类，它继承自 markdown_item_base 基类。对象实例化时，需要传递一个图片路径参数。
        
        参数:
            path (str): 图片的路径。
        
        例子:
            mi = MImage('/path/to/image.jpg')
            mi.flush_row_anchor('anchor_str')
        """

        self.path = path

    def flush_row_anchor(self, anchor_str) -> [str]:
        """
        这是一个MImage类的方法，用于生成markdown的图片链接。
        
        Args:
            anchor_str: 一个锚字符串，用于标识图片。但是在当前的方法实现中，这个参数并未被使用。
        
        Returns:
            返回一个字符串列表，列表中只有一个元素，这个元素是一个markdown的图片链接。图片链接的形式是：
            ![a{当前时间戳}](图片路径)
            其中，a和当前时间戳组成了图片的标识符，图片路径是类在初始化时传入的路径。
        
        注意：
            此方法会忽略anchor_str参数。
            使用此方法需要确保传入的图片路径是正确的，否则生成的markdown链接可能无法正常工作。
        """

        return [f"![a{str(time.time())}]({self.path})\n"]


class Mstring(markdown_item_base):
    """
    # Mstring类是一个基于markdown的字符串处理类，它继承自markdown_item_base基础类。
    # 这个类主要用来存储和处理markdown格式的字符串，提供一些常用的方法进行字符串的添加和格式化。
    
    该类的主要方法包括：
    
    - `__init__`：初始化方法，用于创建一个Mstring实例，该实例内容为空。
    
    - `set`：添加字符串的方法，可以把指定的字符串content添加到实例的内容中。
    
    - `set_bold`：添加加粗字符串的方法，可以把指定的字符串content以加粗的格式添加到实例的内容中。
    
    - `flush_row_anchor`：返回实例内容的方法，返回的是一个包含所有字符串的列表。
    
    一个使用Mstring类的例子：
    
    ```python
    ms = Mstring()
    ms.set('Hello, world!')
    ms.set_bold('I am bold text.')
    print(ms.flush_row_anchor())
    ```
    
    在上面的例子中，我们创建了一个Mstring实例ms，并分别添加了普通字符串和加粗字符串。最后我们打印出这个实例的所有内容。
    
    注意：
    在使用`set`和`set_bold`方法时，输入的字符串会被`_convert_char`方法处理，这个方法的具体实现并没有在这里给出，可能会对字符串的内容进行一些转换或者过滤。
    """

    def __init__(self):
        """
        初始化Mstring类的实例。
        
        Mstring类是一个处理Markdown语法的类，用户可以使用此类添加和处理字符串内容，并将其转换为Markdown格式。此类包括添加普通内容(set方法)和加粗内容(set_bold方法)等功能。初始化Mstring类的实例时，将创建一个空列表用于存储字符串内容。
        
        示例:
             mstring = Mstring()
             mstring.set('hello')
             mstring.set_bold('world')
             mstring.contents
            ['hello', '**world**']
        
        注意:
            类的方法中使用了_convert_char函数来处理特殊Markdown字符，但此函数在给定的代码段中未定义。如果未在其他地方定义，这可能会导致运行错误。
        
        """

        self.contents = []

    def set(self, content):
        """
        这是一个set函数，用于设置Mstring类的内容。具体做法是将输入的内容转化为特定格式，然后添加到类的内容列表中。
        
        参数列表:
            content: 需要添加的内容，类型为str。
        
        返回类型:
            无。
        
        注意：
            本函数使用了内部函数_convert_char()，用于将输入的内容转化为特定格式。如果输入的内容不能被_convert_char()接受，可能会抛出异常。
        """

        self.contents.append(_convert_char(content))

    def set_bold(self, content):
        """
        将传入的字符串转化为markdown语言的加粗格式并添加到内容列表。
        
        参数:
            content (str): 需要设置为加粗的字符串。
        
        返回:
            无返回值
        
        示例:
            mstring = Mstring()
            mstring.set_bold("Hello World")
            assert mstring.contents == ["**Hello World**"]
        """

        self.contents.append(f"**{_convert_char(content)}**")

    def flush_row_anchor(self, anchor_str) -> [str]:
        """
        此方法的设计目的是获取Mstring实例的所有内容并返回。内容保存在实例的contents变量中，这是一个列表，所以此方法直接返回这个列表。
        
        参数:
            anchor_str (str): 这个参数在方法中没有被使用，可能是为了与其他方法保持一致的参数列表而设计的。
        
        返回类型:
            List[str]: 返回Mstring实例的所有内容，都保存在一个字符串列表中。
        
        注意:
            此方法可能存在错误或者bug，因为在方法中并没有使用到参数anchor_str，这可能会导致一些不可预见的问题。
        """

        return [ll + "\n\n" for ll in self.contents]


class markdowndoc:
    # version 1.1

    """
    这是一个处理markdown文档的类`markdowndoc`。类的主要功能是接收字符串或者markdown项目（markdown_item_base类型），然后将它们转换成markdown格式的文本，并写入到指定的文件中。
    
    类的主要属性包括：
      - `items`：存储markdown项目的列表
      - `stream_lines`：存储待写入文件的字符串列表
      - `stream_lines_type`：存储待写入字符串的类型列表
      - `path`：指定的写入文件的路径
    
    类的主要方法包括：
      - `flush`：依次处理`items`中的markdown项目和`stream_lines`中的字符串，将它们转换成markdown格式，并写入到指定的文件中。
      - `write`：接收字符串或markdown项目，并将它们存储到相应的列表中。
    
    使用示例：
    
    ```python
    doc = markdowndoc('example.md') #创建一个实例，指定写入文件名为'example.md'
    doc.write('hello world!')  # 添加字符串到doc中
    item = markdown_item_base('example')  # 创建一个markdown项目
    doc.write(item)  # 添加markdown项目到doc中
    doc.flush()  # 写入到文件
    ```
    以上示例将创建一个名为'example.md'的markdown文件，文件内容为转换后的字符串'hello world!'和markdown项目。
    
    注意事项：
      - `write`方法只接收字符串和markdown_item_base类型的参数，如果输入其他类型的参数，将不会被处理。
      - `flush`方法需要在所有内容添加完毕后调用，以保证所有内容能够正确转换并写入文件。
    """

    def __init__(self, path):
        """
        初始化markdowndoc类的实例。
        
        参数：
            path (str): 文件的路径，用于保存markdown文档的内容。
        
        属性：
            items (list): 用于存储markdown项的列表，每个项是markdown_item_base类的实例。
            stream_lines (list): 用于存储markdown文档的实际行内容的列表。
            stream_lines_type (list): 用于存储与stream_lines对应的行类型的列表。-1表示该行是普通文本，其他值表示该行是markdown项，值为该项在items列表中的索引。
            path (str): 文件路径。
        
        用法示例：
            md = markdowndoc("example.md")
            md.write("Hello, world!")
            md.flush()  # 将"Hello, world!"写入example.md文件
        
        注意：
            这个类并没有处理文件路径无效或者无法写入的情况，使用者需要确保提供的路径是有效的，且具有写入权限。
        """

        self.items: list[markdown_item_base] = []
        self.stream_lines = []
        self.stream_lines_type = []
        self.path = path

    def flush(self):
        """
        这是一个用于处理Markdown文档对象（`markdowndoc`类）的`flush`方法。此方法的主要目的是将当前文档对象中的所有项目（`items`）和流行（`stream_lines`）转换成最终的markdown文档输出行（`doc_output_lines`）。最后，这些输出行将被写入到目标文件中。
        
        在此过程中，对于每个项目，会先调用`flush_begin`方法进行初始化操作。然后，对于每个流行，根据其类型进行不同的处理。如果流行类型为-1，表示这是一个普通字符串，直接进行字符的转换并添加到输出行中。如果流行类型不是-1，表示这是一个markdown项目，会使用该项目的`flush_row_anchor`方法进行处理并将处理结果添加到输出行中。
        
        此方法无需显式的参数输入，同时也不会返回任何结果。
        
        注意，此方法在使用前，请确保提供正确的markdown项目和流行，否则可能会导致生成的markdown文档格式错误。
        
        参数:
        无
        
        返回:
        无
        
        错误和异常:
        可能会因为提供的markdown项目或流行格式不正确导致生成的markdown文档格式错误。
        
        示例:
        ```python
        doc = markdowndoc(path="path_to_your_file")
        doc.write("Your Markdown content")
        doc.flush()
        ```
        以上示例会将字符串`"Your Markdown content"`写入到名为`path_to_your_file`的文件中。
        """

        write_file(self.path, self.flush_out_str())

    def flush_out_str(self):
        doc_output_lines = []

        for item in self.items:
            item.flush_begin()

        for line, line_type in zip(self.stream_lines, self.stream_lines_type):
            if line_type == -1:
                doc_output_lines.append(_convert_char(line))
            else:
                convert_lines = self.items[line_type].flush_row_anchor(line)
                for l in convert_lines:
                    doc_output_lines.append(l)
                pass

        return "".join(doc_output_lines)

    def write(self, content):
        """
        这是一个write函数，用于将内容写入Markdown文件。
        
        根据传入的内容类型，该函数会将内容添加到文档流中，并更新流类型列表。如果内容是字符串，那么它将被直接添加到文档流中，同时在流类型列表中添加-1。如果内容是markdown_item_base类的实例，那么它将被添加到items列表中，同时在文档流和流类型列表中添加相应的指针和类型。
        
        参数：
            content：写入的内容，可以是字符串或者markdown_item_base类的实例。
        
        返回：
            返回传入的内容。
        
        例如，你可以这样调用write函数：
        
            doc = markdowndoc('path_to_your_file')
            doc.write('This is a markdown document.')
            item = markdown_item_base('title', 'This is a title.')
            doc.write(item)
        
        这样，字符串和markdown_item_base实例都会被写入到markdown文件中。
        """

        if isinstance(content, str):
            self.stream_lines_type.append(-1)
            self.stream_lines.append(content + "\n\n")
        if isinstance(content, markdown_item_base):
            self.items.append(content)
            self.stream_lines_type.append(len(self.items) - 1)
            self.stream_lines.append(content.anchor_pointer_outer())
        return content

# def write_title(self, stra, level):
#
#     if not self.title_with_index:
#         self.file_lines.append(f"{self._generate_count_char('#', level)} {self._convert_char(stra)} \n")
#     else:
#         if level > self._title_index_level:
#             if level != self._title_index_level + 1:
#                 raise Exception("title level error")
#             self.title_index_stack.append(1)
#             self._title_index_level = level
#         elif level == self._title_index_level:
#             self.title_index_stack[-1] += 1
#         elif level < self._title_index_level:
#             while True:
#                 if len(self.title_index_stack) > level:
#                     self.title_index_stack.pop(-1)
#                     continue
#                 break
#             self.title_index_stack[-1] += 1
#             self._title_index_level = level
#         index_str = ".".join([str(xx_) for xx_ in self.title_index_stack])
#         self.title_index[stra] = index_str
#         self.file_lines.append(f"{self._generate_count_char('#', level)} {index_str} {self._convert_char(stra)} \n")
#
