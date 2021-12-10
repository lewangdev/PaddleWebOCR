import os
import time
import datetime
import json
import logging
import tornado.web
import tornado.gen
import tornado.httpserver
from jsonencoder import MyEncoder
from util import *
from ocr import text_ocr
import log

logger = logging.getLogger(log.LOGGER_ROOT_NAME + '.' + __name__)


class IndexHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        self.render('../webui/dist/index.html')


class OcrHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_status(404)
        self.write("404 : Please use POST")

    @tornado.gen.coroutine
    def post(self):
        '''
        :return:
        报错：
        400 没有请求参数
        '''
        start_time = time.time()
        img_upload = self.request.files.get('file', None)
        img_b64 = self.get_argument('img', None)
        compress_size = self.get_argument('compress', None)
        ocr_model = self.get_argument('ocr_model', 'ch_ppocr_mobile_v2.0_xx')

        # check params
        if compress_size is not None:
            try:
                compress_size = int(compress_size)
            except ValueError as ex:
                logger.error(exc_info=True)
                self.finish(json.dumps(
                    {'code': 400, 'msg': 'compress参数类型有误，只能是int类型'}, cls=MyEncoder))
                return

        self.set_header('content-type', 'application/json')

        # 判断是上传的图片还是 base64
        if img_upload is not None and len(img_upload) > 0:
            img_upload = img_upload[0]
            img = convert_bytes_to_image(img_upload.body)
        elif img_b64 is not None:
            img = convert_b64_to_image(img_b64)
        else:
            self.set_status(400)
            logger.error(json.dumps(
                {'code': 400, 'msg': '没有传入参数'}, cls=MyEncoder))
            self.finish(json.dumps(
                {'code': 400, 'msg': '没有传入参数'}, cls=MyEncoder))
            return

        try:
            img = rotate_image(img)
        except Exception as ex:
            error_log = json.dumps(
                {'code': 400, 'msg': '产生了一点错误，请检查日志', 'err': str(ex)}, cls=MyEncoder)
            logger.error(error_log, exc_info=True)
            self.finish(error_log)
            return

        img = img.convert("RGB")
        img = compress_image(img, compress_size)

        texts = text_ocr(img, ocr_model)
        img_drawed = draw_rectange_on_image(img.copy(), texts)
        img_drawed_b64 = convert_image_to_b64(img_drawed)

        log_info = {
            'ip': self.request.host,
            'texts': texts,
            'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        logger.info(json.dumps(log_info, cls=MyEncoder, ensure_ascii=False))
        self.finish(json.dumps(
            {'code': 200, 'msg': '成功',
             'data': {'img_detected': 'data:image/jpeg;base64,' + img_drawed_b64,
                      'raw_out': list(map(lambda x: [x[0], x[1][0], x[1][1]], texts)),
                      'speed_time': round(time.time() - start_time, 2)}},
            cls=MyEncoder, ensure_ascii=False))
        return
