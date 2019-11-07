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
from lib.get_detail import *
import time


class TestChangeName(unittest.TestCase):
    token, name, uid, = dealer_login()
    agent_id = get_id()
    # print('id=' + str(agent_id))
    userid = str(uid)
    time.sleep(5)
    headers = {"Content-Type": "application/json"}
    url_info = dealer_url + '/cba/agentInfo/selectAgentInfoList'
    url_rename_detail = dealer_url + '/cba/agentInfo/rename/detail'
    url_detail = dealer_url + '/cba/agentInfo/detail'
    url_submit = dealer_url + '/cba/agentInfo/rename/submit'
    url_list_task = dealer_url + '/act/list/task'
    url_finish = dealer_url + '/act/list/user/finished'
    url_actfinish = dealer_url + '/cba/agentInfo/actFinish'
    url_save = dealer_url + '/cba/agentInfo/rename/save'

    agentcode, agentname, oldAgentAbbr, contractIdentifier, telephone, address, city, cityid, area, areaId, \
    corporateName, email, province, provinceId, establishmentDate, registerCapital, companyType, businessScope, \
    image_id_one, image_id_two, creditCode = get_rename_detail()    

    @classmethod
    def setUpClass(cls):
        print('=== setUpModule ===')
        cls.data_list = excel_to_list(os.path.join(data_path, "test_dealer_data.xlsx"), "agentInfo_basesave")
        # cls.data_list 同 self.data_list 都是该类的公共属性

    @classmethod
    def tearDownModule(cls):  # 当前模块执行后只执行一次
        print('=== tearDownModule ===')


    # 取detail里的值
    def get_detail(self):
        # agent_id = self.get_id()
        data_detail = json.dumps({
            "id": self.agent_id,
            "token": self.token
        })
        res = requests.post(url=self.url_detail, data=data_detail, headers=self.headers)
        res_text = json.loads(res.text)

    #  更名提交
    def test_a_name_submit(self):
        # old_id = self.get_id()
        data_submit = json.dumps({
            "oldId": self.agent_id,
            "id": self.agent_id,
            "agentCode": self.agentcode,
            "oldAgentAbbr": self.oldAgentAbbr,
            "contractIdentifier": self.contractIdentifier,
            "renameReason": "天气好冷啊",
            "renameStartDate": "2019-10-22",
            "agentName": self.agentname,
            "creditCode": self.creditCode,
            "areaId": self.areaId,
            "area": self.area,
            "cityId": self.cityid,
            "city": self.city,
            "provinceId": self.provinceId,
            "province": self.provinceId,
            "address": self.address,
            "establishmentDate": self.establishmentDate,
            "companyType": self.companyType,
            "corporateName": self.corporateName,
            "telephone": self.telephone,
            "email": self.email,
            "registerCapital": self.registerCapital,
            "businessScope": self.businessScope,
            "businessLicenceRename": "2894",
            "corporateIdcard": str(self.image_id_one) + "," + str(self.image_id_two),
            "adviceNoteRename": "2895",
            "userId": self.userid,
            "userName": self.name,
            "token": self.token
        })
        res = requests.post(url=self.url_submit, data=data_submit, headers=self.headers)

        data_finsh = json.dumps({
            "userId": self.userid,
            "page": 1,
            "size": 10,
            "actType": "rename",
            "searchType": "ower",
            "perType": "cbapermission",
            "token": self.token
        })
        res_finish = requests.post(url=self.url_finish, data=data_finsh, headers=self.headers)
        # res_finish_text = json.loads(res_finish.text)
        # for i in range(0, 10):
        #     if res_finish_text['data']['result']['records'][i]['uniqueId'] == self.agent_id:
        #         i_i = i
        #         res_finish_task_name = res_finish_text['data']['result']['records'][i_i]['task']['name']
        #         try:
        #             self.assertEqual(res_finish_task_name, '市场部经理')
        #         except Exception as e:
        #             print('Assertion test fail.', format(e))

    # 判断是哪个值提交 待办理页面
    def judge(self):
        data_task = json.dumps({
            "userId": self.userid,
            "page": 1,
            "size": 20,
            "actType": "rename",
            "searchType": "ower",
            "perType": "cbapermission",
            "token": self.token
        })
        res = requests.post(url=self.url_list_task, data=data_task, headers=self.headers)
        res_text = json.loads(res.text)
        for i in range(0, 20):
            if res_text['data']['result']['records'][i]['uniqueId'] == self.agent_id:
                res_id = i
                return res_id

    # 我发起页面
    def get_finish_id(self):
        # agenid = self.get_id()
        data_finish_id = json.dumps({
            "userId": self.userid,
            "page": 1,
            "size": 100,
            "actType": "rename",
            "searchType": "ower",
            "perType": "cbapermission",
            "token": self.token
        })
        res = requests.post(url=self.url_finish, data=data_finish_id, headers=self.headers)
        res_text = json.loads(res.text)
        for i in range(0, 20):
            if res_text['data']['result']['records'][i]['uniqueId'] == self.agent_id:
                return i

    # 获取pid和tid
    def get_pid_tid(self):
        i = self.judge()
        # print('i=' + str(i))
        data_pid_tid = json.dumps({
            "userId": self.userid,
            "page": 1,
            "size": 20,
            "actType": "rename",
            "perType": "cbapermission",
            "token": self.token
        })
        res = requests.post(url=self.url_list_task, data=data_pid_tid, headers=self.headers)
        res_text = json.loads(res.text)
        pid = int(res_text['data']['result']['records'][i]['processInstanceId'])
        tid = int(res_text['data']['result']['records'][i]['task']['id'])
        employ_id = int(res_text['data']['result']['records'][i]['employeeId'])
        return pid, tid, employ_id

    # 市场部经理审核不同意
    def test_b_market_disagree(self):
        # print(self.agent_id)
        pid, tid,employ_id = self.get_pid_tid()
        # print(pid, tid)
        data_market = json.dumps({
            "actType": "rename",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "managerReviewPass,managerReviewBackReason",
                "values": "false,不同意_市场部同意",
                "types": "B,S"
            },
            "token": self.token
        })
        res = requests.post(url=self.url_actfinish, data=data_market, headers=self.headers)
        # res_text = json.loads(res.text)
        data_finish = json.dumps({
            "userId": self.userid,
            "page": 1,
            "size": 10,
            "actType": "rename",
            "searchType": "ower",
            "perType": "cbapermission",
            "token": self.token
        })
        res_finish = requests.post(url=self.url_finish, data=data_finish, headers=self.headers)
        res_finish_text = json.loads(res_finish.text)
        i = self.get_finish_id()
        res_reason = res_finish_text['data']['result']['records'][i]['reasonType']
        try:
            self.assertEqual(res_reason, 'false')
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 市场部驳回后重新提交
    def test_c_submit_agree(self):
        data_submit = json.dumps({
            "oldId": self.agent_id,
            "id": self.agent_id,
            "agentCode": self.agentcode,
            "oldAgentAbbr": self.oldAgentAbbr,
            "contractIdentifier": self.contractIdentifier,
            "renameReason": "天气好冷啊",
            "renameStartDate": "2019-10-22",
            "agentName": self.agentname,
            "creditCode": self.creditCode,
            "areaId": self.areaId,
            "area": self.area,
            "cityId": self.cityid,
            "city": self.city,
            "provinceId": self.provinceId,
            "province": self.provinceId,
            "address": self.address,
            "establishmentDate": self.establishmentDate,
            "companyType": self.companyType,
            "corporateName": self.corporateName,
            "telephone": self.telephone,
            "email": self.email,
            "registerCapital": self.registerCapital,
            "businessScope": self.businessScope,
            "businessLicenceRename": "2894",
            "corporateIdcard": str(self.image_id_one) + "," + str(self.image_id_two),
            "adviceNoteRename": "2895",
            "userId": self.userid,
            "userName": self.name,
            "token": self.token
        })
        res = requests.post(url=self.url_submit, data=data_submit, headers=self.headers)

    # 市场部经理审核同意
    def test_d_market_again_agree(self):
        pid, tid,employ_id = self.get_pid_tid()
        data_market = json.dumps({
            "actType": "rename",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "managerReviewPass,managerReviewBackReason",
                "values": "true,同意_市场部同意",
                "types": "B,S"
            },
            "token": self.token
        })
        res = requests.post(url=self.url_actfinish, data=data_market, headers=self.headers)
        res_text = json.loads(res.text)
        res_reason = res_text['data']['result']['reason']
        res_uniqueId = res_text['data']['result']['uniqueId']
        # print(res_uniqueId)
        try:
            self.assertEqual(res_reason, 'settlementOprAudit')
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 结算科新账户名称保存后提交
    def test_f_first_trail_save(self):
        pid, tid, employ_id = self.get_pid_tid()
        data_save = json.dumps({
            "oldId": self.agent_id,
            "id": employ_id,
            "agentCode": self.agentcode,
            "agentAbbr": "小蚊子",
            "oldAgentAbbr": self.oldAgentAbbr,
            "contractIdentifier": self.contractIdentifier,
            "renameReason": "天气好冷啊",
            "renameStartDate": "2019-10-22",
            "agentName": self.agentname,
            "creditCode": self.creditCode,
            "areaId": self.areaId,
            "area": self.area,
            "cityId": self.cityid,
            "city": self.city,
            "provinceId": self.provinceId,
            "province": self.provinceId,
            "address": self.address,
            "establishmentDate": self.establishmentDate,
            "companyType": self.companyType,
            "corporateName": self.corporateName,
            "telephone": self.telephone,
            "email": self.email,
            "registerCapital": self.registerCapital,
            "businessScope": self.businessScope,
            "businessLicenceRename": "2894",
            "corporateIdcard": str(self.image_id_one) + "," + str(self.image_id_two),
            "adviceNoteRename": "2895",
            "userId": self.userid,
            "userName": self.name,
            "token": self.token
        })
        res = requests.post(url=self.url_save, data=data_save, headers=self.headers)
        res_text = json.loads(res.text)
        res_result = res_text['data']['result']
        try:
            self.assertEqual(res_result, '保存成功')
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 保存新名称后审批同意
    def test_g_first_trail_agree(self):
        pid, tid, employ_id = self.get_pid_tid()
        data_first_trail = json.dumps({
            "actType": "rename",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "settlementOprPass,settlementOprBackReason",
                "values": "true,同意_123123",
                "types": "B,S"
            },
            "token": self.token
        })
        res_first = requests.post(url=self.url_actfinish, data=data_first_trail, headers=self.headers)
        res_first_text = json.loads(res_first.text)
        res_reason = res_first_text['data']['result']['reason']
        try:
            self.assertEqual(res_reason, 'settlementReviewAudit')
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 结算科复核审核通过
    def test_h_recheck_agree(self):
        pid, tid, employ_id = self.get_pid_tid()
        data_recheck = json.dumps({
            "actType": "rename",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "settlementReviewPass,settlementReviewBackReason",
                "values": "true,同意_复审同意",
                "types": "B,S"
            },
            "token": self.token
        })
        res = requests.post(url=self.url_actfinish, data=data_recheck, headers=self.headers)
        res_text = json.loads(res.text)
        res_reason = res_text['data']['result']['reason']
        try:
            self.assertEqual(res_reason, 'maketLeaderAudit')
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 市场部领导审批同意
    def test_i_market_agree(self):
        pid, tid, employ_id = self.get_pid_tid()
        data_market = json.dumps({
            "actType": "rename",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "maketLeaderPass,maketLeaderBackReason",
                "values": "true,同意_市场部同意",
                "types": "B,S"
            },
            "token": self.token
        })
        res = requests.post(url=self.url_actfinish, data=data_market, headers=self.headers)
        res_text = json.loads(res.text)
        res_reason = res_text['data']['result']['reason']
        try:
            self.assertEqual(res_reason, 'settlementLeaderAudit')
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 结算科负责人审批同意
    def test_j_principal(self):
        pid, tid, employ_id = self.get_pid_tid()
        data_principal = json.dumps({
            "actType": "rename",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "settlementLeaderPass,settlementLeaderBackReason",
                "values": "true,同意_负责人同意",
                "types": "B,S"
            },
            "token": self.token
        })
        res = requests.post(url=self.url_actfinish, data=data_principal, headers=self.headers)
        res_text = json.loads(res.text)
        res_reason = res_text['data']['result']['reason']
        try:
            self.assertEqual(res_reason, 'settlementOpenAudit')
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 城市零售申请表提交图片
    def test_k_city_upload_image(self):
        pid, tid, employ_id = self.get_pid_tid()
        data_upload = json.dumps({
            "actType": "rename",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "settlementOpenPass,settlementOpenBackReason",
                "values": "Y,同意_提交图片",
                "types": "B,S"
            },
            "fileIds": "2912",
            "token": self.token
        })
        res = requests.post(url=self.url_actfinish, data=data_upload, headers=self.headers)
        res_text = json.loads(res.text)
        res_reason = res_text['data']['result']['reason']
        try:
            self.assertEqual(res_reason, 'statisticReviewAudit')
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 统计科审核同意
    def test_l_statistics_agree(self):
        pid, tid, employ_id = self.get_pid_tid()
        data_statistics = json.dumps({
            "actType": "rename",
            "userId": self.userid,
            "pId": pid,
            "taskId": tid,
            "var": {
                "keys": "statisticReviewPass,statisticReviewBackReason",
                "values": "true,同意_统计科同意",
                "types": "B,S"
            },
            "fileIds": "2913",
            "token": self.token
        })
        requests.post(url=self.url_actfinish, data=data_statistics, headers=self.headers)
        i = self.get_finish_id()
        data_finish = json.dumps({
            "userId": self.userid,
            "page": 1,
            "size": 10,
            "actType": "rename",
            "perType": "cbapermission",
            "token": self.token
        })
        res_finish = requests.post(url=self.url_finish, data=data_finish, headers=self.headers)
        res_text = json.loads(res_finish.text)
        res_reason = res_text['data']['result']['records'][i]['historicVariableInstance']['variableName']
        try:
            self.assertEqual(res_reason, 'statisticReviewBackReason')
        except Exception as e:
            print('Assertion test fail.', format(e))


if __name__ == '__main__':
    unittest.main(verbosity=2)
