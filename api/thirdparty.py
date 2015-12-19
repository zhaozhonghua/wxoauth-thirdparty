# -*- coding: utf-8 -*-
"""
第三方授权api接口实现
"""
from tornado import gen
from api.base import BaseApi

class ThirdparyOauthApi(BaseApi):

    @gen.coroutine
    def get_api_component_token(self, app_id, app_secret, component_verify_ticket):
        """
        获取我们第三方平台的component_token
        """
        api_component_token = 'https://api.weixin.qq.com/cgi-bin/component/api_component_token'
        data = {
                    "component_appid": app_id,
                    "component_appsecret": app_secret,
                    "component_verify_ticket": component_verify_ticket
                }

        component_token = yield self.async_http_post_ori(api_component_token, data)

        raise gen.Return(component_token)

    @gen.coroutine
    def get_api_create_preauthcode(self, component_access_token, component_appid):
        """
        获取预授权码
        :param component_access_token:
        :param component_appid:
        :return:
        """
        api_create_preauthcode = 'https://api.weixin.qq.com/cgi-bin/component/api_create_preauthcode?component_access_token={component_access_token}'.format(component_access_token=component_access_token)
        data = {'component_appid': component_appid}

        preauthcode = yield self.async_http_post_ori(api_create_preauthcode, data)

        raise gen.Return(preauthcode)

    @gen.coroutine
    def get_api_query_auth(self, component_access_token, authorization_code, component_appid):
        """
        取得预授权码
        :param component_access_token:
        :param authorization_code:
        :return:
        """

        api_query_auth = 'https://api.weixin.qq.com/cgi-bin/component/api_query_auth?component_access_token={component_access_token}'.format(component_access_token=component_access_token.get('component_access_token'))

        data = {'component_appid': component_appid, 'authorization_code': authorization_code}

        query_auth = yield self.async_http_post_ori(api_query_auth, data)

        raise gen.Return(query_auth)

    @gen.coroutine
    def get_api_get_authorizer_info(self, component_access_token, component_appid, authorizer_appid):
        """
        获取授权公众号信息
        :param component_access_token:
        :param component_appid:
        :param authorizer_appid:
        :return:
        """
        api_get_authorizer_info = 'https://api.weixin.qq.com/cgi-bin/component/api_get_authorizer_info?component_access_token={component_access_token}'.format(component_access_token=component_access_token.get('component_access_token'))
        data = {"component_appid":component_appid, "authorizer_appid": authorizer_appid}

        authorizer_info = self.async_http_post_ori(api_get_authorizer_info, data)

        raise gen.Return(authorizer_info)

    @gen.coroutine
    def get_jsticket(self, access_token):
        """
        获取jsticket
        :param access_token:
        :param signature:
        :return:
        """
        jsticket_api = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi" % access_token

        jsticket = yield self.async_http_get_ori(jsticket_api)

        raise gen.Return(jsticket.get('ticket', ''))

