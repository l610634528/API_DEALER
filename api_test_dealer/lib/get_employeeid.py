import sys
sys.path.append('..')
# from config import *
from lib.dealer_login_token import *
from lib.get_agentid import *
from config.config import dealer_url

url_info = dealer_url + '/cba/agentInfo/selectAgentInfoList'
headers = {"Content-Type": "application/json"}
url_continueSubmit = dealer_url + '/cba/agentInfo/continueSubmit'
url_rename_detail = dealer_url + '/cba/agentInfo/rename/detail'
url_detail = dealer_url + '/cba/agentInfo/detail'
headers = {"Content-Type": "application/json"}
token, name, uid = dealer_login()
userid = str(uid)
agentid = get_agentid()

# 已开户经销提交续签获得resultid
def get_a_resultid():
    data_submit = json.dumps({
        "oldId": agentid,
        "agentType": 1,
        "creatorId": userid,
        "creatorName": "吕结算科",
        "baseStatus": "2",
        "infoStatus": "2",
        "contractStatus": "2",
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
            "agentName": "好好的哈回事",
            "creditCode": "6466444448",
            "address": "好好的还行吧",
            "establishmentDate": "2018-05-08",
            "companyType": "回电话",
            "corporateName": "还好吧",
            "telephone": "15100000000",
            "email": "",
            "registerCapital": "200",
            "businessScope": "并不代表下",
            "bail": "1",
            "firstAmount": "50",
            "isSaled": 2,
            "lastSalesVolume": "",
            "originalSupplier": "",
            "agentId": agentid,
            "areaId": "81",
            "area": "昌黎县",
            "cityId": "76",
            "city": "秦皇岛市",
            "provinceId": "37",
            "province": "河北省",
            "preSignedProduct": '',
            "agentContent": '',
            "warehouse": '',
            "payInPower": ''
        },
        "info": {
            "isDepositary": "2",
            "depositaryName": "",
            "depositarySex": "",
            "depositaryIdcard": "",
            "businessLicence": "900",
            "corporateIdcard": "901,902",
            "depositaryLetterAttach": "",
            "depositaryIdcardAttach": "",
            "paymentProof": "903",
            "depositaryContent": "",
            "corporateIdcardNum": "411111111111111111"
        },
        "contract": {
            "contractStartDate": "2020-01-01",
            "contractEndDate": "2020-12-31",
            "otherAppoint": "磁暴步兵",
            "priceOtherAppoint": '',
            "businessChannel": "1,2",
            "totalNumber1": "200",
            "totalDiscount1": "20",
            "totalNumber2": "",
            "totalDiscount2": "",
            "paymentWay": "1,2",
            "stockRequire": "200",
            "signedProductAttach": "",
            "businessAreaRemark": ""
        },
        "areaList": [{
            "id": 1487,
            "agentId": agentid,
            "areaIds": "393",
            "areaNames": "开鲁县",
            "cityId": "389",
            "city": "通辽市",
            "provinceId": "351",
            "province": "内蒙古自治区"
        }, {
            "id": 1488,
            "agentId": agentid,
            "areaIds": "936",
            "areaNames": "下城区",
            "cityId": "934",
            "city": "杭州市",
            "provinceId": "933",
            "province": "浙江省"
        }, {
            "id": 1489,
            "agentId": agentid,
            "areaIds": "937",
            "areaNames": "江干区",
            "cityId": "934",
            "city": "杭州市",
            "provinceId": "933",
            "province": "浙江省"
        }, {
            "id": 1490,
            "agentId": agentid,
            "areaIds": "935",
            "areaNames": "上城区",
            "cityId": "934",
            "city": "杭州市",
            "provinceId": "933",
            "province": "浙江省"
        }, {
            "id": 1491,
            "agentId": agentid,
            "areaIds": "940",
            "areaNames": "滨江区",
            "cityId": "934",
            "city": "杭州市",
            "provinceId": "933",
            "province": "浙江省"
        }],
        "signInfoList": [{
            "id": 2185,
            "agentId": agentid,
            "baseNumber1": "100",
            "baseNumber2": "",
            "baseNumber3": "",
            "discount1": "20",
            "discount2": "",
            "discount3": "",
            "largeClassId": 4,
            "largeClassName": "PE-RT",
            "signProductList": [{
                "agentId": agentid,
                "id": 11403,
                "productId": 127,
                "largeClassId": 4,
                "classify": "1",
                "color": "产品色",
                "downPoints": "20",
                "typePrice": "WHS水暖供热系统",
                "enabled": 1
            }, {
                "agentId": agentid,
                "id": 11404,
                "productId": 123,
                "largeClassId": 4,
                "classify": "2",
                "color": "橘红色",
                "downPoints": "10",
                "typePrice": "PE-RT（Ⅰ）阻氧管材",
                "enabled": 1
            }, {
                "agentId": agentid,
                "id": 11405,
                "productId": 95,
                "largeClassId": 4,
                "classify": "2",
                "color": "象牙色",
                "downPoints": "99",
                "typePrice": "PB（A）内阻氧管材-冷盘管",
                "enabled": 1
            }]
        }],
        "deliveryAddressList": [{
            "id": 2810,
            "agentId": agentid,
            "type": "1",
            "acceptor": "刚刚好",
            "phoneNum": "15100000000",
            "address": "滚滚滚哈哈",
            "area": "巴林右旗",
            "areaId": "382",
            "city": "赤峰市",
            "cityId": "376",
            "province": "内蒙古自治区",
            "provinceId": "351",
            "remark": "风风光光"
        }, {
            "id": 2811,
            "type": "2",
            "acceptor": "发个还好吧盒",
            "phoneNum": "13111111111",
            "address": "沟沟壑壑",
            "area": "麻山区",
            "areaId": "698",
            "city": "鸡西市",
            "cityId": "692",
            "province": "黑龙江省",
            "provinceId": "655",
            "email": "556555225@163.com"
        }],
        "personalPaymentList": [],
        "thirdPaymentList": [{
            "id": 827,
            "agentId": agentid,
            "name": "212121",
            "reasons": "12323",
            "companyCreditCode": "1111",
            "files": "959,960,961"
        }],
        "salesResolveList": [{
            "id": 7444,
            "agentId": agentid,
            "largeClassId": 4,
            "largeClassName": "PE-RT",
            "month": 1,
            "sales": 200
        }, {
            "id": 7445,
            "agentId": agentid,
            "largeClassId": 4,
            "largeClassName": "PE-RT",
            "month": 2,
            "sales": ""
        }, {
            "id": 7446,
            "agentId": agentid,
            "largeClassId": 4,
            "largeClassName": "PE-RT",
            "month": 3,
            "sales": 200
        }, {
            "id": 7447,
            "agentId": agentid,
            "largeClassId": 4,
            "largeClassName": "PE-RT",
            "month": 4,
            "sales": ""
        }, {
            "id": 7448,
            "agentId": agentid,
            "largeClassId": 4,
            "largeClassName": "PE-RT",
            "month": 5,
            "sales": ""
        }, {
            "id": 7449,
            "agentId": agentid,
            "largeClassId": 4,
            "largeClassName": "PE-RT",
            "month": 6,
            "sales": ""
        }, {
            "id": 7450,
            "agentId": agentid,
            "largeClassId": 4,
            "largeClassName": "PE-RT",
            "month": 7,
            "sales": ""
        }, {
            "id": 7451,
            "agentId": agentid,
            "largeClassId": 4,
            "largeClassName": "PE-RT",
            "month": 8,
            "sales": ""
        }, {
            "id": 7452,
            "agentId": agentid,
            "largeClassId": 4,
            "largeClassName": "PE-RT",
            "month": 9,
            "sales": ""
        }, {
            "id": 7453,
            "agentId": agentid,
            "largeClassId": 4,
            "largeClassName": "PE-RT",
            "month": 10,
            "sales": ""
        }, {
            "id": 7454,
            "agentId": agentid,
            "largeClassId": 4,
            "largeClassName": "PE-RT",
            "month": 11,
            "sales": ""
        }, {
            "id": 7455,
            "agentId": agentid,
            "largeClassId": 4,
            "largeClassName": "PE-RT",
            "month": 12,
            "sales": ""
        }],
        "token": token
    })
    res = requests.post(url=url_continueSubmit, data=data_submit, headers=headers)
    res_text = json.loads(res.text)
    empId = res_text['data']['result']
    return empId



if __name__ == '__main__':
    print(get_a_resultid())