#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time   :  2023/10/12 13:53
# @Author :  Allen
import asyncio
import json
from datetime import datetime
import nsq


class NSQSubscriber:
    def __init__(self, nsqd_addresses, topics, channel='test', max_in_flight=1):
        self.nsqd_addresses = nsqd_addresses
        self.topics = topics if isinstance(topics, list) else [topics]
        self.channel = channel
        self.max_in_flight = max_in_flight
        self.loop = self.get_event_loop()

    def get_event_loop(self):
        """安全获取事件循环，避免 DeprecationWarning"""
        try:
            return asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop

    async def message_handler(self, message: nsq.Message):
        """处理 NSQ 消息"""
        message.enable_async()
        data = message.body.decode()
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            print(f"解析 NSQ JSON 失败: {data}")
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{now} - 接受数据: {data}")
        message.finish()

    async def subscribe(self):
        """订阅 NSQ 主题"""
        for topic in self.topics:
            nsq.Reader(
                message_handler=self.message_handler,
                nsqd_tcp_addresses=self.nsqd_addresses,
                topic=topic,
                channel=self.channel,
                max_in_flight=self.max_in_flight
            )
            print(f"订阅开始: {topic}")

    def run(self):
        """启动 NSQ 订阅"""
        self.loop.create_task(self.subscribe())
        try:
            self.loop.run_forever()
        finally:
            self.loop.close()


if __name__ == '__main__':
    subscriber = NSQSubscriber(
        nsqd_addresses=['localhost:4150'],
        topics=['nsq-test-writer']
    )
    subscriber.run()

