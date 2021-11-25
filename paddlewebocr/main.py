import os
import sys
import logging
from tornado.options import define, options
import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.web import StaticFileHandler

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

import log
from webhandler import PpocrRun
from webhandler import Index


logger = logging.getLogger(log.LOGGER_ROOT_NAME + '.' + __name__)

current_path = os.path.dirname(__file__)
settings = dict(
    static_path=os.path.join(current_path, "dist/TrWebOcr_fontend")  # 配置静态文件路径
)


def make_app():

    return tornado.web.Application([
        (r"/api/tr-run/", PpocrRun),
        (r"/", Index),
        (r"/(.*)", StaticFileHandler,
         {"path": os.path.join(current_path, "dist/TrWebOcr_fontend"), "default_filename": "index.html"}),

    ], **settings)


if __name__ == "__main__":
    define("port", default=8080, type=int, help='指定运行时端口号')
    tornado.options.parse_command_line()
    port = options.port

    app = make_app()

    server = tornado.httpserver.HTTPServer(app)
    server.bind(port)
    server.start(1)
    print(f'Server is running: http://0.0.0.0:{port}')

    # tornado.ioloop.IOLoop.instance().start()
    tornado.ioloop.IOLoop.current().start()
