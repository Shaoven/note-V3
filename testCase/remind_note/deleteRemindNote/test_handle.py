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
class TestDeleteRemindNote(unittest.TestCase):
    """删除便签接口level1"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['DeleteNote']['Path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    sidB = envConfig['sidB']
    user_id = envConfig['user_id']
    userB_id = envConfig['userB_id']
    apiRe = ApiRe()
    createRemindNote = CreateRemindNotes()
    deleteRemindNote = DeleteRemindNotes()
    startIndex = 0
    rows = 9999
    getRemindNoteListPath = apiConfig['GetRemindNoteList']['Path']
    getRemindNoteListUrl = host + getRemindNoteListPath
    recycleNotePath = f'/v3/notesvr/user/{user_id}/invalid/startindex/{startIndex}/rows/{rows}/notes'
    recycleNoteUrl = host + recycleNotePath
    emptyRecyclePath = apiConfig['EmptyRecycle']['Path']
    emptyRecycleUrl = host + emptyRecyclePath
    recoverNotePath = f'/v3/notesvr/user/{user_id}/notes'
    recoverNoteUrl = host + recoverNotePath

    def testCase01_state_limit(self):
        """删除便签接口 接口handle：删除在回收站中的日历便签"""
        info('STEP:清空日历便签数据')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:请求删除便签接口')
        body = {
            'noteId': note_id[0]
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)

        info('STEP:再次删除该条数据')
        res02 = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(403, res02.status_code, msg='状态码异常')

    def testCase02_state_limit(self):
        """删除便签接口 接口handle：删除在回收站中清空的日历便签"""
        info('STEP:清空日历便签数据')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:请求删除便签接口')
        body = {
            'noteId': note_id[0]
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)

        info('STEP:清空该条便签')
        empty_body = {
            'noteIds': [note_id[0]]
        }
        empty_res = self.apiRe.note_post(self.emptyRecycleUrl, self.user_id, self.sid, empty_body)
        self.assertEqual(200, empty_res.status_code, msg='状态码异常')

        info('STEP:再次删除该条数据')
        res02 = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(403, res02.status_code, msg='状态码异常')

    def testCase03_state_limit(self):
        """删除便签接口 接口handle：删除在回收站中恢复的日历便签"""
        info('STEP:清空日历便签数据')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:请求删除便签接口')
        body = {
            'noteId': note_id[0]
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)

        info('STEP:恢复该条便签')
        recover_body = {
            'userId': self.user_id,
            'noteIds': [note_id[0]]
        }
        recover_res = self.apiRe.note_post(self.emptyRecycleUrl, self.user_id, self.sid, recover_body)
        self.assertEqual(200, recover_res.status_code, msg='状态码异常')

        info('STEP:再次删除该条数据')
        res02 = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res02.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:获取日历便签列表，检查数据是否还在')
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
        self.assertNotIn(note_id[0], remind_note_ids, msg='日历便签删除不成功')

    def testCase04_userB_delete_userA_RemindNote(self):
        """删除便签接口 接口handle：用户B删除用户A的日历便签"""
        info('STEP:清空日历便签数据')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:请求删除便签接口')
        body = {
            'noteId': note_id[0]
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sidB, body)
        self.assertEqual(412, res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:获取日历便签列表，检查数据是否还在')
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
        self.assertIn(note_id[0], remind_note_ids, msg='用户B真的删除成功用户A的日历便签了')

    def testCase05_delete_zero_RemindNote(self):
        """删除便签接口 接口handle：删除0条日历便签"""
        info('STEP:清空日历便签数据')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:请求删除便签接口')
        body = {
            'noteId': 'test'
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')

    def testCase06_delete_two_RemindNote(self):
        """删除便签接口 接口handle：删除2条日历便签"""
        info('STEP:清空日历便签数据')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建2条日历便签')
        note_id = self.createRemindNote.create_remind_notes(2)

        info('STEP:请求2次删除便签接口')
        body = {
            'noteId': note_id[0]
        }
        body02 = {
            'noteId': note_id[1]
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码异常')
        res02 = self.apiRe.note_post(self.url, self.user_id, self.sid, body02)
        self.assertEqual(200, res02.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:获取日历便签列表，检查数据是否还在')
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
        self.assertNotIn(note_id[0], remind_note_ids, msg='日历便签删除不成功')
        self.assertNotIn(note_id[1], remind_note_ids, msg='日历便签删除不成功')

        info('STEP:请求查看回收站下便签列表')
        recycle_body = {
            'userid': self.user_id,
            'startIndex': 0,
            'rows': 9999
        }
        recycle_res = self.apiRe.note_get(self.recycleNoteUrl, self.sid)
        recycle_note_id = []
        for n in recycle_res.json()['webNotes']:
            recycle_note_id.append(n['noteId'])
        self.assertIn(note_id[0], recycle_note_id, msg='日历便签不在回收站中')
        self.assertIn(note_id[1], recycle_note_id, msg='日历便签不在回收站中')
