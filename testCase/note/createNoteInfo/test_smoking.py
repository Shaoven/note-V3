import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn


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

    def testCase01_major(self):
        """新建普通便签主体"""
        # 根据当前时间定义note_id，精确到毫秒
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id
        }
        # 请求上传便签信息主体接口，并获取接口返回结果
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码有问题')
        # 校验输出结果
        expect_output = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
        CheckTools().check_output(expect_output, res.json())
