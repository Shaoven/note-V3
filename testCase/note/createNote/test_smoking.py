import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn
from businessCommon.delete_notes import DeleteNotes


@class_case_log
class TestCreateNote(unittest.TestCase):
    """新建便签接口level1"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['CreateNote']['Path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    deleteNote = DeleteNotes()
    createNoteInfoPath = apiConfig['CreateNoteInfo']['Path']
    createNoteInfoUrl = host + createNoteInfoPath
    startIndex = 0
    rows = 9999
    getHomeNotePath = f'/v3/notesvr/user/{user_id}/home/startindex/{startIndex}/rows/{rows}/notes'
    getHomeNoteUrl = host + getHomeNotePath

    def testCase01_major(self):
        """新建普通便签"""
        info('STEP:清空首页便签数据')
        self.deleteNote.delete_notes()

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
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验输出结果
        expect_output = {'responseTime': int, 'contentVersion': int, 'contentUpdateTime': int}
        CheckTools().check_output(expect_output, res.json())
        # 校验数据源
        info('STEP:请求获取首页便签接口')
        home_note_res = self.apiRe.note_get(self.getHomeNoteUrl, self.sid)
        self.assertEqual(200, home_note_res.status_code, msg='状态码异常')
        note_ids = []
        for i in home_note_res.json()['webNotes']:
            note_ids.append(i['noteId'])
        self.assertIn(note_id, note_ids, msg='id不在')
