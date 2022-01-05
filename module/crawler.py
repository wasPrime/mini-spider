# -*- coding: utf-8 -*-
"""实现抓取线程"""

import logging
import pathlib
import queue
import re
import threading
import time

from module import (config_load, seedfile_load, url_table, webpage_get,
                    webpage_parse, webpage_save)


class Crawler(threading.Thread):
    """爬虫线程

    不直接使用，统一通过 CrawlerController 控制。

    Attributes:
        conf: 配置类
        url_queue: url 队列
        url_set: url 已访问集合
        event: 停止线程事件
        pattern: url 正则表达式匹配模式
    """

    def __init__(self, conf: config_load.Config,
                 url_queue: queue.Queue, url_set: url_table.URLTable,
                 event: threading.Event, pattern: re.Pattern):
        threading.Thread.__init__(self)

        self.__conf = conf
        self.__url_table = url_set
        self.__url_queue = url_queue
        self.__stop_event = event

        self.__pattern = pattern

    def run(self) -> None:
        while not self.__stop_event.is_set():
            url, depth = self.__url_queue.get()
            if self.__url_table.has_element(url):
                self.__url_queue.task_done()
                continue
            # 在处理 sub_url 前就将此 url 放入已访问集合中，避免重复处理同一个 url
            self.__url_table.put(url)

            if not self.__pattern.match(url):
                logging.warning("url[%s] doesn't match url regex pattern", url)
                self.__url_queue.task_done()
                continue

            content = webpage_get.webpage_get(
                url, self.__conf.crawl_timeout)

            if content:
                webpage_save.save_file(
                    content, url, self.__conf.output_directory)

                # 到达广度遍历最深处则直接结束本轮操作
                if depth >= self.__conf.max_depth:
                    self.__url_queue.task_done()
                    continue

                sub_urls = webpage_parse.webpage_parse(content, url)
                for sub_url in sub_urls:
                    if self.__url_table.has_element(sub_url):
                        continue
                    self.__url_queue.put((sub_url, depth + 1))

            self.__url_queue.task_done()

            time.sleep(self.__conf.crawl_interval)


class CrawlerController:
    """爬虫控制类

    控制整体爬虫逻辑。

    Attributes:
        conf_dir: 配置文件目录
        conf: 配置类
    """

    def __init__(self, conf_dir: str, conf: config_load.Config):
        self.__conf_dir = conf_dir
        self.__conf = conf

        self.__urls_queue = queue.Queue()  # 自身线程安全的队列，队列元素为 (seed_url, depth)
        self.__url_table = url_table.URLTable()
        self.__event = threading.Event()

        # 预处理 url 的正则表达式
        # 多个 Crawler 复用此 pattern，避免多次构造
        self.__pattern = re.compile(self.__conf.target_url)

    def start(self) -> None:
        """开始爬取"""

        self.__read_seeds()
        self.__create_output_directory()
        self.__start_crawl()

    def __read_seeds(self) -> None:
        """读取种子 url"""

        try:
            seed_urls = seedfile_load.read_seed(
                self.__conf_dir, self.__conf.url_list_file)
        except FileNotFoundError as e:
            logging.fatal(
                "failed to read seed, conf_dir[%s], url_list_file[%s], error: %s",
                self.__conf_dir, self.__conf.url_list_file, e)
            exit(-1)

        for seed_url in seed_urls:
            if not self.__pattern.match(seed_url):
                logging.warning(
                    "seed_url[%s] doesn't match url regex pattern", seed_url)
                continue

            if not webpage_get.is_url_accessible(seed_url, self.__conf.crawl_timeout):
                logging.warning(
                    "seed_url[%s] isn't accessible", seed_url)
                continue

            self.__urls_queue.put((seed_url, 0))

    def __create_output_directory(self) -> None:
        """创建输出目录"""

        pathlib.Path(self.__conf.output_directory).mkdir(
            parents=True, exist_ok=True)  # 输出目录已存在则忽略

    def __start_crawl(self) -> None:
        """正式开始多线程爬虫爬取"""

        thread_list = []
        for _ in range(self.__conf.thread_count):
            thread = Crawler(self.__conf, self.__urls_queue,
                             self.__url_table, self.__event, self.__pattern)
            thread.setDaemon(True)  # 主线程运行结束时，不对这个子线程进行检查，直接退出
            thread_list.append(thread)

        for thread in thread_list:
            thread.start()

        self.__urls_queue.join()
        self.__event.set()
