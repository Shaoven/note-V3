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
class TestCreateRemindNoteInfo(unittest.TestCase):
    """新建日历便签主体接口level1"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['CreateNoteInfo']['Path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    special = apiConfig['CreateNoteInfo']['special']
    createGroup = CreateGroups()

    def testCase01_remindTime_input_special_number(self):
        """ 新建日历便签主体接口 remindTime输入特殊值：0 """
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id,
            'remindTime': 0,
            'remindType': 0
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase02_remindTime_input_special_number(self):
        """ 新建日历便签主体接口 remindTime输入特殊值：-1 """
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id,
            'remindTime': -1,
            'remindType': 0
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')

    def testCase03_remindTime_input_min_number(self):
        """ 新建日历便签主体接口 remindTime输入最小值：-2147483649 """
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id,
            'remindTime': -2147483649,
            'remindType': 0
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')

    def testCase04_remindTime_input_max_number(self):
        """ 新建日历便签主体接口 remindTime输入最大值：2147483648 """
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id,
            'remindTime': 2147483648,
            'remindType': 0
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')

    def testCase05_remindTime_input_float_number(self):
        """ 新建日历便签主体接口 remindTime输入小数：1.5 """
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id,
            'remindTime': 1.5,
            'remindType': 0
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase06_remindTime_input_string_number(self):
        """ 新建日历便签主体接口 remindTime输入字符串形式的数值：“1” """
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id,
            'remindTime': '1',
            'remindType': 0
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase07_remindTime_input_none(self):
        """ 新建日历便签主体接口 remindTime输入空值‘’ """
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id,
            'remindTime': '',
            'remindType': 0
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')

    def testCase08_remindType_input_special_number(self):
        """ 新建日历便签主体接口 remindType输入特殊值：0 """
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        remind_time = int(time.time() * 1000)
        body = {
            'noteId': note_id,
            'remindTime': remind_time,
            'remindType': 0
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase09_remindType_input_special_number(self):
        """ 新建日历便签主体接口 remindType输入特殊值：-1 """
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        remind_time = int(time.time() * 1000)
        body = {
            'noteId': note_id,
            'remindTime': remind_time,
            'remindType': -1
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')

    def testCase10_remindType_input_min_number(self):
        """ 新建日历便签主体接口 remindType输入最小值：-2147483649 """
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        remind_time = int(time.time() * 1000)
        body = {
            'noteId': note_id,
            'remindTime': remind_time,
            'remindType': -2147483649
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')

    def testCase11_remindType_input_max_number(self):
        """ 新建日历便签主体接口 remindType输入最大值：2147483648 """
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        remind_time = int(time.time() * 1000)
        body = {
            'noteId': note_id,
            'remindTime': remind_time,
            'remindType': 2147483648
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')

    def testCase12_remindType_input_float_number(self):
        """ 新建日历便签主体接口 remindType输入小数：1.5 """
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        remind_time = int(time.time() * 1000)
        body = {
            'noteId': note_id,
            'remindTime': remind_time,
            'remindType': 1.5
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase13_remindType_input_string_number(self):
        """ 新建日历便签主体接口 remindType输入字符串形式的数值：“1” """
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        remind_time = int(time.time() * 1000)
        body = {
            'noteId': note_id,
            'remindTime': remind_time,
            'remindType': '1'
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase14_remindType_input_none(self):
        """ 新建日历便签主体接口 remindType输入空值‘’ """
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        remind_time = int(time.time() * 1000)
        body = {
            'noteId': note_id,
            'remindTime': remind_time,
            'remindType': ''
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')
