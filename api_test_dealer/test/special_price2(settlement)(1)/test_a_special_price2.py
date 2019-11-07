import unittest
import requests
import json
import sys
sys.path.append("../..")  # 提升2级到项目根目录下
from config.config import *  # 从项目路径下导入
from lib.read_excel import *  # 从项目路径下导入
from lib.dealer_login_token import *
from lib.get_agentid import *
import time


class TestAdditional(unittest.TestCase):
    token, name, uid, = dealer_login()
    userid = str(uid)
    agent_id = get_id()
    time.sleep(5)
    headers = {"Content-Type": "application/json"}
    url_info = dealer_url + '/cba/agentInfo/selectAgentInfoList'
    url_special_price = dealer_url + '/cba/priceApply/list'
    url_detail = dealer_url + '/cba/priceApply/detail'

    # 获取经销商信息
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

    # 特殊价格申请
    url_special_price_apply = dealer_url + '/cba/priceApply/save'

    def test_a_special_price_apply(self):
        id_d = self.agent_id
        agentAbbr, agentCode, branchName, orgName, companyName, branchCode, orgCode = self.get_queryInfo()
        data_apply = json.dumps(
            {"keys": [],
             "agentList": [{
                 "agentId": id_d,
                 "agentAbbr": agentAbbr[0],
                 "agentCode": agentCode[0],
                 "branchName": branchName[0],
                 "orgName": orgName[0],
                 "companyName": companyName[0],
                 "branchCode": branchCode[0],
                 "orgCode": orgCode[0],
                 "gross": "100",
                 "controlDosage": "100"
             }],
             "auditReason": "特殊价格申请结算科",
             "type": "1",
             "projectName": "工程名称1",
             "projectAddress": "工程地址1",
             "startTime": "2019-10-25",
             "endTime": "2019-10-31",
             "monthly": "全额",
             "monthlyOther": "月说明",
             "annual": "全额",
             "annualOther": "年说明",
             "rebate": "全额",
             "rebateOther": "经销商返利",
             "other": "nothing",
             "applyReason": "everything",
             "productList": [{
                 "productName": "PE",
                 "productDetail": "PE双壁波纹管件",
                 "signProductId": 139,
                 "productColor": "产品色",
                 "price": "50",
                 "productId": 6
             }],
             "userName": self.name,
             "userId": self.userid,
             "applyType": "2",
             "token": self.token
             })
        res = requests.post(url=self.url_special_price_apply, data=data_apply, headers=self.headers)
        res_text = json.loads(res.text)
        try:
            self.assertEqual(res_text['data']['result'], '操作成功！')
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 判断特殊价格申请（结算科）
    def test_b_judgement(self):
        id_d = self.agent_id
        data_list = json.dumps({
            "actType": "specialPrice",
            "perType": "cbapermission",
            "page": 1,
            "size": 10,
            "userId": self.userid,
            "userName": self.name,
            "startTime": "",
            "endTime": "",
            "type": "",
            "token": self.token
        })
        res = requests.post(url=self.url_special_price, data=data_list, headers=self.headers)
        res_text = json.loads(res.text)
        # for i in range(0, 10):
        detail_id = int(res_text['data']['result']['records'][0]['id'])
        data_detail = json.dumps(
            {"userName": self.name,
             "userId": self.userid,
             "id": detail_id})
        res_detail = requests.post(url=self.url_detail, data=data_detail, headers=self.headers)
        res_detail_text = json.loads(res_detail.text)
        id_detail = res_detail_text['data']['result']['agentList'][0]['agentId']
        try:
            self.assertEqual(id_detail, id_d)
        except Exception as e:
            print('Assertion test fail.', format(e))


if __name__ == '__main__':
    unittest.main(verbosity=2)