import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn


@class_case_log
class TestCreateGroup(unittest.TestCase):
    """新建分组接口 接口处理"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['CreateGroup']['Path']
    mustKey = apiConfig['CreateGroup']['must_key']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    sidB = envConfig['sidB']
    user_id = envConfig['user_id']
    userB_id = envConfig['userB_id']
    apiRe = ApiRe()
    getGroupListPath = apiConfig['GetGroupList']['Path']
    get_group_list_url = host + getGroupListPath

    def testCase01_order_is_not_exist(self):
        """数值限制：不传参数order时，order默认存储0"""
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
        # 校验数据源
        get_group_list_body = {}
        get_group_list_res = self.apiRe.note_post(self.get_group_list_url, self.user_id, self.sid, get_group_list_body)
        for i in get_group_list_res.json()['noteGroups']:
            if i['groupId'] == group_id:
                self.assertEqual(0, i['order'], msg='order不等于0')

    def testCase02_no_send_order(self):
        """数值限制：不传参数order时，order默认存储0"""
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
        # 校验数据源
        get_group_list_body = {}
        get_group_list_res = self.apiRe.note_post(self.get_group_list_url, self.user_id, self.sid, get_group_list_body)
        for i in get_group_list_res.json()['noteGroups']:
            if i['groupId'] == group_id:
                self.assertEqual(0, i['order'], msg='order不等于0')

    def testCase03_not_me_create_group(self):
        """用户A为用户B新增分组"""
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        res = self.apiRe.note_post(self.url, self.userB_id, self.sid, body)

        # 校验状态码
        self.assertEqual(412, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
