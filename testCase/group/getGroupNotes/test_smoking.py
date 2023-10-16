import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn


@class_case_log
class TestGetGroupNotes(unittest.TestCase):
    """获取分组下便签接口level1"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['GetGroupNote']['Path']
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

    # getGroupListPath = apiConfig['GetGroupList']['Path']
    # get_group_list_url = host + getGroupListPath

    def testCase01_major(self):
        """获取分组下的1条便签"""
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

        info('STEP:请求获取分组便签接口')
        body = {
            'groupId': group_id
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
        # 校验输出结果
        expect_output = {'responseTime': int, 'webNotes': [
            {'noteId': str, 'createTime': int, 'star': int, 'remindTime': int, 'remindType': int, 'infoVersion': int,
             'infoUpdateTime': int, 'groupId': str, 'title': str, 'summary': str, 'thumbnail': str,
             'contentVersion': int, 'contentUpdateTime': int}]}
        CheckTools().check_output(expect_output, res.json())
        # 校验是否只有一条便签内容
        self.assertEqual(1, len(res.json()['webNotes']), msg='便签数量不等于1')
        # 校验是否为刚新增的便签内容
        note_ids = []
        for i in res.json()['webNotes']:
            note_ids.append(i['noteId'])
        self.assertIn(note_id, note_ids, msg='刚刚新增的便签不在这个分组便签中')
