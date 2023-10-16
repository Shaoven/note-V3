import unittest
from BeautifulReport import BeautifulReport
import os

DIR = os.path.dirname(os.path.abspath(__file__))
testLoader = unittest.TestLoader()


# 线上：Online  测试：Offline
Environ = "Online"


def run(test_suite):
    # 定义输出的文件位置和名字
    filename = "report.html"
    result = BeautifulReport(test_suite)
    result.report(filename=filename, description='测试报告', report_dir='./')


if __name__ == '__main__':
    pattern = 'all'  # all执行全量用例，smoking冒烟用例
    if pattern == 'all':
        suite = testLoader.discover("./testCase", "test*.py")  #
    else:
        suite = testLoader.discover("./testCase", "test_level1*.py")
    run(suite)
