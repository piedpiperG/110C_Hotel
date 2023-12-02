import asyncio

import numpy as np
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging
from Air_Condition.models import Message
from asgiref.sync import sync_to_async
from datetime import datetime
from django.core.exceptions import ValidationError
from Air_Condition.models import Scheduler, Room
from channels.db import database_sync_to_async

logger = logging.getLogger(__name__)


# ===============类================
class RoomCounter:  # 分配房间号
    num = 0
    dic = {}


class RoomInfo:  # Room->字典
    dic = {
        "target_temp": "--",
        "init_temp": "--",
        "current_temp": "--",
        "fan_speed": "--",
        "fee": 0,
        "room_id": 0
    }

    def __init__(self, room):
        self.dic["target_temp"] = room.target_temp
        self.dic["init_temp"] = room.init_temp
        self.dic["current_temp"] = int(room.current_temp)
        self.dic["fan_speed"] = speed_ch[room.fan_speed]
        self.dic["fee"] = int(room.fee)
        self.dic["room_id"] = room.room_id


class RoomsInfo:  # 监控器使用
    def __init__(self, rooms):
        self.dic = {
            "room_id": [0],
            "state": [""],
            "fan_speed": [""],
            "current_temp": [0],
            "fee": [0],
            "target_temp": [0],
            "fee_rate": [0]
        }
        if rooms:
            for room in rooms:  # 从1号房开始
                self.dic["room_id"].append(room.room_id)
                self.dic["state"].append(state_ch[room.state])
                self.dic["fan_speed"].append(speed_ch[room.fan_speed])
                self.dic["current_temp"].append('%.2f' % room.current_temp)
                self.dic["fee"].append('%.2f' % room.fee)
                self.dic["target_temp"].append(room.target_temp)
                self.dic["fee_rate"].append(room.fee_rate)


class RoomBuffer:  # 房间数据缓存
    on_flag = [None, False, False, False, False, False]
    target_temp = [32, 25, 25, 25, 25, 25]  # 不要用数组。。。。
    init_temp = [0, 30, 28, 30, 29, 35]


class ChartData:
    open_time = []  # 五个房间的开机时长
    record_num = 0  # 详单数
    schedule_num = 0  # 调度次数
    open_num = []  # 五个房间的*开机次数*
    change_temp_num = []  # 五个房间的调温次数
    change_fan_num = []  # 五个房间的调风速次数
    # ---numpy---
    fee = np.zeros([6, 30])  # 五个房间，30分钟内费用 + 30分钟内总费用


# ============静态变量===========
room_c = RoomCounter  # 静态
room_info = RoomInfo
room_b = RoomBuffer
speed_ch = ["", "高速", "中速", "低速"]
state_ch = ["", "服务中", "等待", "关机", "休眠"]
scheduler = Scheduler()  # 属于model模块


# ===============================


class MyConsumer(AsyncWebsocketConsumer):
    INFO = False

    async def connect(self):
        logger.info("WebSocket连接建立")
        await self.accept()

        # 启动定期发送消息的任务
        self.send_task = asyncio.create_task(self.send_message_periodically())

    async def disconnect(self, close_code):
        # 当WebSocket断开连接时，取消定期发送消息的任务
        if self.send_task:
            self.send_task.cancel()
            try:
                await self.send_task
            except asyncio.CancelledError:
                logger.info("定期发送消息的任务已取消")

    async def receive(self, text_data):
        if not text_data:
            logger.error("Empty message received")
            return  # 不处理空消息，但保持连接开放

        try:
            data = json.loads(text_data)
            logger.info(f"Received data: {data}")
            # 处理数据...
            # ---------------------------------------------------------------------------------------------#
            # 假设数据包含一个特定的动作
            action = data.get('action')
            if action == 'init':
                await self.get_room_id(data)
                await self.init_sch(data)
            if action == 'power':
                await self.power(data)
            if action == 'change_high':
                await self.change_high(data)
            if action == 'change_mid':
                await self.change_mid(data)
            if action == 'change_low':
                await self.change_low(data)
            if action == 'change_up':
                await self.change_up(data)
            if action == 'change_down':
                await self.change_down(data)

            # --------------------------------------------------------------------------------------------#
            # 异步保存消息到数据库
            await self.save_message(data)

        except json.JSONDecodeError as e:
            logger.error(f"JSON解析错误: {e}")
            # 发生解析错误时不关闭连接，只记录错误信息

        await self.send('即时返回消息')

    async def get_room_id(self, data):
        # 处理特定的动作
        # 这里可以进行消息的发送或接收处理

        s_id = data.get('room_id')
        logger.info(s_id)
        if s_id not in room_c.dic:
            room_c.num = room_c.num + 1
            room_c.dic[s_id] = room_c.num
            return room_c.num
        else:
            return room_c.dic[s_id]

    async def init_sch(self, data):
        room_id = int(await self.get_room_id(data))
        await self.async_update_state(room_id)

    async def power(self, data):
        room_id = int(await self.get_room_id(data))
        if not room_b.on_flag[room_id]:
            room_b.on_flag[room_id] = True
            await self.async_request_on(room_id, room_b.init_temp[room_id])
            await self.async_set_init_temp(room_id, room_b.init_temp[room_id])
        else:
            room_b.on_flag[room_id] = False
            await self.async_request_off(room_id)

    async def change_high(self, data):
        room_id = int(await self.get_room_id(data))
        await self.async_change_fan_speed(room_id, 1)

    async def change_mid(self, data):
        room_id = int(await self.get_room_id(data))
        await self.async_change_fan_speed(room_id, 2)

    async def change_low(self, data):
        room_id = int(await self.get_room_id(data))
        await self.async_change_fan_speed(room_id, 3)

    async def change_up(self, data):
        room_id = int(await self.get_room_id(data))
        temperature = room_b.target_temp[room_id] + 1
        room_b.target_temp[room_id] = temperature
        await self.async_change_target_temp(room_id, temperature)

    async def change_down(self, data):
        room_id = int(await self.get_room_id(data))
        temperature = room_b.target_temp[room_id] - 1
        room_b.target_temp[room_id] = temperature
        await self.async_change_target_temp(room_id, temperature)

    @database_sync_to_async
    def async_request_on(self, room_id, init_temp):
        scheduler.request_on(room_id, init_temp)

    @database_sync_to_async
    def async_update_state(self, room_id):
        scheduler.update_room_state(room_id)

    @database_sync_to_async
    def async_set_init_temp(self, room_id, init_temp):
        scheduler.set_init_temp(room_id, init_temp)

    @database_sync_to_async
    def async_request_off(self, room_id):
        scheduler.request_off(room_id)

    @database_sync_to_async
    def async_change_fan_speed(self, room_id, speed):
        scheduler.change_fan_speed(room_id, speed)

    @database_sync_to_async
    def async_change_target_temp(self, room_id, temperature):
        scheduler.change_target_temp(room_id, temperature)

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
            # room_id = get_room_id(request)
            # room = scheduler.update_room_state(room_id)

            # 定时向客户端发送消息
            await self.send(text_data=json.dumps({
                'current_temp': '20',
            }))
            await asyncio.sleep(1)  # 根据需要调整休眠时间
            # logger.info('发送周期性消息:20')
