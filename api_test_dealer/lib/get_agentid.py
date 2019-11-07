import sys
sys.path.append('..')
# from config import *
from lib.dealer_login_token import *

from config.config import dealer_url

url_info = dealer_url + '/cba/agentInfo/selectAgentInfoList'
headers = {"Content-Type": "application/json"}

token, name, uid = dealer_login()
userid = str(uid)


def get_id():
    data_info = json.dumps({
        "tag": 4,
        "userId": userid,
        "keyword": "",
        "companyId": "",
        "branchId": "",
        "orgId": "",
        "agentStatusParam": 8,
        "page": 1,
        "size": 100,
        "token": token
    })
    res = requests.post(url=url_info, data=data_info, headers=headers)
    res_text = json.loads(res.text)
    for i in range(0, 100):
        if res_text['data']['result']['records'][i]['agentStatusText'] == '已开户':
            agent_id = res_text['data']['result']['records'][i]['id']
            print(i)
            return agent_id

# 已开户未续签,但提交续签的未审核的也是状态2
def get_agentid():
    data_info = json.dumps({
        "tag": 4,
        "userId": userid,
        "keyword": "",
        "companyId": "",
        "branchId": "",
        "orgId": "",
        "agentStatusParam": 8,
        "page": 1,
        "size": 100,
        "token": token
    })
    res = requests.post(url=url_info, data=data_info, headers=headers)
    res_text = json.loads(res.text)
    for i in range(0, 10):
        if res_text['data']['result']['records'][i]['agentStatusText'] == '已开户' and \
                res_text['data']['result']['records'][i]['continueFlag'] == 2:
            print(i)
            agent_id = res_text['data']['result']['records'][i]['id']
            return agent_id


if __name__ == '__main__':
    get_id()
    print(get_agentid())
