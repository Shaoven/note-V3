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
class TestCreateNoteInfo(unittest.TestCase):
    """新建便签主体接口level1"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['CreateNoteInfo']['Path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    mustKey = apiConfig['CreateNoteInfo']['must_key']
    special = apiConfig['CreateNoteInfo']['special']
    createGroup = CreateGroups()

    @parameterized.expand(mustKey)
    def testCase01_input_must_key(self, dic):
        """新建便签主体接口 必填校验"""
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id
        }
        body.pop(dic['key'])
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(dic['code'], res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase02_lost_x_user_key(self):
        """新建便签主体接口 未传入X-user-key"""
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id
        }
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid}'
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body, headers)
        self.assertEqual(412, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase03_note_id_is_too_long(self):
        """新建便签主体接口 note_id的长度=1000"""
        note_id = str(int(time.time() * 1000)) + '_test_noteId' + 'test' * 250
        body = {
            'noteId': note_id
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    @parameterized.expand(special)
    def testCase04_note_id_special(self, spe):
        """新建便签主体接口 note_id输入特殊字符@#￥%……&*（；"""
        note_id = str(int(time.time() * 1000)) + '_test_noteId' + spe
        body = {
            'noteId': note_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase05_note_id_english_big_small(self):
        """新建便签主体接口 note_id输入英文大小写"""
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase06_note_id_input_chinese(self):
        """新建便签主体接口 note_id输入中文"""
        note_id = str(int(time.time() * 1000)) + '_test_便签id'
        body = {
            'noteId': note_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase07_note_id_input_none(self):
        """新建便签主体接口 note_id输入空值None"""
        note_id = None
        body = {
            'noteId': note_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase08_note_id_input_kong(self):
        """新建便签主体接口 note_id输入"" """
        note_id = ""
        body = {
            'noteId': note_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase09_note_id_input_sql(self):
        """ 新建便签主体接口 note_id输入" or " 1= 1 """
        note_id = str(int(time.time() * 1000)) + '_test_noteId' + '" or " 1= 1'
        body = {
            'noteId': note_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase10_note_id_input_sql(self):
        """ 新建便签主体接口 note_id输入' or ' 1= 1 """
        note_id = str(int(time.time() * 1000)) + '_test_noteId' + "' or ' 1= 1"
        body = {
            'noteId': note_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase11_star_input_special_number(self):
        """ 新建便签主体接口 star输入特殊值：0 """
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id,
            'star': 0
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase12_star_input_special_number(self):
        """ 新建便签主体接口 star输入特殊值：-1 """
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id,
            'star': -1
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')

    def testCase13_star_input_min_number(self):
        """ 新建便签主体接口 star输入最小值：-2147483649 """
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id,
            'star': -2147483649
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')

    def testCase14_star_input_max_number(self):
        """ 新建便签主体接口 star输入最大值：2147483648 """
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id,
            'star': 2147483648
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')

    def testCase15_star_input_float_number(self):
        """ 新建便签主体接口 star输入小数：1.5 """
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id,
            'star': 1.5
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase16_star_input_string_number(self):
        """ 新建便签主体接口 star输入字符串形式的数值：“1” """
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id,
            'star': '1'
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase17_star_input_none(self):
        """ 新建便签主体接口 star输入空值‘’ """
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id,
            'star': ''
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(404, res.status_code, msg='状态码异常')

    def testCase18_group_id_is_too_long(self):
        """新建便签主体接口 group_id的长度=1000"""
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        group_id = str(int(time.time() * 1000)) + '_test_groupId' + 'test' * 250
        body = {
            'noteId': note_id,
            'groupId': group_id
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(404, res.status_code, msg='状态码异常')

    @parameterized.expand(special)
    def testCase19_group_id_special(self, spe):
        """新建便签主体接口 group_id输入特殊字符@#￥%……&*（；"""
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        group_id = str(self.createGroup.create_group(1)) + spe
        body = {
            'noteId': note_id,
            'groupId': group_id
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase20_group_id_english_big_small(self):
        """新建便签主体接口 group_id输入英文大小写"""
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        group_id = str(self.createGroup.create_group(1)) + 'Aa'
        body = {
            'noteId': note_id,
            'groupId': group_id
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase21_group_id_input_chinese(self):
        """新建便签主体接口 group_id输入中文"""
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        group_id = str(self.createGroup.create_group(1)) + '分组'
        body = {
            'noteId': note_id,
            'groupId': group_id
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase22_group_id_input_none(self):
        """ 新建便签主体接口 group_id输入空值“” """
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        group_id = ''
        body = {
            'noteId': note_id,
            'groupId': group_id
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(404, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase23_group_id_input_sql(self):
        """ 新建便签主体接口 group_id输入" or " 1= 1 """
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        group_id = '505807555' + '" or " 1= 1'
        body = {
            'noteId': note_id,
            'groupId': group_id
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase24_group_id_input_sql(self):
        """ 新建便签主体接口 group_id输入' or ' 1= 1 """
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        group_id = '505807555' + "' or ' 1= 1"
        body = {
            'noteId': note_id,
            'groupId': group_id
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

