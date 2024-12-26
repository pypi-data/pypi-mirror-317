# pass_generate
import threading, time
from queue import Queue
from collections import OrderedDict


class AtomicCounter:
    """
    这是一个线程安全的原子计数器类，使用python的内置线程锁(threading.Lock)实现。
    
    类的主要目的是在多线程环境下提供一个安全的自增操作。它用于在多线程中跟踪某些资源的使用情况，例如计数器或ID生成器等。
    
    类的使用方式如下：
    ```python
    counter = AtomicCounter() # 创建一个原子计数器实例
    
    counter.increment() # 自增1
    counter.increment(3) # 自增3
    print(counter.Value) # 获取当前值
    ```
    
    主要方法：
    - __init__：类的构造函数，初始化value为0，_lock为线程锁。
    
    - increment(add_value=1)：自增函数，参数为自增的值，默认为1。使用线程锁保证在多线程环境下的安全性。函数返回自增后的值。
    
    - Value：类的property属性，返回当前的计数值。
    
    注意：目前类是线程安全的，但是在多进程环境下未经测试，可能会有问题。
    """

    def __init__(self):
        """
        初始化AtomicCounter类。
        
        这个类是一个线程安全的计数器，用于在多线程环境中安全地增加一个计数值。它使用了一个线程锁来确保在增加计数值时的线程安全。
        
        属性:
            value: 计数器的当前值。初始值为0。
            _lock: 一个线程锁，用于在增加计数值时保持线程安全。
        
        使用示例:
        ```python
        counter = AtomicCounter()
        counter.increment()
        print(counter.Value)  # 输出: 1
        ```
        """

        self.value = 0
        self._lock = threading.Lock()

    def increment(self, add_value=1):
        """
        此函数是为了增加AtomicCounter类的value值。
        
        参数:
            add_value (int, optional): 要增加的值，默认值为1
        
        返回:
            Incremented value after adding the `add_value` to the current value.
        
        此函数通过使用线程锁确保了在多线程环境下的安全性，可以防止数据竞争。
        
        示例：
            counter = AtomicCounter()
            counter.increment(5)
            print(counter.Value)  # 输出: 5
            counter.increment()
            print(counter.Value)  # 输出: 6
        
        注意:此函数不是线程安全的，如果在没有使用线程锁的情况下在多线程环境中使用，可能会导致数据的不一致。为了避免这种情况，应当始终在调用此函数时使用线程锁。
        """

        with self._lock:
            self.value += add_value
            return self.value

    @property
    def Value(self):
        """
        这是一个类的属性方法，用于获取AtomicCounter类实例的当前值。
        
        Attributes:
            无
        
        Returns:
            返回AtomicCounter类实例的当前value值，为整数类型。
        
        Examples:
            假设我们有一个AtomicCounter类的实例counter，可以通过以下方式获取其当前值：
        
            >>> counter = AtomicCounter()
            >>> counter.increment(5)
            5
            >>> print(counter.Value)
            5
        
        Notes:
            这个方法是线程安全的，可以在多线程环境下安全使用。
        """

        return self.value


def do_multitask(iterations, task_fun, thread_count=3, max_queue_buffer=0):
    """
    这是一个多线程任务执行函数，目的是将任务分配给多个线程并行处理，以提高任务执行效率。使用生产者-消费者模型，一个线程负责将任务放入队列，多个工作线程从队列中取出任务执行，然后将结果放入结果队列，最后从结果队列中取出所有结果。
    
    参数:
    iterations: 可迭代对象，表示需要处理的任务集合
    task_fun: 函数，表示处理任务的函数，接受一个参数，即从iterations中取出的任务
    thread_count: int，可选参数，默认为3，表示工作线程的数目
    max_queue_buffer: int，可选参数，默认为0，表示任务队列和结果队列的最大容量，如果为0，则队列容量无限制
    
    返回:
    生成器，每次生成一个元组，元组的第一个元素是任务，第二个元素是该任务的处理结果
    
    示例:
    def task_fun(x):
        return x * x
    
    for item, result in do_multitask(range(10), task_fun, thread_count=5):
        print(f'任务：{item}，结果：{result}')
    
    注意事项：
    - 输入的任务集合必须是可迭代的
    - 处理任务的函数必须接收一个参数
    - 线程数必须是正整数
    - 队列最大容量必须是非负整数
    - 本函数不保证任务的执行顺序和结果的生成顺序与输入的任务集合的顺序一致
    """

    task_q = Queue(maxsize=max_queue_buffer)
    result_q = Queue(maxsize=max_queue_buffer)

    locker_queue = Queue(maxsize=thread_count + 1)
    for _ in range(thread_count + 1):
        locker_queue.put(threading.Event())

    def put_task():
        """
        `put_task`是一个内部定义的函数，用于异步地将任务放入队列并管理线程锁。
        
        该函数首先通过迭代给定的任务，将每个任务以及对应的线程锁放入队列中，然后等待每个任务完成，并将完成的任务放在结果队列中。
        
        在所有任务都放入队列后，该函数还会在队列中添加`None`任务，用于通知所有工作线程退出。
        
        在所有任务都处理完成后，该函数会等待最后一个任务的完成，然后退出。
        
        该函数没有输入参数，也没有返回值。
        
        函数内部的`last_lock`变量用于存储上一个任务的线程锁，`current_lock`变量用于存储当前任务的线程锁。
        
        以下是一个简单的使用示例：
        
        ```python
        def put_task():
            last_lock = None
            for item in iterations:
                current_lock = locker_queue.get()
                current_lock.clear()
                task_q.put((last_lock, item, current_lock), block=True)
                last_lock = current_lock
            for _ in range(thread_count):
                task_q.put((None, None, None))
            last_lock.wait()
        ```
        
        注意：本函数在多线程环境中运行，需要确保线程同步和互斥。在实际使用中，应注意避免线程死锁和资源竞争的问题。
        """

        last_lock = None
        # 将任务放入队列
        for item in iterations:
            current_lock = locker_queue.get()
            current_lock.clear()
            task_q.put((last_lock, item, current_lock), block=True)
            last_lock = current_lock

        for _ in range(thread_count):  # 在队列中加入None，以通知所有工作线程退出
            task_q.put((None, None, None))

        last_lock.wait()

    Insert_thread = threading.Thread(target=put_task)
    Insert_thread.start()

    def worker():
        """
        这是一个工作线程函数，其主要功能是获取任务队列中的任务并执行，执行完成后将结果放入结果队列。如果队列中的任务为空，则终止循环。
        
        函数的工作流程如下：
        
        1. 从任务队列中获取任务，如果任务为空，则终止循环。
        2. 使用传入的任务函数处理任务。
        3. 如果上一个任务锁存在，等待上一个任务完成后再继续。
        4. 将处理结果与原始任务一起放入结果队列。
        5. 设置当前任务锁，表示当前任务已经完成。
        
        参数：
        无
        
        返回：
        无
        
        示例:
        
        假设我们有一个简单的任务函数，它只是将输入的数字乘以2：
        
        ```
        def multiply_by_two(n):
            return n * 2
        ```
        我们可以用这个任务函数和我们的工作线程函数一起使用，以在多个线程上并行处理一系列数值：
        
        ```
        for result in do_multitask(range(10), multiply_by_two, thread_count=5):
            print(result)
        ```
        这将会打印出每个数值乘以2的结果。
        
        注意：此函数应在多线程环境中使用，不应在主线程中直接调用。
        """

        while True:
            last_lock, item, cur_lock = task_q.get(block=True)
            if item is None:
                break
            result = task_fun(item)

            if last_lock is not None:
                last_lock.wait()
                locker_queue.put(last_lock)

            result_q.put((item, result))
            cur_lock.set()

    # 启动工作线程
    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    for _ in iterations:
        yield result_q.get(block=True)

# def ddd(a):
#     time.sleep(0.5)
#     return a + 10
#
#
# for p in do_multitask([1, 2, 3, 4, 5, 6, 7, 8, 9], ddd, max_queue_buffer=5):
#     print(p)
#
# time.time()
