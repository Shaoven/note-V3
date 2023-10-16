import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn
from businessCommon.create_remind_notes import CreateRemindNotes


@class_case_log
class TestGetRemindNoteList(unittest.TestCase):
    """查看日历下便签接口 level1"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['GetRemindNoteList']['Path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    createRemindNote = CreateRemindNotes()

    def testCase01_major(self):
        """查看日历下便签"""
        info('STEP:新建一条日历便签')
        remind_note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 9999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')

        # 校验输出结果
        expect_output = {'responseTime': int, 'webNotes': [
            {'noteId': str, 'createTime': int, 'star': int, 'remindTime': int, 'remindType': int,
             'infoVersion': int, 'infoUpdateTime': int, 'groupId': str, 'title': str, 'summary': str, 'thumbnail': str,
             'contentVersion': int, 'contentUpdateTime': int}]}
        CheckTools().check_output(expect_output, res.json())

        # 校验数据源
        note_ids = []
        for i in res.json()['webNotes']:
            note_ids.append(i['noteId'])
        self.assertIn(remind_note_id[0], note_ids, msg='日历便签新建失败')
