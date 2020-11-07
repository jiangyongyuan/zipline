#!/usr/bin/env python
#@Time:2020-10-27 16:27
#@Author:wanc
#@File:.py
#@software:PyCharm

import base64
import ctypes
import json
import os

import Crypto

from Crypto.Cipher import PKCS1_v1_5
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA


class WxWork:
    CORP_ID = 'wx4e87264ba9cc0cf1'
    PRI_KEY = 'MIICWwIBAAKBgQDYhwh1Vggcq1W41oLifAPGutzkH2Tc8yFZDUGqMzFh4n4/l5xs6ol0vb/IQbWYTlbWhMj8RvYEscz/F7s6P9c+/B0IGEA5zHwJ6Sxo/Ez/AsNPtKBKHMB4ESJf1Tr93KPfzEZQ3mW+Mzr5fxbN7ousha27hht8hvu5r4kklv0WYQIDAQABAn9xtpeGHDPwp00FRsumo30Vp4+un4uVJvaoAmQFcG8cN7k3Bgrh240FXSF16gxhSLjKhzbib3uEc/WSOq/aZjRan1kWAlhs1vtrmjD1Mnaf2ot333Wd49LUnaYGVOZm8KvOuEbUIVSNh7lbE7UwXGfgBXHO0TnlK+/04O1sMk0hAkEA76tt4uzS5hk18W6buqdTAqYEsF060jZ3u7kvEzhvaf2NSgmSg0Pe4E+c9YH3dFArx0fRai5cP657u+c4M/YmMQJBAOdH7wEfICH/9zbU45q9KAMa+c9l+PdsZpr4aHtR4neTQcxY7XNwxgH4sETzNFpstogJOSyglcbYPKySkHBPdzECQQC5kVtAw6s7m7OHnuOW7u039MFWqKjdkGy+fdC0KhMh1r7p32WAmzFbLmlSMfIeLeDnqHS9qO2mJPwK7ik3GlRRAkBS5YOTAVcBGL/BFXknA1mOE2MqpUAhXuc/8H1yhh0IAu34kn85e1hdaIe1jv5a0tBx3exyRHSquuK0cCv5NWJhAkEAlccWCiJ7ASh9ieKwddELwVOZ4/K9ntCPBxqRHReopTld4ot2B1lpCQHVr2/u9ubRDN9vAuU0bJZwVU6N60TDsA=='
    CHAT_SECRET = 'xC8hUZnihLsxXJ-vQ3Et82X5fdDLMASGhTEpnq1XLSk'

    @classmethod
    def sync_msg(cls):
        dll = ctypes.cdll.LoadLibrary(os.getcwd() + "/libWeWorkFinanceSdk_C.so")  # 真实libWeWorkFinanceSdk_C位置
        new_sdk = dll.NewSdk()
        result = dll.Init(new_sdk, cls.CORP_ID.encode(), cls.CHAT_SECRET.encode())
        if result != 0:
            return
        private_key = RSA.import_key(cls.PRI_KEY)
        cipher = Crypto.Signature.PKCS1_v1_5.new(private_key)
        seq = 0
        while True:
            s = dll.NewSlice()
            dll.GetChatData(new_sdk, seq, 1000, '', '', 5, ctypes.c_long(s))
            data = dll.GetContentFromSlice(s)
            data = ctypes.string_at(data, -1).decode("utf-8")
            dll.FreeSlice(s)
            data = json.loads(data).get('chatdata')
            if not data:
                break
            seq = data[-1].get('seq')
            for msg in data:
                encrypt_key = cipher.decrypt(base64.b64decode(msg.get('encrypt_random_key')), "ERROR")
                ss = dll.NewSlice()
                dll.DecryptData(encrypt_key, msg.get('encrypt_chat_msg').encode(), ctypes.c_long(ss))
                result = dll.GetContentFromSlice(ss)
                result = ctypes.string_at(result, -1).decode("utf-8")
                result = json.loads(result)
                dll.FreeSlice(ss)
                print(result)
        dll.DestroySdk(new_sdk)


if __name__ == '__main__':
    WxWork.sync_msg()