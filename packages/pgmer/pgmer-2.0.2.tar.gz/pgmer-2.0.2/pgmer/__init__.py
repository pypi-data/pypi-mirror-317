from Exce_postion import WebsocketProxy
from typing import Union
from loguru import logger
import websocket
import json
import ssl
import websockets
import asyncio

class Pgmer(WebsocketProxy):
# 启动事件循环
    host_proxy = '127.0.0.1'
    port_proxy = 8080
    url_host = ''
    message_box_text=''
    def on_message(ws, message:str)->str:
        try:
            data = json.loads(message)
            logger.info(f"WebSocket数据: {data}")
            if "key" in data:
                logger.info(f"Value=>",{data['key']})
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
    def __init__(self, url: Union[str, None] = None):
        self.url_host = url if url else WebsocketProxy.url_host
        self.ssl_context = ssl.create_default_context()

    def set_url(self, url: Union[str, None]) -> str:
        try:
            if url is None:
                return "url is None, 数据不能为空!"
            else:
                self.url_host = url
                return self.url_host
        except Exception as e:
            logger.error(f"连接失败! URL不正确! {e}")
            return "连接失败! URL不正确!"

    async def proxy_handler(self, client_websocket, path):
        try:
            # 连接到目标 WebSocket 服务器
            async with websockets.connect(self.url_host, ssl=self.ssl_context) as target_websocket:
                logger.info(f"Connected to target server: {self.url_host}")

                # 创建两个任务来处理双向通信
                client_to_target_task = asyncio.create_task(self.client_to_target(client_websocket, target_websocket))
                target_to_client_task = asyncio.create_task(self.target_to_client(client_websocket, target_websocket))

                # 等待两个任务完成
                await asyncio.gather(client_to_target_task, target_to_client_task)
        except Exception as e:
            logger.error(f"Error in proxy handler: {e}")

    async def client_to_target(self, client_websocket, target_websocket):
        try:
            async for message in client_websocket:
                logger.info(f"Client to Target (原始): {message}")
                # 在这里可以修改消息
                modified_message = self.modify_client_to_target(message)
                await target_websocket.send(modified_message)
                logger.info(f"Sent to Target (修改后): {modified_message}")
        except Exception as e:
            logger.error(f"Error in client_to_target: {e}")

    async def target_to_client(self, client_websocket, target_websocket):
        try:
            async for message in target_websocket:
                logger.info(f"Target to Client (原始): {message}")
                # 在这里可以修改消息
                modified_message = self.modify_target_to_client(message)
                await client_websocket.send(modified_message)
                logger.info(f"Sent to Client (修改后): {modified_message}")
        except Exception as e:
            logger.error(f"Error in target_to_client: {e}")

    def modify_client_to_target(self, message: str) -> str:
        # 自定义修改逻辑
        # 例如，在消息末尾添加 "[Client Modified]"
        return message + WebsocketProxy.message_box_text

    def modify_target_to_client(self, message: str) -> str:
        # 自定义修改逻辑
        # 例如，在消息末尾添加 "[Target Modified]"
        return message +WebsocketProxy.message_box_text

    async def start_server(self):
        proxy_server = await websockets.serve(self.proxy_handler, self.host_proxy, self.port_proxy)
        logger.info(f"服务启动了端口在代理为 ws://{self.host_proxy}:{self.port_proxy}")
        await proxy_server.wait_closed()

    def run(self):
        asyncio.run(self.start_server())

    def set_proxy(self, proxty_host: str, proxty_port: Union[str, int], url: str) -> str:
        self.host_proxy = proxty_host
        self.port_proxy = proxty_port
        self.url_host = url
        logger.info('启动代理成功!')
        return f"启动代理成功! 代理地址: ws://{self.host_proxy}:{self.port_proxy} 目标服务器地址: {self.url_host}"

    def connect(self):
        if self.host_proxy == '127.0.0.1' and self.port_proxy == 8080:
            logger.warning('您当前为系统默认代理,建议配置代理!')
        self.run()

    @staticmethod
    def Disk_connect(ip: str, port: Union[str, int], url: str) -> str:
        proxy = WebsocketProxy(url)
        proxy.set_proxy(ip, port, url)
        proxy.connect()
        return f"启动代理成功! 代理地址: ws://{ip}:{port} 目标服务器地址: {url}"
    def Message(message_box:str):
        logger.info(f"Message: {message_box}")
        WebsocketProxy.message_box_text=message_box
        return WebsocketProxy.message_box_text