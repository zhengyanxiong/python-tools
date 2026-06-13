"""Python Tools - 可复用工具库全局配置"""

import logging
import os

# 日志配置
LOG_LEVEL = os.getenv("PYTHON_TOOLS_LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger("python-tools")
