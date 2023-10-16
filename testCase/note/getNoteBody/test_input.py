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
class TestGetNoteBody(unittest.TestCase):
    """获取便签内容接口level1"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['GetNoteBody']['Path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    must_key = apiConfig['GetNoteBody']['must_key']
    createNote = CreateNotes()
    deleteNote = DeleteNotes()

    def testCase01_noteIds_input_kong(self):
        """获取便签内容接口 接口input：输入[]"""
        info('STEP:清空首页便签数据')
        self.deleteNote.delete_notes()

        info('STEP:新建一条便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:获取便签内容')
        body = {
            'noteIds': [],
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(500, res.status_code, msg='状态码异常')

    def testCase02_noteIds_input_sub_object(self):
        """获取便签内容接口 接口input：输入子对象 ["234", ["123", "123"]]"""
        info('STEP:清空首页便签数据')
        self.deleteNote.delete_notes()

        info('STEP:新建3条便签')
        note_id = self.createNote.create_notes(3)

        info('STEP:获取便签内容')
        body = {
            'noteIds': [note_id[0], [note_id[1], note_id[2]]],
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(500, res.status_code, msg='状态码异常')

    def testCase03_noteIds_list_obj(self):
        """获取便签内容接口 接口input：列表值的类型校验：int"""
        info('STEP:清空首页便签数据')
        self.deleteNote.delete_notes()

        info('STEP:新建1条便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:获取便签内容')
        body = {
            'noteIds': [int(note_id[0])],
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(500, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(0, len(res.json()['noteBodies']), msg='返回的数据不等于0')

    def testCase04_noteIds_list_obj(self):
        """获取便签内容接口 接口input：列表值的类型校验：float"""
        info('STEP:清空首页便签数据')
        self.deleteNote.delete_notes()

        info('STEP:新建1条便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:获取便签内容')
        body = {
            'noteIds': [float(note_id[0])],
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(500, res.status_code, msg='状态码异常')
        # 校验数据源
        self.assertEqual(0, len(res.json()['noteBodies']), msg='返回的数据不等于0')

    def testCase05_noteIds_input_none(self):
        """获取便签内容接口 接口input：noteIds输入None"""
        info('STEP:清空首页便签数据')
        self.deleteNote.delete_notes()

        info('STEP:新建1条便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:获取便签内容')
        body = {
            'noteIds': None,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(500, res.status_code, msg='状态码异常')

    @parameterized.expand(must_key)
    def testCase06_must_key(self, dic):
        """获取便签内容接口 接口input：key不存在"""
        info('STEP:清空首页便签数据')
        self.deleteNote.delete_notes()

        info('STEP:新建1条便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:获取便签内容')
        body = {
            'noteIds': [note_id[0]],
        }
        body.pop(dic['key'])
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(dic['code'], res.status_code, msg='状态码异常')

    def testCase07_noteIds_input_sql(self):
        """ 获取便签内容接口 noteIds输入" or " 1= 1 """
        info('STEP:清空首页便签数据')
        self.deleteNote.delete_notes()

        info('STEP:新建1条便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:获取便签内容')
        body = {
            'noteIds': [note_id[0] + "' or ' 1= 1"],
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(500, res.status_code, msg='状态码异常')

    def testCase08_noteIds_input_sql(self):
        """ 获取便签内容接口 noteIds输入' or ' 1= 1 """
        info('STEP:清空首页便签数据')
        self.deleteNote.delete_notes()

        info('STEP:新建1条便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:获取便签内容')
        body = {
            'noteIds': [note_id[0] + '" or " 1= 1'],
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(500, res.status_code, msg='状态码异常')

    def testCase09_lost_x_user_key(self):
        """获取便签内容接口 未传入X-user-key"""
        info('STEP:清空首页便签数据')
        self.deleteNote.delete_notes()

        info('STEP:新建1条便签')
        note_id = self.createNote.create_notes(1)

        info('STEP:获取便签内容')
        body = {
            'noteIds': [note_id[0]],
        }
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid}'
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body, headers)
        self.assertEqual(412, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
