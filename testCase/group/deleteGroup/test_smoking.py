import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn


class TestDeleteGroup(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['DeleteGroup']['Path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    createGroupPath = apiConfig['CreateGroup']['Path']
    createGroupUrl = host + createGroupPath
    getGroupListPath = apiConfig['GetGroupList']['Path']
    getGroupListUrl = host + getGroupListPath

    def testCase01_major(self):
        """删除1个分组"""
        info('STEP:新增分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')

        info('STEP:删除分组')
        delete_group_body = {
            'groupId': group_id
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, delete_group_body)
        # 判断状态码
        self.assertIn('responseTime', res.json().keys(), msg='参数responseTime未返回')
        # 校验输出结果
        expect_output = {'responseTime': int}
        CheckTools().check_output(expect_output, res.json())

        info('获取分组列表，校验数据源')
        get_group_list_body = {}
        get_group_list_res = self.apiRe.note_post(self.getGroupListUrl, self.user_id, self.sid, get_group_list_body)
        group_ids = []
        for i in get_group_list_res.json()['noteGroups']:
            group_ids.append(i['groupId'])

        # 判断数据源
        self.assertNotIn(group_id, group_ids, msg='删除失败')

