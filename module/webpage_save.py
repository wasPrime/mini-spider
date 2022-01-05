# -*- coding: utf-8 -*-
"""将网页保存到磁盘"""

import logging
import os
import urllib.parse


def save_file(content: bytes, url: str, output_dir: str) -> None:
    """保存文件

    Args:
        content: 网页正文
        url: url 名称
        output_dir: 输出文件夹
    """

    file_name = urllib.parse.quote_plus(url)  # 格式化各种符号，如 ':' -> %3A
    file_path = os.path.join(output_dir, file_name)

    try:
        # 以二进制格式保存
        with open(file_path, "wb+") as file:
            file.truncate()
            file.write(content)
            logging.info("succeed to save url[%s] in disk", url)
    except OSError as e:
        logging.error("failed to save file[%s], error: %s", file_path, e)
