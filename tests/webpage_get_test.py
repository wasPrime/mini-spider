import unittest
from module import webpage_get

NORMAL_URL_LIST = ["http://www.baidu.com"]
ABNORMAL_URL_LIST = ["aaa"]
DEFAULT_TIMEOUT = 1


class TestIsUrlAccessible(unittest.TestCase):
    def test_normal(self):
        for normal_url in NORMAL_URL_LIST:
            ret = webpage_get.is_url_accessible(normal_url, DEFAULT_TIMEOUT)
            self.assertTrue(ret)

    def test_abnormal(self):
        for abnormal_url in ABNORMAL_URL_LIST:
            ret = webpage_get.is_url_accessible(abnormal_url, DEFAULT_TIMEOUT)
            self.assertFalse(ret)


class TestWebpageGet(unittest.TestCase):
    def test_normal(self):
        for normal_url in NORMAL_URL_LIST:
            content = webpage_get.webpage_get(normal_url, DEFAULT_TIMEOUT)
            self.assertIsNotNone(content)
            self.assertIsNot(content, "")

    def test_abnormal(self):
        for abnormal_url in ABNORMAL_URL_LIST:
            content = webpage_get.webpage_get(abnormal_url, DEFAULT_TIMEOUT)
            self.assertIsNotNone(content)
            self.assertIs(content, "")
