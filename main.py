import logging
import os

from dotenv import load_dotenv

from src.server import MyLinuxServer
from src.utils import load_toml_file

CONFIG_PATH = "./config.toml"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    load_dotenv()
    config = load_toml_file(path=CONFIG_PATH)

    ip = os.getenv("SV_IP")
    port = int(os.getenv("SV_PORT"))
    username = os.getenv("SV_USERNAME")
    password = os.getenv("SV_PASSWORD")

    remote_path = config["data_path"]["remote_path"]
    local_path = config["data_path"]["local_path"]

    with MyLinuxServer(ip=ip, port=port, username=username, password=password, logger=logger) as server:
        server.download_file(remote_path=remote_path, local_path=local_path)
