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
class TestDeleteNote(unittest.TestCase):
    """删除便签接口level1"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['DeleteNote']['Path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    createNote = CreateNotes()
    deleteNote = DeleteNotes()
    startIndex = 0
    rows = 9999
    getHomeNotePath = f'/v3/notesvr/user/{user_id}/home/startindex/{startIndex}/rows/{rows}/notes'
    getHomeNoteUrl = host + getHomeNotePath
    recycleNotePath = f'/v3/notesvr/user/{user_id}/invalid/startindex/{startIndex}/rows/{rows}/notes'
    recycleNoteUrl = host + recycleNotePath

    def testCase01_major(self):
        """删除1条普通便签"""
        info('STEP:清空数据')
        self.deleteNote.delete_notes()

        info('STEP:新建一条便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:请求删除便签接口')
        body = {
            'noteId': note_id[0]
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')
        # 校验输出结果
        expect_out = {'responseTime': int}
        CheckTools().check_output(expect_out, res.json())

        # 校验数据源
        info('STEP:请求获取首页便签接口')
        home_res = self.apiRe.note_get(self.getHomeNoteUrl, self.sid)
        self.assertEqual(200, home_res.status_code, msg='状态码异常')
        note_ids = []
        for i in home_res.json()['webNotes']:
            note_ids.append(i['noteId'])
        self.assertNotIn(note_id[0], note_ids, msg='删除不成功')

        info('STEP:请求查看回收站下便签列表')
        recycle_body = {
            'userid': self.user_id,
            'startIndex': 0,
            'rows': 9999
        }
        recycle_res = self.apiRe.note_get(self.recycleNoteUrl, self.sid)
        recycle_note_id = []
        for n in recycle_res.json()['webNotes']:
            recycle_note_id.append(n['noteId'])
        self.assertEqual(note_id, recycle_note_id, msg='便签不在回收站中')
