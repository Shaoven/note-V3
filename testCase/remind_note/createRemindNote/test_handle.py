import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn


@class_case_log
class TestCreateRemindNote(unittest.TestCase):
    """新建日历便签接口level1"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['CreateNote']['Path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    sidB = envConfig['sidB']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    createNoteInfoPath = apiConfig['CreateNoteInfo']['Path']
    createNoteInfoUrl = host + createNoteInfoPath
    getRemindNoteListPath = apiConfig['GetRemindNoteList']['Path']
    getRemindNoteListUrl = host + getRemindNoteListPath

    def testCase01_userB_create_userA_RemindNote(self):
        """操作对象：用户B给用户A上传日历便签"""
        info('STEP:新建日历便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        remind_time = int(time.time() * 1000)
        create_note_info_body = {
            'noteId': note_id,
            'remindTime': remind_time,
            'remindType': 0
        }
        create_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid,
                                                    create_note_info_body)

        info('STEP:新建日历便签内容')
        body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': create_note_info_res.json()['infoVersion'],
            'BodyType': 1.5
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sidB, body)
        self.assertEqual(412, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

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
        self.assertNotIn(note_id, remind_note_ids, msg='日历便签新建不成功')

