import unittest
import requests
import time
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn


class CreateGroups(unittest.TestCase):
    envConfig = ReadYaml.env_yaml()
    apiConfig = ReadYaml.api_yaml('api.yml')
    path = apiConfig['CreateGroup']['Path']
    host = envConfig['host']
    url = host + path
    apiRe = ApiRe()
    sid = envConfig['sid']
    user_id = envConfig['user_id']

    def create_group(self, n):
        group_ids = []
        info(f'正在新建{n}个分组..')
        for i in range(n):
            # 根据当前时间定义note_id，精确到毫秒
            group_id = str(int(time.time() * 1000)) + '_test_groupId'
            group_name = str(int(time.time() * 1000)) + '_test_groupName'
            body = {
                'groupId': group_id,
                'groupName': group_name,
            }
            res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
            # 校验状态码
            self.assertEqual(200, res.status_code, msg='状态码异常')

            # 记录新建的便签id
            group_ids.append(group_id)

        info(f'成功新增了{n}个分组。')
        return group_ids
