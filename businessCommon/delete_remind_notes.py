import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn


class DeleteRemindNotes(unittest.TestCase):
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
    getRemindNoteListPath = apiConfig['GetRemindNoteList']['Path']
    getRemindNoteListUrl = host + getRemindNoteListPath
    emptyRecycleNotePath = apiConfig['EmptyRecycle']['Path']
    emptyRecycleNoteUrl = host + emptyRecycleNotePath
    getRecycleNotePath = f'/v3/notesvr/user/{user_id}/invalid/startindex/{start_index}/rows/{rows}/notes'
    getRecycleNoteUrl = host + getRecycleNotePath

    def delete_remind_notes(self):
        info('正在清空首页便签数据')
        # 请求获取日历便签列表
        get_remind_note_body = {
            'remindStartTime': 1695652,
            'remindEndTime': int(time.time() * 1000),
            'startIndex': 0,
            'rows': 9999
        }
        res = self.apiRe.note_post(self.getRemindNoteListUrl, self.user_id, self.sid, get_remind_note_body)
        # 获取所有remind_note_Ids
        remind_note_ids = []
        for i in res.json()['webNotes']:
            remind_note_ids.append(i['noteId'])

        for i in range(len(remind_note_ids)):
            # 请求删除便签接口
            body = {
                'noteId': remind_note_ids[i]
            }
            delete_note_res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)

            # 校验状态码
            self.assertEqual(200, delete_note_res.status_code, msg='状态码异常')

        # 再次获取日历便签列表，检查是否清空
        res02 = self.apiRe.note_post(self.getRemindNoteListUrl, self.user_id, self.sid, get_remind_note_body)
        self.assertEqual(0, len(res02.json()['webNotes']), msg='日历便签还未清空')

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

        return info('日历便签数据已清空')
