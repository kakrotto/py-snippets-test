#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time   :  2025/3/27 17:58
# @Author :  Allen
import sys
import asyncio
import logging

from tortoise import Tortoise

from models.model1 import Model1
from models.model2 import Model2
from log import PygmentsFormatter
from config import CONFIG


class DBManager:

    def __init__(self):
        # 初始化日志
        self.logger = self.setup_logger()

    @staticmethod
    def setup_logger():
        """设置日志"""
        fmt = PygmentsFormatter(
            fmt="{asctime} - {name}:{lineno} - {levelname} - {message}",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(fmt)

        # 配置 logger
        logger = logging.getLogger("tortoise")
        logger.setLevel(logging.DEBUG)
        logger.addHandler(sh)


        return logger

    async def __aenter__(self):
        """初始化数据库连接"""
        await Tortoise.init(
            {
                "connections": {
                    "db1": CONFIG['database']['db1'],
                    "db2": CONFIG['database']['db2']
                },
                "apps": {
                    "app1": {"models": ["models.model1"], "default_connection": "db1"},
                    "app2": {"models": ["models.model2"], "default_connection": "db2"},
                },
                "use_tz": False,
                "timezone": "UTC",
            }
        )
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await Tortoise.close_connections()
        self.logger.info("Database connection closed")

    @staticmethod
    async def get_record(model, **filters):
        """查询单个记录"""
        return await model.filter(**filters).first()

async def main():
    async with DBManager() as db:
        await db.get_record(Model1, id=1)
        await db.get_record(Model2, id=1)

if __name__ == '__main__':
    asyncio.run(main())