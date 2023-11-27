import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging
from Air_Condition.models import Message
from asgiref.sync import sync_to_async
from datetime import datetime
from django.core.exceptions import ValidationError

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
            # 异步保存消息到数据库
            await self.save_message(data)

        except json.JSONDecodeError as e:
            logger.error(f"JSON解析错误: {e}")
            # 发生解析错误时不关闭连接，只记录错误信息

    async def save_message(self, data):
        # 解析 current_time 字段
        current_time_str = data.get('current_time', '')
        try:
            # 使用适合时间（不包含日期）的格式字符串
            current_time = datetime.strptime(current_time_str, '%H:%M:%S').time()
        except ValueError:
            logger.error("日期时间格式错误")
            # 可以在这里处理错误，例如发送错误消息回客户端
            return  # 返回以避免进一步执行

        try:
            # 使用 sync_to_async 包装同步的数据库操作
            await sync_to_async(Message.objects.create)(
                room_id=data.get('room_id', ''),
                temperature_set=data.get('temperature_set', ''),
                temperature_out=data.get('temperature_out', ''),
                fan_model=data.get('fan_model', ''),
                fan_speed=data.get('fan_speed', ''),
                condition_set=data.get('condition_set', ''),
                current_time=current_time,  # 使用解析后的时间
            )
        except ValidationError as e:
            logger.error(f"验证错误: {e}")
            # 可以在这里处理验证错误
        except:
            logger.error('空数据')

    async def send_message_periodically(self):
        while True:
            # 定时向客户端发送消息
            await self.send(text_data=json.dumps({
                'message': 'Periodic message from server',
            }))
            await asyncio.sleep(1)  # 休眠5秒，可以根据需求调整
            logger.error('发送')
