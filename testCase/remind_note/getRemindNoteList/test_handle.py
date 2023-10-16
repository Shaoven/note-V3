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
class TestGetRemindNoteList(unittest.TestCase):
    """查看日历下便签接口 接口handle"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['GetRemindNoteList']['Path']
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
    createNoteInfoPath = apiConfig['CreateNoteInfo']['Path']
    createNoteInfoUrl = host + createNoteInfoPath
    createNotePath = apiConfig['CreateNote']['Path']
    createNoteUrl = host + createNotePath

    def testCase01_number_limit(self):
        """查看日历下便签接口 接口handle：用户存在2条日历便签，startIndex=0，rows=1"""
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建2条日历便签')
        self.createRemindNote.create_remind_notes(2)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 1
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(1, len(res.json()['webNotes']), msg='查询出来的数量不等于1')

    def testCase02_number_limit(self):
        """查看日历下便签接口 接口handle：用户存在2条日历便签，startIndex=0，rows=3"""
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建2条日历便签')
        self.createRemindNote.create_remind_notes(2)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 3
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(2, len(res.json()['webNotes']), msg='查询出来的数量不等于2')

    def testCase03_number_limit(self):
        """查看日历下便签接口 接口handle：用户存在2条日历便签，startIndex=0，rows=0"""
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建2条日历便签')
        self.createRemindNote.create_remind_notes(2)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 0
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(0, len(res.json()['webNotes']), msg='查询出来的数量不等于0')

    def testCase04_number_limit(self):
        """查看日历下便签接口 接口handle：用户存在1条日历便签，starIndex=2，rows=1"""
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建1条日历便签')
        self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 2,
            'rows': 1
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(0, len(res.json()['webNotes']), msg='查询出来的数量不等于0')

    def testCase05_userB_get_userA_RemindNote(self):
        """查看日历下便签接口 接口handle：用户B查看用户A的日历便签"""
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建1条日历便签')
        self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 2,
            'rows': 1
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sidB, body)
        # 校验状态码
        self.assertEqual(412, res.status_code, msg='状态码异常')

    def testCase06_get_zero_RemindNote(self):
        """查看日历下便签接口 接口handle：获取0条日历便签"""
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 2,
            'rows': 1
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        self.assertEqual(0, len(res.json()['webNotes']), msg='查询的日历便签数量不等于0')

    def testCase07_get_two_RemindNote(self):
        """查看日历下便签接口 接口handle：获取2条日历便签"""
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建2条日历便签')
        remind_note_id = self.createRemindNote.create_remind_notes(2)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        self.assertEqual(2, len(res.json()['webNotes']), msg='查询的日历便签数量不等于2')
        # 校验数据源
        note_ids = []
        for i in res.json()['webNotes']:
            note_ids.append(i['noteId'])
        self.assertIn(remind_note_id[0], note_ids, msg='日历便签不在里面')
        self.assertIn(remind_note_id[1], note_ids, msg='日历便签不在里面')

    def testCase08_state_limit(self):
        """查看日历下便签接口 接口handle：回收站有1条日历便签"""
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建1条日历便签')
        remind_note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:删除这条日历便签')
        delete_body = {
            'noteId': remind_note_id[0]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)
        self.assertEqual(200, delete_res.status_code, msg='状态码异常')

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        self.assertEqual(0, len(res.json()['webNotes']), msg='查询的日历便签数量不等于0')

    def testCase09_state_limit(self):
        """查看日历下便签接口 接口handle：回收站中有1条被清空的日历便签"""
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建1条日历便签')
        remind_note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:删除这条日历便签')
        delete_body = {
            'noteId': remind_note_id[0]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)
        self.assertEqual(200, delete_res.status_code, msg='状态码异常')

        info('STEP:清空回收站')
        empty_body = {
            'noteIds': [remind_note_id[0]]
        }
        empty_res = self.apiRe.note_post(self.emptyRecycleUrl, self.user_id, self.sid, empty_body)
        self.assertEqual(200, empty_res.status_code, msg='状态码异常')

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        self.assertEqual(0, len(res.json()['webNotes']), msg='查询的日历便签数量不等于0')

    def testCase10_state_limit(self):
        """查看日历下便签接口 接口handle：回收站中有1条被恢复的日历便签"""
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建1条日历便签')
        remind_note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:删除这条日历便签')
        delete_body = {
            'noteId': remind_note_id[0]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)
        self.assertEqual(200, delete_res.status_code, msg='状态码异常')

        info('STEP:恢复这个日历便签')
        recover_body = {
            'userId': self.user_id,
            'noteIds': [remind_note_id[0]]
        }
        recover_res = self.apiRe.note_patch(self.recoverNoteUrl, self.sid, recover_body)
        self.assertEqual(200, recover_res.status_code, msg='状态码异常')

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        self.assertEqual(1, len(res.json()['webNotes']), msg='查询的日历便签数量不等于1')
        note_ids = []
        for i in res.json()['webNotes']:
            note_ids.append(i['noteId'])
        self.assertEqual(remind_note_id[0], note_ids[0], msg='日历便签没有恢复')

    def testCase11_time_limit(self):
        """查看日历下便签接口 接口handle：时间精确到秒，检查数据正确性"""
        info('STEP:清空日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条时间为：2023-08-31 23:59:59的日历便签')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        remind_note_info_body = {
            'noteId': note_id,
            'remindTime': 1693497599,
            'remindType': 0
        }
        remind_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid,
                                                    remind_note_info_body)
        self.assertEqual(200, remind_note_info_res.status_code, msg='状态码异常')
        create_remind_note_body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': remind_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        create_remind_note_res = self.apiRe.note_post(self.createNoteUrl, self.user_id, self.sid, create_remind_note_body)
        self.assertEqual(200, create_remind_note_res.status_code, msg='状态码异常')

        info('STEP:新建一条时间为：2023-09-01 00:00:00的日历便签')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        remind_note_info_body = {
            'noteId': note_id,
            'remindTime': 1693497600,
            'remindType': 0
        }
        remind_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid,
                                                    remind_note_info_body)
        self.assertEqual(200, remind_note_info_res.status_code, msg='状态码异常')
        create_remind_note_body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': remind_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        create_remind_note_res = self.apiRe.note_post(self.createNoteUrl, self.user_id, self.sid, create_remind_note_body)
        self.assertEqual(200, create_remind_note_res.status_code, msg='状态码异常')

        info('STEP:新建一条时间为：2023-09-01 00:00:01的日历便签')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        remind_note_info_body = {
            'noteId': note_id,
            'remindTime': 1693497601,
            'remindType': 0
        }
        remind_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid,
                                                    remind_note_info_body)
        self.assertEqual(200, remind_note_info_res.status_code, msg='状态码异常')
        create_remind_note_body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': remind_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        create_remind_note_res = self.apiRe.note_post(self.createNoteUrl, self.user_id, self.sid, create_remind_note_body)
        self.assertEqual(200, create_remind_note_res.status_code, msg='状态码异常')

        info('STEP:新建一条时间为：2023-09-30 23:59:59的日历便签')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        remind_note_info_body = {
            'noteId': note_id,
            'remindTime': 1696089599,
            'remindType': 0
        }
        remind_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid,
                                                    remind_note_info_body)
        self.assertEqual(200, remind_note_info_res.status_code, msg='状态码异常')
        create_remind_note_body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': remind_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        create_remind_note_res = self.apiRe.note_post(self.createNoteUrl, self.user_id, self.sid, create_remind_note_body)
        self.assertEqual(200, create_remind_note_res.status_code, msg='状态码异常')

        info('STEP:新建一条时间为：2023-10-01 00:00:00的日历便签')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        remind_note_info_body = {
            'noteId': note_id,
            'remindTime': 1696089600,
            'remindType': 0
        }
        remind_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid,
                                                    remind_note_info_body)
        self.assertEqual(200, remind_note_info_res.status_code, msg='状态码异常')
        create_remind_note_body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': remind_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        create_remind_note_res = self.apiRe.note_post(self.createNoteUrl, self.user_id, self.sid, create_remind_note_body)
        self.assertEqual(200, create_remind_note_res.status_code, msg='状态码异常')

        # 查询九月份下的便签数，共三条
        info('STEP:请求查看九月份的日历便签数')
        body = {
            'remindStartTime': 1693497600,
            'remindEndTime': 1696089599,
            'startIndex': 0,
            'rows': 999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(3, len(res.json()['webNotes']), msg='返回的数量不等于3')
