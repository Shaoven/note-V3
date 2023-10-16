import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn


class TestGetGroupList(unittest.TestCase):
    """获取分组列表接口level1"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['GetGroupList']['Path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    createGroupPath = apiConfig['CreateGroup']['Path']
    create_group_url = host + createGroupPath

    def testCase01_major(self):
        """获取分组列表"""
        info('STEP:新建一个分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name
        }
        create_group_res = self.apiRe.note_post(self.create_group_url, self.user_id, self.sid, body)
        # 判断新建分组的状态是否200
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        # 获取分组列表
        info('STEP:获取分组列表')
        get_group_list_body = {}
        get_group_list_res = self.apiRe.note_post(self.url, self.user_id, self.sid, get_group_list_body)
        # 判断状态码
        self.assertEqual(200, get_group_list_res.status_code, msg='状态码异常')
        # 校验输出结果
        expect_output = {'requestTime': int, 'noteGroups': [
            {'userId': str, 'groupId': str, 'groupName': str, 'order': int, 'valid': int, 'updateTime': int}]}
        CheckTools().check_output(expect_output, get_group_list_res.json())

