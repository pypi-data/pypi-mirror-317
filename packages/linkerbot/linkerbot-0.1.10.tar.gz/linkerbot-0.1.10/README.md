# LinkerBot Python SDK
灵巧手服务端相关的SDK

## 安装

```bash
pip install linkerbot
```

## 使用

```python
from linkerbot_sdk import LinkerBot
bot = LinkerBot()
# 下载数据集
print("开始下载数据集...")
result = bot.download_dataset(dataset="graspnet/objects",cache_dir="../test")
print(f"下载完成，文件保存在: {result}")
```

## 功能

- 数据集下载

## 协议

This project is licensed under the MIT License.
