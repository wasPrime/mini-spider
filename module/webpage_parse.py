# -*- coding: utf-8 -*-
"""对抓取网页的解析"""

import html.parser
import logging
import urllib.parse
from typing import List

HTTP_PREFIX = "http:"


class PageParser(html.parser.HTMLParser):
    """个性化的 HTMLParser

    src_url: 来源 url
    sub_links: 网页正文（content）中的链接列表
    """

    def __init__(self, src_url):
        html.parser.HTMLParser.__init__(self)
        self.__src_url = src_url

        self.sub_links = []

    def handle_starttag(self, tag: str, attrs: List[str]) -> None:
        """handle_starttag

        Args:
            tag: HTML 标签
            attrs: 结构化 HTTP 属性
        """

        if tag == "a" or tag == "link":
            for k, v in attrs:
                if k == "href":
                    new_url = self.join_url(self.__src_url, v)
                    if new_url != "":
                        self.sub_links.append(new_url)

    @staticmethod
    def join_url(src_url: str, href_url: str) -> str:
        """拼接 url

        Args:
            src_url: 来源 url
            href_url: 后缀 url

        Returns:
            拼接后的 url 结果。
        """

        url_parser = urllib.parse.urlparse(href_url)
        href_loc = url_parser.netloc
        href_scheme = url_parser.scheme
        href_path = url_parser.path

        logging.info(
            "href_loc[%s] href_scheme[%s] href_path[%s]", href_loc, href_scheme, href_path)

        if href_loc == "":
            url = urllib.parse.urljoin(
                src_url, href_path) if href_scheme != "javascript" else ""
        elif href_scheme == "":
            url = HTTP_PREFIX + href_url
        else:
            url = href_url

        return url


def webpage_parse(content: bytes, src_url: str) -> List[str]:
    page_parser = PageParser(src_url)
    page_parser.feed(str(content))
    page_parser.close()

    logging.debug(
        "the sub urls list from url[%s]: %s", src_url, page_parser.sub_links)

    return page_parser.sub_links
