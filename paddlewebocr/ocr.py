import os
from paddleocr import PaddleOCR
from PIL import Image
import numpy as np

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

OCR = {
    "chinese_cht_mobile_v2.0": PaddleOCR(lang="chinese_cht",
                                         det_model_dir=BASE_PATH + "/inference/ch_ppocr_mobile_v2.0_det_infer",
                                         cls_model_dir=BASE_PATH+"/inference/ch_ppocr_mobile_v2.0_cls_infer",
                                         rec_model_dir=BASE_PATH + "/inference/chinese_cht_mobile_v2.0_rec_infer",
                                         use_gpu=False, total_process_num=os.cpu_count(), use_mp=True),
    "ch_ppocr_mobile_v2.0_xx": PaddleOCR(lang="ch",
                                         det_model_dir=BASE_PATH + "/inference/ch_ppocr_mobile_v2.0_det_infer",
                                         cls_model_dir=BASE_PATH+"/inference/ch_ppocr_mobile_v2.0_cls_infer",
                                         rec_model_dir=BASE_PATH + "/inference/ch_ppocr_mobile_v2.0_rec_infer",
                                         use_gpu=False, total_process_num=os.cpu_count(), use_mp=True),
    "ch_PP-OCRv2_xx":  PaddleOCR(lang="ch",
                                 det_model_dir=BASE_PATH + "/inference/ch_PP-OCRv2_det_infer",
                                 cls_model_dir=BASE_PATH + "/inference/ch_ppocr_mobile_v2.0_cls_infer",
                                 rec_model_dir=BASE_PATH + "/inference/ch_PP-OCRv2_rec_infer",
                                 use_gpu=False, total_process_num=os.cpu_count(), use_mp=True),
    "ch_ppocr_server_v2.0_xx":  PaddleOCR(lang="ch",
                                          det_model_dir=BASE_PATH + "/inference/ch_ppocr_server_v2.0_det_infer",
                                          cls_model_dir=BASE_PATH + "/inference/ch_ppocr_mobile_v2.0_cls_infer",
                                          rec_model_dir=BASE_PATH + "/inference/ch_ppocr_server_v2.0_rec_infer",
                                          use_gpu=False, total_process_num=os.cpu_count(), use_mp=True)
}


def text_ocr(img: Image, ocr_model: str):
    ocr = OCR.get(ocr_model, OCR['ch_ppocr_mobile_v2.0_xx'])
    return ocr.ocr(np.array(img), cls=False)
