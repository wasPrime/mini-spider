# -*- coding: utf-8 -*-
"""读取种子文件"""

import logging
import os
from typing import List


def read_seed(seed_dir: str, seed_file_name: str) -> List[str]:
    """读取种子

    Args:
        seed_dir: 种子文件所在文件夹
        seed_file_name: 种子文件名

    Returns:
        种子 url 列表。

    Raise: FileNotFoundError
    """

    # 拼接种子文件实际完整路径
    seed_file_path = os.path.join(seed_dir, seed_file_name)
    if not os.path.isfile(seed_file_path):
        logging.error(
            "seed file[%s] doesn't exist or isn't a file", seed_file_path)
        raise FileNotFoundError(seed_file_path)

    logging.info("seed_file_path: %s", seed_file_path)

    seed_list = []
    with open(seed_file_path) as seed_file:
        for seed in seed_file:
            seed_list.append(seed.strip())

    logging.info(
        "succeed to import seed list from seed file[%s]", seed_file_path)

    return seed_list
