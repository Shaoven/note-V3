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
    """删除分组接口 接口input"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['DeleteGroup']['Path']
    mustKey = apiConfig['DeleteGroup']['must_key']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    createGroupPath = apiConfig['CreateGroup']['Path']
    createGroupUrl = host + createGroupPath
    createNoteInfoPath = apiConfig['CreateNoteInfo']['Path']
    createNoteInfoUrl = host + createNoteInfoPath
    createNotePath = apiConfig['CreateNote']['Path']
    createNoteUrl = host + createNotePath
    special = apiConfig['DeleteGroup']['special']

    @parameterized.expand(mustKey)
    def testCase01_input_must_key(self, dic):
        """删除分组接口 必填校验"""
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:请求删除分组接口')
        delete_group_body = {
            'groupId': group_id,
        }
        delete_group_body.pop(dic['key'])
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, delete_group_body)
        self.assertEqual(dic['code'], res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase02_lost_x_user_key(self):
        """删除分组接口 未传入X-user-key"""
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:请求删除分组接口')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid}'
        }
        delete_group_body = {
            'groupId': group_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, delete_group_body, headers)
        self.assertEqual(412, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase03_group_id_is_too_long(self):
        """删除分组接口 group_id的长度=1000"""
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId' + 'test'*250
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        # self.assertEqual(200, create_group_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:请求删除分组接口')
        body = {
            'groupId': group_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    @parameterized.expand(special)
    def testCase04_group_id_special(self, spe):
        """删除分组接口 group_id输入特殊字符@#￥%……&*（；"""
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId' + spe
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)

        info('STEP:请求删除分组接口')
        body = {
            'groupId': group_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase05_group_id_english_big_small(self):
        """删除分组接口 group_id输入英文大小写"""
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_GROUPID'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)

        info('STEP:请求删除分组接口')
        body = {
            'groupId': group_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase06_group_id_input_chinese(self):
        """删除分组接口 group_id输入中文"""
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_分组名称'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)

        info('STEP:请求删除分组接口')
        body = {
            'groupId': group_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase07_group_id_input_none(self):
        """删除分组接口 group_id输入空值None"""
        info('STEP:新建分组')
        group_id = None
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)

        info('STEP:请求删除分组接口')
        body = {
            'groupId': group_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase08_group_id_input_kong(self):
        """删除分组接口 group_id输入"" """
        info('STEP:新建分组')
        group_id = ""
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)

        info('STEP:请求删除分组接口')
        body = {
            'groupId': group_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase09_group_id_input_sql(self):
        """ 删除分组接口 group_id输入" or " 1= 1 """
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId' + '" or " 1= 1'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)

        info('STEP:请求删除分组接口')
        body = {
            'groupId': group_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase10_group_id_input_sql(self):
        """ 删除分组接口 group_id输入' or ' 1= 1 """
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId' + "' or ' 1= 1"
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)

        info('STEP:请求删除分组接口')
        body = {
            'groupId': group_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
