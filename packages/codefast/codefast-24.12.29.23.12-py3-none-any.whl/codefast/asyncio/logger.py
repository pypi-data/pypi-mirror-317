#!/usr/bin/env python3
import inspect
import os
import json
from codefast.utils import b64decode
import httpx
import pydantic
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_fixed
import sys

logger.remove()
logger.add(
    sys.stderr,
    level="INFO",
    format="<level>{time:YYYY-MM-DD HH:mm:ss} | {message}</level>",
    colorize=True
)

logger.add(
    "/tmp/cf.log",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {message}",
    colorize=True
)

API_ENCODED = 'aHR0cHM6Ly9sb2dzLmN1Zm8uY2MvYXBpL2xvZ3MvYWRkCg=='
API = b64decode(API_ENCODED)


class LogData(pydantic.BaseModel):
    project: str = "default"
    filename: str
    level: str
    linenum: int
    content: str

    def __str__(self):
        return json.dumps(self.model_dump(), ensure_ascii=False, indent=4)


class AsyncLogger:
    def __init__(self):
        self.project = "default"
        self.upload = True

    def config(self, project: str, upload: bool = True):
        self.project = project
        self.upload = upload
        return self

    async def info(self, content: str):
        await add_log("INFO", content, self.project, self.upload)

    async def error(self, content: str):
        await add_log("ERROR", content, self.project, self.upload)

    async def warning(self, content: str):
        await add_log("WARNING", content, self.project, self.upload)

    async def debug(self, content: str):
        await add_log("DEBUG", content, self.project, self.upload)

    async def critical(self, content: str):
        await add_log("CRITICAL", content, self.project, self.upload)


async def add_log(level: str, content: str, project: str = "default", upload: bool = True):
    caller_frame = inspect.currentframe().f_back.f_back
    filename = os.path.basename(caller_frame.f_code.co_filename)
    line_number = caller_frame.f_lineno

    log_data = LogData(filename=filename,
                       linenum=line_number,
                       content=str(content),
                       level=level,
                       project=project)

    if level == "INFO":
        logger.info(log_data.model_dump_json())
    elif level == "ERROR":
        logger.error(log_data.model_dump_json())
    elif level == "WARNING":
        logger.warning(log_data.model_dump_json())
    elif level == "DEBUG":
        logger.debug(log_data.model_dump_json())
    elif level == "CRITICAL":
        logger.critical(log_data.model_dump_json())
    else:
        logger.info(log_data.model_dump_json())

    if not upload:
        return

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    async def send_log_to_api():
        async with httpx.AsyncClient() as client:
            response = await client.post(API,
                                         json={
                                             "content": str(log_data),
                                             "level": level,
                                         },
                                         timeout=30.0)
            response.raise_for_status()

    try:
        await send_log_to_api()
    except httpx.HTTPStatusError as e:
        error_data = {
            "filename": filename,
            "linenum": line_number,
            "content": f"Failed to send log to API. Status code: {e.response.status_code}"
        }
        logger.error(error_data)
    except httpx.RequestError as e:
        error_data = {
            "filename": filename,
            "linenum": line_number,
            "content": f"Network error occurred while sending log to API: {str(e)}"
        }
        logger.error(error_data)
    except Exception as e:
        error_data = {
            "filename": filename,
            "linenum": line_number,
            "content": f"Unexpected error occurred while sending log to API: {str(e)}"
        }
        logger.error(error_data)


alogger = AsyncLogger()


if __name__ == "__main__":
    import asyncio
    asyncio.run(alogger.info("test"))
    try:
        raise Exception("test alooger")  # noqa
    except Exception as e:
        from traceback import format_exc
        asyncio.run(alogger.error(format_exc()))
