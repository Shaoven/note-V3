import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn


class TestUpdateGroup(unittest.TestCase):
    """更新分组接口level1"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['CreateGroup']['Path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    sidB = envConfig['sidB']
    user_id = envConfig['user_id']
    userB_id = envConfig['userB_id']
    apiRe = ApiRe()
    getGroupListPath = apiConfig['GetGroupList']['Path']
    getGroupListUrl = host + getGroupListPath

    def testCase01_group_id_not_me_update_group(self):
        """用户A更新用户B的分组"""
        info('STEP:用户B新建一个分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        res = self.apiRe.note_post(self.url, self.userB_id, self.sidB, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:用户A更新用户B的分组信息')
        res2 = self.apiRe.note_post(self.url, self.user_id, self.sid, body)

        # 校验状态码
        self.assertEqual(412, res2.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
