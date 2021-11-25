import os
import time
import random
import datetime
import json
import logging
import base64
from io import BytesIO
import cv2
import numpy as np
import tornado.web
import tornado.gen
import tornado.httpserver
from PIL import Image, ImageDraw
from paddleocr import PaddleOCR, draw_ocr
from jsonencoder import MyEncoder
import log

logger = logging.getLogger(log.LOGGER_ROOT_NAME + '.' + __name__)

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

OCR = {
	"ch_PP-OCRv2_xx": PaddleOCR(lang="ch", det_model_dir=BASE_PATH + "/inference/ch_ppocr_mobile_v2.0_det_infer", cls_model_dir=BASE_PATH+"/inference/ch_ppocr_mobile_v2.0_cls_infer",
			rec_model_dir=BASE_PATH + "/inference/ch_ppocr_mobile_v2.0_rec_infer", use_gpu=False, total_process_num=os.cpu_count(), use_mp=True),

	"ch_ppocr_mobile_v2.0_xx" :  PaddleOCR(lang="ch", det_model_dir=BASE_PATH + "/inference/ch_PP-OCRv2_det_infer", cls_model_dir=BASE_PATH + "/inference/ch_ppocr_mobile_v2.0_cls_infer",
			rec_model_dir=BASE_PATH + "/inference/ch_PP-OCRv2_rec_infer", use_gpu=False, total_process_num=os.cpu_count(), use_mp=True),

	"ch_ppocr_server_v2.0_xx" :  PaddleOCR(lang="ch", det_model_dir=BASE_PATH + "/inference/ch_ppocr_server_v2.0_det_infer", cls_model_dir=BASE_PATH + "/inference/ch_ppocr_mobile_v2.0_cls_infer",
			rec_model_dir=BASE_PATH + "/inference/ch_ppocr_server_v2.0_rec_infer", use_gpu=False, total_process_num=os.cpu_count(), use_mp=True)  
}

class Index(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        self.render(os.path.join(BASE_PATH, 'dist/TrWebOcr_fontend/index.html'))


class PpocrRun(tornado.web.RequestHandler):
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
        MAX_SIZE = 1600

        img_upload = self.request.files.get('file', None)
        img_b64 = self.get_argument('img', None)
        compress_size = self.get_argument('compress', None)
        ocr_model = self.get_argument('ocr_model', 'ch_ppocr_mobile_v2.0_xx')

        # 判断是上传的图片还是base64
        self.set_header('content-type', 'application/json')
        up_image_type = None
        if img_upload is not None and len(img_upload) > 0:
            img_upload = img_upload[0]
            up_image_type = img_upload.content_type
            up_image_name = img_upload.filename
            img = Image.open(BytesIO(img_upload.body))
        elif img_b64 is not None:
            raw_image = base64.b64decode(img_b64.encode('utf8'))
            img = Image.open(BytesIO(raw_image))
        else:
            self.set_status(400)
            logger.error(json.dumps({'code': 400, 'msg': '没有传入参数'}, cls=MyEncoder))
            self.finish(json.dumps({'code': 400, 'msg': '没有传入参数'}, cls=MyEncoder))
            return

        try:
            if hasattr(img, '_getexif') and img._getexif() is not None:
                orientation = 274
                exif = dict(img._getexif().items())
                if orientation in exif:
                    if exif[orientation] == 3:
                        img = img.rotate(180, expand=True)
                    elif exif[orientation] == 6:
                        img = img.rotate(270, expand=True)
                    elif exif[orientation] == 8:
                        img = img.rotate(90, expand=True)
        except Exception as ex:
            error_log = json.dumps({'code': 400, 'msg': '产生了一点错误，请检查日志', 'err': str(ex)}, cls=MyEncoder)
            logger.error(error_log, exc_info=True)
            self.finish(error_log)
            return
        img = img.convert("RGB")

        '''
        是否开启图片压缩
        默认为1600px
        值为 0 时表示不开启压缩
        非 0 时则压缩到该值的大小
        '''
        if compress_size is not None:
            try:
                compress_size = int(compress_size)
            except ValueError as ex:
                logger.error(exc_info=True)
                self.finish(json.dumps({'code': 400, 'msg': 'compress参数类型有误，只能是int类型'}, cls=MyEncoder))
                return

            if compress_size < 1:
                MAX_SIZE = max(img.height, img.width)
            else:
                MAX_SIZE = compress_size

        if img.height > MAX_SIZE or img.width > MAX_SIZE:
            scale = max(img.height / MAX_SIZE, img.width / MAX_SIZE)

            new_width = int(img.width / scale + 0.5)
            new_height = int(img.height / scale + 0.5)
            img = img.resize((new_width, new_height), Image.ANTIALIAS)

        ocr = OCR.get(ocr_model, OCR['ch_ppocr_mobile_v2.0_xx'])
        res = ocr.ocr(np.array(img), cls=False)

        img_detected = img.copy()

        img_draw = ImageDraw.Draw(img_detected)
        colors = ['red', 'green', 'blue', "purple"]

        for line in res:
            points = [tuple(point) for point in line[0]]
            points.append(points[0])
            #img_draw.polygon(points, outline=colors[random.randint(0, len(colors) - 1)])
            img_draw.line(points, width=4, fill=colors[random.randint(0, len(colors) - 1)])

        output_buffer = BytesIO()
        img_detected.save(output_buffer, format='JPEG')
        byte_data = output_buffer.getvalue()
        img_detected_b64 = base64.b64encode(byte_data).decode('utf8')

        log_info = {
            'ip': self.request.host,
            'return': res,
            'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        logger.info(json.dumps(log_info, cls=MyEncoder, ensure_ascii=False))
        self.finish(json.dumps(
            {'code': 200, 'msg': '成功',
             'data': {'img_detected': 'data:image/jpeg;base64,' + img_detected_b64, 'raw_out': list(map(lambda x: [x[0], x[1][0], x[1][1]], res)),
                      'speed_time': round(time.time() - start_time, 2)}},
            cls=MyEncoder, ensure_ascii=False))
        return

