#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time   :  2025/3/31 13:45
# @Author :  Allen
from tortoise import Model, fields


class Model1(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    deleted_at = fields.DatetimeField(null=True)

    class Meta:
        table = "M1"
        app = "app1"