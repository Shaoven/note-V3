import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn


@class_case_log
class TestCreateNote(unittest.TestCase):
    """新建便签接口level1"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['CreateNote']['Path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    sidB = envConfig['sidB']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    createNoteInfoPath = apiConfig['CreateNoteInfo']['Path']
    createNoteInfoUrl = host + createNoteInfoPath
    startIndex = 0
    rows = 9999
    getHomeNotePath = f'/v3/notesvr/user/{user_id}/home/startindex/{startIndex}/rows/{rows}/notes'
    getHomeNoteUrl = host + getHomeNotePath

    def testCase01_userB_create_userA_note(self):
        """操作对象：用户B给用户A上传普通便签"""
        info('STEP:新建便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        create_note_info_body = {
            'noteId': note_id
        }
        create_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid,
                                                    create_note_info_body)

        info('STEP:新建便签内容')
        body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': create_note_info_res.json()['infoVersion'],
            'BodyType': 1.5
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sidB, body)
        self.assertEqual(412, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
        # 校验首页便签有没有这条便签
        info('STEP:请求获取首页便签接口')
        home_note_res = self.apiRe.note_get(self.getHomeNoteUrl, self.sid)
        self.assertEqual(200, home_note_res.status_code, msg='状态码异常')
        note_ids = []
        for i in home_note_res.json()['webNotes']:
            note_ids.append(i['noteId'])
        self.assertNotIn(note_id, note_ids, msg='id在')

    def testCase02_no_info_create_note(self):
        """时序：在未进行便签主体新建时，请求新建便签内容"""
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        info('STEP:新建便签内容')
        body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 'infoVersion',
            'BodyType': 1.5
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sidB, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
