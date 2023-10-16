import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn


class CreateNotes(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    host = envConfig['host']
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    createNoteInfoPath = apiConfig['CreateNoteInfo']['Path']
    createNoteInfoUrl = host + createNoteInfoPath
    createNotePath = apiConfig['CreateNote']['Path']
    createNoteUrl = host + createNotePath
    apiRe = ApiRe()

    def create_notes(self, n):
        note_ids = []
        info(f'正在新建{n}条便签..')
        for i in range(n):
            # 根据当前时间定义note_id，精确到毫秒
            note_id = str(int(time.time() * 1000))
            get_note_info_body = {
                'noteId': note_id
            }
            # 请求上传便签信息主体接口，并获取接口返回结果
            get_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid, get_note_info_body)
            # 校验状态码
            self.assertEqual(200, get_note_info_res.status_code, msg='状态码有问题')

            get_note_body = {
                'noteId': note_id,
                'title': 'test',
                'summary': 'test',
                'body': 'test',
                'localContentVersion': get_note_info_res.json()['infoVersion'],
                'BodyType': 0
            }
            get_note_res = self.apiRe.note_post(self.createNoteUrl, self.user_id, self.sid, get_note_body)
            # 校验状态码
            self.assertEqual(200, get_note_res.status_code, msg='状态码异常')

            # 记录新建的便签id
            note_ids.append(note_id)

        info(f'成功新建{n}条便签。')
        return note_ids

