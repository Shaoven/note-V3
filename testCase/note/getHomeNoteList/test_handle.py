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
from businessCommon.create_remind_notes import CreateRemindNotes
from businessCommon.delete_remind_notes import DeleteRemindNotes


@class_case_log
class TestGetHomeNoteList(unittest.TestCase):
    """获取首页便签列表接口 接口handle"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    host = envConfig['host']
    sid = envConfig['sid']
    sidB = envConfig['sidB']
    user_id = envConfig['user_id']
    userB_id = envConfig['userB_id']
    apiRe = ApiRe()
    createNote = CreateNotes()
    createRemindNote = CreateRemindNotes()
    deleteNote = DeleteNotes()
    deleteRemindNote = DeleteRemindNotes()
    deleteNotePath = apiConfig['DeleteNote']['Path']
    deleteNoteUrl = host + deleteNotePath
    emptyRecycleNotePath = apiConfig['EmptyRecycle']['Path']
    emptyRecycleNoteUrl = host + emptyRecycleNotePath
    recoverRecycleNotePath = f'/v3/notesvr/user/{user_id}/notes'
    recoverRecycleNoteUrl = host + recoverRecycleNotePath

    def testCase01_rows_number_limit(self):
        """数值限制：用户存在2条普通便签，startIndex=0，rows=1"""
        info('STEP:清空首页便签数据')
        self.deleteNote.delete_notes()
        info('STEP:新建两条便签数据')
        note_ids = self.createNote.create_notes(2)

        info('STEP:获取首页便签列表')
        start_index = 0
        rows = 1
        path = f'/v3/notesvr/user/{self.user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(1, len(res.json()['webNotes']), msg='返回的数据不是1条')

    def testCase02_rows_number_limit(self):
        """数值限制：用户存在2条普通便签，startIndex=0，rows=3"""
        info('STEP:清空首页便签数据')
        self.deleteNote.delete_notes()
        info('STEP:新建两条便签数据')
        note_ids = self.createNote.create_notes(2)

        info('STEP:获取首页便签列表')
        start_index = 0
        rows = 3
        path = f'/v3/notesvr/user/{self.user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(2, len(res.json()['webNotes']), msg='返回的数据不是2条')

    def testCase03_rows_number_limit(self):
        """数值限制：用户存在2条普通便签，startIndex=0，rows=0"""
        info('STEP:清空首页便签数据')
        self.deleteNote.delete_notes()
        info('STEP:新建两条便签数据')
        note_ids = self.createNote.create_notes(2)

        info('STEP:获取首页便签列表')
        start_index = 0
        rows = 0
        path = f'/v3/notesvr/user/{self.user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(0, len(res.json()['webNotes']), msg='返回的数据不是0条')

    def testCase04_startIndex_number_limit(self):
        """数值限制：用户存在1条普通便签，starIndex=2，rows=1"""
        info('STEP:清空首页便签数据')
        self.deleteNote.delete_notes()
        info('STEP:新建1条便签数据')
        note_ids = self.createNote.create_notes(1)

        info('STEP:获取首页便签列表')
        start_index = 2
        rows = 1
        path = f'/v3/notesvr/user/{self.user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(0, len(res.json()['webNotes']), msg='返回的数据不是0条')

    def testCase05_state_limit(self):
        """状态限制：用户有1条普通便签，1条回收站的普通便签"""
        info('STEP:清空首页便签数据')
        self.deleteNote.delete_notes()
        info('STEP:新建两条便签数据')
        note_ids = self.createNote.create_notes(2)

        info('STEP:删除一条普通便签到回收站')
        delete_note_body = {
            'noteId': note_ids[0]
        }
        delete_note_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_note_body)
        self.assertEqual(200, delete_note_res.status_code, msg='状态码异常')

        info('STEP:获取首页便签列表')
        start_index = 0
        rows = 2
        path = f'/v3/notesvr/user/{self.user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(1, len(res.json()['webNotes']), msg='返回的数据不是1条')

    def testCase06_state_limit(self):
        """状态限制：用户有1条普通便签，1条日历便签"""
        info('STEP:清空首页便签数据')
        self.deleteNote.delete_notes()
        info('STEP:清空日历便签数据')
        self.deleteRemindNote.delete_remind_notes()
        info('STEP:新建1条普通便签数据')
        note_ids = self.createNote.create_notes(1)
        info('STEP:新建1条日历便签数据')
        remind_note_ids = self.createRemindNote.create_remind_notes(1)

        info('STEP:获取首页便签列表')
        start_index = 0
        rows = 2
        path = f'/v3/notesvr/user/{self.user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(1, len(res.json()['webNotes']), msg='返回的数据不是1条')
        note_id = []
        for i in res.json()['webNotes']:
            note_id.append(i['noteId'])
        self.assertEqual(note_ids, note_id, msg='不是普通便签的noteId')

    def testCase07_state_limit(self):
        """状态限制：用户有1条普通便签，1条在回收站中被清空的普通便签"""
        info('STEP:清空首页便签数据')
        self.deleteNote.delete_notes()
        info('STEP:新建两条便签数据')
        note_ids = self.createNote.create_notes(2)

        info('STEP:删除一条便签数据')
        delete_note_body = {
            'noteId': note_ids[0]
        }
        delete_note_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_note_body)
        self.assertEqual(200, delete_note_res.status_code, msg='状态码异常')
        info('STEP:清空回收站中该数据')
        empty_recycle_note_body = {
            'noteIds': [note_ids[0]]
        }
        empty_res = self.apiRe.note_post(self.emptyRecycleNoteUrl, self.user_id, self.sid, empty_recycle_note_body)
        self.assertEqual(200, empty_res.status_code, msg='状态码异常')

        info('STEP:获取首页便签列表')
        start_index = 0
        rows = 2
        path = f'/v3/notesvr/user/{self.user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(1, len(res.json()['webNotes']), msg='返回的数据不是1条')

    def testCase08_startIndex_number_limit(self):
        """状态限制：用户有1条普通便签，1条回收站中恢复的普通便签"""
        info('STEP:清空首页便签数据')
        self.deleteNote.delete_notes()
        info('STEP:新建两条便签数据')
        note_ids = self.createNote.create_notes(2)

        info('STEP:删除一条便签数据')
        delete_note_body = {
            'noteId': note_ids[0]
        }
        delete_note_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_note_body)
        self.assertEqual(200, delete_note_res.status_code, msg='状态码异常')

        info('STEP:恢复那条便签数据')
        recover_body = {
            'userId': self.user_id,
            'noteIds': [note_ids[0]]
        }
        recover_res = self.apiRe.note_patch(self.recoverRecycleNoteUrl, self.sid, recover_body)
        self.assertEqual(200, recover_res.status_code, msg='状态码异常')

        info('STEP:获取首页便签列表')
        start_index = 0
        rows = 2
        path = f'/v3/notesvr/user/{self.user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(2, len(res.json()['webNotes']), msg='返回的数据不是2条')
        note_id = []
        for i in res.json()['webNotes']:
            note_id.append(i['noteId'])
        for n in range(len(note_id)):
            self.assertIn(note_id[n], note_ids, msg='id不一致')

    def testCase09_userB_get_userA_note(self):
        """操作对象：用户B获取用户A的普通便签"""
        info('STEP:清空首页便签数据')
        self.deleteNote.delete_notes()
        info('STEP:新建1条便签数据')
        note_ids = self.createNote.create_notes(1)

        info('STEP:获取首页便签列表')
        start_index = 0
        rows = 9999
        path = f'/v3/notesvr/user/{self.userB_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sidB)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        user_b_note_id = []
        for i in res.json()['webNotes']:
            user_b_note_id.append(i['noteId'])
        # 校验数据源
        self.assertNotIn(note_ids, user_b_note_id, msg='用户B查询到用户A的便签id')

    def testCase10_has_zero_note(self):
        """处理数量：用户A存在0条便签数据"""
        info('STEP:清空首页便签数据')
        self.deleteNote.delete_notes()

        info('STEP:获取首页便签列表')
        start_index = 0
        rows = 999
        path = f'/v3/notesvr/user/{self.user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(0, len(res.json()['webNotes']), msg='返回的数据不是0条')

    def testCase11_has_two_note(self):
        """处理数量：用户A存在2条便签数据"""
        info('STEP:清空首页便签数据')
        self.deleteNote.delete_notes()
        info('STEP:新建两条便签数据')
        note_ids = self.createNote.create_notes(2)

        info('STEP:获取首页便签列表')
        start_index = 0
        rows = 999
        path = f'/v3/notesvr/user/{self.user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(2, len(res.json()['webNotes']), msg='返回的数据不是2条')
