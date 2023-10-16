import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn


@class_case_log
class TestDeleteGroup(unittest.TestCase):
    """删除分组接口 接口handle"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['DeleteGroup']['Path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    sidB = envConfig['sidB']
    user_id = envConfig['user_id']
    userB_id = envConfig['userB_id']
    apiRe = ApiRe()
    createGroupPath = apiConfig['CreateGroup']['Path']
    createGroupUrl = host + createGroupPath
    createNoteInfoPath = apiConfig['CreateNoteInfo']['Path']
    createNoteInfoUrl = host + createNoteInfoPath
    createNotePath = apiConfig['CreateNote']['Path']
    createNoteUrl = host + createNotePath
    getGroupListPath = apiConfig['GetGroupList']['Path']
    getGroupListUrl = host + getGroupListPath

    def testCase01_group_id_not_exist(self):
        """数值限制 groupId的值不存在"""
        info('前置步骤：清空所有分组')
        info('STEP:请求删除分组接口')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        body = {
            'groupId': group_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase02_number_limit(self):
        """数值限制 删除的分组A中有1条便签数据"""
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        # 校验状态码
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:新建分组便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        create_note_info_body = {
            'noteId': note_id,
            'groupId': group_id
        }
        create_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid,
                                                    create_note_info_body)
        # 校验状态码
        self.assertEqual(200, create_note_info_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:新建分组便签内容')
        create_note_body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': create_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        create_note_res = self.apiRe.note_post(self.createNoteUrl, self.user_id, self.sid, create_note_body)
        # 校验状态码
        self.assertEqual(200, create_note_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:请求删除分组接口')
        body = {
            'groupId': group_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(412, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase03_state_limit(self):
        """状态限制 回收站中有1个分组A"""
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        # 校验状态码
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:请求删除分组接口')
        body = {
            'groupId': group_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:再次请求删除分组接口')
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')

    def testCase04_userA_delete_userB_group(self):
        """操作对象 用户A删除用户B的分组"""
        info('用户B新建分组')
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.userB_id, self.sidB, create_group_body)
        # 校验状态码
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:用户A请求删除用户B的分组')
        body = {
            'groupId': group_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        # self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        # 校验用户B的分组是否还在
        info('STEP:用户B请求获取分组列表')
        get_group_list_body = {}
        get_group_list_res = self.apiRe.note_post(self.getGroupListUrl, self.userB_id, self.sidB, get_group_list_body)
        group_ids = []
        for i in get_group_list_res.json()['noteGroups']:
            group_ids.append(i['groupId'])

        self.assertIn(group_id, group_ids, msg='分组不存在')
