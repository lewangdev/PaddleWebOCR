import os
from paddleocr import PaddleOCR
from PIL import Image
import numpy as np


OCR = {
    "chinese_cht_mobile_v2.0": PaddleOCR(lang="chinese_cht",
                                         det_model_dir="./inference/ch_ppocr_mobile_v2.0_det_infer",
                                         cls_model_dir="./inference/ch_ppocr_mobile_v2.0_cls_infer",
                                         rec_model_dir="./inference/chinese_cht_mobile_v2.0_rec_infer",
                                         use_gpu=False, total_process_num=os.cpu_count(), use_mp=True, show_log=False),
    "ch_ppocr_mobile_v2.0_xx": PaddleOCR(lang="ch",
                                         det_model_dir="./inference/ch_ppocr_mobile_v2.0_det_infer",
                                         cls_model_dir="./inference/ch_ppocr_mobile_v2.0_cls_infer",
                                         rec_model_dir="./inference/ch_ppocr_mobile_v2.0_rec_infer",
                                         use_gpu=False, total_process_num=os.cpu_count(), use_mp=True, show_log=False),
    "ch_PP-OCRv2_xx":  PaddleOCR(lang="ch",
                                 det_model_dir="./inference/ch_PP-OCRv2_det_infer",
                                 cls_model_dir="./inference/ch_ppocr_mobile_v2.0_cls_infer",
                                 rec_model_dir="./inference/ch_PP-OCRv2_rec_infer",
                                 use_gpu=False, total_process_num=os.cpu_count(), use_mp=True, show_log=False),
    "ch_ppocr_server_v2.0_xx":  PaddleOCR(lang="ch",
                                          det_model_dir="./inference/ch_ppocr_server_v2.0_det_infer",
                                          cls_model_dir="./inference/ch_ppocr_mobile_v2.0_cls_infer",
                                          rec_model_dir="./inference/ch_ppocr_server_v2.0_rec_infer",
                                          use_gpu=False, total_process_num=os.cpu_count(), use_mp=True, show_log=False)
}


def text_ocr(img: Image, ocr_model: str):
    ocr = OCR.get(ocr_model, OCR["ch_ppocr_mobile_v2.0_xx"])
    return ocr.ocr(np.array(img), cls=False)
