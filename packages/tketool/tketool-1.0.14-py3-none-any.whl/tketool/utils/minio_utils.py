from minio import Minio
import os
from tketool.JConfig import ConfigManager
from tketool.files import enum_files
from pathlib import Path
from tketool.utils.progressbar import process_status_bar
from tketool.logs import log
from threading import Thread


def get_minio_client(config: ConfigManager = None, endpoint=None, access_key=None, secret_key=None):
    if config is not None:
        t_endpoint = config.get_config("minio_endpoint")
        t_access_key = config.get_config("minio_access_key")
        t_secret_key = config.get_config("minio_secret_key")

    else:
        t_endpoint = endpoint
        t_access_key = access_key
        t_secret_key = secret_key

    return Minio(t_endpoint, t_access_key, t_secret_key, secure=False)


def _object_exsited(client, bucket_name, filepath):
    try:
        client.stat_object(bucket_name, filepath)
        return True
    except:
        return False


def compare_file(client, bucket_name, obj_name, local_path):
    # 获取远程文件元数据
    s3_object_info = client.stat_object(bucket_name, obj_name)
    remote_file_size = s3_object_info.size

    # 获取本地文件大小
    local_file_size = os.path.getsize(local_path)

    if remote_file_size != local_file_size:
        return False

    # 如果文件大小相同，继续比较前1KB的数据
    data = client.get_object(bucket_name, obj_name)
    remote_data_head = data.read(1024)

    with open(local_path, 'rb') as file:
        local_data_head = file.read(1024)

    return remote_data_head == local_data_head


class Minio_Progress(Thread):
    def __init__(self, process_bar: process_status_bar, max, key="upload"):
        super().__init__()
        if max == 0:
            max = 1
        self.process_bar = process_bar
        self.process_bar.start(key, max)
        self.last_size = 0

    def set_meta(self, total_length, object_name):
        pass

    def update(self, uploaded_size):
        self.last_size += uploaded_size
        self.process_bar.set_value(int(self.last_size / 1024 / 1024))

    def end(self):
        self.process_bar.stop_current()


def get_file_size_in_mb(file_path):
    size_in_bytes = os.path.getsize(file_path)
    size_in_mb = size_in_bytes / (1024 * 1024)
    return int(size_in_mb)


def upload_plus(client, bucket_name, local_file_path, remote_path, bar=None, ):
    if bar is None:
        client.fput_object(bucket_name, remote_path, local_file_path, )
    else:
        mp = Minio_Progress(bar, get_file_size_in_mb(local_file_path), "uploading")
        client.fput_object(bucket_name, remote_path, local_file_path, progress=mp)
        mp.end()


def download_plus(client, bucket_name, local_file_path, remote_path, bar=None, ):
    if bar is None:
        client.fget_object(bucket_name, remote_path, local_file_path)
        # client.fput_object(bucket_name, remote_path, local_file_path, )
    else:
        stats = client.stat_object(bucket_name, remote_path)
        size = int(stats.size / 1024 / 1024)

        mp = Minio_Progress(bar, size, "downloading")
        client.fget_object(bucket_name, remote_path, local_file_path, progress=mp)
        # client.fput_object(bucket_name, remote_path, local_file_path, progress=mp)
        mp.end()


def syc_upload_folder(local_path, bucket_name, folder_name, config: ConfigManager = None):
    client = get_minio_client(config)

    upload_files = set()

    pb = process_status_bar()

    files = [f for f in enum_files(local_path, recursive=True)]

    for path, file in pb.iter_bar(files, key="files"):
        relative_path = os.path.relpath(path, local_path)
        absolute_path = os.path.abspath(path)
        linux_path = Path(folder_name, relative_path)
        linux_path = linux_path.as_posix()

        pb.process_print(relative_path)

        upload_files.add(linux_path)

        if _object_exsited(client, bucket_name, linux_path):
            if not compare_file(client, bucket_name, linux_path, absolute_path):
                upload_plus(client, bucket_name, absolute_path, linux_path, bar=pb)
                pb.print_log(f"find the change, download the file {absolute_path}")
            else:
                pb.print_log(f"pass the file {absolute_path}")
        else:
            upload_plus(client, bucket_name, absolute_path, linux_path, bar=pb)
            # client.fput_object(bucket_name, linux_path, absolute_path, )

    objects = client.list_objects(bucket_name, prefix=f'{folder_name}/',
                                  recursive=True)

    for obj in objects:
        if obj.object_name in upload_files:
            pass
        else:
            client.remove_object(bucket_name, obj.object_name)
            log(f"remove the remote file :{obj.object_name}")


def syc_download_folder(local_path, bucket_name, folder_name, config: ConfigManager = None):
    client = get_minio_client(config)
    objects = client.list_objects(bucket_name, prefix=f'{folder_name}/',
                                  recursive=True)
    objects_list = [obj for obj in objects]
    pb = process_status_bar()

    for obj in pb.iter_bar(objects_list, key="files"):
        relative_name_start = obj.object_name.find("/") + 1
        relative_name = obj.object_name[relative_name_start:]
        lPath = os.path.join(local_path, relative_name)
        local_abs_path = os.path.abspath(lPath)

        pb.process_print(obj.object_name)

        if os.path.exists(local_abs_path):
            if not compare_file(client, bucket_name, obj.object_name, local_abs_path):
                download_plus(client, bucket_name, local_abs_path, obj.object_name, bar=pb)
                # client.fget_object(bucket_name, obj.object_name, local_abs_path)
                pb.print_log(f"redownload the file {obj.object_name}")
            else:
                pb.print_log(f"pass the file {obj.object_name}")
        else:
            download_plus(client, bucket_name, local_abs_path, obj.object_name, bar=pb)
            # client.fget_object(bucket_name, obj.object_name, local_abs_path)
        pass
        # if obj.object_name in upload_files:
        #     pass
        # else:
        #     client.remove_object(bucket_name, obj.object_name)
