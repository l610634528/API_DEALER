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
    a = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    headers = {"Content-Type": "application/json"}
    url_info = dealer_url + '/cba/agentInfo/selectAgentInfoList'
    url_user_finish = dealer_url + '/act/list/user/finished'
    url_list_task = dealer_url + '/act/list/task'
    url_actFinish = dealer_url + '/cba/agentInfo/actFinish'
    url_finish = dealer_url + '/act/list/user/finished'
    url_query = dealer_url + '/cba/contract/change/query'
    url_apply = dealer_url + '/cba/contract/change/apply'

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

        signInfoList_dic_add1 = {
            "id": "", "agentId": id_d, "baseNumber1": "1", "baseNumber2": "", "baseNumber3": "", "discount1": "1",
            "discount2": "", "discount3": "", "largeClassId": 1, "largeClassName": "PVC",
            "signProductList": [{"agentId": id_d, "id": "", "productId": 61, "largeClassId": 1, "classify": 1,
                                "color": "中国红", "downPoints": "1", "typePrice": "精装专供电工套管管件（中国红）",
                                "enabled": ""}]}

        signInfoList_dic_add2 = {
            "id": "", "agentId": id_d, "baseNumber1": "1", "baseNumber2": "", "baseNumber3": "",  "discount1": "1",
            "discount2": "", "discount3": "", "largeClassId": 2, "largeClassName": "Z-HOME",
            "signProductList": [{"agentId": id_d, "id": "", "productId": 1, "largeClassId": 2, "classify": 2,
                                   "color": "外橘红内白", "downPoints": "1", "typePrice": "Z-HOME-PPR复合管材（耐冻系列）",
                                   "enabled": ""}]}

        signInfoList_dic_add3 = {
            "id": "", "agentId": id_d, "baseNumber1": "1", "baseNumber2": "", "baseNumber3": "", "discount1": "1",
            "discount2": "", "discount3": "", "largeClassId": 4, "largeClassName": "PE-RT",
            "signProductList": [{"agentId": id_d, "id": "", "productId": 120, "largeClassId": 4, "classify": 2,
                                   "color": "玛瑙红", "downPoints": "1", "typePrice": "PE-RT家装地暖专用管材-玛瑙红",
                                   "enabled": ""}]}

        signInfoList_dic_add4 = {
            "id": "", "agentId": id_d, "baseNumber1": "1", "baseNumber2": "", "baseNumber3": "", "discount1": "1",
            "discount2": "", "discount3": "", "largeClassId": 3, "largeClassName": "PPR",
            "signProductList": [{"agentId": id_d, "id": "", "productId": 39, "largeClassId": 3, "classify": 1,
                                   "color": "咖喱色", "downPoints": "1", "typePrice": "PPR全塑管件-咖喱色",
                                   "enabled": ""}]}

        signInfoList_dic_add_list = [signInfoList_dic_add1, signInfoList_dic_add2, signInfoList_dic_add3,
                                     signInfoList_dic_add4]

        salesResolve_dic_add1 = {"id": "", "agentId": id_d, "largeClassId": "1", "largeClassName": "PVC", "month": "",
                                "sales": 1}
        salesResolve_dic_add2 = {"id": "", "agentId": id_d, "largeClassId": "2", "largeClassName": "Z-HOME", "month": "",
                                "sales": 1}
        salesResolve_dic_add3 = {"id": "", "agentId": id_d, "largeClassId": "4", "largeClassName": "PE-RT", "month": "",
                                "sales": 1}
        salesResolve_dic_add4 = {"id": "", "agentId": id_d, "largeClassId": "3", "largeClassName": "PPR", "month": "",
                                "sales": 1}
        salesResolve_dic_add_list = [salesResolve_dic_add1, salesResolve_dic_add2, salesResolve_dic_add3, salesResolve_dic_add4]

        add = 0
        signInfoList_length = 0
        while add < 4:
            if signInfoList_length < length_signinfo:
                if signInfoList_dic_add_list[add]['largeClassId'] == signInfoList[signInfoList_length]['largeClassId']:
                    signInfoList_length = length_signinfo + 1
                else:
                    signInfoList_length += 1
            if signInfoList_length == length_signinfo:
                break
            else:
                add += 1
        signInfoList.append(signInfoList_dic_add_list[add])
        signLargeCalssAdded = signInfoList_dic_add_list[add]['largeClassName']
        for j in range(0, 12):
            for key in salesResolve_dic_add_list[add].keys():
                if key == "month":
                    salesResolve_dic_add_list[add][key] = j + 1
            salesResolveList.append(salesResolve_dic_add_list[add].copy())

        data_apply = json.dumps({
            "userId": self.userid,
            "userName": self.name,
            "agentId": id_d,
            "contractChangeType": "1",
            "serviceAreasList": serviceAreasList,
            "businessChannel": businessChannel,
            "businessAreaRemark": businessAreaRemark,
            "signInfoList": signInfoList,
            "salesResolveList": salesResolveList,
            "firstOrderNum": "100",
            "signLargeCalssAdded": signLargeCalssAdded,
            "authPeriodStart": self.a,
            "authPeriodEnd": self.a[:4] + '-12-31',
            "contractChangeRemark": "备注也是必填项？有点儿反常规。",
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
        employeeid = int(res_text['data']['result']['records'][i]['employeeId'])
        return pid, tid, uniqueid, employeeid

    # 市场部经理不同意
    def test_b_bazaar_disagree(self):
        pid, tid, uniqueid, employeeid = self.get_pid_tid()
        pid_d = str(pid)
        tid_d = str(tid)
        data_actFinish = json.dumps({
            "actType": "productChange",
            "userId": self.userid,
            "pId": pid_d,
            "taskId": tid_d,
            "var": {
                "keys": "managerReviewPass,managerReviewBackReason",
                "values": "false,不同意_市场部不同意",
                "types": "B,S"
            },
            "token": self.token
        })
        res = requests.post(url=self.url_actFinish, data=data_actFinish, headers=self.headers)

        # 判断市场部不同意是否成功
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
        try:
            self.assertEqual(res_text['data']['result']['records'][0]['reasonType'], 'false')
        except Exception as e:
            print('Assertion test fail.', format(e))

        reapply_data = json.dumps({
            "userId": self.userid,
            "page": 1,
            "size": "10",
            "actType": "productChange",
            "perType": "cbapermission",
            "searchType": "ower",
            "token": self.token
        })
        res_reapply = requests.post(url=self.url_finish, data=reapply_data, headers=self.headers)
        res_reapply_text = json.loads(res_reapply.text)
        agent_id = int(res_reapply_text['data']['result']['records'][0]['uniqueId'])
        reasontype = str(res_reapply_text['data']['result']['records'][0]['reasonType'])
        try:
            self.assertEqual(agent_id, self.agent_id) and self.assertEqual(reasontype, "false")
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 重新申请产品变更
    def test_c_reapply(self):
        id_d = self.agent_id
        data_my_apply = json.dumps({
            "userId": self.userid,
            "page": 1,
            "size": 10,
            "actType": "productChange",
            "perType": "cbapermission",
            "searchType": "ower",
            "token": self.token
        })
        res_my_apply = requests.post(url=self.url_finish, data=data_my_apply, headers=self.headers)
        res_text = json.loads(res_my_apply.text)
        uniqueId = res_text['data']['result']['records'][0]['uniqueId']
        employeeid = res_text['data']['result']['records'][0]['employeeId']
        try:
            self.assertEqual(uniqueId, id_d)
        except Exception as e:
            print('Assertion test fail.', format(e))

        businessAreaRemark, businessChannel, address_id, areaIds, signinfo_id, \
        signproduct_id, salesResolve_id, baseNumber1, baseNumber2, baseNumber3, discount1, discount2, discount3, \
        largeClassId, largeClassName, length_salesResolve = self.get_queryInfo(id_d)
        salesResolve_dic = {"id": "", "agentId": employeeid, "largeClassId": 6, "largeClassName": "PE", "month": "",
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

        serviceAreas_dic = {"id": "", "agentId": employeeid, "areaIds": "", "areaNames": "西城区", "cityId": "2",
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
        signProductList_dic = {"agentId": employeeid, "id": "", "productId": 138, "largeClassId": 6, "classify": "1",
                               "color": "产品色", "downPoints": "1", "typePrice": "PE双壁波纹管件", "enabled": 1}
        length_signinfo = len(signinfo_id)
        for l in range(0, length_signinfo):
            for m in range(0, len(signproduct_id[l])):
                for key_pro in signProductList_dic.keys():
                    if key_pro == "id":
                        signProductList_dic[key_pro] = signproduct_id[l][m]
                        signProductList[l].append(signProductList_dic)
            signInfoList_dic = {"id": "", "agentId": employeeid, "baseNumber1": "", "baseNumber2": "", "baseNumber3": "",
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

        data_apply = json.dumps({
            "userId": self.userid,
            "userName": self.name,
            "agentId": id_d,
            "contractChangeType": "1",
            "serviceAreasList": serviceAreasList,
            "businessChannel": businessChannel,
            "businessAreaRemark": businessAreaRemark,
            "signInfoList": signInfoList,
            "salesResolveList": salesResolveList,
            "firstOrderNum": "100",
            "signLargeCalssAdded": "PVC",
            "authPeriodStart": self.a,
            "authPeriodEnd": self.a[:4] + '-12-31',
            "contractChangeRemark": "备注也是必填项？有点儿反常规。重新申请Mark！",
            "token": self.token})
        res = requests.post(url=self.url_apply, data=data_apply, headers=self.headers)
        res_text = json.loads(res.text)
        try:
            self.assertEqual(res_text['data']['result'], '申请成功')
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 市场部经理同意
    def test_d_bazaar_agree(self):
        pid, tid, uniqueid, employeeid = self.get_pid_tid()
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

    # 结算科操作员初审不同意
    def test_e_settlement_dis(self):
        pid, tid, uniqueid, employeeid = self.get_pid_tid()
        data_settl = json.dumps({
            "actType": "productChange",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "settlementOprPass,settlementOprBackReason",
                "values": "false,不同意_不同意",
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
            self.assertEqual(res_task_text, '市场部经理') and self.assertEqual(res_task_uniqueid, uniqueid)
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 市场部经理同意
    def test_f_bazaar_agree(self):
        pid, tid, uniqueid, employeeid = self.get_pid_tid()
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
    def test_g_settlement_agree(self):
        pid, tid, uniqueid, employeeid = self.get_pid_tid()
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

    # 结算科复核不同意
    def test_h_settlementReview_dis(self):
        pid, tid, uniqueid, employeeid = self.get_pid_tid()
        data_agree = json.dumps({
            "actType": "productChange",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "settlementReviewPass,settlementReviewBackReason",
                "values": "false,不同意_2312",
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
            self.assertEqual(res_task_text, '结算科操作员') and self.assertEqual(res_task_uniqueid, uniqueid)
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 结算科操作员初审同意
    def test_i_settlement_agree(self):
        pid, tid, uniqueid, employeeid = self.get_pid_tid()
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
    def test_j_settlementReview_agree(self):
        pid, tid, uniqueid, employeeid = self.get_pid_tid()
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

    # 市场部领导不同意
    def test_k_marketLeader_dis(self):
        pid, tid, uniqueid, employeeid = self.get_pid_tid()
        data_market = json.dumps({
            "actType": "productChange",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "maketLeaderPass,maketLeaderBackReason",
                "values": "false,不同意_123",
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
            self.assertEqual(res_task_text, '结算科操作员') and self.assertEqual(res_task_uniqueid, uniqueid)
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 结算科初审同意
    def test_l_settlement_agree(self):
        pid, tid, uniqueid, employeeid = self.get_pid_tid()
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
    def test_m_settlementReview_agree(self):
        pid, tid, uniqueid, employeeid = self.get_pid_tid()
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
    def test_n_marketLeader_agree(self):
        pid, tid, uniqueid, employeeid = self.get_pid_tid()
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

    # 结算科负责人不同意
    def test_o_settlementLeader_dis(self):
        pid, tid, uniqueid, employeeid = self.get_pid_tid()
        data_principal = json.dumps({
            "actType": "productChange",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "settlementLeaderPass,settlementLeaderBackReason",
                "values": "false,不同意_1015",
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
            self.assertEqual(res_task_text, '结算科操作员') and self.assertEqual(res_task_uniqueid, uniqueid)
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 结算科操作员初审同意
    def test_p_settlement_agree(self):
        pid, tid, uniqueid, employeeid = self.get_pid_tid()
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
    def test_q_settlementReview_agree(self):
        pid, tid, uniqueid, employeeid = self.get_pid_tid()
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
    def test_r_marketLeader_agree(self):
        pid, tid, uniqueid, employeeid = self.get_pid_tid()
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
    def test_s_settlementLeader_agree(self):
        pid, tid, uniqueid, employeeid = self.get_pid_tid()
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

    # 总监1不同意
    def test_t_direct1_dis(self):
        pid, tid, uniqueid, employeeid = self.get_pid_tid()
        data_majordomo = json.dumps({
            "actType": "productChange",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "director1Pass,director1BackReason",
                "values": "false,不同意_产品变更总监1不通过",
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
            self.assertEqual(res_task_text, '结算科负责人') and self.assertEqual(res_task_uniqueid, uniqueid)
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 结算科负责人同意
    def test_u_settlementLeader_agree(self):
        pid, tid, uniqueid, employeeid = self.get_pid_tid()
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
    def test_v_direct1_agree(self):
        pid, tid, uniqueid, employeeid = self.get_pid_tid()
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

    # 总监2审核不同意
    def test_w_direct2_dis(self):
        pid, tid, uniqueid, employeeid = self.get_pid_tid()
        data_majordomo = json.dumps({
            "actType": "productChange",
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
            "actType": "productChange",
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
    def test_x_settlementLeader_agree(self):
        pid, tid, uniqueid, employeeid = self.get_pid_tid()
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
    def test_y_direct1_agree(self):
        pid, tid, uniqueid, employeeid = self.get_pid_tid()
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
    def test_z_direct2_agree(self):
        pid, tid, uniqueid, employeeid = self.get_pid_tid()
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