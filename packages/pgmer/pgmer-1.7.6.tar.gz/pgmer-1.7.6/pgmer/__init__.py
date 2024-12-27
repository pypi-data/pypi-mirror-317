from Exce_postion import WebsocketProxy
from typing import Union
from loguru import logger
import websocket
import json
import ssl
class Pgmer(WebsocketProxy):
# 启动事件循环
    def on_message(ws, message:str)->str:
        try:
            data = json.loads(message)
            logger.info(f"WebSocket数据: {data}")
            if "key" in data:
                print(f"Value=>",{data['key']})
        except Exception as e:
            logger.error(f"Error: {e}")
    def on_error(ws, error:str)->str:
        logger.error(f"WebSocket 连接错误!: {error}")
    def on_close(ws, close_status_code, close_msg):
        logger.info("WebSocket 连接断开了!.",close_status_code,close_msg)
    def on_open(ws:str)->str:
        logger.info("WebSocket 连接已经建立成功!正在等待数据....")
    def Websocket_connect(ws_server: Union[str])->str:
       logger.info(f'WebSocket server: {ws_server}')
       try:
            server_top = websocket.WebSocketApp(ws_server,
            on_open=Pgmer.on_open,
            on_message=Pgmer.on_message,
            on_error=Pgmer.on_error,
            on_close=Pgmer.on_close)
            server_top.run_forever()
       except Exception as e:
           logger.info(f'Error: WebSocket connection failed.{e}')
    def ssl_websocket(ws_server: Union[str])->str:
          ssl_context=ssl.create_default_context()
          websocket_s=websocket.create_connection(ws_server,ssl=ssl_context)
          try:
              while True:
                data=websocket_s.recv()
                if data:
                    logger.info("收到数据:",data)
          except websocket.WebSocketConnectionClosedException as e:
              logger.info(f"WebSocket连接已关闭: {e}")
          finally:
              websocket_s.close()