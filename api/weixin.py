# -*- coding: utf-8 -*-
"""
微信api接口实现
"""
from tornado import gen
from api.base import BaseApi

class WeixinApi(BaseApi):

    @gen.coroutine
    def custom_send(self, access_token, open_id, content):
        """
        微信客服接口
        :param access_token:
        :param open_id:
        :param content:
        :return:
        """
        api_custom_send = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%(access_token)s'.format(access_token=access_token)

        data = {
            "touser": open_id,
            "msgtype": "text",
            "text":
            {
                 "content": content
            }
        }
        custom_reply = yield self.async_http_post_ori(api_custom_send, data)

        raise gen.Return(custom_reply)

