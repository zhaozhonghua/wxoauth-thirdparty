# -*- coding: utf-8 -*-
"""
微信第三方平台授权
"""
from handler.base import BaseHandler
import tornado.httpclient
import xml.etree.ElementTree as ET

import time
import json
import logging

from util.wx_encrypt import WXBizMsgCrypt
from tornado import gen
from urllib import quote

class WxThirdPartyOauthHandler(BaseHandler):

    @gen.coroutine
    def prepare(self):

        super(WxThirdPartyOauthHandler, self).prepare()

        self.http_client = tornado.httpclient.AsyncHTTPClient()

    @gen.coroutine
    def get(self):
        try:
            # 获取我们第三方平台的component_token
            d_component_access_token = yield self._get_api_component_token()

            if d_component_access_token:
                component_access_token = d_component_access_token.get('component_access_token')

                pre_auth_code = yield self.thirdparyOauthApi.get_api_create_preauthcode(component_access_token,
                                                                                            self.settings.component_app_id)

                if 'errcode' not in pre_auth_code:

                    login_page = self._get_componentloginpage(self.settings.component_app_id,
                                                               pre_auth_code.get('pre_auth_code'))

                    self.redirect(login_page)
                else:
                    self.write(pre_auth_code)
            else:
                self.write(u"component_access_token is not exist")

        except Exception, e:
            logging.error(e)
            self.write(u"oauth failed")

    def _get_componentloginpage(self, component_app_id, pre_auth_code):
        """
        组合微信授权登陆页面url
        """

        redirect_uri = quote('http://{host}/oauth?m=callback'.format(host=self.request.host))

        login_page = 'https://mp.weixin.qq.com/cgi-bin/componentloginpage?' \
                             'component_appid={component_appid}&' \
                             'pre_auth_code={pre_auth_code}&' \
                             'redirect_uri={redirect_uri}'.format(component_appid=component_app_id,
                                                                  pre_auth_code=pre_auth_code,
                                                                  redirect_uri=redirect_uri)
        return login_page

    @gen.coroutine
    def _get_api_component_token(self):
        """
        获取我们第三方平台的component_token
        """
        # 先从redis中查看component_access_token
        component_token = self.redis.get('component_access_token')
        logging.debug("get component_access_token from redis: {0}".format(component_token))

        if component_token:
            component_token = json.loads(component_token)

        # component_token不存在或已过期，获取我们第三方平台的component_token
        if not component_token or (int(time.time()) - int(component_token.get('create_time'))) > component_token.get('expires_in')/2:

            # 获取我们第三方平台的component_verify_ticket
            component_verify_ticket = self.redis.get("ComponentVerifyTicket")
            if not component_verify_ticket:
                logging.error("get component_verify_ticket failed from redis, component_token : {0}".format(component_token))
                raise gen.Return("")

            logging.debug("component_verify_ticket : {0}".format(component_verify_ticket))

            component_token = self.thirdparyOauthApi.get_api_component_token(self.settings.component_app_id,
                                                                                 self.settings.component_app_secret,
                                                                                 str(json.loads(component_verify_ticket).get('ComponentVerifyTicket')))

            if 'errcode' not in component_token:
                component_token.update({'create_time': int(time.time())})
                self.redis.set("component_access_token", json.dumps(component_token), 7200)
            else:
                logging.error("get component_token failed, {0}".format(component_token))

        raise gen.Return(component_token)

class WxThirdPartyCallbackHandler(BaseHandler):
    """
    微信第三方授权回调Handler
    """
    @gen.coroutine
    def prepare(self):

        super(WxThirdPartyCallbackHandler, self).prepare()

        self.http_client = tornado.httpclient.AsyncHTTPClient()

    @gen.coroutine
    def get(self):
        try:
            component_access_token = self.redis.get("component_access_token")

            if component_access_token:
                component_access_token = json.loads(component_access_token)

            authorization_code = self.get_argument('auth_code')

            # 取得预授权码
            wechat_auth = yield self.thirdparyOauthApi.get_api_query_auth(component_access_token, authorization_code, self.settings.component_app_id)

            wechat_auth = wechat_auth.get('authorization_info')

            # 取得微信号授权后返回的信息
            wechat_info = yield self.thirdparyOauthApi.get_api_get_authorizer_info(component_access_token,
                                                                                       self.settings.component_app_id,
                                                                                       wechat_auth.get('authorizer_appid'))

            wechat_info['create_time'] = int(time.time()) - 3600

            # 保存至redis，redis的key按照业务需求自己设计吧
            self.redis.set(wechat_info['AuthorizerAppid'], wechat_info)

            # 授权成功的公众号信息
            self.write(wechat_info)

        except Exception, e:
            logging.error(e)
            self.write(u"授权失败")

class WxThirdPartyOauthEventHandler(BaseHandler):
    """
    接收推送的响应事件
    """
    @gen.coroutine
    def post(self):

        from_xml = self.request.body

        timestamp = self.get_argument('timestamp')
        msg_sign  = self.get_argument('msg_signature')
        nonce = self.get_argument('nonce')

        try:
            decrypt_test = WXBizMsgCrypt(self.settings.component_token,
                                         self.settings.component_encodingAESKey,
                                         self.settings.component_app_id)
            ret, decryp_xml = decrypt_test.DecryptMsg(from_xml, msg_sign, timestamp, nonce)
        except Exception, e:
            logging.error(e)

        logging.debug("{0}, {1}".format(ret, decryp_xml))

        try:
            data = self._parse_msg(decryp_xml)
        except Exception, e:
            logging.error(e)

        logging.debug(data)

        # 监听ComponentVerifyTicket事件，获取Ticket
        if data.get('ComponentVerifyTicket'):
            self.redis.set("ComponentVerifyTicket", json.dumps(data), timeout=600)
            self.write(u'success')

        # {'InfoType': 'unauthorized', 'CreateTime': '1440691639', 'AuthorizerAppid': 'wx570bc396a51b8ff8', 'AppId': 'wx98aa120730a78275'}
        if data.get('InfoType') == 'unauthorized':
            # 解除授权时刨除测试号
            if data.get('AuthorizerAppid') != 'wx570bc396a51b8ff8':
                # 从redis中清除
                self.redis.delete(data.get('AuthorizerAppid'))

            self.write(u'unauthorized')

    def _parse_msg(self, rawmsgstr):
        """
        xml转换为json
        :param rawmsgstr:
        :return:
        """
        root = ET.fromstring(rawmsgstr)
        msg = {}
        for child in root:
            msg[child.tag] = child.text
        return msg

    def check_xsrf_cookie(self):
        """
        关闭xsrf验证
        :return:
        """
        return True