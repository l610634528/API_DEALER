import logging
import os
import datetime
import requests
# 项目路径
prj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 当前文件的上一级的上一级目录（增加一级）
# print(prj_path)
data_path = os.path.join(prj_path, 'data')  # 数据目录
test_path = os.path.join(prj_path, 'test')   # 用例目录

log_file = os.path.join(prj_path, 'log', 'log.txt')  # 更改路径到log目录下
report_file = os.path.join(prj_path, 'report', 'report.html')  # 更改路径到report目录下
REPORT_PATH = os.path.join(prj_path, 'report')
# log配置
logging.basicConfig(level=logging.DEBUG,  # log level
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',  # log格式
                    datefmt='%Y-%m-%d %H:%M:%S',  # 日期格式
                    filename=log_file,  # 日志输出文件
                    filemode='a')  # 追加模式

# 数据库配置
db_host = '115.28.108.130'
db_port = 3306
db_user = 'test'
db_passwd = '123456'
db = 'api_test'

# 邮件配置
smtp_server = 'smtp.163.com'
smtp_user = 'l610634528@163.com'
smtp_password = 'lvxj64518881'

sender = smtp_user  # 发件人
receiver = '610634528@qq.com'  # 收件人
subject = '接口测试报告'  # 邮件主题

# token
dealer_url = 'http://autotest.cba.zcabc.com'
login = dealer_url + 'login'
# JJ_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIiLCJhdWQiOiIiLCJpYXQiOjE1NjUyNTA3ODksImlkIjozOTh9.2DH8W0XkPPuqQDwhuDnUPSy-50l3zpo1IkAV-upfFH4"

# 获取当前系统时间，精确到天
curr_time = datetime.datetime.now()
curr_time_start = str(datetime.datetime.now().year + 1) + '-01-01'
curr_time_end = str(datetime.datetime.now().year + 1) + '-12-31'
# print(curr_time)
time = curr_time.date()
# print(curr_time_start)

