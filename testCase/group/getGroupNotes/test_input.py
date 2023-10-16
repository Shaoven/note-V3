import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn


@class_case_log
class TestCreateGroupNotes(unittest.TestCase):
    """获取分组便签接口 接口input"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['GetGroupNote']['Path']
    mustKey = apiConfig['GetGroupNote']['must_key']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    createGroupPath = apiConfig['CreateGroup']['Path']
    createGroupUrl = host + createGroupPath
    createNoteInfoPath = apiConfig['CreateNoteInfo']['Path']
    createNoteInfoUrl = host + createNoteInfoPath
    createNotePath = apiConfig['CreateNote']['Path']
    createNoteUrl = host + createNotePath
    special = apiConfig['GetGroupNote']['special']

    @parameterized.expand(mustKey)
    def testCase01_input_must_key(self, dic):
        """获取分组便签接口 必填校验"""
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:请求获取分组便签接口')
        get_group_note_body = {
            'groupId': group_id,
            'startIndex': 0,
            'rows': 10
        }
        get_group_note_body.pop(dic['key'])
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, get_group_note_body)
        self.assertEqual(dic['code'], res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase02_lost_x_user_key(self):
        """获取分组便签接口 未传入X-user-key"""
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:获取分组便签接口')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid}'
        }
        get_group_note_body = {
            'groupId': group_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, get_group_note_body, headers)
        self.assertEqual(412, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase03_group_id_is_too_long(self):
        """获取分组便签接口 group_id的长度=1000"""
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId' + 'test'*250
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        # self.assertEqual(200, create_group_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:获取分组便签接口')
        body = {
            'groupId': group_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    @parameterized.expand(special)
    def testCase04_group_id_special(self, spe):
        """获取分组便签接口 group_id输入特殊字符@#￥%……&*（；"""
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId' + spe
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)

        info('STEP:获取分组便签接口')
        body = {
            'groupId': group_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase05_group_id_english_big_small(self):
        """获取分组便签接口 group_id输入英文大小写"""
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_GROUPID'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)

        info('STEP:获取分组便签接口')
        body = {
            'groupId': group_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase06_group_id_input_chinese(self):
        """获取分组便签接口 group_id输入中文"""
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_分组名称'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)

        info('STEP:获取分组便签接口')
        body = {
            'groupId': group_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase07_group_id_input_none(self):
        """获取分组便签接口 group_id输入空值None"""
        info('STEP:新建分组')
        group_id = None
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)

        info('STEP:获取分组便签接口')
        body = {
            'groupId': group_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase08_group_id_input_kong(self):
        """获取分组便签接口 group_id输入"" """
        info('STEP:新建分组')
        group_id = ""
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)

        info('STEP:获取分组便签接口')
        body = {
            'groupId': group_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase09_group_id_input_sql(self):
        """ 获取分组便签接口 group_id输入" or " 1= 1 """
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId' + '" or " 1= 1'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)

        info('STEP:获取分组便签接口')
        body = {
            'groupId': group_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase10_group_id_input_sql(self):
        """ 获取分组便签接口 group_id输入' or ' 1= 1 """
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId' + "' or ' 1= 1"
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)

        info('STEP:获取分组便签接口')
        body = {
            'groupId': group_id,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase11_startIndex_input_special_number(self):
        """ 获取分组便签接口 startIndex输入特殊值：0 """
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')

        info('STEP:获取分组便签接口')
        body = {
            'groupId': group_id,
            'startIndex': 0
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase12_startIndex_input_special_number(self):
        """ 获取分组便签接口 startIndex输入特殊值：-1 """
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')

        info('STEP:获取分组便签接口')
        body = {
            'groupId': group_id,
            'startIndex': -1
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase13_startIndex_input_min_number(self):
        """ 获取分组便签接口 startIndex输入最小值：-2147483649 """
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')

        info('STEP:获取分组便签接口')
        body = {
            'groupId': group_id,
            'startIndex': -2147483649
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase14_startIndex_input_max_number(self):
        """ 获取分组便签接口 startIndex输入最大值：2147483648 """
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')

        info('STEP:获取分组便签接口')
        body = {
            'groupId': group_id,
            'startIndex': 2147483648
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase15_startIndex_input_float_number(self):
        """ 获取分组便签接口 startIndex输入小数：1.5 """
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')

        info('STEP:获取分组便签接口')
        body = {
            'groupId': group_id,
            'startIndex': 1.5
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase16_startIndex_input_string_number(self):
        """ 获取分组便签接口 startIndex输入字符串形式的数值：“1” """
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')

        info('STEP:获取分组便签接口')
        body = {
            'groupId': group_id,
            'startIndex': "1"
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase17_startIndex_input_none(self):
        """ 获取分组便签接口 startIndex输入空值：None """
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')

        info('STEP:获取分组便签接口')
        body = {
            'groupId': group_id,
            'startIndex': None
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase18_rows_input_special_number(self):
        """ 获取分组便签接口 rows输入特殊值：0 """
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')

        info('STEP:获取分组便签接口')
        body = {
            'groupId': group_id,
            'rows': 0
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase19_rows_input_special_number(self):
        """ 获取分组便签接口 rows输入特殊值：-1 """
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')

        info('STEP:获取分组便签接口')
        body = {
            'groupId': group_id,
            'rows': -1
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase20_rows_input_min_number(self):
        """ 获取分组便签接口 rows输入最小值：-2147483649 """
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')

        info('STEP:获取分组便签接口')
        body = {
            'groupId': group_id,
            'rows': -2147483649
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase21_rows_input_max_number(self):
        """ 获取分组便签接口 rows输入最大值：2147483648 """
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')

        info('STEP:获取分组便签接口')
        body = {
            'groupId': group_id,
            'rows': 2147483648
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase22_rows_input_float_number(self):
        """ 获取分组便签接口 rows输入小数：1.5 """
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')

        info('STEP:获取分组便签接口')
        body = {
            'groupId': group_id,
            'rows': 1.5
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase23_rows_input_string_number(self):
        """ 获取分组便签接口 rows输入字符串形式的数值：“1” """
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')

        info('STEP:获取分组便签接口')
        body = {
            'groupId': group_id,
            'rows': "1"
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase24_rows_input_none(self):
        """ 获取分组便签接口 rows输入空值：None """
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')

        info('STEP:获取分组便签接口')
        body = {
            'groupId': group_id,
            'rows': None
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
