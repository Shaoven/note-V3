import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn
from businessCommon.delete_notes import DeleteNotes


@class_case_log
class TestCreateRemindNote(unittest.TestCase):
    """新建日历便签接口level1"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['CreateNote']['Path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    deleteNote = DeleteNotes()
    createNoteInfoPath = apiConfig['CreateNoteInfo']['Path']
    createNoteInfoUrl = host + createNoteInfoPath
    getRemindNoteListPath = apiConfig['GetRemindNoteList']['Path']
    getRemindNoteListUrl = host + getRemindNoteListPath

    def testCase01_major(self):
        """新建日历便签"""
        info('STEP:新建日历便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        remind_time = int(time.time() * 1000)
        remind_note_info_body = {
            'noteId': note_id,
            'remindTime': remind_time,
            'remindType': 0
        }
        remind_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid,
                                                    remind_note_info_body)
        self.assertEqual(200, remind_note_info_res.status_code, msg='状态码异常')

        info('STEP:新建日历便签内容')
        body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': remind_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验输出结果
        expect_output = {'responseTime': int, 'contentVersion': int, 'contentUpdateTime': int}
        CheckTools().check_output(expect_output, res.json())

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
        remind_note_ids = []
        for i in get_remind_note_list.json()['webNotes']:
            remind_note_ids.append(i['noteId'])
        self.assertIn(note_id, remind_note_ids, msg='日历便签新建不成功')
