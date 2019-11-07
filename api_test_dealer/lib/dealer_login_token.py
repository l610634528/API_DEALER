import unittest
import requests
import json
import sys
sys.path.append("..")  # 提升2级到项目根目录下
from config.config import *  # 从项目路径下导入
# from lib.read_excel import *  # 从项目路径下导入
# from lib.case_log import log_case_info  # 从项目路径下导入
import time

# 登录获取token
def dealer_login():
    time.sleep(5)
    url = dealer_url + '/php/account/login'
    data = json.dumps({
        "mobile":"15067126933",
        "password":"e10adc3949ba59abbe56e057f20f883e",
        "deviceld":"",
        "loginType":1,
        "isSend":0,
        "verify":""
        })
    res = requests.post(url=url, data=data)
    restext = json.loads(res.text)
    # print(restext)
    dealer_token = restext['data']['result']['token']
    # print(dealer_token)
    name = restext['data']['result']['name']
    uid = restext['data']['result']['id']
    # print(name)
    return dealer_token, name, uid


# 新增经销商申请id获取
def dealer_id():
    token, name, uid = dealer_login()
    userid = str(uid)
    url_id = dealer_url + '/cba/agentInfo/baseSave'
    headers = {"Content-Type":"application/json"}
    data_id = json.dumps({
        "agentType": "1",
        "agentStatus": "1",
        "creatorId": userid,
        "creatorName": "吕结算科",
        "userId": userid,
        "userName": "吕结算科",
        "isInsert": "1",
        "base": {
            "agentAccountType": 1,
        "branchId": 8,
        "branchName": "重庆管道城市零售市场部",
        "companyId": 2,
        "companyName": "莫干山总部",
        "branchCode": "CQGDSCB",
        "branchAbbr": "重庆",
        "orgId": 78,
        "orgName": "重庆暖通组",
        "orgCode": "cqsz",
        "agentName": only_one_name(),
        "creditCode": "201212",
        "address": "213",
        "establishmentDate": "2019-10-09",
        "companyType": "22222",
        "corporateName": "法人吕",
        "telephone": "15067126937",
        "email": "610634528@qq.com",
        "registerCapital": "123",
        "businessScope": "1321",
        "bail": "123",
        "firstAmount": "213",
        "isSaled": 2,
        "lastSalesVolume": "",
        "originalSupplier": "",
        "areaId": "3",
        "area": "东城区",
        "cityId": "2",
        "city": "北京市",
        "provinceId": "1",
        "province": "北京",
        "preSignedProduct": "",
        "agentContent": "",
        "warehouse": "",
        "payInPower": ""
            },
            "baseStatus": "2",
            "token": '1'
        })
    res = requests.post(url=url_id, data=data_id, headers=headers)
    restext = json.loads(res.text)
    # print(restext)
    dealerid = restext['data']['result']
    # print(dealerid)
    return dealerid

# 暂不用
# def data_infosave():
#     # dealerid = dealer_id()
#     token, name = dealer_login()
#     headers = {"Content-Type":"application/json"}
#     url = dealer_url + 'cba/agentInfo/infoSave'
#     # 客户json
#     data_infosave = json.dumps(
#         {
#     "id": 1631,
#     "agentType": 1,
#     "agentStatus": "1",
#     "creatorId": 2,
#     "creatorName": name,
#     "userId": 2,
#     "userName": name,
#     "isInsert": "1",
#     "info": {
#         "isDepositary": "2",
#         "depositaryName": "",
#         "depositarySex": "",
#         "depositaryIdcard": "",
#         "businessLicence": "2730",
#         "corporateIdcard": "2731",
#         "depositaryLetterAttach": "",
#         "depositaryIdcardAttach": "",
#         "paymentProof": "2732",
#         "depositaryContent": "123",
#         "corporateIdcardNum": "330327199311122878"
#     },
#     "infoStatus": "1",
#     "token": token
#     })
#     # res = requests.post(url=url, data=data_infosave, headers=headers)
def only_one_name():
    name = curr_time
    return str(name)
    
def get_year_month_day():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    return str(year) + '-' + str(month) + '-' + str(day)

def get_finish_year_month_day():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    return str(year+1) + '-' + str(month) + '-' + str(day)

# 经销商审核
def submit_to_manager():
    uid, token, name = dealer_login()
    dealerid = dealer_id()
    headers = {"Content-Type":"application/json"}
    # token, name = dealer_login()
    url_con = 'http://autotest.cba.zcabc.com/cba/agentInfo/contractSave'
    url_info = 'http://autotest.cba.zcabc.com/cba/agentInfo/infoSave'
    # 提交至经理
    url_updatastatus_2 = dealer_url + 'cba/agentInfo/updateStatus'
    # 经理提交至初审
    url_updatastatus_5 = dealer_url + 'cba/agentInfo/updateStatus'
    # 初审提交
    url_first_trial = dealer_url + 'cba/agentInfo/actFinish'

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
        "creatorId": 426,
        "creatorName": name,
        "userId": 426,
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
    

    data_con = json.dumps({
        "id": dealerid,
        "agentType": 1,
        "isInsert": "1",
        "creatorId": 426,
        "creatorName": "admin",
        "userId": 426,
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
        "areaList": [
            {
                "id": "",
                "agentId": dealerid,
                "areaIds": "4",
                "areaNames": "西城区",
                "cityId": "2",
                "city": "北京市",
                "provinceId": "1",
                "province": "北京"
            }
        ],
        "signInfoList": [
            {
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
                "signProductList": [
                    {
                        "agentId": dealerid,
                        "id": "",
                        "productId": 138,
                        "largeClassId": "6",
                        "classify": 2,
                        "color": "产品色",
                        "downPoints": 1,
                        "typePrice": "PE双壁波纹管材"
                    }
                ]
            }
        ],
        "deliveryAddressList": [
            {
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
        "salesResolveList": [
            {
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
        "token":token 
            })
    
    res1 = requests.post(url=url_con, data=data_con, headers=headers)
    res2 = requests.post(url=url_info, data=data_infosave, headers=headers)
    res4 = requests.post(url=url_updatastatus_2, data=data_updatastatus_2, headers=headers)
    res4 = requests.post(url=url_updatastatus_5, data=data_updatastatus_5, headers=headers)

# 获取初审pid
def first_trial_pid():
    url = dealer_url + 'act/list/task'
    headers = {"Content-Type":"application/json"}
    data_pid = json.dumps({
    "userId": 426,
    "page": 1,
    "size": 10,
    "actType": "sign",
    "perType": "cbapermission",
    "token": token
        })
    res = requests.post(url=url, data=data_pid, headers=headers)
    restext = json.load(res.text)
    pid = restext['data']['result']['records']['0']['processInstanceId']
    return pid

# 获取初审tid
def first_trial_tid():
    pid = first_trial_pid()
    url = dealer_url + 'act/task/detail'
    data_tid = json.dumps({
    "pId": pid,
    "actType": "sign",
    "token": token
        })
    res = requests.post(url=url, data=data_tid, headers=headers)
    restext = json.loads(res.text)
    tid = restext['data']['result']['records']['0']['id']
    return tid

if __name__ == '__main__':
    print('strat')
    submit_to_manager()
    print('over')
    # data_infosave()
    # print(dealerid)
    