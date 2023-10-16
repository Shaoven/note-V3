import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.ymlOperation import ReadYaml
from businessCommon.apiRe import ApiRe
from common.caseLogMethod import class_case_log, info, error, warn


@class_case_log
class TestGetGroupNotes(unittest.TestCase):
    """获取分组便签接口 接口handle"""
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['GetGroupNote']['Path']
    mustKey = apiConfig['GetGroupNote']['must_key']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid']
    sidB = envConfig['sidB']
    user_id = envConfig['user_id']
    userB_id = envConfig['userB_id']
    apiRe = ApiRe()
    createGroupPath = apiConfig['CreateGroup']['Path']
    createGroupUrl = host + createGroupPath
    createNoteInfoPath = apiConfig['CreateNoteInfo']['Path']
    createNoteInfoUrl = host + createNoteInfoPath
    createNotePath = apiConfig['CreateNote']['Path']
    createNoteUrl = host + createNotePath
    special = apiConfig['GetGroupNote']['special']
    deleteGroupPath = apiConfig['DeleteGroup']['Path']
    deleteGroupUrl = host + deleteGroupPath
    deleteNotePath = apiConfig['DeleteNote']['Path']
    deleteNoteUrl = host + deleteNotePath
    recoverRecycleNotePath = f'/v3/notesvr/user/{user_id}/notes'
    recoverRecycleNoteUrl = host + recoverRecycleNotePath
    emptyRecycleNotePath = apiConfig['EmptyRecycle']['Path']
    emptyRecycleNoteUrl = host + emptyRecycleNotePath

    def testCase01_rows_number_limit(self):
        """数值限制 用户分组A下有2条便签，startIndex=0，rows=1"""
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        # 校验状态码
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        for i in range(2):
            info('STEP:新建分组便签主体')
            note_id = str(int(time.time() * 1000)) + '_test_noteId'
            create_note_info_body = {
                'noteId': note_id,
                'groupId': group_id
            }
            create_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid,
                                                        create_note_info_body)
            # 校验状态码
            self.assertEqual(200, create_note_info_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

            info('STEP:新建分组便签内容')
            create_note_body = {
                'noteId': note_id,
                'title': 'test',
                'summary': 'test',
                'body': 'test',
                'localContentVersion': create_note_info_res.json()['infoVersion'],
                'BodyType': 0
            }
            create_note_res = self.apiRe.note_post(self.createNoteUrl, self.user_id, self.sid, create_note_body)
            # 校验状态码
            self.assertEqual(200, create_note_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:请求获取分组便签接口')
        body = {
            'groupId': group_id,
            'startIndex': 0,
            'rows': 1
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
        # 校验数据源，是否只返回一条分组便签数据
        self.assertEqual(1, len(res.json()['webNotes']), msg='该分组下便签数量不等于1')

    def testCase02_rows_number_limit(self):
        """数值限制 用户分组A下有2条便签，startIndex=0，rows=3"""
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        # 校验状态码
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        for i in range(2):
            info('STEP:新建分组便签主体')
            note_id = str(int(time.time() * 1000)) + '_test_noteId'
            create_note_info_body = {
                'noteId': note_id,
                'groupId': group_id
            }
            create_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid,
                                                        create_note_info_body)
            # 校验状态码
            self.assertEqual(200, create_note_info_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

            info('STEP:新建分组便签内容')
            create_note_body = {
                'noteId': note_id,
                'title': 'test',
                'summary': 'test',
                'body': 'test',
                'localContentVersion': create_note_info_res.json()['infoVersion'],
                'BodyType': 0
            }
            create_note_res = self.apiRe.note_post(self.createNoteUrl, self.user_id, self.sid, create_note_body)
            # 校验状态码
            self.assertEqual(200, create_note_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:请求获取分组便签接口')
        body = {
            'groupId': group_id,
            'startIndex': 0,
            'rows': 3
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
        # 校验数据源
        self.assertEqual(2, len(res.json()['webNotes']), msg='该分组下便签数量不等于2')

    def testCase03_rows_number_limit(self):
        """数值限制 用户分组A下有2条便签，startIndex=0，rows=0"""
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        # 校验状态码
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        for i in range(2):
            info('STEP:新建分组便签主体')
            note_id = str(int(time.time() * 1000)) + '_test_noteId'
            create_note_info_body = {
                'noteId': note_id,
                'groupId': group_id
            }
            create_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid,
                                                        create_note_info_body)
            # 校验状态码
            self.assertEqual(200, create_note_info_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

            info('STEP:新建分组便签内容')
            create_note_body = {
                'noteId': note_id,
                'title': 'test',
                'summary': 'test',
                'body': 'test',
                'localContentVersion': create_note_info_res.json()['infoVersion'],
                'BodyType': 0
            }
            create_note_res = self.apiRe.note_post(self.createNoteUrl, self.user_id, self.sid, create_note_body)
            # 校验状态码
            self.assertEqual(200, create_note_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:请求获取分组便签接口')
        body = {
            'groupId': group_id,
            'startIndex': 0,
            'rows': 0
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
        # 校验数据源
        self.assertEqual(0, len(res.json()['webNotes']), msg='该分组下便签数量不等于0')

    def testCase04_starIndex_number_limit(self):
        """数值限制 用户分组A下有1条便签，startIndex=2，rows=1"""
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        # 校验状态码
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:新建分组便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        create_note_info_body = {
            'noteId': note_id,
            'groupId': group_id
        }
        create_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid,
                                                    create_note_info_body)
        # 校验状态码
        self.assertEqual(200, create_note_info_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:新建分组便签内容')
        create_note_body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': create_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        create_note_res = self.apiRe.note_post(self.createNoteUrl, self.user_id, self.sid, create_note_body)
        # 校验状态码
        self.assertEqual(200, create_note_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:请求获取分组便签接口')
        body = {
            'groupId': group_id,
            'startIndex': 2,
            'rows': 1
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
        # 校验数据源
        self.assertEqual(0, len(res.json()['webNotes']), msg='该分组下便签数量不等于0')

    def testCase05_no_send_rows(self):
        """数值限制 不传rows参数时，rows默认为50"""
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        # 校验状态码
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        for i in range(51):
            info('STEP:新建分组便签主体')
            note_id = str(int(time.time() * 1000)) + '_test_noteId'
            create_note_info_body = {
                'noteId': note_id,
                'groupId': group_id
            }
            create_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid,
                                                        create_note_info_body)
            # 校验状态码
            self.assertEqual(200, create_note_info_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

            info('STEP:新建分组便签内容')
            create_note_body = {
                'noteId': note_id,
                'title': 'test',
                'summary': 'test',
                'body': 'test',
                'localContentVersion': create_note_info_res.json()['infoVersion'],
                'BodyType': 0
            }
            create_note_res = self.apiRe.note_post(self.createNoteUrl, self.user_id, self.sid, create_note_body)
            # 校验状态码
            self.assertEqual(200, create_note_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:请求获取分组便签接口')
        body = {
            'groupId': group_id,
            'startIndex': 0,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
        # 校验数据源
        self.assertEqual(50, len(res.json()['webNotes']), msg='该分组下便签数量不等于50')

    def testCase06_no_send_startIndex(self):
        """数值限制 不传startIndex参数时，startIndex默认为0"""
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        # 校验状态码
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        for i in range(2):
            info('STEP:新建分组便签主体')
            note_id = str(int(time.time() * 1000)) + '_test_noteId'
            create_note_info_body = {
                'noteId': note_id,
                'groupId': group_id
            }
            create_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid,
                                                        create_note_info_body)
            # 校验状态码
            self.assertEqual(200, create_note_info_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

            info('STEP:新建分组便签内容')
            create_note_body = {
                'noteId': note_id,
                'title': 'test',
                'summary': 'test',
                'body': 'test',
                'localContentVersion': create_note_info_res.json()['infoVersion'],
                'BodyType': 0
            }
            create_note_res = self.apiRe.note_post(self.createNoteUrl, self.user_id, self.sid, create_note_body)
            # 校验状态码
            self.assertEqual(200, create_note_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:请求获取分组便签接口')
        body = {
            'groupId': group_id,
            'rows': 2,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
        # 校验数据源
        self.assertEqual(2, len(res.json()['webNotes']), msg='该分组下便签数量不等于2')

    def testCase07_groupId_not_exist(self):
        """数值限制 groupId的值不存在"""
        info('前置步骤：清空所有分组包括分组下有便签数据的分组')
        info('STEP:请求获取分组列表接口,获取所有groupId')
        get_group_body = {}
        res = self.apiRe.note_post(self.getGroupListUrl, self.user_id, self.sid, get_group_body)
        group_ids = []
        for i in res.json()['noteGroups']:
            group_ids.append(i['groupId'])

        info('STEP:请求删除分组接口，删除分组')
        for d in range(len(group_ids)):
            delete_body = {
                'groupId': group_ids[d]
            }
            res = self.apiRe.note_post(self.url, self.user_id, self.sid, delete_body)

        info('STEP:请求获取分组便签接口')
        body = {
            'groupId': 'group_id',
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase08_state_limit(self):
        """状态限制 回收站中的有1条便签属于分组A"""
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        # 校验状态码
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:新建一条分组便签')
        info('STEP:新建分组便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        create_note_info_body = {
            'noteId': note_id,
            'groupId': group_id
        }
        create_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid,
                                                    create_note_info_body)
        # 校验状态码
        self.assertEqual(200, create_note_info_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:新建分组便签内容')
        create_note_body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': create_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        create_note_res = self.apiRe.note_post(self.createNoteUrl, self.user_id, self.sid, create_note_body)
        # 校验状态码
        self.assertEqual(200, create_note_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:再次新建一条分组便签并删除')
        info('STEP:新建分组便签主体')
        note_id2 = str(int(time.time() * 1000)) + '_test_noteId'
        create_note_info_body = {
            'noteId': note_id2,
            'groupId': group_id
        }
        create_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid,
                                                    create_note_info_body)
        # 校验状态码
        self.assertEqual(200, create_note_info_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:新建分组便签内容')
        create_note_body = {
            'noteId': note_id2,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': create_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        create_note_res = self.apiRe.note_post(self.createNoteUrl, self.user_id, self.sid, create_note_body)
        # 校验状态码
        self.assertEqual(200, create_note_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('删除这条分组便签')
        info('STEP:删除便签')
        delete_note_body = {
            'noteId': note_id2
        }
        delete_note_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_note_body)
        # 校验状态码
        self.assertEqual(200, delete_note_res.status_code, msg='状态码异常')

        info('STEP:请求获取分组便签接口')
        body = {
            'groupId': group_id,
            'rows': 2,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
        # 校验数据源
        self.assertEqual(1, len(res.json()['webNotes']), msg='该分组下便签数量不等于1')

    def testCase09_state_limit(self):
        """状态限制 回收站中的恢复1条分组A下的便签"""
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        # 校验状态码
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('新建一条分组便签')
        info('STEP:新建分组便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        create_note_info_body = {
            'noteId': note_id,
            'groupId': group_id
        }
        create_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid,
                                                    create_note_info_body)
        # 校验状态码
        self.assertEqual(200, create_note_info_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:新建分组便签内容')
        create_note_body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': create_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        create_note_res = self.apiRe.note_post(self.createNoteUrl, self.user_id, self.sid, create_note_body)
        # 校验状态码
        self.assertEqual(200, create_note_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('删除这条分组便签')
        info('STEP:删除便签')
        delete_note_body = {
            'noteId': note_id
        }
        delete_note_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_note_body)
        # 校验状态码
        self.assertEqual(200, delete_note_res.status_code, msg='状态码异常')

        info('恢复这条分组便签')
        info('STEP:请求恢复便签接口')
        recover_recycle_note_body = {
            'userId': self.user_id,
            'noteIds': [note_id]
        }
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid}'
        }
        recover_recycle_note_res = requests.patch(url=self.recoverRecycleNoteUrl, headers=headers,
                                                  json=recover_recycle_note_body)
        # 校验状态码
        self.assertEqual(200, recover_recycle_note_res.status_code, msg='状态码异常')

        info('STEP:请求获取分组便签接口')
        body = {
            'groupId': group_id,
            'rows': 2,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
        # 校验数据源
        self.assertEqual(1, len(res.json()['webNotes']), msg='该分组下便签数量不等于1')

    def testCase10_state_limit(self):
        """状态限制 回收站中的清空1条分组A下的便签"""
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        # 校验状态码
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('新建一条分组便签')
        info('STEP:新建分组便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        create_note_info_body = {
            'noteId': note_id,
            'groupId': group_id
        }
        create_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid,
                                                    create_note_info_body)
        # 校验状态码
        self.assertEqual(200, create_note_info_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:新建分组便签内容')
        create_note_body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': create_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        create_note_res = self.apiRe.note_post(self.createNoteUrl, self.user_id, self.sid, create_note_body)
        # 校验状态码
        self.assertEqual(200, create_note_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('删除这条分组便签')
        info('STEP:删除便签')
        delete_note_body = {
            'noteId': note_id
        }
        delete_note_res = self.apiRe.note_post(self.deleteNoteUrl, self.user_id, self.sid, delete_note_body)
        # 校验状态码
        self.assertEqual(200, delete_note_res.status_code, msg='状态码异常')

        info('清空这条分组便签')
        info('STEP:请求清空便签接口')
        empty_recycle_note_body = {
            'noteIds': [note_id]
        }
        empty_recycle_note_res = self.apiRe.note_post(self.emptyRecycleNoteUrl, self.user_id, self.sid,
                                                      empty_recycle_note_body)
        # 校验状态码
        self.assertEqual(200, empty_recycle_note_res.status_code, msg='状态码异常')

        info('STEP:请求获取分组便签接口')
        body = {
            'groupId': group_id,
            'rows': 2,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
        # 校验数据源
        self.assertEqual(0, len(res.json()['webNotes']), msg='该分组下便签数量不等于0')

    def testCase11_userA_get_userB_group_note(self):
        """操作对象 用户A获取用户B的分组便签数据"""
        info('用户B新建一条分组便签')
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.userB_id, self.sidB, create_group_body)
        # 校验状态码
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('新建一条分组便签')
        info('STEP:新建分组便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        create_note_info_body = {
            'noteId': note_id,
            'groupId': group_id
        }
        create_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.userB_id, self.sidB,
                                                    create_note_info_body)
        # 校验状态码
        self.assertEqual(200, create_note_info_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:新建分组便签内容')
        create_note_body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': create_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        create_note_res = self.apiRe.note_post(self.createNoteUrl, self.userB_id, self.sidB, create_note_body)
        # 校验状态码
        self.assertEqual(200, create_note_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:请求获取分组便签接口')
        body = {
            'groupId': group_id,
            'rows': 2,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(403, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

    def testCase12_userA_has_two_group(self):
        """操作对象 同一用户的分组A和分组B都存在1条便签数据，请求分组A下的便签数据"""
        info('新建一条分组便签')
        info('STEP:新建分组')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body = {
            'groupId': group_id,
            'groupName': group_name,
        }
        create_group_res = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body)
        # 校验状态码
        self.assertEqual(200, create_group_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:新建分组便签主体')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        create_note_info_body = {
            'noteId': note_id,
            'groupId': group_id
        }
        create_note_info_res = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid,
                                                    create_note_info_body)
        # 校验状态码
        self.assertEqual(200, create_note_info_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:新建分组便签内容')
        create_note_body = {
            'noteId': note_id,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': create_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        create_note_res = self.apiRe.note_post(self.createNoteUrl, self.user_id, self.sid, create_note_body)
        # 校验状态码
        self.assertEqual(200, create_note_res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('再次新建一条分组便签')
        info('STEP:新建分组')
        group_id2 = str(int(time.time() * 1000)) + '_test_groupId'
        group_name2 = str(int(time.time() * 1000)) + '_test_groupName'
        create_group_body2 = {
            'groupId': group_id2,
            'groupName': group_name2,
        }
        create_group_res2 = self.apiRe.note_post(self.createGroupUrl, self.user_id, self.sid, create_group_body2)
        # 校验状态码
        self.assertEqual(200, create_group_res2.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:新建分组便签主体')
        note_id2 = str(int(time.time() * 1000)) + '_test_noteId'
        create_note_info_body2 = {
            'noteId': note_id2,
            'groupId': group_id2
        }
        create_note_info_res2 = self.apiRe.note_post(self.createNoteInfoUrl, self.user_id, self.sid,
                                                     create_note_info_body2)
        # 校验状态码
        self.assertEqual(200, create_note_info_res2.status_code, msg='状态码异常')  # 先描述期望值，再描述结果

        info('STEP:新建分组便签内容')
        create_note_body2 = {
            'noteId': note_id2,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': create_note_info_res.json()['infoVersion'],
            'BodyType': 0
        }
        create_note_res2 = self.apiRe.note_post(self.createNoteUrl, self.user_id, self.sid, create_note_body2)
        # 校验状态码
        self.assertEqual(200, create_note_res2.status_code, msg='状态码异常')

        info('STEP:请求获取分组便签接口')
        body = {
            'groupId': group_id,
            'rows': 2,
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # 校验状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 先描述期望值，再描述结果
        # 校验数据源
        note_ids = []
        for i in res.json()['webNotes']:
            note_ids.append(i['noteId'])
        self.assertIn(note_id, note_ids, msg='便签不在这个分组里面')
        self.assertNotIn(note_id2, note_ids, msg='便签在这个分组里面')
