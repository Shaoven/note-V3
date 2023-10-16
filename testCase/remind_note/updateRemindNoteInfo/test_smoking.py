import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn


@class_case_log
class TestUpdateRemindNoteInfo(unittest.TestCase):
    """更新便签主体接口level1"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['CreateNoteInfo']['Path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    createNotePath = apiConfig['CreateNote']['Path']
    createNoteUrl = host + createNotePath
    getRemindNoteListPath = apiConfig['GetRemindNoteList']['Path']
    getRemindNoteListUrl = host + getRemindNoteListPath

    def testCase01_major(self):
        """更新日历便签主体"""
        info('STEP:新建日历便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        remind_time = int(time.time() * 1000)
        body = {
            'noteId': note_id,
            'remindTime': remind_time,
            'remindType': 0
        }
        # 请求上传便签信息主体接口，并获取接口返回结果
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码有问题')

        info('STEP:更新日历便签主体')
        update_body = {
            'noteId': note_id,
            'remindTime': remind_time,
            'remindType': 1
        }
        update_res = self.apiRe.note_post(self.url, self.user_id, self.sid, update_body)
        self.assertEqual(200, update_res.status_code, msg='状态码有问题')

        info('STEP:上传日历便签的内容')
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
                self.assertEqual(1, i['remindType'], msg='remindType的值不等于1，更新失败')  # 先描述期望值，再描述结果
