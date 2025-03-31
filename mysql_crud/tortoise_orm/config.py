#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time   :  2025/3/27 18:05
# @Author :  Allen
import yaml
from pathlib import Path


# 获取项目根目录路径
project_root = Path(__file__).parent.absolute()

# 配置文件路径
local_config_path = project_root.parent.parent.joinpath('config.local.yaml')
example_config_path = project_root.parent.parent.joinpath('config.yaml')

# 如果config.local.yaml不存在，使用config.yaml
config_path = local_config_path if local_config_path.exists() else example_config_path

# 读取配置文件
try:
    with open(config_path) as f:
        CONFIG = yaml.safe_load(f)
        if CONFIG is None:
            CONFIG = {}
except FileNotFoundError as e:
    CONFIG = {}  # type: ignore
    print(f"解析配置文件错误：{e}，退出")
    exit()


TORTOISE_ORM = {
    "connections": {"default": CONFIG["database"]['db_local']},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


