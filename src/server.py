import logging
import os
import time
from typing import Callable, Optional, Union

import paramiko
from paramiko import AuthenticationException, SFTPError, SSHException


class MyLinuxServer:
    def __init__(
        self,
        ip: str,
        port: int,
        username: str,
        password: str,
        ssh_timeout: int = 10,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.ssh_timeout = ssh_timeout
        self.logger = logger or logging.getLogger(__name__)

        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._connected = False

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self) -> None:
        if self._connected:
            return

        try:
            self._ssh.connect(
                hostname=self.ip,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=self.ssh_timeout,
                banner_timeout=30,
            )
            self._connected = True
            self.logger.info("SSH 连接成功建立")
        except AuthenticationException as e:
            self.logger.error("认证失败，请检查用户名密码")
            raise RuntimeError("SSH 认证失败") from e
        except (SSHException, OSError) as e:
            self.logger.error(f"连接失败: {str(e)}")
            raise RuntimeError(f"SSH 连接失败: {str(e)}") from e

    def disconnect(self) -> None:
        if self._connected:
            self._ssh.close()
            self._connected = False
            self.logger.info("SSH 连接已关闭")

    def _ensure_connection(self) -> None:
        if not (self._connected and self._ssh.get_transport().is_active()):
            self.logger.warning("SSH 连接已断开，正在尝试重连...")
            self.connect()

    @staticmethod
    def _default_progress_callback(transferred: int, total: int) -> None:
        print(f"\r传输进度: {transferred}/{total} bytes ({transferred/total:.1%})", end="")

    def download_file(
        self,
        remote_path: str,
        local_path: str,
        retries: int = 3,
        retry_delay: Union[int, float] = 5,
        callback: Optional[Callable[[int, int], None]] = None,
    ) -> None:
        # 参数验证
        if not os.path.basename(remote_path):
            raise ValueError("远程路径必须为文件路径")
        if not os.path.basename(local_path):
            raise ValueError("本地路径必须为文件路径")

        # 准备本地目录
        local_dir = os.path.dirname(local_path) or "."
        os.makedirs(local_dir, exist_ok=True)

        # 配置回调函数
        callback = callback or self._default_progress_callback
        last_error = None

        for attempt in range(retries + 1):
            try:
                self._ensure_connection()
                with self._ssh.open_sftp() as sftp:
                    sftp.get(remote_path, local_path, callback=callback)

                self.logger.info(f"文件下载成功: {remote_path} -> {local_path}")
                return  # 成功时退出

            except (SFTPError, SSHException, OSError) as e:
                last_error = e
                self.logger.warning(f"下载失败（尝试 {attempt+1}/{retries+1}）: {str(e)}")

                # 非最终尝试时进行延迟
                if attempt < retries:
                    self.logger.info(f"{retry_delay}秒后重试...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # 指数退避策略

            except Exception as e:
                last_error = e
                self.logger.error("发生未预期的错误", exc_info=True)
                break

        # 所有尝试失败后处理
        error_msg = f"无法下载文件，最终错误: {str(last_error)}\n" f"远程路径: {remote_path}\n本地路径: {local_path}"
        self.logger.error(error_msg)
        raise RuntimeError(error_msg)

    def execute_command(self, command: str) -> tuple:
        self._ensure_connection()
        stdin, stdout, stderr = self._ssh.exec_command(command)
        exit_code = stdout.channel.recv_exit_status()
        return stdout.read().decode(), stderr.read().decode(), exit_code
