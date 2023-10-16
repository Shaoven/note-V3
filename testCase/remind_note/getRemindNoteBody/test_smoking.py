import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn
from businessCommon.create_remind_notes import CreateRemindNotes
from businessCommon.delete_remind_notes import DeleteRemindNotes


@class_case_log
class TestGetRemindNoteBody(unittest.TestCase):
    """获取日历便签内容接口 level1"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['GetNoteBody']['Path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    createRemindNote = CreateRemindNotes()
    deleteRemindNote = DeleteRemindNotes()

    def testCase01_major(self):
        """获取日历便签内容"""
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:获取日历便签内容')
        body = {
            'noteIds': [note_id[0]],
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')

        # 校验输出结果
        expect_output = {'responseTime': int, 'noteBodies': [
            {'summary': str, 'noteId': str, 'bodyType': int, 'body': str, 'contentVersion': int,
             'contentUpdateTime': int, 'title': str, 'valid': int}]}
        CheckTools().check_output(expect_output, res.json())
