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
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    getGroupListPath = apiConfig['GetGroupList']['Path']
    getGroupListUrl = host + getGroupListPath

    def testCase01_major(self):
        """更新1个分组"""
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 判断新建分组的状态是否200
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
        # 更新这个分组
        info('STEP:更新分组')
        update_group_name = str(int(time.time() * 1000)) + 'update_group_name'
        update_body = {
            'groupId': group_id,
            'groupName': update_group_name
        }
        update_res = self.apiRe.note_post(self.url, self.user_id, self.sid, update_body)
        # 判断更新状态
        self.assertEqual(200, update_res.status_code, msg='状态码异常')
        # 校验输出结果
        expect_output = {'responseTime': int, 'updateTime': int}
        CheckTools().check_output(expect_output, update_res.json())

        # 获取分组列表
        info('STEP:获取分组列表，校验数据是否更新成功')
        get_group_list_body = {}
        get_group_list_res = self.apiRe.note_post(self.getGroupListUrl, self.user_id, self.sid,
                                                  get_group_list_body)
        group_names = []
        for i in get_group_list_res.json()['noteGroups']:
            group_names.append(i['groupName'])

        # 判断数据源是否正确
        self.assertIn(update_group_name, group_names, msg='更新失败')
