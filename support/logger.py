# -*- coding: UTF-8 -*-
from loguru import logger as log


def configure_logger():
    # 配置 loguru
    log.add(
        "app.log",
        rotation="20 MB",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        enqueue=True  # 多进程安全
    )

