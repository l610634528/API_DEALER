import sys
sys.path.append('..')
# from api_test_dealer.config import *
from lib.dealer_login_token import *
from lib.get_agentid import *
from config.config import dealer_url

url_info = dealer_url + '/cba/agentInfo/selectAgentInfoList'
headers = {"Content-Type": "application/json"}

token, name, uid = dealer_login()
userid = str(uid)
agent_id = get_id()
url_rename_detail = dealer_url + '/cba/agentInfo/rename/detail'
headers = {"Content-Type": "application/json"}


# 取rename_detail里的值
def get_rename_detail():
    # agent_id = self.get_id()
    data_rename_detail = json.dumps({
        "id": agent_id,
        "token": token
    })
    res = requests.post(url=url_rename_detail, data=data_rename_detail, headers=headers)
    res_text = json.loads(res.text)
    # 账户代码
    agentcode = res_text['data']['result']['agentCode']
    # 客户全程
    agentname = res_text['data']['result']['agentName']
    # 原账户名称
    oldAgentAbbr = res_text['data']['result']['oldAgentAbbr']
    # 合同编号
    contractIdentifier = res_text['data']['result']['contractIdentifier']
    # 联系电话
    telephone = res_text['data']['result']['telephone']
    # 详细地址
    address = res_text['data']['result']['address']
    # 市区
    city = res_text['data']['result']['city']
    # 市区id
    cityid = res_text['data']['result']['cityId']
    # 地区
    area = res_text['data']['result']['area']
    # 地区id
    areaId = res_text['data']['result']['areaId']
    # 法人

    corporateName = res_text['data']['result']['corporateName']
    # 邮箱
    email = res_text['data']['result']['email']

    # 省
    province = res_text['data']['result']['province']
    # 省id
    provinceId = res_text['data']['result']['provinceId']
    # 成立时间
    establishmentDate = res_text['data']['result']['establishmentDate']
    # 注册资本
    registerCapital = res_text['data']['result']['registerCapital']
    # 单位类型
    companyType = res_text['data']['result']['companyType']
    # 经营范围
    businessScope = res_text['data']['result']['businessScope']
    # 法人照片id
    image_id_one = res_text['data']['result']['corporateIdcardAttachList'][0]['id']
    image_id_two = res_text['data']['result']['corporateIdcardAttachList'][1]['id']
    # 信用代码
    creditCode = res_text['data']['result']['creditCode']

    return agentcode, agentname, oldAgentAbbr, contractIdentifier, telephone, address, city, cityid, area, areaId, corporateName, \
           email, province, provinceId, establishmentDate, registerCapital, companyType, businessScope, image_id_one, \
           image_id_two, creditCode

if __name__ == '__main__':
    print(get_rename_detail())