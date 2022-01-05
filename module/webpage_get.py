import logging

import requests
import retrying

STATUS_CODE_SUCCESS = 200

CHARSET_UTF8 = "utf-8"


@retrying.retry(
    stop_max_attempt_number=2,  # 最大尝试次数（即总共最多尝试 stop_max_attempt_number 次）
    wait_fixed=100,
    retry_on_exception=lambda e: isinstance(e, (requests.exceptions.ConnectionError,
                                                requests.exceptions.ReadTimeout,
                                                requests.exceptions.RequestException))
)
def retry_get(url: str, timeout: float) -> requests.Response:
    return requests.get(url, timeout=timeout)


def is_url_accessible(url: str, timeout: float) -> bool:
    """判断 url 是否可访问

    Args:
        url: url
        timeout: 超时时间
    """

    try:
        response = retry_get(url, timeout=timeout)
    except (requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout,
            requests.exceptions.RequestException) as e:
        logging.error("url[%s] isn't accessible, error: %s", url, e)
        return False

    status_code = response.status_code
    return status_code == STATUS_CODE_SUCCESS


def webpage_get(url: str, timeout: int) -> bytes:
    """获取 HTTP 结果并按 UTF-8 编码格式解析

    Args:
        url: url
        timeout: 超时时间

    Returns:
        按 UTF-8 编码格式解析的 HTTP 结果。
        如果 HTTP 访问失败，返回空字符串。
    """

    try:
        response = retry_get(url, timeout=timeout)
    except (requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout,
            requests.exceptions.RequestException) as e:
        logging.error("failed to get url[%s], error: %s", url, e)
        return bytes("", encoding=CHARSET_UTF8)

    content = response.content

    # response 有 apparent_encoding 和 encoding 两个编码字段，
    # 优先考虑 apparent_encoding
    charset = response.apparent_encoding if response.apparent_encoding else response.encoding
    if not charset:
        logging.warning("url[%s] charset is empty", url)
        return content

    try:
        content_after_recode = content.decode(charset).encode(CHARSET_UTF8)
    except UnicodeDecodeError as e:
        logging.error("failed to decode content, error: %s", e)
        return content

    return content_after_recode
