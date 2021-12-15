import time
from typing import Optional
from fastapi import APIRouter, File, UploadFile
from util import *
from ocr import text_ocr

router = APIRouter()


@router.post('/ocr')
async def ocr(img_upload: Optional[UploadFile] = File(...),
              img_b64: Optional[str] = None,
              compress_size: Optional[int] = 0,
              ocr_model: Optional[str] = 'ch_ppocr_mobile_v2.0_xx'):
    start_time = time.time()

    if img_upload is not None and len(img_upload) > 0:
        img_upload = img_upload[0]
        img = convert_bytes_to_image(img_upload.body)
    elif img_b64 is not None:
        img = convert_b64_to_image(img_b64)
    else:
        return {'code': 400, 'msg': '没有传入参数'}

    try:
        img = rotate_image(img)
    except Exception as ex:
        return {'code': 400, 'msg': '产生了一点错误，请检查日志', 'err': str(ex)}

    img = img.convert("RGB")
    img = compress_image(img, compress_size)

    texts = text_ocr(img, ocr_model)
    img_drawed = draw_box_on_image(img.copy(), texts)
    img_drawed_b64 = convert_image_to_b64(img_drawed)

    return {'code': 200, 'msg': '成功',
            'data': {'img_detected': 'data:image/jpeg;base64,' + img_drawed_b64,
                     'raw_out': list(map(lambda x: [x[0], x[1][0], x[1][1]], texts)),
                     'speed_time': round(time.time() - start_time, 2)}}
