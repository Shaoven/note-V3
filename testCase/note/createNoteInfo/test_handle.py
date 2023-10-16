import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn
from businessCommon.create_notes import CreateNotes


@class_case_log
class TestCreateNoteInfo(unittest.TestCase):
    """新建便签主体接口level1"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['CreateNoteInfo']['Path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    userB_id = envConfig['userB_id']
    apiRe = ApiRe()
    createNote = CreateNotes()
    startIndex = 0
    rows = 9999
    getHomeNotePath = f'/v3/notesvr/user/{user_id}/home/startindex/{startIndex}/rows/{rows}/notes'
    getHomeNoteUrl = host + getHomeNotePath
    createNotePath = apiConfig['CreateNote']['Path']
    createNoteUrl = host + createNotePath

    def testCase01_group_id_not_exist(self):
        """约束条件：分组id不存在"""
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        group_id = str(int(time.time() * 1000))
        body = {
            'noteId': note_id,
            'groupId': group_id
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase02_no_send_star(self):
        """约束条件：不传参数star"""
        info('STEP:创建1条便签，不传参数star')
        note_id = self.createNote.create_notes(1)

        # 校验数据源
        info('STEP:请求获取首页便签接口')
        res = self.apiRe.note_get(self.getHomeNoteUrl, self.sid)
        for i in res.json()['webNotes']:
            if i['noteId'] == note_id:
                self.assertEqual(0, i['star'], msg='star的值不等于0')  # 先描述期望值，再描述结果

    def testCase03_star_send_1(self):
        """枚举值校验：star=1"""
        info('STEP:新建便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id,
            'star': 1
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:新建便签内容')
        get_note_body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': res.json()['infoVersion'],
            'BodyType': 0
        }
        create_note_res = self.apiRe.note_post(self.createNoteUrl, self.user_id, self.sid, get_note_body)
        self.assertEqual(200, create_note_res.status_code, msg='状态码异常')
        # 校验数据源
        info('STEP:请求获取首页便签接口')
        res = self.apiRe.note_get(self.getHomeNoteUrl, self.sid)
        for i in res.json()['webNotes']:
            if i['noteId'] == note_id:
                self.assertEqual(1, i['star'], msg='star的值不等于1')  # 先描述期望值，再描述结果

    def testCase04_star_send_0(self):
        """枚举值校验：star=0"""
        info('STEP:新建便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id,
            'star': 0
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:新建便签内容')
        get_note_body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': res.json()['infoVersion'],
            'BodyType': 0
        }
        create_note_res = self.apiRe.note_post(self.createNoteUrl, self.user_id, self.sid, get_note_body)
        self.assertEqual(200, create_note_res.status_code, msg='状态码异常')
        # 校验数据源
        info('STEP:请求获取首页便签接口')
        res = self.apiRe.note_get(self.getHomeNoteUrl, self.sid)
        for i in res.json()['webNotes']:
            if i['noteId'] == note_id:
                self.assertEqual(0, i['star'], msg='star的值不等于0')  # 先描述期望值，再描述结果

    def testCase05_userA_create_userB_note_info(self):
        """操作对象：用户A给用户B上传普通便签主体"""
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id,
            'star': 0
        }
        res = self.apiRe.note_post(self.url, self.userB_id, self.sid, body)
        self.assertEqual(412, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
