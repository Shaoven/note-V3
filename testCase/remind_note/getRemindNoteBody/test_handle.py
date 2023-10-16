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
class TestGetNoteBody(unittest.TestCase):
    """获取便签内容接口level1"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['GetNoteBody']['Path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    sidB = envConfig['sidB']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    createRemindNote = CreateRemindNotes()
    deleteRemindNote = DeleteRemindNotes()
    deleteNotePath = apiConfig['DeleteNote']['Path']
    deleteNoteUrl = host + deleteNotePath
    emptyRecyclePath = apiConfig['EmptyRecycle']['Path']
    emptyRecycleUrl = host + emptyRecyclePath
    recoverNotePath = f'/v3/notesvr/user/{user_id}/notes'
    recoverNoteUrl = host + recoverNotePath

    def testCase01_get_recycle_RemindNote_body(self):
        """获取便签内容接口 接口handle：回收站中有1条日历便签，获取该便签内容"""
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:删除该便签')
        delete_body = {
            'noteId': note_id[0]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)
        self.assertEqual(200, delete_res.status_code, msg='状态码异常')

        info('STEP:获取日历便签内容')
        body = {
            'noteIds': [note_id[0]],
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(500, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(0, len(res.json()['noteBodies']), msg='删除便签后，还是能获取便签内容')

    def testCase02_get_empty_RemindNote_body(self):
        """获取便签内容接口 接口handle：回收站中有1条清空的日历便签，获取该便签内容"""
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:删除该便签')
        delete_body = {
            'noteId': note_id[0]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)
        self.assertEqual(200, delete_res.status_code, msg='状态码异常')

        info('STEP:清空便签')
        empty_body = {
            'noteIds': [note_id[0]]
        }
        empty_res = self.apiRe.note_post(self.emptyRecycleUrl, self.user_id, self.sid, empty_body)
        self.assertEqual(200, empty_res.status_code, msg='状态码异常')

        info('STEP:获取便签内容')
        body = {
            'noteIds': [note_id[0]],
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(500, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(0, len(res.json()['noteBodies']), msg='删除便签后，还是能获取便签内容')

    def testCase03_get_recover_RemindNote_body(self):
        """获取便签内容接口 接口handle：回收站中有1条恢复的普通便签，获取该便签内容"""
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:删除该标签')
        delete_body = {
            'noteId': note_id[0]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)
        self.assertEqual(200, delete_res.status_code, msg='状态码异常')

        info('STEP:恢复便签')
        recover_body = {
            'userId': self.user_id,
            'noteIds': [note_id[0]]
        }
        recover_res = self.apiRe.note_patch(self.recoverNoteUrl, self.sid, recover_body)
        self.assertEqual(200, recover_res.status_code, msg='状态码异常')

        info('STEP:获取便签内容')
        body = {
            'noteIds': [note_id[0]],
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(1, len(res.json()['noteBodies']), msg='恢复便签后，无法获取便签内容')
        note_ids = []
        for i in res.json()['noteBodies']:
            note_ids.append(i['noteId'])
        self.assertEqual(note_id, note_ids, msg='恢复便签后，获取的便签内容不正确')

    def testCase04_userB_get_userA_RemindNote_body(self):
        """获取便签内容接口 接口handle：用户B获取用户A的日历便签内容"""
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:获取便签内容')
        body = {
            'noteIds': [note_id[0] + 'test'],
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sidB, body)
        # 校验状态码
        self.assertEqual(412, res.status_code, msg='状态码异常')

    def testCase05_get_zero_RemindNote_body(self):
        """获取便签内容接口 接口handle：获取0条日历便签内容"""
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:获取便签内容')
        body = {
            'noteIds': ['test'],
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(403, res.status_code, msg='状态码异常')

    def testCase06_get_two_RemindNote_body(self):
        """获取便签内容接口 接口handle：获取2条日历便签内容"""
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建2条日历便签')
        note_id = self.createRemindNote.create_remind_notes(2)

        info('STEP:获取便签内容')
        body = {
            'noteIds': [note_id[0], note_id[1]],
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(2, len(res.json()['noteBodies']), msg='返回的数据长度不等于2')
        for i in res.json()['noteBodies']:
            self.assertIn(i['noteId'], note_id, msg='获取到的便签id不正确')
