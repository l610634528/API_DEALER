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

# 状态为已开户的经销商进行撤户
class TestRemoveAccount(unittest.TestCase):
    token, name, uid, = dealer_login()
    userid = str(uid)
    # 撤户url
    url_updatestatus = dealer_url + '/cba/agentInfo/updateStatus'
    url_infolist = dealer_url + '/cba/agentInfo/selectAgentInfoList'
    headers = {"Content-Type":"application/json"}

    @classmethod
    def setUpClass(cls):
        print('=== setUpModule ===')
        cls.data_list = excel_to_list(os.path.join(data_path, "test_dealer_data.xlsx"), "agentInfo_basesave")  
        # cls.data_list 同 self.data_list 都是该类的公共属性
    @classmethod
    def tearDownModule(cls): # 当前模块执行后只执行一次
        print('=== tearDownModule ===')

    def get_a_list(self):
        data_infolist = json.dumps({
            "tag": 4,
            "userId": self.userid,
            "keyword": "",
            "companyId": "",
            "branchId": "",
            "orgId": "",
            "page": 1,
            "size": 50,
            "token": self.token
            })
        res = requests.post(url=self.url_infolist, data=data_infolist, headers=self.headers)
        res_text = json.loads(res.text)
        for i in range(0, 10):
            if res_text['data']['result']['records'][i]['agentStatusText'] == '已开户':
                # print(res_text['data']['result']['records'][i]['id'])
                # print(i)
                return res_text['data']['result']['records'][i]['id'], i
                

    # 选择已开户的经销商进行撤户操作
    def test_a_撤户(self):
        res_id, i = self.get_a_list()
        data_updatestatus = json.dumps({
            "id": res_id,
            "agentStatus": 9,
            "userId": self.userid,
            "userName": self.name,
            "token": self.token
            })
        res = requests.post(url=self.url_updatestatus, data=data_updatestatus, headers=self.headers)
        data_infolist = json.dumps({
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
        res_info = requests.post(url=self.url_infolist, data=data_infolist, headers=self.headers)
        res_info_text = json.loads(res_info.text)
        res_remove = res_info_text['data']['result']['records'][i]['agentStatusText']
        try:
            self.assertEqual(res_remove, '已撤户')
        except Exception as e:
            print('Assertion test fail.', format(e))

if __name__ == '__main__':
    unittest.main(verbosity=2)