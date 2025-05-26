# -*- coding: UTF-8 -*-

import os
import signal

from loguru import logger

from flask_app import start_flask_app
from support.logger import configure_logger


# 定义处理停止服务的函数
def shutdown_server(sig, frame):
    logger.info("Flask App shutting down")
    os.kill(os.getpid(), signal.SIGINT)


if __name__ == '__main__':
    # 系统日志
    configure_logger()

    # 注册信号处理
    signal.signal(signal.SIGTERM, shutdown_server)
    signal.signal(signal.SIGINT, shutdown_server)

    start_flask_app()
