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
    """恢复回收站便签 接口handle"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    user_id = envConfig['user_id']
    sid = envConfig['sid']
    sidB = envConfig['sidB']
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
    recycleNotePath = f'/v3/notesvr/user/{user_id}/invalid/startindex/{startIndex}/rows/{rows}/notes'
    recycleNoteUrl = host + recycleNotePath
    emptyRecyclePath = apiConfig['EmptyRecycle']['Path']
    emptyRecycleUrl = host + emptyRecyclePath

    def testCase01_userB_recover_userA_recycle_note(self):
        """恢复回收站便签 操作对象：用户B恢复用户A回收站中的便签"""
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
        body = {
            'userId': self.user_id,
            'noteIds': [note_id[0]]
        }
        res = self.apiRe.note_patch(self.url, self.sidB, body)
        self.assertEqual(412, res.status_code, msg='状态码异常')

    def testCase02_has_two_recycle_note_recover_one(self):
        """恢复回收站便签 处理数量：回收站中有2条便签，只恢复1条"""
        info('STEP:清空所有普通便签和日历便签')
        self.deleteNote.delete_notes()
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建2条普通便签')
        note_id = self.createNote.create_notes(2)

        info('STEP:删除这2条便签')
        delete_body = {
            'noteId': note_id[0]
        }
        delete_body02 = {
            'noteId': note_id[1]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body02)

        info('STEP:恢复1条便签')
        body = {
            'userId': self.user_id,
            'noteIds': [note_id[0]]
        }
        res = self.apiRe.note_patch(self.url, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:请求回收站中便签接口，检查数据源')
        recycle_res = self.apiRe.note_get(self.recycleNoteUrl, self.sid)
        self.assertEqual(200, recycle_res.status_code, msg='状态码异常')
        self.assertEqual(1, len(recycle_res.json()['webNotes']), msg='回收站中剩下的便签数量不等于1')
        recycle_note_id = []
        for i in recycle_res.json()['webNotes']:
            recycle_note_id.append(i['noteId'])
        self.assertIn(note_id[1], recycle_note_id, msg='回收站中剩下未恢复的便签id不正确')

    def testCase03_has_two_recycle_note_recover_two(self):
        """恢复回收站便签 处理数量：回收站中有2条便签，恢复2条"""
        info('STEP:清空所有普通便签和日历便签')
        self.deleteNote.delete_notes()
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建2条普通便签')
        note_id = self.createNote.create_notes(2)

        info('STEP:删除这2条便签')
        delete_body = {
            'noteId': note_id[0]
        }
        delete_body02 = {
            'noteId': note_id[1]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body02)

        info('STEP:恢复2条便签')
        body = {
            'userId': self.user_id,
            'noteIds': [note_id[0], note_id[1]]
        }
        res = self.apiRe.note_patch(self.url, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:请求获取首页便签接口，检查数据源')
        home_note_res = self.apiRe.note_get(self.getHomeNoteUrl, self.sid)
        self.assertEqual(200, home_note_res.status_code, msg='状态码异常')
        self.assertEqual(2, len(home_note_res.json()['webNotes']), msg='首页中的便签数量不等于2，恢复两条便签有问题')
        note_ids = []
        for i in home_note_res.json()['webNotes']:
            note_ids.append(i['noteId'])
        self.assertIn(note_id[0], note_ids, msg='首页中的便签id没有恢复的便签id')
        self.assertIn(note_id[1], note_ids, msg='首页中的便签id没有恢复的便签id')

    def testCase04_state_limit(self):
        """恢复回收站便签 状态限制：回收站中已恢复便签A，再次恢复该便签"""
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
        body = {
            'userId': self.user_id,
            'noteIds': [note_id[0]]
        }
        res = self.apiRe.note_patch(self.url, self.sid, body)
        info('STEP:再次恢复这条便签')
        res02 = self.apiRe.note_patch(self.url, self.sid, body)
        self.assertEqual(500, res02.status_code, msg='状态码异常')

    def testCase05_state_limit(self):
        """恢复回收站便签 状态限制：回收站中清空便签A后，恢复便签A"""
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

        info('STEP:恢复这条便签')
        body = {
            'userId': self.user_id,
            'noteIds': [note_id[0]]
        }
        res = self.apiRe.note_patch(self.url, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:请求获取首页便签，检查是否真的恢复了')
        home_note_res = self.apiRe.note_get(self.getHomeNoteUrl, self.sid)
        self.assertEqual(0, len(home_note_res.json()['webNotes']), msg='首页的便签数量不等于0,清空的便签还是被恢复了')

    def testCase06_number_limit(self):
        """恢复回收站便签 处理数量：恢复0条回收站中的便签数据"""
        info('STEP:清空所有普通便签和日历便签')
        self.deleteNote.delete_notes()
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:请求恢复回收站便签接口')
        body = {
            'userId': self.user_id,
            'noteIds': '123'
        }
        res = self.apiRe.note_patch(self.url, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')
