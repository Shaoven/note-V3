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
    """新建分组接口level1"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['CreateGroup']['Path']
    mustKey = apiConfig['CreateGroup']['must_key']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    getGroupListPath = apiConfig['GetGroupList']['Path']
    get_group_list_url = host + getGroupListPath

    def testCase01_major(self):
        """新增1个分组"""
        info('STEP: 新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
        expect_output = {'responseTime': int, 'updateTime': int}
        # 校验输出结果
        CheckTools().check_output(expect_output, res.json())
        # 校验数据源
        info('STEP: 获取分组')
        get_group_list_body = {}
        get_group_list_res = self.apiRe.note_post(self.get_group_list_url, self.user_id, self.sid, get_group_list_body)
        group_ids = []
        for i in get_group_list_res.json()['noteGroups']:
            group_ids.append(i['groupId'])
        self.assertIn(group_id, group_ids, msg='分组未新建成功')
