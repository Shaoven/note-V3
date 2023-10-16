import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn


@class_case_log
class TestUpdateRemindNote(unittest.TestCase):
    """更新日历便签接口level1"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['CreateNote']['Path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    createNoteInfoPath = apiConfig['CreateNoteInfo']['Path']
    createNoteInfoUrl = host + createNoteInfoPath
    getNoteBodyPath = apiConfig['GetNoteBody']['Path']
    getNoteBodyUrl = host + getNoteBodyPath

    def testCase01_major(self):
        """更新日历便签内容"""
        info('STEP:新建日历便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        remind_time = int(time.time() * 1000)
        get_note_info_body = {
            'noteId': note_id,
            'remindTime': remind_time,
            'remindType': 0
        }
        get_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid, get_note_info_body)
        # 校验状态码
        self.assertEqual(200, get_note_info_res.status_code, msg='状态码有问题')

        info('STEP:新建便签内容')
        body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': get_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码异常')

        info('STEP:更新便签内容')
        update_body = {
            'noteId': note_id,
            'title': 'test_update',
            'summary': 'test_update',
            'body': 'test_update',
            'localContentVersion': get_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        update_res = self.apiRe.note_post(self.url, self.user_id, self.sid, update_body)
        # 校验状态码
        self.assertEqual(200, update_res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:请求获取便签内容')
        note_body = {
            'noteIds': [note_id]
        }
        note_body_res = self.apiRe.note_post(self.getNoteBodyUrl, self.user_id, self.sid, note_body)
        self.assertEqual(200, note_body_res.status_code, msg='状态码异常')
        for i in note_body_res.json()['noteBodies']:
            if i['noteId'] == note_id:
                self.assertEqual(i['summary'], 'test_update', msg='summary未更新成功')
                self.assertEqual(i['title'], 'test_update', msg='title未更新成功')
                self.assertEqual(i['body'], 'test_update', msg='body未更新成功')
