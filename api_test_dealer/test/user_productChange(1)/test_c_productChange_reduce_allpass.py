import unittest
import requests
import json
import sys
# sys.path.append("../..")  # 提升2级到项目根目录下
from config.config import *  # 从项目路径下导入
from lib.read_excel import *  # 从项目路径下导入
from lib.dealer_login_token import *
from lib.get_agentid import *
import time


# 已开户产品变更全部同意
class TestAdditional(unittest.TestCase):
    token, name, uid, = dealer_login()
    userid = str(uid)
    agent_id = get_id()
    time.sleep(5)
    headers = {"Content-Type": "application/json"}
    url_info = dealer_url + '/cba/agentInfo/selectAgentInfoList'
    url_user_finish = dealer_url + '/act/list/user/finished'
    url_query = dealer_url + '/cba/contract/change/query'
    url_apply = dealer_url + '/cba/contract/change/apply'
    url_list_task = dealer_url + '/act/list/task'
    url_actFinish = dealer_url + '/cba/agentInfo/actFinish'
    url_finish = dealer_url + '/act/list/user/finished'

    # 产品变更获取地址和产品id
    def get_queryInfo(self, agent_id):
        data_query = json.dumps({
            "agentId": agent_id,
            "justLook": "0",
            "token": self.token
        })
        res = requests.post(url=self.url_query, data=data_query, headers=self.headers)
        res_text = json.loads(res.text)
        # startData = res_text['data']['result']['contractStartDate']
        # contractEndDate = res_text['data']['result']['contractEndDate']
        businessAreaRemark = res_text['data']['result']['businessAreaRemark']
        businessChannel = res_text['data']['result']['businessChannel']
        length_area = len(res_text['data']['result']['serviceAreasList'])
        address_id = []
        areaIds = []
        for i in range(0, length_area):
            address_id.append(int(res_text['data']['result']['serviceAreasList'][i]['id']))
            areaIds.append(res_text['data']['result']['serviceAreasList'][i]['areaIds'])
        length_signinfo = len(res_text['data']['result']['signInfoList'])
        signinfo_id = []
        signproduct_id = [[] for count in range(10)]
        baseNumber1 = []
        baseNumber2 = []
        baseNumber3 = []
        discount1 = []
        discount2 = []
        discount3 = []
        largeClassId = []
        largeClassName = []
        for i in range(0, length_signinfo):
            signinfo_id.append(int(res_text['data']['result']['signInfoList'][i]['id']))
            baseNumber1.append(res_text['data']['result']['signInfoList'][i]['baseNumber1'])
            baseNumber2.append(res_text['data']['result']['signInfoList'][i]['baseNumber2'])
            baseNumber3.append(res_text['data']['result']['signInfoList'][i]['baseNumber3'])
            discount1.append(res_text['data']['result']['signInfoList'][i]['discount1'])
            discount2.append(res_text['data']['result']['signInfoList'][i]['discount2'])
            discount3.append(res_text['data']['result']['signInfoList'][i]['discount3'])
            largeClassId.append(int(res_text['data']['result']['signInfoList'][i]['largeClassId']))
            largeClassName.append(res_text['data']['result']['signInfoList'][i]['largeClassName'])
            length_signproduct = len(res_text['data']['result']['signInfoList'][i]['signProductList'])
            for j in range(0, length_signproduct):
                signproduct_id[i].append(res_text['data']['result']['signInfoList'][i]['signProductList'][j]['id'])
        length_salesResolve = len(res_text['data']['result']['salesResolveList'])
        salesResolve_id = []
        for k in range(0, length_salesResolve):
            salesResolve_id.append(int(res_text['data']['result']['salesResolveList'][k]['id']))
        return businessAreaRemark, businessChannel, address_id, areaIds, signinfo_id, \
               signproduct_id, salesResolve_id, baseNumber1, baseNumber2, baseNumber3, discount1, discount2, discount3, \
               largeClassId, largeClassName, length_salesResolve

    # 产品变更提交
    def test_a_apply(self):
        id_d = self.agent_id
        businessAreaRemark, businessChannel, address_id, areaIds, signinfo_id, \
        signproduct_id, salesResolve_id, baseNumber1, baseNumber2, baseNumber3, discount1, discount2, discount3, \
        largeClassId, largeClassName, length_salesResolve = self.get_queryInfo(id_d)
        salesResolve_dic = {"id": "", "agentId": id_d, "largeClassId": 6, "largeClassName": "PE", "month": "",
                            "sales": 1}
        salesResolveList = []
        for i in range(0, length_salesResolve):
            if (i + 1) % 12 == 0:
                month = 12
            else:
                month = (i + 1) % 12
            for key in salesResolve_dic.keys():
                if key == "id":
                    salesResolve_dic[key] = salesResolve_id[i]
                elif key == "month":
                    salesResolve_dic[key] = month
            salesResolveList.append(salesResolve_dic.copy())

        serviceAreas_dic = {"id": "", "agentId": id_d, "areaIds": "", "areaNames": "西城区", "cityId": "2",
                            "city": "北京", "provinceId": "1", "province": "北京"}
        serviceAreasList = []
        length_serviceAreas = len(address_id)
        for Areas in range(0, length_serviceAreas):
            for key_areas in serviceAreas_dic.keys():
                if key_areas == "id":
                    serviceAreas_dic[key_areas] = address_id[Areas]
                elif key_areas == "areaIds":
                    serviceAreas_dic[key_areas] = areaIds[Areas]
            serviceAreasList.append(serviceAreas_dic)

        signProductList = [[] for count in range(10)]
        signInfoList = []
        signProductList_dic = {"agentId": id_d, "id": "", "productId": 138, "largeClassId": 6, "classify": "1",
                               "color": "产品色", "downPoints": "1", "typePrice": "PE双壁波纹管件", "enabled": 1}
        length_signinfo = len(signinfo_id)
        for l in range(0, length_signinfo):
            for m in range(0, len(signproduct_id[l])):
                for key_pro in signProductList_dic.keys():
                    if key_pro == "id":
                        signProductList_dic[key_pro] = signproduct_id[l][m]
                        signProductList[l].append(signProductList_dic)
            signInfoList_dic = {"id": "", "agentId": id_d, "baseNumber1": "", "baseNumber2": "", "baseNumber3": "",
                                "discount1": "", "discount2": "", "discount3": "", "largeClassId": "",
                                "largeClassName": "", "signProductList": signProductList[l]}
            for key_info in signInfoList_dic.keys():
                if key_info == "id":
                    signInfoList_dic[key_info] = signinfo_id[l]
                elif key_info == "baseNumber1":
                    signInfoList_dic[key_info] = baseNumber1[l]
                elif key_info == "baseNumber2":
                    signInfoList_dic[key_info] = baseNumber2[l]
                elif key_info == "baseNumber3":
                    signInfoList_dic[key_info] = baseNumber3[l]
                elif key_info == "discount1":
                    signInfoList_dic[key_info] = discount1[l]
                elif key_info == "discount1":
                    signInfoList_dic[key_info] = discount2[l]
                elif key_info == "discount3":
                    signInfoList_dic[key_info] = discount3[l]
                elif key_info == "largeClassId":
                    signInfoList_dic[key_info] = largeClassId[l]
                elif key_info == "largeClassName":
                    signInfoList_dic[key_info] = largeClassName[l]
            signInfoList.append(signInfoList_dic)

        if length_signinfo > 1:
            signInfoList[length_signinfo - 1]['signProductList'][0]['enabled'] = 2
        else:
            print("请选择具有一个以上产品的经销商！")

        data_apply = json.dumps({
            "userId": self.userid,
            "userName": self.name,
            "agentId": id_d,
            "contractChangeType": "2",
            "serviceAreasList": serviceAreasList,
            "businessChannel": businessChannel,
            "businessAreaRemark": businessAreaRemark,
            "signInfoList": signInfoList,
            "salesResolveList": [],
            "firstOrderNum": "",
            "signLargeCalssAdded": "",
            "authPeriodStart": "",
            "authPeriodEnd": "",
            "contractChangeRemark": "减少产品",
            "token": self.token})
        res = requests.post(url=self.url_apply, data=data_apply, headers=self.headers)
        res_text = json.loads(res.text)
        try:
            self.assertEqual(res_text['data']['result'], '申请成功')
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 补充备案获取pid
    def get_act_data(self):
        id_d = self.agent_id
        data_pid = json.dumps({
            "userId": self.userid,
            "page": 1,
            "size": 100,
            "actType": "productChange",
            "perType": "cbapermission",
            "token": self.token
        })
        res = requests.post(url=self.url_list_task, data=data_pid, headers=self.headers)
        res_text = json.loads(res.text)
        for i in range(0, 100):
            uniqueid = res_text['data']['result']['records'][i]['uniqueId']
            if uniqueid == id_d:
                return i

    def get_pid_tid(self):
        i = self.get_act_data()
        data_pid = json.dumps({
            "userId": self.userid,
            "page": 1,
            "size": 100,
            "actType": "productChange",
            "perType": "cbapermission",
            "token": self.token
        })
        res = requests.post(url=self.url_list_task, data=data_pid, headers=self.headers)
        res_text = json.loads(res.text)
        pid = int(res_text['data']['result']['records'][i]['processInstanceId'])
        tid = int(res_text['data']['result']['records'][i]['task']['id'])
        uniqueid = res_text['data']['result']['records'][i]['uniqueId']
        return pid, tid, uniqueid

    # 市场部同意
    def test_b_market_agree(self):
        pid, tid, uniqueid = self.get_pid_tid()
        pid_d = str(pid)
        tid_d = str(tid)
        data_actFinish = json.dumps({
            "actType": "productChange",
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
            "actType": "productChange",
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
    def test_c_settlement_agree(self):
        pid, tid, uniqueid = self.get_pid_tid()
        data_settl = json.dumps({
            "actType": "productChange",
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
            "actType": "productChange",
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
    def test_d_settlementReview_agree(self):
        pid, tid, uniqueid = self.get_pid_tid()
        data_agree = json.dumps({
            "actType": "productChange",
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
            "actType": "productChange",
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
    def test_e_marketLeader_agree(self):
        pid, tid, uniqueid = self.get_pid_tid()
        data_market = json.dumps({
            "actType": "productChange",
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
            "actType": "productChange",
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
    def test_f_settlementLeader_agree(self):
        pid, tid, uniqueid = self.get_pid_tid()
        data_principal = json.dumps({
            "actType": "productChange",
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
            "actType": "productChange",
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
    def test_g_direct1_agree(self):
        pid, tid, uniqueid = self.get_pid_tid()
        data_majordomo = json.dumps({
            "actType": "productChange",
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
            "actType": "productChange",
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
    def test_h_direct2_agree(self):
        pid, tid, uniqueid = self.get_pid_tid()
        data_majordomo = json.dumps({
            "actType": "productChange",
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
            "actType": "productChange",
            "perType": "cbapermission",
            "token": self.token
        })
        res_finish = requests.post(url=self.url_finish, data=data_majordomo_finish, headers=self.headers)
        res_text = json.loads(res_finish.text)
        res_processType = res_text['data']['result']['records'][0]['processType']
        res_task_uniqueid = int(res_text['data']['result']['records'][0]['uniqueId'])
        try:
            self.assertEqual(res_processType, '1') and self.assertEqual(res_task_uniqueid, uniqueid)
        except Exception as e:
            print('Assertion test fail.', format(e))


if __name__ == '__main__':
    unittest.main(verbosity=2)