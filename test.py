import requests
import time
import unittest

url = 'http://note-api.wps.cn' + '/v3/notesvr/set/notegroup'
headers = {
    'Content-Type': 'application/json',
    'X-user-key': '922061821',
    'Cookie': 'wps_sid=V02SG3oIwfZGY3-EWrNqRBP1J1oAr6E00ab36a440036f58bfd'
}

groupId = str(int(time.time() * 1000)) + '_test_groupId'
groupName = str(int(time.time() * 1000)) + '_test_groupName'
body = {
    'groupId': groupId,
    'groupName': groupName,
    'order': 0
}
res = requests.post(url=url, headers=headers, json=body)
assert res.status_code == 200
assert 'responseTime' in res.json().keys()
assert type(res.json()['responseTime']) == int
assert 'updateTime' in res.json().keys()
assert type(res.json()['updateTime']) == int
assert len(res.json().keys()) == 2

get_group_url = 'http://note-api.wps.cn' + '/v3/notesvr/get/notegroup'
body = {}
get_group_res = requests.post(url=get_group_url, headers=headers, json=body)
groupIds = []
groupNames = []
for item in get_group_res.json()['noteGroups']:
    groupIds.append(item['groupId'])
    groupNames.append(item['groupName'])
assert groupId in groupIds
assert groupName in groupNames

