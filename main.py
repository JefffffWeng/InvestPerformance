# -*- coding: utf-8 -*-
import os

from dotenv import load_dotenv

from src.server import MyLinuxServer
from src.utils import get_logger, load_toml_file

CONFIG_PATH = "./config.toml"

# 加载配置文件和临时环境变量
load_dotenv(encoding="utf-8")
config = load_toml_file(path=CONFIG_PATH)

# 配置logs
log_dir = config["log"]["log_dir"]
logger = get_logger(__name__, log_dir=log_dir)

if __name__ == "__main__":
    # 从环境变量中读取服务器配置
    ip = os.getenv("SERVER_IP")
    port = int(os.getenv("SERVER_PORT"))
    username = os.getenv("SERVER_USERNAME")
    password = os.getenv("SERVER_PASSWORD")

    # 远端地址及本地地址（若不存在则创建）
    remote_path = config["data_path"]["remote_path"]
    local_path = config["data_path"]["local_path"]

    # 使用上下文管理下载远端数据
    with MyLinuxServer(ip=ip, port=port, username=username, password=password, logger=logger) as server:
        server.download_file(remote_path=remote_path, local_path=local_path)
