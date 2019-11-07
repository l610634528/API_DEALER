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

# 总监2不同意后继续审核通过开户
class TestBaseSave(unittest.TestCase):
    present_time = get_year_month_day()
    token, name, uid, = dealer_login()
    userid = str(uid)
    # print(token, name, userid)
    time.sleep(5)
    dealerid = dealer_id()
    # print(dealerid)
    headers = {"Content-Type":"application/json"}
    # 经销商申请
    url_basesave = dealer_url + '/cba/agentInfo/baseSave'
    url_infosave = dealer_url + '/cba/agentInfo/infoSave'
    url_contractsave = dealer_url + '/cba/agentInfo/contractSave'
    # 提交至经理
    url_updatastatus_2 = dealer_url + '/cba/agentInfo/updateStatus'
    # 经理提交至初审
    url_updatastatus_5 = dealer_url + '/cba/agentInfo/updateStatus'

    url_pid = dealer_url + '/act/list/task'

    url_tid = dealer_url + '/act/task/detail'

    data_pid = json.dumps({
        "userId": userid,
        "page": 1,
        "size": 10,
        "actType": "sign",
        "perType": "cbapermission",
        "token": token
        })

    @classmethod
    def setUpClass(cls):
        print('=== setUpModule ===签约总监2不同意')
        cls.data_list = excel_to_list(os.path.join(data_path, "test_dealer_data.xlsx"), "agentInfo_basesave")  
        # cls.data_list 同 self.data_list 都是该类的公共属性
    @classmethod
    def tearDownModule(): # 当前模块执行后只执行一次
        print('=== tearDownModule ===')
    # 获取pid
    def pid_first_trial(self):
        res = requests.post(url=self.url_pid, data=self.data_pid, headers=self.headers)
        restext = json.loads(res.text)
        pid = int(restext['data']['result']['records'][0]['processInstanceId'])
        return pid

    # 经理提交至初审
    data_updatastatus_5 = json.dumps({
        "id": dealerid,
        "userId": userid,
        "userName": "吕结算科",
        "agentStatus": "5",
        "token": token
        })

    # 提交至经理
    data_updatastatus_2 = json.dumps({
        "id": dealerid,
        "userId": userid,
        "userName": "吕结算科",
        "agentStatus": "2",
        "token": token
        })    
    # 客户json
    data_infosave = json.dumps({
        "id": dealerid,
        "agentType": 1,
        "agentStatus": "1",
        "creatorId": userid,
        "creatorName": name,
        "userId": userid,
        "userName": name,
        "isInsert": "1",
        "info":{
        "isDepositary": "2",
        "depositaryName": "",
        "depositarySex": "",
        "depositaryIdcard": "",
        "businessLicence": "2733",
        "corporateIdcard": "2734,2735",
        "depositaryLetterAttach": "",
        "depositaryIdcardAttach": "",
        "paymentProof": "2748",
        "depositaryContent": "123",
        "corporateIdcardNum": "330327199311122878"
          },
          "infoStatus":"2",
          "token":token
    })

    # 合同json
    data_contractsave = json.dumps({
        "id": dealerid,
        "agentType": 1,
        "isInsert": "1",
        "creatorId": userid,
        "creatorName": "admin",
        "userId": userid,
        "userName": "admin",
        "contract": {
            "contractStartDate": "2019-10-09",
            "contractEndDate": "2019-12-31",
            "otherAppoint": "213",
            "priceOtherAppoint": "1",
            "businessChannel": "1",
            "totalNumber1": "1",
            "totalDiscount1": "2",
            "totalNumber2": "1",
            "totalDiscount2": "2",
            "paymentWay": "1",
            "stockRequire": "1",
            "businessAreaRemark": "123",
            "signedProductAttach": ""
        },
        "areaList": [{
            "id": "",
            "agentId": dealerid,
            "areaIds": "4",
            "areaNames": "西城区",
            "cityId": "2",
            "city": "北京市",
            "provinceId": "1",
            "province": "北京"
        }],
        "signInfoList": [{
            "id": "",
            "agentId": dealerid,
            "baseNumber1": "1",
            "baseNumber2": "1",
            "baseNumber3": "1",
            "discount1": "1",
            "discount2": "1",
            "discount3": "1",
            "largeClassId": "6",
            "largeClassName": "PE",
            "signProductList": [{
                "agentId": dealerid,
                "id": "",
                "productId": 138,
                "largeClassId": "6",
                "classify": 2,
                "color": "产品色",
                "downPoints": 1,
                "typePrice": "PE双壁波纹管材"
            }]
        }],
        "deliveryAddressList": [{
                "id": "",
                "agentId": dealerid,
                "type": "1",
                "acceptor": "吕",
                "phoneNum": "15067126937",
                "address": "123",
                "area": "峰峰矿区",
                "areaId": "88",
                "city": "邯郸市",
                "cityId": "84",
                "province": "河北省",
                "provinceId": "37",
                "remark": "123"
            },
            {
                "id": "",
                "type": "2",
                "acceptor": "吕",
                "phoneNum": "15067126937",
                "address": "123",
                "area": "东城区",
                "areaId": "3",
                "city": "北京市",
                "cityId": "2",
                "province": "北京",
                "provinceId": "1",
                "email": "610634528@qq.com"
            }
        ],
        "personalPaymentList": [],
        "thirdPaymentList": [],
        "salesResolveList": [{
                "id": "",
                "agentId": dealerid,
                "largeClassId": "6",
                "largeClassName": "PE",
                "month": 1,
                "sales": 1
            },
            {
                "id": "",
                "agentId": dealerid,
                "largeClassId": "6",
                "largeClassName": "PE",
                "month": 2,
                "sales": 1
            },
            {
                "id": "",
                "agentId": dealerid,
                "largeClassId": "6",
                "largeClassName": "PE",
                "month": 3,
                "sales": 1
            },
            {
                "id": "",
                "agentId": dealerid,
                "largeClassId": "6",
                "largeClassName": "PE",
                "month": 4,
                "sales": 1
            },
            {
                "id": "",
                "agentId": dealerid,
                "largeClassId": "6",
                "largeClassName": "PE",
                "month": 5,
                "sales": 1
            },
            {
                "id": "",
                "agentId": dealerid,
                "largeClassId": "6",
                "largeClassName": "PE",
                "month": 6,
                "sales": 1
            },
            {
                "id": "",
                "agentId": dealerid,
                "largeClassId": "6",
                "largeClassName": "PE",
                "month": 7,
                "sales": 1
            },
            {
                "id": "",
                "agentId": dealerid,
                "largeClassId": "6",
                "largeClassName": "PE",
                "month": 8,
                "sales": 1
            },
            {
                "id": "",
                "agentId": dealerid,
                "largeClassId": "6",
                "largeClassName": "PE",
                "month": 9,
                "sales": 1
            },
            {
                "id": "",
                "agentId": dealerid,
                "largeClassId": "6",
                "largeClassName": "PE",
                "month": 10,
                "sales": 1
            },
            {
                "id": "",
                "agentId": dealerid,
                "largeClassId": "6",
                "largeClassName": "PE",
                "month": 11,
                "sales": 1
            },
            {
                "id": "",
                "agentId": dealerid,
                "largeClassId": "6",
                "largeClassName": "PE",
                "month": 12,
                "sales": 1
            }
        ],
        "token": token
    })
    

    @classmethod
    def setUpClass(cls):
        print('=== setUpModule ===')
        cls.data_list = excel_to_list(os.path.join(data_path, "test_dealer_data.xlsx"), "agentInfo_basesave")  
        # cls.data_list 同 self.data_list 都是该类的公共属性
    @classmethod
    def tearDownModule(cls): # 当前模块执行后只执行一次
        print('=== tearDownModule ===')

    def test_a_数据保存(self):
        # case_data = get_test_data(self.data_list, 'test_basesave_normal')  # 从数据列表中查找到该用例数据
        # if not case_data:  # 有可能为None
        #     logging.error("用例数据不存在")
        # expect_res = json.loads(case_data.get('expect_res'))  # 期望数据
        res_1 = requests.post(url=self.url_infosave, data=self.data_infosave, headers=self.headers)
        res = json.loads(res_1.text)

    def test_b_数据填写(self):

        res_2 = requests.post(url=self.url_contractsave, data=self.data_contractsave, headers=self.headers)
        # try:
        #     self.assertEuqal()
        # except Exception as e:
        #     print('Assertion test fail.', format(e))
    # 提交至经理
    def test_c_提交至经理(self):

        res_3 = requests.post(url=self.url_updatastatus_2, data=self.data_updatastatus_2, headers=self.headers)
    
    # 提交至初审
    def test_d_提交至初审(self):
        
        res_4 = requests.post(url=self.url_updatastatus_5, data=self.data_updatastatus_5, headers=self.headers)
    
    def tid_1_first_trial(self):
        res = requests.post(url=self.url_pid, data=self.data_pid, headers=self.headers)
        restext = json.loads(res.text)
        tid = restext['data']['result']['records'][0]['task']['id']
        return int(tid)
  
    # 结算科初审同意
    url_audit = dealer_url + '/cba/agentInfo/actFinish'
    def test_e_初审同意(self):
        # 获取tid1
        tid_1 = self.tid_1_first_trial()
        data_settle_first_trial = json.dumps({
            "actType": "sign",
            "userId": self.userid,
            "pId": self.pid_first_trial(),
            "taskId": tid_1,
            "var": {
                "keys": "settlementOprPass,settlementOprBackReason",
                "values": "true,同意_1初审同意",
                "types": "B,S"
            },
            "token": self.token
            })
        res = requests.post(url=self.url_audit, data=data_settle_first_trial, headers=self.headers)
    
    # 结算科复审
    def test_f_复审同意(self):
        # 获取tid2
        tid_2 = self.tid_1_first_trial()
        data_settle_recheck = json.dumps({
            "actType": "sign",
            "userId": self.userid,
            "pId": self.pid_first_trial(),
            "taskId": tid_2,
            "var": {
                "keys": "settlementReviewPass,settlementReviewBackReason",
                "values": "true,同意_2复核通过",
                "types": "B,S"
            },
            "token": self.token
            })
        requests.post(url=self.url_audit, data=data_settle_recheck, headers=self.headers)
    
    # 市场部审核
    def test_g_市场部同意(self):
        # 获取tid3
        tid_3 = self.tid_1_first_trial()
        data_bazaar = json.dumps({
            "actType": "sign",
            "userId": self.userid,
            "pId": self.pid_first_trial(),
            "taskId": tid_3,
            "var": {
                "keys": "maketLeaderPass,maketLeaderBackReason",
                "values": "true,同意_3市场部同意",
                "types": "B,S"
            },
            "fileIds": "2738",
            "token": self.token
            })
        requests.post(url=self.url_audit, data=data_bazaar, headers=self.headers)

    # 结算科负责人终审
    def test_h_负责人终审同意(self):
        # 获取tid4
        tid_4 = self.tid_1_first_trial()
        data_trial_finish = json.dumps({
            "actType": "sign",
            "userId": self.userid,
            "pId": self.pid_first_trial(),
            "taskId": tid_4,
            "var": {
                "keys": "settlementLeaderPass,settlementLeaderBackReason",
                "values": "true,同意_4结算科负责人",
                "types": "B,S"
            },
            "token": self.token
            })
        res = requests.post(url=self.url_audit, data=data_trial_finish, headers=self.headers)

    # 总监1审核同意
    def test_i_总监1同意(self):
        # 获取tid5
        tid_5 = self.tid_1_first_trial()
        data_majordomo = json.dumps({
            "actType": "sign",
            "userId": self.userid,
            "pId": self.pid_first_trial(),
            "taskId": tid_5,
            "var": {
                "keys": "director1Pass,director1BackReason",
                "values": "true,同意_5总监1",
                "types": "B,S"
            },
            "fileIds": "2739",
            "token": self.token
            }
            )
        res = requests.post(url=self.url_audit, data=data_majordomo, headers=self.headers)


    # 总监2审核不同意
    def test_j_总监2不同意(self):
        # 获取tid6
        tid_6 = self.tid_1_first_trial()
        data_majordomo_2 = json.dumps({
            "actType": "sign",
            "userId": self.userid,
            "pId": self.pid_first_trial(),
            "taskId": tid_6,
            "var": {
                "keys": "director2Pass,director2BackReason",
                "values": "N,不同意_不同意123",
                "types": "S,S"
            },
            "fileIds": "",
            "token": self.token
        })
        res = requests.post(url=self.url_audit, data=data_majordomo_2, headers=self.headers)

    # 结算科负责人终审_2
    def test_k_负责人再次同意(self):
        tid_7 = self.tid_1_first_trial()
        data_trial_finish_2 = json.dumps({
            "actType": "sign",
            "userId": self.userid,
            "pId": self.pid_first_trial(),
            "taskId": tid_7,
            "var": {
                "keys": "settlementLeaderPass,settlementLeaderBackReason",
                "values": "true,同意_4结算科负责人",
                "types": "B,S"
                },
            "token": self.token
            })
        res = requests.post(url=self.url_audit, data=data_trial_finish_2, headers=self.headers)

    # 总监1再审核_2
    def test_l_总监1再次同意(self):
        # 获取tid5
        tid_8 = self.tid_1_first_trial()
        data_majordomo = json.dumps({
            "actType": "sign",
            "userId": self.userid,
            "pId": self.pid_first_trial(),
            "taskId": tid_8,
            "var": {
                "keys": "director1Pass,director1BackReason",
                "values": "true,同意_5总监1",
                "types": "B,S"
            },
            "fileIds": "2739",
            "token": self.token
        })
        res = requests.post(url=self.url_audit, data=data_majordomo, headers=self.headers)

    # 总监2再审核_2
    def test_m_总监2同意(self):
        # 获取tid6
        tid_9 = self.tid_1_first_trial()
        data_majordomo_2 = json.dumps({
            "actType": "sign",
            "userId": self.userid,
            "pId": self.pid_first_trial(),
            "taskId": tid_9,
            "var": {
                "keys": "director2Pass,director2BackReason",
                "values": "N,不同意_不同意123",
                "types": "S,S"
            },
            "fileIds": "",
            "token": self.token
        })
        res = requests.post(url=self.url_audit, data=data_majordomo_2, headers=self.headers)

    # 开户操作
    def test_n_开户(self):
        # 获取tid7
        tid_10 = self.tid_1_first_trial()
        data_open_account = json.dumps({
            "actType": "sign",
            "userId": self.userid,
            "pId": self.pid_first_trial(),
            "taskId": tid_10,
            "var": {
                "keys": "settlementOpenPass,settlementOpenBackReason",
                "values": "Y,同意_",
                "types": "S,S"
            },
            "fileIds": "2755",
            "token": self.token
            })
        res = requests.post(url=self.url_audit, data=data_open_account, headers=self.headers)

    # 开户确认
    def test_o_开户确认(self):
        tid_11 = self.tid_1_first_trial()
        data_open_true = json.dumps({
            "actType": "sign",
            "userId": self.userid,
            "pId": self.pid_first_trial(),
            "taskId": tid_11,
            "var": {
                "keys": "statisticReviewPass,statisticReviewBackReason",
                "values": "true,同意_开户确认",
                "types": "B,S"
            },
            "fileIds": "2756",
            "token": self.token
            })
        res = requests.post(url=self.url_audit, data=data_open_true, headers=self.headers)

    # 获取id
    url_get_id = dealer_url + '/cba/agentInfo/selectAgentInfoList'
    def get_id(self):
        data_get_id = json.dumps({
            "tag": 4,
            "userId": self.userid,
            "keyword": "",
            "companyId": "",
            "branchId": "",
            "orgId": "",
            "page": 1,
            "size": 10,
            "token": self.token
            })
        res = requests.post(url=self.url_get_id, data=data_get_id, headers=self.headers)
        res_text = json.loads(res.text)
        res_id = int(res_text['data']['result']['records'][0]['id'])
        return res_id

    # 开户
    url_open = dealer_url + '/cba/agentInfo/openSubmit'
    def test_q_确认开户(self):
        id_d = self.get_id()
        data_open = json.dumps({
            "id": id_d,
            "agentStatus": 8,
            "userId": self.userid,
            "userName": "Andy",
            "open": {
                "submitFlag": 1,
                "agentCode": "test01_lvxj",
                "accountCtime": self.present_time,
                "agentAbbr": "test01",
                "contractIdentifier": "",
                "bail": "1",
                "bailOrderNum": "1",
                "receiptNum": "1",
                "isReceivedContract": "2",
                "receivedCount": "",
                "expressNum": "1",
                "remark": "1"
            },
            "token": self.token
            })
        res = requests.post(url=self.url_open, data=data_open, headers=self.headers)

if __name__ == '__main__':
    unittest.main(verbosity=2)