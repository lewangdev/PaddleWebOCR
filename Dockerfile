FROM nodejs as nodejsbuilder
FROM gcc:8.2.0-centos7 as gccbuilder
FROM python:3.7-centos7

COPY --from=gccbuilder /usr/local/gcc-8.2.0 /usr/local/gcc-8.2.0

ENV LD_LIBRARY_PATH=/usr/local/gcc-8.2.0/lib64:${LD_LIBRARY_PATH}

RUN yum install -y \
	    gmp-devel \
	    mpfr-devel \
	    libmpc-devel

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -i https://mirror.baidu.com/pypi/simple/  \
        --no-cache-dir \
        -r requirements.txt

ADD https://paddleocr.bj.bcebos.com/PP-OCRv2/chinese/ch_PP-OCRv2_det_infer.tar inference/
ADD https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar inference/
ADD https://paddleocr.bj.bcebos.com/PP-OCRv2/chinese/ch_PP-OCRv2_rec_infer.tar inference/
ADD https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_det_infer.tar inference/
ADD https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar inference/
ADD https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_rec_infer.tar inference/
ADD https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_server_v2.0_det_infer.tar inference/
ADD https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar inference/
ADD https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_server_v2.0_rec_infer.tar	inference/
ADD https://paddleocr.bj.bcebos.com/dygraph_v2.0/multilingual/chinese_cht_mobile_v2.0_rec_infer.tar inference/

COPY paddlewebocr paddlewebocr

COPY --from=nodejsbuilder /app/dist webui/dist

COPY docker-entrypoint.sh /usr/local/bin/

ENTRYPOINT ["docker-entrypoint.sh"]

EXPOSE 8080

VOLUME /app/logs

CMD ["python", "paddlewebocr/main.py"]
