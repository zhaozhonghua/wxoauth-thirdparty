# -*- coding: utf-8 -*-
"""
BaseHandler
"""
import tornado.web
import importlib
import logging

from tornado import gen

class BaseHandler(tornado.web.RequestHandler):

    @property
    def redis(self):
        return self.application.redis

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)

        # instance all service
        thirdparty_mod             = importlib.import_module('api.{0}'.format('thirdparty'))

        self.thirdparyOauthApi = getattr(thirdparty_mod, 'ThirdparyOauthApi')()

    @gen.coroutine
    def get_current_user(self):
        """
        目前还未用到用户，默认为None
        :return:
        """
        user = None
        raise gen.Return(user)

    def write_error(self, status_code, **kwargs):
        """
        页面出错提示
        :param status_code:
        :param kwargs:
        :return:
        """
        if status_code == 404:
            self.render('error/404.html')
        elif status_code == 500:
            self.render('error/500.html')
        else:
            self.render('error/500.html')

        logging.error("status_code : {0}, kwargs : {1}".format(status_code, str(kwargs)))

    def get(self):
        self.write({'status': 1, 'message': 'not supported'})

    def post(self):
        self.write({'status': 1, 'message': 'not supported'})

    def put(self):
        self.write({'status': 1, 'message': 'not supported'})

    def delete(self):
        self.write({'status': 1, 'message': 'not supported'})

    def options(self):
        self.post()

    @gen.coroutine
    def prepare(self):
        """
        设置current_user
        :return:
        """
        self._current_user = yield self.get_current_user()

class IndexHandler(BaseHandler):
    """
    页面Index
    """
    @gen.coroutine
    def get(self):
        self.render("thirdparty/index.html")
