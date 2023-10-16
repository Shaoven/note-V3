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


@class_case_log
class TestGetHomeNoteList(unittest.TestCase):
    """获取首页便签列表接口level1"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    host = envConfig['host']
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    cookies = {'wps_sid': sid}
    startIndex = 0
    rows = 10
    path = f'/v3/notesvr/user/{user_id}/home/startindex/{startIndex}/rows/{rows}/notes'
    url = host + path
    apiRe = ApiRe()
    createNoteInfoPath = apiConfig['CreateNoteInfo']['Path']
    createNoteInfoUrl = host + createNoteInfoPath
    createNotePath = apiConfig['CreateNote']['Path']
    createNoteUrl = host + createNotePath
    createNote = CreateNotes()
    deleteNote = DeleteNotes()

    def testCase01_major(self):
        """获取1条首页便签数据"""
        self.deleteNote.delete_notes()
        note_ids = self.createNote.create_notes(1)

        info('STEP:请求获取首页便签列表接口')
        get_home_note_list_res = self.apiRe.note_get(url=self.url, sid=self.sid)
        # 校验状态码
        self.assertEqual(200, get_home_note_list_res.status_code, msg='状态码异常')
        # 校验输出结果
        expect_output = {'responseTime': int, 'webNotes': [
            {'noteId': str, 'createTime': int, 'star': int, 'remindTime': int, 'remindType': int, 'infoVersion': int,
             'infoUpdateTime': int, 'groupId': None, 'title': str, 'summary': str, 'thumbnail': None,
             'contentVersion': int, 'contentUpdateTime': int}]}
        CheckTools().check_output(expect_output, get_home_note_list_res.json())

        notes_id = []
        for i in get_home_note_list_res.json()['webNotes']:
            notes_id.append(i['noteId'])

        # 数据源校验
        self.assertEqual(note_ids, notes_id, msg='note_id不存在')
