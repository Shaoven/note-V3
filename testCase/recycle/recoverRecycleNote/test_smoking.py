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
class TestRecoverRecycleNote(unittest.TestCase):
    """恢复回收站便签 level1"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    user_id = envConfig['user_id']
    sid = envConfig['sid']
    host = envConfig['host']
    path = f"/v3/notesvr/user/{user_id}/notes"
    url = host + path
    apiRe = ApiRe()
    createRemindNote = CreateRemindNotes()
    deleteRemindNote = DeleteRemindNotes()
    createNote = CreateNotes()
    deleteNote = DeleteNotes()
    deleteNotePath = apiConfig['DeleteNote']['Path']
    deleteNoteUrl = host + deleteNotePath
    getRemindNoteListPath = apiConfig['GetRemindNoteList']['Path']
    getRemindNoteListUrl = host + getRemindNoteListPath
    startIndex = 0
    rows = 9999
    getHomeNotePath = f'/v3/notesvr/user/{user_id}/home/startindex/{startIndex}/rows/{rows}/notes'
    getHomeNoteUrl = host + getHomeNotePath

    def testCase01_major(self):
        """恢复回收站便签"""
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

        info('STEP:恢复这两条便签')
        body = {
            'userId': self.user_id,
            'noteIds': [note_id[0]]
        }
        body02 = {
            'userId': self.user_id,
            'noteIds': [remind_note_id[0]]
        }
        res = self.apiRe.note_patch(self.url, self.sid, body)
        res02 = self.apiRe.note_patch(self.url, self.sid, body02)
        self.assertEqual(200, res.status_code, msg='状态码异常')
        self.assertEqual(200, res02.status_code, msg='状态码异常')
        # 校验数据源
        info('STEP:获取首页便签列表')
        home_note_res = self.apiRe.note_get(self.getHomeNoteUrl, self.sid)
        home_note_ids = []
        for i in home_note_res.json()['webNotes']:
            home_note_ids.append(i['noteId'])
        self.assertEqual(note_id[0], home_note_ids[0], msg='普通便签恢复失败')

        info('STEP:获取日历便签列表')
        remind_note_body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 9999
        }
        remind_note_res = self.apiRe.note_post(self.getRemindNoteListUrl, self.user_id, self.sid,
                                               remind_note_body)
        remind_note_ids = []
        for m in remind_note_res.json()['webNotes']:
            remind_note_ids.append(m['noteId'])
        self.assertIn(remind_note_id[0], remind_note_ids, msg='日历便签恢复失败')
