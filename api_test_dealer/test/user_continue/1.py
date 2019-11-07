# -*- coding: utf-8 -*-

' a test module '
import unittest
import requests
import json

__author__ = 'lvxinjin'
a = {
    'id': 4168,
    'agentId': 2560,
    'type': 2,
    'acceptor': '吕',
    'phoneNum': '15067126937',
    'address': '123',
    'area': '东城区',
    'areaId': 3,
    'city': '北京市',
    'cityId': 2,
    'province': '北京',
    'provinceId': 1,
    'remark': None,
    'email': '610634528@qq.com'
}
b = json.dumps(a)

print(b)
print(json.loads(b))
