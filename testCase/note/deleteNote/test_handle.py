import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn
from businessCommon.create_notes import CreateNotes
from businessCommon.delete_notes import DeleteNotes


@class_case_log
class TestDeleteNote(unittest.TestCase):
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
    createNote = CreateNotes()
    deleteNote = DeleteNotes()
    startIndex = 0
    rows = 9999
    getHomeNotePath = f'/v3/notesvr/user/{user_id}/home/startindex/{startIndex}/rows/{rows}/notes'
    getHomeNoteUrl = host + getHomeNotePath
    recycleNotePath = f'/v3/notesvr/user/{user_id}/invalid/startindex/{startIndex}/rows/{rows}/notes'
    recycleNoteUrl = host + recycleNotePath
    emptyRecyclePath = apiConfig['EmptyRecycle']['Path']
    emptyRecycleUrl = host + emptyRecyclePath
    recoverNotePath = f'/v3/notesvr/user/{user_id}/notes'
    recoverNoteUrl = host + recoverNotePath

    def testCase01_state_limit(self):
        """删除便签接口 接口handle：删除在回收站中的普通便签"""
        info('STEP:清空数据')
        self.deleteNote.delete_notes()

        info('STEP:新建一条便签')
        note_id = self.createNote.create_notes(1)

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
        """删除便签接口 接口handle：删除在回收站中清空的普通便签"""
        info('STEP:清空数据')
        self.deleteNote.delete_notes()

        info('STEP:新建一条便签')
        note_id = self.createNote.create_notes(1)

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
        """删除便签接口 接口handle：删除在回收站中恢复的普通便签"""
        info('STEP:清空数据')
        self.deleteNote.delete_notes()

        info('STEP:新建一条便签')
        note_id = self.createNote.create_notes(1)

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

    def testCase04_userB_delete_userA_note(self):
        """删除便签接口 接口handle：用户B删除用户A的普通便签"""
        info('STEP:清空数据')
        self.deleteNote.delete_notes()

        info('STEP:新建一条便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:请求删除便签接口')
        body = {
            'noteId': note_id[0]
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sidB, body)
        self.assertEqual(412, res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:请求获取首页便签接口')
        home_res = self.apiRe.note_get(self.getHomeNoteUrl, self.sid)
        self.assertEqual(200, home_res.status_code, msg='状态码异常')
        note_ids = []
        for i in home_res.json()['webNotes']:
            note_ids.append(i['noteId'])
        self.assertEqual(note_id, note_ids, msg='用户B删除用户A的数据删除成功了')

    def testCase05_delete_zero_note(self):
        """删除便签接口 接口handle：删除0条普通便签"""
        info('STEP:清空数据')
        self.deleteNote.delete_notes()

        info('STEP:请求删除便签接口')
        body = {
            'noteId': 'test'
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')

    def testCase06_delete_two_note(self):
        """删除便签接口 接口handle：删除2条普通便签"""
        info('STEP:清空数据')
        self.deleteNote.delete_notes()

        info('STEP:新建2条便签')
        note_id = self.createNote.create_notes(2)

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
        info('STEP:请求获取首页便签接口')
        home_res = self.apiRe.note_get(self.getHomeNoteUrl, self.sid)
        self.assertEqual(200, home_res.status_code, msg='状态码异常')
        note_ids = []
        for i in home_res.json()['webNotes']:
            note_ids.append(i['noteId'])
        self.assertNotIn(note_id[0], note_ids, msg='删除不成功')
        self.assertNotIn(note_id[1], note_ids, msg='删除不成功')

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
        self.assertIn(note_id[0], recycle_note_id, msg='便签不在回收站中')
        self.assertIn(note_id[1], recycle_note_id, msg='便签不在回收站中')
