import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn


@class_case_log
class TestCreateGroup(unittest.TestCase):
    """新建分组接口 接口input"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['CreateGroup']['Path']
    mustKey = apiConfig['CreateGroup']['must_key']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    getGroupListPath = apiConfig['GetGroupList']['Path']
    get_group_list_url = host + getGroupListPath
    special = apiConfig['CreateGroup']['special']

    @parameterized.expand(mustKey)
    def testCase01_input_must_key(self, dic):
        """新建分组 必填校验"""
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        body.pop(dic['key'])
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(dic['code'], res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase02_lost_x_user_key(self):
        """新建分组接口 未传入X-user-key"""
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid}'
        }
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body, headers)
        self.assertEqual(412, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase03_group_id_is_too_long(self):
        """新建分组接口 group_id的长度=100"""
        group_id = str(int(time.time() * 1000)) + '_test_groupId' + 'test'*250
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    @parameterized.expand(special)
    def testCase04_group_id_special(self, spe):
        """新建分组接口 group_id输入特殊字符@#￥%……&*（；"""
        group_id = str(int(time.time() * 1000)) + '_test_groupId' + spe
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase05_group_id_english_big_small(self):
        """新建分组接口 group_id输入英文大小写"""
        group_id = str(int(time.time() * 1000)) + '_test_GROUPID'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase05_group_id_input_chinese(self):
        """新建分组接口 group_id输入中文"""
        group_id = str(int(time.time() * 1000)) + '_test_分组名称'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase06_group_id_input_none(self):
        """新建分组接口 group_id输入空值None"""
        group_id = None
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase07_group_id_input_kong(self):
        """ 新建分组接口 group_id输入"" """
        group_id = ""
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase08_group_id_input_sql(self):
        """ 新建分组接口 group_id输入" or " 1= 1 """
        group_id = str(int(time.time() * 1000)) + '_test_groupId' + '" or " 1= 1'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase09_group_id_input_sql(self):
        """ 新建分组接口 group_id输入' or ' 1= 1 """
        group_id = str(int(time.time() * 1000)) + '_test_groupId' + "' or ' 1= 1"
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase10_group_name_is_too_long(self):
        """新建分组接口 group_name的长度=100"""
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName' + 'test'*250
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    @parameterized.expand(special)
    def testCase11_group_name_special(self, spe):
        """新建分组接口 group_name输入特殊字符@#￥%……&*（；"""
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName' + spe
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase12_group_name_english_big_small(self):
        """新建分组接口 group_name输入英文大小写"""
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase13_group_name_input_chinese(self):
        """新建分组接口 group_name输入中文"""
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_分组名称'
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase14_group_name_input_none(self):
        """新建分组接口 group_name输入空值None"""
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = None
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase15_group_name_input_kong(self):
        """ 新建分组接口 group_name输入"" """
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = ""
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase16_group_name_input_sql(self):
        """ 新建分组接口 group_name输入" or " 1= 1 """
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName' + '" or " 1= 1'
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase17_group_name_input_sql(self):
        """ 新建分组接口 group_name输入' or ' 1= 1 """
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName' + "' or ' 1= 1"
        body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase18_order_input_special_number(self):
        """ 新建分组接口 order输入特殊值：0 """
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
            'order': 0
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase19_order_input_special_number(self):
        """ 新建分组接口 order输入特殊值：-1 """
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
            'order': -1
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase20_order_input_min_number(self):
        """ 新建分组接口 order输入最小值：-2147483649 """
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
            'order': -2147483649
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase21_order_input_max_number(self):
        """ 新建分组接口 order输入最大值：2147483648 """
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
            'order': 2147483648
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase22_order_input_float_number(self):
        """ 新建分组接口 order输入小数：1.5 """
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
            'order': 1.5
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase23_order_input_string_number(self):
        """ 新建分组接口 order输入字符串形式的数值：“1” """
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
            'order': "1"
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase24_order_input_none(self):
        """ 新建分组接口 order输入空值：None """
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name,
            'order': None
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
