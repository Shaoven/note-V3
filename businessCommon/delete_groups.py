import unittest
import requests
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn


class DeleteGroups(unittest.TestCase):
    envConfig = ReadYaml.env_yaml()
    apiConfig = ReadYaml.api_yaml('api.yml')
    path = apiConfig['DeleteGroup']['Path']
    host = envConfig['host']
    url = host + path
    apiRe = ApiRe()
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    getGroupListPath = apiConfig['GetGroupList']['Path']
    getGroupListUrl = host + getGroupListPath

    def delete_groups(self):
        info('STEP:请求获取分组列表接口,获取所有groupId')
        body = {}
        res = self.apiRe.note_post(self.getGroupListUrl, self.user_id, self.sid, body)
        group_ids = []
        for i in res.json()['noteGroups']:
            group_ids.append(i['groupId'])

        print(group_ids)
        print(res.json())

        info('STEP:请求删除分组接口，删除分组')
        for d in range(len(group_ids)):
            print(d)
            body = {
                'groupId': group_ids[d]
            }
            res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
            print(res.status_code)
            # 校验状态
            # self.assertEqual(200, res.status_code, msg='状态异常')

        # info('STEP:请求获取分组列表接口，校验是否真的删除成功')
        # body = {}
        # res = self.apiRe.note_post(self.getGroupListUrl, self.user_id, self.sid, body)
        # print(res.json())


de = DeleteGroups()
de.delete_groups()
