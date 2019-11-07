import unittest
import requests
import json
import sys

sys.path.append("../..")  # 提升2级到项目根目录下
from config.config import *  # 从项目路径下导入
from lib.read_excel import *  # 从项目路径下导入
from lib.dealer_login_token import *
import time
from lib.get_renew import *


class TestRenew(unittest.TestCase):
    token, name, uid, = dealer_login()
    userid = str(uid)
    time.sleep(5)
    headers = {"Content-Type": "application/json"}
    url_info = dealer_url + '/cba/agentInfo/selectAgentInfoList'
    url_continueSubmit = dealer_url + '/cba/agentInfo/continueSubmit'
    url_actfinish = dealer_url + '/cba/agentInfo/actFinish'
    url_update = dealer_url + '/cba/agentInfo/updateStatus'
    url_task = dealer_url + '/act/list/task'
    empid = get_a_resultid()

    # 续签市场部提交
    def test_a_market_submit(self):
        # empid = self.get_a_resultid()
        # print(empid)
        data_update = json.dumps({
            "id": self.empid,
            "userId": self.userid,
            "userName": self.name,
            "agentStatus": "5",
            "token": self.token
        })
        res = requests.post(url=self.url_update, data=data_update, headers=self.headers)
        res_text = json.loads(res.text)
        res_subcode = int(res_text['data']['subCode'])
        try:
            self.assertEqual(res_subcode, 10000)
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 获取pid和tid
    def get_pid_tid(self):
        data_pid_tid = json.dumps({
            "userId": self.userid,
            "page": 1,
            "size": 100,
            "actType": "sign",
            "perType": "cbapermission",
            "token": self.token
        })
        res = requests.post(url=self.url_task, data=data_pid_tid, headers=self.headers)
        res_text = json.loads(res.text)
        pid = res_text['data']['result']['records'][0]['processInstanceId']
        tid = res_text['data']['result']['records'][0]['task']['id']
        return pid, tid

    # 结算科初审同意
    def test_b_first_trial_agree(self):
        pid, tid = self.get_pid_tid()
        data_act = json.dumps({
            "actType": "sign",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "settlementOprPass,settlementOprBackReason",
                "values": "true,同意_1初审同意",
                "types": "B,S"
            },
            "token": self.token
        })
        res = requests.post(url=self.url_actfinish, data=data_act, headers=self.headers)
        res_text = json.loads(res.text)
        res_reason = res_text['data']['result']['reason']
        try:
            self.assertEqual(res_reason, 'settlementReviewAudit')
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 结算科复审
    def test_c_recheck_agree(self):
        pid, tid = self.get_pid_tid()
        data_act = json.dumps({
            "actType": "sign",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "settlementReviewPass,settlementReviewBackReason",
                "values": "true,同意_2复核通过",
                "types": "B,S"
            },
            "token": self.token
        })
        res = requests.post(url=self.url_actfinish, data=data_act, headers=self.headers)
        res_text = json.loads(res.text)
        res_reason = res_text['data']['result']['reason']
        try:
            self.assertEqual(res_reason, 'maketLeaderAudit')
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 市场部审核同意
    def test_d_market_leader_agree(self):
        pid, tid = self.get_pid_tid()
        data_market = json.dumps({
            "actType": "sign",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "maketLeaderPass,maketLeaderBackReason",
                "values": "true,同意_3市场部同意",
                "types": "B,S"
            },
            "fileIds": "2738",
            "token": self.token
        })
        res = requests.post(url=self.url_actfinish, data=data_market, headers=self.headers)
        res_text = json.loads(res.text)
        res_reason = res_text['data']['result']['reason']
        try:
            self.assertEqual(res_reason, 'settlementLeaderAudit')
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 结算科负责人审核同意
    def test_e_principal_agree(self):
        pid, tid = self.get_pid_tid()
        data_principal = json.dumps({
            "actType": "sign",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "settlementLeaderPass,settlementLeaderBackReason",
                "values": "true,同意_4结算科负责人",
                "types": "B,S"
            },
            "token": self.token
        })
        res = requests.post(url=self.url_actfinish, data=data_principal, headers=self.headers)
        res_text = json.loads(res.text)
        res_reason = res_text['data']['result']['reason']
        try:
            self.assertEqual(res_reason, 'director1Audit')
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 总监1审核通过
    def test_f_leader_one_agree(self):
        pid, tid = self.get_pid_tid()
        data_majordomo = json.dumps({
            "actType": "sign",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "director1Pass,director1BackReason",
                "values": "true,同意_5总监1",
                "types": "B,S"
            },
            "fileIds": "2739",
            "token": self.token
        })
        res = requests.post(url=self.url_actfinish, data=data_majordomo, headers=self.headers)
        res_text = json.loads(res.text)
        res_reason = res_text['data']['result']['reason']
        try:
            self.assertEqual(res_reason, 'director2Audit')
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 总监2审核通过
    def test_g_leader_two_agree(self):
        pid, tid = self.get_pid_tid()
        data_majordomo2 = json.dumps({
            "actType": "sign",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "director2Pass,director2BackReason",
                "values": "continue,同意_续签流程总监2审批",
                "types": "S,S"
            },
            "fileIds": "",
            "token": self.token
        })
        res = requests.post(url=self.url_actfinish, data=data_majordomo2, headers=self.headers)
        res_text = json.loads(res.text)
        res_code = res_text['data']['subCode']
        try:
            self.assertEqual(res_code, 10000)
        except Exception as e:
            print('Assertion test fail.', format(e))


if __name__ == '__main__':
    unittest.main(verbosity=2)
