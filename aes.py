import base64
import hashlib

from Crypto.Cipher import AES as _AES
from cryptography.hazmat.primitives import padding

# 第一部分 为了保证AES秘钥的隐式处理使用base64先进行加密 ->此处可忽略
# BASE64_KEY = base64.b64encode("longge=666love!!".encode("utf-8")).decode()
# BASE64_IV = base64.b64encode("longge=888love!!".encode("utf-8")).decode()
# AES_SALT = base64.b64encode("longge=999love!!".encode("utf-8")).decode()


AES_KEY = base64.b64decode("bG9uZ2dlPTY2NmxvdmUhIQ==").decode()  # 请修改 一定是 16位的字符串
AES_IV = base64.b64decode("bG9uZ2dlPTg4OGxvdmUhIQ==").decode()
AES_SALT = base64.b64decode("bG9uZ2dlPTk5OWxvdmUhIQ==").decode()


class AESEnCrpTor:
    # base64.b64encode("密钥".encode("utf-8")).decode()
    """https: // tool.chacuo.net / cryptaes"""

    def __init__(self):
        self.IV = AES_IV.encode("utf-8")
        self.KEY = AES_KEY.encode("utf-8")
        self.SALT = AES_SALT.encode("utf-8")

    def pkcs7_padding(self, data, block_size=128):
        """
        密码必须满足8的倍数所以需要补位，PKCS7Padding用'\n'补位
        :param data:
        :param block_size:
        :return:
        """
        if not isinstance(data, bytes):
            data = data.encode('utf-8')
        padder = padding.PKCS7(block_size).padder()
        return padder.update(data) + padder.finalize()

    def generateKey(self):
        """
        key加盐
        :return:
        """
        return hashlib.pbkdf2_hmac(hash_name="sha1", password=self.KEY, salt=self.SALT, iterations=1,
                                   dklen=16)

    def aes_encrypt(self, password: str):
        """
        aes加密
        :param password:
        :return:
        """
        key = self.generateKey()
        padded_data = self.pkcs7_padding(password)
        cipher = _AES.new(key, _AES.MODE_CBC, self.IV)
        return base64.b64encode(cipher.encrypt(padded_data)).decode()

    def aes_decrypt(self, content: str):
        """
        aes解密
        :param content:
        :return:
        """
        key = self.generateKey()
        cipher = _AES.new(key, _AES.MODE_CBC, self.IV)
        content = base64.b64decode(content)
        return (cipher.decrypt(content).decode('utf-8')).replace('\n', '')


ace = AESEnCrpTor()

__all__ = ["ace"]

if __name__ == '__main__':
    enc_data = ace.aes_encrypt("123456")
    print("加密:>>>>>{}".format(enc_data))  # VKkb+3g8UolLl0AtTLi0Ig==
    dec_data = ace.aes_decrypt(enc_data)
    print("解码:>>>>>{}".format(dec_data))  # 123456