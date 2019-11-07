import sys

sys.path.append('..')
# from config import *
import json
from config.config import dealer_url
from lib.get_agentid import *
from lib.dealer_login_token import *

url_detail = dealer_url + '/cba/agentInfo/detail'
agentid = get_agentid()  # 已开户但未续签的
headers = {"Content-Type": "application/json"}
token, name, uid = dealer_login()
url_continueSubmit = dealer_url + '/cba/agentInfo/continueSubmit'
userid = str(uid)


# 客户概况
def get_many_messages_type_one():
    data_messages = json.dumps({
        "id": agentid,
        "token": token,
        "type": 1
    })
    res = requests.post(url=url_detail, data=data_messages, headers=headers)
    res_text = json.loads(res.text)
    # 账户类型
    agentAccountType = res_text['data']['result']['base']['agentAccountType']
    # 法人代表
    corporateName = res_text['data']['result']['base']['corporateName']
    # 地区_东城区
    area = res_text['data']['result']['base']['area']
    # areaId
    areaId = res_text['data']['result']['base']['areaId']
    # businessScope_公司经营范围
    businessScope = res_text['data']['result']['base']['businessScope']
    # city
    city = res_text['data']['result']['base']['city']
    # cityId
    cityId = res_text['data']['result']['base']['cityId']
    # 客户全称
    agentName = res_text['data']['result']['base']['agentName']
    # 地址
    address = res_text['data']['result']['base']['address']
    # 公司id
    companyId = res_text['data']['result']['base']['companyId']
    # 公司名称
    companyName = res_text['data']['result']['base']['companyName']
    # 公司Type
    companyType = res_text['data']['result']['base']['companyType']
    # 保证金bail
    bail = res_text['data']['result']['base']['bail']
    # branchabbr
    branchAbbr = res_text['data']['result']['base']['branchAbbr']
    branchCode = res_text['data']['result']['base']['branchCode']
    branchId = res_text['data']['result']['base']['branchId']
    branchName = res_text['data']['result']['base']['branchName']
    # 信用代码
    creditCode = res_text['data']['result']['base']['creditCode']
    # 邮箱
    email = res_text['data']['result']['base']['email']
    # 成立时间
    establishmentDate = res_text['data']['result']['base']['establishmentDate']
    # 首次打款金额
    firstAmount = res_text['data']['result']['base']['firstAmount']
    # 隶属开发组代码
    orgCode = res_text['data']['result']['base']['orgCode']
    # 隶属开发组
    orgName = res_text['data']['result']['base']['orgName']
    # 隶属id
    orgId = res_text['data']['result']['base']['orgId']
    # 省
    province = res_text['data']['result']['base']['province']
    # 省id
    provinceId = res_text['data']['result']['base']['provinceId']
    # 注册资本
    registerCapital = res_text['data']['result']['base']['registerCapital']
    # 电话号码
    telephone = res_text['data']['result']['base']['telephone']
    # idStr_one
    idStr = res_text['data']['result']['base']['idStr']
    isSaled = res_text['data']['result']['base']['isSaled']
    # agentType
    agentType = res_text['data']['result']['agentType']
    lastSalesVolume = res_text['data']['result']['base']['lastSalesVolume']
    originalSupplier = res_text['data']['result']['base']['originalSupplier']
    preSignedProduct = res_text['data']['result']['base']['preSignedProduct']
    agentContent = res_text['data']['result']['base']['agentContent']
    warehouse = res_text['data']['result']['base']['warehouse']
    payInPower = res_text['data']['result']['base']['payInPower']
    # print(agentAccountType, corporateName, area, areaId, businessScope, city, cityId, agentName, address,
    #       companyId, companyName, companyType, bail, branchAbbr, branchCode, branchId, branchName, creditCode, email,
    #       establishmentDate,
    #       firstAmount, orgCode, orgName, orgId, province, provinceId, registerCapital, telephone, idStr, isSaled,
    #       agentType,
    #       lastSalesVolume, originalSupplier, preSignedProduct, agentContent, warehouse, payInPower)
    return agentAccountType, corporateName, area, areaId, businessScope, city, cityId, agentName, address, \
           companyId, companyName, companyType, bail, branchAbbr, branchCode, branchId, branchName, creditCode, email, establishmentDate, \
           firstAmount, orgCode, orgName, orgId, province, provinceId, registerCapital, telephone, idStr, isSaled, agentType, \
           lastSalesVolume, originalSupplier, preSignedProduct, agentContent, warehouse, payInPower


# 客户信息
def get_many_messages_type_two():
    data_messages = json.dumps({
        "id": agentid,
        "toekn": token,
        "type": 2
    })
    res = requests.post(url=url_detail, data=data_messages, headers=headers)
    res_text = json.loads(res.text)
    # 身份证
    corporateIdcardNum = res_text['data']['result']['info']['corporateIdcardNum']
    corporateIdcard = res_text['data']['result']['info']['corporateIdcard']
    businessLicence = res_text['data']['result']['info']['businessLicence']
    isDepositary = res_text['data']['result']['info']['isDepositary']
    paymentProof = res_text['data']['result']['info']['paymentProof']
    depositaryName = res_text['data']['result']['info']['depositaryName']
    depositarySex = res_text['data']['result']['info']['depositarySex']
    depositaryContent = res_text['data']['result']['info']['depositaryContent']
    depositaryLetterAttach = res_text['data']['result']['info']['depositaryLetterAttach']
    depositaryIdcardAttach = res_text['data']['result']['info']['depositaryIdcardAttach']
    depositaryIdcard = res_text['data']['result']['info']['depositaryIdcard']
    # print(corporateIdcardNum, corporateIdcard, businessLicence, isDepositary, paymentProof, depositaryName,
    #       depositarySex, depositaryContent, depositaryLetterAttach, depositaryIdcardAttach, depositaryIdcard)
    return corporateIdcardNum, corporateIdcard, businessLicence, isDepositary, paymentProof, depositaryName, \
           depositarySex, depositaryContent, depositaryLetterAttach, depositaryIdcardAttach, depositaryIdcard


# 合同信息
def get_many_messages_type_four():
    data_messages = json.dumps({
        "id": agentid,
        "token": token,
        "type": 4
    })
    res = requests.post(url=url_detail, data=data_messages, headers=headers)
    res_text = json.loads(res.text)
    otherAppoint = res_text['data']['result']['contract']['otherAppoint']
    paymentWay = res_text['data']['result']['contract']['paymentWay']
    priceOtherAppoint = res_text['data']['result']['contract']['priceOtherAppoint']
    businessChannel = res_text['data']['result']['contract']['businessChannel']
    businessAreaRemark = res_text['data']['result']['contract']['businessAreaRemark']
    stockRequire = res_text['data']['result']['contract']['stockRequire']
    signedProductAttach = res_text['data']['result']['contract']['signedProductAttach']
    totalDiscount1 = res_text['data']['result']['contract']['totalDiscount1']
    totalDiscount2 = res_text['data']['result']['contract']['totalDiscount2']
    totalNumber1 = res_text['data']['result']['contract']['totalNumber1']
    totalNumber2 = res_text['data']['result']['contract']['totalNumber2']
    # print(otherAppoint, paymentWay, priceOtherAppoint, businessChannel, businessAreaRemark, stockRequire,
    #       signedProductAttach, totalDiscount1, totalDiscount2, totalNumber1, totalNumber2)
    return otherAppoint, paymentWay, priceOtherAppoint, businessChannel, businessAreaRemark, stockRequire, \
           signedProductAttach, totalDiscount1, totalDiscount2, totalNumber1, totalNumber2


# 合同信息地址
def get_contract_arealist():
    data_messages_list = json.dumps({
        "id": agentid,
        "token": token,
        "type": 4
    })
    res = requests.post(url=url_detail, data=data_messages_list, headers=headers)
    res_text = json.loads(res.text)
    area_dic = {"id": '', "agentId": '', "areaIds": '', "areaNames": '', "cityId": '', "city": '', "provinceId": '',
                "province": ''}
    rea_arealist = res_text['data']['result']['areaList']
    arealistnumber = int(len(rea_arealist))
    # print(arealistnumber)
    arealists = []
    l = {}
    for i in range(0, arealistnumber):
        tmp = []
        for j in area_dic.keys():
            for k in rea_arealist[i].keys():
                if j == k:
                    area_dic[j] = rea_arealist[i][k]
                    tmp.append(area_dic[j])
        arealists.append(tmp)
        # print(rea_arealist[i])
    # print(arealist)
    h = []
    x = []
    for arealist in arealists:
        for k in area_dic.keys():
            h.append(k)
        l = dict(zip(h, arealist))
        x.append(l)
    # print(x)
    return x


# 合同信息签约产品
def get_contract_signproductlist():
    data_productlist = json.dumps({
        "id": agentid,
        "token": token,
        "type": 4
    })
    res = requests.post(url=url_detail, data=data_productlist, headers=headers)
    res_text = json.loads(res.text)
    signlist_dict = {"agentId": '', "id": '', "productId": '', "largeClassId": '', "classify": '', "color": '',
                     "downPoints": '', "typePrice": '', "enabled": ''}
    signinfo_dict = {"id": '', "agentId": '', "baseNumber1": '', "baseNumber2": '', "baseNumber3": '', "discount1": '',
                     "discount2": '', "discount3": '', "largeClassId": '', "largeClassName": '', "signProductList": ''}
    signinfolist = res_text['data']['result']['signInfoList']
    # print(signinfolist)
    signnumber = int(len(signinfolist))
    # print(signnumber)
    all_signproductlist = []

    y = []
    # for number in range(0, signnumber):
    # 去signproductlist下面的值[0][1][2]...
    for i in range(0, signnumber):
        signproductlist = signinfolist[i]['signProductList']
        # print(signproductlist)
        signproductnumber = len(signproductlist)
        signproductlists = []
        for j in range(0, signproductnumber):
            tmp = []
            for k in signlist_dict.keys():
                for l in signproductlist[j].keys():
                    if k == l:
                        signlist_dict[k] = signproductlist[j][l]
                        tmp.append(signlist_dict[k])
            signproductlists.append(tmp)
        h = []
        x = []
        # y = []
        for signprolist in signproductlists:
            # y = []
            for k in signlist_dict.keys():
                h.append(k)
            l = dict(zip(h, signprolist))
            x.append(l)
        y.append(x)
    # print(y)
    # print(y[0])
    signinfolists = []
    signinfolists_dict = {}
    for i in range(0, signnumber):
        tmp = []
        for j in signinfo_dict.keys():
            for k in signinfolist[i].keys():
                if j == k and j != 'signProductList':
                    signinfo_dict[j] = signinfolist[i][j]
                    signinfo_dict['signProductList'] = y[i]
                    tmp.append(signinfo_dict[j])
        tmp = tmp + [signinfo_dict['signProductList']]

        # print(tmp)
        # tmp = tmp + signinfo_dict['signProductList']
        signinfolists.append(tmp)
    # print(signinfolists)
    listone = []
    listtwo = []
    for signinfo_list in signinfolists:
        for k in signinfo_dict.keys():
            listone.append(k)
        signinfolists_dict = dict(zip(listone, signinfo_list))
        listtwo.append(signinfolists_dict)
    # print(json.dumps(listtwo))
    return listtwo
    # print(listtwo)

    # y.append(x)
    # print(y)

    #     tmp_list = []
    #     for sign_j in signinfo_dict.keys():
    #         for sign_k in signinfolist[number].keys():
    #             if sign_j == sign_k:
    #                 signinfo_dict[sign_j] = signinfolist[number][sign_k]
    #                 tmp_list.append(signinfo_dict[sign_j])
    #     all_signproductlist.append(tmp_list)
    # h = []
    # x = []
    # for productlist in all_signproductlist:
    #     for k in signinfo_dict.keys():
    #         h.append(k)
    #     l = dict(zip(h,productlist))
    #     x.append(l)
    # print(x)


# 收货地址，邮寄地址
def get_deliveryAddressList():
    data_address = json.dumps({
        "id": agentid,
        "token": token,
        "type": 4
    })
    res = requests.post(url=url_detail, data=data_address, headers=headers)
    res_text = json.loads(res.text)
    address_dict = {"id": '', "agentId": '', "type": '', "acceptor": '', "phoneNum": '', "address": '', "area": '',
                    "areaId": '', "city": '', "cityId": '', "province": '', "provinceId": '', "remark": '', "email": ''}
    address_list = res_text['data']['result']['deliveryAddressList']
    address_number = int(len(address_list))
    addresslists = []
    l = {}
    for i in range(0, address_number):
        tmp = []
        for j in address_dict.keys():
            for k in address_list[i].keys():
                if j == k:
                    address_dict[j] = address_list[i][k]
        addresslists.append(address_dict.copy())
    # print(json.dumps(addresslists))
    return addresslists


# personalPaymentList
def get_personalPaymentList():
    data_personlpay = json.dumps({
        "id": agentid,
        "token": token,
        "type": 4
    })
    res = requests.post(url=url_detail, data=data_personlpay, headers=headers)
    res_text = json.loads(res.text)
    personlpaydict = {"idCard": '', "idCardAttach": '', "id": '', "agentId": '', "name": '', "effectiveDate": '',
                      "effectiveDateEnd": '', "reasons": ''}
    personal_list = res_text['data']['result']['personalPaymentList']
    personal_number = int(len(personal_list))
    personallists = []
    # l = {}
    for i in range(0, personal_number):
        tmp = []
        for j in personlpaydict.keys():
            for k in personal_list[i].keys():
                if j == k:
                    personlpaydict[j] = personal_list[i][k]
        personallists.append(personlpaydict.copy())
    # print(json.dumps(personallists))
    return personallists


# thirdPaymentList
def get_thirdpaymentlist():
    data_personlpay = json.dumps({
        "id": agentid,
        "token": token,
        "type": 4
    })
    res = requests.post(url=url_detail, data=data_personlpay, headers=headers)
    res_text = json.loads(res.text)
    thirdpersonaldict = {"idCard": '', "idCardAttach": '', "id": '', "agentId": '', "name": '', "effectiveDate": '',
                         "effectiveDateEnd": '', "reasons": ''}
    thirdpersonal_list = res_text['data']['result']['personalPaymentList']
    personal_number = int(len(thirdpersonal_list))
    thirdlists = []
    # l = {}
    for i in range(0, personal_number):
        tmp = []
        for j in thirdpersonaldict.keys():
            for k in thirdpersonal_list[i].keys():
                if j == k:
                    thirdpersonaldict[j] = thirdpersonal_list[i][k]
        thirdlists.append(thirdpersonaldict.copy())
    # print(json.dumps(thirdlists))
    return thirdlists


# salesResolveList
def get_salesResolveList():
    data_personlpay = json.dumps({
        "id": agentid,
        "token": token,
        "type": 4
    })
    res = requests.post(url=url_detail, data=data_personlpay, headers=headers)
    res_text = json.loads(res.text)
    salesdict = {"id": '', "agentId": '', "largeClassId": '', "largeClassName": '', "month": '', "sales": ''}
    salesResolve_List = res_text['data']['result']['salesResolveList']
    sales_number = int(len(salesResolve_List))
    saleslists = []
    # l = {}
    for i in range(0, sales_number):
        tmp = []
        for j in salesdict.keys():
            for k in salesResolve_List[i].keys():
                if j == k:
                    salesdict[j] = salesResolve_List[i][k]
        saleslists.append(salesdict.copy())
    # print(json.dumps(saleslists))
    return saleslists


# 已开户经销提交续签获得resultid,empid
agentAccountType, corporateName, area, areaId, businessScope, city, cityId, agentName, address, \
companyId, companyName, companyType, bail, branchAbbr, branchCode, branchId, branchName, creditCode, email, establishmentDate, \
firstAmount, orgCode, orgName, orgId, province, provinceId, registerCapital, telephone, idStr, isSaled, agentType, \
lastSalesVolume, originalSupplier, preSignedProduct, agentContent, warehouse, payInPower = get_many_messages_type_one()

corporateIdcardNum, corporateIdcard, businessLicence, isDepositary, paymentProof, depositaryName, \
depositarySex, depositaryContent, depositaryLetterAttach, depositaryIdcardAttach, depositaryIdcard = get_many_messages_type_two()

otherAppoint, paymentWay, priceOtherAppoint, businessChannel, businessAreaRemark, stockRequire, \
signedProductAttach, totalDiscount1, totalDiscount2, totalNumber1, totalNumber2 = get_many_messages_type_four()

contract_arealist = get_contract_arealist()

contract_signproductlist = get_contract_signproductlist()

deliveryAddressList = get_deliveryAddressList()

personalPaymentList = get_personalPaymentList()

thirdpaymentlist = get_thirdpaymentlist()

salesResolveList = get_salesResolveList()

# 取empid
def get_a_resultid():
    agentid = get_agentid()
    data_submit = json.dumps({
        "oldId": agentid,
        "agentType": 1,
        "creatorId": userid,
        "creatorName": name,
        "baseStatus": "2",
        "infoStatus": "2",
        "contractStatus": "2",
        "base": {
            "agentAccountType": agentAccountType,
            "branchId": branchId,
            "branchName": branchName,
            "companyId": companyId,
            "companyName": companyName,
            "branchCode": branchCode,
            "branchAbbr": branchAbbr,
            "orgId": orgId,
            "orgName": orgName,
            "orgCode": orgCode,
            "agentName": agentName,
            "creditCode": creditCode,
            "address": address,
            "establishmentDate": establishmentDate,
            "companyType": companyType,
            "corporateName": corporateName,
            "telephone": telephone,
            "email": email,
            "registerCapital": registerCapital,
            "businessScope": businessScope,
            "bail": bail,
            "firstAmount": firstAmount,
            "isSaled": isSaled,
            "lastSalesVolume": lastSalesVolume,
            "originalSupplier": originalSupplier,
            "agentId": agentid,
            "areaId": areaId,
            "area": area,
            "cityId": cityId,
            "city": city,
            "provinceId": provinceId,
            "province": province,
            "preSignedProduct": preSignedProduct,
            "agentContent": agentContent,
            "warehouse": warehouse,
            "payInPower": payInPower
        },
        "info": {
            "isDepositary": isDepositary,
            "depositaryName": depositaryName,
            "depositarySex": depositarySex,
            "depositaryIdcard": depositaryIdcard,
            "businessLicence": businessLicence,
            "corporateIdcard": corporateIdcard,
            "depositaryLetterAttach": depositaryLetterAttach,
            "depositaryIdcardAttach": depositaryIdcardAttach,
            "paymentProof": paymentProof,
            "depositaryContent": depositaryContent,
            "corporateIdcardNum": corporateIdcardNum
        },
        "contract": {
            "contractStartDate": curr_time_start,
            "contractEndDate": curr_time_end,
            "otherAppoint": otherAppoint,
            "priceOtherAppoint": priceOtherAppoint,
            "businessChannel": businessChannel,
            "totalNumber1": totalNumber1,
            "totalDiscount1": totalDiscount1,
            "totalNumber2": totalNumber2,
            "totalDiscount2": totalDiscount2,
            "paymentWay": paymentWay,
            "stockRequire": stockRequire,
            "signedProductAttach": signedProductAttach,
            "businessAreaRemark": businessAreaRemark
        },
        "areaList": contract_arealist,
        "signInfoList": contract_signproductlist,
        "deliveryAddressList": deliveryAddressList,
        "personalPaymentList": personalPaymentList,
        "thirdPaymentList": thirdpaymentlist,
        "salesResolveList": salesResolveList,
        "token": token
    })
    # print(data_submit)
    res = requests.post(url=url_continueSubmit, data=data_submit, headers=headers)
    res_text = json.loads(res.text)
    # print(res_text)
    # print(agentid)
    empId = res_text['data']['result']
    # print(empId)
    return empId


if __name__ == '__main__':
    # get_contract_signproductlist()
    # get_many_messages_type_one()
    # get_contract_arealist()
    # get_deliveryAddressList()
    # get_personalPaymentList()
    # get_thirdpaymentlist()
    # get_salesResolveList()
    get_a_resultid()
    print("")