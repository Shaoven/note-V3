import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn


@class_case_log
class TestUpdateNote(unittest.TestCase):
    """更新便签接口level1"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['CreateNote']['Path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    sidB = envConfig['sidB']
    user_id = envConfig['user_id']
    userB_id = envConfig['userB_id']
    apiRe = ApiRe()
    createNoteInfoPath = apiConfig['CreateNoteInfo']['Path']
    createNoteInfoUrl = host + createNoteInfoPath
    getNoteBodyPath = apiConfig['GetNoteBody']['Path']
    getNoteBodyUrl = host + getNoteBodyPath
    deleteNotePath = apiConfig['DeleteNote']['Path']
    deleteNoteUrl = host + deleteNotePath
    emptyRecyclePath = apiConfig['EmptyRecycle']['Path']
    emptyRecycleUrl = host + emptyRecyclePath
    recoverNotePath = f'/v3/notesvr/user/{user_id}/notes'
    recoverNoteUrl = host + recoverNotePath

    def testCase01_userB_update_userA_note(self):
        """用户A更新用户B的普通便签内容"""
        info('STEP:新建便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        get_note_info_body = {
            'noteId': note_id
        }
        get_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid, get_note_info_body)
        # 校验状态码
        self.assertEqual(200, get_note_info_res.status_code, msg='状态码有问题')

        info('STEP:新建便签内容')
        body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': get_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码异常')

        info('STEP:更新便签内容')
        update_body = {
            'noteId': note_id,
            'title': 'test_update',
            'summary': 'test_update',
            'body': 'test_update',
            'localContentVersion': get_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        update_res = self.apiRe.note_post(self.url, self.user_id, self.sidB, update_body)
        # 校验状态码
        self.assertEqual(412, update_res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:请求获取便签内容')
        note_body = {
            'noteIds': [note_id]
        }
        note_body_res = self.apiRe.note_post(self.getNoteBodyUrl, self.user_id, self.sid, note_body)
        self.assertEqual(200, note_body_res.status_code, msg='状态码异常')
        for i in note_body_res.json()['noteBodies']:
            if i['noteId'] == note_id:
                self.assertEqual(i['summary'], 'test', msg='summary更新成功')
                self.assertEqual(i['title'], 'test', msg='title更新成功')
                self.assertEqual(i['body'], 'test', msg='body更新成功')

    def testCase02_noteId_not_exist(self):
        """数值限制：noteId的值不存在"""
        info('STEP:新建便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        get_note_info_body = {
            'noteId': note_id
        }
        get_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid, get_note_info_body)
        # 校验状态码
        self.assertEqual(200, get_note_info_res.status_code, msg='状态码有问题')

        info('STEP:新建便签内容')
        body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': get_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码异常')

        info('STEP:更新便签内容')
        update_body = {
            'noteId': '',
            'title': 'test_update',
            'summary': 'test_update',
            'body': 'test_update',
            'localContentVersion': get_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        update_res = self.apiRe.note_post(self.url, self.user_id, self.sid, update_body)
        # 校验状态码
        self.assertEqual(500, update_res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:请求获取便签内容')
        note_body = {
            'noteIds': [note_id]
        }
        note_body_res = self.apiRe.note_post(self.getNoteBodyUrl, self.user_id, self.sid, note_body)
        self.assertEqual(200, note_body_res.status_code, msg='状态码异常')
        for i in note_body_res.json()['noteBodies']:
            if i['noteId'] == note_id:
                self.assertEqual(i['summary'], 'test', msg='summary更新成功')
                self.assertEqual(i['title'], 'test', msg='title更新成功')
                self.assertEqual(i['body'], 'test', msg='body更新成功')

    def testCase03_update_recycle_note(self):
        """用户有1条普通便签在回收站，更新这个便签"""
        info('STEP:新建便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        get_note_info_body = {
            'noteId': note_id
        }
        get_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid, get_note_info_body)
        # 校验状态码
        self.assertEqual(200, get_note_info_res.status_code, msg='状态码有问题')

        info('STEP:新建便签内容')
        body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': get_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码异常')

        info('STEP:删除这个便签')
        delete_body = {
            'noteId': note_id
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)
        self.assertEqual(200, delete_res.status_code, msg='状态码异常')

        info('STEP:更新便签内容')
        update_body = {
            'noteId': note_id,
            'title': 'test_update',
            'summary': 'test_update',
            'body': 'test_update',
            'localContentVersion': get_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        update_res = self.apiRe.note_post(self.url, self.user_id, self.sid, update_body)
        # 校验状态码
        self.assertEqual(200, update_res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:请求获取便签内容')
        note_body = {
            'noteIds': [note_id]
        }
        note_body_res = self.apiRe.note_post(self.getNoteBodyUrl, self.user_id, self.sid, note_body)
        self.assertEqual(200, note_body_res.status_code, msg='状态码异常')
        for i in note_body_res.json()['noteBodies']:
            if i['noteId'] == note_id:
                self.assertEqual(i['summary'], 'test', msg='便签在回收站，summary还是更新成功')
                self.assertEqual(i['title'], 'test', msg='便签在回收站，title还是更新成功')
                self.assertEqual(i['body'], 'test', msg='便签在回收站，body还是更新成功')

    def testCase04_update_delete_note(self):
        """用户有1条普通便签在回收站中被清空，更新这个便签"""
        info('STEP:新建便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        get_note_info_body = {
            'noteId': note_id
        }
        get_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid, get_note_info_body)
        # 校验状态码
        self.assertEqual(200, get_note_info_res.status_code, msg='状态码有问题')

        info('STEP:新建便签内容')
        body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': get_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码异常')

        info('STEP:删除这个便签')
        delete_body = {
            'noteId': note_id
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)
        self.assertEqual(200, delete_res.status_code, msg='状态码异常')

        info('STEP:清空回收站')
        empty_body = {
            'noteIds': [note_id]
        }
        empty_res = self.apiRe.note_post(self.emptyRecycleUrl, self.user_id, self.sid, empty_body)
        self.assertEqual(200, empty_res.status_code, msg='状态码异常')

        info('STEP:更新便签内容')
        update_body = {
            'noteId': note_id,
            'title': 'test_update',
            'summary': 'test_update',
            'body': 'test_update',
            'localContentVersion': get_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        update_res = self.apiRe.note_post(self.url, self.user_id, self.sid, update_body)
        # 校验状态码
        self.assertEqual(200, update_res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:请求获取便签内容')
        note_body = {
            'noteIds': [note_id]
        }
        note_body_res = self.apiRe.note_post(self.getNoteBodyUrl, self.user_id, self.sid, note_body)
        self.assertEqual(200, note_body_res.status_code, msg='状态码异常')
        for i in note_body_res.json()['noteBodies']:
            if i['noteId'] == note_id:
                self.assertEqual(i['summary'], 'test', msg='清空便签后，summary还是更新成功')
                self.assertEqual(i['title'], 'test', msg='清空便签后，title还是更新成功')
                self.assertEqual(i['body'], 'test', msg='清空便签后，body还是更新成功')

    def testCase05_update_recover_note(self):
        """更新在回收站中恢复的普通便签内容"""
        info('STEP:新建便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        get_note_info_body = {
            'noteId': note_id
        }
        get_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid, get_note_info_body)
        # 校验状态码
        self.assertEqual(200, get_note_info_res.status_code, msg='状态码有问题')

        info('STEP:新建便签内容')
        body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': get_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码异常')

        info('STEP:删除这个便签')
        delete_body = {
            'noteId': note_id
        }
        delete_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_body)
        self.assertEqual(200, delete_res.status_code, msg='状态码异常')

        info('STEP:恢复这个便签')
        recover_body = {
            'userId': self.user_id,
            'noteIds': [note_id]
        }
        recover_res = self.apiRe.note_patch(self.recoverNoteUrl, self.sid, recover_body)
        self.assertEqual(200, recover_res.status_code, msg='状态码异常')

        info('STEP:更新便签内容')
        update_body = {
            'noteId': note_id,
            'title': 'test_update',
            'summary': 'test_update',
            'body': 'test_update',
            'localContentVersion': get_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        update_res = self.apiRe.note_post(self.url, self.user_id, self.sid, update_body)
        # 校验状态码
        self.assertEqual(200, update_res.status_code, msg='状态码异常')

        # 校验数据源
        info('STEP:请求获取便签内容')
        note_body = {
            'noteIds': [note_id]
        }
        note_body_res = self.apiRe.note_post(self.getNoteBodyUrl, self.user_id, self.sid, note_body)
        self.assertEqual(200, note_body_res.status_code, msg='状态码异常')
        for i in note_body_res.json()['noteBodies']:
            if i['noteId'] == note_id:
                self.assertEqual(i['summary'], 'test_update', msg='恢复便签后，summary没有更新成功')
                self.assertEqual(i['title'], 'test_update', msg='恢复便签后，title没有更新成功')
                self.assertEqual(i['body'], 'test_update', msg='恢复便签后，body没有更新成功')
