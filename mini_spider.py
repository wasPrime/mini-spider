# -*- coding: utf-8 -*-
"""主程序"""

import argparse
import configparser
import logging
import logging.handlers
import os
import pathlib
import traceback

from module import config_load, crawler

PROJECT_NAME = "mini-spider"
DEFAULT_CONF_DIR = "conf"
DEFAULT_CONF_NAME = "spider.conf"
DEFAULT_LOG_DIR = "log"
DEFAULT_LOG_FILE_NAME = "mini_spider.log"


def version() -> str:
    return "v1.0.0"


def init_logging(log_dir: str, log_file_name: str) -> None:
    pathlib.Path(log_dir).mkdir(parents=True, exist_ok=True)  # 日志目录已存在则忽略

    logging.basicConfig(
        # 日志文件在 handler 中设置切分
        # filename=os.path.join(log_dir, log_file_name),
        # filemode="a+",
        level=logging.WARNING,
        handlers=[logging.handlers.TimedRotatingFileHandler(
            filename=os.path.join(log_dir, log_file_name),
            when='H',  # 按小时切分
            interval=1,
            backupCount=72  # 保存 3 天的日志
        )],
        # format="%(asctime)s.%(msecs)03d %(pathname)s:%(lineno)d [%(levelname)s] %(message)s",
        format="%(asctime)s.%(msecs)03d %(filename)s:%(lineno)d [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")


def arg_parse() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(description=PROJECT_NAME)

    arg_parser.add_argument("--conf-dir", type=str,
                            default=DEFAULT_CONF_DIR, help="set configuration dir")
    arg_parser.add_argument("-c", "--conf", type=str,
                            default=DEFAULT_CONF_NAME, help="set configuration file name")

    arg_parser.add_argument("--log-dir", type=str,
                            default=DEFAULT_LOG_DIR, help="set log dir")
    arg_parser.add_argument("--log", type=str,
                            default=DEFAULT_LOG_FILE_NAME, help="set log file name")

    arg_parser.add_argument("-v", "--version", action="version",
                            version=version(), help="show mini-spider version")

    return arg_parser.parse_args()


if __name__ == "__main__":
    args = arg_parse()

    init_logging(args.log_dir, args.log)

    try:
        conf = config_load.read_conf(args.conf_dir, args.conf)
    except (FileNotFoundError,
            configparser.ParsingError,
            KeyError,
            ValueError,
            TypeError):
        logging.fatal("failed to read conf, error: %s",
                      traceback.format_exc())
        exit(-1)

    controller = crawler.CrawlerController(args.conf_dir, conf)
    controller.start()
