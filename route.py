# -*- coding: utf-8 -*-
"""
全局路由
"""
from handler.base import IndexHandler
from handler.weixin import WxThirdAutoReplyHandler
from handler.thirdparty import WxThirdPartyOauthHandler
from handler.thirdparty import WxThirdPartyCallbackHandler
from handler.thirdparty import WxThirdPartyOauthEventHandler

routes = [
             # 微信端自动回复
             (r"/wxtp/?([0-9a-z]*)", WxThirdAutoReplyHandler),

             # 微信第三方授权入口路径
             (r"/wxtp/oauth",        WxThirdPartyOauthHandler),

             # 微信第三方授权回调事件
             (r"/wxtp/callback",     WxThirdPartyCallbackHandler),

             # 微信第三方授权推送事件
             (r"/wxtp/pushevent",    WxThirdPartyOauthEventHandler),

             # base
             (r"/.*",                IndexHandler)
]