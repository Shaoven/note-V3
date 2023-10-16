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
class TestCreateRemindNoteInfo(unittest.TestCase):
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
    createNotePath = apiConfig['CreateNote']['Path']
    createNoteUrl = host + createNotePath
    getRemindNoteListPath = apiConfig['GetRemindNoteList']['Path']
    getRemindNoteListUrl = host + getRemindNoteListPath

    def testCase01_userA_create_userB_RemindNoteInfo(self):
        """新建日历便签主体 操作对象：用户A给用户B上传日历便签主体"""
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        remind_time = int(time.time() * 1000)
        body = {
            'noteId': note_id,
            'remindTime': remind_time,
            'remindType': 0
        }
        res = self.apiRe.note_post(self.url, self.userB_id, self.sid, body)
        self.assertEqual(412, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase02_remindType_send_0(self):
        """新建日历便签主体 枚举值校验：remindType=0"""
        info('STEP:新建日历便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        remind_time = int(time.time() * 1000)
        body = {
            'noteId': note_id,
            'remindTime': remind_time,
            'remindType': 0
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:新建日历便签内容')
        remind_note_body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': res.json()['infoVersion'],
            'BodyType': 0
        }
        create_remind_note_res = self.apiRe.note_post(self.createNoteUrl, self.user_id, self.sid, remind_note_body)
        self.assertEqual(200, create_remind_note_res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:获取日历便签列表')
        remind_note_list_body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 9999
        }
        get_remind_note_list = self.apiRe.note_post(self.getRemindNoteListUrl, self.user_id, self.sid,
                                                    remind_note_list_body)
        for i in get_remind_note_list.json()['webNotes']:
            if i['noteId'] == note_id:
                self.assertEqual(0, i['remindType'], msg='remindType的值不等于0')  # 先描述期望值，再描述结果

    def testCase03_remindType_send_1(self):
        """新建日历便签主体 枚举值校验：remindType=1"""
        info('STEP:新建日历便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        remind_time = int(time.time() * 1000)
        body = {
            'noteId': note_id,
            'remindTime': remind_time,
            'remindType': 1
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:新建日历便签内容')
        remind_note_body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': res.json()['infoVersion'],
            'BodyType': 0
        }
        create_remind_note_res = self.apiRe.note_post(self.createNoteUrl, self.user_id, self.sid, remind_note_body)
        self.assertEqual(200, create_remind_note_res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:获取日历便签列表')
        remind_note_list_body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 9999
        }
        get_remind_note_list = self.apiRe.note_post(self.getRemindNoteListUrl, self.user_id, self.sid,
                                                    remind_note_list_body)
        for i in get_remind_note_list.json()['webNotes']:
            if i['noteId'] == note_id:
                self.assertEqual(1, i['remindType'], msg='remindType的值不等于1')  # 先描述期望值，再描述结果

    def testCase04_remindType_send_2(self):
        """新建日历便签主体 枚举值校验：remindType=2"""
        info('STEP:新建日历便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        remind_time = int(time.time() * 1000)
        body = {
            'noteId': note_id,
            'remindTime': remind_time,
            'remindType': 2
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:新建日历便签内容')
        remind_note_body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': res.json()['infoVersion'],
            'BodyType': 0
        }
        create_remind_note_res = self.apiRe.note_post(self.createNoteUrl, self.user_id, self.sid, remind_note_body)
        self.assertEqual(200, create_remind_note_res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:获取日历便签列表')
        remind_note_list_body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 9999
        }
        get_remind_note_list = self.apiRe.note_post(self.getRemindNoteListUrl, self.user_id, self.sid,
                                                    remind_note_list_body)
        for i in get_remind_note_list.json()['webNotes']:
            if i['noteId'] == note_id:
                self.assertEqual(2, i['remindType'], msg='remindType的值不等于2')  # 先描述期望值，再描述结果
