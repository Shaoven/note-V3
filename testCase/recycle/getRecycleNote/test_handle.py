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
    """查看回收站下便签 接口handle"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    user_id = envConfig['user_id']
    userB_id = envConfig['userB_id']
    sid = envConfig['sid']
    sidB = envConfig['sidB']
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
    recoverNotePath = f'/v3/notesvr/user/{user_id}/notes'
    recoverNoteUrl = host + recoverNotePath
    emptyRecyclePath = apiConfig['EmptyRecycle']['Path']
    emptyRecycleUrl = host + emptyRecyclePath

    def testCase01_rows_number_limit(self):
        """查看回收站下便签接口 数值限制：用户存在2条便签，startIndex=0，rows=1"""
        info('STEP:清空所有普通便签和日历便签')
        self.deleteNote.delete_notes()
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建2条普通便签')
        note_id = self.createNote.create_notes(2)

        info('STEP:删除这两条便签')
        delete_body = {
            'noteId': note_id[0]
        }
        delete_body02 = {
            'noteId': note_id[1]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)
        delete_res02 = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body02)

        info('STEP:请求查看回收站下便签接口')
        start_index = 0
        rows = 1
        path = f'/v3/notesvr/user/{self.user_id}/invalid/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(1, len(res.json()['webNotes']), msg='返回的数据不是1条')
        for i in res.json()['webNotes']:
            self.assertIn(i['noteId'], note_id, msg='便签不在回收站中')

    def testCase02_rows_number_limit(self):
        """查看回收站下便签接口 数值限制：用户存在2条便签，startIndex=0，rows=3"""
        info('STEP:清空所有普通便签和日历便签')
        self.deleteNote.delete_notes()
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建2条普通便签')
        note_id = self.createNote.create_notes(2)

        info('STEP:删除这两条便签')
        delete_body = {
            'noteId': note_id[0]
        }
        delete_body02 = {
            'noteId': note_id[1]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)
        delete_res02 = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body02)

        info('STEP:请求查看回收站下便签接口')
        start_index = 0
        rows = 3
        path = f'/v3/notesvr/user/{self.user_id}/invalid/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(2, len(res.json()['webNotes']), msg='返回的数据不是2条')
        for i in res.json()['webNotes']:
            self.assertIn(i['noteId'], note_id, msg='便签不在回收站中')

    def testCase03_rows_number_limit(self):
        """查看回收站下便签接口 数值限制：用户存在2条普通便签，startIndex=0，rows=0"""
        info('STEP:清空所有普通便签和日历便签')
        self.deleteNote.delete_notes()
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建2条普通便签')
        note_id = self.createNote.create_notes(2)

        info('STEP:删除这两条便签')
        delete_body = {
            'noteId': note_id[0]
        }
        delete_body02 = {
            'noteId': note_id[1]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)
        delete_res02 = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body02)

        info('STEP:请求查看回收站下便签接口')
        start_index = 0
        rows = 0
        path = f'/v3/notesvr/user/{self.user_id}/invalid/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(0, len(res.json()['webNotes']), msg='返回的数据不是0条')

    def testCase04_startIndex_number_limit(self):
        """查看回收站下便签接口 数值限制：用户存在1条普通便签，starIndex=2，rows=1"""
        info('STEP:清空所有普通便签和日历便签')
        self.deleteNote.delete_notes()
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建1条普通便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:删除这1条便签')
        delete_body = {
            'noteId': note_id[0]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)

        info('STEP:请求查看回收站下便签接口')
        start_index = 2
        rows = 1
        path = f'/v3/notesvr/user/{self.user_id}/invalid/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(0, len(res.json()['webNotes']), msg='返回的数据不是0条')

    def testCase05_state_limit(self):
        """查看回收站下便签接口 状态限制：恢复回收站中1条便签"""
        info('STEP:清空所有普通便签和日历便签')
        self.deleteNote.delete_notes()
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建1条普通便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:删除这1条便签')
        delete_body = {
            'noteId': note_id[0]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)

        info('STEP:恢复这条便签')
        recover_body = {
            'userId': self.user_id,
            'noteIds': [note_id[0]]
        }
        recover_res = self.apiRe.note_patch(self.recoverNoteUrl, self.sid, recover_body)
        self.assertEqual(200, recover_res.status_code, msg='状态码异常')

        info('STEP:请求查看回收站下便签接口')
        res = self.apiRe.note_get(self.url, self.sid)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(0, len(res.json()['webNotes']), msg='返回的数据不是0条')

    def testCase06_state_limit(self):
        """查看回收站下便签接口 状态限制：清空回收站中1条便签"""
        info('STEP:清空所有普通便签和日历便签')
        self.deleteNote.delete_notes()
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建1条普通便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:删除这1条便签')
        delete_body = {
            'noteId': note_id[0]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)

        info('STEP:清空这条便签')
        empty_body = {
            'noteIds': [note_id[0]]
        }
        empty_res = self.apiRe.note_post(self.emptyRecycleUrl, self.user_id, self.sid, empty_body)
        self.assertEqual(200, empty_res.status_code, msg='状态码异常')

        info('STEP:请求查看回收站下便签接口')
        res = self.apiRe.note_get(self.url, self.sid)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(0, len(res.json()['webNotes']), msg='返回的数据不是0条')

    def testCase07_userB_get_userA_recycle_note(self):
        """操作对象：用户B获取用户A回收站中的便签"""
        info('STEP:清空所有普通便签和日历便签')
        self.deleteNote.delete_notes()
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建1条普通便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:删除这1条便签')
        delete_body = {
            'noteId': note_id[0]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)

        info('STEP:请求查看回收站下便签接口')
        res = self.apiRe.note_get(self.url, self.sidB)
        # 校验状态码
        self.assertEqual(412, res.status_code, msg='状态码异常')

    def testCase08_has_zero_recycle_note(self):
        """处理数量：用户A存在0条便签数据"""
        info('STEP:清空所有普通便签和日历便签')
        self.deleteNote.delete_notes()
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:请求查看回收站下便签接口')
        res = self.apiRe.note_get(self.url, self.sid)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(0, len(res.json()['webNotes']), msg='返回的数据不是0条')

    def testCase09_has_two_recycle_note(self):
        """处理数量：用户A存在2条便签数据"""
        info('STEP:清空所有普通便签和日历便签')
        self.deleteNote.delete_notes()
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建2条普通便签')
        note_id = self.createNote.create_notes(2)

        info('STEP:删除这两条便签')
        delete_body = {
            'noteId': note_id[0]
        }
        delete_body02 = {
            'noteId': note_id[1]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)
        delete_res02 = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body02)

        info('STEP:请求查看回收站下便签接口')
        res = self.apiRe.note_get(self.url, self.sid)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(2, len(res.json()['webNotes']), msg='返回的数据不是2条')
