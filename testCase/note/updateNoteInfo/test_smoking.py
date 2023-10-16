import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn


@class_case_log
class TestUpdateNoteInfo(unittest.TestCase):
    """更新便签主体接口level1"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['CreateNoteInfo']['Path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    startIndex = 0
    rows = 9999
    getHomeNotePath = f'/v3/notesvr/user/{user_id}/home/startindex/{startIndex}/rows/{rows}/notes'
    getHomeNoteUrl = host + getHomeNotePath

    def testCase01_major(self):
        """更新普通便签主体"""
        # 根据当前时间定义note_id，精确到毫秒
        info('STEP:新建便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id
        }
        # 请求上传便签信息主体接口，并获取接口返回结果
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)

        update_body = {
            'noteId': note_id,
            'star': 1
        }
        update_res = self.apiRe.note_post(self.url, self.user_id, self.sid, update_body)
        # 校验状态码
        self.assertEqual(200, update_res.status_code, msg='状态码有问题')
        # 校验数据源
        info('STEP:请求获取首页便签接口')
        res = self.apiRe.note_get(self.getHomeNoteUrl, self.sid)
        for i in res.json()['webNotes']:
            if i['noteId'] == note_id:
                self.assertEqual(1, i['star'], msg='star的值不等于1')  # 先描述期望值，再描述结果

