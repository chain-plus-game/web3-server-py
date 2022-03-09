import os
from logging.config import dictConfig
from config import log_config
from loguru import logger
from fastapi import FastAPI, WebSocket


dictConfig(log_config)
# 日志设置
dir_log = "/home/log"
path_log = os.path.join(dir_log, 'server.log')
# 路径，每日分割时间，是否异步记录，日志是否序列化，编码格式，最长保存日志时间
logger.add(path_log, rotation='0:00', enqueue=True, serialize=False, encoding="utf-8", retention="10 days")
logger.info("======= server start ======")

app = FastAPI()



import route