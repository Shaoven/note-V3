import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn
from businessCommon.create_group import CreateGroups


@class_case_log
class TestUpdateNoteInfo(unittest.TestCase):
    """更新便签主体接口 接口handle"""
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
    startIndex = 0
    rows = 9999
    getHomeNotePath = f'/v3/notesvr/user/{user_id}/home/startindex/{startIndex}/rows/{rows}/notes'
    getHomeNoteUrl = host + getHomeNotePath

    def testCase01_check_update_infoVersion(self):
        """更新便签主体接口 infoVersion的值每次更新时自动递增"""
        # 根据当前时间定义note_id，精确到毫秒
        info('STEP:新建便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id
        }
        # 请求上传便签信息主体接口，并获取接口返回结果
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        update_res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, update_res.status_code, msg='状态码有问题')
        # 校验数据源
        self.assertEqual(res.json()['infoVersion']+1, update_res.json()['infoVersion'], msg='infoVersion更新后没有+1')

    def testCase02_update_group_id_not_exist(self):
        """更新便签主体接口 groupId的值不存在"""
        # 根据当前时间定义note_id，精确到毫秒
        info('STEP:新建便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        group_id = str(self.createGroup.create_group(1))
        body = {
            'noteId': note_id,
            'group_id': group_id
        }
        # 请求上传便签信息主体接口，并获取接口返回结果
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)

        info('STEP:更新便签主体')
        update_body = {
            'noteId': note_id,
            'group_id': str(int(time.time() * 1000))
        }
        update_res = self.apiRe.note_post(self.url, self.user_id, self.sid, update_body)
        # 校验状态码
        self.assertEqual(403, update_res.status_code, msg='状态码有问题')

    def testCase03_state_limit(self):
        """更新便签主体接口 状态限制：用户有1条普通便签在回收站，更新回收站中的便签主体"""
        # 根据当前时间定义note_id，精确到毫秒
        info('STEP:新建便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id,
        }
        # 请求上传便签信息主体接口，并获取接口返回结果
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)

        info('STEP:删除这条便签主体')
        delete_body = {
            'noteId': note_id
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)
        self.assertEqual(200, delete_res.status_code, msg='状态码有问题')

        info('STEP:更新已删除的便签主体')
        update_body = {
            'noteId': note_id,
        }
        update_res = self.apiRe.note_post(self.url, self.user_id, self.sid, update_body)
        # 校验状态码
        self.assertEqual(403, update_res.status_code, msg='状态码有问题')

    def testCase04_state_limit(self):
        """更新便签主体接口 状态限制：用户有1条普通便签在回收站中被清空，更新被清空的便签主体"""
        # 根据当前时间定义note_id，精确到毫秒
        info('STEP:新建便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id,
        }
        # 请求上传便签信息主体接口，并获取接口返回结果
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)

        info('STEP:删除这条便签主体')
        delete_body = {
            'noteId': note_id
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)
        self.assertEqual(200, delete_res.status_code, msg='状态码有问题')

        info('STEP:删除回收站中这条便签主体')
        empty_recycle_note_body = {
            'noteIds': [note_id]
        }
        empty_res = self.apiRe.note_post(self.emptyRecycleNoteUrl, self.user_id, self.sid, empty_recycle_note_body)
        self.assertEqual(200, empty_res.status_code, msg='状态码异常')

        info('STEP:更新已删除的便签主体')
        update_body = {
            'noteId': note_id,
        }
        update_res = self.apiRe.note_post(self.url, self.user_id, self.sid, update_body)
        # 校验状态码
        self.assertEqual(403, update_res.status_code, msg='状态码有问题')

    def testCase05_state_limit(self):
        """更新便签主体接口 状态限制：用户有1条普通便签在回收站中被恢复"""
        # 根据当前时间定义note_id，精确到毫秒
        info('STEP:新建便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id,
        }
        # 请求上传便签信息主体接口，并获取接口返回结果
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)

        info('STEP:删除这条便签主体')
        delete_body = {
            'noteId': note_id
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)
        self.assertEqual(200, delete_res.status_code, msg='状态码有问题')

        info('STEP:恢复那条便签数据')
        recover_body = {
            'userId': self.user_id,
            'noteIds': [note_id]
        }
        recover_res = self.apiRe.note_patch(self.recoverRecycleNoteUrl, self.sid, recover_body)
        self.assertEqual(200, recover_res.status_code, msg='状态码异常')

        info('STEP:更新已恢复的便签主体')
        update_body = {
            'noteId': note_id,
        }
        update_res = self.apiRe.note_post(self.url, self.user_id, self.sid, update_body)
        # 校验状态码
        self.assertEqual(200, update_res.status_code, msg='状态码有问题')
        # 校验数据源
        self.assertEqual(res.json()['infoVersion'] + 1, update_res.json()['infoVersion'], msg='infoVersion更新后没有+1')

    def testCase06_userB_update_userA_note(self):
        """操作对象：用户B更新用户A的普通便签主体"""
        info('STEP:新建便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id,
            'star': 0
        }
        # 请求上传便签信息主体接口，并获取接口返回结果
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)

        info('STEP:用户B更新用户A的便签主体')
        update_body = {
            'noteId': note_id,
            'star': 1
        }
        update_res = self.apiRe.note_post(self.url, self.user_id, self.sidB, update_body)
        # 校验状态码
        self.assertEqual(412, update_res.status_code, msg='状态码有问题')
