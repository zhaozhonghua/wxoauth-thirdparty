# -*- coding: utf-8 -*-

import json
import logging
from tornado import gen
import tornado.httpclient
from tornado.httputil import url_concat

class BaseApi:

    def __init__(self):

        self.http_client = tornado.httpclient.AsyncHTTPClient()

    @gen.coroutine
    def async_http_get_ori(self, url, params={}, timeout=5):
        """
        usage: 异步请求Get
        @gen.coroutine
        def get(self):
            data = yield async_http_get_ori("http://www.abc.com/api/data")
            self.write(data)
        """
        # build query string with url
        url = url_concat(url, params)
        logging.debug("jdata:{0}".format(url))

        data = yield self.http_client.fetch(url, request_timeout=timeout)

        retVal = json.loads(data.body)
        logging.debug("jdata res: {0}".format(retVal))

        # raise back
        raise gen.Return(retVal)

    @gen.coroutine
    def async_http_post_ori(self, url, body={}, timeout=5):
        """
        usage: 异步请求Post
        @gen.coroutine
        def post(self):
            data = yield async_http_post_ori("http://www.abc.com/api/data", {'name': 'kikodo'})
            self.write(data)
        """
        logging.debug("jdata:{0}, {1}".format(url, body))

        response = yield self.http_client.fetch(url, method="POST", body=body, request_timeout=timeout)

        data = json.loads(response.body)
        logging.debug("response: {0}".format(data))

        raise gen.Return(data)