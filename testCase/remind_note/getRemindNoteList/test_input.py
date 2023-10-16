import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn
from businessCommon.create_remind_notes import CreateRemindNotes
from businessCommon.delete_remind_notes import DeleteRemindNotes


@class_case_log
class TestGetRemindNoteList(unittest.TestCase):
    """查看日历下便签接口 接口input"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['GetRemindNoteList']['Path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    must_key = apiConfig['GetRemindNoteList']['must_key']
    createRemindNote = CreateRemindNotes()
    deleteRemindNote = DeleteRemindNotes()

    def testCase01_lost_x_user_key(self):
        """查看日历下便签接口 未传入X-user-key"""
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        remind_note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 9999
        }
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid}'
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body, headers)
        self.assertEqual(412, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    @parameterized.expand(must_key)
    def testCase02_must_key(self, dic):
        """查看日历下便签接口 接口input：key不存在"""
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 9999
        }
        body.pop(dic['key'])
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(dic['code'], res.status_code, msg='状态码异常')

    def testCase03_remindStartTime_input_special_number(self):
        """ 查看日历下便签接口 remindStartTime输入特殊值：0 """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        remind_note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 0,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 9999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase04_remindStartTime_input_special_number(self):
        """ 查看日历下便签接口 remindStartTime输入特殊值：-1 """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        remind_note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': -1,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 9999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase05_remindStartTime_input_min_number(self):
        """ 查看日历下便签接口 remindStartTime输入最小值：-2147483649 """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        remind_note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': -2147483649,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 9999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase06_remindStartTime_input_max_number(self):
        """ 查看日历下便签接口 remindStartTime输入最大值：2147483648 """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        remind_note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 2147483648,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 9999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase07_remindStartTime_input_float_number(self):
        """ 查看日历下便签接口 remindStartTime输入小数：1.5 """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        remind_note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1.5,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 9999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase08_remindStartTime_input_string_number(self):
        """ 查看日历下便签接口 remindStartTime输入字符串形式的数值：“1” """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        remind_note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': '1',
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 9999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase09_remindStartTime_input_none(self):
        """ 查看日历下便签接口 remindStartTime输入空值：None """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        remind_note_id = self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': None,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 9999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase10_remindEndTime_input_special_number(self):
        """ 查看日历下便签接口 remindEndTime输入特殊值：0 """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': 0,
            'startIndex': 0,
            'rows': 9999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase11_remindEndTime_input_special_number(self):
        """ 查看日历下便签接口 remindEndTime输入特殊值：-1 """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': -1,
            'startIndex': 0,
            'rows': 9999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase12_remindEndTime_input_min_number(self):
        """ 查看日历下便签接口 remindEndTime输入最小值：-2147483649 """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': -2147483649,
            'startIndex': 0,
            'rows': 9999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase13_remindEndTime_input_max_number(self):
        """ 查看日历下便签接口 remindEndTime输入最大值：2147483648 """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': 2147483648,
            'startIndex': 0,
            'rows': 9999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase14_remindEndTime_input_float_number(self):
        """ 查看日历下便签接口 remindEndTime输入小数：1.5 """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': 1.5,
            'startIndex': 0,
            'rows': 9999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase15_remindEndTime_input_string_number(self):
        """ 查看日历下便签接口 remindEndTime输入字符串形式的数值：“1” """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': '1',
            'startIndex': 0,
            'rows': 9999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase16_remindEndTime_input_none(self):
        """ 查看日历下便签接口 remindEndTime输入空值：None """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': None,
            'startIndex': 0,
            'rows': 9999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase17_startIndex_input_special_number(self):
        """ 查看日历下便签接口 startIndex输入特殊值：0 """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 9999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase18_startIndex_input_special_number(self):
        """ 查看日历下便签接口 startIndex输入特殊值：-1 """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': -1,
            'rows': 9999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase19_startIndex_input_min_number(self):
        """ 查看日历下便签接口 startIndex输入最小值：-2147483649 """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': -2147483649,
            'rows': 9999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase20_startIndex_input_max_number(self):
        """ 查看日历下便签接口 startIndex输入最大值：2147483648 """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 2147483648,
            'rows': 9999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase21_startIndex_input_float_number(self):
        """ 查看日历下便签接口 startIndex输入小数：1.5 """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 1.5,
            'rows': 9999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase22_startIndex_input_string_number(self):
        """ 查看日历下便签接口 startIndex输入字符串形式的数值：“1” """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': '1',
            'rows': 9999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase23_startIndex_input_none(self):
        """ 查看日历下便签接口 startIndex输入空值：None """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': None,
            'rows': 9999
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase24_rows_input_special_number(self):
        """ 查看日历下便签接口 rows输入特殊值：0 """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 0
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase25_rows_input_special_number(self):
        """ 查看日历下便签接口 rows输入特殊值：-1 """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': -1
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase26_rows_input_min_number(self):
        """ 查看日历下便签接口 rows输入最小值：-2147483649 """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': -2147483649
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase27_rows_input_max_number(self):
        """ 查看日历下便签接口 rows输入最大值：2147483648 """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 2147483648
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase28rows_input_float_number(self):
        """ 查看日历下便签接口 rows输入小数：1.5 """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 1.5
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase29_rows_input_string_number(self):
        """ 查看日历下便签接口 rows输入字符串形式的数值：“1” """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': '1'
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase30_rows_input_none(self):
        """ 查看日历下便签接口 rows输入空值：None """
        info('STEP:清空所有日历便签')
        self.deleteRemindNote.delete_remind_notes()

        info('STEP:新建一条日历便签')
        self.createRemindNote.create_remind_notes(1)

        info('STEP:请求查看日历下便签接口')
        body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': None
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
