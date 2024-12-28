
import os
import hashlib
import requests
from tqdm import tqdm

class ECSM_REPO:
    """
    ECSM 镜像管理 - 镜像仓库
    """

    def __init__(self, srv_ip, srv_port):
        self.srv_ip = srv_ip
        self.srv_port = srv_port

    def __upload_chunk(self, file, splits, index, data_size):
        offset = (index - 1) *data_size

        with open(file["path"], "rb") as f:
            f.seek(offset)
            data = f.read(data_size)

        # 请求参数
        # description   string  否  文件描述信息
        # total         int     是  镜像文件分片个数
        # index         int     是  当前上传片段索引，从 1 开始
        # imageHash     string  是  完整的镜像文件 hash。注意：非当前镜像片段 hash
        # totalSize     int     是  完整镜像文件总大小，单位为 Byte
        # bufferSize    int     是  当前镜像片段大小，单位为 Byte
        # offset        int     是  切片大小，单位为 Byte

        headers = {
            "description": file["desc"],
            "imageHash": file["hash"],
            "totalSize": str(file["size"]),
            "total": str(splits),
            "index": str(index),
            "bufferSize": str(len(data)),
            "offset": str(data_size),
            "Content-Type": "application/octet-stream",
        }

        # 发送 POST 请求上传文件片段
        url = f"http://{self.srv_ip}:{self.srv_port}" + "/api/v1/image"

        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            self.progress.update(len(data))
            msg = f"Uploaded chunk {index} successfully."
        else:
            msg = f"Error: Failed to upload chunk {index}. Status code: {response.status_code}"

        # resp_body = response.json()
        # resp_upoadid = resp_body.get("data", {}).get("uploadId")

        return (0 if response.status_code == 200 else -1, msg)

    def upload_image(self, file_path, file_desc):
        """
        ECSM 镜像管理 - 镜像仓库 - 上传镜像
        """

        if not os.path.exists(file_path):
            return (-1, f"文件 {file_path} 不存在")

        file_info = os.stat(file_path)
        file_size = file_info.st_size

        # 计算文件的哈希值
        file_hash_md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                file_hash_md5.update(chunk)

        target_file = {
            "desc": file_desc,
            "path": file_path,
            "size": file_size,
            "hash": file_hash_md5.hexdigest()
        }

        taget_splits_size = 1 * 1024 * 1024
        target_splits = file_size // taget_splits_size + 1 if file_size % taget_splits_size else 0

        upload_id = ""
        self.progress = tqdm(total=file_size, unit="B", unit_scale=True, desc="上传进度")
        for index in range(0, target_splits):
            code, msg = self.__upload_chunk(target_file, target_splits, index + 1, taget_splits_size)
            if code < 0:
                self.progress.close()
                return (-1, msg)

        self.progress.close()
        return (0, "上传成功")

    def search_file_upload_prog(self, uploadId):
        """
        ECSM 镜像管理 - 镜像仓库 - 查询镜像上传进度
        """

        url = f"http://{self.srv_ip}:{self.srv_port}" + "/api/v1/image/upload/" + uploadId

        # 发送 POST 请求上传文件片段
        response = requests.get(url)
        if response.status_code == 200:
            return (0, response.content)

        return (-1, "")

    def __list_page(self, isLocal, page_num, page_size) -> tuple[int, list]:

        repo_type = "local" if isLocal > 0 else "remote"

        url = f"http://{self.srv_ip}:{self.srv_port}" + "/api/v1/image?"
        url += f"registryId={repo_type}&pageNum={page_num}&pageSize={page_size}"

        print(url)

        response = requests.get(url)
        if response.status_code == 200:
            resp_body = response.json()

            repo_list = []

            for item in resp_body['data']['list']:
                item_dict = {
                    "name": item['name'],
                    "arch": item['arch'],
                    "os":   item['os'],
                    "desc": item['description'],
                    "tag":  item['tag'],
                    "id":   item['id']
                }
                repo_list.append(item_dict)

            return 0, repo_list

        return -1, []

    def list(self) -> tuple[int, list]:
        local = 1
        page_num = 1
        page_size = 100

        code, list = self.__list_page(local, page_num, page_size)
        if code == 0:
            return code, list

        return -1, []

    def summary(self) -> tuple[int, dict]:

        url = f"http://{self.srv_ip}:{self.srv_port}" + "/api/v1/image/summary"

        response = requests.get(url)
        if response.status_code != 200:
            return (-1, {})

        resp_body = response.json()
        resp_con = {
            "local": resp_body.get("data", {}).get("local"),
            "remote": resp_body.get("data", {}).get("remote")
        }

        return 0, resp_con
