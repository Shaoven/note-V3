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
    """删除/清空回收站便签 接口input"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    user_id = envConfig['user_id']
    sid = envConfig['sid']
    host = envConfig['host']
    path = apiConfig['EmptyRecycle']['Path']
    url = host + path
    mustKey = apiConfig['EmptyRecycle']['must_key']
    apiRe = ApiRe()
    createRemindNote = CreateRemindNotes()
    deleteRemindNote = DeleteRemindNotes()
    createNote = CreateNotes()
    deleteNote = DeleteNotes()
    deleteNotePath = apiConfig['DeleteNote']['Path']
    deleteNoteUrl = host + deleteNotePath
    startIndex = 0
    rows = 9999
    recycleNotePath = f'/v3/notesvr/user/{user_id}/invalid/startindex/{startIndex}/rows/{rows}/notes'
    recycleNoteUrl = host + recycleNotePath

    @parameterized.expand(mustKey)
    def testCase01_input_must_key(self, dic):
        """删除/清空回收站便签 必填校验"""
        info('STEP:清空所有普通便签和日历便签')
        self.deleteNote.delete_notes()
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建1条普通便签')
        note_id = self.createNote.create_notes(1)
        remind_note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:删除这条便签')
        delete_body = {
            'noteId': note_id[0]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)

        info('STEP:清空这条便签')
        body = {
            'noteIds': [note_id[0]]
        }
        body.pop(dic['key'])
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(dic['code'], res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase02_lost_x_user_key(self):
        """删除/清空回收站便签 未传入X-user-key"""
        info('STEP:清空所有普通便签和日历便签')
        self.deleteNote.delete_notes()
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建1条普通便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:删除这条便签')
        delete_body = {
            'noteId': note_id[0]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)

        info('STEP:清空这条便签')
        body = {
            'noteIds': [note_id[0]]
        }
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid}'
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body, headers)
        self.assertEqual(412, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase03_noteIds_input_kong(self):
        """删除/清空回收站便签 接口input：输入[]"""
        info('STEP:清空所有普通便签和日历便签')
        self.deleteNote.delete_notes()
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建1条普通便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:删除这条便签')
        delete_body = {
            'noteId': note_id[0]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)

        info('STEP:清空这条便签')
        body = {
            'noteIds': []
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:请求回收站便签，检查是否被清空')
        recycle_note_res = self.apiRe.note_get(self.recycleNoteUrl, self.sid)
        self.assertEqual(200, recycle_note_res.status_code, msg='状态码异常')
        self.assertEqual(1, len(recycle_note_res.json()['webNotes']), msg='回收站中的便签被清空了')

    def testCase04_noteIds_input_sub_object(self):
        """删除/清空回收站便签 接口input：输入子对象 ["234", ["123", "123"]]"""
        info('STEP:清空所有普通便签和日历便签')
        self.deleteNote.delete_notes()
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建3条普通便签')
        note_id = self.createNote.create_notes(3)

        info('STEP:删除这3条便签')
        delete_body = {
            'noteId': note_id[0]
        }
        delete_body1 = {
            'noteId': note_id[1]
        }
        delete_body2 = {
            'noteId': note_id[2]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body1)
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body2)

        info('STEP:清空这3条便签')
        body = {
            'noteIds': [note_id[0], [note_id[1], note_id[2]]]
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:请求回收站便签，检查是否被清空')
        recycle_note_res = self.apiRe.note_get(self.recycleNoteUrl, self.sid)
        self.assertEqual(200, recycle_note_res.status_code, msg='状态码异常')
        self.assertEqual(3, len(recycle_note_res.json()['webNotes']), msg='回收站中的便签被清空了')

    def testCase05_noteIds_list_obj(self):
        """删除/清空回收站便签 接口input：列表值的类型校验：int(note_id[0])"""
        info('STEP:清空所有普通便签和日历便签')
        self.deleteNote.delete_notes()
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建1条普通便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:删除这条便签')
        delete_body = {
            'noteId': note_id[0]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)

        info('STEP:清空这条便签')
        body = {
            'noteIds': [int(note_id[0])]
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:请求回收站便签，检查是否被清空')
        recycle_note_res = self.apiRe.note_get(self.recycleNoteUrl, self.sid)
        self.assertEqual(200, recycle_note_res.status_code, msg='状态码异常')
        self.assertEqual(1, len(recycle_note_res.json()['webNotes']), msg='列表值的类型是int类型时，回收站中的便签被清空了')

    def testCase06_noteIds_list_obj(self):
        """删除/清空回收站便签 接口input：列表值的类型校验：[float(note_id[0])]"""
        info('STEP:清空所有普通便签和日历便签')
        self.deleteNote.delete_notes()
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建1条普通便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:删除这条便签')
        delete_body = {
            'noteId': note_id[0]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)

        info('STEP:清空这条便签')
        body = {
            'noteIds': [float(note_id[0])]
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:请求回收站便签，检查是否被清空')
        recycle_note_res = self.apiRe.note_get(self.recycleNoteUrl, self.sid)
        self.assertEqual(200, recycle_note_res.status_code, msg='状态码异常')
        self.assertEqual(1, len(recycle_note_res.json()['webNotes']), msg='列表值的类型是float类型时，回收站中的便签被清空了')

    def testCase07_noteIds_input_none(self):
        """删除/清空回收站便签 接口input：noteIds输入None"""
        info('STEP:清空所有普通便签和日历便签')
        self.deleteNote.delete_notes()
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建1条普通便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:删除这条便签')
        delete_body = {
            'noteId': note_id[0]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)

        info('STEP:清空这条便签')
        body = {
            'noteIds': None
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:请求回收站便签，检查是否被清空')
        recycle_note_res = self.apiRe.note_get(self.recycleNoteUrl, self.sid)
        self.assertEqual(200, recycle_note_res.status_code, msg='状态码异常')
        self.assertEqual(1, len(recycle_note_res.json()['webNotes']), msg='noteIds等于None时，回收站中的便签被清空了')
