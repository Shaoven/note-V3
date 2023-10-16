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
class TestGetRecycleNote(unittest.TestCase):
    """查看回收站下便签 level1"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    user_id = envConfig['user_id']
    sid = envConfig['sid']
    host = envConfig['host']
    startIndex = 0
    rows = 999
    path = f"/v3/notesvr/user/{user_id}/invalid/startindex/{startIndex}/rows/{rows}/notes"
    url = host + path
    apiRe = ApiRe()
    getRemindNoteListPath = apiConfig['GetRemindNoteList']['Path']
    getRemindNoteListUrl = host + getRemindNoteListPath
    createRemindNote = CreateRemindNotes()
    deleteRemindNote = DeleteRemindNotes()
    createNote = CreateNotes()
    deleteNote = DeleteNotes()
    deleteNotePath = apiConfig['DeleteNote']['Path']
    deleteNoteUrl = host + deleteNotePath

    def testCase01_major(self):
        """查看回收站下便签"""
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

        info('STEP:查看回收站下这两条便签')
        res = self.apiRe.note_get(self.url, self.sid)
        self.assertEqual(200, res.status_code, msg='状态码有问题')
        self.assertEqual(2, len(res.json()['webNotes']), msg='返回的数量不等于2')
        expect_out = {'responseTime': int, 'webNotes': [
            {'noteId': str, 'createTime': int, 'star': int, 'remindTime': int, 'remindType': int, 'infoVersion': int,
             'infoUpdateTime': int, 'groupId': str, 'title': str, 'summary': str, 'thumbnail': str,
             'contentVersion': int, 'contentUpdateTime': int, }]}
        CheckTools().check_output(expect_out, res.json())
