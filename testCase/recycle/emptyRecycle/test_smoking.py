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
from businessCommon.create_notes import CreateNotes
from businessCommon.delete_notes import DeleteNotes


@class_case_log
class TestEmptyRecycle(unittest.TestCase):
    """删除/清空回收站便签 level1"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    user_id = envConfig['user_id']
    sid = envConfig['sid']
    host = envConfig['host']
    path = apiConfig['EmptyRecycle']['Path']
    url = host + path
    apiRe = ApiRe()
    createRemindNote = CreateRemindNotes()
    deleteRemindNote = DeleteRemindNotes()
    createNote = CreateNotes()
    deleteNote = DeleteNotes()
    startIndex = 0
    rows = 9999
    recycleNotePath = f'/v3/notesvr/user/{user_id}/invalid/startindex/{startIndex}/rows/{rows}/notes'
    recycleNoteUrl = host + recycleNotePath
    deleteNotePath = apiConfig['DeleteNote']['Path']
    deleteNoteUrl = host + deleteNotePath

    def testCase01_major(self):
        """删除/清空回收站便签"""
        info('STEP:清空所有普通便签和日历便签')
        self.deleteNote.delete_notes()
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建1条日历便签和1条普通便签')
        note_id = self.createNote.create_notes(1)
        remind_note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:删除这两条便签')
        delete_body = {
            'noteId': note_id[0]
        }
        delete_body02 = {
            'noteId': remind_note_id[0]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)
        delete_res02 = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body02)

        info('STEP:清空这2条便签')
        body = {
            'noteIds': [note_id[0], remind_note_id[0]]
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验输出结果
        expect_out = {'responseTime': int}
        CheckTools().check_output(expect_out, res.json())

        # 校验数据源
        info('STEP:请求回收站便签，检查是否被清空')
        recycle_note_res = self.apiRe.note_get(self.recycleNoteUrl, self.sid)
        self.assertEqual(200, recycle_note_res.status_code, msg='状态码异常')
        self.assertEqual(0, len(recycle_note_res.json()['webNotes']), msg='回收站中的便签未被清空')
