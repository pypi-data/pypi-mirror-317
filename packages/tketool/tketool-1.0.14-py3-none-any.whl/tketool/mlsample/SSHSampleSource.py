import io
import paramiko
from paramiko import SFTPClient, SSHClient
from tketool.mlsample.LocalSampleSource import LocalDisk_NLSampleSource
from tketool.JConfig import get_config_instance
from tketool.files import create_folder_if_not_exists
from tketool.utils.progressbar import process_status_bar
from tketool.logs import log
import os


class SSHSampleSource(LocalDisk_NLSampleSource):
    """
    SSHSampleSource类是一个用于处理SSH源文件的类，继承自LocalDisk_NLSampleSource类。这个类实现了各种对SSH源文件的操作，包括下载、更新、创建新的数据集、检查数据集是否存在、添加行、获取元数据键、迭代数据、获取远程目录列表等等。
    
    注意：此类需要先安装paramiko库才能使用。
    
    类的初始化函数参数介绍：
    - folder_path: 本地文件夹路径
    - endpoint: SSH服务器的IP地址或者主机名
    - access_user: SSH登录的用户名
    - secret_pwd: SSH登录的密码
    - target_path: SSH服务器上的目标文件夹路径
    - port: SSH服务器的端口，默认为22
    
    使用示例:
    ```python
    ssh_source = SSHSampleSource('/local/path', 'ssh.server.com', 'user', 'password', '/remote/path')
    ssh_source.download('dataset_name')
    ```
    
    此类可能存在的问题:
    - 对于大文件的同步可能会有性能问题
    - 当SSH服务器连接问题时，可能会出现异常
    - 使用的SSH连接库paramiko没有对并发做优化，可能会有并发问题
    """

    @staticmethod
    def instance_default():
        """
        这是一个staticmethod，命名为instance_default的类方法。这个方法主要用于获取配置信息，并依据这些配置信息创建一个SSHSampleSource实例。
        
        这个方法的工作流程是：
        1. 通过调用get_config_instance().get_config("ssh_samplesource_xxx")函数，获取必要的SSH连接参数，包括folder_path, endpoint, access_user, access_pwd和access_target_path等。
        2. 使用上述获取的参数创建并返回一个SSHSampleSource实例。
        
        返回类型：
        该方法返回一个SSHSampleSource类的实例。
        
        使用示例：
        sample_source = SSHSampleSource.instance_default()
        
        注意事项：
        在使用这个方法的过程中需要注意，所有的配置信息都需要在应用的配置文件中进行预设，并且这个方法在读取配置信息的时候不会进行任何的错误处理，所以如果配置信息不存在或者格式错误，都会导致程序运行错误。
        """

        folder_path = get_config_instance().get_config("ssh_samplesource_folderpath")
        endpoint = get_config_instance().get_config("ssh_samplesource_endpoint")
        access_user = get_config_instance().get_config("ssh_samplesource_user")
        access_pwd = get_config_instance().get_config("ssh_samplesource_pwd")
        access_target_path = get_config_instance().get_config("ssh_samplesource_target_apth")

        return SSHSampleSource(folder_path, endpoint, access_user, access_pwd, access_target_path)

    def __init__(self, folder_path, endpoint, access_user, secret_pwd, target_path, port=22):
        """"""

        super().__init__(folder_path)
        self._folder_path = folder_path
        self._endpoint = endpoint
        self._access_key = access_user
        self._secret_key = secret_pwd
        self._target_path = target_path
        self._porter = port

        self._sshclient = SSHClient()
        self._sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self._sshclient.connect(self._endpoint, self._porter, self._access_key, self._secret_key)
        self._sftpclient = SFTPClient.from_transport(self._sshclient.get_transport())

    def _download_if_not_exsited(self, name: str):
        """
        该函数主要用于判断指定的文件集是否已经存在，如果不存在，则从远程服务器上下载。
        
        参数:
            name (str): 文件集的名称。
        
        返回:
            无返回值，但如果在远程服务器上未找到指定的文件集，将会抛出异常。
        """

        if super().has_set(name):
            return
        all_sets = self._sftpclient.listdir(self._target_path)
        if name in all_sets:
            create_folder_if_not_exists(os.path.join(self.base_folder, name))

            all_set_files = self._sftpclient.listdir(os.path.join(self._target_path, name))

            bar = process_status_bar()
            for remote_f in bar.iter_bar(all_set_files, key="download", max=len(all_set_files)):
                bar.process_print(f"Download the set {name} ...")

                remote_path = os.path.join(self._target_path, name, remote_f)
                local_path = os.path.join(self.base_folder, name, remote_f)
                self._sftpclient.get(remote_path, local_path)
        else:
            raise Exception("没有此set")

    def _object_exsited(self, name_or_path):
        """
        函数名称: _object_exsited
        
        这个方法用于检查远程路径下的文件或目录是否存在。
        
        参数:
            name_or_path (str): 需要检查的远程文件或目录的路径。
        
        返回类型:
            tuple: 返回一个元组，第一个元素是一个布尔值，如果文件或目录存在则返回True，否则返回False；
                   第二个元素是一个整数，如果文件存在则返回文件的大小（单位：字节），如果文件不存在或检查过程中发生错误，则返回-1。
        
        注意:
            1. 这个函数只能在类的内部使用，不能从类的外部直接调用。
            2. 如果在检查过程中发生异常，该函数会捕获异常并返回(False, -1)。
            3. 这个函数依赖于sftpclient的stat方法来获取远程文件或目录的状态。
        """

        try:
            info = self._sftpclient.stat(name_or_path)
            return True, info.st_size
        except BaseException:
            return False, -1

    def update(self, set_name=None):
        """
            这个函数的目的是更新SSH样本源。如果给出了set_name，则只更新此set的样本; 如果没有给出，那么更新所有样本。
        
            函数首先清理旧的样本, 然后检查要更新的样本列表。对每个样本，函数首先检查远端是否存在此样本，如果不存在则创建。
        
            接着，函数读取本地的样本文件并检查远端是否存在此文件。如果远端不存在此文件，那么文件将被上传; 否则，函数将检查本地和远端文件的前160个字节和文件大小是否相同。如果不同，则上传本地文件。
        
            这个函数不返回任何值。
        
            参数:
            set_name: str, 可选的。要更新的样本名。如果不给出，则更新所有样本。
        
            示例:
        
            ```python
            ssh_sample_source = SSHSampleSource(folder_path, endpoint, access_user, secret_pwd, target_path)
            ssh_sample_source.update('sample1')
            ```
        
            注意: 这个函数在处理大文件的时候可能会有性能问题，因为它总是检查文件的前160个字节。如果文件很大，这可能会消耗大量的时间。更好的方法是只检查文件大小，如果文件大小与远端相同，那么可以认为文件没有改变。
        """

        super().flush()
        if set_name is not None:
            local_sets = [set_name]
        else:
            local_sets = super().get_dir_list()

        all_remote_list = self._sftpclient.listdir(self._target_path)

        # comput count
        totle_count = 0
        for set in local_sets:
            for file in [f for f in os.listdir(os.path.join(self._folder_path, set)) if not f.startswith('.')]:
                totle_count += 1

        pb = process_status_bar()
        for set in pb.iter_bar(local_sets, key="set", max=len(local_sets)):
            pb.process_print(f"Upload set '{set}'")

            set_dir = self._target_path + "/" + set

            if set not in all_remote_list:
                self._sftpclient.mkdir(set_dir)

            file_list = [f for f in os.listdir(os.path.join(self._folder_path, set)) if not f.startswith('.')]
            for file in pb.iter_bar(file_list, key="file", max=len(file_list)):
                f_l_path = os.path.join(self._folder_path, set, file)
                o_path = os.path.join(set_dir, file)

                exsited_state, remote_size = self._object_exsited(o_path)

                if not exsited_state:
                    self._sftpclient.put(f_l_path, o_path)
                    # client.fput_object(self._bucket_name, o_path, f_l_path)
                else:
                    with self._sftpclient.open(o_path, 'rb') as f_obj:
                        remote_data = f_obj.read(160)

                    with open(f_l_path, 'rb') as f_obj:
                        fobj_data = f_obj.read(160)
                    local_size = os.path.getsize(f_l_path)
                    if (remote_data != fobj_data) or (remote_size != local_size):
                        self._sftpclient.put(f_l_path, o_path)

    def create_new_set(self, name: str, description: str, tags: [str], keys: [str], base_set="",
                       base_set_process="") -> bool:
        """
        创建一个新的样本集。
        
        使用此方法可以在SSH样本源中创建一个新的样本集。如果存在同名的样本集，则会抛出异常。
        
        参数:
            name (str): 新样本集的名字。
            description (str): 对新样本集的描述信息。
            tags ([str]): 新样本集的标签列表。
            keys ([str]): 新样本集的关键字列表。
            base_set (str, 可选): 可以指定一个基础样本集，新样本集会在此基础上创建。默认为空字符串，表示不使用基础样本集。
            base_set_process (str, 可选): 对基础样本集的处理方式。默认为空字符串，表示不对基础样本集进行任何处理。
        
        返回:
            bool: 如果样本集成功创建，返回True。
        
        抛出:
            Exception: 如果已存在同名的样本集，将抛出异常。
        
        示例:
            ```python
            sample_source = SSHSampleSource(...)
            sample_source.create_new_set("new_set", "This is a new set.", ["tag1", "tag2"], ["key1", "key2"])
            ```
        
        注意:
            在创建新样本集之前，应确保没有同名的样本集存在。可以使用has_set(name)方法进行检查。
        """

        if self.has_set(name):
            raise Exception("已存在同名的set")
        return super().create_new_set(name, description, tags, keys, base_set=base_set,
                                      base_set_process=base_set_process)

    def has_set(self, name: str) -> bool:
        """
            def has_set(self, name: str) -> bool:
        
            这是一个检查某个名称的数据集是否存在的方法。
        
            参数:
                name (str): 要检查的数据集的名称。
        
            返回:
                bool: 如果指定名称的数据集存在则返回True，否则返回False。
        
            例子:
                has_set("example_set")
                >>> True
        """

        if super().has_set(name):
            return True
        all_sets = self._sftpclient.listdir(self._target_path)
        if name in all_sets:
            return True
        return False

    def add_row(self, name: str, data) -> bool:
        """
        这个方法被用来向指定名称的数据集中添加一行数据。
        
        参数:
            name: str, 数据集的名称。
            data: 需要添加的数据。
        
        返回:
            bool, 如果添加数据成功，返回True，否则返回False。
        
        注意:
            如果数据集不存在，将会抛出异常。
        """

        self._download_if_not_exsited(name)
        return super().add_row(name, data)

    def get_metadata_keys(self, name: str) -> {}:
        """
        此方法用于获取样本集的元数据键。
        
        参数:
            name : str
                样本集的名称。
        
        返回:
            dict
                返回样本集的元数据键。如果样本集不存在，则会先下载。
        
        示例:
            get_metadata_keys('sample_set')
        
        注意:
            在调用此方法之前，请确保样本集已存在，否则会引发异常。
        """

        self._download_if_not_exsited(name)
        return super().get_metadata_keys(name)

    def iter_data(self, name: str):
        """
        该方法用于遍历指定名称的数据集。如果该数据集在本地不存在，它会先从远程SSH服务器下载。
        
        参数:
            name (str): 要遍历的数据集的名称。
        
        使用方法:
            ```
            sshSampleSource = SSHSampleSource(folder_path, endpoint, access_user, secret_pwd, target_path, port)
            for data in sshSampleSource.iter_data("dataset_name"):
                process(data)
            ```
        
        返回:
            这是一个生成器方法，每次迭代返回数据集中的一条数据。
        
        注意:
            如果远程SSH服务器上不存在指定名称的数据集，会抛出异常。
        """

        self._download_if_not_exsited(name)
        return super().iter_data(name)

    def get_remote_dir_list(self) -> {}:
        """
            获取远程目录列表。
        
            此方法用于获取在SSH服务器上的远程目录列表，包括每个目录的元数据信息，总条目数量和子文件数量。
        
            返回:
                返回一个字典，键是目录名称，值是一个包含元数据，总条目数量和子文件数量的字典。
        
            示例:
            ```
            ssh_instance = SSHSampleSource(folder_path, endpoint, access_user, secret_pwd, target_path)
            remote_dir_list = ssh_instance.get_remote_dir_list()
            print(remote_dir_list)
            ```
        
            异常:
                如果在读取远程文件过程中出现问题，可能会抛出异常。
        
            注意:
                由于使用的是SFTP协议，所以需要保证目标服务器的SFTP服务是开启状态，并且相关的目录和文件有读取权限。
        """

        sets = self._sftpclient.listdir(self._target_path)
        sets_infos = {}
        # start_seek = self.int_size * 5 + self.pointer_size + self.header_node_size
        for p_set in sets:
            with io.BytesIO() as ib:
                o_path = f"{self._target_path}/{p_set}/{p_set}.dlib"
                try:
                    with self._sftpclient.open(o_path, 'rb') as f_obj:
                        remote_data = f_obj.read(self.start_seek)
                except  Exception as ex:
                    log(f"open {o_path} failed.")
                # remote_data = client.get_object(self._bucket_name, o_path, 0, start_seek).data
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
        该方法用于从远程服务器下载指定的数据集。
        
        参数:
            name: str类型，需要下载的数据集的名称。
        
        返回值:
            无返回值。
        
        使用方式:
            该方法用于从SSH服务器下载数据。如果在本地检测到数据集已存在，则跳过下载过程。如果数据集在本地不存在，会从SSH服务器下载到本地。
        
        异常处理:
            如果给定的数据集名称在服务器上不存在，或者遇到网络问题导致下载失败，会抛出异常。
        
        示例：
            ssh_source = SSHSampleSource(folder_path, endpoint, user, password, target_path)
            ssh_source.download("dataset_name")
        """

        self._download_if_not_exsited(name)
