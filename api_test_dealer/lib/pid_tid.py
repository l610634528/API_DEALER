import unittest
import requests
import json
import sys
sys.path.append("..")  # 提升2级到项目根目录下
from config.config import *  # 从项目路径下导入
# from lib.read_excel import *  # 从项目路径下导入
# from lib.case_log import log_case_info  # 从项目路径下导入
import time

token, name, uid = dealer_login()
userid = str(uid)

# 获取pid和tid
url_task = 'http://test.cba.zcabc.com/act/list/task'
def get_pid_tid(self):
    data_pid_tid = json.dumps({
        "userId": self.userid,
        "page": 1,
        "size": 10,
        "actType": "sign",
        "perType": "cbapermission",
        "token": self.token
        })
    res = requests.post(url=self.url_task, data=data_pid_tid, headers=self.headers)
    res_text = json.loads(res.text)
    pid = res_text['data']['result']['records'][0]['processInstanceId']
    tid = res_text['data']['result']['records'][0]['task']['id']
    return pid, tid

if __name__ == '__main__':
    print("")