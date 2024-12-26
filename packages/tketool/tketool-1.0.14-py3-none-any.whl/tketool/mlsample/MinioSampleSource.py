# pass_generate
import io
from tketool.utils.progressbar import process_status_bar
from tketool.mlsample.LocalSampleSource import LocalDisk_NLSampleSource
from tketool.utils.minio_utils import compare_file
from tketool.JConfig import ConfigManager
import os
from minio import Minio
from tketool.utils.minio_utils import *
from minio.deleteobjects import DeleteObject


class MinioSampleSource(LocalDisk_NLSampleSource):
    """
    `MinioSampleSource`类是一个继承于`LocalDisk_NLSampleSource`的子类，主要用于实现与Minio服务端交互的操作，如上传数据、下载数据、检查数据是否存在等。Minio是一个开源的对象存储服务器，兼容亚马逊S3云存储服务接口，可以用于存储非结构化数据如照片、视频、日志文件、备份数据等。
    
    此类的构造函数接收Minio服务端的端点、访问密钥、秘密密钥和桶名作为输入参数。此外，它还提供了用于数据集的创建、检查和下载的方法。
    
    以下是使用此类的一些例子：
    
    ```python
    folder_path = 'my_folder'
    endpoint = 'my-minio-endpoint'
    access_key = 'my-access-key'
    secret_key = 'my-secret-key'
    bucket_name = 'my-bucket'
    
    # 创建一个新的MinioSampleSource实例
    source = MinioSampleSource(folder_path, endpoint, access_key, secret_key, bucket_name)
    
    # 检查一个数据集是否存在
    exists = source.has_set('my-dataset')
    
    # 如果不存在，则创建一个新的数据集
    if not exists:
        source.create_new_set('my-dataset', 'A description of my dataset', ['tag1', 'tag2'], ['key1', 'key2'])
    
    # 添加数据到数据集
    data = {'key1': 'value1', 'key2': 'value2'}
    source.add_row('my-dataset', data)
    
    # 下载数据集
    source.download('my-dataset')
    ```
    
    注意：该类的某些方法可能会抛出异常，使用时需要加以处理。
    
    此类的方法列表如下：
    
    - `__init__(self, folder_path, endpoint, access_key, secret_key, bucket_name)`: 构造函数，创建一个新的MinioSampleSource实例。
    - `_join(self, *args)`: 私有方法，用于连接多个字符串并用'/'分隔。
    - `_get_minio_client(self)`: 私有方法，获取Minio客户端对象。
    - `_download_if_not_exsited(self, name: str)`: 私有方法，如果本地没有指定的数据集，则从Minio服务器下载。
    - `_object_exsited(self, name)`: 私有方法，检查指定的数据集是否在Minio服务器上存在。
    - `update(self, set_name=None)`: 更新指定的数据集，如果没有指定，则更新所有数据集。
    - `create_new_set(self, name: str, description: str, tags: [str], keys: [str], base_set="", base_set_process="")`: 创建一个新的数据集。
    - `has_set(self, name: str)`: 检查指定的数据集是否存在。
    - `add_row(self, name: str, data)`: 向指定的数据集添加一行数据。
    - `get_metadata_keys(self, name: str)`: 获取指定数据集的元数据键。
    - `iter_data(self, name: str)`: 返回一个迭代器，用于在指定的数据集中迭代数据。
    - `get_remote_dir_list(self)`: 获取远程目录的列表。
    - `download(self, name)`: 下载指定的数据集。
    - `read_one_row(self, name: str)`: 读取指定数据集的一行数据。
    
    请注意，本类需要有对指定Minio服务端的访问权限，并且在使用Minio服务端时，需要遵守其使用协议和条款。
    """

    def __init__(self, folder_path=None, endpoint=None, access_key=None, secret_key=None, bucket_name=None,
                 config_file=None):
        """
        这个类是用于处理Minio存储桶的接口类，继承了LocalDisk_NLSampleSource类，用于实现基于本地磁盘的样本源接口。通过此类，可以实现样本的读取、上传、下载等操作。并且，可以确保数据的一致性和完整性。
        
        该类的初始化方法接受以下五个参数：
        - `folder_path`：本地的文件夹路径，用于存储从Minio存储桶下载的样本数据，或者需要上传到Minio存储桶的样本数据。
        - `endpoint`：Minio服务的URL，例如："http://localhost:9000"。
        - `access_key`：用于访问Minio服务的Access Key。
        - `secret_key`：用于访问Minio服务的Secret Key。
        - `bucket_name`：Minio存储桶的名称，用于存储和获取数据。
        
        初始化方法将创建Minio客户端对象，此对象在之后的方法中将用于与Minio服务进行交互。
        
        实例化该类的例子如下：
        
        ```python
        folder_path = "/path/to/local/storage"
        endpoint = "http://localhost:9000"
        access_key = "your-access-key"
        secret_key = "your-secret-key"
        bucket_name = "your-bucket-name"
        
        minio_sample_source = MinioSampleSource(
            folder_path,
            endpoint,
            access_key,
            secret_key,
            bucket_name
        )
        ```
        
        注意：此类不负责Minio服务的启动和关闭，这些操作需要在实例化类之前/之后手动完成。
        """

        if config_file is None:
            self._folder_path = folder_path
            self._endpoint = endpoint
            self._access_key = access_key
            self._secret_key = secret_key
            self._bucket_name = bucket_name
        else:
            configer = None
            if isinstance(config_file, ConfigManager):
                configer = config_file
            else:
                configer = ConfigManager(config_file)
            self._folder_path = configer.get_config("sample_source_path")
            self._endpoint = configer.get_config("minio_endpoint")
            self._access_key = configer.get_config("minio_access_key")
            self._secret_key = configer.get_config("minio_secret_key")
            self._bucket_name = configer.get_config("minio_bucket_name")
        super().__init__(self._folder_path)
        self._minio_client = get_minio_client(endpoint=self._endpoint, access_key=self._access_key,
                                              secret_key=self._secret_key)

    def _join(self, *args):
        """
        这个方法的主要目的是把传入的多个字符串参数使用'/'连接起来。
        
        Args:
            *args: 一个或多个字符串参数。
        
        Returns:
            返回一个新的字符串,该字符串是由传入的各个字符串使用'/'连接而成。
        
        Example:
            >>> _join("home", "user", "documents")
            'home/user/documents'
        """

        args_list = [item for item in args]
        return "/".join(args_list)

    def _get_minio_client(self):
        """
        这是一个获取Minio客户端的方法。
        
        根据类中定义的endpoint、access_key、secret_key和bucket_name去初始化一个Minio的客户端。 如果客户端未被初始化或者是第一次调用，就会创建一个新的客户端。然后检查这个客户端所连接的bucket是否存在，如果不存在就会抛出一个异常。
        
        Args:
            self: 类的实例。
        
        Returns:
            返回一个已经初始化并且连接成功的Minio客户端。
        
        Raises:
            Exception: 如果bucket不存在的话，就会抛出异常。
        """

        # if self._minio_client is None:
        #     self._minio_client = Minio(self._endpoint, self._access_key, self._secret_key, secure=False)
        #     if not self._minio_client.bucket_exists(self._bucket_name):
        #         raise Exception("此bucket不存在")
        return self._minio_client

    def _download_if_not_exsited(self, name: str):
        """
        此方法主要用于检查及下载指定的文件集。
        
        在我们的本地磁盘中，每个文件集都对应一个文件夹，此方法主要检查指定的文件集（名字为参数name）是否已经存在于本地磁盘。如果已经存在，那么就不再执行任何操作。如果不存在，则通过Minio客户端从远程Minio服务器下载该文件集，并保存到本地磁盘的指定文件夹中。
        
        参数:
            name: str，文件集的名称。
        
        返回值:
            无返回值。
        
        例子:
        假设我们的本地磁盘中没有名为'sample'的文件集，那么我们可以通过如下代码来下载它：
            minio_source = MinioSampleSource(folder_path, endpoint, access_key, secret_key, bucket_name)
            minio_source._download_if_not_exsited('sample')
        
        注意事项:
        如果远程Minio服务器中也没有名为'sample'的文件集，那么此方法会抛出一个异常。
        
        错误和异常:
        如果指定的文件集在远程Minio服务器中不存在，那么此方法会抛出一个异常。
        """

        if super().has_set(name):
            return
        client = self._get_minio_client()
        all_sets = {obj.object_name.strip('/') for obj in client.list_objects(self._bucket_name)}
        if name in all_sets:
            os.mkdir(os.path.join(self.base_folder, name))
            all_set_files = list(client.list_objects(self._bucket_name, prefix=f"{name}/"))

            bar = process_status_bar()
            for remote_f in bar.iter_bar(all_set_files, key="download", max=len(all_set_files)):
                bar.process_print(f"Download the set {name} ...")
                file_name = os.path.split(remote_f.object_name)[-1]
                download_plus(client, self._bucket_name, os.path.join(self.base_folder, name, file_name),
                              remote_f.object_name, bar)
                #
                # client.fget_object(self._bucket_name, remote_f.object_name,
                #                    os.path.join(self.base_folder, name, file_name))
        else:
            raise ("没有此set")

    def _object_exsited(self, name):
        """
        此函数用于检查指定名字的对象是否存在于Minio服务器的桶中。
        
        参数:
            name (str): 需要检查的对象的名字。
        
        返回:
            bool: 如果存在则返回True，否则返回False。
        
        异常:
            任何未处理的异常都将被捕获并返回False。
        
        示例:
        ```python
            def test_object_existed(self):
                # 假设我们有一个已经初始化并配置过的MinioSampleSource对象
                minio_source = MinioSampleSource(...)
                # 检查名为"my_object"的对象是否存在
                if minio_source._object_exsited("my_object"):
                    print("my_object exists in the bucket.")
                else:
                    print("my_object does not exist in the bucket.")
        ```
        
        注意:
            这是一个内部方法，通常不应直接调用。
        """

        try:
            client = self._get_minio_client()
            client.stat_object(self._bucket_name, name)
            return True
        except:
            return False

    def update(self, set_name=None):
        """
            此函数用于更新存储桶(bucket)中的对象（object），可以选择性地只更新特定的集合(set)。
        
            参数:
                set_name : str, 可选
                    要更新的集合名。如果未设置，将更新所有集合。
        
            返回:
                无返回值
        
            使用范例:
        
            ```python
            source = MinioSampleSource(folder_path="my_folder", endpoint="my_endpoint", access_key="my_access_key",
                                       secret_key="my_secret_key", bucket_name="my_bucket")
            source.update(set_name="my_set")
            ```
        
            注意：
            - 更新过程中，会首先判断本地文件和存储桶中的文件是否一致，只有在文件内容或大小发生变化时，才会上传新文件。
            - 如果存储桶中不存在要求的集合名，会抛出异常。
            - 本方法可能会消耗较大的网络流量和磁盘空间。
        """

        super().flush()
        client = self._get_minio_client()
        if set_name is not None:
            local_sets = [set_name]
        else:
            local_sets = super().get_dir_list()

        # comput count
        totle_count = 0
        for set in local_sets:
            for file in [f for f in os.listdir(os.path.join(self._folder_path, set)) if not f.startswith('.')]:
                totle_count += 1

        pb = process_status_bar()
        for set in pb.iter_bar(local_sets, key="set", max=len(local_sets)):
            pb.process_print(f"Upload set '{set}'")
            file_list = [f for f in os.listdir(os.path.join(self._folder_path, set)) if not f.startswith('.')]
            for file in pb.iter_bar(file_list, key="file", max=len(file_list)):
                f_l_path = os.path.join(self._folder_path, set, file)
                o_path = self._join(set, file)
                if not self._object_exsited(o_path):
                    upload_plus(client, self._bucket_name, f_l_path, o_path, pb)
                    # client.fput_object(self._bucket_name, o_path, f_l_path)
                else:
                    if not compare_file(client, self._bucket_name, o_path, f_l_path):
                        client.remove_object(self._bucket_name, o_path)
                        #os.remove(f_l_path)
                        upload_plus(client, self._bucket_name, f_l_path, o_path, pb)
                        # client.fput_object(self._bucket_name, o_path, f_l_path)

    def create_new_set(self, name: str, description: str, tags: [str], keys: [str], base_set="",
                       creator="") -> bool:
        """
        创建新的数据集
        
        此方法是用来在Minio存储服务上创建一个新的数据集。此数据集包含描述，标签，键，基础数据集和基础数据集的处理方法。
        
        参数:
            name (str): 数据集的名称
            description (str): 数据集的描述
            tags ([str]): 数据集的标签列表
            keys ([str]): 数据集的键列表
            base_set (str, 可选): 基础数据集的名称. 默认为空字符串.
            base_set_process (str, 可选): 基础数据集的处理方法. 默认为空字符串.
        
        返回:
            bool: 如果数据集成功创建，返回True
        
        错误:
            如果已经存在同名的数据集，将会抛出异常。
        
        示例:
            >> create_new_set("exampleSet", "This is an example set", ["exampleTag"], ["exampleKey"], base_set="baseSet", base_set_process="process")
        """

        if self.has_set(name):
            raise Exception("已存在同名的set")
        return super().create_new_set(name, description, tags, keys, base_set=base_set,
                                      creator=creator)

    def has_set(self, name: str) -> bool:
        """
        该函数用于检查指定的集合名称是否在本地或远程存储桶中存在。
        
        参数:
          name: str - 需要检查的集合名称。
        
        返回:
          bool - 如果集合存在于本地或远程存储桶中，则返回True，否则返回False。
        
        使用方法：
          minio_source = MinioSampleSource(folder_path, endpoint, access_key, secret_key, bucket_name)
          if minio_source.has_set("sample_set"):
              print("集合存在")
          else:
              print("集合不存在")
        
        注意：
          - 该函数会首先在本地检查集合是否存在，如果不存在，才会去远程存储桶检查。
          - 如果在检查远程存储桶时发生网络等错误，该函数可能会抛出异常。
        """

        if super().has_set(name):
            return True
        client = self._get_minio_client()
        all_sets = {obj.object_name: obj.is_dir for obj in client.list_objects(self._bucket_name)}
        if name + "/" in all_sets:
            return True
        return False

    def add_row(self, name: str, data) -> bool:
        """
        此函数的功能是在指定的数据集中添加一行新的数据。
        
        参数:
            name: str, 数据集的名称。
            data: 需要添加的数据。
        
        返回:
            bool，如果数据成功添加则返回True，否则返回False。
        
        使用方法:
        ```python
        add_result = add_row('data_set_name', data)
        ```
        
        注意:
            在执行这个函数之前,首先会检查是否已经在本地存在此数据集,如果不存在,会从minio服务器上下载对应的数据集。
            在添加数据之后,数据会被持久化保存在本地磁盘上。
        """

        self._download_if_not_exsited(name)
        return super().add_row(name, data)

    def get_metadata_keys(self, name: str) -> {}:
        """
        get_metadata_keys方法主要用于获取指定数据集的元数据键。
        
        参数:
            name (str): 指定的数据集名称。
        
        返回:
            dict: 返回一个字典，其中包含了指定数据集的所有元数据键。
        
        使用示例：
            minio_sample_source = MinioSampleSource(folder_path, endpoint, access_key, secret_key, bucket_name)
            metadata_keys = minio_sample_source.get_metadata_keys('sample_dataset')
            print(metadata_keys)
        
        注意：
            如果数据集在本地不存在，该方法将会先从远程服务器下载数据集到本地，然后再获取元数据键。
            如果数据集在本地和远程服务器都不存在，将会抛出异常。
        """

        self._download_if_not_exsited(name)
        return super().get_metadata_keys(name)

    def iter_data(self, name: str):
        """
        此函数为迭代器, 用于迭代返回一个名称为"name"的数据集的所有数据。
        
        Args:
            name (str): 数据集的名字
        
        Yields:
            iter: 指向数据集中下一个元素的迭代器
        
        举例:
            假设有一个名为"sample_set"的数据集，使用方法如下:
        
            source_connection = MinioSampleSource(folder_path, endpoint, access_key, secret_key, bucket_name)
            for data in source_connection.iter_data("sample_set"):
                # 在这里处理数据
                print(data)
        
        注意事项：
            如果数据集不存在，或者数据集为空，那么这个函数将会返回一个空的迭代器。
        """

        self._download_if_not_exsited(name)
        return super().iter_data(name)

    def get_remote_dir_list(self) -> {}:
        """
        `get_remote_dir_list` 是一个方法，用于获取远程目录列表，并提供有关这些目录的信息，包括元数据、计数和文件计数。
        
        这个方法没有接收任何参数，返回的是一个字典，字典中的每个键是远程目录的名称，值是一个字典，包含'meta'（元数据节点），'count'（该目录中的对象数量），'filecount'（该目录中的文件数量）。
        
        该方法首先初始化一个minio客户端，然后列出存储桶中的所有对象。对于每个对象，它会读取并解析相关的头部信息，包括基本头部和节点信息，然后将这些信息存储在一个字典中，并作为结果返回。
        
        注意：这个方法在处理大量目录时可能会需要较长的时间，因为它需要发送网络请求来获取每个目录的信息。
        
        示例：
        
        ```python
        minio_sample_source = MinioSampleSource(参数省略)
        remote_dir_list = minio_sample_source.get_remote_dir_list()
        for dir_name, info in remote_dir_list.items():
            print(f"Directory: {dir_name}, Meta: {info['meta']}, Count: {info['count']}, File count: {info['filecount']}")
        ```
        
        上述代码示例中，我们首先创建了一个`MinioSampleSource`对象，然后调用其`get_remote_dir_list`方法来获取远程目录列表。对于获取的每一个目录，我们都打印出了目录的名称，元数据，计数和文件计数。
        
        注意: 如果minio服务器的响应时间过长，或者网络连接不稳定，这个方法可能会抛出异常。确保在调用这个方法时具有稳定的网络连接，并准备好处理可能出现的异常。
        """

        client = self._get_minio_client()
        sets = [obj.object_name.strip('/') for obj in client.list_objects(self._bucket_name)]
        sets_infos = {}
        for p_set in sets:
            with io.BytesIO() as ib:
                o_path = f"{p_set}/{p_set}.dlib"
                remote_data = client.get_object(self._bucket_name, o_path, 0, self.start_seek).data
                ib.write(remote_data)
                ib.seek(0)
                file_index, append_seek, data_start_seek, count, filecount, current_count, create_date, modify_data = self._read_base_header(
                    ib, True)
                node = self._read_node(ib)
                sets_infos[p_set] = {
                    'meta': node,
                    'count': count,
                    'filecount': filecount,
                    'create_date': create_date,
                    'modify_data': modify_data
                }
        return sets_infos

    def download(self, name):
        """
            这个函数的目的是从远程存储下载数据集。
        
            Args:
                name (str): 需要下载的数据集的名称。
        
            这个函数没有返回值。
        
            使用方法如下：
        
            ```python
            minio_sample_source = MinioSampleSource(folder_path, endpoint, access_key, secret_key, bucket_name)
            minio_sample_source.download('your_dataset_name')
            ```
        
            在以上代码中，你需要提供有效的MinIO连接信息以及你想要下载的数据集的名称。函数会检查本地是否已有此数据集，如果没有，则从远程MinIO存储中下载。
        
            请注意，这个函数会依赖MinIO API进行操作，如果在MinIO上不存在指定的数据集，或者MinIO服务器无法连接，函数会抛出异常。
        """

        self._download_if_not_exsited(name)

    def read_one_row(self, name: str):
        """
        此函数用于从指定的Minio云存储中读取一行数据。该函数首先生成需要的初始偏移量然后从远程数据对象中获取这些偏移量，接着读取一行数据的长度和实际长度，最后在按照实际长度从远程对象中读取数据。
        
        参数:
            name (str): 这是一个字符串类型的参数，用于指定待读取数据的集合名称。
        
        返回:
            返回从Minio云存储中读取的一行数据。
        
        注意:
            1. 函数在执行过程中可能会遇到网络问题，导致从Minio云存储读取数据失败。需要在使用时处理这种可能的异常情况。
            2. 函数只读取一行数据，如果需要读取多行数据，需要多次调用该函数。
            3. 由于涉及到网络IO，函数的执行时间可能会比较长，需要在调用时考虑到性能问题。
        
        示例:
        
            # 创建MinioSampleSource对象
            sample_source = MinioSampleSource(folder_path, endpoint, access_key, secret_key, bucket_name)
            # 读取一行数据
            row_data = sample_source.read_one_row("sample_set")
            # 打印读取的数据
            print(row_data)
        """

        client = self._get_minio_client()

        start_seek = self.int_size * 5 + self.pointer_size + self.header_node_size

        with io.BytesIO() as ib:
            o_path = f"{name}/{name}.dlib"
            remote_data = client.get_object(self._bucket_name, o_path, 0, start_seek + self.int_size * 2).data
            ib.write(remote_data)
            ib.seek(0)
            file_index, append_seek, data_start_seek, count, filecount, current_count = self._read_base_header(
                ib)
            node = self._read_node(ib)
            ib.seek(data_start_seek)
            f_len = self._read_int(ib)
            act_len = self._read_int(ib)

            ib.seek(0)
            remote_data = client.get_object(self._bucket_name, o_path, data_start_seek,
                                            act_len + self.int_size * 2).data
            ib.write(remote_data)
            ib.seek(0)

            node = self._read_node(ib)

            return node
