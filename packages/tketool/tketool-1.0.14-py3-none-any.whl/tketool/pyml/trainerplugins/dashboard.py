# pass_generate
import pickle, os, threading
from flask import Flask, send_from_directory, send_file, url_for, redirect
import logging
from tketool.logs import get_log_history
from jinja2 import Environment, FileSystemLoader, PackageLoader
from tketool.pyml.pytrainer import *
from datetime import datetime, timedelta


class dashboard_plugin(trainer_plugin_base):
    """
    这是一个名为dashboard_plugin的类，它继承自trainer_plugin_base。这个类的主要目的是为训练过程提供一个可视化的仪表板，用于实时监视训练过程中的变化，如损失函数值、参数更新次数、模型的训练进度等。它使用了flask框架来启动一个web服务，使用者可以在本地浏览器中查看训练过程。这个类还提供了一些辅助函数，比如时间戳的转换、数据的缩放等。
    
    使用这个类时，只需要在训练脚本中创建一个dashboard_plugin的实例，然后在训练循环中调用其相关方法即可。例如：
    
    ```python
    dashboard = dashboard_plugin(port=8080)
    for epoch in range(epochs):
        for batch in dataloader:
            ...
            dashboard.step_cost_cal(global_state, epoch_state, step_state)
        dashboard.epoch_end(global_state, epoch_state, step_state)
    dashboard.start(global_state, epoch_state, step_state)
    ```
    
    类内方法描述：
    1. `__init__(self, port=None)`: 这是初始化方法，创建一个dashboard_plugin的实例。参数port是可选的，表示flask服务监听的端口号，默认为None。
    2. `convert_time(self, timestamp)`: 这个方法用于将时间戳转换为本地时间。
    3. `start(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board)`: 这个方法在训练开始时调用，用于初始化一些状态和启动flask服务。
    4. `_scale_data(self, data: list)`: 这是一个私有方法，用于缩放数据，使得它们能在仪表板上更好地显示。
    5. `refresh_page(self, global_state: global_state_board)`: 这个方法在每次训练轮次结束时调用，用于刷新仪表板的显示。
    6. `epoch_end(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board)`: 这个方法在每个训练轮次结束时调用，用于记录本轮次的损失函数值。
    7. `start_flask_server(self, global_state: global_state_board)`: 这个方法用于启动flask服务。
    8. `step_cost_cal(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board)`: 这个方法在每个训练步骤结束时调用，用于计算本步骤的耗时。
    9. `epoch_cost_cal(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board)`: 这个方法在每个训练轮次结束时调用，用于计算本轮次的耗时。
    
    注意：这个类目前没有发现明显的bug或错误，但需要注意的是，如果训练数据量过大，可能会引起flask服务的内存溢出问题。
    """

    def __init__(self, port=None):
        """
        初始化dashboard_plugin类。这个类用于监测训练过程，可以实时查看训练过程中的损失、精度等信息，支持通过web页面查看。
        
        参数:
            port: int或None, 可选参数, 默认为None.
                用于开启flask服务器的端口号。如果为None，将不会开启flask服务器。
        
        属性：
            epoch_data: list, 用于存储每个epoch的数据。
            port: int或None, flask服务器的端口号。
            step_count: int, 统计训练过程中的步数。
            step_cost: float, 统计每步的耗时。
            epoch_count: int, 统计训练过程中的epoch数。
            epoch_cost: float, 统计每个epoch的耗时。
            process_batch_count: int, 每次处理的batch数。
            process_batch_index: int, 当前正在处理的batch的索引。
            buffer_global_state: global_state_board对象, 用于存储全局状态。
            template: jinja2模板对象, 用于渲染web页面。
        
        示例：
            db_plugin = dashboard_plugin(port=5000) # 创建一个dashboard_plugin对象，并指定flask服务器的端口为5000
        """

        self.epoch_data = []
        self.port = port

        self.step_count = 0
        self.step_cost = 0

        self.epoch_count = 0
        self.epoch_cost = 0

        self.process_batch_count = 100
        self.process_batch_index = 1

        self.buffer_global_state = None
        # self.buffer_epoch_state = None
        # self.buffer_step_state = None

        env = Environment(loader=PackageLoader('tketool.pyml', 'trainerplugins'))
        # env = Environment(loader=FileSystemLoader('pyml/trainerplugins/'))
        self.template = env.get_template("webreport_temp.html")

    def convert_time(self, timestamp):
        """
        这是一个将时间戳转换为本地时间字符串的函数。
        
        参数:
            timestamp (int): 时间戳，代表某一时刻的秒数。
        
        返回:
            str: 本地时间字符串，格式为YYYY-MM-DD HH-MM-SS。
        
        使用示例:
            >>> convert_time(1609459200)
            '2021-01-01 08-00-00'
        
        注意:
            该函数默认的时区是东八区，即中国北京时间。
        """

        utc_time = datetime.utcfromtimestamp(timestamp)
        local_time = utc_time + timedelta(hours=8)
        return local_time.strftime('%Y-%m-%d %H-%M-%S')

    @invoke_at([plugin_invoke_Enum.Begin])
    def start(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        """
        这是一个名为"start"的成员函数，它是dashboard_plugin类的一部分。这个函数在插件开始时被调用，用于初始化一些参数并可能启动一个Flask服务器。
        
        参数:
        global_state (global_state_board): 一个global_state_board对象，包含全局状态信息，如batch_count等。
        epoch_state (epoch_state_board): 一个epoch_state_board对象，包含了当前时间步的训练状态信息。
        step_state (step_state_board): 一个step_state_board对象，包含了每个训练步骤的状态信息。
        
        返回:
        无返回值。
        
        异常:
        无异常。
        
        示例:
        假设我们有一个dashboard_plugin对象dp，全局状态对象gs，时间步状态对象es和步骤状态对象ss，可以如下调用此函数：
        dp.start(gs, es, ss)
        
        注意:
        这个函数可能会启动一个Flask服务器，这取决于端口是否被设置。如果端口被设置，Flask服务器将被启动用于处理web请求。
        """

        if self.port is not None:
            self.start_flask_server(global_state)

        self.process_batch_count = global_state.batch_count
        self.buffer_global_state = global_state

    def _scale_data(self, data: list):
        """
        这个方法是用来对数据进行缩放的。其作用是对一个比较大的数据集进行缩放，使得它的长度可以适应图表的绘制。如果数据集的大小超过200，那么它会取第一个数据，然后对剩余的数据每两个进行一次平均，最后取最后一个数据。如果数据集的大小没有超过200，那么直接返回原数据集。
        
        参数:
            data: list，需要进行缩放处理的数据集。
        
        返回:
            list，长度被缩放后的数据集。
        """

        len_list = []
        if len(data) > 200:
            len_list.append(data[0])
            for x in range(2, len(data) - 1):
                len_list.append((data[x] + data[x - 1]) / 2)
            len_list.append(data[-1])
        else:
            len_list = data
        return len_list

    def refresh_page(self, global_state: global_state_board):
        """
        这个方法用于刷新训练进度的可视化仪表板页面。
        
        参数：
            global_state (global_state_board): 一个全局状态对象，包含所有全局级别的信息，如模型、优化器等的状态。
        
        返回：
            无
        
        我们首先将历史的epoch数据进行缩放以适应可视化图表。然后，我们从全局状态对象中获取训练的相关信息，并且将它们组织成一个字典。接着，我们用这些信息来生成一个新的HTML页面，该页面可以显示在训练过程中的各种信息，包括模型的训练进度、损失和精度等。最后，我们将生成的HTML保存到指定的文件中。
        
        这个方法没有返回值，它的目的是生成一个新的HTML页面来展示训练的状态。这个页面可以在训练过程中不断刷新，以达到实时查看训练进度的效果。
        """

        self.epoch_data = self._scale_data(self.epoch_data)

        model_info = {
            "epoch_count": global_state.epoch_count,  # base_wall['epoch_count'],
            "set_name": global_state.sample_set.set_name,  # base_wall['train_set'].set_name,
            "model_folder": global_state.model_folder,  # base_wall['model_folder'],
            "train_epoch": len(self.epoch_data),
            "parameter_update_times": global_state.parameter_update_times,
            "parameter_count": global_state.update_parameter_count,
            "start_time": self.convert_time(global_state.start_time),
            "type_precision": str(""),
            "per_step_cost": float(self.step_cost) / self.step_count if self.step_count > 0 else 0,
            "per_epoch_cost": float(self.epoch_cost) / self.epoch_count if self.epoch_count > 0 else 0,
            # base_wall['parameter_update_times'],
        }

        # Separate epoch data into different lists for plotting
        epoch_loss_index = list(range(len(self.epoch_data)))
        epoch_loss = self.epoch_data

        all_keys_data = global_state.chart_datas
        all_keys_data_length_data = [len(v) for v in all_keys_data.values()]

        template_vars = {"model_info": model_info,
                         "progress_value_val": self.process_batch_index,
                         "progress_value_max": self.process_batch_count if self.process_batch_count > 0 else 1,
                         "progress_value_str": f"{self.process_batch_index} / {self.process_batch_count}",
                         "epoch_index": epoch_loss_index,
                         "epoch_loss": epoch_loss,
                         "all_keys": all_keys_data,
                         "log_content": "\n".join(get_log_history()),
                         "all_keys_data_length": max(all_keys_data_length_data) if len(
                             all_keys_data_length_data) > 0 else 0
                         }

        wpath = os.path.join(global_state.model_folder, 'web_report.html')
        with open(wpath, 'w', encoding='utf-8') as f:
            f.write(self.template.render(template_vars))

    @invoke_at([plugin_invoke_Enum.Epoch_end])
    def epoch_end(self, global_state: global_state_board, epoch_state: epoch_state_board, step_state: step_state_board):
        """
        此函数的主要功能是在每个周期结束时更新相关状态信息。
        
        函数参数:
        - global_state (global_state_board): 保存全局状态信息的类实例。
        - epoch_state (epoch_state_board): 保存周期状态信息的类实例。
        - step_state (step_state_board): 保存步骤状态信息的类实例。
        
        返回值: 无
        
        注：此函数没有返回值，它主要是在每个训练周期结束时，更新保存在实例中的状态信息，包括周期损失等。并且，该函数也会把当前的全局状态信息保存到buffer_global_state变量中，以备后续使用。
        """

        epoch_loss = epoch_state.epoch_loss  # epoch_wall['epoch_loss']
        # epoch_data = (epoch_loss, {})
        self.epoch_data.append(epoch_loss)
        self.buffer_global_state = global_state

    def start_flask_server(self, global_state: global_state_board):
        """
        此方法用于启动一个Flask服务器，以便于查看模型训练的实时报告。
        
        参数:
            global_state (global_state_board):
                global_state对象，包含了模型训练的全局状态信息。
        
        此方法不返回任何值。
        
        方法中主要步骤如下：
        1. 创建一个Flask应用实例，设置静态文件夹为模型保存的文件夹。
        2. 设定Flask应用的日志级别，设置为ERROR，只有错误信息会被记录。
        3. 定义Flask应用的路由。当访问服务器的根目录('/')时，会调用serve_dashboard函数。该函数会刷新报告页面，并返回生成的HTML文件。
        4. 启动一个新线程来运行Flask应用，以便于主程序继续执行模型训练，而不会被阻塞。
        
        注意：
        这个方法会在主程序中开启一个新的线程来运行Flask服务器，以便于主程序继续执行模型训练。但是因为Flask服务器和主程序共享了全局状态对象，所以在多线程环境下可能会出现数据竞争的问题。目前的代码中并没有看到对全局状态对象的写操作，所以应该不会出现数据竞争的问题。但是如果后续有对全局状态对象的写操作，需要注意线程安全问题。
        
        此外，如果同时启动了多个训练任务，由于所有任务都在同一个端口启动服务器，可能会出现端口冲突问题。可以考虑让用户在启动任务时指定端口，或者动态分配端口以避免冲突。
        """

        app = Flask(__name__, static_folder=os.path.join(os.getcwd(), global_state.model_folder))

        app.logger.setLevel(logging.ERROR)
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

        @app.route('/')
        def serve_dashboard():
            self.refresh_page(self.buffer_global_state)
            return send_from_directory(app.static_folder, 'web_report.html')
            # return redirect(url_for('static', filename='web_report.html'))

        thread = threading.Thread(target=app.run, kwargs={'port': self.port, 'host': '0.0.0.0'})
        thread.start()

    @invoke_at([plugin_invoke_Enum.Batch_end])
    def step_cost_cal(self, global_state: global_state_board, epoch_state: epoch_state_board,
                      step_state: step_state_board):
        """
        这个函数是用来计算每个步骤的耗时并更新处理批次的索引的。
        
        参数:
            global_state (global_state_board): 全局状态板，保存了全局状态的信息。
            epoch_state (epoch_state_board): epoch状态板，保存了epoch状态的信息。
            step_state (step_state_board): 步骤状态板，保存了步骤状态的信息。
        
        返回值:
            无返回值
        """

        self.step_count += 1
        self.step_cost += step_state.end_time - step_state.start_time

        self.process_batch_index = step_state.batch_idx

    @invoke_at([plugin_invoke_Enum.Epoch_end])
    def epoch_cost_cal(self, global_state: global_state_board, epoch_state: epoch_state_board,
                       step_state: step_state_board):
        """
        该函数主要用于计算每个epoch的运算时间成本。该函数会在每个epoch结束时被调用。
        
        参数:
            global_state: global_state_board类的一个实例，表示全局状态信息。其中包含了训练过程中的各种全局性的信息。
            epoch_state: epoch_state_board类的一个实例，表示当前epoch状态信息。其中包含了当前epoch的训练信息，如epoch的损失等。
            step_state: step_state_board类的一个实例，表示当前step状态信息。其中包含了当前训练步骤的信息，如每步的开始和结束时间等。
        
        返回:
            无返回值。但是会修改类的属性，计算并更新self.epoch_count（完成的epoch数量）和self.epoch_cost（完成所有epoch花费的时间）。
        
        注意事项:
            1. 该函数计算的是每个epoch的运算时间，即完成一个epoch所花费的时间。是通过结束时间减去开始时间得到的。
            2. 该函数会在每个epoch结束时被调用一次，所以self.epoch_count和self.epoch_cost会在每个epoch结束时更新。
        """

        self.epoch_count += 1
        self.epoch_cost += epoch_state.end_time - epoch_state.start_time
