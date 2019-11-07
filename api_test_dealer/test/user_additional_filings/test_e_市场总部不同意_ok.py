import unittest
import requests
import json
import sys
sys.path.append("../..")  # 提升2级到项目根目录下
# from config.config import *  # 从项目路径下导入
# from lib.read_excel import *  # 从项目路径下导入
# from lib.dealer_login_token import *
from config.config import *  # 从项目路径下导入
from lib.read_excel import *  # 从项目路径下导入
from lib.dealer_login_token import *
import time

# 已开户经销商补充备案市场总部领导不同意继续审核通过
class TestAdditional(unittest.TestCase):
    token, name, uid, = dealer_login()
    userid = str(uid)
    time.sleep(5)
    headers = {"Content-Type":"application/json"}

    # 获取已开户列表第一条数据id
    url_info = dealer_url + '/cba/agentInfo/selectAgentInfoList'
    url_user_finish = dealer_url + '/act/list/user/finished'
    @classmethod
    def setUpClass(cls):
        print('=== setUpModule ===')
        cls.data_list = excel_to_list(os.path.join(data_path, "test_dealer_data.xlsx"), "agentInfo_basesave")  
        # cls.data_list 同 self.data_list 都是该类的公共属性
    @classmethod
    def tearDownModule(cls): # 当前模块执行后只执行一次
        print('=== tearDownModule ===')
    def get_name(self):
        data_user_finish = json.dumps({
            "userId": self.userid,
            "page": 1,
            "actType": "sign",
            "perType": "cbapermission",
            "token": self.token
                })
        res = requests.post(url=self.url_user_finish, data=data_user_finish, headers=self.headers)
        res_text = json.loads(res.text)
        res_name = res_text['data']['result']['records'][0]['name']
        return res_name

    def get_id(self):
        keyword = self.get_name()
        data_info = json.dumps({
            "tag": 4,
            "userId": self.userid,
            "keyword": keyword,
            "companyId": "",
            "branchId": "",
            "orgId": "",
            "agentStatusParam": 8,
            "page": 1,
            "size": 10,
            "token": self.token
                })
        res = requests.post(url=self.url_info, data=data_info, headers=self.headers)
        res_text = json.loads(res.text)
        for i in range(0, 10):
            if res_text['data']['result']['records'][i]['agentStatusText'] == '已开户':
                agent_id = int(res_text['data']['result']['records'][0]['id'])
                return agent_id

    # 补充备案取id
    url_query = dealer_url + '/cba/supplement/filing/query'
    def get_additional_id(self):
        id_d = self.get_id()
        data_query = json.dumps({
            "agentId": id_d,
            "justLook": "0",
            "token": self.token
            })
        res = requests.post(url=self.url_query, data=data_query, headers=self.headers)
        res_text = json.loads(res.text)
        res_id = int(res_text['data']['result']['reciverAddressList'][0]['id'])
        return res_id

    # 补充备案提交
    url_apply = dealer_url + '/cba/supplement/filing/apply'
    def test_a_补充备案提交(self):
        query_id = self.get_additional_id()
        id_d = self.get_id()
        data_apply = json.dumps({
            "userId": self.userid,
            "userName": "吕结算科",
            "agentId": id_d,
            "supplementFiling": "2773",
            "reciverAddressList": [{
                "id": query_id,
                "address": "123",
                "type": 1,
                "agentId": id_d,
                "enabled": 1,
                "acceptor": "吕",
                "remark": "123",
                "phoneNum": "15067126937",
                "area": "峰峰矿区",
                "areaId": "88",
                "city": "邯郸市",
                "cityId": "84",
                "province": "河北省",
                "provinceId": "37"
            }],
            "paymentWay": "1,3",
            "thirdPaymentList": [],
            "personalPaymentList": [{
                "idCard": "330327199311122878",
                "idCardAttach": "2772",
                "id": "",
                "agentId": id_d,
                "effectiveDate": "2019-10-14",
                "enabled": 1,
                "name": "自然人开款",
                "reasons": "852",
                "effectiveDateEnd": "2019-12-31"
                }],
            "token": self.token
            })
        res = requests.post(url=self.url_apply, data=data_apply, headers=self.headers)
        res_text = json.loads(res.text)
        try:
            self.assertEqual(res_text['data']['result'], '申请成功')
        except Exception as e:
            print('Assertion test fail.', format(e))


    def test_b_提交后状态判断(self):
        keyword = self.get_name()
        data_info = json.dumps({
            "tag": 4,
            "userId": self.userid,
            "keyword": keyword,
            "companyId": "",
            "branchId": "",
            "orgId": "",
            "agentStatusParam": 8,
            "page": 1,
            "size": 10,
            "token": self.token
            })
        res = requests.post(url=self.url_info, data=data_info, headers=self.headers)
        res_text = json.loads(res.text)
        try:
            self.assertEqual(res_text['data']['result']['records'][0]['agentStatusText'], '补充备案审核中')
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 补充备案获取pid
    url_list_task = dealer_url + '/act/list/task'
    def get_pid_tid(self):
        data_pid = json.dumps({
            "userId": self.userid,
            "page": 1,
            "size": 10,
            "actType": "supplement",
            "perType": "cbapermission",
            "token": self.token
                })
        res = requests.post(url=self.url_list_task, data=data_pid, headers=self.headers)
        res_text = json.loads(res.text)
        pid = int(res_text['data']['result']['records'][0]['processInstanceId'])
        tid = int(res_text['data']['result']['records'][0]['task']['id'])
        return pid, tid

    # 市场部同意
    url_actFinish = dealer_url + '/cba/agentInfo/actFinish'
    url_finish = dealer_url + '/act/list/user/finished'
    def test_c_市场部同意(self):
        pid, tid = self.get_pid_tid()
        pid_d = str(pid)
        tid_d = str(tid)
        data_actFinish = json.dumps({
            "actType": "supplement",
            "userId": self.userid,
            "pId": pid_d,
            "taskId": tid_d,
            "var": {
                "keys": "managerReviewPass,managerReviewBackReason",
                "values": "true,同意_",
                "types": "B,S"
                },
            "token": self.token
            })
        res = requests.post(url=self.url_actFinish, data=data_actFinish, headers=self.headers)

        # 判断市场部同意是否成立
        
        data_finish = json.dumps({
            "userId": self.userid,
            "page": 1,
            "size": 10,
            "actType": "supplement",
            "perType": "cbapermission",
            "searchType": "ower",
            "token": self.token
            })
        res_finish = requests.post(url=self.url_finish, data=data_finish, headers=self.headers)
        res_text = json.loads(res_finish.text)
        try:
            self.assertEqual(res_text['data']['result']['records'][0]['task']['name'], '结算科操作员')
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 结算科操作员初审同意  
    def test_d_初审同意(self):
        pid, tid = self.get_pid_tid()
        data_settl = json.dumps({
            "actType": "supplement",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "settlementOprPass,settlementOprBackReason",
                "values": "true,同意_同意",
                "types": "B,S"
                },
            "token": self.token
            })
        res = requests.post(url=self.url_actFinish, data=data_settl, headers=self.headers)
        data_task = json.dumps({
            "userId": self.userid,
            "page": 1,
            "size": 10,
            "actType": "supplement",
            "perType": "cbapermission",
            "token": self.token
            })
        res_task = requests.post(url=self.url_list_task, data=data_task, headers=self.headers)
        res_text = json.loads(res_task.text)
        res_task_text = str(res_text['data']['result']['records'][0]['task']['name'])
        try:
            self.assertEqual(res_task_text, '结算科复核')
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 结算科复核同意
    def test_e_复审同意(self):
        pid, tid = self.get_pid_tid()
        data_agree = json.dumps({
            "actType": "supplement",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "settlementReviewPass,settlementReviewBackReason",
                "values": "true,同意_2312",
                "types": "B,S"
                },
            "token": self.token
            })
        res = requests.post(url=self.url_actFinish, data=data_agree, headers=self.headers)
        data_task = json.dumps({
            "userId": self.userid,
            "page": 1,
            "size": 10,
            "actType": "supplement",
            "perType": "cbapermission",
            "token": self.token
            })
        res_task = requests.post(url=self.url_list_task, data=data_task, headers=self.headers)
        res_text = json.loads(res_task.text)
        res_task_text = str(res_text['data']['result']['records'][0]['task']['name'])
        try:
            self.assertEqual(res_task_text, '市场领导')
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 市场部领导不同意
    def test_f_市场部不同意(self):
        pid, tid = self.get_pid_tid()
        data_market = json.dumps({
            "actType": "supplement",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "maketLeaderPass,maketLeaderBackReason",
                "values": "false,同意_123",
                "types": "B,S"
                },
            "fileIds": "2776",
            "token": self.token
            })
        res = requests.post(url=self.url_actFinish, data=data_market, headers=self.headers)

    # 结算科初审再次同意
    def test_g_初审再次同意(self):
        pid, tid = self.get_pid_tid()
        data_settl = json.dumps({
            "actType": "supplement",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "settlementOprPass,settlementOprBackReason",
                "values": "true,同意_同意",
                "types": "B,S"
                },
            "token": self.token
            })
        res = requests.post(url=self.url_actFinish, data=data_settl, headers=self.headers)
        data_task = json.dumps({
            "userId": self.userid,
            "page": 1,
            "size": 10,
            "actType": "supplement",
            "perType": "cbapermission",
            "token": self.token
            })
        res_task = requests.post(url=self.url_list_task, data=data_task, headers=self.headers)
        res_text = json.loads(res_task.text)
        res_task_text = str(res_text['data']['result']['records'][0]['task']['name'])
        try:
            self.assertEqual(res_task_text, '结算科复核')
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 结算科复审再次同意
    def test_h_复审再次同意(self):
        pid, tid = self.get_pid_tid()
        data_agree = json.dumps({
            "actType": "supplement",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "settlementReviewPass,settlementReviewBackReason",
                "values": "true,同意_2312",
                "types": "B,S"
                },
            "token": self.token
            })
        res = requests.post(url=self.url_actFinish, data=data_agree, headers=self.headers)
        data_task = json.dumps({
            "userId": self.userid,
            "page": 1,
            "size": 10,
            "actType": "supplement",
            "perType": "cbapermission",
            "token": self.token
            })
        res_task = requests.post(url=self.url_list_task, data=data_task, headers=self.headers)
        res_text = json.loads(res_task.text)
        res_task_text = str(res_text['data']['result']['records'][0]['task']['name'])
        try:
            self.assertEqual(res_task_text, '市场领导')
        except Exception as e:
            print('Assertion test fail.', format(e))   

    # 市场部领导再次审核同意
    def test_i_市场部领导再次同意(self):
        pid, tid = self.get_pid_tid()
        data_market = json.dumps({
            "actType": "supplement",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "maketLeaderPass,maketLeaderBackReason",
                "values": "true,同意_123",
                "types": "B,S"
                },
            "fileIds": "2776",
            "token": self.token
            })
        res = requests.post(url=self.url_actFinish, data=data_market, headers=self.headers)
        data_task = json.dumps({
            "userId": self.userid,
            "page": 1,
            "size": 10,
            "actType": "supplement",
            "perType": "cbapermission",
            "token": self.token
            })
        res_task = requests.post(url=self.url_list_task, data=data_task, headers=self.headers)
        res_text = json.loads(res_task.text)
        res_task_text = str(res_text['data']['result']['records'][0]['task']['name'])
        try:
            self.assertEqual(res_task_text, '结算科负责人')
        except Exception as e:
            print('Assertion test fail.', format(e))
        
    # 结算科负责人同意
    def test_j_负责人同意(self):
        pid, tid = self.get_pid_tid()
        data_principal = json.dumps({
            "actType": "supplement",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "settlementLeaderPass,settlementLeaderBackReason",
                "values": "true,同意_1015",
                "types": "B,S"
                },
            "token": self.token
            })
        res = requests.post(url=self.url_actFinish, data=data_principal, headers=self.headers)
        data_task = json.dumps({
            "userId": self.userid,
            "page": 1,
            "size": 10,
            "actType": "supplement",
            "perType": "cbapermission",
            "token": self.token
            })
        res_task = requests.post(url=self.url_list_task, data=data_task, headers=self.headers)
        res_text = json.loads(res_task.text)
        res_task_text = str(res_text['data']['result']['records'][0]['task']['name'])
        try:
            self.assertEqual(res_task_text, '总监2')
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 总监2审核同意
    def test_k_总监2同意(self):
        pid, tid = self.get_pid_tid()
        data_majordomo = json.dumps({
            "actType": "supplement",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "director2Pass,director2BackReason",
                "values": "Y,同意_总监2同意",
                "types": "B,S"
                },
            "fileIds": "2777",
            "token": self.token
            })
        res = requests.post(url=self.url_actFinish, data=data_majordomo, headers=self.headers)
        data_majordomo_finish = json.dumps({
            "userId": self.userid,
            "page": 1,
            "size": 10,
            "actType": "supplement",
            "perType": "cbapermission",
            "token": self.token
            })
        res_finish = requests.post(url=self.url_finish, data=data_majordomo_finish, headers=self.headers)
        res_text = json.loads(res_finish.text)
        res_processType = res_text['data']['result']['records'][0]['processType']
        try:
            self.assertEqual(res_processType, '1')
        except Exception as e:
            print('Assertion test fail.', format(e))

if __name__ == '__main__':
    unittest.main(verbosity=2)