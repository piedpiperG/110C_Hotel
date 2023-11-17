# consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging

logger = logging.getLogger(__name__)


class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info("WebSocket连接建立")
        await self.accept()

    async def receive(self, text_data):
        if not text_data:
            logger.error("Empty message received")
            return  # 不处理空消息，但保持连接开放

        try:
            data = json.loads(text_data)
            logger.info(f"Received data: {data}")
            # 处理数据...
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析错误: {e}")
            # 发生解析错误时不关闭连接，只记录错误信息
