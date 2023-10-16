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
    mustKey = apiConfig['DeleteNote']['must_key']
    special = apiConfig['DeleteNote']['special']

    @parameterized.expand(mustKey)
    def testCase01_input_must_key(self, dic):
        """删除便签接口 必填校验"""
        info('STEP:清空数据')
        self.deleteNote.delete_notes()

        info('STEP:新建一条便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:请求删除便签接口')
        body = {
            'noteId': note_id[0]
        }
        body.pop(dic['key'])
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(dic['code'], res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase02_lost_x_user_key(self):
        """删除便签接口 未传入X-user-key"""
        info('STEP:清空数据')
        self.deleteNote.delete_notes()

        info('STEP:新建一条便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:请求删除便签接口')
        body = {
            'noteId': note_id[0]
        }
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid}'
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body, headers)
        self.assertEqual(412, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase03_note_id_is_too_long(self):
        """删除便签接口 note_id的长度=1000"""
        info('STEP:清空数据')
        self.deleteNote.delete_notes()

        info('STEP:新建一条便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:请求删除便签接口')
        body = {
            'noteId': note_id[0] + 'test' * 250
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    @parameterized.expand(special)
    def testCase04_note_id_special(self, spe):
        """删除便签接口 note_id输入特殊字符@#￥%……&*（；"""
        info('STEP:清空数据')
        self.deleteNote.delete_notes()

        info('STEP:新建一条便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:请求删除便签接口')
        body = {
            'noteId': note_id[0] + spe,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase05_note_id_english_big_small(self):
        """删除便签接口 note_id输入英文大小写"""
        info('STEP:清空数据')
        self.deleteNote.delete_notes()

        info('STEP:新建一条便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:请求删除便签接口')
        body = {
            'noteId': note_id[0] + 'Ss',
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase06_note_id_input_chinese(self):
        """删除便签接口 note_id输入中文"""
        info('STEP:清空数据')
        self.deleteNote.delete_notes()

        info('STEP:新建一条便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:请求删除便签接口')
        body = {
            'noteId': note_id[0] + '便签',
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase07_note_id_input_none(self):
        """删除便签接口 note_id输入空值None"""
        note_id = None
        body = {
            'noteId': note_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase08_note_id_input_kong(self):
        """删除便签接口 note_id输入"" """
        note_id = ""
        body = {
            'noteId': note_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase09_note_id_input_sql(self):
        """ 删除便签接口 note_id输入" or " 1= 1 """
        info('STEP:清空数据')
        self.deleteNote.delete_notes()

        info('STEP:新建一条便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:请求删除便签接口')
        body = {
            'noteId': note_id[0] + '" or " 1 = 1',
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase10_note_id_input_sql(self):
        """ 删除便签接口 note_id输入' or ' 1= 1 """
        info('STEP:清空数据')
        self.deleteNote.delete_notes()

        info('STEP:新建一条便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:请求删除便签接口')
        body = {
            'noteId': note_id[0] + "' or ' 1 = 1",
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
