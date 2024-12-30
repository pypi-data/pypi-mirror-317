import copy
import logging
import sys
from typing import List

from loguru import logger

_base_format = "{time:YYYY-MM-DD HH:mm:ss.SSS} {process.name},{thread.name} {file.name}:{line} [{level.name}] {message}"
_level_mapper = {
    "debug": {"level": logging.DEBUG, "format": f"<cyan>{_base_format}</cyan>"},
    "warning": {"level": logging.WARNING, "format": f"<yellow>{_base_format}</yellow>"},
    "warn": {"level": logging.WARNING, "format": f"<yellow>{_base_format}</yellow>"},
    "info": {"level": logging.INFO, "format": f"<green>{_base_format}</green>"},
    "error": {"level": logging.ERROR, "format": f"<red>{_base_format}</red>"},
    "critical": {"level": logging.CRITICAL, "format": f"<magenta>{_base_format}</magenta>"},
}


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def install(log_defines: List = None):
    # 删除默认handler
    logger.remove()
    # 兼容默认logging
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.NOTSET)

    if not log_defines:
        log_defines = [{"level": "debug"}]

    for ori_log_define in log_defines:
        #  获取定义的参数
        log_define = copy.deepcopy(ori_log_define)
        sink = log_define.pop("sink", sys.stdout)
        level_define = log_define.pop("level", "debug")
        colorize = log_define.pop("colorize", True)
        enqueue = log_define.pop("enqueue", True)

        level_detail = _level_mapper[level_define]
        level = level_detail.get("level")
        level_format = level_detail.get("format")
        formatter = log_define.pop("format", level_format)

        logger.add(
            sink,
            level=level,
            format=formatter,
            colorize=colorize,
            enqueue=enqueue,
            **log_define,
        )


def debug(message, *args, **kwargs):
    logger.debug(message, *args, **kwargs)


def info(message, *args, **kwargs):
    logger.info(message, *args, **kwargs)


def warning(message, *args, **kwargs):
    logger.warning(message, *args, **kwargs)


def error(message, *args, **kwargs):
    logger.error(message, *args, **kwargs)


def critical(message, *args, **kwargs):
    logger.critical(message, *args, **kwargs)


def exception(message, *args, **kwargs):
    logger.exception(message, *args, **kwargs)
