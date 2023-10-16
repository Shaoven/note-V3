import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn


@class_case_log
class TestGetGroupList(unittest.TestCase):
    """获取分组列表接口 接口处理"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['GetGroupList']['Path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    sidB = envConfig['sidB']
    user_id = envConfig['user_id']
    userB_id = envConfig['userB_id']
    apiRe = ApiRe()
    createGroupPath = apiConfig['CreateGroup']['Path']
    createGroupUrl = host + createGroupPath
    deleteGroupPath = apiConfig['DeleteGroup']['Path']
    deleteGroupUrl = host + deleteGroupPath

    def testCase01_no_groups(self):
        """处理数量：没有分组"""
        info('STEP:请求获取分组列表接口,获取所有groupId')
        body = {}
        get_group_list_res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        group_ids = []
        for i in get_group_list_res.json()['noteGroups']:
            group_ids.append(i['groupId'])

        info('STEP:请求删除分组接口，删除分组')
        for d in range(len(group_ids)):
            print(d)
            body = {
                'groupId': group_ids[d]
            }
            delete_group_res = self.apiRe.note_post(self.deleteGroupUrl, self.user_id, self.sid, body)
            # 校验状态
            # self.assertEqual(200, delete_group_res.status_code, msg='状态异常')

        info('STEP:请求获取分组列表接口')
        body = {}
        get_group_list_res02 = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, get_group_list_res02.status_code, msg='状态码异常')
        # 判断返回的noteGroups是否为空
        self.assertEqual('[]', get_group_list_res02.json()['noteGroups'], msg='返回的noteGroups不为空')

    def testCase02_two_group(self):
        """处理数量：有2个分组"""
        info('STEP:请求获取分组列表接口,获取所有groupId')
        body = {}
        get_group_list_res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        group_ids = []
        for i in get_group_list_res.json()['noteGroups']:
            group_ids.append(i['groupId'])

        info('STEP:请求删除分组接口，删除分组')
        for d in range(len(group_ids)):
            print(d)
            body = {
                'groupId': group_ids[d]
            }
            delete_group_res = self.apiRe.note_post(self.deleteGroupUrl, self.user_id, self.sid, body)
            # 校验状态
            # self.assertEqual(200, delete_group_res.status_code, msg='状态异常')

        info('STEP:请求新增分组接口，新增两个分组')
        for i in range(2):
            group_id = str(int(time.time() * 1000)) + '_test_groupId'
            group_name = str(int(time.time() * 1000)) + '_test_groupName'
            body = {
                'groupId': group_id,
                'groupName': group_name,
            }
            create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, body)
            # 校验状态
            self.assertEqual(200, create_group_res.status_code, msg='状态异常')

        info('STEP:请求获取分组列表接口，检查是否获取两个分组')
        body = {}
        get_group_list_res02 = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(2, len(get_group_list_res02.json()['noteGroups']), msg='首页分组数量不等于2')

    def testCase03_not_me_create_group(self):
        """状态限制：回收站中有1个分组"""
        info('STEP:先保证没有任何分组，执行清空分组脚本')
        info('STEP:请求新增分组接口，新增1个分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, body)
        # 校验状态
        self.assertEqual(200, create_group_res.status_code, msg='状态异常')

        info('STEP:请求删除分组接口，删除刚刚新增的分组')
        delete_group_body = {
            'groupId': group_id
        }
        delete_res = self.apiRe.note_post(self.deleteGroupUrl, self.user_id, self.sid, delete_group_body)
        # 校验状态
        self.assertEqual(200, delete_res.status_code, msg='状态异常')

        info('STEP:请求获取分组列表')
        body = {}
        get_group_list_res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, get_group_list_res.status_code, msg='状态异常')
        self.assertEqual(0, len(get_group_list_res.json()['noteGroups']), msg='首页分组列表中还存在分组')
