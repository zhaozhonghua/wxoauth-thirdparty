# -*- coding: utf-8 -*-
"""
微信自动回复实现
"""
import json
import time
import logging

from handler.base import BaseHandler
from util.wx_util import sanitize, parse_msg, gen_timetoken, verification
from util.wx_encrypt import WXBizMsgCrypt
from tornado import gen

class WxThirdAutoReplyHandler(BaseHandler):

    @gen.coroutine
    def get(self, app_id):

        echostr = self.get_argument('echostr', '')

        if echostr and self._verification():
            # sanitize xss filter
            self.write(sanitize(echostr, ''))
        else:
            self.write("")

    @gen.coroutine
    def post(self, app_id):
        try:
            msg = self._get_msg()

            # 验证第三方平台
            if app_id and app_id == 'wx570bc396a51b8ff8':
                # ver 1
                if msg.get('MsgType') == 'event':
                    text = '{0}from_callback'.format(msg.get('Event'))
                    rep_info = \
                        """
                        <xml>
                        <ToUserName><![CDATA[%s]]></ToUserName>
                        <FromUserName><![CDATA[%s]]></FromUserName>
                        <CreateTime>%s</CreateTime>
                        <MsgType><![CDATA[text]]></MsgType>
                        <Content><![CDATA[%s]]></Content>
                        </xml>
                        """
                    to_xml = rep_info % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())), text)

                    #测试加密接口
                    encryp_test = WXBizMsgCrypt(self.settings.component_token,
                                                self.settings.component_encodingAESKey,
                                                self.settings.component_app_id)

                    ret, encrypt_xml = encryp_test.EncryptMsg(to_xml, self.get_argument('nonce'))

                    logging.debug("ret:{0}, {1}".format(ret, encrypt_xml))
                    self.write(encrypt_xml.encode('utf-8'))

                # ver 2
                if msg.get('MsgType') == 'text' and msg.get('Content') == 'TESTCOMPONENT_MSG_TYPE_TEXT':
                    text = '{0}_callback'.format(msg.get('Content'))
                    logging.debug(text)
                    rep_info = \
                        """
                        <xml>
                        <ToUserName><![CDATA[%s]]></ToUserName>
                        <FromUserName><![CDATA[%s]]></FromUserName>
                        <CreateTime>%s</CreateTime>
                        <MsgType><![CDATA[text]]></MsgType>
                        <Content><![CDATA[%s]]></Content>
                        </xml>
                        """
                    to_xml = rep_info % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())), text)

                    #测试加密接口
                    encryp_test = WXBizMsgCrypt(self.settings.component_token,
                                                self.settings.component_encodingAESKey,
                                                self.settings.component_app_id)

                    ret, encrypt_xml = encryp_test.EncryptMsg(to_xml, self.get_argument('nonce'))

                    logging.debug("ret:{0}, {1}".format(ret, encrypt_xml))
                    self.write(encrypt_xml.encode('utf-8'))

                # ver 3
                if msg.get('MsgType') == 'text' and 'QUERY_AUTH_CODE' in msg.get('Content'):

                    component_access_token = self.redis.get('component_access_token')

                    query_auth_code = msg.get('Content').split(':')[1]
                    # {
                    # "authorization_info": {
                    # "authorizer_appid": "wxf8b4f85f3a794e77",
                    # "authorizer_access_token": "QXjUqNqfYVH0yBE1iI_7vuN_9gQbpjfK7hYwJ3P7xOa88a89-Aga5x1NMYJyB8G2yKt1KCl0nPC3W9GJzw0Zzq_dBxc8pxIGUNi_bFes0qM",
                    # "expires_in": 7200,
                    # "authorizer_refresh_token": "dTo-YCXPL4llX-u1W1pPpnp8Hgm4wpJtlR6iV0doKdY"
                    # }
                    if component_access_token:

                        component_access_token = json.loads(component_access_token)

                        data = yield self.thirdparyOauthApi.get_api_query_auth(component_access_token.get('component_access_token'),
                                                                               self.settings.component_app_id,
                                                                               query_auth_code)

                        logging.debug(data)

                        text = '{query_auth_code}_from_api'.format(query_auth_code=query_auth_code)

                        res = yield self.weixinApi.custom_send(data.get('authorization_info').get('authorizer_access_token'),
                                                               msg['FromUserName'],
                                                               text)

                        logging.debug(res)

                        rep_info = \
                            """
                            <xml>
                            <ToUserName><![CDATA[%s]]></ToUserName>
                            <FromUserName><![CDATA[%s]]></FromUserName>
                            <CreateTime>%s</CreateTime>
                            <MsgType><![CDATA[text]]></MsgType>
                            <Content><![CDATA[%s]]></Content>
                            </xml>
                            """
                        to_xml = rep_info % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())), text)

                        #测试加密接口
                        encryp_test = WXBizMsgCrypt(self.settings.component_token,
                                                    self.settings.component_encodingAESKey,
                                                    self.settings.component_app_id)
                        ret, encrypt_xml = encryp_test.EncryptMsg(to_xml, self.get_argument('nonce'))

                        logging.debug("ret:{0}, {1}".format(ret, encrypt_xml))
                        self.write(encrypt_xml.encode('utf-8'))
                    else:
                        logging.debug("token is not exist")

        except Exception, e:
            logging.error(e)

    def check_xsrf_cookie(self):
        """
        禁用xsrf验证
        :return:
        """
        return True

    def _get_msg(self):
        """
        获取xml的dict信息
        :return:
        """
        from_xml  = self.request.body

        timestamp = self.get_argument('timestamp')
        msg_sign  = self.get_argument('msg_signature')
        nonce     = self.get_argument('nonce')

        try:
            decrypt_test = WXBizMsgCrypt(self.settings.component_token,
                                         self.settings.component_encodingAESKey,
                                         self.settings.component_app_id)

            ret, decryp_xml = decrypt_test.DecryptMsg(from_xml, msg_sign, timestamp, nonce)
        except Exception, e:
            logging.error(e)

        logging.debug("ret:{0}, {1}".format(ret, decryp_xml))
        from_xml = decryp_xml

        return parse_msg(from_xml)

    def _verification(self):
        """
        校验
        :param token:
        :return:
        """
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')

        # 存在redis中的用户token
        token = ''

        return verification(signature, timestamp, nonce, token)
