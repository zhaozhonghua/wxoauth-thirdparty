# -*- coding: utf-8 -*-
"""
配置信息 样本
"""
from tornado.options import define

define("port", default=9000, help="run on the given port", type=int)

settings = {}

# system settings
settings['xsrf_cookies'] = True
settings['cookie_secret'] = "EEB1C2AB05DDF04D35BADFDF776DD4B0"
settings['debug'] = True
settings["login_url"] = "/"

# system path
settings['template_path'] = "template"
settings['static_path'] = "static"

# redis config
settings['redis'] = {
    'host': 'localhost',
    'port': 6379,
    'pass': ''
}

# 第三方应用 需要的key
settings['component_app_id'] = 'wx98aa120730a78275'
settings['component_app_secret'] = '0c79e1fa963cd80cc0be99b20a18faeb'
settings['component_encodingAESKey'] = 'YhwSCu0CGkfeaHaAE9XHXfxeX2P0r5skvlDEl1pVK2a'
settings['component_token'] = 'c37f1cd03cb111e5a2be00163e004a1f'