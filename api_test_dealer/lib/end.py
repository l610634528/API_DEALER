import requests
import json
url = "http://test.waterhome.zcabc.com/app/myorder/endOrder"
data = {
    "id":"5570",
    "orderFinishStatus":1,
    "orderFinishRemark":"",
    "token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIiLCJhdWQiOiIiLCJpYXQiOjE1Njk4MjE5MDQsImlkIjoxMn0.frOIY84cyNyDrglpeHgbP1haC-8gWZaxGEdb75XeP54"
    }
res = requests.post(url=url,data=data)
print(res.text)
# restext = json.loads(res.text)
# print(restext)