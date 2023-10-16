import unittest
import requests
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn


class DeleteNotes(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['DeleteNote']['Path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    cookies = {'wps_sid': sid}
    apiRe = ApiRe()
    start_index = 0
    rows = 9999
    getHomeNoteListPath = f'/v3/notesvr/user/{user_id}/home/startindex/{start_index}/rows/{rows}/notes'
    getHomeNoteListUrl = host + getHomeNoteListPath
    emptyRecycleNotePath = apiConfig['EmptyRecycle']['Path']
    emptyRecycleNoteUrl = host + emptyRecycleNotePath
    getRecycleNotePath = f'/v3/notesvr/user/{user_id}/invalid/startindex/{start_index}/rows/{rows}/notes'
    getRecycleNoteUrl = host + getRecycleNotePath

    def delete_notes(self):
        info('正在清空首页便签数据')
        # 获取首页便签列表的url
        res = requests.get(url=self.getHomeNoteListUrl, cookies=self.cookies)
        # 获取首页便签列表中所有noteId
        note_ids = []
        for i in res.json()['webNotes']:
            note_ids.append(i['noteId'])

        for i in range(len(note_ids)):
            # 请求删除便签接口
            body = {
                'noteId': note_ids[i]
            }
            delete_note_res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)

            # 校验状态码
            self.assertEqual(200, delete_note_res.status_code, msg='状态码异常')

        # 再次获取首页数据，检查是否清空
        res02 = requests.get(url=self.getHomeNoteListUrl, cookies=self.cookies)
        self.assertEqual(0, len(res02.json()['webNotes']), msg='首页便签还未清空')

        # 清空回收站
        empty_recycle_body = {
            'noteIds': ['-1']
        }
        empty_recycle_res = self.apiRe.note_post(self.emptyRecycleNoteUrl, self.user_id, self.sid, empty_recycle_body)
        # 校验状态码
        self.assertEqual(200, empty_recycle_res.status_code, msg='状态异常')

        # 获取回收站数据，检查数据是否清空成功
        get_recycle_note_res = requests.get(url=self.getRecycleNoteUrl, cookies=self.cookies)
        self.assertEqual(0, len(get_recycle_note_res.json()['webNotes']), msg='回收站还存在数据')

        return info('首页便签数据已清空')
