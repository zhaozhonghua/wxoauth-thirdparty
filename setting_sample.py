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
settings['component_app_id'] = '1'
settings['component_app_secret'] = '1'
settings['component_encodingAESKey'] = '1'
settings['component_token'] = '1'