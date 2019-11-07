import unittest
from lib.HTMLTestReportCN import HTMLTestRunner
# from api_test_dealer.lib.HTMLTestRunner import HTMLTestRunner
from config.config import *
from lib.send_email import send_email
import time
logging.info("================================== 测试开始 ==================================")
suite = unittest.defaultTestLoader.discover(test_path)
now = time.strftime('%Y-%m-%d_%H_%M', time.localtime(time.time()))
report = REPORT_PATH + '\\%s.html' % now
print(report)
with open(report, 'wb') as f:  # 从配置文件中读取
    HTMLTestRunner(stream=f, title="经销商审批", description="测试描述", tester="lv and wang").run(suite)

send_email(report)  # 从配置文件中读取
logging.info("================================== 测试结束 ==================================")
