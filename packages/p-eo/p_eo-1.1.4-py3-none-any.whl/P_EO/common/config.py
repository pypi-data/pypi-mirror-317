import logging
import os
from pathlib import Path


class Default:
    IMPLICITLY_WAIT = 5
    TIMEOUT = 5
    INTERVAL = 0.25
    ACTION_WAIT = 0.25
    REFRESH_WAIT = 2
    TEMP_PATH = os.environ.get('P_EO_PATH', os.getcwd())  # 定义P_EO缓存目录
    SCREENSHOTS = False
    SCREENSHOTS_PATH = Path(TEMP_PATH, 'screenshots')
    ERROR_PATH = Path(SCREENSHOTS_PATH, 'error_img')
    WEB_PAGE_PATH = Path(SCREENSHOTS_PATH, 'web_page')


class LogConfig:
    # STREAM输出相关配置
    STREAM = False
    STREAM_LEVEL = logging.INFO
    STREAM_FORMAT = ''

    # Log文件相关配置
    LOG_FILE = ''
    LOG_FILE_LEVEL = logging.INFO
    LOG_FILE_FORMAT = ''

    SAVE_ERROR = False
