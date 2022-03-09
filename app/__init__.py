from fastapi import FastAPI, WebSocket
from loguru import logger
from app.ws_client import ws_client
import uuid
import os
from logging.config import dictConfig
from app.config import log_config

dictConfig(log_config)
# 日志设置
dir_log = "logs"
path_log = os.path.join(dir_log, 'server.log')
# 路径，每日分割时间，是否异步记录，日志是否序列化，编码格式，最长保存日志时间
logger.add(path_log, rotation='0:00', enqueue=True, serialize=False, encoding="utf-8", retention="10 days")
logger.info("======= server start ======")

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, uri: str):
    await websocket.accept()
    client_id = str(uuid.uuid4())
    w3ok = await ws_client.init_w3(client_id, uri)
    if not w3ok:
        await websocket.send_text('connect fail')
        await websocket.close()
    ws_client.connect(client_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await ws_client.receive(client_id, data)
    except Exception as e:
        logger.error(e)
        await websocket.close()
