import log
import os
import sys
import logging
from tornado.options import define, options
import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.web import StaticFileHandler
from webhandler import IndexHandler, OcrHandler

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_PATH)


logger = logging.getLogger(log.LOGGER_ROOT_NAME + '.' + __name__)

current_path = os.path.dirname(__file__)
settings = dict(
    static_path=os.path.join(current_path, "..", "webui", "dist")
)


def make_app():
    return tornado.web.Application([
        (r"/api/ocr", OcrHandler),
        (r"/", IndexHandler),
        (r"/(.*)", StaticFileHandler,
         {"path": os.path.join(current_path, "..", "webui", "dist"), "default_filename": "index.html"}),

    ], **settings)


if __name__ == "__main__":
    define("addr", default='0.0.0.0', type=str, help='指定运行时绑定的地址')
    define("port", default=8080, type=int, help='指定运行时端口号')
    tornado.options.parse_command_line()
    port = options.port
    addr = options.addr
    app = make_app()
    app.listen(port, addr)
    logger.info("Application is running on: http://%s:%s/" % (addr, port))
    tornado.ioloop.IOLoop.current().start()
