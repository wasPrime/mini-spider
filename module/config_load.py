# -*- coding: utf-8 -*-
"""读取配置文件"""

import configparser
import logging
import os
from dataclasses import dataclass

MAIN_SECTION_NAME = "spider"


@dataclass
class Config:
    url_list_file: str  # 种子文件路径
    output_directory: str  # 抓取结果存储目录
    max_depth: int  # 最大抓取深度（种子为 0 级）
    crawl_interval: int  # 抓取间隔. 单位: 秒
    crawl_timeout: int  # 抓取超时. 单位: 秒
    target_url: str  # 需要存储的目标网页 URL pattern（正则表达式）
    thread_count: int  # 抓取线程数


def read_conf(conf_dir: str, conf_file_name: str) -> Config:
    """读取配置文件

    Args:
        conf_dir: 配置文件所在文件夹
        conf_file_name: 配置文件名

    Returns:
        配置文件解析出的 Config 对象。

    Raise:
        FileNotFoundError
        configparser.ParsingError
        KeyError
        ValueError
        TypeError
    """

    # 拼接配置文件实际完整路径
    conf_file_path = os.path.join(conf_dir, conf_file_name)
    if not os.path.isfile(conf_file_path):
        logging.error(
            "config file[%s] doesn't exist or isn't a file", conf_file_path)
        raise FileNotFoundError(conf_file_path)

    logging.info("conf_file_path: %s", conf_file_path)

    # 读取配置文件
    conf_parser = configparser.ConfigParser()
    conf_parser.read(conf_file_path)

    # 保证有主 section
    if not conf_parser.has_section(MAIN_SECTION_NAME):
        logging.error(
            "config file[%s] doesn't have section[%s]", conf_file_path, MAIN_SECTION_NAME)
        raise configparser.ParsingError(
            "No section named %s" % MAIN_SECTION_NAME)

    # 解析各项 option
    options = conf_parser[MAIN_SECTION_NAME]
    config_file_keys = set(options.keys())  # 配置文件中 key 集合
    config_class_keys = set(Config.__dataclass_fields__.keys())  # Config 类字段集合
    # 只取需要的字段，支持配置文件中存在冗余字段
    useful_field_dict = {}
    for config_class_key in config_class_keys:
        # 若配置文件未提供 Config 需要的字段，抛出异常
        if config_class_key not in config_file_keys:
            logging.error(
                "config_class_key[%s] not in config_file_keys", config_class_key)
            raise KeyError(config_class_key)

        field_type = Config.__dataclass_fields__[config_class_key].type
        if field_type == int:
            value = options.getint(config_class_key)
        elif field_type == float:
            value = options.getfloat(config_class_key)
        elif field_type == bool:
            value = options.getboolean(config_class_key)
        elif field_type == str:
            value = options.get(config_class_key)
        else:
            raise TypeError("invalid type %s for field %s",
                            field_type, config_class_key)

        useful_field_dict[config_class_key] = value

    conf = Config(**useful_field_dict)
    logging.info(
        "succeed to parse config file[%s] to Config[%s]", conf_file_path, conf)

    return conf
