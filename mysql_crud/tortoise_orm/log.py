#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time   :  2025/3/27 19:42
# @Author :  Allen
import logging

from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers.sql import PostgresLexer


class PygmentsFormatter(logging.Formatter):
    postgres = PostgresLexer()
    terminal_formatter = TerminalFormatter()

    def __init__(
        self,
        fmt="{asctime} - {name}:{lineno} - {levelname} - {message}",
        datefmt="%H:%M:%S",
    ):
        self.datefmt = datefmt
        self.fmt = fmt
        logging.Formatter.__init__(self, None, datefmt)

    def format(self, record: logging.LogRecord):
        """Format the logging record with slq's syntax coloration."""
        own_records = {
            attr: val
            for attr, val in record.__dict__.items()
            if not attr.startswith("_")
        }
        message = record.getMessage()
        name = record.name
        asctime = self.formatTime(record, self.datefmt)

        if name == "tortoise.db_client":
            if (
                record.levelname == "DEBUG"
                and not message.startswith("Created connection pool")
                and not message.startswith("Closed connection pool")
            ):
                message = highlight(message, self.postgres, self.terminal_formatter).rstrip()

        own_records.update(
            {
                "message": message,
                "name": name,
                "asctime": asctime,
            }
        )

        return self.fmt.format(**own_records)