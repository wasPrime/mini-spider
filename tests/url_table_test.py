import unittest
from module import url_table


class TestURLTable(unittest.TestCase):
    url_cases = [
        "http://www.baidu.com",
    ]

    def test_normal(self):
        table = url_table.URLTable()
        for url in self.url_cases:
            table.put(url)
            self.assertTrue(table.has_element(url))

    def test_abnormal(self):
        table = url_table.URLTable()
        for url in self.url_cases:
            self.assertFalse(table.has_element(url))
