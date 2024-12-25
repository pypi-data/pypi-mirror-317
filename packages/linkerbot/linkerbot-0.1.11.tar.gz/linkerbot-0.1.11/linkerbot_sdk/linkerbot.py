import os
import requests
from urllib.parse import urljoin
from tqdm import tqdm


class LinkerBot:
    """A simple SDK class with two utility methods."""

    def __init__(self, token=None, base_url = None):
        self.token = token
        self.default_cache_dir = os.path.join(os.path.expanduser("~"), "linkerbot-sdk-dir")
        self.default_dataset_dir = self.default_cache_dir + "/datasets"
        self.base_url = base_url or "https://api.linkerbot.cn"
    
    def download_dataset(self, dataset, cache_dir=None):
        """Download the dataset.
        
        Args:
            dataset_id: The ID of the dataset to download
            cache_dir: The directory to save files to. Defaults to /Users/a1/linkerbot-sdk/test
        """
        if not dataset:
            raise ValueError("dataset cannot be empty")

        organization = dataset.split('/')[0]
        # 使用默认缓存目录如果没有指定
        cache_dir = cache_dir or self.default_dataset_dir

        response = requests.post(urljoin(self.base_url, "/common/get-download-keys"), json={"key": dataset, "token": self.token})
        response.raise_for_status()  # 确保请求成功
        keys = response.json().get("keys", [])
        baseUrl = response.json().get("baseUrl", "")
        children = response.json().get("children", [])
        # 确保基础缓存目录存在
        os.makedirs(cache_dir, exist_ok=True)

        for key in keys:
            # 构建完整的本地路径
            local_key = key['key'].split(f"/{organization}/")[-1]
            local_path = os.path.join(cache_dir, local_key.lstrip('/'))

            if key['key'].endswith('/'):
                # 如果是目录路径，创建目录
                os.makedirs(local_path, exist_ok=True)
                print(f"创建目录: {local_path}")
            else:
                # 如果是文件，下载文件
                # 确保文件的目录存在
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                # 构建完整的URL
                url = urljoin(baseUrl, key['key'])
                # 下载文件
                print(f"Downloading: {os.path.basename(local_path)}")
                response = requests.get(url, stream=True)
                response.raise_for_status()  # 确保请求成功
                # 获取文件大小
                total_size = key['size']
                downloaded_size = 0
                
                # 创建进度条
                progress_bar = tqdm(
                    total=total_size,
                    unit='iB',
                    unit_scale=True,
                    desc=os.path.basename(local_path)
                )
                
                # 写入文件，同时更新进度条
                with open(local_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        size = f.write(chunk)
                        downloaded_size += size
                        progress_bar.update(size)
                
                progress_bar.close()

        for child in children:
            # 递归下载子目录
            self.download_dataset(child, cache_dir=cache_dir)

        print(f"最终下载的目录: {cache_dir}")
        return cache_dir
