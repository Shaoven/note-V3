import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn


@class_case_log
class TestGetHomeNoteList(unittest.TestCase):
    """获取首页便签列表接口 接口input"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    host = envConfig['host']
    sid = envConfig['sid']
    apiRe = ApiRe()
    special = apiConfig['GetHomeNoteList']['special']

    def testCase01_sid_not_exist(self):
        """获取首页便签列表接口 sid不存在"""
        user_id = 505807555
        start_index = 0
        rows = 1
        path = f'/v3/notesvr/user/{user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        sid = '123asd'
        res = self.apiRe.note_get(url, sid)
        self.assertEqual(401, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase02_user_id_is_too_long(self):
        """获取首页便签列表接口 user_id的长度=1000"""
        user_id = '5' * 1000
        start_index = 0
        rows = 1
        path = f'/v3/notesvr/user/{user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    @parameterized.expand(special)
    def testCase03_user_id_special(self, spe):
        """获取首页便签列表接口 user_id输入特殊字符@#￥%……&*（；"""
        user_id = '505807555' + spe
        start_index = 0
        rows = 1
        path = f'/v3/notesvr/user/{user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase04_user_id_english_big_small(self):
        """获取首页便签列表接口 user_id输入英文大小写"""
        user_id = '505807555Ss'
        start_index = 0
        rows = 1
        path = f'/v3/notesvr/user/{user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase05_user_id_input_chinese(self):
        """获取首页便签列表接口 user_id输入中文"""
        user_id = '505807555测试'
        start_index = 0
        rows = 1
        path = f'/v3/notesvr/user/{user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase06_user_id_input_none(self):
        """ 获取首页便签列表接口 user_id输入空值“” """
        user_id = ''
        start_index = 0
        rows = 1
        path = f'/v3/notesvr/user/{user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        self.assertEqual(404, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase07_user_id_input_sql(self):
        """ 获取首页便签列表接口 user_id输入" or " 1= 1 """
        user_id = '505807555' + '" or " 1= 1'
        start_index = 0
        rows = 1
        path = f'/v3/notesvr/user/{user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase8_user_id_input_sql(self):
        """ 获取首页便签列表接口 user_id输入' or ' 1= 1 """
        user_id = '505807555' + "' or ' 1= 1"
        start_index = 0
        rows = 1
        path = f'/v3/notesvr/user/{user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase9_startIndex_input_special_number(self):
        """ 获取首页便签列表接口 startIndex输入特殊值：0 """
        user_id = '505807555'
        start_index = 0
        rows = 1
        path = f'/v3/notesvr/user/{user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase10_startIndex_input_special_number(self):
        """ 获取首页便签列表接口 startIndex输入特殊值：-1 """
        user_id = '505807555'
        start_index = -1
        rows = 1
        path = f'/v3/notesvr/user/{user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase11_startIndex_input_min_number(self):
        """ 获取首页便签列表接口 startIndex输入最小值：-2147483649 """
        user_id = '505807555'
        start_index = -2147483649
        rows = 1
        path = f'/v3/notesvr/user/{user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase12_startIndex_input_max_number(self):
        """ 获取首页便签列表接口 startIndex输入最大值：2147483648 """
        user_id = '505807555'
        start_index = 2147483648
        rows = 1
        path = f'/v3/notesvr/user/{user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase13_startIndex_input_float_number(self):
        """ 获取首页便签列表接口 startIndex输入小数：1.5 """
        user_id = '505807555'
        start_index = 1.5
        rows = 1
        path = f'/v3/notesvr/user/{user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase14_startIndex_input_string_number(self):
        """ 获取首页便签列表接口 startIndex输入字符串形式的数值：“1” """
        user_id = '505807555'
        start_index = '1'
        rows = 1
        path = f'/v3/notesvr/user/{user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase15_startIndex_input_none(self):
        """ 获取首页便签列表接口 startIndex输入空值‘’ """
        user_id = '505807555'
        start_index = ''
        rows = 1
        path = f'/v3/notesvr/user/{user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        self.assertEqual(404, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase16_rows_input_special_number(self):
        """ 获取首页便签列表接口 rows输入特殊值：0 """
        user_id = '505807555'
        start_index = 0
        rows = 0
        path = f'/v3/notesvr/user/{user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase17_rows_input_special_number(self):
        """ 获取首页便签列表接口 rows输入特殊值：-1 """
        user_id = '505807555'
        start_index = 0
        rows = -1
        path = f'/v3/notesvr/user/{user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase18_rows_input_min_number(self):
        """ 获取首页便签列表接口 rows输入最小值：-2147483649 """
        user_id = '505807555'
        start_index = 0
        rows = -2147483649
        path = f'/v3/notesvr/user/{user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase19_rows_input_max_number(self):
        """ 获取首页便签列表接口 rows输入最大值：2147483648 """
        user_id = '505807555'
        start_index = 0
        rows = 2147483648
        path = f'/v3/notesvr/user/{user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase20_rows_input_float_number(self):
        """ 获取首页便签列表接口 rows输入小数：1.5 """
        user_id = '505807555'
        start_index = 0
        rows = 1.5
        path = f'/v3/notesvr/user/{user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase21_rows_input_string_number(self):
        """ 获取首页便签列表接口 rows输入字符串形式的数值：“1” """
        user_id = '505807555'
        start_index = 0
        rows = '1'
        path = f'/v3/notesvr/user/{user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase22_rows_input_none(self):
        """ 获取首页便签列表接口 rows输入空值：‘’ """
        user_id = '505807555'
        start_index = 0
        rows = ''
        path = f'/v3/notesvr/user/{user_id}/home/startindex/{start_index}/rows/{rows}/notes'
        url = self.host + path
        res = self.apiRe.note_get(url, self.sid)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
