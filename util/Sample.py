#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# Author: jonyqin
# Created Time: Thu 11 Sep 2014 03:55:41 PM CST
# File Name: demo.py
# Description: WXBizMsgCrypt 使用demo文件
#########################################################################
from wx_encrypt import WXBizMsgCrypt

if __name__ == "__main__":
   """
   1.第三方回复加密消息给公众平台；
   2.第三方收到公众平台发送的消息，验证消息的安全性，并对消息进行解密。
   """
   # encodingAESKey = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFG"
   # to_xml = """ <xml><ToUserName><![CDATA[oia2TjjewbmiOUlr6X-1crbLOvLw]]></ToUserName><FromUserName><![CDATA[gh_7f083739789a]]></FromUserName><CreateTime>1407743423</CreateTime><MsgType>  <![CDATA[video]]></MsgType><Video><MediaId><![CDATA[eYJ1MbwPRJtOvIEabaxHs7TX2D-HV71s79GUxqdUkjm6Gs2Ed1KF3ulAOA9H1xG0]]></MediaId><Title><![CDATA[testCallBackReplyVideo]]></Title><Descript  ion><![CDATA[testCallBackReplyVideo]]></Description></Video></xml>"""
   # token = "spamtest"
   # nonce = "1320562132"
   # appid = "wx2c2769f8efd9abc2"
   # #测试加密接口
   # encryp_test = WXBizMsgCrypt(token,encodingAESKey,appid)
   # ret,encrypt_xml = encryp_test.EncryptMsg(to_xml,nonce)
   # print ret,encrypt_xml
   #
   #
   # #测试解密接口
   # timestamp = "1409735669"
   # msg_sign  = "5d197aaffba7e9b25a30732f161a50dee96bd5fa"
   #
   # from_xml = """<xml><ToUserName><![CDATA[gh_10f6c3c3ac5a]]></ToUserName><FromUserName><![CDATA[oyORnuP8q7ou2gfYjqLzSIWZf0rs]]></FromUserName><CreateTime>1409735668</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[abcdteT]]></Content><MsgId>6054768590064713728</MsgId><Encrypt><![CDATA[hyzAe4OzmOMbd6TvGdIOO6uBmdJoD0Fk53REIHvxYtJlE2B655HuD0m8KUePWB3+LrPXo87wzQ1QLvbeUgmBM4x6F8PGHQHFVAFmOD2LdJF9FrXpbUAh0B5GIItb52sn896wVsMSHGuPE328HnRGBcrS7C41IzDWyWNlZkyyXwon8T332jisa+h6tEDYsVticbSnyU8dKOIbgU6ux5VTjg3yt+WGzjlpKn6NPhRjpA912xMezR4kw6KWwMrCVKSVCZciVGCgavjIQ6X8tCOp3yZbGpy0VxpAe+77TszTfRd5RJSVO/HTnifJpXgCSUdUue1v6h0EIBYYI1BD1DlD+C0CR8e6OewpusjZ4uBl9FyJvnhvQl+q5rv1ixrcpCumEPo5MJSgM9ehVsNPfUM669WuMyVWQLCzpu9GhglF2PE=]]></Encrypt></xml>"""
   # decrypt_test = WXBizMsgCrypt(token,encodingAESKey,appid)
   # ret ,decryp_xml = decrypt_test.DecryptMsg(from_xml, msg_sign, timestamp, nonce)
   # print ret ,decryp_xml

   test_encodingAESKey = "YhwSCu0CGkfeaHaAE9XHXfxeX2P0r5skvlDEl1pVK2a"
   test_token = "c37f1cd03cb111e5a2be00163e004a1f"
   test_nonce = "649282517"
   test_timestamp = "1440678040"
   test_msg_sign  = "e4e868dbaa2dc3b33b34bf0766079d4aa2212ad7"
   test_appid = "wx96653e603761ba3e"
   test_xml= """<xml>
        <AppId><![CDATA[wx96653e603761ba3e]]></AppId>
        <Encrypt><![CDATA[5t48h2vPqg4OE4VnUTgQDXi2dYZRgjTHFFDJEQ6EtVgXnN3HiEgBPVAgOJ3HxgqIlZ9fVkKHNA/aTGx6+m/V9ji3bHEQB4VAJslmDk57+DTDm5agomuWRC/OUuxmqx+9cLxz58aUTKSX52gHmm+XlBkwOEy5+E42xHgqThxoadPtmSvxeEItPsK1xqB50Kp04TjPzrZe8GARk2Zg6YaHphzwqcKSFOGbh1O5U/8uvcoRzNriz/JrBC6RZPD1Lqy/Yzg+PDBU7MlbN/slOhxc73fSQ8CoPrbSROwh2DhckbBp5wOhXTNitJL1JAvla7ohmD04SG5gFAy9Lot760PtbY6crpdd6jRzUYaVfcLrjDBxUUYnjLBqk5UF34JAWbbl5GU3WH59m3Dt6kJP2A7Tv0VAOHqbEo28M1aYwAaYgMvLV49sikGJ3eBrIuWfmOEHVP26yeDEU2UOlmV3guIj3Q==]]></Encrypt>
    </xml>"""

   decrypt_test = WXBizMsgCrypt(test_token, test_encodingAESKey, test_appid)
   ret ,decryp_xml = decrypt_test.DecryptMsg(test_xml, test_msg_sign, test_timestamp, test_nonce)
   print ret ,decryp_xml