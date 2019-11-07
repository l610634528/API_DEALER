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
from lib.get_agentid import *
# from lib.get_detail import *
import time


# 总监1不同意
class TestSpecialPrice(unittest.TestCase):
    token, name, uid = dealer_login()
    userid = str(uid)
    # start_time = get_year_month_day()
    # finish_time = get_finish_year_month_day()
    url_info = dealer_url + '/cba/agentInfo/selectAgentInfoList'
    url_apply_save = dealer_url + '/cba/priceApply/save'
    url_list_task = dealer_url + '/act/list/task'
    url_product_info = dealer_url + '/cba/agentInfo/detail/sign/info'
    url_actFinish = dealer_url + '/cba/agentInfo/actFinish'
    url_finish = dealer_url + '/act/list/user/finished'
    agent_id = get_id()
    headers = {"Content-Type": "application/json"}

    # 获取申请所需信息
    def get_queryInfo(self):
        agent_id = self.agent_id
        data_info = json.dumps({
            "tag": 4,
            "userId": self.userid,
            "keyword": "",
            "companyId": "",
            "branchId": "",
            "orgId": "",
            "agentStatusParam": 8,
            "page": 1,
            "size": 100,
            "token": self.token
        })
        res = requests.post(url=self.url_info, data=data_info, headers=headers)
        res_text = json.loads(res.text)
        agentAbbr = []
        agentCode = []
        branchName = []
        branchCode = []
        orgName = []
        orgCode = []
        companyName = []
        for i in range(0, 100):
            if res_text['data']['result']['records'][i]['id'] == agent_id:
                agentAbbr.append(res_text['data']['result']['records'][i]['agentAbbr'])
                agentCode.append(res_text['data']['result']['records'][i]['agentCode'])
                branchName.append(res_text['data']['result']['records'][i]['branchName'])
                branchCode.append(res_text['data']['result']['records'][i]['branchCode'])
                orgName.append(res_text['data']['result']['records'][i]['orgName'])
                orgCode.append(res_text['data']['result']['records'][i]['orgCode'])
                companyName.append(res_text['data']['result']['records'][i]['companyName'])
                return agentAbbr, agentCode, branchName, orgName, companyName, branchCode, orgCode

    def get_productInfo(self):
        agent_id = self.agent_id
        data_info = json.dumps({
            "id": agent_id,
            "token": self.token
        })
        res = requests.post(url=self.url_product_info, data=data_info, headers=headers)
        res_text = json.loads(res.text)
        length = len(res_text['data']['result'])
        productName = []
        productDetail = []
        signproductId = []
        productColor = []
        productId = []
        if length == 0:
            productName.append("自定义")
            productDetail.append("自定义")
            signproductId.append("")
            productColor.append("白色")
            productId.append("0")
        else:
            for i in range(0, length):
                productName.append(res_text['data']['result'][i]['largeClassName'])
                productDetail.append(res_text['data']['result'][i]['typePrice'])
                signproductId.append(int(res_text['data']['result'][i]['id']))
                productColor.append(res_text['data']['result'][i]['color'])
                productId.append(int(res_text['data']['result'][i]['productId']))
        # print(productName, productDetail, signproductId, productColor, productId)
        return productName, productDetail, signproductId, productColor, productId

    # 特殊价格申请提交
    def test_a_special_submit(self):
        id_d = self.agent_id
        agentAbbr, agentCode, branchName, orgName, companyName, branchCode, orgCode = self.get_queryInfo()
        productName, productDetail, signproductId, productColor, productId = self.get_productInfo()
        data_save = json.dumps({
            "keys": [],
            "auditReason": "special_reason",
            "type": "3",
            "gross": "500",
            "controlDosage": "100",
            "projectName": "工程23",
            "projectAddress": "杭州滨江",
            "startTime": "2019-10-01",
            "endTime": "2019-10-31",
            "monthly": "全额",
            "monthlyOther": "全额",
            "annual": "全额",
            "annualOther": "全额",
            "rebate": "全额",
            "rebateOther": "全额",
            "other": "123",
            "applyReason": "特殊价格申请123",
            "productList": [{
                "productName": productName[0],
                "productDetail": productDetail[0],
                "signProductId": signproductId[0],
                "productColor": productColor[0],
                "price": "500",
                "productId": productId[0]
            }],
            "agentList": [{
                "agentId": id_d,
                "agentAbbr": agentAbbr[0],
                "agentCode": agentCode[0],
                "branchName": branchName[0],
                "orgName": orgName[0],
                "companyName": companyName[0],
                "branchCode": branchCode[0],
                "orgCode": orgCode[0],
                "gross": "500",
                "controlDosage": "100"
            }],
            "userName": self.name,
            "userId": self.userid,
            "token": self.token,
            "applyType": "1"
        })
        res = requests.post(url=self.url_apply_save, data=data_save, headers=self.headers)
        res_text = json.loads(res.text)
        res_result = res_text['data']['result']
        try:
            self.assertEqual(res_result, "操作成功！")
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 获取pid
    def get_act_data(self):
        id_d = self.agent_id
        data_pid = json.dumps({
            "userId": self.userid,
            "page": 1,
            "size": 100,
            "actType": "specialPrice",
            "searchType": "ower",
            "perType": "cbapermission",
            "token": self.token
        })
        res = requests.post(url=self.url_list_task, data=data_pid, headers=self.headers)
        res_text = json.loads(res.text)
        for i in range(0, 100):
            employeeId = int(res_text['data']['result']['records'][i]['employeeId'])
            if employeeId == id_d:
                return i

    def get_pid_tid(self):
        i = self.get_act_data()
        data_pid = json.dumps({
            "userId": self.userid,
            "page": 1,
            "size": 100,
            "actType": "specialPrice",
            "searchType": "ower",
            "perType": "cbapermission",
            "token": self.token
        })
        res = requests.post(url=self.url_list_task, data=data_pid, headers=self.headers)
        res_text = json.loads(res.text)
        pid = int(res_text['data']['result']['records'][i]['processInstanceId'])
        tid = int(res_text['data']['result']['records'][i]['task']['id'])
        uniqueid = int(res_text['data']['result']['records'][i]['uniqueId'])
        return pid, tid, uniqueid

    # 市场部同意
    def test_b_bazaar_agree(self):
        pid, tid, uniqueid = self.get_pid_tid()
        pid_d = str(pid)
        tid_d = str(tid)
        data_actFinish = json.dumps({
            "actType": "specialPrice",
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

        # 判断市场部同意是否成功
        data_finish = json.dumps({
            "userId": self.userid,
            "page": 1,
            "size": 10,
            "actType": "specialPrice",
            "perType": "cbapermission",
            "token": self.token
        })
        res_finish = requests.post(url=self.url_finish, data=data_finish, headers=self.headers)
        res_text = json.loads(res_finish.text)
        res_task_text = str(res_text['data']['result']['records'][0]['task']['name'])
        res_task_uniqueid = int(res_text['data']['result']['records'][0]['uniqueId'])
        try:
            self.assertEqual(res_task_text, '结算科操作员') and self.assertEqual(res_task_uniqueid, uniqueid)
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 结算科操作员初审同意
    def test_c_settlement(self):
        pid, tid, uniqueid = self.get_pid_tid()
        data_settl = json.dumps({
            "actType": "specialPrice",
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
            "actType": "specialPrice",
            "perType": "cbapermission",
            "token": self.token
        })
        res_task = requests.post(url=self.url_list_task, data=data_task, headers=self.headers)
        res_text = json.loads(res_task.text)
        res_task_text = str(res_text['data']['result']['records'][0]['task']['name'])
        res_task_uniqueid = int(res_text['data']['result']['records'][0]['uniqueId'])
        try:
            self.assertEqual(res_task_text, '结算科复核') and self.assertEqual(res_task_uniqueid, uniqueid)
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 结算科复核同意
    def test_d_settlement(self):
        pid, tid, uniqueid = self.get_pid_tid()
        data_agree = json.dumps({
            "actType": "specialPrice",
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
            "actType": "specialPrice",
            "perType": "cbapermission",
            "token": self.token
        })
        res_task = requests.post(url=self.url_list_task, data=data_task, headers=self.headers)
        res_text = json.loads(res_task.text)
        res_task_text = str(res_text['data']['result']['records'][0]['task']['name'])
        res_task_uniqueid = int(res_text['data']['result']['records'][0]['uniqueId'])
        try:
            self.assertEqual(res_task_text, '市场领导') and self.assertEqual(res_task_uniqueid, uniqueid)
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 市场部领导同意
    def test_e_market(self):
        pid, tid, uniqueid = self.get_pid_tid()
        data_market = json.dumps({
            "actType": "specialPrice",
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
            "actType": "specialPrice",
            "perType": "cbapermission",
            "token": self.token
        })
        res_task = requests.post(url=self.url_list_task, data=data_task, headers=self.headers)
        res_text = json.loads(res_task.text)
        res_task_text = str(res_text['data']['result']['records'][0]['task']['name'])
        res_task_uniqueid = int(res_text['data']['result']['records'][0]['uniqueId'])
        try:
            self.assertEqual(res_task_text, '结算科负责人') and self.assertEqual(res_task_uniqueid, uniqueid)
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 结算科负责人同意
    def test_f_principal(self):
        pid, tid, uniqueid = self.get_pid_tid()
        data_principal = json.dumps({
            "actType": "specialPrice",
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
            "actType": "specialPrice",
            "perType": "cbapermission",
            "token": self.token
        })
        res_task = requests.post(url=self.url_list_task, data=data_task, headers=self.headers)
        res_text = json.loads(res_task.text)
        res_task_text = str(res_text['data']['result']['records'][0]['task']['name'])
        res_task_uniqueid = int(res_text['data']['result']['records'][0]['uniqueId'])
        try:
            self.assertEqual(res_task_text, '总监1') and self.assertEqual(res_task_uniqueid, uniqueid)
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 总监1审核同意
    def test_g_majordomo(self):
        pid, tid, uniqueid = self.get_pid_tid()
        data_majordomo = json.dumps({
            "actType": "specialPrice",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "director1Pass,director1BackReason",
                "values": "true,同意_产品变更总监1通过",
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
            "actType": "specialPrice",
            "perType": "cbapermission",
            "token": self.token
        })
        res_finish = requests.post(url=self.url_finish, data=data_majordomo_finish, headers=self.headers)
        res_text = json.loads(res_finish.text)
        res_task_text = res_text['data']['result']['records'][0]['task']['name']
        res_task_uniqueid = int(res_text['data']['result']['records'][0]['uniqueId'])
        try:
            self.assertEqual(res_task_text, '总监2') and self.assertEqual(res_task_uniqueid, uniqueid)
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 总监2审核同意
    def test_h_majordomo(self):
        pid, tid, uniqueid = self.get_pid_tid()
        data_majordomo = json.dumps({
            "actType": "specialPrice",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "director2Pass,director2BackReason",
                "values": "N,不同意_总监2不同意",
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
            "actType": "specialPrice",
            "perType": "cbapermission",
            "token": self.token
        })
        res_finish = requests.post(url=self.url_finish, data=data_majordomo_finish, headers=self.headers)
        res_text = json.loads(res_finish.text)
        res_task_text = res_text['data']['result']['records'][0]['task']['name']
        res_task_uniqueid = int(res_text['data']['result']['records'][0]['uniqueId'])
        try:
            self.assertEqual(res_task_text, '结算科负责人') and self.assertEqual(res_task_uniqueid, uniqueid)
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 结算科负责人同意
    def test_i_principal(self):
        pid, tid, uniqueid = self.get_pid_tid()
        data_principal = json.dumps({
            "actType": "specialPrice",
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
            "actType": "specialPrice",
            "perType": "cbapermission",
            "token": self.token
        })
        res_task = requests.post(url=self.url_list_task, data=data_task, headers=self.headers)
        res_text = json.loads(res_task.text)
        res_task_text = str(res_text['data']['result']['records'][0]['task']['name'])
        res_task_uniqueid = int(res_text['data']['result']['records'][0]['uniqueId'])
        try:
            self.assertEqual(res_task_text, '总监1') and self.assertEqual(res_task_uniqueid, uniqueid)
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 总监1审核同意
    def test_j_majordomo(self):
        pid, tid, uniqueid = self.get_pid_tid()
        data_majordomo = json.dumps({
            "actType": "specialPrice",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "director1Pass,director1BackReason",
                "values": "true,同意_产品变更总监1通过",
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
            "actType": "specialPrice",
            "perType": "cbapermission",
            "token": self.token
        })
        res_finish = requests.post(url=self.url_finish, data=data_majordomo_finish, headers=self.headers)
        res_text = json.loads(res_finish.text)
        res_task_text = res_text['data']['result']['records'][0]['task']['name']
        res_task_uniqueid = int(res_text['data']['result']['records'][0]['uniqueId'])
        try:
            self.assertEqual(res_task_text, '总监2') and self.assertEqual(res_task_uniqueid, uniqueid)
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 总监2审核同意
    def test_k_majordomo(self):
        pid, tid, uniqueid = self.get_pid_tid()
        data_majordomo = json.dumps({
            "actType": "specialPrice",
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
            "actType": "specialPrice",
            "perType": "cbapermission",
            "token": self.token
        })
        res_finish = requests.post(url=self.url_finish, data=data_majordomo_finish, headers=self.headers)
        res_text = json.loads(res_finish.text)
        res_processType = res_text['data']['result']['records'][0]['processType']
        res_task_uniqueid = int(res_text['data']['result']['records'][0]['uniqueId'])
        try:
            self.assertEqual(res_processType, '2') and self.assertEqual(res_task_uniqueid, uniqueid)
        except Exception as e:
            print('Assertion test fail.', format(e))


if __name__ == '__main__':
    unittest.main(verbosity=2)