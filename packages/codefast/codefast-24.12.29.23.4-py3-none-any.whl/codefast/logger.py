#!/usr/bin/env python3
import inspect
import os
import json
import pydantic
from loguru import logger as loguru_logger
import sys

loguru_logger.remove()
loguru_logger.add(
    sys.stderr,
    level="INFO",
    format="<level>{time:YYYY-MM-DD HH:mm:ss} | {message}</level>",
    colorize=True
)

loguru_logger.add(
    "/tmp/cf.log",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {message}",
    colorize=True
)


class LogData(pydantic.BaseModel):
    project: str = "default"
    filename: str
    level: str
    linenum: int
    content: str

    def __str__(self):
        return ' | '.join([self.level, self.project, self.filename, str(self.linenum), self.content])

    def model_dump_json(self, *args, **kwargs):
        return str(self)

class Logger:
    def __init__(self):
        self.project = "default"

    def config(self, project: str):
        self.project = project
        return self

    def info(self, content: str):
        add_log("INFO", content, self.project)

    def error(self, content: str):
        add_log("ERROR", content, self.project)

    def warning(self, content: str):
        add_log("WARNING", content, self.project)

    def debug(self, content: str):
        add_log("DEBUG", content, self.project)

    def critical(self, content: str):
        add_log("CRITICAL", content, self.project)


def add_log(level: str, content: str, project: str = "default"):
    caller_frame = inspect.currentframe().f_back.f_back
    filename = os.path.basename(caller_frame.f_code.co_filename)
    line_number = caller_frame.f_lineno

    log_data = LogData(filename=filename,
                       linenum=line_number,
                       content=str(content),
                       level=level,
                       project=project)

    if level == "INFO":
        loguru_logger.info(log_data.model_dump_json())
    elif level == "ERROR":
        loguru_logger.error(log_data.model_dump_json())
    elif level == "WARNING":
        loguru_logger.warning(log_data.model_dump_json())
    elif level == "DEBUG":
        loguru_logger.debug(log_data.model_dump_json())
    elif level == "CRITICAL":
        loguru_logger.critical(log_data.model_dump_json())
    else:
        loguru_logger.info(log_data.model_dump_json())

logger = Logger()
info = logger.info
error = logger.error
warning = logger.warning
debug = logger.debug
critical = logger.critical

if __name__ == "__main__":
    logger.info("codefast info test")
    logger.error("codefast error test")
    logger.warning("codefast warning test")
    logger.debug("codefast debug test")
    logger.critical("codefast critical test")
