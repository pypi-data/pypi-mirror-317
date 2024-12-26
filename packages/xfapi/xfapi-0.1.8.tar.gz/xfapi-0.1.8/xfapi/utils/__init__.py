from . import auth
from .log import LoggingTool
from .sql_utils import SQLUtils
from .load_yaml import YamlConfig
from .response import response
from . import decorator
import os

# 检查 log 文件夹是否存在，如果不存在则创建
if not os.path.exists('log'):
    os.makedirs('log')
logging_tool = LoggingTool("./log")
logger = logging_tool.setup_logger()