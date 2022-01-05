# -*- coding: utf-8 -*-
"""保存已抓取的 URL 列表，用于去重"""

import threading


class URLTable:
    """线程安全的 URL 集合

    存储已访问过的 URL。

    Attributes:
        visited_url_set: 集合
        lock: 对 visited_url_set 的读写锁
    """

    def __init__(self):
        self.__visited_url_set = set()
        self.__lock = threading.Lock()

    def put(self, url: str):
        """插入元素"""

        with self.__lock:
            self.__visited_url_set.add(url)

    def has_element(self, url: str) -> bool:
        """判断元素是否已存在"""

        with self.__lock:
            ret = url in self.__visited_url_set
        return ret
