# pass_generate
import os, importlib.util
import pickle
import shutil
import paramiko
from paramiko import SFTPClient, SSHClient
from tketool.logs import log


def create_folder_if_not_exists(*args) -> str:
    """
    创建一个文件夹，如果该文件夹不存在。这个函数的目标是为了确保当程序需要在某个特定的路径下写入文件或者创建新的文件夹时，这个路径确实存在。这也可以避免在程序试图访问不存在的路径时发生错误。
    
    参数：
    *args：一个或多个字符串，表示要创建的文件夹的路径。例如，create_folder_if_not_exists('folder1', 'folder2') 将在当前目录下创建一个名为 'folder1/folder2' 的文件夹。
    
    返回值：
    str：返回创建的文件夹的完整路径。
    
    使用例子：
    ```python
    path = create_folder_if_not_exists('folder1', 'folder2')
    ```
    
    注意：
    该函数使用了os模块的os.path.join函数来连接路径。这是一个与平台无关的方式，可以在Linux、Windows等不同的操作系统上都能正常工作。同时，该函数也使用了os模块的os.makedirs函数来创建文件夹。其中的exist_ok参数设为True，表示如果路径已经存在，不会抛出错误，而是直接返回路径。
    
    此外，该函数假定程序有相应的文件操作权限。如果没有，os.makedirs可能会抛出PermissionError异常。
    """

    path = os.path.join(*args)
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return path


def write_file_line(path: str, lines: list, ignor_n_char=True) -> None:
    # version 1.1

    """
    这个函数的主要目的是将给定的行列表写入到指定的文件中。如果指定了ignor_n_char参数为True，那么在写入文件之前，会将行列表中的每一行中的"\n"字符进行移除。
    
    参数:
        path (str): 待写入的文件的路径。
        lines (list): 需要写入的行列表，每个元素代表一行。
        ignor_n_char (bool): 是否在写入文件之前移除每一行中的"\n"字符，默认为True。
    
    返回类型:
        无返回值
    
    使用示例:
        write_file_line("/tmp/test.txt", ["Hello\n", "World"], True)
    
    注意事项:
        在进行文件写入操作时，请确保拥有对应文件的写权限，否则可能会引发权限错误。
    
    错误或异常:
        如果给定的文件路径不存在，或者没有写权限，函数会抛出异常。
    """

    if ignor_n_char:
        newline = [str(x).replace("\n", "") for x in lines]
    else:
        newline = lines

    write_file(path, "\n".join(newline))


def read_file_lines(path: str, replace_n_char=False) -> list:
    # version 1.1

    """
    这是一个简单的函数，用于读取文本文件的内容。此函数根据用户的需求，可以选择是否删除行尾的换行符。
    
    参数:
    
        path (str): 指定要打开的文件的路径。
    
        replace_n_char (bool): 如果为True，则在返回的行尾会删除换行符。默认为False，即不删除换行符。
    
    返回:
    
        List[str]: 返回一个列表，其中包含文件中的所有行。如果文件打开失败，或者在读取文件过程中发生了其他错误，那么返回一个空列表。
    
    示例:
    
        lines = read_file_lines("example.txt", replace_n_char=True)
        # 从"example.txt"文件中读取所有行，并删除每一行的行尾换行符。
    
    错误和异常:
    
        如果在尝试打开或读取文件的过程中发生了错误，此函数会打印出错误原因，并返回一个空列表。
    """

    try:
        with open(path, 'r') as ff:
            if replace_n_char:
                return [line.replace("\n", "") for line in ff.readlines()]
            else:
                return [line for line in ff.readlines()]
    except Exception as e:
        print(f"Error reading from file {path}. Reason: {e}")
        return []


def write_file(path: str, content: str) -> None:
    """
    这个函数是用来将特定的内容写入到指定的文件中。
    
    Args:
        path(str): 需要写入内容的文件的路径。
        content(str): 需要写入的内容。
    
    Returns:
        None. 这个函数没有返回值，只是执行写入文件的操作。
    
    Raises:
        Exception: 如果写入文件过程中出现错误，会抛出异常。
    
    Example:
        ```python
        write_file('example.txt', '这是一段示例内容。')
        ```
        这个例子中，函数会将'这是一段示例内容。'这段话写入到'example.txt'这个文件中。
    
    Note:
        这个函数使用 'w' 模式打开文件，所以如果文件已经存在，它的原有内容会被新的内容覆盖。
    """

    try:
        with open(path, 'w') as ff:
            ff.write(content)
    except Exception as e:
        print(f"Error writing to file {path}. Reason: {e}")


def read_file(path: str) -> str:
    """
    此函数是用于读取指定路径的文件。
    
    参数:
        path (str): 文件的路径。
    
    返回:
        str: 返回读取的文件内容。如果读取过程中有任何错误，会返回一个空列表。
    
    示例:
        函数调用可以如下所示:
        read_file('path/to/your/file.txt')
    
    错误:
        如果文件路径不存在或者文件无法打开，函数会捕获异常并打印错误信息。
    """

    try:
        with open(path, 'r') as ff:
            return ff.read()
    except Exception as e:
        print(f"Error reading from file {path}. Reason: {e}")
        return []


def enum_directories(path, recursive=False):
    """
    enum_directories函数将遍历给定路径下的所有目录，并根据参数决定是否递归遍历子目录。
    
    参数:
        path (str): 需要遍历的目录路径。
        recursive (bool, 可选): 是否递归遍历子目录。默认为False，表示只遍历顶层目录。
    
    返回:
        generator: 一个生成器，每次yield一个元组，包含两个元素，第一个元素是完整的目录路径，第二个元素是目录的名字。
    
    使用方法:
        for dir_path, dir_name in enum_directories('/path/to/directory', recursive=True):
            print(f'Found directory: {dir_path} with name: {dir_name}')
    
    错误或者bug:
        如果输入的路径不存在或者不是一个目录，函数会抛出异常。
    """

    for root, dirs, files in os.walk(path):
        for dir_name in dirs:
            yield os.path.join(root, dir_name), dir_name

        # 如果不需要递归，则只需处理顶层目录
        if not recursive:
            break


def enum_files(path, recursive=False):
    """
    这是一个枚举目录中文件的函数。
    
    参数:
        path (str): 需要枚举的目录路径。
        recursive (bool): 是否需要递归枚举子目录中的文件，如果设为False，则只枚举顶层目录中的文件。
    
    返回:
        generator: 这是一个生成器函数，每次调用都会返回下一个文件的完整路径和文件名。
    
    例子:
    
        # 枚举当前目录下的所有文件
        for full_path, file_name in enum_files('.'):
            print(full_path, file_name)
    
        # 枚举当前目录及其子目录下的所有文件
        for full_path, file_name in enum_files('.', True):
            print(full_path, file_name)
    
    注意:
        该函数依赖于os模块，使用前请确保已经正确导入os模块：import os。
    """

    for root, dirs, files in os.walk(path):
        for file_name in files:
            yield os.path.join(root, file_name), file_name

        # 如果不需要递归，则只需处理顶层目录
        if not recursive:
            break


def delete_files_in_directory(directory):
    """
    删除给定目录下的所有文件和子目录。
    
    这个函数会遍历给定目录，对于目录下的每一个文件或目录，如果是文件或者链接，直接删除；如果是目录，递归删除该目录及其包含的所有文件和子目录。
    
    参数：
        directory (str): 需要删除文件的目录路径
    
    返回：
        None
    
    错误：
        如果删除文件或目录过程中出现错误，会打印错误信息，但不会中断程序。
    
    使用示例：
        delete_files_in_directory('/path/to/directory')
    
    注意：
        调用这个函数需要谨慎，因为它会删除指定目录下的所有文件和子目录，且不可恢复。
    """

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def get_file_path_in_sftpserver(folder_path, filename, endpoint, access_user, secret_pwd, remote_folder_path, port=22):
    """
    这是一个Python函数，用于在SFTP服务器中获取文件的路径。如果在本地路径中找不到文件，那么函数将会尝试连接SFTP服务器并从中下载文件。
    
    参数：
        folder_path (str): 本地文件夹路径，用于和文件名拼接成文件的完整本地路径。
        filename (str): 需要获取路径的文件的文件名。
        endpoint (str): SFTP服务器的IP地址或者主机名。
        access_user (str): 登陆SFTP服务器的用户名。
        secret_pwd (str): 登陆SFTP服务器的密码。
        remote_folder_path (str): 远程SFTP服务器文件夹路径，用于和文件名拼接成文件的完整远程路径。
        port (int, optional): SFTP服务器的端口，默认为22。
    
    返回：
        str: 文件的本地路径。
    
    示例：
    
    ```python
        local_path = get_file_path_in_sftpserver('/local/folder', 'test.txt', 'sftp.server.com', 'user', 'password', '/remote/folder')
        print(local_path) # 输出: '/local/folder/test.txt'
    ```
    
    注意：
    
        - 如果本地文件不存在，且尝试从SFTP服务器下载时发生错误，那么函数会抛出异常。
        - 函数使用了`paramiko`库建立SSH连接和SFTP客户端，确保在使用前已安装此库。
        - 函数使用了自定义的`log`函数记录日志，请在同一个作用域内定义此函数，否则将会抛出`NameError`异常。
    
    """

    local_path = os.path.join(folder_path, filename)
    if os.path.exists(local_path):
        return local_path

    log(f"start download the file '{filename}'")

    _sshclient = SSHClient()
    _sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    _sshclient.connect(endpoint, port, access_user, secret_pwd)
    _sftpclient = SFTPClient.from_transport(_sshclient.get_transport())

    remote_path = f"{remote_folder_path}/{filename}"
    _sftpclient.get(remote_path, local_path)

    log(f"download the file '{filename}' completed.")

    _sshclient.close()
    return local_path


def pickle_file(path, obj):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)


def load_pickle_file(path):
    with open(path, 'rb') as f:
        return pickle.load(path)
