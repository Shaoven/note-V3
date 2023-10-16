import unittest


class CheckTools(unittest.TestCase):
    def check_output(self, expect, actual):
        """
        :param expect: {'responseTime': '1', 'contentVersion': int}
        :param actual: res.json()
        校验点：
        1.必填项是否存在
        2.返回的字段类型是否一致
        3.没有多余的字段
        4.值是否相等
        :return: None
        """
        # 校验字段长度是否一致
        self.assertEqual(len(expect.keys()), len(actual.keys()), msg='字段长度不匹配')

        for k, v in expect.items():
            # 遇到嵌套的字典，进行递归
            if type(v) == dict:
                self.check_output(expect[k], actual[k])
            elif type(v) == list:
                for item in range(len(expect[k])):
                    if type(expect[k][item]) == dict:
                        self.check_output(expect[k][item], actual[k][item])
                    else:
                        if type(expect[k][item]) == type:
                            self.assertEqual(expect[k][item], type(actual[k][item]), msg=f'{k} 字段类型不一致')
                        else:
                            self.assertEqual(type(expect[k][item]), type(actual[k][item]), msg=f'{k} 字段类型不一致')
                            self.assertEqual(expect[k][item], actual[k][item], msg=f'{k} 字段值不一致')
            else:
                self.assertIn(k, actual.keys(), msg=f'{k} 字段不存在')
                if type(v) == type:
                    self.assertEqual(v, type(actual[k]), msg=f'{k} 字段类型不一致')
                else:
                    self.assertEqual(type(v), type(actual[k]), msg=f'{k} 字段类型不一致')
                    self.assertEqual(v, actual[k], msg=f'{k} 字段值不一致')
