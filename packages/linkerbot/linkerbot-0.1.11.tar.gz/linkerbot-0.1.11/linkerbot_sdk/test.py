from linkerbot_sdk.linkerbot import LinkerBot  # 改为绝对导入

def main():
    # 创建SDK实例
    bot = LinkerBot()
    # 下载数据集
    print("开始下载数据集...")
    result = bot.download_dataset(dataset="linkerbot/物品数据集",cache_dir="../../test")
    print(f"下载完成，文件保存在: {result}")

if __name__ == "__main__":
    main()
