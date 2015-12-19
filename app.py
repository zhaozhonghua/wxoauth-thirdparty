# -*- coding: utf-8 -*-
"""
app.py

"""
import tornado.httpserver
import tornado.ioloop
import tornado.web
import logging
import redis

from tornado.options import options
from route import routes

try:
    from setting import settings
except:
    from setting_sample import settings

class Application(tornado.web.Application):

    def __init__(self):
        tornado.web.Application.__init__(self, routes, **settings)

        # 将配置写入self
        self.settings = settings

        # redis client
        if settings['redis']['pass']:
            self.redis = redis.StrictRedis(
                host=settings['redis']['host'],
                port=settings['redis']['port'],
                password=settings['redis']['pass']
            )
        else:
            self.redis = redis.StrictRedis(
                host=settings['redis']['host'],
                port=settings['redis']['port']
            )

def main():

    tornado.options.parse_command_line()

    logging.info('Wxthirdparty Oauth Server Starting...')

    application = Application()
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)

    http_server.listen(options.port)

    try:
        tornado.ioloop.IOLoop.instance().start()

    except Exception, e:
        logging.error(e)

    finally:
        application.redis.disconnect()

        logging.info("Wxthirdparty Oauth Server Shutdown...")

if __name__ == "__main__":
    main()
