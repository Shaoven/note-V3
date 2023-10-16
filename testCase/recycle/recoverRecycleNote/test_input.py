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
    """恢复回收站便签 接口input"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    user_id = envConfig['user_id']
    sid = envConfig['sid']
    host = envConfig['host']
    path = f"/v3/notesvr/user/{user_id}/notes"
    url = host + path
    apiRe = ApiRe()
    must_key = apiConfig['RecoverRecycleNote']['must_key']
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

    def testCase01_sid_not_exist(self):
        """恢复回收站便签 sid不存在"""
        info('STEP:清空所有普通便签和日历便签')
        self.deleteNote.delete_notes()
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建1条普通便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:恢复这条便签')
        body = {
            'userId': self.user_id,
            'noteIds': [note_id[0]]
        }
        sid = '123asd'
        res = self.apiRe.note_patch(self.url, sid, body)
        self.assertEqual(401, res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:获取首页便签列表')
        home_note_res = self.apiRe.note_get(self.getHomeNoteUrl, self.sid)
        home_note_ids = []
        for i in home_note_res.json()['webNotes']:
            home_note_ids.append(i['noteId'])
        self.assertNotIn(note_id[0], home_note_ids[0], msg='sid不正确的情况下，普通便签还恢复成功了')

    def testCase02_userId_input_special_number(self):
        """ 恢复回收站便签 userId输入特殊值：0 """
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

        info('STEP:恢复这条便签')
        body = {
            'userId': 0,
            'noteIds': [note_id[0]]
        }
        res = self.apiRe.note_patch(self.url, self.sid, body)
        self.assertEqual(412, res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:获取首页便签列表')
        home_note_res = self.apiRe.note_get(self.getHomeNoteUrl, self.sid)
        home_note_ids = []
        for i in home_note_res.json()['webNotes']:
            home_note_ids.append(i['noteId'])
        self.assertNotIn(note_id[0], home_note_ids, msg='userId不正确的情况下，普通便签还恢复成功了')

    def testCase03_userId_input_special_number(self):
        """ 恢复回收站便签 userId输入特殊值：-1 """
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

        info('STEP:恢复这条便签')
        body = {
            'userId': -1,
            'noteIds': [note_id[0]]
        }
        res = self.apiRe.note_patch(self.url, self.sid, body)
        self.assertEqual(412, res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:获取首页便签列表')
        home_note_res = self.apiRe.note_get(self.getHomeNoteUrl, self.sid)
        home_note_ids = []
        for i in home_note_res.json()['webNotes']:
            home_note_ids.append(i['noteId'])
        self.assertNotIn(note_id[0], home_note_ids, msg='userId不正确的情况下，普通便签还恢复成功了')

    def testCase04_userId_input_min_number(self):
        """ 恢复回收站便签 userId输入最小值：-2147483649 """
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

        info('STEP:恢复这条便签')
        body = {
            'userId': -2147483649,
            'noteIds': [note_id[0]]
        }
        res = self.apiRe.note_patch(self.url, self.sid, body)
        self.assertEqual(412, res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:获取首页便签列表')
        home_note_res = self.apiRe.note_get(self.getHomeNoteUrl, self.sid)
        home_note_ids = []
        for i in home_note_res.json()['webNotes']:
            home_note_ids.append(i['noteId'])
        self.assertNotIn(note_id[0], home_note_ids, msg='userId不正确的情况下，普通便签还恢复成功了')

    def testCase05_userId_input_max_number(self):
        """ 恢复回收站便签 userId输入最大值：2147483648 """
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

        info('STEP:恢复这条便签')
        body = {
            'userId': 2147483648,
            'noteIds': [note_id[0]]
        }
        res = self.apiRe.note_patch(self.url, self.sid, body)
        self.assertEqual(412, res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:获取首页便签列表')
        home_note_res = self.apiRe.note_get(self.getHomeNoteUrl, self.sid)
        home_note_ids = []
        for i in home_note_res.json()['webNotes']:
            home_note_ids.append(i['noteId'])
        self.assertNotIn(note_id[0], home_note_ids, msg='userId不正确的情况下，普通便签还恢复成功了')

    def testCase06_userId_input_float_number(self):
        """ 恢复回收站便签 userId输入小数：1.5 """
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

        info('STEP:恢复这条便签')
        body = {
            'userId': 1.5,
            'noteIds': [note_id[0]]
        }
        res = self.apiRe.note_patch(self.url, self.sid, body)
        self.assertEqual(412, res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:获取首页便签列表')
        home_note_res = self.apiRe.note_get(self.getHomeNoteUrl, self.sid)
        home_note_ids = []
        for i in home_note_res.json()['webNotes']:
            home_note_ids.append(i['noteId'])
        self.assertNotIn(note_id[0], home_note_ids, msg='userId不正确的情况下，普通便签还恢复成功了')

    def testCase07_userId_input_string_number(self):
        """ 恢复回收站便签 userId输入字符串形式的数值：“1” """
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

        info('STEP:恢复这条便签')
        body = {
            'userId': '1',
            'noteIds': [note_id[0]]
        }
        res = self.apiRe.note_patch(self.url, self.sid, body)
        self.assertEqual(412, res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:获取首页便签列表')
        home_note_res = self.apiRe.note_get(self.getHomeNoteUrl, self.sid)
        home_note_ids = []
        for i in home_note_res.json()['webNotes']:
            home_note_ids.append(i['noteId'])
        self.assertNotIn(note_id[0], home_note_ids, msg='userId不正确的情况下，普通便签还恢复成功了')

    def testCase08_userId_input_none(self):
        """ 恢复回收站便签 userId输入空值：None """
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

        info('STEP:恢复这条便签')
        body = {
            'userId': None,
            'noteIds': [note_id[0]]
        }
        res = self.apiRe.note_patch(self.url, self.sid, body)
        self.assertEqual(412, res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:获取首页便签列表')
        home_note_res = self.apiRe.note_get(self.getHomeNoteUrl, self.sid)
        home_note_ids = []
        for i in home_note_res.json()['webNotes']:
            home_note_ids.append(i['noteId'])
        self.assertNotIn(note_id[0], home_note_ids, msg='userId不正确的情况下，普通便签还恢复成功了')

    def testCase09_noteIds_input_kong(self):
        """恢复回收站便签 接口input：输入[]"""
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

        info('STEP:恢复这条便签')
        body = {
            'userId': self.user_id,
            'noteIds': []
        }
        res = self.apiRe.note_patch(self.url, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:获取首页便签列表')
        home_note_res = self.apiRe.note_get(self.getHomeNoteUrl, self.sid)
        home_note_ids = []
        for i in home_note_res.json()['webNotes']:
            home_note_ids.append(i['noteId'])
        self.assertNotIn(note_id[0], home_note_ids, msg='noteIds不正确的情况下，普通便签还恢复成功了')

    def testCase10_noteIds_input_sub_object(self):
        """恢复回收站便签 接口input：输入子对象 ["234", ["123", "123"]]"""
        info('STEP:清空所有普通便签和日历便签')
        self.deleteNote.delete_notes()
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建3条普通便签')
        note_id = self.createNote.create_notes(3)

        info('STEP:删除这3条便签')
        delete_body = {
            'noteId': note_id[0]
        }
        delete_body02 = {
            'noteId': note_id[1]
        }
        delete_body03 = {
            'noteId': note_id[2]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body02)
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body03)

        info('STEP:恢复这3条便签')
        body = {
            'userId': self.user_id,
            'noteIds': [note_id[0], [note_id[1], note_id[2]]]
        }
        res = self.apiRe.note_patch(self.url, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:获取首页便签列表')
        home_note_res = self.apiRe.note_get(self.getHomeNoteUrl, self.sid)
        home_note_ids = []
        for i in home_note_res.json()['webNotes']:
            home_note_ids.append(i['noteId'])
        self.assertNotIn(note_id[0], home_note_ids, msg='noteIds不正确的情况下，普通便签还恢复成功了')
        self.assertNotIn(note_id[1], home_note_ids, msg='noteIds不正确的情况下，普通便签还恢复成功了')
        self.assertNotIn(note_id[2], home_note_ids, msg='noteIds不正确的情况下，普通便签还恢复成功了')

    def testCase11_noteIds_list_obj(self):
        """恢复回收站便签 接口input：列表值的类型校验：int"""
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

        info('STEP:恢复这条便签')
        body = {
            'userId': self.user_id,
            'noteIds': [int(note_id[0])]
        }
        res = self.apiRe.note_patch(self.url, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:获取首页便签列表')
        home_note_res = self.apiRe.note_get(self.getHomeNoteUrl, self.sid)
        home_note_ids = []
        for i in home_note_res.json()['webNotes']:
            home_note_ids.append(i['noteId'])
        self.assertNotIn(note_id[0], home_note_ids, msg='noteIds不正确的情况下，普通便签还恢复成功了')

    def testCase12_noteIds_list_obj(self):
        """恢复回收站便签 接口input：列表值的类型校验：[float(note_id[0])]"""
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

        info('STEP:恢复这条便签')
        body = {
            'userId': self.user_id,
            'noteIds': [float(note_id[0])]
        }
        res = self.apiRe.note_patch(self.url, self.sid, body)
        self.assertEqual(412, res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:获取首页便签列表')
        home_note_res = self.apiRe.note_get(self.getHomeNoteUrl, self.sid)
        home_note_ids = []
        for i in home_note_res.json()['webNotes']:
            home_note_ids.append(i['noteId'])
        self.assertNotIn(note_id[0], home_note_ids, msg='noteIds不正确的情况下，普通便签还恢复成功了')

    def testCase13_noteIds_input_none(self):
        """恢复回收站便签 接口input：noteIds输入None"""
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

        info('STEP:恢复这条便签')
        body = {
            'userId': self.user_id,
            'noteIds': None
        }
        res = self.apiRe.note_patch(self.url, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:获取首页便签列表')
        home_note_res = self.apiRe.note_get(self.getHomeNoteUrl, self.sid)
        home_note_ids = []
        for i in home_note_res.json()['webNotes']:
            home_note_ids.append(i['noteId'])
        self.assertNotIn(note_id[0], home_note_ids, msg='noteIds不正确的情况下，普通便签还恢复成功了')

    @parameterized.expand(must_key)
    def testCase14_must_key(self, dic):
        """恢复回收站便签 接口input：key不存在, body.pop(dic['key'])"""
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

        info('STEP:恢复这条便签')
        body = {
            'userId': self.user_id,
            'noteIds': None
        }
        body.pop(dic['key'])
        res = self.apiRe.note_patch(self.url, self.sid, body)
        self.assertEqual(dic['code'], res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:获取首页便签列表')
        home_note_res = self.apiRe.note_get(self.getHomeNoteUrl, self.sid)
        home_note_ids = []
        for i in home_note_res.json()['webNotes']:
            home_note_ids.append(i['noteId'])
        self.assertNotIn(note_id[0], home_note_ids, msg='key不存在的情况下，普通便签还恢复成功了')
