# -*- coding: utf-8 -*-
import logging
import os
import tomllib
from logging.handlers import TimedRotatingFileHandler


def load_toml_file(path: str):
    with open(path, "rb") as f:
        return tomllib.load(f)


def setup_logger(
    name: str,
    log_dir: str,
    log_level: str = "INFO",
    log_format: str = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    date_format: str = "%Y-%m-%d %H:%M:%S",
    backup_count: int = 7,
) -> logging.Logger:
    # 确保日志目录存在
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 日志文件命名（根据logger name来区分文件，或统一名称）
    log_file = os.path.join(log_dir, f"{name}.log")

    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # 防止重复添加handler（如果已存在同名logger，就不要重复添加）
    if not logger.handlers:
        # 创建文件handler（按天切分）
        file_handler = TimedRotatingFileHandler(
            filename=log_file,
            when="D",  # 每天轮转，可改为 "H"、"M"、"S"、"midnight" 等
            interval=1,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setLevel(log_level)
        file_formatter = logging.Formatter(log_format, datefmt=date_format)
        file_handler.setFormatter(file_formatter)

        # 创建控制台handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter(log_format, datefmt=date_format)
        console_handler.setFormatter(console_formatter)

        # 将handler添加到logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


def get_logger(
    name: str,
    log_dir: str,
    log_level: str = "INFO",
    log_format: str = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    date_format: str = "%Y-%m-%d %H:%M:%S",
    backup_count: int = 7,
) -> logging.Logger:
    """
    获取已初始化好的日志记录器。如果未初始化，则使用默认配置初始化。
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        # 如果没有handler，说明未初始化，则使用默认配置初始化
        setup_logger(
            name=name,
            log_dir=log_dir,
            log_level=log_level,
            log_format=log_format,
            date_format=date_format,
            backup_count=backup_count,
        )
    return logger
