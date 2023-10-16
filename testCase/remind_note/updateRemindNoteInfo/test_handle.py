import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn
from businessCommon.create_group import CreateGroups
from businessCommon.create_remind_notes import CreateRemindNotes


@class_case_log
class TestUpdateRemindNoteInfo(unittest.TestCase):
    """更新日历便签主体接口 接口handle"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['CreateNoteInfo']['Path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    sidB = envConfig['sidB']
    user_id = envConfig['user_id']
    userB_id = envConfig['userB_id']
    apiRe = ApiRe()
    createGroup = CreateGroups()
    deleteNotePath = apiConfig['DeleteNote']['Path']
    deleteNoteUrl = host + deleteNotePath
    emptyRecycleNotePath = apiConfig['EmptyRecycle']['Path']
    emptyRecycleNoteUrl = host + emptyRecycleNotePath
    recoverRecycleNotePath = f'/v3/notesvr/user/{user_id}/notes'
    recoverRecycleNoteUrl = host + recoverRecycleNotePath
    createRemindNote = CreateRemindNotes()
    getRemindNoteListPath = apiConfig['GetRemindNoteList']['Path']
    getRemindNoteListUrl = host + getRemindNoteListPath

    def testCase01_check_update_infoVersion(self):
        """更新日历便签主体接口 infoVersion的值每次更新时自动递增"""
        info('STEP:新建日历便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        remind_time = int(time.time() * 1000)
        body = {
            'noteId': note_id,
            'remindTime': remind_time,
            'remindType': 0
        }
        # 请求上传便签信息主体接口，并获取接口返回结果
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        update_res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, update_res.status_code, msg='状态码有问题')
        # 校验数据源
        self.assertEqual(res.json()['infoVersion']+1, update_res.json()['infoVersion'], msg='infoVersion更新后没有+1')

    def testCase02_state_limit(self):
        """更新日历便签主体接口 状态限制：用户有1条日历便签在回收站，更新回收站中的日历便签主体"""
        info('STEP:新建一条日历便签')
        remind_note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:删除这条日历便签')
        delete_body = {
            'noteId': remind_note_id[0]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)
        self.assertEqual(200, delete_res.status_code, msg='状态码有问题')

        info('STEP:更新已删除的日历便签主体')
        remind_time = int(time.time() * 1000)
        update_body = {
            'noteId': remind_note_id[0],
            'remindTime': remind_time,
            'remindType': 0
        }
        update_res = self.apiRe.note_post(self.url, self.user_id, self.sid, update_body)
        # 校验状态码
        self.assertEqual(403, update_res.status_code, msg='状态码有问题')

    def testCase03_state_limit(self):
        """更新便签主体接口 状态限制：用户有1条日历便签在回收站中被清空，更新被清空的便签主体"""
        info('STEP:新建一条日历便签')
        remind_note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:删除这条日历便签')
        delete_body = {
            'noteId': remind_note_id[0]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)
        self.assertEqual(200, delete_res.status_code, msg='状态码有问题')

        info('STEP:删除回收站中这条日历便签主体')
        empty_recycle_note_body = {
            'noteIds': [remind_note_id[0]]
        }
        empty_res = self.apiRe.note_post(self.emptyRecycleNoteUrl, self.user_id, self.sid, empty_recycle_note_body)
        self.assertEqual(200, empty_res.status_code, msg='状态码异常')

        info('STEP:更新已删除的便签主体')
        remind_time = int(time.time() * 1000)
        update_body = {
            'noteId': remind_note_id[0],
            'remindTime': remind_time,
            'remindType': 0
        }
        update_res = self.apiRe.note_post(self.url, self.user_id, self.sid, update_body)
        # 校验状态码
        self.assertEqual(403, update_res.status_code, msg='状态码有问题')

    def testCase04_state_limit(self):
        """更新便签主体接口 状态限制：用户有1条日历便签在回收站中被恢复"""
        info('STEP:新建一条日历便签')
        remind_note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:删除这条日历便签主体')
        delete_body = {
            'noteId': remind_note_id[0]
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)
        self.assertEqual(200, delete_res.status_code, msg='状态码有问题')

        info('STEP:恢复那条便签数据')
        recover_body = {
            'userId': self.user_id,
            'noteIds': [remind_note_id[0]]
        }
        recover_res = self.apiRe.note_patch(self.recoverRecycleNoteUrl, self.sid, recover_body)
        self.assertEqual(200, recover_res.status_code, msg='状态码异常')

        info('STEP:更新已恢复的便签主体')
        remind_time = int(time.time() * 1000)
        update_body = {
            'noteId': remind_note_id[0],
            'remindTime': remind_time,
            'remindType': 1
        }
        update_res = self.apiRe.note_post(self.url, self.user_id, self.sid, update_body)
        # 校验状态码
        self.assertEqual(200, update_res.status_code, msg='状态码有问题')
        # 校验数据源
        info('STEP:获取日历便签列表')
        remind_note_list_body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 9999
        }
        get_remind_note_list = self.apiRe.note_post(self.getRemindNoteListUrl, self.user_id, self.sid,
                                                    remind_note_list_body)
        for i in get_remind_note_list.json()['webNotes']:
            if i['noteId'] == remind_note_id[0]:
                self.assertEqual(1, i['remindType'], msg='remindType的值不等于1')  # 先描述期望值，再描述结果

    def testCase05_userB_update_userA_RemindNote(self):
        """操作对象：用户B更新用户A的日历便签主体"""
        info('STEP:新建一条日历便签')
        remind_note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:用户B更新用户A的日历便签主体')
        remind_time = int(time.time() * 1000)
        body = {
            'noteId': remind_note_id[0],
            'remindTime': remind_time,
            'remindType': 1
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sidB, body)
        # 校验状态码
        self.assertEqual(412, res.status_code, msg='状态码有问题')
        # 校验数据源
        info('STEP:获取日历便签列表')
        remind_note_list_body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 9999
        }
        get_remind_note_list = self.apiRe.note_post(self.getRemindNoteListUrl, self.user_id, self.sid,
                                                    remind_note_list_body)
        for i in get_remind_note_list.json()['webNotes']:
            if i['noteId'] == remind_note_id[0]:
                self.assertEqual(0, i['remindType'], msg='被用户B更新成功了，remindType的值不等于0')  # 先描述期望值，再描述结果
