#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time   :  2025/3/31 13:53
# @Author :  Allen
# 监听 redis 队列, 获取到的数据推送到 nsq
import asyncio
import nsq
from redis.asyncio import Redis


class RedisToNSQ:
    def __init__(self, redis_url="redis://localhost:6379/0", nsq_addresses=None, redis_queue="redis_queue", nsq_topic="nsq-test-writer"):
        self.redis_url = redis_url
        self.nsq_addresses = nsq_addresses or ["localhost:4150"]
        self.redis_queue = redis_queue
        self.nsq_topic = nsq_topic

        self.redis = None
        self.producer = None

    async def connect(self):
        """初始化 Redis 和 NSQ 连接"""
        self.redis = await Redis.from_url(self.redis_url)
        self.producer = nsq.Writer(nsqd_tcp_addresses=self.nsq_addresses)

    async def close(self):
        """关闭 Redis 连接"""
        if self.redis:
            await self.redis.aclose()

    @staticmethod
    def finish_pub(conn, data):
        """NSQ 消息发布回调"""
        print("Published data:", data)
        print("Connection:", conn)

    async def push_to_nsq(self, data):
        """发送数据到 NSQ"""
        await self.producer.pub(self.nsq_topic, data.encode(), self.finish_pub)

    async def redis_reader(self):
        """从 Redis 读取数据并推送到 NSQ"""
        try:
            while True:
                data = await self.redis.blpop(self.redis_queue, timeout=60 * 5)
                if data:
                    _, message = data
                    print(f"Received from Redis: {message.decode()}")
                    await self.push_to_nsq(message.decode())
        except asyncio.CancelledError:
            pass
        finally:
            await self.close()

    async def run(self):
        """运行主逻辑"""
        await self.connect()
        await self.redis_reader()


if __name__ == "__main__":
    service = RedisToNSQ()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(service.run())

